"""Export the J04 packaging studies as checked, binary, millimetre STL files.

Run from the repository with runtime/cad/venv/bin/python. No viewer is launched.
ASSUMES: the source solids have outward face winding, as supplied by build123d.
Signed volume is checked for every written component, including reflected legs.
The separate envelopes retain the study's overlaps; these are viewing meshes.
"""
import sys
sys.dont_write_bytecode = True

from collections import OrderedDict
import hashlib
import json
import math
from pathlib import Path
import struct

import build123d as cad
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRepTools import BRepTools
import joint_cartridge as jc
import leg_packaging as lp
import leg_animation as la

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'models'
SOURCE_FILES = (Path(__file__), HERE/'joint_cartridge.py', HERE/'leg_packaging.py',
                HERE/'leg_animation.py', HERE/'j04-c01.example.json', la.PARAMETERS)
MAX_BYTES = 5_000_000
BBOX_TOLERANCE_MM = 0.5
# A finite fallback ladder; each trial uses a fresh CAD build to avoid cached meshes.
TESSELLATIONS = ((0.25, 0.2), (0.5, 0.3), (1.0, 0.4))
TRIANGLE = struct.Struct('<12fH')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes():
    return {str(p.relative_to(HERE.parent)): sha(p) for p in SOURCE_FILES}


def specifications():
    """Each component has its posed FL solid and its animation XY reflection."""
    cartridge = jc.build(jc.read_parameters(HERE/'j04-c01.example.json'))
    # Local shaft Z -> body X, local link +Y -> world +Z: base horizontal below it.
    upright = cad.Plane(origin=(0, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    cartridge = [(name, upright*shape, 1, 1) for name, shape in cartridge.items()]
    result = OrderedDict()
    result['joint-cartridge.stl'] = dict(
        description='J04-C01 joint cartridge, all six assembly solids',
        components=cartridge, stance=None, variant=None,
        orientation='Z up; original local (x, y, z) maps to world (z, x, y)',
        parameters='cad/j04-c01.example.json')
    for variant, filename in [('direct', 'leg-direct-knee.stl'),
                              ('proximal', 'leg-belt-knee.stl')]:
        p, v = lp.read_parameters(la.PARAMETERS, variant)
        model = lp.Model(p, v).build()
        posed = model.pose(**p['poses']['stance'])
        # Same prototype leaves and shared-part rule as leg_animation.main().
        leg = [(n, posed[n], 1, 1) for n in lp.leg_names(model)]
        result[filename] = dict(
            description=('Front-left leg, placement A, '+
                         ('direct knee' if v == 'direct' else 'belt knee and transmission envelopes')+
                         ', with cradle'),
            components=[('cradle', posed['cradle'], 1, 1)]+leg,
            stance=p['poses']['stance'], variant=v,
            orientation='Source body frame: +X forward, +Y left, +Z up',
            parameters='cad/'+la.PARAMETERS.name)
        if v == 'direct':
            four = [('body_envelope', posed['body_envelope'], 1, 1),
                    ('cradle', posed['cradle'], 1, 1)]
            for label, (sx, sy, _) in la.LEGS.items():
                four += [(label+'_'+n, shape, sx, sy) for n, shape, _, _ in leg]
            full = dict(description='Prototype body box, cradle and four direct-knee legs at stance',
                        components=four, stance=p['poses']['stance'], variant=v,
                        orientation='Source body frame: +X forward, +Y left, +Z up',
                        parameters='cad/'+la.PARAMETERS.name)
    result['mack-four-legs-prototype.stl'] = full
    # Independent CAD bounds: reflect BReps, rather than the exported mesh vertices.
    for spec in result.values():
        shapes = []
        for _, shape, sx, sy in spec['components']:
            if sx < 0:
                shape = shape.mirror(cad.Plane.YZ)
            if sy < 0:
                shape = shape.mirror(cad.Plane.XZ)
            shapes.append(shape)
        spec['model_bbox_mm'] = lp.extents(shapes)
    return result


def float32(value):
    # Remove CAD roundoff at the origin before writing IEEE-754 binary32 vertices.
    return struct.unpack('<f', struct.pack('<f', 0. if abs(value) < 1e-9 else value))[0]


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def geometry(points):
    a, b, c = points
    normal = cross([b[i]-a[i] for i in range(3)], [c[i]-a[i] for i in range(3)])
    length = math.sqrt(sum(x*x for x in normal))
    if not math.isfinite(length) or length <= 1e-12:
        raise ValueError('Zero-area or nonfinite triangle')
    normal = tuple(x/length for x in normal)
    volume = sum(a[i]*cross(b, c)[i] for i in range(3))/6
    return normal, volume


def encode(spec, tolerance, angular):
    records, components = bytearray(), []
    count = 0
    for name, shape, sx, sy in spec['components']:
        # build123d.mesh() defaults to relative deflection. Pre-mesh explicitly in
        # absolute millimetres so the recorded linear tolerance means what it says.
        BRepTools.Clean_s(shape.wrapped)
        BRepMesh_IncrementalMesh(shape.wrapped, tolerance, False, angular, True)
        vertices, triangles = shape.tessellate(tolerance, angular)
        points = [(float32(v.X*sx), float32(v.Y*sy), float32(v.Z)) for v in vertices]
        start = count
        for i, j, k in triangles:
            # A single-axis reflection has negative determinant and reverses winding.
            if sx*sy < 0:
                j, k = k, j
            p = [points[i], points[j], points[k]]
            normal, _ = geometry(p)
            records.extend(TRIANGLE.pack(*normal, *p[0], *p[1], *p[2], 0))
            count += 1
        components.append(dict(name=name, first_triangle=start, triangle_count=count-start,
                               model_volume_mm3=shape.volume, reflection_xy=[sx, sy],
                               winding_reversed=sx*sy < 0))
    header = b'J04 packaging study | mm | Z up | example envelopes | not for manufacture'
    return header.ljust(80, b' ')+struct.pack('<I', count)+records, components


def inspect_stl(path, spec, components):
    """Re-read only the file bytes for mesh bounds, normals, counts and volumes."""
    data = path.read_bytes()
    if len(data) < 84:
        raise ValueError(f'{path.name}: truncated binary STL header')
    count = struct.unpack_from('<I', data, 80)[0]
    length_ok = len(data) == 84+50*count
    checks = dict(binary_length=length_ok, under_5_MB=len(data) < MAX_BYTES,
                  at_least_200_triangles=count >= 200)
    if not length_ok:
        raise ValueError(f'{path.name}: binary STL size/header mismatch')
    bounds = {'min': [math.inf]*3, 'max': [-math.inf]*3}
    volumes = []
    normal_errors, degenerate = 0, 0
    for offset in range(84, len(data), 50):
        values = TRIANGLE.unpack_from(data, offset)
        normal, points = values[:3], [values[i:i+3] for i in (3, 6, 9)]
        if not all(math.isfinite(x) for x in values[:12]):
            raise ValueError(f'{path.name}: nonfinite coordinates or normal')
        for p in points:
            for i in range(3):
                bounds['min'][i] = min(bounds['min'][i], p[i])
                bounds['max'][i] = max(bounds['max'][i], p[i])
        try:
            expected, volume = geometry(points)
            normal_errors += int(max(abs(a-b) for a, b in zip(normal, expected)) > 1e-6)
            volumes.append(volume)
        except ValueError:
            degenerate += 1
            volumes.append(0.)
    component_checks = []
    for component in components:
        row = dict(component)
        start, n = row['first_triangle'], row['triangle_count']
        volume = math.fsum(volumes[start:start+n])
        error = abs(volume-row['model_volume_mm3'])/row['model_volume_mm3']
        row.update(signed_mesh_volume_mm3=volume, relative_volume_error=error,
                   outward_winding_passed=volume > 0 and error < .02)
        component_checks.append(row)
    error = max(abs(bounds[end][i]-spec['model_bbox_mm'][end][i])
                for end in ('min', 'max') for i in range(3))
    checks.update(finite_triangles=True, no_zero_area_triangles=degenerate == 0,
                  normals_match_winding=normal_errors == 0,
                  all_components_outward=all(c['outward_winding_passed'] for c in component_checks),
                  stance_bbox_within_0_5_mm=error <= BBOX_TOLERANCE_MM)
    return dict(file=path.name, bytes=len(data), triangle_count=count, sha256=sha(path),
                bbox_mm=bounds, size_mm=lp.sub(bounds['max'], bounds['min']),
                model_bbox_mm=spec['model_bbox_mm'], bbox_max_error_mm=error,
                stance_deg=spec['stance'], knee_variant=spec['variant'],
                orientation=spec['orientation'], parameters=spec['parameters'],
                component_count=len(components), components=component_checks,
                degenerate_triangles=degenerate, normal_errors=normal_errors,
                checks=checks, passed=all(checks.values()))


def write_readme(specs, rows):
    def vector(values):
        return '('+', '.join(f'{v:.2f}' for v in values)+')'
    lines = ['# 3D packaging studies', '', 'Click a file to turn it with the mouse.', '',
             'Packaging-study envelopes with benchmark actuator blocks and example dimensions; nothing built or tested.', '',
             'All models use millimetres with Z up. Bounding boxes list X, Y, Z.', '',
             '| File | What it is | Bounding box in mm (min → max; size) | Triangles |',
             '| --- | --- | --- | ---: |']
    for row in rows:
        b = row['bbox_mm']
        lines.append(f"| [{row['file']}]({row['file']}) | {specs[row['file']]['description']} | "
                     f"{vector(b['min'])} → {vector(b['max'])}; {vector(row['size_mm'])} | {row['triangle_count']:,} |")
    lines += ['', 'Placement A stance: 12° hip spread, −35° hip swing, 70° knee bend. '
              'The example uses a 50 mm upper link for the direct knee and 30 mm for the belt knee.', '',
              'Known study overlaps remain; these separate envelopes are for viewing, not manufacture.', '',
              '[Editable sources](../cad/) · [STEP files](../cad/exports/) · '
              '[Leg packaging study](../leg-packaging.md) · [Mesh checks](models-check.json)', '',
              'Rebuild from the repository root: '
              '`runtime/cad/venv/bin/python hardware/joints/cad/export_models.py`.', '']
    (OUT/'README.md').write_text('\n'.join(lines))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    before = source_hashes()
    report = dict(state='STOPPED', units='mm', up_axis='Z', python=sys.version.split()[0],
                  build123d=cad.__version__, script_sha256=sha(Path(__file__)),
                  source_sha256=before, files=[], failures=[],
                  browser_proof='UNRUN: models not viewed; repository rendering and mouse interaction belong to caller.',
                  scope='Packaging envelopes only; known overlaps retained. No fit, physics, structural or physical testing.')
    try:
        if sys.version_info[:2] != (3, 12) or cad.__version__ != '0.12.0':
            raise ValueError('Requires Python 3.12 and build123d 0.12.0')
        print('Building four Z-up packaging models…', flush=True)
        specs = specifications()
        for index, (name, spec) in enumerate(specs.items(), 1):
            for trial, (tolerance, angular) in enumerate(TESSELLATIONS):
                if trial:
                    spec = specifications()[name]
                data, components = encode(spec, tolerance, angular)
                if len(data) < MAX_BYTES:
                    break
            path = OUT/name
            path.write_bytes(data)
            row = inspect_stl(path, spec, components)
            row['tessellation'] = dict(linear_tolerance_mm=tolerance, angular_tolerance_rad=angular,
                                       deflection_mode='absolute')
            report['files'].append(row)
            if not row['passed']:
                report['failures'].append(name+': '+', '.join(k for k, ok in row['checks'].items() if not ok))
            print(f"{index} of 4 · {name} · {row['bytes']:,} bytes · {row['triangle_count']:,} triangles · "
                  +('PASS' if row['passed'] else 'FAIL'), flush=True)
        report['source_files_unchanged'] = source_hashes() == before
        if not report['source_files_unchanged']:
            report['failures'].append('A source changed during export; rerun from a stable source revision')
        if not report['failures']:
            write_readme(specs, report['files'])
            report['state'] = 'BUILT'
    except Exception as error:
        report['failures'].append(f'{type(error).__name__}: {error}')
    report['passed'] = report['state'] == 'BUILT'
    (OUT/'models-check.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    if report['failures']:
        print('FAIL · '+'; '.join(report['failures']), file=sys.stderr, flush=True)
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

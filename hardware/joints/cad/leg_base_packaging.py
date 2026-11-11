"""J04-L03 rigid base and short-leg packaging envelopes, millimetres/grams/degrees."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys
import time

# Importing the read-only L02 helper must not create an L02 bytecode artifact.
sys.dont_write_bytecode = True
import leg_packaging as old
import build123d as cad

HERE = Path(__file__).resolve().parent
EPS = old.EPS
SCOPE = old.SCOPE
add, sub, mul, norm, cross = old.add, old.sub, old.mul, old.norm, old.cross
rx, ry, bbox, centre = old.rx, old.ry, old.bbox, old.centre
box, cyl, common_volume = old.box, old.cyl, old.common_volume
AXES = ('a', 'b', 'c')
KINDS = ('own_leg', 'base', 'shell', 'neighbour')
MIRRORS = {'FL': (1, 1), 'FR': (1, -1), 'RL': (-1, 1), 'RR': (-1, -1)}
BASE_NAMES = ('base_top_plate', 'base_bottom_plate', 'base_spine')


def read_parameters(path, variant):
    p = json.loads(path.read_text())
    def finite(value, name, positive=False):
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
            raise ValueError(f'{name} must be finite numeric')
        if positive and value <= 0:
            raise ValueError(f'{name} must be positive')
    def visit(value, name='parameters'):
        if isinstance(value, dict):
            for key, child in value.items():
                visit(child, name+'.'+key)
        elif isinstance(value, list):
            for child in value:
                visit(child, name)
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            finite(value, name)
    visit(p)
    positive = {
        'body': ('width_Y', 'depth_X', 'height_Z'),
        'base': ('top_plate_thickness', 'bottom_plate_thickness', 'interior_height',
                 'plate_half_width_Y', 'spine_half_width_X', 'density_g_cm3'),
        'actuator': ('W', 'H', 'D', 'mass_g', 'axis_offset_from_near_end', 'horn_diameter',
                     'horn_height', 'idler_diameter', 'idler_height', 'stall_torque_Nm'),
        'hip': ('d_direct', 'd_proximal', 'carrier_plate_half_span', 'carrier_hub_radius',
                'carrier_neck_half_height'),
        'links': ('L1', 'L2', 'plate_thickness', 'plate_width', 'hub_radius', 'clearance', 'density_g_cm3'),
        'knee': ('pulley_diameter', 'pulley_width', 'belt_thickness', 'belt_mass_g', 'shaft_diameter',
                 'bearing_mass_g', 'pulley_density_g_cm3', 'shaft_density_g_cm3'),
        'foot': ('radius', 'density_g_cm3'),
        'mass_model': ('reference_mass_kg', 'g_m_s2'),
    }
    for section, keys in positive.items():
        for key in keys:
            finite(p[section][key], section+'.'+key, True)
    for section, keys in {'hip': ('j2_dx', 'h2', 'j2_axial_offset'),
                          'base': ('z_top', 'plate_inset_X'),
                          'poses': ('stance_spread_a',)}.items():
        for key in keys:
            finite(p[section][key], section+'.'+key)
    for key in ('hardware_allowance_g_per_joint', 'clearance_floor'):
        finite(p[key], key)
        if p[key] < 0:
            raise ValueError(key+' must be nonnegative')
    for section, key in [('hip', 'P1')]+[('mass_model', key+'_centroid') for key in ('shell', 'payload', 'battery')]:
        values = p[section][key]
        if len(values) != 3:
            raise ValueError(section+'.'+key+' requires three coordinates')
        for value in values:
            finite(value, section+'.'+key)
    for key in ('shell_g', 'payload_g', 'battery_g'):
        finite(p['mass_model'][key], 'mass_model.'+key)
        if p['mass_model'][key] < 0:
            raise ValueError('Mass cannot be negative')
    h, ac, base, links = [p[key] for key in ('hip', 'actuator', 'base', 'links')]
    if h['P1'][1] == 0 or h['j1_horn_dir'] not in ('+X', '-X'):
        raise ValueError('P1 must define an outboard sign and J1 horn must face +/-X')
    fixed = [(h['j1_case_long_dir'], 'inboard'), (h['j2_case_long_dir'], 'rearward'),
             (h['j2_horn_dir'], 'outboard'), (h['j2_axial_offset'], 0),
             (p['knee']['direct_case_frame'], 'lower'), (p['knee']['direct_case_long_dir'], 'down'),
             (p['knee']['horn_dir'], 'outboard'), (p['knee']['proximal_mount_side'], 'outboard')]
    if any(value != required for value, required in fixed):
        raise ValueError('Unsupported actuator orientation for the L03 construction')
    if ac['axis_offset_from_near_end'] >= ac['H'] or ac['horn_height'] != ac['idler_height']:
        raise ValueError('Axis offset must be inside case H and boss heights must match')
    if h['carrier_plate_half_span']-links['plate_thickness'] <= ac['D']/2+ac['horn_height']:
        raise ValueError('Carrier hubs require positive span beyond J1 bosses')
    if base['plate_inset_X'] < 0 or base['plate_inset_X'] >= p['body']['depth_X']/2:
        raise ValueError('Invalid base plate inset')
    if base['spine_half_width_X'] > p['body']['depth_X']/2-base['plate_inset_X']:
        raise ValueError('Base spine exceeds plate footprint')
    if not isinstance(p['neighbors'], bool):
        raise ValueError('neighbors must be boolean')
    bearing = p['knee']['bearing_id_od_w']
    if len(bearing) != 3:
        raise ValueError('bearing_id_od_w requires ID, OD, width')
    for value in bearing:
        finite(value, 'bearing_id_od_w', True)
    if not 0 < bearing[0] < bearing[1] < 2*links['hub_radius']:
        raise ValueError('Bearing requires ID < OD < hub diameter')
    if variant == 'proximal' and p['knee']['shaft_diameter'] > bearing[0]:
        raise ValueError('Proximal shaft exceeds bearing ID')
    requirement = p['requirements']['under_shell_height_mm']
    for key in ('target', 'min', 'max'):
        finite(requirement[key], 'under_shell_height_mm.'+key, True)
    if not requirement['min'] <= requirement['target'] <= requirement['max']:
        raise ValueError('Requirement must have min <= target <= max')
    for height in p['poses']['height_sweep_mm']:
        finite(height, 'height_sweep_mm', True)
    count = 1
    for axis in AXES:
        finite(p['poses']['reference_pose'][axis], 'reference_pose.'+axis)
        values = p['poses']['sweep'][axis]
        if len(values) != 3:
            raise ValueError('Sweep requires min, max, step')
        for value in values:
            finite(value, 'sweep.'+axis)
        if values[0] > values[1] or values[2] <= 0:
            raise ValueError('Sweep requires min <= max and positive step')
        count *= math.ceil((values[1]-values[0])/values[2])+1
    if count > 5000:
        raise ValueError('Sweep bounded to 5000 discrete poses')
    return p


class Model(old.Model):
    def __init__(self, p, variant):
        self.p, self.variant = p, variant
        self.parts, self.meta, self.datums, self.findings = {}, {}, {}, []
        self.P1 = p['hip']['P1']
        self.s = 1 if self.P1[1] > 0 else -1
        self.P2 = add(self.P1, [p['hip']['j2_dx'], self.s*p['hip']['d_'+variant], -p['hip']['h2']])
        self.P3 = add(self.P2, [0, 0, -p['links']['L1']])
        self.P4 = add(self.P3, [0, 0, -p['links']['L2']])
        self.P5 = add(self.P4, [0, 0, -p['foot']['radius']])
        self.axes = [cad.Axis(self.P1, (1, 0, 0)), cad.Axis(self.P2, (0, 1, 0)), cad.Axis(self.P3, (0, 1, 0))]

    def direction(self, word):
        if word == 'rearward':
            return [-1, 0, 0]
        return super().direction(word)

    def put(self, name, shape, frame, mass_class='polymer', fixed_mass=None, color=None):
        if not shape.is_valid or len(shape.solids()) != 1 or shape.volume <= 0:
            raise ValueError(f'{name}: invalid, empty or multi-solid part')
        shape = shape.solids()[0]
        shape.label = name
        colors = old.COLORS
        color = color or colors['foot' if name == 'foot' else 'actuator' if mass_class in ('actuator', 'boss')
                                else 'steel' if mass_class in ('steel', 'pulley', 'bearing', 'belt') else frame]
        shape.color = cad.Color(color)
        densities = {'polymer': self.p['links']['density_g_cm3'], 'base': self.p['base']['density_g_cm3'],
                     'foot': self.p['foot']['density_g_cm3'], 'steel': self.p['knee']['shaft_density_g_cm3'],
                     'pulley': self.p['knee']['pulley_density_g_cm3']}
        mass = shape.volume*densities.get(mass_class, 0)/1000 if fixed_mass is None else fixed_mass
        self.parts[name] = shape
        self.meta[name] = {'name': name, 'frame': frame, 'mass_class': mass_class, 'mass_g': mass,
                           'volume_mm3': shape.volume, 'centroid_mm': centre(shape), 'color': color}
        return shape

    def chain(self, a, b, c):
        p2 = add(add(self.P1, [self.p['hip']['j2_dx'], 0, 0]),
                 rx([0, self.s*self.p['hip']['d_'+self.variant], -self.p['hip']['h2']], a))
        p3 = add(p2, rx(ry([0, 0, -self.p['links']['L1']], b), a))
        p4 = add(p3, rx(ry([0, 0, -self.p['links']['L2']], b+c), a))
        return p2, p3, p4

    def foot_axis_point(self, angles, y_offset=0):
        a, b, c = angles
        p4 = self.chain(a, b, c)[2]
        return add(p4, rx(ry([0, y_offset, -self.p['foot']['radius']], b+c), a))

    def build(self):
        p = self.p
        h, l, k, ac, base = [p[key] for key in ('hip', 'links', 'knee', 'actuator', 'base')]
        x1, y1, z1 = self.P1
        x2, y2, z2 = self.P2
        x3, y3, z3 = self.P3
        z4 = self.P4[2]
        tp, half, radius = l['plate_thickness'], h['carrier_plate_half_span'], h['carrier_hub_radius']
        dx, dy = p['body']['depth_X']/2, p['body']['width_Y']/2
        self.put('body_envelope', box(-dx, dx, -dy, dy, 0, p['body']['height_Z']), 'body', 'envelope', 0)
        px, py = dx-base['plate_inset_X'], base['plate_half_width_Y']
        self.base_height = base['top_plate_thickness']+base['interior_height']+base['bottom_plate_thickness']
        top, bottom = base['z_top'], base['z_top']-self.base_height
        self.put('base_top_plate', box(-px, px, -py, py, top-base['top_plate_thickness'], top), 'body', 'base')
        self.put('base_bottom_plate', box(-px, px, -py, py, bottom, bottom+base['bottom_plate_thickness']), 'body', 'base')
        self.put('base_spine', box(-base['spine_half_width_X'], base['spine_half_width_X'], -py, py,
                                  bottom+base['bottom_plate_thickness'], top-base['top_plate_thickness']), 'body', 'base')
        self.actuator('j1_actuator', [1, 0, 0], 'inboard', self.P1, 0, h['j1_horn_dir'], 'body')
        jb = self.datums['j1_actuator']['case_bbox']
        for plate in BASE_NAMES[:2]:
            plate_bounds = bbox(self.parts[plate])
            overlap = min(jb['max'][2], plate_bounds['max'][2])-max(jb['min'][2], plate_bounds['min'][2])
            if overlap > 0:
                self.findings.append({'name': 'j1_case_into_base_plate', 'plate': plate, 'overlap_mm': overlap})
        gap = top-base['top_plate_thickness']-jb['max'][2]
        xlo, xhi = max(-px, jb['min'][0]), min(px, jb['max'][0])
        ylo, yhi = max(-py, jb['min'][1]), min(py, jb['max'][1])
        if gap > 1e-9 and xhi > xlo and yhi > ylo:
            self.put('j1_mount', box(xlo, xhi, ylo, yhi, jb['max'][2], top-base['top_plate_thickness']), 'body')
        self.actuator('j2_actuator', [0, 1, 0], 'rearward', self.P2, 0, 'outboard', 'carrier')
        j2 = self.datums['j2_actuator']
        jb2 = j2['case_bbox']
        for word, side in [('horn', 1 if h['j1_horn_dir'] == '+X' else -1),
                           ('idler', -1 if h['j1_horn_dir'] == '+X' else 1)]:
            xa, xb = sorted([x1+side*(half-tp), x1+side*half])
            near_y = jb2['min'][1] if self.s > 0 else jb2['max'][1]
            plate = (cyl([0, y1, z1], [1, 0, 0], xa, xb, radius)
                     + box(xa, xb, y1, near_y, z1-h['carrier_neck_half_height'], z1+h['carrier_neck_half_height'])
                     + box(xa, xb, jb2['min'][1], jb2['max'][1], z2-ac['W']/2, z2+ac['W']/2))
            self.put('carrier_'+word+'_plate', plate, 'carrier')
            lo, hi = sorted([side*(ac['D']/2+ac['horn_height']), side*(half-tp)])
            self.put('carrier_hub_'+word, cyl(self.P1, [1, 0, 0], lo, hi, radius), 'carrier')
        upper_outer = {}
        for word, side in [('horn', self.s), ('idler', -self.s)]:
            inner = j2[word+'_boss_outer_centre'][1]
            band = sorted([inner, inner+side*tp])
            upper_outer[side] = inner+side*tp
            plate = self.link_plate(self.P2, self.P3, *band)
            if self.variant == 'proximal':
                plate -= cyl([x3, 0, z3], [0, 1, 0], band[0]-1, band[1]+1, k['bearing_id_od_w'][1]/2)
            self.put('upper_'+word+'_plate', plate, 'upper')
        if self.variant == 'direct':
            self.actuator('knee_actuator', [0, 1, 0], 'down', self.P3, 0, 'outboard', 'lower')
            kb = self.datums['knee_actuator']['case_bbox']
            for sign, word in [(1, 'plus'), (-1, 'minus')]:
                xx = x3+sign*(ac['W']/2+tp/2)
                self.put('shank_channel_'+word, box(xx-tp/2, xx+tp/2, kb['min'][1], kb['max'][1],
                                                  z4, z3+ac['axis_offset_from_near_end']), 'lower')
            self.foot_band = [kb['min'][1], kb['max'][1]]
        else:
            self.build_proximal(upper_outer)
        self.put('foot', cyl([self.P5[0], 0, self.P5[2]], [0, 1, 0], *self.foot_band, p['foot']['radius']), 'lower', 'foot')
        self.stance_solution = solve_stance(self, p['requirements']['under_shell_height_mm']['target'])
        self.stance = self.stance_solution['pose_deg']
        if p['neighbors']:
            posed = self.pose(**self.stance)
            for leg in ('FR', 'RL', 'RR'):
                for name in old.leg_names(self):
                    if name.startswith('nb_'):
                        continue
                    shape = mirror_shape(posed[name], leg)
                    self.put('nb_'+leg+'_'+name, shape, 'body', 'neighbor_envelope', 0, self.meta[name]['color'])
        return self

    def build_proximal(self, upper_outer):
        p, tp = self.p, self.p['links']['plate_thickness']
        k, ac, l = [p[key] for key in ('knee', 'actuator', 'links')]
        x2, y2, z2 = self.P2
        x3, y3, z3 = self.P3
        side = self.s
        matching_outer = upper_outer[side]
        offset = matching_outer-y2+side*(ac['horn_height']+ac['D']/2)
        self.actuator('knee_actuator', [0, 1, 0], 'down', self.P2, offset, 'outboard', 'upper')
        knee = self.datums['knee_actuator']
        far_y = knee['case_axis_centre'][1]+side*ac['D']/2
        self.put('knee_mount', box(x2-ac['W']/2, x2+ac['W']/2, matching_outer, far_y,
                                  knee['far_end_point'][2]-tp, knee['far_end_point'][2]), 'upper')
        pulley_inner = knee['horn_boss_outer_centre'][1]
        pulley_outer = pulley_inner+side*k['pulley_width']
        band = sorted([pulley_inner, pulley_outer])
        for name, point in [('pulley_hip', self.P2), ('pulley_knee', self.P3)]:
            self.put(name, cyl([point[0], 0, point[2]], [0, 1, 0], *band, k['pulley_diameter']/2), 'upper', 'pulley')
            self.datums[name] = {'axis_point': [point[0], sum(band)/2, point[2]], 'axis_dir': [0, 1, 0], 'y_band_mm': band}
        self.put('belt', box(x2-k['pulley_diameter']/2, x2+k['pulley_diameter']/2, *band, z3, z2), 'upper', 'belt', k['belt_mass_g'])
        self.put('upper_tie', box(x2-6, x2+6, y2-ac['D']/2-ac['idler_height'], y2+ac['D']/2+ac['horn_height'],
                                 z3-4, z3+4), 'upper')
        bands = []
        for direction in (-1, 1):
            anchor = pulley_outer if direction == side else upper_outer[direction]
            yy = anchor+direction*l['clearance']
            plate_band = sorted([yy, yy+direction*tp])
            bands.append(plate_band)
            self.put('lower_plate_'+('out' if direction == self.s else 'in'),
                     self.link_plate(self.P3, self.P4, *plate_band, end_hub=False), 'lower')
        self.foot_band = [min(v[0] for v in bands), max(v[1] for v in bands)]
        self.put('knee_shaft', cyl([x3, 0, z3], [0, 1, 0], *self.foot_band, k['shaft_diameter']/2), 'upper', 'steel')
        self.datums['knee_shaft'] = {'axis_point': self.P3, 'axis_dir': [0, 1, 0], 'y_band_mm': self.foot_band}
        bi, bo, bw = k['bearing_id_od_w']
        for direction in (-1, 1):
            yy = upper_outer[direction]-direction*tp/2
            band = [yy-bw/2, yy+bw/2]
            ring = (cyl([x3, 0, z3], [0, 1, 0], *band, bo/2)
                    - cyl([x3, 0, z3], [0, 1, 0], band[0]-1, band[1]+1, bi/2))
            self.put('knee_bearing_'+('out' if direction == self.s else 'in'), ring, 'upper', 'bearing', k['bearing_mass_g'])


def mirror_point(point, leg):
    x, y = MIRRORS[leg]
    return [x*point[0], y*point[1], point[2]]


def mirror_shape(shape, leg):
    x, y = MIRRORS[leg]
    if y < 0:
        shape = shape.mirror(cad.Plane.XZ)
    if x < 0:
        shape = shape.mirror(cad.Plane.YZ)
    return shape


def angles_tuple(pose):
    return tuple(pose[axis] for axis in AXES)


def under_shell(m, angles):
    return -bbox(m.transform(m.parts['foot'], 'lower', *angles))['min'][2]


def solve_stance(m, target):
    a = m.p['poses']['stance_spread_a']
    def height(c):
        return under_shell(m, (a, -c/2, c))
    low, high = 0., 130.
    endpoints = [height(low), height(high)]
    reached = min(endpoints)-1e-9 <= target <= max(endpoints)+1e-9
    iterations = 0
    if reached:
        for iterations in range(1, 61):
            mid = (low+high)/2
            value = height(mid)
            if abs(value-target) < 1e-8:
                break
            if (value > target) == (endpoints[0] > endpoints[1]):
                low = mid
            else:
                high = mid
        c = mid
    else:
        c = min((0., 130.), key=lambda angle: abs(height(angle)-target))
    pose = {'a': a, 'b': -c/2, 'c': c}
    actual = height(c)
    return {'target_mm': target, 'pose_deg': pose, 'under_shell_height_mm': actual,
            'stance_reached': reached and abs(actual-target) <= .01,
            'achievable_range_mm': sorted(endpoints), 'endpoint_heights_mm': endpoints,
            'bisection_iterations': iterations, 'error_mm': actual-target,
            'method': 'Bisection c in [0,130], b=-c/2; each height from posed foot BRep bounding box.'}


def pose_checks(m):
    rows = []
    offset = sum(m.foot_band)/2-m.P5[1]
    for angles in old.TEST_POSES:
        actual = centre(m.transform(m.parts['foot'], 'lower', *angles))
        axis_point = m.foot_axis_point(angles)
        expected = m.foot_axis_point(angles, offset)
        rows.append({'pose_deg': angles, 'foot_centroid_mm': actual, 'P5_mm': axis_point,
                     'expected_centroid_mm': expected, 'rigid_formula_error_mm': norm(sub(actual, expected)),
                     'centroid_to_P5_mm': norm(sub(actual, axis_point))})
    return {'tests': rows, 'maximum_error_mm': max(r['rigid_formula_error_mm'] for r in rows),
            'rigid_formula_satisfied': all(r['rigid_formula_error_mm'] < 1e-6 for r in rows),
            'foot_axis_midpoint_offset_Y_mm': offset,
            'maximum_literal_centroid_to_P5_error_mm': max(r['centroid_to_P5_mm'] for r in rows),
            'literal_P5_centroid_satisfied': all(r['centroid_to_P5_mm'] < 1e-6 for r in rows),
            'formula': 'P5=P4+Rx(a)Ry(b+c)(0,0,-radius); centroid=P5+Rx(a)(0,mean(foot Y band)-y2,0).',
            'scope': 'Proximal prescribed foot span is asymmetric about P5. Its axial midpoint offset is included explicitly.'}


def intentional_pairs(m):
    result = old.intentional_pairs(m)
    def skip(x, y, reason):
        if x in m.parts and y in m.parts:
            result[tuple(sorted((x, y)))] = reason
    for word in ('horn', 'idler'):
        skip('upper_'+word+'_plate', 'knee_actuator_'+word, 'Direct knee boss outer face on thigh inner face')
        skip('carrier_'+word+'_plate', 'j2_actuator', 'Carrier inner face on flat J2 case end face')
    skip('knee_shaft', 'upper_tie', 'Nominal shaft through upper tie')
    # The proximal knee is mounted at P2, so its idler is on the upper horn plate.
    if m.variant == 'proximal':
        skip('upper_horn_plate', 'knee_actuator_idler', 'Proximal idler on mounting thigh outer face')
        for word in ('horn', 'idler'):
            result.pop(tuple(sorted(('upper_'+word+'_plate', 'knee_actuator_'+word))), None)
        skip('upper_horn_plate', 'knee_actuator_idler', 'Proximal idler on mounting thigh outer face')
    return result


def pair_kind(x, y):
    if x.startswith('nb_') or y.startswith('nb_'):
        return 'neighbour'
    if 'body_envelope' in (x, y):
        return 'shell'
    if x in BASE_NAMES or y in BASE_NAMES:
        return 'base'
    return 'own_leg'


def moving_pairs(m):
    frames = {frame: [n for n in m.parts if m.meta[n]['frame'] == frame]
              for frame in ('body', 'carrier', 'upper', 'lower')}
    skipped = intentional_pairs(m)
    pairs = []
    for moving, targets in [('carrier', ['body']), ('upper', ['carrier', 'body']), ('lower', ['upper', 'carrier', 'body'])]:
        for x in frames[moving]:
            for frame in targets:
                for y in frames[frame]:
                    if tuple(sorted((x, y))) not in skipped:
                        pairs.append((x, y))
    return pairs


def collisions_at(m, pose):
    posed = m.pose(**pose)
    bounds = {n: bbox(shape) for n, shape in posed.items()}
    rows = []
    counts = dict.fromkeys(KINDS, 0)
    for x, y in moving_pairs(m):
        volume = common_volume(posed[x], posed[y], bounds[x], bounds[y])
        if volume > EPS:
            kind = pair_kind(x, y)
            rows.append({'parts': [x, y], 'kind': kind, 'volume_mm3': volume})
            counts[kind] += 1
    return {'pose_deg': pose, 'counts_by_class': counts, 'colliding_pairs': rows}


def neutral_check(m):
    bounds = {n: bbox(shape) for n, shape in m.parts.items()}
    overlaps, inside = [], []
    for x, y in itertools.combinations(m.parts, 2):
        volume = common_volume(m.parts[x], m.parts[y], bounds[x], bounds[y])
        if volume > EPS:
            overlaps.append({'parts': [x, y], 'volume_mm3': volume,
                             'intentional_contact': intentional_pairs(m).get(tuple(sorted((x, y))))})
    for name in m.parts:
        if name == 'body_envelope':
            continue
        volume = common_volume(m.parts[name], m.parts['body_envelope'], bounds[name], bounds['body_envelope'])
        if volume > EPS:
            common = m.parts[name] & m.parts['body_envelope']
            b = bbox(common)
            inside.append({'parts': [name, 'body_envelope'], 'volume_mm3': volume,
                           'z_range_mm': [b['min'][2], b['max'][2]],
                           'classification': 'unknown shell interior; physical intake question'})
    return overlaps, inside


def sweep(m, quick):
    """L02 exact-volume/distance algorithm with L03's four pair classes."""
    start = time.monotonic()
    grids = {axis: old.grid(m.p['poses']['sweep'][axis], quick) for axis in AXES}
    poses = list(itertools.product(*(grids[axis] for axis in AXES)))
    cache, samples = {}, []
    for angles in poses:
        a, b, c = angles
        sample = {}
        for name, shape in m.parts.items():
            frame = m.meta[name]['frame']
            relevant = {'body': (), 'carrier': (a,), 'upper': (a, b), 'lower': angles}[frame]
            key = name, relevant
            if key not in cache:
                moved = m.transform(shape, frame, *angles)
                cache[key] = moved, bbox(moved)
            sample[name] = cache[key]
        samples.append(sample)
    hits = [dict.fromkeys(KINDS, 0) for _ in poses]
    records = []
    exact_common, exact_distance, reused = 0, 0, 0
    progress = start
    pairs = moving_pairs(m)
    for pair_index, (x, y) in enumerate(pairs):
        kind = pair_kind(x, y)
        record = {'parts': [x, y], 'kind': kind, 'minimum_distance_mm': math.inf,
                  'minimum_distance_pose_deg': None, 'colliding_poses': 0,
                  'colliding_pose_indices': [], 'collision_samples': [], 'maximum_overlap_mm3': 0.}
        fx, fy = m.meta[x]['frame'], m.meta[y]['frame']
        volumes, distances, candidates = {}, {}, []
        for index, (angles, sample) in enumerate(zip(poses, samples)):
            a, b, c = angles
            key = ({'carrier': (a,), 'upper': (a, b), 'lower': angles}[fx] if fy == 'body'
                   else (c,) if fy == 'upper' else (b,) if fx == 'upper' else (b, c))
            sx, bx = sample[x]
            sy, by = sample[y]
            candidates.append((old.bbox_gap(bx, by), index, key))
            if key in volumes:
                volume = volumes[key]
                reused += 1
            else:
                possible = old.boxes_overlap(bx, by)
                volume = common_volume(sx, sy, bx, by) if possible else 0.
                exact_common += int(possible)
                volumes[key] = volume
            if volume > EPS:
                hits[index][kind] += 1
                record['colliding_poses'] += 1
                record['colliding_pose_indices'].append(index)
                record['maximum_overlap_mm3'] = max(record['maximum_overlap_mm3'], volume)
                if record['minimum_distance_pose_deg'] is None:
                    record['minimum_distance_mm'] = 0.
                    record['minimum_distance_pose_deg'] = list(angles)
                if len(record['collision_samples']) < 8:
                    record['collision_samples'].append({'pose_deg': list(angles), 'volume_mm3': volume})
        if not record['colliding_poses']:
            for gap, index, key in sorted(candidates):
                if gap >= record['minimum_distance_mm'] and record['minimum_distance_pose_deg'] is not None:
                    break
                if key in distances:
                    continue
                distance = samples[index][x][0].distance_to(samples[index][y][0])
                distances[key] = distance
                exact_distance += 1
                if distance < record['minimum_distance_mm']:
                    record['minimum_distance_mm'] = distance
                    record['minimum_distance_pose_deg'] = list(poses[index])
        records.append(record)
        now = time.monotonic()
        if pair_index == 0 or now-progress > 15 or pair_index+1 == len(pairs):
            print(f'sweep {pair_index+1}/{len(pairs)} pairs; {len(poses)} poses; {now-start:.1f}s', file=sys.stderr, flush=True)
            progress = now
    clear = [list(angles) for angles, row in zip(poses, hits) if not sum(row.values())]
    clear_no_nb = [list(angles) for angles, row in zip(poses, hits) if not sum(row[k] for k in KINDS[:-1])]
    points = [m.chain(*angles)[2] for angles in poses]
    skipped = intentional_pairs(m)
    result = {'quick': quick, 'grids_deg': grids, 'total_poses': len(poses),
              'colliding_poses': len(poses)-len(clear), 'clear_poses': len(clear),
              'colliding_poses_ignoring_neighbours': len(poses)-len(clear_no_nb),
              'clear_poses_deg': clear, 'clear_poses_ignoring_neighbours_deg': clear_no_nb,
              'pose_table': [{'index': i, 'pose_deg': list(angles), **{k+'_pairs': count for k, count in row.items()}}
                             for i, (angles, row) in enumerate(zip(poses, hits))],
              'pairs': records, 'interferences': [row for row in records if row['colliding_poses']],
              'near_misses': [row for row in records if not row['colliding_poses'] and row['minimum_distance_mm'] < m.p['clearance_floor']],
              'skipped_pairs': [{'parts': list(pair), 'reason': reason} for pair, reason in sorted(skipped.items())],
              'pair_counts_by_class': {kind: {'tested_pairs': sum(row['kind'] == kind for row in records),
                                            'colliding_pairs': sum(row['kind'] == kind and row['colliding_poses'] > 0 for row in records),
                                            'pair_pose_collisions': sum(row['colliding_poses'] for row in records if row['kind'] == kind)}
                                       for kind in KINDS},
              'query_counts': {'exact_common': exact_common, 'exact_distance': exact_distance, 'rigid_invariance_cache_hits': reused},
              'sweep_seconds': time.monotonic()-start, 'scope': SCOPE,
              'distance_method': 'Exact BRep distance, AABB lower-bound pruning. Exact common volume for every potentially overlapping configuration. Rigid invariance reuses exact results.'}
    reach = {'kinematic_only': old.reach_bounds(points),
             'collision_free_subset': old.reach_bounds([point for point, row in zip(points, hits) if not sum(row.values())]),
             'collision_free_ignoring_neighbours': old.reach_bounds([m.chain(*angles)[2] for angles in clear_no_nb])}
    return result, reach


def contact_point(m, pose):
    angles = angles_tuple(pose)
    foot = m.transform(m.parts['foot'], 'lower', *angles)
    endpoints = [m.foot_axis_point(angles, yy-m.P5[1]) for yy in m.foot_band]
    endpoint = (mul(add(*endpoints), .5) if abs(pose['a']) < 1e-12
                else min(endpoints, key=lambda point: point[2]))
    return [m.foot_axis_point(angles)[0], endpoint[1], bbox(foot)['min'][2]]


def static_torque(m, pose, mass_kg):
    contact = contact_point(m, pose)
    p2, p3, _ = m.chain(**pose)
    axes = [[1, 0, 0], rx([0, 1, 0], pose['a']), rx([0, 1, 0], pose['a'])]
    rows = []
    for feet in (4, 3, 2):
        load = mass_kg*m.p['mass_model']['g_m_s2']/feet
        force = [0, 0, load]
        torques = [abs(sum(x*y for x, y in zip(cross(mul(sub(contact, point), .001), force), axis)))
                   for point, axis in zip((m.P1, p2, p3), axes)]
        rows.append({'feet': feet, 'load_per_foot_N': load,
                     'J1_Nm': torques[0], 'J2_Nm': torques[1], 'J3_Nm': torques[2],
                     **{'J'+str(i+1)+'_stall_share': torque/m.p['actuator']['stall_torque_Nm'] for i, torque in enumerate(torques)}})
    return {'mass_kg': mass_kg, 'pose_deg': pose, 'contact_point_mm': contact,
            'axis_points_mm': [m.P1, p2, p3], 'axis_directions': axes, 'rows': rows,
            'method': 'Magnitude of ((contact-axis_point)/1000 cross vertical force) dot posed unit axis. Equal load sharing; external vertical contact force only.'}


def mass_report(m):
    totals = dict.fromkeys(('carrier', 'upper', 'lower', 'foot'), 0.)
    names = old.leg_names(m)
    allowance = m.p['hardware_allowance_g_per_joint']
    angles = angles_tuple(m.stance)
    posed = m.pose(*angles)
    items = []
    for leg in MIRRORS:
        for name in names:
            item = m.meta[name]
            items.append({'name': leg+'_'+name, 'mass_g': item['mass_g'],
                          'centroid_mm': mirror_point(centre(posed[name]), leg), 'mass_class': item['mass_class']})
        p2, p3, _ = m.chain(*angles)
        for joint, point in enumerate((m.P1, p2, p3), 1):
            items.append({'name': leg+'_J'+str(joint)+'_hardware_allowance', 'mass_g': allowance,
                          'centroid_mm': mirror_point(point, leg), 'mass_class': 'hardware_allowance'})
    for name in BASE_NAMES:
        items.append({'name': name, 'mass_g': m.meta[name]['mass_g'], 'centroid_mm': centre(m.parts[name]), 'mass_class': 'base'})
    mm = m.p['mass_model']
    for name in ('shell', 'payload', 'battery'):
        items.append({'name': name, 'mass_g': mm[name+'_g'], 'centroid_mm': mm[name+'_centroid'],
                      'provenance': mm[name+'_provenance'], 'mass_class': 'assumed_payload'})
    for name in names:
        frame = 'carrier' if name.startswith('j1_') else 'foot' if name == 'foot' else m.meta[name]['frame']
        totals[frame] += m.meta[name]['mass_g']
    leg_mass = sum(totals.values())+3*allowance
    total = sum(row['mass_g'] for row in items)
    com = [sum(row['mass_g']*row['centroid_mm'][i] for row in items)/total for i in range(3)]
    moving = [name for name in names if m.meta[name]['frame'] in ('upper', 'lower')]
    inertias = {}
    for label, angles in [('neutral', (0, 0, 0)), ('stance', angles_tuple(m.stance))]:
        shapes = m.pose(*angles)
        p2, p3, _ = m.chain(*angles)
        axis = rx([0, 1, 0], angles[0])
        inertias[label] = sum(m.meta[name]['mass_g']*norm(cross(sub(centre(shapes[name]), p2), axis))**2 for name in moving)
        inertias[label] += allowance*norm(cross(sub(p3, p2), axis))**2
    weighted = [0., 0., 0.]
    fl_items = [row for row in items if row['name'].startswith('FL_')]
    for item in fl_items:
        weighted = add(weighted, mul(item['centroid_mm'], item['mass_g']))
    floor = contact_point(m, m.stance)[2]
    return {'items': items, 'frame_group_g': totals, 'hardware_allowance_g_per_joint': allowance,
            'hardware_allowance_total_g': 3*allowance, 'leg_total_g': leg_mass, 'four_legs_g': 4*leg_mass,
            'base_g': sum(m.meta[name]['mass_g'] for name in BASE_NAMES), 'total_mass_g': total,
            'com_mm': com, 'floor_z_mm': floor, 'com_height_above_floor_mm': com[2]-floor,
            'moving_about_j2_g': sum(m.meta[name]['mass_g'] for name in moving)+allowance,
            'moving_inertia_about_j2_gmm2': inertias, 'leg_centroid_stance_mm': mul(weighted, 1/leg_mass),
            'method': 'Four mirrored legs include each J1 case/boss/mount once, and three allowances at P1/posed P2/posed P3. Base counted once. Inertia is centroid-lumped sum m*r^2, not tensor inertia.',
            'assumptions': 'Masses and positions tagged ASSUMED in the parameters drive CoM and support. Shell 229 g is catalog complete-clock mass, assumed fully retained.'}


def support_report(m, mass):
    cp = contact_point(m, m.stance)
    contacts = {leg: mirror_point(cp, leg) for leg in MIRRORS}
    x, y, _ = mass['com_mm']
    margins = {'margin_front': max(p[0] for p in contacts.values())-x,
               'margin_rear': x-min(p[0] for p in contacts.values()),
               'margin_left': max(p[1] for p in contacts.values())-y,
               'margin_right': y-min(p[1] for p in contacts.values())}
    lifted = []
    for leg in MIRRORS:
        points = [point for name, point in contacts.items() if name != leg]
        cx = sum(point[0] for point in points)/3
        cy = sum(point[1] for point in points)/3
        points.sort(key=lambda point: math.atan2(point[1]-cy, point[0]-cx))
        distances = []
        for a, b in zip(points, points[1:]+points[:1]):
            dx, dy = b[0]-a[0], b[1]-a[1]
            length = math.hypot(dx, dy)
            if length <= 1e-12:
                raise ValueError('Degenerate support triangle from invalid stance parameters')
            distances.append((dx*(y-a[1])-dy*(x-a[0]))/length)
        lifted.append({'lifted_leg': leg, 'signed_margin_mm': min(distances), 'edge_signed_distances_mm': distances})
    height = mass['com_height_above_floor_mm']
    return {'contact_points_mm': contacts, 'four_feet_margins_mm': margins,
            'minimum_margin_mm': min(margins.values()),
            'tip_angle_deg': math.degrees(math.atan2(min(margins.values()), height)),
            'three_feet': lifted, 'com_height_above_floor_mm': height,
            'assumptions': mass['assumptions'],
            'method': 'Rectangle axis-aligned margins. Triangle edges oriented counterclockwise; minimum inward signed perpendicular edge distance, negative outside.'}


def proportions(m, pose):
    posed = m.pose(**pose)
    names = old.leg_names(m)
    all_shapes = [posed[name] for name in BASE_NAMES]
    leg_shapes = []
    hips = []
    for leg in MIRRORS:
        for name in names:
            shape = mirror_shape(posed[name], leg)
            all_shapes.append(shape)
            leg_shapes.append(shape)
            if m.meta[name]['frame'] in ('carrier', 'upper'):
                hips.append(shape)
    # Exact clipped solids give the envelope of geometry below the shell plane.
    bounds = old.extents(all_shapes)
    clip = box(bounds['min'][0]-1, bounds['max'][0]+1, bounds['min'][1]-1, bounds['max'][1]+1,
               bounds['min'][2]-1, 0)
    below = []
    for shape in all_shapes:
        b = bbox(shape)
        if b['min'][2] >= 0:
            continue
        below.append(shape if b['max'][2] <= 0 else shape & clip)
    envelope = old.extents(below)
    hip_bounds = old.extents(hips)
    leg_bounds = old.extents(leg_shapes)
    cp = contact_point(m, pose)
    base_bounds = old.extents(m.parts[name] for name in BASE_NAMES)
    result = {'width_across_hips_mm': 2*max(abs(hip_bounds['min'][1]), abs(hip_bounds['max'][1])),
              'overall_width_mm': envelope['max'][1]-envelope['min'][1],
              'overall_length_mm': envelope['max'][0]-envelope['min'][0],
              'beyond_face_mm': max(0., leg_bounds['max'][0]-m.p['body']['depth_X']/2),
              'track_width_mm': 2*abs(cp[1]), 'wheelbase_mm': 2*abs(cp[0]),
              'base_height_mm': base_bounds['max'][2]-base_bounds['min'][2],
              'base_below_shell_mm': max(0., -base_bounds['min'][2]),
              'inside_shell_mm': max(0., base_bounds['max'][2]), 'below_shell_bbox_mm': envelope,
              'build_target_reference_mm': m.p['requirements']['build_target_reference_mm']}
    ref = result['build_target_reference_mm']
    result['differences_from_build_target_mm'] = {
        'visible_base_below_shell': result['base_below_shell_mm']-ref['visible_base_below_shell'],
        'track_width_at_feet': result['track_width_mm']-ref['track_width_at_feet'],
        'width_across_hips': result['width_across_hips_mm']-ref['width_across_hips']}
    return result


def ground_report(m):
    posed = m.pose(**m.stance)
    floor = bbox(posed['foot'])['min'][2]
    rows = [{'name': name, 'clearance_mm': bbox(posed[name])['min'][2]-floor}
            for name in old.leg_names(m) if name != 'foot']
    lowest = min(rows, key=lambda row: row['clearance_mm'])
    negative = [row for row in rows if row['clearance_mm'] < 0]
    return {'floor_z_mm': floor, 'clearances': rows, 'ground_contact_ok': not negative,
            'below_floor': negative, 'lowest_nonfoot_solid': lowest}


def independent_estimates(m, requirement, heights):
    if m.variant != 'direct':
        return {'scope': 'Brief estimates apply to direct variant only.'}
    p2 = m.chain(12, 0, 0)[0]
    reference = under_shell(m, angles_tuple(m.p['poses']['reference_pose']))
    knee70 = next(row['pose_deg']['c'] for row in heights if row['target_mm'] == 70.)
    estimates = [('stance_b_deg', -50.6, m.stance['b'], 1.5), ('stance_c_deg', 101.2, m.stance['c'], 1.5),
                 ('straight_under_shell_mm', 78.2, requirement['straight_leg_under_shell_mm'], 1.5),
                 ('reference_under_shell_mm', 66.7, reference, 1.5), ('height70_c_deg', 59., knee70, 1.5)]
    return {'P2_at_12_mm': p2, 'P2_estimate_mm': [32., 56.77, -7.03],
            'P2_difference_mm': sub(p2, [32., 56.77, -7.03]),
            'rows': [{'name': name, 'estimate': estimate, 'model': actual, 'difference': actual-estimate,
                      'within_tolerance': abs(actual-estimate) <= tolerance} for name, estimate, actual, tolerance in estimates],
            'derivation': 'For direct, with theta=c/2 and a fixed: P5z=z1+s*d*sin(a)-(L1+L2+radius)*cos(theta)*cos(a). Foot bbox minimum=P5z-(D/2)*abs(sin(a))-radius*abs(cos(a)). All reported heights and solves use BRep bounding boxes, not this estimate.'}


def build_report(m, quick):
    checks = pose_checks(m)
    if not checks['rigid_formula_satisfied']:
        raise ValueError('Invalid solid posing: foot-centroid chain check failed')
    overlaps, inside = neutral_check(m)
    print(f'neutral {len(overlaps)} overlaps; beginning sweep', file=sys.stderr, flush=True)
    result, reach = sweep(m, quick)
    mass = mass_report(m)
    requirement = {**m.p['requirements']['under_shell_height_mm'], **m.stance_solution,
                   'solved_stance_pose_deg': m.stance,
                   'overall_height_mm': m.p['body']['height_Z']+m.stance_solution['under_shell_height_mm'],
                   'within_range': m.p['requirements']['under_shell_height_mm']['min'] <= m.stance_solution['under_shell_height_mm'] <= m.p['requirements']['under_shell_height_mm']['max'],
                   'straight_leg_under_shell_mm': under_shell(m, (m.p['poses']['stance_spread_a'], 0, 0))}
    reference_pose = m.p['poses']['reference_pose']
    heights = []
    for height in m.p['poses']['height_sweep_mm']:
        solved = solve_stance(m, height)
        pose = solved['pose_deg']
        p2, p3, _ = m.chain(**pose)
        collision = collisions_at(m, pose)
        heights.append({**solved, 'knee_forward_offset_mm': p3[0]-p2[0],
                        'beyond_face_mm': proportions(m, pose)['beyond_face_mm'],
                        'colliding_pair_counts': collision['counts_by_class'],
                        'static_torque_reference_four_feet': static_torque(m, pose, m.p['mass_model']['reference_mass_kg'])['rows'][0]})
    torque = {}
    for label, pose in [('stance', m.stance), ('reference_pose', reference_pose)]:
        torque[label] = {'reference_mass': static_torque(m, pose, m.p['mass_model']['reference_mass_kg']),
                         'model_mass': static_torque(m, pose, mass['total_mass_g']/1000)}
    stance = stance_report(m)
    return {'solids': list(m.meta.values()), 'neutral_overlaps': overlaps, 'inside_shell_envelope': inside,
            'parameter_interferences': m.findings, 'pose_formula_check': checks, 'sweep': result,
            'interferences': m.findings+result['interferences'], 'near_misses': result['near_misses'],
            'total_poses': result['total_poses'], 'colliding_poses': result['colliding_poses'],
            'sweep_seconds': result['sweep_seconds'], 'stance': stance, 'reach': reach, 'mass': mass,
            'mass_and_com': mass, 'datums': m.datums, 'requirement': requirement,
            'reference_pose': {'pose_deg': reference_pose, 'under_shell_height_mm': under_shell(m, angles_tuple(reference_pose)),
                               'overall_height_mm': m.p['body']['height_Z']+under_shell(m, angles_tuple(reference_pose))},
            'ground': ground_report(m), 'proportions': proportions(m, m.stance), 'height_sweep': heights,
            'contact_point': {'stance_mm': contact_point(m, m.stance), 'reference_pose_mm': contact_point(m, reference_pose),
                              'method': 'X of posed P5; Y of the lower posed axis endpoint (axis midpoint at a=0); Z from foot BRep minimum.'},
            'static_torque': torque, 'support': support_report(m, mass),
            'stance_interferences': collisions_at(m, m.stance), 'independent_estimates': independent_estimates(m, requirement, heights),
            'construction_notes': ['J2 case clamped between the carrier end plates is the tie. No carrier_web.',
                                   'No upper_web; no lower_web. Direct knee case is the lower-frame shank.',
                                   'Proximal foot axial midpoint is offset from P5 by its asymmetric prescribed span; centroid formula includes that measured offset.'],
            'brief_conflicts': ([] if checks['literal_P5_centroid_satisfied'] else
                                ['Proximal prescribed foot outer-face span is asymmetric about P5. A centroid=P5 check would fail. Geometry retained; rigid centroid check includes the axial midpoint offset and literal error is separately reported.'])}


def stance_report(m):
    posed = m.pose(**m.stance)
    foot = bbox(posed['foot'])
    fc = centre(posed['foot'])
    extent = old.extents(posed[name] for name in old.leg_names(m))
    dx, dy = m.p['body']['depth_X']/2, m.p['body']['width_Y']/2
    return {'pose_deg': m.stance, 'foot_bottom_z_mm': foot['min'][2],
            'overall_height_mm': m.p['body']['height_Z']-foot['min'][2], 'clock_bottom_clearance_mm': -foot['min'][2],
            'foot_centre_xy_mm': fc[:2], 'stance_width_mm': 2*abs(fc[1]), 'leg_extents_mm': extent,
            'leg_neutral_extents_mm': old.extents(m.parts[name] for name in old.leg_names(m)),
            'body_bbox_exceedance': {'X_plus_mm': max(0., extent['max'][0]-dx), 'X_minus_mm': max(0., -dx-extent['min'][0]),
                                      'Y_plus_mm': max(0., extent['max'][1]-dy), 'Y_minus_mm': max(0., -dy-extent['min'][1])}}


def export(m, report, out, parameter_path):
    out.mkdir(parents=True, exist_ok=True)
    assembly = cad.Compound(label=m.p['revision']+'-'+m.variant, children=list(m.parts.values()))
    output = out/('j04-l03-'+m.variant+'.step')
    cad.export_step(assembly, output, timestamp='2026-11-11T00:00:00+00:00')
    restored = cad.import_step(output)
    original_volume = sum(shape.volume for shape in m.parts.values())
    volume_error = abs(restored.volume-original_volume)
    bbox_error = max(abs(a-b) for a, b in zip(assembly.bounding_box().size, restored.bounding_box().size))
    if not restored.is_valid or len(restored.solids()) != len(m.parts) or volume_error > 1e-4 or bbox_error > 1e-5:
        raise ValueError(f'STEP round trip failed: {len(restored.solids())}/{len(m.parts)} solids, volume error {volume_error}, bbox error {bbox_error}')
    report.update({'revision': m.p['revision'], 'variant': m.variant, 'status': m.p['status'], 'provenance': m.p['provenance'],
                   'provenance_echo': old.provenance_echo(m.p), 'build123d': cad.__version__,
                   'parameter_sha256': hashlib.sha256(parameter_path.read_bytes()).hexdigest(),
                   'generator_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   'helper_sha256': hashlib.sha256((HERE/'leg_packaging.py').read_bytes()).hexdigest(),
                   'template_sha256': hashlib.sha256((HERE/'leg-viewer-template.html').read_bytes()).hexdigest(),
                   'step_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
                   'step_round_trip': {'solids': len(restored.solids()), 'volume_error_mm3': volume_error,
                                       'bounding_box_error_mm': bbox_error, 'valid': restored.is_valid},
                   'assembly_size_mm': old.vec(assembly.bounding_box().size), 'no_structural_analysis_or_physical_testing': True,
                   'scope': SCOPE, 'viewer_verification': 'Browser/GUI proof unrun here; owned by caller.'})
    meshes = []
    for name, shape in m.parts.items():
        vertices, triangles = shape.tessellate(.25, .2)
        meshes.append({'name': name, 'frame': m.meta[name]['frame'], 'color': m.meta[name]['color'],
                       'vertices': [[round(v.X, 6), round(v.Y, 6), round(v.Z, 6)] for v in vertices], 'triangles': triangles})
    # Viewer-only derived stance leaves the input JSON untouched.
    viewer_parameters = {**m.p, 'poses': {**m.p['poses'], 'stance': m.stance}}
    data = {'parts': meshes, 'parameters': viewer_parameters, 'variant': m.variant, 'report': report,
            'P1': m.P1, 'P2': m.P2, 'P3': m.P3, 'floor_z': report['stance']['foot_bottom_z_mm'], 'step_file': output.name}
    embedded = json.dumps(data, separators=(',', ':'), allow_nan=False).replace('<', '\\u003c')
    template = (HERE/'leg-viewer-template.html').read_text()
    template = template.replace('J04-L02-D01', 'J04-L03-D01').replace('J04-L02', 'J04-L03')
    template = template.replace('One leg, with its place reserved.', 'Base module and short leg.')
    template = template.replace("$(axis+'-value').value=angles[axis]+'°'", "$(axis+'-value').value=angles[axis].toFixed(1)+'°'")
    template = template.replace('step="1"', 'step="any"')
    preview = template.replace('/* MODEL_DATA */', embedded)
    (out/'preview.html').write_text(preview)
    report['preview_embedding_check'] = {'mesh_parts': len(meshes), 'triangles': sum(len(mesh['triangles']) for mesh in meshes),
                                         'embedded_model': '/* MODEL_DATA */' not in preview,
                                         'sliders': preview.count('type="range"'), 'start_pose_deg': m.stance,
                                         'browser_checked': False}
    (out/'geometry-check.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')


def variant_summary(report):
    mass, sweep_result = report['mass_and_com'], report['sweep']
    return {'variant': report['variant'], 'parameter_sha256': report['parameter_sha256'],
            'generator_sha256': report['generator_sha256'], 'quick': sweep_result['quick'],
            'solved_stance_pose_deg': report['requirement']['solved_stance_pose_deg'],
            'under_shell_height_mm': report['requirement']['under_shell_height_mm'],
            'overall_height_mm': report['requirement']['overall_height_mm'],
            'stance_reached': report['requirement']['stance_reached'], 'within_range': report['requirement']['within_range'],
            'ground_contact_ok': report['ground']['ground_contact_ok'],
            'leg_mass_g': mass['leg_total_g'], 'four_leg_mass_g': mass['four_legs_g'],
            'total_mass_g': mass['total_mass_g'], 'com_mm': mass['com_mm'],
            'com_height_above_floor_mm': mass['com_height_above_floor_mm'], 'support': report['support'],
            'stance_static_torque': report['static_torque']['stance'], 'proportions': report['proportions'],
            'sweep': {key: sweep_result[key] for key in ('total_poses', 'colliding_poses', 'clear_poses', 'pair_counts_by_class')},
            'height_sweep': report['height_sweep'], 'brief_conflicts': report['brief_conflicts']}


def update_summary(report):
    path = HERE/'exports/l03-summary.json'
    variants = {}
    if path.exists():
        existing = json.loads(path.read_text())
        variants = {key: value for key, value in existing.get('variants', {}).items()
                    if value['parameter_sha256'] == report['parameter_sha256']
                    and value['generator_sha256'] == report['generator_sha256']}
    variants[report['variant']] = variant_summary(report)
    source = HERE/'exports/l02-A-under-direct/geometry-check.json'
    baseline = json.loads(source.read_text())
    comparison = {key: baseline['stance'][key] for key in ('overall_height_mm', 'clock_bottom_clearance_mm', 'stance_width_mm')}
    comparison.update({'leg_mass_g': baseline['mass']['leg_total_g'], 'total_poses': baseline['total_poses'],
                       'colliding_poses': baseline['colliding_poses'], 'source': str(source.relative_to(HERE)),
                       'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    summary = {'revision': report['revision'], 'variants': variants, 'l02_A_under_direct': comparison,
               'rounding': 'JSON retains full floats; printed tables round once to 0.1 mm/degree/gram, 0.001 N m, whole percentages.',
               'printed_tables': summary_tables(variants, comparison)}
    path.write_text(json.dumps(summary, indent=2, allow_nan=False)+'\n')
    return summary


def summary_tables(variants, comparison):
    tables = {}
    for variant, row in variants.items():
        pose = row['solved_stance_pose_deg']
        props = row['proportions']
        lines = ['| Metric | Model |', '|---|---:|',
                 f'| Stance a / b / c (deg) | {pose["a"]:.1f} / {pose["b"]:.1f} / {pose["c"]:.1f} |']
        for label, key in [('Under shell (mm)', 'under_shell_height_mm'), ('Overall height (mm)', 'overall_height_mm'),
                           ('Leg mass (g)', 'leg_mass_g'), ('Four legs (g)', 'four_leg_mass_g'), ('Total mass (g)', 'total_mass_g'),
                           ('CoM height above floor (mm)', 'com_height_above_floor_mm')]:
            lines.append(f'| {label} | {row[key]:.1f} |')
        lines += [f'| Stance reached / in range / ground contact | {row["stance_reached"]} / {row["within_range"]} / {row["ground_contact_ok"]} |',
                  '| CoM XYZ (mm) | '+' / '.join(f'{value:.1f}' for value in row['com_mm'])+' |']
        for key in ('width_across_hips_mm', 'overall_width_mm', 'overall_length_mm', 'beyond_face_mm', 'track_width_mm',
                    'wheelbase_mm', 'base_height_mm', 'base_below_shell_mm', 'inside_shell_mm'):
            lines.append(f'| {key} | {props[key]:.1f} |')
        for key, value in row['support']['four_feet_margins_mm'].items():
            lines.append(f'| {key} (mm) | {value:.1f} |')
        lines.append(f'| Minimum-margin tip angle (deg) | {row["support"]["tip_angle_deg"]:.1f} |')
        for item in row['support']['three_feet']:
            lines.append(f'| Lifted {item["lifted_leg"]}, signed margin (mm) | {item["signed_margin_mm"]:.1f} |')
        lines.append(f'| Sweep total / colliding / clear poses | {row["sweep"]["total_poses"]} / {row["sweep"]["colliding_poses"]} / {row["sweep"]["clear_poses"]} |')
        lines += ['', '| Height target / actual (mm) | a / b / c (deg) | Reached | Knee forward (mm) | Beyond face (mm) | Own / base / shell / neighbour pairs | J1 / J2 / J3 (N m), 1 kg / 4 feet |',
                  '|---|---|---|---:|---:|---|---|']
        for height in row['height_sweep']:
            pose, counts, torque = height['pose_deg'], height['colliding_pair_counts'], height['static_torque_reference_four_feet']
            lines.append(f'| {height["target_mm"]:.1f} / {height["under_shell_height_mm"]:.1f} | '
                         +' / '.join(f'{pose[axis]:.1f}' for axis in AXES)+f' | {height["stance_reached"]} | {height["knee_forward_offset_mm"]:.1f} | {height["beyond_face_mm"]:.1f} | '
                         +' / '.join(str(counts[kind]) for kind in KINDS)+' | '
                         +' / '.join(f'{torque["J"+str(i)+"_Nm"]:.3f}' for i in (1, 2, 3))+' |')
        tables[variant] = '\n'.join(lines)
    tables['l02_A_under_direct'] = ('| L02 comparison | Value |\n|---|---:|\n'
                                  + '\n'.join(f'| {key} | {comparison[key]:.1f} |' for key in
                                              ('overall_height_mm', 'clock_bottom_clearance_mm', 'leg_mass_g', 'stance_width_mm'))
                                  +f'\n| total / colliding poses | {comparison["total_poses"]} / {comparison["colliding_poses"]} |')
    return tables


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parameters', type=Path, default=HERE/'j04-l03.base-short.json')
    parser.add_argument('--out', type=Path)
    parser.add_argument('--variant', choices=('direct', 'proximal'))
    parser.add_argument('--quick', action='store_true', help='Double sweep step, retain inclusive endpoints')
    args = parser.parse_args()
    start = time.monotonic()
    initial = json.loads(args.parameters.read_text())
    variant = args.variant or initial['knee']['variant']
    if variant not in ('direct', 'proximal'):
        raise ValueError('Variant must be direct or proximal')
    p = read_parameters(args.parameters, variant)
    model = Model(p, variant).build()
    print(f'built {len(model.parts)} valid solid leaves; {variant}', file=sys.stderr, flush=True)
    report = build_report(model, args.quick)
    report['build_seconds_before_export'] = time.monotonic()-start
    out = args.out or HERE/'exports'/('l03-base-'+variant)
    export(model, report, out, args.parameters)
    report['total_build_seconds'] = time.monotonic()-start
    (out/'geometry-check.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    summary = update_summary(report)
    print(json.dumps(report, indent=2, allow_nan=False))
    print(summary['printed_tables'][variant], file=sys.stderr)


if __name__ == '__main__':
    main()

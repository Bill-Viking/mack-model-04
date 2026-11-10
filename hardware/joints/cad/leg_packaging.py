"""J04-L02 nominal rigid leg packaging; no structural or walking claims.

ASSUMES: all solids are rigid in their declared frame. A foot pad therefore
rotates with the lower link, including its offset below P4. The report retains
both the brief's unrotated-offset comparison and the rigid-body comparison.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys
import time

import build123d as cad

HERE = Path(__file__).resolve().parent
EPS = 1e-5
SCOPE = ('Nominal rigid envelopes; discrete pose samples, not a continuous collision proof. '
         'No cables, fasteners, stops, encoders, covers, batteries or measured shell interior.')
COLORS = {'body': '#a8aaa5', 'carrier': '#d8c6a6', 'upper': '#6f97a2',
          'lower': '#7896a0', 'actuator': '#4a5261', 'steel': '#aab6bf', 'foot': '#303b40'}
TEST_POSES = [(0, 0, 0), (12, -35, 70), (-30, 90, 120), (30, -90, 0), (15, 45, -30)]


def vec(v):
    return list(v)


def add(a, b):
    return [x+y for x, y in zip(a, b)]


def sub(a, b):
    return [x-y for x, y in zip(a, b)]


def mul(v, k):
    return [x*k for x in v]


def norm(v):
    return math.sqrt(sum(x*x for x in v))


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def rx(v, a):
    a = math.radians(a)
    x, y, z = v
    return [x, y*math.cos(a)-z*math.sin(a), y*math.sin(a)+z*math.cos(a)]


def ry(v, b):
    b = math.radians(b)
    x, y, z = v
    return [x*math.cos(b)+z*math.sin(b), y, -x*math.sin(b)+z*math.cos(b)]


def bbox(shape):
    b = shape.bounding_box()
    return {'min': vec(b.min), 'max': vec(b.max)}


def centre(shape):
    return vec(shape.center(cad.CenterOf.MASS))


def box(x0, x1, y0, y1, z0, z1):
    lo, hi = [min(x0, x1), min(y0, y1), min(z0, z1)], [max(x0, x1), max(y0, y1), max(z0, z1)]
    size = sub(hi, lo)
    if min(size) <= 1e-9:
        raise ValueError(f'Empty box dimensions: {size}')
    return cad.Pos(*mul(add(lo, hi), .5))*cad.Box(*size)


def cyl(point, axis, low, high, radius):
    if high <= low or radius <= 0:
        raise ValueError('Cylinder span and radius must be positive')
    mid = add(point, mul(axis, (low+high)/2))
    return cad.Plane(origin=mid, z_dir=axis)*cad.Cylinder(radius, high-low)


def bbox_gap(a, b):
    return norm([max(0., a['min'][i]-b['max'][i], b['min'][i]-a['max'][i]) for i in range(3)])


def boxes_overlap(a, b):
    return all(min(a['max'][i], b['max'][i])-max(a['min'][i], b['min'][i]) > 1e-8 for i in range(3))


def common_volume(a, b, ba=None, bb=None):
    if not boxes_overlap(ba or bbox(a), bb or bbox(b)):
        return 0.
    common = a & b
    return 0. if common is None else sum(s.volume for s in common.solids())


def grid(v, quick=False):
    low, high, step = v
    step *= 2 if quick else 1
    return sorted(set([min(low+i*step, high) for i in range(math.ceil((high-low)/step)+1)] + [high]))


def read_parameters(path, variant=None):
    p = json.loads(path.read_text())
    def finite(value, name, positive=False):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or (positive and value <= 0):
            raise ValueError(f'{name} must be finite' + (' and positive' if positive else ''))
    positive = {'body': ['width_Y', 'depth_X', 'height_Z'],
                'cradle': ['thickness', 'density_g_cm3'],
                'actuator': ['W', 'H', 'D', 'mass_g', 'axis_offset_from_near_end',
                             'horn_diameter', 'horn_height', 'idler_diameter', 'idler_height'],
                'hip': ['d', 'carrier_plate_half_span', 'carrier_hub_radius'],
                'links': ['L1', 'L2', 'plate_thickness', 'plate_width', 'hub_radius', 'web_half_width', 'clearance', 'density_g_cm3'],
                'knee': ['pulley_diameter', 'pulley_width', 'belt_thickness', 'belt_mass_g',
                         'shaft_diameter', 'bearing_mass_g', 'pulley_density_g_cm3', 'shaft_density_g_cm3'],
                'foot': ['X', 'Y', 'Z', 'density_g_cm3']}
    for section, keys in positive.items():
        for key in keys:
            finite(p[section][key], f'{section}.{key}', True)
    for section, keys in {'cradle': ['inset', 'z_top', 'window_clearance'], 'hip': ['h2', 'j2_axial_offset']}.items():
        for key in keys:
            finite(p[section][key], f'{section}.{key}')
    for key in ('hardware_allowance_g_per_joint', 'clearance_floor'):
        finite(p[key], key)
        if p[key] < 0:
            raise ValueError(f'{key} must be nonnegative')
    if len(p['hip']['P1']) != 3:
        raise ValueError('hip.P1 must have three coordinates')
    for value in p['hip']['P1']:
        finite(value, 'hip.P1 coordinate')
    if p['hip']['P1'][1] == 0:
        raise ValueError('hip.P1 Y must be nonzero to define outboard')
    v = variant or p['knee']['variant']
    if v not in ('direct', 'proximal'):
        raise ValueError('knee.variant must be direct or proximal')
    # A parameter file may carry one upper-link length per knee variant (links.L1_direct /
    # links.L1_proximal); the one for the running variant replaces links.L1. ASSUMES: when both
    # keys are absent, links.L1 is the length for either variant.
    per_variant = p['links'].get(f'L1_{v}')
    if per_variant is not None:
        finite(per_variant, f'links.L1_{v}', True)
        p['links']['L1'] = per_variant
    if p['hip']['j2_case_long_dir'] != 'down':
        raise ValueError('D01 supports only hip.j2_case_long_dir = down')
    if v == 'proximal' and p['knee']['mount_side'] not in ('inboard', 'outboard'):
        raise ValueError('Proximal variant requires knee.mount_side inboard or outboard; '
                         f"received {p['knee']['mount_side']!r}. The unchanged example uses inline.")
    if p['knee']['case_long_dir'] not in ('up', 'down'):
        raise ValueError('knee.case_long_dir must be up or down')
    if p['hip']['j1_case_long_dir'] not in ('inboard', 'outboard', 'up', 'down'):
        raise ValueError('hip.j1_case_long_dir must be inboard, outboard, up or down')
    if p['hip']['j1_horn_dir'] not in ('+X', '-X'):
        raise ValueError('hip.j1_horn_dir must be +X or -X')
    for section, key in [('hip', 'j2_horn_dir'), ('knee', 'horn_dir')]:
        if p[section][key] not in ('inboard', 'outboard'):
            raise ValueError(f'{section}.{key} must be inboard or outboard')
    if p['actuator']['axis_offset_from_near_end'] >= p['actuator']['H']:
        raise ValueError('actuator axis offset must lie inside H')
    if p['actuator']['horn_height'] != p['actuator']['idler_height']:
        raise ValueError('D01 requires equal horn and idler boss heights')
    if p['hip']['carrier_plate_half_span']-p['links']['plate_thickness'] <= p['actuator']['D']/2+p['actuator']['horn_height']:
        raise ValueError('Carrier inner faces must leave a positive hub span beyond J1 bosses')
    if p['cradle']['inset'] < 0 or p['cradle']['window_clearance'] < 0 or 2*p['cradle']['inset'] >= min(p['body']['depth_X'], p['body']['width_Y']):
        raise ValueError('Invalid cradle inset or window clearance')
    if not isinstance(p['neighbors'], bool):
        raise ValueError('neighbors must be boolean')
    bearing = p['knee']['bearing_id_od_w']
    if len(bearing) != 3:
        raise ValueError('bearing_id_od_w requires three values')
    for value in bearing:
        finite(value, 'bearing_id_od_w', True)
    if not bearing[0] < bearing[1] < 2*p['links']['hub_radius']:
        raise ValueError('Bearing ID < OD < hub diameter is required')
    if v == 'proximal' and p['knee']['shaft_diameter'] > bearing[0]:
        raise ValueError('Shaft cannot exceed bearing ID')
    n = 1
    for axis in ('a', 'b', 'c'):
        finite(p['poses']['stance'][axis], f'stance.{axis}')
        values = p['poses']['sweep'][axis]
        if len(values) != 3:
            raise ValueError(f'sweep.{axis} requires min, max, step')
        for value in values:
            finite(value, f'sweep.{axis}')
        if values[2] <= 0 or values[1] < values[0]:
            raise ValueError(f'sweep.{axis} requires min <= max and positive step')
        n *= math.ceil((values[1]-values[0])/values[2])+1
    if n > 5000:
        raise ValueError('Sweep is bounded to 5000 discrete poses')
    return p, v


class Model:
    def __init__(self, p, variant):
        self.p, self.variant = p, variant
        self.parts, self.meta, self.datums, self.findings = {}, {}, {}, []
        h, l = p['hip'], p['links']
        self.P1 = h['P1']
        self.s = 1 if self.P1[1] > 0 else -1
        self.P2 = add(self.P1, [0, self.s*h['d'], -h['h2']])
        self.P3 = add(self.P2, [0, 0, -l['L1']])
        self.P4 = add(self.P3, [0, 0, -l['L2']])
        self.axes = [cad.Axis(self.P1, (1, 0, 0)), cad.Axis(self.P2, (0, 1, 0)), cad.Axis(self.P3, (0, 1, 0))]

    def direction(self, word):
        return {'+X': [1, 0, 0], '-X': [-1, 0, 0], 'up': [0, 0, 1], 'down': [0, 0, -1],
                'outboard': [0, self.s, 0], 'inboard': [0, -self.s, 0]}[word]

    def put(self, name, shape, frame, mass_class='polymer', fixed_mass=None, color=None):
        # Export a solid leaf, never a nested Compound leaf.
        if not shape.is_valid or len(shape.solids()) != 1 or shape.volume <= 0:
            raise ValueError(f'{name}: invalid, empty or multi-solid part')
        shape = shape.solids()[0]
        shape.label = name
        color = color or COLORS['foot' if name == 'foot' else 'actuator' if mass_class in ('actuator', 'boss') else 'steel' if mass_class in ('steel', 'pulley', 'bearing', 'belt') else frame]
        shape.color = cad.Color(color)
        self.parts[name] = shape
        density = {'polymer': self.p['links']['density_g_cm3'], 'cradle': self.p['cradle']['density_g_cm3'],
                   'foot': self.p['foot']['density_g_cm3'], 'steel': self.p['knee']['shaft_density_g_cm3'],
                   'pulley': self.p['knee']['pulley_density_g_cm3']}.get(mass_class, 0.)
        self.meta[name] = {'name': name, 'frame': frame, 'mass_class': mass_class,
                           'mass_g': fixed_mass if fixed_mass is not None else shape.volume*density/1000,
                           'volume_mm3': shape.volume, 'centroid_mm': centre(shape), 'color': color}
        return shape

    def actuator(self, label, axis_dir, long_dir, point, axial_offset, horn_dir, frame="body"):
        p = self.p['actuator']
        a, l, horn = axis_dir, self.direction(long_dir), self.direction(horn_dir)
        w = cross(a, l)
        if abs(norm(w)-1) > 1e-9 or abs(sum(x*y for x, y in zip(a, horn))) < .999:
            raise ValueError(f'{label}: actuator directions must be perpendicular, horn parallel to axis')
        axis_centre = add(point, mul(a, axial_offset))
        e, H, D = p['axis_offset_from_near_end'], p['H'], p['D']
        centre_case = add(axis_centre, mul(l, H/2-e))
        shape = cad.Plane(origin=centre_case, x_dir=w, z_dir=a)*cad.Box(p['W'], H, D)
        case = self.put(label, shape, frame, 'actuator', p['mass_g'])
        face_h = add(axis_centre, mul(horn, D/2))
        face_i = sub(axis_centre, mul(horn, D/2))
        self.put(label+'_horn', cyl(face_h, horn, 0, p['horn_height'], p['horn_diameter']/2), frame, 'boss', 0.)
        self.put(label+'_idler', cyl(face_i, mul(horn, -1), 0, p['idler_height'], p['idler_diameter']/2), frame, 'boss', 0.)
        self.datums[label] = {'axis_point': vec(point), 'axis_dir': vec(a), 'axial_offset_mm': axial_offset,
                              'case_axis_centre': axis_centre, 'near_end_point': sub(axis_centre, mul(l, e)),
                              'far_end_point': add(axis_centre, mul(l, H-e)), 'horn_face_centre': face_h,
                              'idler_face_centre': face_i, 'horn_boss_outer_centre': add(face_h, mul(horn, p['horn_height'])),
                              'idler_boss_outer_centre': sub(face_i, mul(horn, p['idler_height'])), 'case_bbox': bbox(case)}
        return tuple(self.parts[label+suffix] for suffix in ("", "_horn", "_idler"))

    def transform(self, shape, frame, a, b, c):
        if frame == 'lower':
            shape = shape.rotate(self.axes[2], c)
        if frame in ('upper', 'lower'):
            shape = shape.rotate(self.axes[1], b)
        if frame in ('carrier', 'upper', 'lower'):
            shape = shape.rotate(self.axes[0], a)
        return shape

    def pose(self, a, b, c):
        return {n: self.transform(sh, self.meta[n]['frame'], a, b, c) for n, sh in self.parts.items()}

    def chain(self, a, b, c):
        p2 = add(self.P1, rx(sub(self.P2, self.P1), a))
        p3 = add(p2, rx(ry([0, 0, -self.p['links']['L1']], b), a))
        return p2, p3, add(p3, rx(ry([0, 0, -self.p['links']['L2']], b+c), a))

    def link_plate(self, start, end, y0, y1, end_hub=True):
        r, pw = self.p['links']['hub_radius'], self.p['links']['plate_width']
        x, _, z = start
        shape = cyl([x, 0, z], [0, 1, 0], min(y0, y1), max(y0, y1), r)
        if abs(end[2]-z) > 1e-9:
            shape += box(x-pw/2, x+pw/2, y0, y1, z, end[2])
        if end_hub:
            shape += cyl([end[0], 0, end[2]], [0, 1, 0], min(y0, y1), max(y0, y1), r)
        return shape

    def build(self):
        p, parts = self.p, self.parts
        h, l, k, ac, cr = [p[x] for x in ('hip', 'links', 'knee', 'actuator', 'cradle')]
        x1, y1, z1 = self.P1
        x2, y2, z2 = self.P2
        x3, y3, z3 = self.P3
        x4, y4, z4 = self.P4
        tp, cl, hg, W, D = l['plate_thickness'], l['clearance'], ac['horn_height'], ac['W'], ac['D']
        dx, dy = p['body']['depth_X']/2, p['body']['width_Y']/2
        self.put('body_envelope', box(-dx, dx, -dy, dy, 0, p['body']['height_Z']), 'body', 'envelope', 0.)
        self.put('cradle', box(-dx+cr['inset'], dx-cr['inset'], -dy+cr['inset'], dy-cr['inset'], cr['z_top']-cr['thickness'], cr['z_top']), 'body', 'cradle')
        self.actuator('j1_actuator', [1, 0, 0], h['j1_case_long_dir'], self.P1, 0, h['j1_horn_dir'], 'body')
        j1 = self.datums['j1_actuator']
        cb, jb = bbox(parts['cradle']), j1['case_bbox']
        overlap = min(cb['max'][2], jb['max'][2])-max(cb['min'][2], jb['min'][2])
        if overlap > 0:
            self.findings.append({'name': 'j1_case_into_cradle', 'overlap_mm': overlap, 'phase': 'before_windows'})
        else:
            zlo, zhi = (jb['max'][2], cb['min'][2]) if jb['max'][2] <= cb['min'][2] else (cb['max'][2], jb['min'][2])
            if zhi-zlo > 1e-9:
                self.put('j1_mount', box(jb['min'][0], jb['max'][0], jb['min'][1], jb['max'][1], zlo, zhi), 'body')
        self.actuator('j2_actuator', [0, 1, 0], 'down', self.P2, h['j2_axial_offset'], h['j2_horn_dir'], 'carrier')
        j2 = self.datums['j2_actuator']
        jb2, half, r = j2['case_bbox'], h['carrier_plate_half_span'], h['carrier_hub_radius']
        for side_name, side in [('horn', 1 if h['j1_horn_dir'] == '+X' else -1), ('idler', -1 if h['j1_horn_dir'] == '+X' else 1)]:
            xa, xb = sorted([x1+side*(half-tp), x1+side*half])
            plate = (cyl([0, y1, z1], [1, 0, 0], xa, xb, r)
                     + box(xa, xb, min(y1, jb2['min'][1]), max(y1, jb2['max'][1]), j2['far_end_point'][2], z1))
            self.put('carrier_'+side_name+'_plate', plate, 'carrier')
            xa, xb = sorted([side*(D/2+hg), side*(half-tp)])
            self.put('carrier_hub_'+side_name, cyl(self.P1, [1, 0, 0], xa, xb, r), 'carrier')
        self.put('carrier_web', box(x1-half+tp, x1+half-tp, jb2['min'][1], jb2['max'][1], j2['far_end_point'][2]-cl-tp, j2['far_end_point'][2]-cl), 'carrier')
        if W/2 >= half-tp:
            self.findings.append({'name': 'j2_case_into_carrier_plates', 'overlap_mm': W/2-(half-tp)})
        # Upper plates sit outside both J2 boss outer faces.
        upper_bands, upper_outer = {}, {}
        for name, word, outward in [('horn', 'horn_boss_outer_centre', 1 if h['j2_horn_dir'] == 'outboard' else -1),
                                    ('idler', 'idler_boss_outer_centre', -1 if h['j2_horn_dir'] == 'outboard' else 1)]:
            side = outward*self.s
            inner = j2[word][1]
            upper_bands[name] = sorted([inner, inner+side*tp])
            upper_outer[side] = inner+side*tp
        y_upper_min, y_upper_max = min(upper_outer.values()), max(upper_outer.values())
        if self.variant == 'direct':
            self.actuator('knee_actuator', [0, 1, 0], k['case_long_dir'], self.P3, 0, k['horn_dir'], 'upper')
            knee = self.datums['knee_actuator']
            zend = knee['far_end_point'][2]+cl
            if zend < z2-(ac['H']-ac['axis_offset_from_near_end'])-cl:
                self.findings.append({'name': 'upper_plates_too_short', 'overlap_mm': z2-(ac['H']-ac['axis_offset_from_near_end'])-cl-zend})
        else:
            zend = z3
        for name, band in upper_bands.items():
            plate = self.link_plate(self.P2, [x3, y3, zend], *band, False)
            if zend <= z3:
                plate += cyl([x3, 0, z3], [0, 1, 0], *band, l['hub_radius'])
            if self.variant == 'proximal':
                plate -= cyl([x3, 0, z3], [0, 1, 0], band[0]-1, band[1]+1, k['bearing_id_od_w'][1]/2)
            self.put('upper_'+name+'_plate', plate, 'upper')
        self.put('upper_web', box(x2-l['web_half_width'], x2+l['web_half_width'], y_upper_min, y_upper_max,
                                   z2+ac['axis_offset_from_near_end']+cl, z2+ac['axis_offset_from_near_end']+cl+tp), 'upper')
        if self.variant == 'direct':
            for sign, name in [(1, 'plus'), (-1, 'minus')]:
                xx = x2+sign*(W/2+cl+tp/2)
                self.put('upper_channel_'+name, box(xx-tp/2, xx+tp/2, min(b[1] for b in upper_bands.values()), max(b[0] for b in upper_bands.values()),
                            j2['far_end_point'][2]-cl, z3+.25*(knee['far_end_point'][2]-z3)), 'upper')
            kb = knee['case_bbox']
            zov = min(kb['max'][2], jb2['max'][2])-max(kb['min'][2], jb2['min'][2])
            yov = min(kb['max'][1], jb2['max'][1])-max(kb['min'][1], jb2['min'][1])
            if zov > 0 and yov > 0:
                self.findings.append({'name': 'knee_case_into_j2_case', 'overlap_mm': zov,
                                      'volume_mm3': common_volume(parts['knee_actuator'], parts['j2_actuator'])})
            lower_bands = {}
            for name, key, direction in [('horn', 'horn_boss_outer_centre', self.direction(k['horn_dir'])[1]),
                                          ('idler', 'idler_boss_outer_centre', -self.direction(k['horn_dir'])[1])]:
                yy = knee[key][1]
                lower_bands[name] = sorted([yy, yy+direction*tp])
                self.put('lower_'+name+'_plate', self.link_plate(self.P3, self.P4, *lower_bands[name]), 'lower')
            ly0, ly1 = min(v[0] for v in lower_bands.values()), max(v[1] for v in lower_bands.values())
            # The case end away from J2 is its lowest Z face (near when long_dir=up).
            z_end = kb['min'][2]
            self.put('lower_web', box(x3-l['web_half_width'], x3+l['web_half_width'], ly0, ly1, *( [z_end-cl-tp, z_end-cl] if k['case_long_dir'] == 'up' else [z_end+cl, z_end+cl+tp] )), 'lower')
        else:
            side = self.direction(k['mount_side'])[1]
            matching_outer = upper_outer[side]
            offset = matching_outer-y2+side*(hg+D/2)
            self.actuator('knee_actuator', [0, 1, 0], 'down', self.P2, offset, k['mount_side'], 'upper')
            knee = self.datums['knee_actuator']
            far_y = knee['case_axis_centre'][1]+side*D/2
            self.put('knee_mount', box(x2-W/2, x2+W/2, matching_outer, far_y,
                                      knee['far_end_point'][2]-tp, knee['far_end_point'][2]), 'upper')
            pulley_inner = knee['horn_boss_outer_centre'][1]
            pulley_outer = pulley_inner+side*k['pulley_width']
            band = sorted([pulley_inner, pulley_outer])
            for name, pp in [('pulley_hip', self.P2), ('pulley_knee', self.P3)]:
                self.put(name, cyl([pp[0], 0, pp[2]], [0, 1, 0], *band, k['pulley_diameter']/2), 'upper', 'pulley')
                self.datums[name] = {'axis_point': [pp[0], sum(band)/2, pp[2]], 'axis_dir': [0, 1, 0], 'y_band_mm': band}
            self.put('belt', box(x2-k['pulley_diameter']/2, x2+k['pulley_diameter']/2, *band, z3, z2), 'upper', 'belt', k['belt_mass_g'])
            lower_bands = {}
            for direction in (-1, 1):
                anchor = pulley_outer if direction == side else upper_outer[direction]
                yy = anchor+direction*cl
                lower_bands[direction] = sorted([yy, yy+direction*tp])
                suffix = 'out' if direction == self.s else 'in'
                self.put('lower_plate_'+suffix, self.link_plate(self.P3, self.P4, *lower_bands[direction]), 'lower')
            ly0, ly1 = min(v[0] for v in lower_bands.values()), max(v[1] for v in lower_bands.values())
            self.put('lower_web', box(x3-l['web_half_width'], x3+l['web_half_width'], ly0, ly1,
                                      z3-l['hub_radius']-cl-tp, z3-l['hub_radius']-cl), 'lower')
            self.put('knee_shaft', cyl([x3, 0, z3], [0, 1, 0], ly0, ly1, k['shaft_diameter']/2), 'upper', 'steel')
            self.datums['knee_shaft'] = {'axis_point': [x3, y3, z3], 'axis_dir': [0, 1, 0], 'y_band_mm': [ly0, ly1]}
            bi, bo, bw = k['bearing_id_od_w']
            for direction in (-1, 1):
                yy = upper_outer[direction]-direction*tp/2
                bb = [yy-bw/2, yy+bw/2]
                ring = cyl([x3, 0, z3], [0, 1, 0], *bb, bo/2)-cyl([x3, 0, z3], [0, 1, 0], bb[0]-1, bb[1]+1, bi/2)
                self.put('knee_bearing_'+('out' if direction == self.s else 'in'), ring, 'upper', 'bearing', k['bearing_mass_g'])
        self.put('foot', box(x4-p['foot']['X']/2, x4+p['foot']['X']/2, y4-p['foot']['Y']/2, y4+p['foot']['Y']/2, z4-p['foot']['Z'], z4), 'lower', 'foot')
        self.cut_windows()
        if p['neighbors']:
            stance = p['poses']['stance']
            posed = self.pose(**stance)
            names = [n for n in parts if self.meta[n]['frame'] != 'body' or n.startswith('j1_')]
            for prefix, mirror_y, mirror_x in [('FR', True, False), ('RL', False, True), ('RR', True, True)]:
                for name in names:
                    sh = posed[name]
                    if mirror_y:
                        sh = sh.mirror(cad.Plane.XZ)
                    if mirror_x:
                        sh = sh.mirror(cad.Plane.YZ)
                    self.put(f'nb_{prefix}_{name}', sh, 'body', 'neighbor_envelope', 0., self.meta[name]['color'])
        return self

    def cut_windows(self):
        cradle = self.parts['cradle']
        hits = [n for n in self.parts if self.meta[n]['frame'] == 'carrier' and common_volume(cradle, self.parts[n]) > EPS]
        self.windows = []
        if hits:
            bounds = [bbox(self.parts[n]) for n in hits]
            margin = self.p['cradle']['window_clearance']
            lo = [min(b['min'][i] for b in bounds)-margin for i in range(2)]
            hi = [max(b['max'][i] for b in bounds)+margin for i in range(2)]
            z = bbox(cradle)
            self.windows.append({'x_mm': [lo[0], hi[0]], 'y_mm': [lo[1], hi[1]], 'intersecting_solids': hits})
            self.put('cradle', cradle-box(lo[0], hi[0], lo[1], hi[1], z['min'][2]-1, z['max'][2]+1), 'body', 'cradle')


def pose(solids_by_frame, a, b, c, P1, P2, P3):
    """Public neutral-frame posing helper; no metadata or input mutation."""
    axes = [cad.Axis(P1, (1, 0, 0)), cad.Axis(P2, (0, 1, 0)), cad.Axis(P3, (0, 1, 0))]
    result = {}
    for frame, solids in solids_by_frame.items():
        result[frame] = {}
        for name, shape in solids.items():
            if frame == 'lower':
                shape = shape.rotate(axes[2], c)
            if frame in ('upper', 'lower'):
                shape = shape.rotate(axes[1], b)
            if frame in ('carrier', 'upper', 'lower'):
                shape = shape.rotate(axes[0], a)
            result[frame][name] = shape
    return result


def pose_checks(m):
    rows = []
    for a, b, c in TEST_POSES:
        actual = centre(m.transform(m.parts['foot'], 'lower', a, b, c))
        p4 = m.chain(a, b, c)[2]
        rigid = add(p4, rx(ry([0, 0, -m.p['foot']['Z']/2], b+c), a))
        brief = sub(p4, [0, 0, m.p['foot']['Z']/2])
        rows.append({'pose_deg': [a, b, c], 'foot_centroid_mm': actual, 'P4_mm': p4,
                     'rigid_expected_centroid_mm': rigid, 'rigid_formula_error_mm': norm(sub(actual, rigid)),
                     'brief_expected_centroid_mm': brief, 'brief_formula_error_mm': norm(sub(actual, brief))})
    return {'tests': rows, 'maximum_error_mm': max(r['rigid_formula_error_mm'] for r in rows),
            'maximum_brief_formula_error_mm': max(r['brief_formula_error_mm'] for r in rows),
            'rigid_formula_satisfied': all(r['rigid_formula_error_mm'] < 1e-6 for r in rows),
            'brief_formula_satisfied': all(r['brief_formula_error_mm'] < 1e-6 for r in rows),
            'scope': 'Rigid lower-frame pad offset rotates with Rx(a) Ry(b+c). The brief subtracts an unrotated Z offset; both measured errors are retained.'}


def intentional_pairs(m):
    pairs = {}
    def skip(a, b, why):
        if a in m.parts and b in m.parts:
            pairs[tuple(sorted([a, b]))] = why
    for word in ('horn', 'idler'):
        skip('carrier_hub_'+word, 'j1_actuator_'+word, 'J1 hub on boss')
        skip('upper_'+word+'_plate', 'j2_actuator_'+word, 'plate on J2 boss')
        skip('lower_'+word+'_plate', 'knee_actuator_'+word, 'plate on knee boss')
    for suffix in ('in', 'out'):
        bearing = 'knee_bearing_'+suffix
        if bearing in m.parts:
            matching = min(('upper_horn_plate', 'upper_idler_plate'),
                           key=lambda n: abs(m.meta[n]['centroid_mm'][1]-m.meta[bearing]['centroid_mm'][1]))
            skip(bearing, matching, 'bearing in matching OD plate hole')
        for name in ('lower_plate_in', 'lower_plate_out', 'pulley_knee', 'knee_bearing_in', 'knee_bearing_out', 'upper_horn_plate', 'upper_idler_plate'):
            skip('knee_shaft', name, 'nominal shaft through bearing/pulley/plate')
    for name in ('pulley_hip', 'pulley_knee'):
        skip('belt', name, 'belt envelope on pulley')
    return pairs


def neutral_check(m):
    bounds = {n: bbox(s) for n, s in m.parts.items()}
    overlaps = []
    for a, b in itertools.combinations(m.parts, 2):
        v = common_volume(m.parts[a], m.parts[b], bounds[a], bounds[b])
        if v > EPS:
            overlaps.append({'parts': [a, b], 'volume_mm3': v})
    inside = []
    for a in ('j1_actuator', 'j1_mount'):
        if a not in m.parts:
            continue
        for b in ('cradle', 'body_envelope'):
            v = common_volume(m.parts[a], m.parts[b])
            if v > EPS:
                common = m.parts[a] & m.parts[b]
                bb = bbox(common)
                inside.append({'parts': [a, b], 'volume_mm3': v, 'z_range_mm': [bb['min'][2], bb['max'][2]],
                               'classification': 'unknown shell interior; physical intake question'})
    return overlaps, inside


def reach_bounds(points):
    if not points:
        return {'count': 0, 'min_mm': None, 'max_mm': None}
    return {'count': len(points), 'min_mm': [min(v[i] for v in points) for i in range(3)],
            'max_mm': [max(v[i] for v in points) for i in range(3)]}


def sweep(m, quick):
    start = time.monotonic()
    skipped = intentional_pairs(m)
    frames = {f: [n for n in m.parts if m.meta[n]['frame'] == f] for f in ('body', 'carrier', 'upper', 'lower')}
    pairs = []
    for moving, targets in [('carrier', ['body']), ('upper', ['carrier', 'body']), ('lower', ['upper', 'carrier', 'body'])]:
        for x in frames[moving]:
            for f in targets:
                for y in frames[f]:
                    if tuple(sorted([x, y])) not in skipped:
                        pairs.append((x, y))
    grids = {f: grid(m.p['poses']['sweep'][f], quick) for f in ('a', 'b', 'c')}
    poses = list(itertools.product(grids['a'], grids['b'], grids['c']))
    cache_shapes, samples = {}, []
    for angles in poses:
        a, b, c = angles
        sample = {}
        for n, sh in m.parts.items():
            frame = m.meta[n]['frame']
            key_angles = {'body': (), 'carrier': (a,), 'upper': (a, b), 'lower': angles}[frame]
            key = (n, key_angles)
            if key not in cache_shapes:
                moved = m.transform(sh, frame, a, b, c)
                cache_shapes[key] = (moved, bbox(moved))
            sample[n] = cache_shapes[key]
        samples.append(sample)
    records, collisions = [], [False]*len(poses)
    # Per-pose hit counts by pair kind, so the report can list the collision-free poses without
    # relying on the capped collision_samples. ASSUMES: a pair's kind is read from the part names:
    # an nb_ prefix is a neighbouring leg, body_envelope and cradle are the shell side, and
    # everything else (the fixed J1 case and its mount included) counts as the leg's own hardware.
    KINDS = ('own_leg', 'shell_cradle', 'neighbour')
    def pair_kind(x, y):
        if x.startswith('nb_') or y.startswith('nb_'):
            return 2
        return 1 if 'body_envelope' in (x, y) or 'cradle' in (x, y) else 0
    hits = [[0, 0, 0] for _ in poses]
    exact_distance_calls, exact_common_calls, invariant_cache_hits = 0, 0, 0
    last_progress = start
    for pair_index, (x, y) in enumerate(pairs):
        record = {'parts': [x, y], 'kind': KINDS[pair_kind(x, y)], 'minimum_distance_mm': math.inf, 'minimum_distance_pose_deg': None,
                  'colliding_poses': 0, 'collision_samples': [], 'colliding_pose_indices': [], 'maximum_overlap_mm3': 0.}
        kind_index = pair_kind(x, y)
        fx, fy = m.meta[x]['frame'], m.meta[y]['frame']
        def configuration(angles):
            a, b, c = angles
            if fy == 'body':
                return {'carrier': (a,), 'upper': (a, b), 'lower': (a, b, c)}[fx]
            return (c,) if fy == 'upper' else (b,) if fx == 'upper' else (b, c)
        volumes, distances, candidates = {}, {}, []
        # First enumerate common volumes. Any collision establishes an exact
        # sweep minimum distance of zero, avoiding redundant distance queries.
        for index, (angles, sample) in enumerate(zip(poses, samples)):
            key = configuration(angles)
            sx, bx = sample[x]
            sy, by = sample[y]
            gap = bbox_gap(bx, by)
            candidates.append((gap, index, key))
            if key in volumes:
                volume = volumes[key]
                invariant_cache_hits += 1
            else:
                overlap_possible = boxes_overlap(bx, by)
                volume = common_volume(sx, sy, bx, by) if overlap_possible else 0.
                exact_common_calls += int(overlap_possible)
                volumes[key] = volume
            if volume > EPS:
                collisions[index] = True
                hits[index][kind_index] += 1
                record['colliding_poses'] += 1
                record['colliding_pose_indices'].append(index)
                record['maximum_overlap_mm3'] = max(record['maximum_overlap_mm3'], volume)
                if record['minimum_distance_pose_deg'] is None:
                    record['minimum_distance_mm'], record['minimum_distance_pose_deg'] = 0., list(angles)
                if len(record['collision_samples']) < 8:
                    record['collision_samples'].append({'pose_deg': list(angles), 'volume_mm3': volume})
        # Exact BRep distances, ordered by their AABB lower bound. AABB gaps
        # never become reported distances. All collision volumes above are kept.
        if not record['colliding_poses']:
            for gap, index, key in sorted(candidates):
                if gap >= record['minimum_distance_mm'] and record['minimum_distance_pose_deg'] is not None:
                    break
                if key in distances:
                    continue
                sx = samples[index][x][0]
                sy = samples[index][y][0]
                distance = sx.distance_to(sy)
                exact_distance_calls += 1
                distances[key] = distance
                if distance < record['minimum_distance_mm']:
                    record['minimum_distance_mm'], record['minimum_distance_pose_deg'] = distance, list(poses[index])
        records.append(record)
        now = time.monotonic()
        if pair_index == 0 or now-last_progress >= 15 or pair_index+1 == len(pairs):
            print(f'sweep pairs {pair_index+1}/{len(pairs)} · {len(poses)} poses · {now-start:.1f}s · {sum(collisions)} colliding poses', file=sys.stderr, flush=True)
            last_progress = now
    all_reach = [m.chain(*angles)[2] for angles in poses]
    clear_reach = [point for point, collision in zip(all_reach, collisions) if not collision]
    clear_no_nb = [point for point, h in zip(all_reach, hits) if h[0]+h[1] == 0]
    pose_table = [{'index': i, 'pose_deg': list(p), 'own_leg_pairs': h[0], 'shell_cradle_pairs': h[1], 'neighbour_pairs': h[2]}
                  for i, (p, h) in enumerate(zip(poses, hits))]
    return {'quick': quick, 'grids_deg': grids, 'total_poses': len(poses), 'colliding_poses': sum(collisions),
            'colliding_poses_ignoring_neighbours': sum(1 for h in hits if h[0]+h[1]),
            'pose_table': pose_table,
            'clear_poses_deg': [list(p) for p, h in zip(poses, hits) if sum(h) == 0],
            'clear_poses_ignoring_neighbours_deg': [list(p) for p, h in zip(poses, hits) if h[0]+h[1] == 0],
            'pose_table_note': 'colliding_pose_indices in each pair index this table; collision_samples keeps only the first eight.',
            'pairs': records, 'interferences': [r for r in records if r['colliding_poses']],
            'near_misses': [r for r in records if not r['colliding_poses'] and r['minimum_distance_mm'] < m.p['clearance_floor']],
            'skipped_pairs': [{'parts': list(key), 'reason': why} for key, why in sorted(skipped.items())],
            'scope': SCOPE, 'sweep_seconds': time.monotonic()-start,
            'query_counts': {'exact_distance': exact_distance_calls, 'exact_common': exact_common_calls, 'rigid_invariance_cache_hits': invariant_cache_hits},
            'distance_method': 'Exact BRep distances; sorted AABB lower bounds prune queries that cannot reduce the exact minimum. All potentially intersecting configurations receive exact common-volume queries. Rigid-frame and unchanged-angle invariance reuse exact results.'}, {'kinematic_only': reach_bounds(all_reach), 'collision_free_subset': reach_bounds(clear_reach), 'collision_free_ignoring_neighbours': reach_bounds(clear_no_nb)}


def leg_names(m):
    return [n for n in m.parts if m.meta[n]['frame'] != 'body' or n.startswith('j1_')]


def extents(shapes):
    bs = [bbox(sh) for sh in shapes]
    return {'min': [min(b['min'][i] for b in bs) for i in range(3)], 'max': [max(b['max'][i] for b in bs) for i in range(3)]}


def stance_report(m):
    posed = m.pose(**m.p['poses']['stance'])
    foot = bbox(posed['foot'])
    fc = centre(posed['foot'])
    names = leg_names(m)
    e = extents(posed[n] for n in names)
    dx, dy = m.p['body']['depth_X']/2, m.p['body']['width_Y']/2
    return {'pose_deg': m.p['poses']['stance'], 'foot_bottom_z_mm': foot['min'][2],
            'overall_height_mm': m.p['body']['height_Z']-foot['min'][2], 'clock_bottom_clearance_mm': -foot['min'][2],
            'foot_centre_xy_mm': fc[:2], 'stance_width_mm': 2*abs(fc[1]), 'leg_extents_mm': e,
            'leg_neutral_extents_mm': extents(m.parts[n] for n in names),
            'body_bbox_exceedance': {'X_plus_mm': max(0., e['max'][0]-dx), 'X_minus_mm': max(0., -dx-e['min'][0]),
                                      'Y_plus_mm': max(0., e['max'][1]-dy), 'Y_minus_mm': max(0., -dy-e['min'][1])}}


def mass_report(m):
    totals = {'carrier': 0., 'upper': 0., 'lower': 0., 'foot': 0.}
    for n in leg_names(m):
        frame = 'carrier' if n.startswith('j1_') else 'foot' if n == 'foot' else m.meta[n]['frame']
        totals[frame] += m.meta[n]['mass_g']
    allowance = m.p['hardware_allowance_g_per_joint']
    total = sum(totals.values())+3*allowance
    moving = [n for n in leg_names(m) if m.meta[n]['frame'] in ('upper', 'lower')]
    inertia = {}
    for label, angles in [('neutral', (0, 0, 0)), ('stance', tuple(m.p['poses']['stance'][v] for v in ('a', 'b', 'c')))]:
        posed = m.pose(*angles)
        p2, p3, _ = m.chain(*angles)
        axis = rx([0, 1, 0], angles[0])
        def r2(point):
            return norm(cross(sub(point, p2), axis))**2
        inertia[label] = sum(m.meta[n]['mass_g']*r2(centre(posed[n])) for n in moving)+allowance*r2(p3)
    posed = m.pose(**m.p['poses']['stance'])
    weighted = [0., 0., 0.]
    for n in leg_names(m):
        weighted = add(weighted, mul(centre(posed[n]), m.meta[n]['mass_g']))
    p2, p3, _ = m.chain(**m.p['poses']['stance'])
    for point in (m.P1, p2, p3):
        weighted = add(weighted, mul(point, allowance))
    return {'frame_group_g': totals, 'hardware_allowance_g_per_joint': allowance, 'hardware_allowance_total_g': 3*allowance,
            'leg_total_g': total, 'four_legs_g': 4*total, 'cradle_g': m.meta['cradle']['mass_g'],
            'moving_about_j2_g': sum(m.meta[n]['mass_g'] for n in moving)+allowance,
            'moving_inertia_about_j2_gmm2': inertia, 'leg_centroid_stance_mm': mul(weighted, 1/total),
            'method': 'Centroid-lumped sum m*r^2, not tensor inertia. Fixed J1 case/mount included in carrier (hip hardware fixed to the cradle). Foot separate from lower subtotal. Three hardware allowances lumped at P1, posed P2 and P3; moving knee allowance at P3. Neighbors excluded.',
            'clock_mass': 'Catalog complete clock 229 g; retained mass unknown. Body envelope carries zero counted mass.'}


def provenance_echo(value):
    if not isinstance(value, dict):
        return {}
    result = {}
    for key, item in value.items():
        if key in ('status', 'provenance') or key.endswith('_provenance'):
            result[key] = item
        elif isinstance(item, dict):
            child = provenance_echo(item)
            if child:
                result[key] = child
    return result


def export(m, report, out_dir, parameter_path):
    out_dir.mkdir(parents=True, exist_ok=True)
    assembly = cad.Compound(label=m.p['revision']+'-'+m.variant, children=list(m.parts.values()))
    output = out_dir/f'j04-l02-{m.variant}.step'
    cad.export_step(assembly, output, timestamp='2026-11-10T00:00:00+00:00')
    restored = cad.import_step(output)
    original_volume = sum(s.volume for s in m.parts.values())
    volume_error = abs(restored.volume-original_volume)
    bbox_error = max(abs(a-b) for a, b in zip(assembly.bounding_box().size, restored.bounding_box().size))
    if not restored.is_valid or len(restored.solids()) != len(m.parts) or volume_error > 1e-4 or bbox_error > 1e-5:
        raise ValueError(f'STEP round trip failed: solids={len(restored.solids())}/{len(m.parts)}, volume error={volume_error}, bbox error={bbox_error}')
    report.update({'revision': m.p['revision'], 'variant': m.variant, 'status': m.p['status'], 'provenance': m.p['provenance'],
                   'provenance_echo': provenance_echo(m.p), 'build123d': cad.__version__,
                   'parameter_sha256': hashlib.sha256(parameter_path.read_bytes()).hexdigest(),
                   'generator_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   'step_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
                   'step_round_trip': {'solids': len(restored.solids()), 'volume_error_mm3': volume_error, 'bounding_box_error_mm': bbox_error},
                   'assembly_size_mm': vec(assembly.bounding_box().size), 'no_structural_analysis_or_physical_testing': True,
                   'scope': SCOPE, 'viewer_verification': 'Browser/GUI proof unrun here; owned by caller.'})
    meshes = []
    for name, shape in m.parts.items():
        vertices, triangles = shape.tessellate(.25, .2)
        meshes.append({'name': name, 'frame': m.meta[name]['frame'], 'color': m.meta[name]['color'],
                       'vertices': [[round(v.X, 6), round(v.Y, 6), round(v.Z, 6)] for v in vertices], 'triangles': triangles})
    data = {'parts': meshes, 'parameters': m.p, 'variant': m.variant, 'report': report,
            'P1': m.P1, 'P2': m.P2, 'P3': m.P3, 'floor_z': report['stance']['foot_bottom_z_mm'], 'step_file': output.name}
    embedded = json.dumps(data, separators=(',', ':'), allow_nan=False).replace('<', '\\u003c')
    (out_dir/'preview.html').write_text((HERE/'leg-viewer-template.html').read_text().replace('/* MODEL_DATA */', embedded))
    (out_dir/'geometry-check.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    print(json.dumps(report, indent=2, allow_nan=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parameters', type=Path, default=HERE/'j04-l02.example.json')
    parser.add_argument('--out', type=Path)
    parser.add_argument('--variant', choices=('direct', 'proximal'))
    parser.add_argument('--quick', action='store_true', help='Double each sweep step; retain inclusive endpoints')
    args = parser.parse_args()
    start = time.monotonic()
    p, variant = read_parameters(args.parameters, args.variant)
    out_dir = args.out or HERE/'exports'/('l02' if variant == 'direct' else 'l02-proximal')
    m = Model(p, variant).build()
    print(f'built {len(m.parts)} valid solid leaves · {variant}', file=sys.stderr, flush=True)
    checks = pose_checks(m)
    if not checks['rigid_formula_satisfied']:
        raise ValueError('Invalid posed geometry: rigid-chain foot-centre check failed')
    overlaps, inside = neutral_check(m)
    print(f'neutral {len(overlaps)} overlapping pairs · beginning bounded discrete sweep', file=sys.stderr, flush=True)
    result, reach = sweep(m, args.quick)
    report = {'solids': list(m.meta.values()), 'neutral_overlaps': overlaps, 'cradle_windows': m.windows,
              'inside_shell_envelope': inside, 'parameter_interferences': m.findings, 'pose_formula_check': checks,
              'sweep': result, 'interferences': m.findings+result['interferences'], 'near_misses': result['near_misses'],
              'total_poses': result['total_poses'], 'colliding_poses': result['colliding_poses'], 'sweep_seconds': result['sweep_seconds'],
              'stance': stance_report(m), 'reach': reach, 'mass': mass_report(m), 'datums': m.datums,
              'build_seconds_before_export': time.monotonic()-start,
              'brief_conflicts': ['Foot centre target subtracts a world-Z offset, inconsistent with rigid lower-frame posing. Both errors reported.',
                                  'Unchanged example knee.mount_side is inline; proximal requires inboard/outboard and refuses inline.']}
    export(m, report, out_dir, args.parameters)


if __name__ == '__main__':
    main()

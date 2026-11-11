"""J04-L02-F01. Headless, model-derived orthographic packaging figures.

ASSUMES: the named placement-A reports describe this parameter file. Rebuilt
mass/height and parameter fingerprints must agree before a figure is written.
All surfaces are convex projections of individual posed solid tessellations.
These stills preserve the packaging study's envelopes and known interferences.
"""
import sys
sys.dont_write_bytecode = True

import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import signal
import xml.etree.ElementTree as ET

import leg_packaging as lp
import leg_animation as animation

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PARAMETERS = HERE / 'j04-l02.candidate-A-under.json'
COMPARISON = HERE / 'exports/l02-comparison.json'
BRIEF = HERE / 'briefs/J04-L02-FIGURES-BRIEF.md'
TEMPLATE = HERE / 'leg-viewer-template.html'
OUT = HERE.parent / 'figures'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
BACKGROUND = '#f4f1e8'
FONT = 'Helvetica, Arial, sans-serif'
ACTUATORS = ('j1_actuator', 'j2_actuator', 'knee_actuator')
TRANSMISSION = ('pulley_hip', 'pulley_knee', 'belt', 'knee_shaft')
EPS = 1e-7


def relative(path):
    return str(path.relative_to(ROOT))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def hull(points):
    points = sorted(set(points))
    halves = []
    for ordered in (points, list(reversed(points))):
        half = []
        for point in ordered:
            while len(half) >= 2 and cross(half[-2], half[-1], point) <= EPS:
                half.pop()
            half.append(point)
        halves.append(half[:-1])
    result = halves[0]+halves[1]
    assert len(result) >= 3, 'Degenerate projected solid'
    return result


def bounds(points):
    return (min(p[0] for p in points), min(p[1] for p in points),
            max(p[0] for p in points), max(p[1] for p in points))


def intersect(a, b, gap=0):
    return (a[0] < b[2]+gap and b[0] < a[2]+gap
            and a[1] < b[3]+gap and b[1] < a[3]+gap)


def segment_inside(a, b, polygon):
    """Clip a segment to a CCW convex polygon, returning its parameter interval."""
    low, high = 0., 1.
    for p, q in zip(polygon, polygon[1:]+polygon[:1]):
        start, end = cross(p, q, a), cross(p, q, b)
        delta = end-start
        if abs(delta) < EPS:
            if start < -EPS:
                return None
            continue
        t = -start/delta
        if delta > 0:
            low = max(low, t)
        else:
            high = min(high, t)
        if low > high+EPS:
            return None
    return low, high


def rectangle(box):
    x0, y0, x1, y1 = box
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def darken(color):
    rgb = [int(color[i:i+2], 16) for i in (1, 3, 5)]
    return '#'+''.join(f'{round(c*.67):02x}' for c in rgb)


def pale(color):
    rgb = [int(color[i:i+2], 16) for i in (1, 3, 5)]
    paper = [int(BACKGROUND[i:i+2], 16) for i in (1, 3, 5)]
    return '#'+''.join(f'{round(c*.35+p*.65):02x}' for c, p in zip(rgb, paper))


def provenance(path, key, value, printed=None):
    return dict(file=relative(path), key=key, value=value,
                printed=str(value) if printed is None else printed)


class Figure:
    def __init__(self, name, title, palette, brief):
        self.name, self.palette = name, palette
        self.root = ET.Element(f'{{{NS}}}svg', {
            'viewBox': '0 0 1600 1000', 'width': '1600', 'height': '1000',
            'font-family': FONT, 'font-size': '24', 'fill': palette['ink'],
            'role': 'img', 'aria-labelledby': 'title description'})
        self.element('title', id='title').text = title
        self.element('desc', id='description').text = (
            'Orthographic convex projections of the posed front-left CAD leg. '
            'Example dimensions. Nothing is built or tested.')
        self.element('rect', x=0, y=0, width=1600, height=1000, fill=BACKGROUND)
        self.text_boxes, self.labels, self.polygons, self.leaders = [], [], [], []
        self.numbers, self.views, self.dimensions = [], [], []
        self.brief = brief
        self.text(48, 43, 'M.A.C. MODEL 04 · MECHANICAL DEVELOPMENT', color=palette['muted'],
                  sources=[provenance(BRIEF, 'Drawing method / masthead', '04')],
                  letter_spacing='1.6')
        self.text(48, 108, title, size=44)
        self.text(48, 151, 'front-left leg shown', color=palette['muted'])
        footer = re.search(r'`(CAD packaging study J04-L02[^`]+)`', brief).group(1)
        self.text(48, 966, footer, sources=[
            provenance(BRIEF, 'Drawing method / footer / study identifier', '04'),
            provenance(BRIEF, 'Drawing method / footer / study identifier', '02')])

    def element(self, tag, **attributes):
        attributes = {k.replace('_', '-'): str(v) for k, v in attributes.items()}
        return ET.SubElement(self.root, f'{{{NS}}}{tag}', attributes)

    def line(self, a, b, color=None, width=1.4, **attributes):
        return self.element('line', x1=f'{a[0]:.6f}', y1=f'{a[1]:.6f}',
                            x2=f'{b[0]:.6f}', y2=f'{b[1]:.6f}',
                            stroke=color or self.palette['muted'], stroke_width=width,
                            **attributes)

    def text(self, x, y, lines, size=24, color=None, sources=(), label=False, **attributes):
        lines = [lines] if isinstance(lines, str) else lines
        width = max(len(line) for line in lines)*.56*size
        box = (x, y-size, x+width, y+(len(lines)-1)*32+size*.2)
        assert 0 <= box[0] and box[2] <= 1560 and box[1] >= 0 and box[3] <= 990, (lines, box)
        for i, line in enumerate(lines):
            self.element('text', x=x, y=y+32*i, font_size=size,
                         fill=color or self.palette['ink'], **attributes).text = line
        item = dict(text=lines, box=box)
        self.text_boxes.append(item)
        if label:
            self.labels.append(item)
        digits = re.findall(r'\d+(?:\.\d+)?', ' '.join(lines))
        sourced_digits = [str(s['printed']) for s in sources]
        assert digits == sourced_digits, f'Missing numeric provenance: {lines}: {digits} != {sourced_digits}'
        for source in sources:
            self.numbers.append(dict(text=' / '.join(lines), **source))
        return box

    def label(self, view, lines, feature, y, sources=(), side='right'):
        """One margin column, one straight leader, terminating at the feature silhouette."""
        x = view.label_x if side == 'right' else view.left_label_x
        box = self.text(x, y, lines, sources=sources, label=True)
        start = (box[0]-12, y-8) if side == 'right' else (box[2]+12, y-8)
        features = [feature] if isinstance(feature, str) else feature
        candidates = []
        for name in features:
            polygon = view.parts[name]['polygon']
            for p, q in zip(polygon, polygon[1:]+polygon[:1]):
                for i in range(21):
                    anchor = (p[0]+(q[0]-p[0])*i/20, p[1]+(q[1]-p[1])*i/20)
                    candidates.append((math.dist(start, anchor), anchor, name))
        for _, anchor, name in sorted(candidates):
            # The target is touched only at t=1. No leader passes through any solid.
            blocked = False
            for part in view.parts.values():
                interval = segment_inside(start, anchor, part['polygon'])
                if interval and interval[0] < 1-1e-5 and interval[1] > 1e-5:
                    blocked = True
                    break
            if blocked:
                continue
            for other in self.text_boxes[:-1]:
                if segment_inside(start, anchor, rectangle(other['box'])):
                    blocked = True
                    break
            if not blocked:
                self.line(start, anchor, width=1.2)
                self.element('circle', cx=f'{anchor[0]:.6f}', cy=f'{anchor[1]:.6f}',
                             r=3.4, fill=self.palette['ink'])
                self.leaders.append(dict(start=start, end=anchor, feature=name, view=view.name))
                return
        raise ValueError(f'No unobstructed straight leader for {lines} in {view.name}')

    def scale_bar(self, x, y, scale):
        length = float(re.search(r'(\d+) mm scale bar', self.brief).group(1))
        self.line((x, y), (x+length*scale, y), width=3, color=self.palette['ink'])
        for end in (x, x+length*scale):
            self.line((end, y-6), (end, y+6), width=2)
        self.text(x+length*scale+16, y+8, f'{length:g} mm', sources=[
            provenance(BRIEF, 'Drawing method / scale bar', length, f'{length:g}')])

    def check(self):
        for a, b in itertools.combinations(self.text_boxes, 2):
            assert not intersect(a['box'], b['box'], 2), f'Text overlap: {a} / {b}'
        for label in self.text_boxes:
            for part in self.polygons:
                assert not intersect(label['box'], part['box'], 3), f'Text over solid: {label} / {part["name"]}'
        for view in self.views:
            baselines = sorted(label['box'][1] for label in self.labels
                               if view.column_start <= label['box'][0] < view.column_end)
            assert all(b-a >= 56 for a, b in zip(baselines, baselines[1:])), 'Label stack below 56 px'
        for leader in self.leaders:
            for text in self.text_boxes:
                assert not segment_inside(leader['start'], leader['end'], rectangle(text['box'])), 'Leader crosses text'
        for first, second in itertools.combinations(self.leaders, 2):
            a, b, c, d = first['start'], first['end'], second['start'], second['end']
            assert not (cross(a, b, c)*cross(a, b, d) < 0 and cross(c, d, a)*cross(c, d, b) < 0), 'Leaders cross'
        payload = ET.tostring(self.root, encoding='unicode', xml_declaration=True)+'\n'
        root = ET.fromstring(payload)
        assert root.attrib['viewBox'] == '0 0 1600 1000'
        for element in root.iter():
            assert element.tag.split('}')[-1] not in ('script', 'image', 'foreignObject', 'use')
            for key, value in element.attrib.items():
                assert not key.endswith('href') and 'url(' not in value, 'External reference'
            if 'font-size' in element.attrib:
                assert float(element.attrib['font-size']) >= 24
        assert 'CAD packaging study J04-L02 · example dimensions · nothing is built or tested' in payload
        return payload, dict(xml_parse=True, footer=True, no_external_references=True,
                             minimum_font_px=24, label_overlap_assertions=True,
                             label_count=len(self.labels), text_box_count=len(self.text_boxes),
                             leader_count=len(self.leaders), leaders_clear_of_solids_and_text=True,
                             labels=self.labels, leaders=self.leaders,
                             numbers=self.numbers, views=[v.receipt for v in self.views],
                             dimensions=self.dimensions)


class View:
    def __init__(self, figure, model, meshes, name, projection, origin_x, ground_y, scale,
                 label_x, ground, style='normal'):
        self.figure, self.model, self.name = figure, model, name
        self.projection, self.origin_x, self.ground_y, self.scale = projection, origin_x, ground_y, scale
        self.ground, self.label_x = ground, label_x
        self.column_start, self.column_end = label_x-1, label_x+350
        self.parts = {}
        depth_axis = 1 if projection == 'SIDE' else 0
        # Looking along -Y/-X: increasing camera-axis coordinate is nearer.
        for name, vertices in meshes.items():
            polygon = hull([self.point(vertex) for vertex in vertices])
            self.parts[name] = dict(polygon=polygon, box=bounds(polygon),
                                    depth=sum(v[depth_axis] for v in vertices)/len(vertices))
        ordered = sorted(self.parts, key=lambda n: self.parts[n]['depth'])
        for name in ordered:
            part = self.parts[name]
            fill = model.meta[name]['color']
            stroke, width = darken(fill), 1.2
            if style == 'actuators':
                fill = figure.palette['ink'] if name in ACTUATORS else pale(fill)
                stroke = '#ffffff' if name in ACTUATORS else pale(stroke)
                width = 2 if name in ACTUATORS else 1.2
            if style == 'knee' and name == 'knee_actuator':
                fill, stroke, width = figure.palette['ink'], '#ffffff', 2
            if style == 'knee' and name in TRANSMISSION:
                fill, stroke = figure.palette['blue'], darken(figure.palette['blue'])
            if name == 'body_envelope':
                fill, stroke = 'none', figure.palette['muted']
                if style == 'actuators':
                    stroke = pale(stroke)
            figure.element('polygon', points=' '.join(f'{x:.6f},{y:.6f}' for x, y in part['polygon']),
                           fill=fill, stroke=stroke, stroke_width=width,
                           data_part=name, data_view=self.name,
                           data_depth_mm=f'{part["depth"]:.9f}')
            figure.polygons.append(dict(name=name, view=self.name, box=part['box']))
        lo = min(part['box'][0] for part in self.parts.values())-20
        hi = max(part['box'][2] for part in self.parts.values())+20
        figure.line((lo, ground_y), (hi, ground_y), width=1.4)
        self.receipt = dict(name=self.name, projection=projection, pixels_per_mm=scale,
                            ground_z_mm=ground, ground_y_px=ground_y,
                            source_solids=len(self.parts), painter_order=ordered,
                            body='outline', neighbours_drawn=False)
        figure.views.append(self)

    def point(self, vertex):
        horizontal = vertex[0] if self.projection == 'SIDE' else vertex[1]
        return (self.origin_x+self.scale*horizontal,
                self.ground_y-self.scale*(vertex[2]-self.ground))

    def axes(self):
        model, figure = self.model, self.figure
        a, b, c = [model.p['poses']['stance'][k] for k in 'abc']
        p2, p3, _ = model.chain(a, b, c)
        for index, (point, axis) in enumerate(zip((model.P1, p2, p3),
                                                ([1, 0, 0], lp.rx([0, 1, 0], a), lp.rx([0, 1, 0], a)))):
            x, y = self.point(point)
            component = axis[1] if self.projection == 'SIDE' else axis[0]
            if abs(component) > EPS:
                # A tilted normal axis gets its exact foreshortened ring.
                figure.element('ellipse', cx=x, cy=y, rx=10, ry=10*abs(component),
                               fill=BACKGROUND, stroke=figure.palette['blue'], stroke_width=2)
                figure.element('circle', cx=x, cy=y, r=2.7, fill=figure.palette['blue'])
            else:
                vector = (axis[0], -axis[2]) if self.projection == 'SIDE' else (axis[1], -axis[2])
                figure.line((x-34*vector[0], y-34*vector[1]), (x+34*vector[0], y+34*vector[1]),
                            color=figure.palette['blue'], stroke_dasharray='15 5 2 5')
            visible = (self.projection == 'FRONT' and index == 0) or (self.projection == 'SIDE' and index > 0)
            if visible:
                radius = 25
                start, end = -155, -35
                points = [(x+radius*math.cos(math.radians(t)), y+radius*math.sin(math.radians(t)))
                          for t in (start, end)]
                figure.element('path', d=f'M {points[0][0]} {points[0][1]} A {radius} {radius} 0 0 1 {points[1][0]} {points[1][1]}',
                               fill='none', stroke=figure.palette['blue'], stroke_width=2)
                for angle, sign, tip in ((start, 1, points[0]), (end, -1, points[1])):
                    t = math.radians(angle)
                    tangent = (-math.sin(t)*sign, math.cos(t)*sign)
                    normal = (math.cos(t), math.sin(t))
                    for side in (-1, 1):
                        figure.line(tip, (tip[0]+8*tangent[0]+side*4*normal[0],
                                          tip[1]+8*tangent[1]+side*4*normal[1]), color=figure.palette['blue'], width=2)

    def link_dimension(self, start, end, length, key, offset):
        a, b = self.point(start), self.point(end)
        dx, dy = b[0]-a[0], b[1]-a[1]
        normal = (-dy/math.hypot(dx, dy), dx/math.hypot(dx, dy))
        p, q = [(v[0]+normal[0]*offset, v[1]+normal[1]*offset) for v in (a, b)]
        f = self.figure
        f.line(a, p, width=1)
        f.line(b, q, width=1)
        f.line(p, q, color=f.palette['blue'])
        for point in (p, q):
            f.line((point[0]-4, point[1]-4), (point[0]+4, point[1]+4), color=f.palette['blue'])
        x = min(p[0], q[0])-80
        y = (p[1]+q[1])/2
        f.text(x, y, f'{length:g} mm', sources=[provenance(PARAMETERS, key, length, f'{length:g}')])
        f.dimensions.append(dict(kind='link', key=key, endpoints_mm=[start, end], nominal_mm=length))

    def height_dimension(self, value, source):
        f = self.figure
        top = self.point([0, 0, self.model.p['body']['height_Z']])[1]
        x = min(part['box'][0] for part in self.parts.values())-36
        f.line((x, top), (x, self.ground_y), width=1.2)
        for y in (top, self.ground_y):
            f.line((x-6, y), (x+6, y), width=1.8)
            f.line((x+10, y), (x+30, y), width=1)
        f.text(x-5, top-20, f'{value:.1f} mm', sources=[source])
        f.dimensions.append(dict(kind='height', ground_z_mm=self.ground,
                                 clock_top_z_mm=self.model.p['body']['height_Z'],
                                 full_precision_mm=value, printed_mm=f'{value:.1f}'))


def build_models():
    models, meshes, reports = {}, {}, {}
    comparison = json.loads(COMPARISON.read_text())['sweeps']
    for variant in ('direct', 'proximal'):
        p, v = lp.read_parameters(PARAMETERS, variant)
        assert [p['poses']['stance'][k] for k in 'abc'] == [12, -35, 70]
        model = lp.Model(p, v).build()
        models[variant] = model
        posed = model.pose(**p['poses']['stance'])
        meshes[variant] = {}
        for name, shape in posed.items():
            if name.startswith('nb_'):
                continue
            assert shape.is_valid
            vertices, _ = shape.tessellate(.25, .2)
            meshes[variant][name] = [tuple(v) for v in vertices]
        key = f'A-under-{variant} · fine'
        row = comparison[key]
        assert row['parameter_sha256'] == sha(PARAMETERS), 'Report parameters differ'
        calculated = dict(mass=lp.mass_report(model)['leg_total_g'],
                          height=lp.stance_report(model)['overall_height_mm'],
                          length=p['links']['L1'])
        for field, actual in [('mass', row['mass']['leg_total_g']), ('height', row['stance']['overall_height_mm'])]:
            assert math.isclose(calculated[field], actual, abs_tol=1e-6), f'Rebuilt {variant} {field} differs'
        # The brief supplies only an independent cross-check, never display data.
        expected = re.search(r'direct ([\d.]+) g,\s*([\d.]+) mm, ([\d.]+) mm; belt ([\d.]+) g,\s*([\d.]+) mm, ([\d.]+) mm', BRIEF.read_text())
        values = [float(value) for value in expected.groups()]
        offset = 0 if variant == 'direct' else 3
        assert [round(calculated[k], 1) for k in ('mass', 'height', 'length')] == values[offset:offset+3], 'Study cross-check differs'
        reports[variant] = dict(key=key, row=row, rebuilt=calculated)
        print(f'Built {variant} · {len(meshes[variant])} front-left/body/cradle solids · report agrees', flush=True)
    return models, meshes, reports


def make_figures(models, meshes, reports, palette, brief):
    direct = models['direct']
    ground = reports['direct']['row']['stance']['foot_bottom_z_mm']
    scale = 2.2
    figures = []
    f = Figure('leg-axes.svg', 'One leg, three powered axes', palette, brief)
    side = View(f, direct, meshes['direct'], 'SIDE', 'SIDE', 230, 760, scale, 475, ground)
    front = View(f, direct, meshes['direct'], 'FRONT', 'FRONT', 1005, 760, scale, 1260, ground)
    f.text(100, 208, 'SIDE', color=palette['muted'])
    f.text(900, 208, 'FRONT', color=palette['muted'])
    for view in (side, front):
        view.axes()
    f.label(side, 'J2 hip swing', ('upper_horn_plate', 'upper_idler_plate'), 574,
            [provenance(HERE/'leg_packaging.py', 'Model.axes[1] / hip swing', 2)])
    f.label(side, 'J3 knee', ('lower_horn_plate', 'lower_idler_plate'), 650,
            [provenance(HERE/'leg_packaging.py', 'Model.axes[2] / knee', 3)])
    f.label(side, 'Foot', 'foot', 738)
    f.label(front, 'J1 hip spread', ('j1_actuator', 'carrier_horn_plate', 'carrier_idler_plate'), 552,
            [provenance(HERE/'leg_packaging.py', 'Model.axes[0] / hip spread', 1)])
    body = direct.p['body']
    f.label(front, ['Body (clock)', f'{body["width_Y"]:g} × {body["depth_X"]:g} × {body["height_Z"]:g} mm'],
            'body_envelope', 330, [provenance(PARAMETERS, f'body.{k}', body[k], f'{body[k]:g}')
                                    for k in ('width_Y', 'depth_X', 'height_Z')])
    p2, p3, p4 = direct.chain(**direct.p['poses']['stance'])
    side.link_dimension(p2, p3, direct.p['links']['L1'], 'links.L1_direct', 110)
    side.link_dimension(p3, p4, direct.p['links']['L2'], 'links.L2', 95)
    f.scale_bar(100, 856, scale)
    figures.append(f)

    f = Figure('actuator-space.svg', 'Where the three actuators sit', palette, brief)
    side = View(f, direct, meshes['direct'], 'SIDE', 'SIDE', 230, 742, scale, 475, ground, 'actuators')
    front = View(f, direct, meshes['direct'], 'FRONT', 'FRONT', 1005, 742, scale, 1260, ground, 'actuators')
    f.text(100, 208, 'SIDE', color=palette['muted'])
    f.text(900, 208, 'FRONT', color=palette['muted'])
    f.label(side, 'J2 actuator', 'j2_actuator', 570,
            [provenance(HERE/'leg_packaging.py', 'Model.build / j2_actuator', 2)])
    f.label(side, ['J3 actuator', '(knee)'], 'knee_actuator', 660,
            [provenance(HERE/'leg_packaging.py', 'Model.build / knee_actuator / third axis', 3)])
    f.label(front, 'J1 actuator', 'j1_actuator', 540,
            [provenance(HERE/'leg_packaging.py', 'Model.build / j1_actuator', 1)])
    ac = direct.p['actuator']
    f.element('rect', x=600, y=780, width=925, height=126, rx=5,
              fill='none', stroke=palette['line'], stroke_width=1.5)
    f.text(625, 820, f'Each block: {ac["W"]:g} × {ac["H"]:g} × {ac["D"]:g} mm · {ac["mass_g"]:g} g',
           sources=[provenance(PARAMETERS, f'actuator.{k}', ac[k], f'{ac[k]:g}') for k in ('W', 'H', 'D', 'mass_g')])
    f.text(625, 868, 'Size and mass benchmark, not a selected motor')
    assert len(ACTUATORS) == 3 and len(animation.LEGS) == 4
    f.text(48, 912, 'Three per leg · twelve in all', sources=[])
    f.numbers.extend([provenance(HERE/'leg_packaging.py', 'Model.build / actuator blocks per leg', len(ACTUATORS), 'Three'),
                      provenance(HERE/'leg_animation.py', 'LEGS × Model.build actuator count', len(animation.LEGS)*len(ACTUATORS), 'twelve')])
    f.scale_bar(100, 830, scale)
    figures.append(f)

    f = Figure('knee-layouts.svg', 'Two knee layouts, neither chosen', palette, brief)
    for variant, x, label_x, title in [('direct', 230, 475, 'Direct knee'),
                                       ('proximal', 1030, 1275, 'Belt-driven knee')]:
        model, report = models[variant], reports[variant]
        row, key = report['row'], report['key']
        view = View(f, model, meshes[variant], variant, 'SIDE', x, 754, scale,
                    label_x, row['stance']['foot_bottom_z_mm'], 'knee')
        f.text(x-110, 205, title, size=30)
        f.label(view, 'knee actuator', 'knee_actuator', 634 if variant == 'direct' else 570)
        if variant == 'proximal':
            f.label(view, 'belt and pulleys', ('belt', 'pulley_hip', 'pulley_knee'), 666)
        mass, height = row['mass']['leg_total_g'], row['stance']['overall_height_mm']
        length = model.p['links']['L1']
        height_source = provenance(COMPARISON, f'sweeps.{key}.stance.overall_height_mm', height, f'{height:.1f}')
        view.height_dimension(height, height_source)
        f.text(x-110, 808, f'Leg mass {mass:.1f} g', sources=[
            provenance(COMPARISON, f'sweeps.{key}.mass.leg_total_g', mass, f'{mass:.1f}')])
        f.text(x-110, 846, f'Standing height {height:.1f} mm', sources=[height_source])
        f.text(x-110, 884, f'Upper link {length:g} mm', sources=[
            provenance(PARAMETERS, f'links.L1_{variant}', length, f'{length:g}')])
    f.scale_bar(650, 922, scale)
    figures.append(f)
    return figures


def main():
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('180 second build limit')))
    signal.alarm(180)
    report = dict(state='STOPPED', browser_proof='UNRUN; caller owned',
                  pixel_render='UNRUN; SVGs were not rendered to pixels',
                  brain_freshness='Not established by supplied evidence', figures={})
    OUT.mkdir(exist_ok=True)
    try:
        palette = dict(re.findall(r'--(ink|muted|line|paper|blue):(#[0-9a-fA-F]{6})', TEMPLATE.read_text()))
        models, meshes, reports = build_models()
        figures = make_figures(models, meshes, reports, palette, BRIEF.read_text())
        payloads = {}
        for figure in figures:
            payload, receipt = figure.check()
            payloads[figure.name] = payload
            report['figures'][figure.name] = receipt
        for name, payload in payloads.items():
            (OUT/name).write_text(payload)
        report.update(state='BUILT', method='Posed solid tessellation → orthographic 2D convex hull → far-to-near fill/outline',
                      pose_source=dict(file=relative(PARAMETERS), key='poses.stance', value=models['direct'].p['poses']['stance']),
                      model_cross_checks={k:v['rebuilt'] for k, v in reports.items()},
                      source_sha256={relative(p):sha(p) for p in (PARAMETERS, COMPARISON, TEMPLATE, BRIEF, HERE/'leg_packaging.py', HERE/'leg_animation.py')},
                      sha256={relative(p):sha(p) for p in [Path(__file__)]+[OUT/name for name in payloads]})
    except Exception as error:
        report['error'] = f'{type(error).__name__}: {error}'
        raise
    finally:
        (OUT/'figures-check.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
        signal.alarm(0)
    print('Three SVGs built · XML, numeric provenance and overlap checks passed · pixel/browser proofs UNRUN', flush=True)


if __name__ == '__main__':
    main()

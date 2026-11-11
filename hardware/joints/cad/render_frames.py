"""Decode the offline animation's DOM capture. No browser or network is used."""
import argparse
import base64
import binascii
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import sys
import tempfile

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
SCENES = ('leg', 'overview', 'walk-prototype', 'walk-concept')


class CaptureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_capture = self.in_title = False
        self.capture, self.title, self.count = [], [], 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title':
            self.in_title = True
        if tag == 'script' and attrs.get('id') == 'capture-frames':
            if attrs.get('type') != 'application/json':
                raise ValueError('capture-frames must be application/json')
            self.in_capture = True
            self.count += 1

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_capture = False
        if tag == 'title':
            self.in_title = False

    def handle_data(self, value):
        if self.in_capture:
            self.capture.append(value)
        if self.in_title:
            self.title.append(value)


def render(dump, out):
    parser = CaptureParser()
    parser.feed(Path(dump).read_text(encoding='utf-8'))
    title = ''.join(parser.title).strip()
    if 'CAPTURE ERROR' in title:
        raise ValueError(title)
    if parser.count != 1:
        raise ValueError('Expected one capture-frames script element; run the capture URL and dump the completed DOM')
    data = json.loads(''.join(parser.capture))
    scene, count, w, h = (data[k] for k in ('scene', 'frames', 'w', 'h'))
    if scene not in SCENES:
        raise ValueError('Unknown capture scene')
    if any(type(v) is not int or v < 1 for v in (count, w, h)) or data.get('fps') != 15:
        raise ValueError('Invalid capture dimensions, frame count or fps (expected 15)')
    if len(data['images']) != count:
        raise ValueError('Capture image count does not match frames')
    images = []
    for index, uri in enumerate(data['images']):
        prefix = 'data:image/png;base64,'
        if not isinstance(uri, str) or not uri.startswith(prefix):
            raise ValueError(f'Frame {index} is not a PNG data URL')
        raw = base64.b64decode(uri[len(prefix):], validate=True)
        with Image.open(io.BytesIO(raw)) as im:
            if im.format != 'PNG' or im.size != (w, h):
                raise ValueError(f'Frame {index} has the wrong type or dimensions')
            im.load()
            images.append(im.convert('RGB'))
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    poster, gif, webp = (out/f'{scene}{suffix}' for suffix in ('-poster.png', '.gif', '.webp'))
    images[0].save(poster)
    palette = [im.quantize(colors=256, method=Image.Quantize.MEDIANCUT) for im in images]
    # GIF uses centiseconds; alternate 60/70 ms to average exactly 15 fps.
    gif_times = [round((i+1)*100/15)*10-round(i*100/15)*10 for i in range(count)]
    webp_times = [round((i+1)*1000/15)-round(i*1000/15) for i in range(count)]
    palette[0].save(gif, save_all=True, append_images=palette[1:], duration=gif_times,
                    loop=0, disposal=2, optimize=False)
    images[0].save(webp, save_all=True, append_images=images[1:], duration=webp_times,
                   loop=0, lossless=True, quality=100)
    for path in (gif, webp, poster):
        print(f'{path.name} · {path.stat().st_size} bytes', flush=True)
    return gif, webp, poster


def selftest():
    # ASSUMES: a completed DOM has exactly one capture payload. Test missing/error cases too.
    with tempfile.TemporaryDirectory(prefix='.frame-selftest-', dir=HERE) as tmp:
        tmp = Path(tmp)
        urls = []
        for i in range(3):
            im = Image.new('RGB', (80, 60), '#f5f3e9')
            ImageDraw.Draw(im).rectangle((5+i*20, 10, 20+i*20, 40), fill=('#356c7a', '#d8c6a6', '#283c45')[i])
            stream = io.BytesIO()
            im.save(stream, format='PNG')
            urls.append('data:image/png;base64,'+base64.b64encode(stream.getvalue()).decode())
        payload = dict(scene='leg', frames=3, w=80, h=60, fps=15, images=urls)
        dump = tmp/'dump.html'
        dump.write_text('<title>CAPTURE DONE leg 3</title><script type="application/json" id="capture-frames">'
                        +json.dumps(payload)+'</script>')
        paths = render(dump, tmp/'out')
        for path, expected in zip(paths, (3, 3, 1)):
            with Image.open(path) as im:
                assert im.size == (80, 60) and getattr(im, 'n_frames', 1) == expected, path
                if expected > 1:
                    assert im.info['loop'] == 0
                for i in range(expected):
                    im.seek(i)
                    im.load()
        for text in ('<title>CAPTURE ERROR deliberate test</title>', '<title>Not captured</title>'):
            dump.write_text(text)
            try:
                render(dump, tmp/'bad')
            except ValueError:
                pass
            else:
                raise AssertionError('Missing/error capture accepted')
        print('SELFTEST PASS · GIF 3 frames · WebP 3 frames · poster 1 frame · missing/error DOM refused')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dump', type=Path, nargs='?')
    parser.add_argument('--out', type=Path)
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    try:
        if args.selftest:
            selftest()
        elif args.dump and args.out:
            render(args.dump, args.out)
        else:
            parser.error('Provide <dump.html> --out <folder>, or --selftest')
    except (ValueError, KeyError, TypeError, OSError, binascii.Error, AssertionError) as exc:
        print(f'Cannot render frames: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

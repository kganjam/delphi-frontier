"""Open, phase-driven scientific story diagrams shared by film profiles.

These animate explanations, never model outputs. Recorded imagery is passed in
by the main renderer, and every claim/scope label stays in the edit profile.
"""
import math
from PIL import Image, ImageDraw

WHITE = '#ffffff'
INK = '#142033'
BLUE = '#2457d6'
MUTED = '#65768b'
PALE = '#d4deea'
CORAL = '#ac6260'


def ease(value):
    value = max(0, min(1, value))
    return value * value * (3 - 2 * value)


class Canvas:
    """A small vocabulary of revealed paths, anchored type, and source imagery."""
    def __init__(self, source_image, font):
        self.image = Image.new('RGB', (1920, 1080), WHITE)
        self.draw = ImageDraw.Draw(self.image)
        self.source_image = source_image
        self.font = font

    def text(self, xy, text, size=42, color=INK, serif=False, center=False, bold=False):
        face = self.font(size, bold=bold, serif=serif)
        x, y = xy
        for j, line in enumerate(text.split('\n')):
            left = x - self.draw.textlength(line, font=face) / 2 if center else x
            self.draw.text((left, y+j*round(size*1.18)), line, font=face, fill=color)

    def source(self, asset, box, crop=None, masks=()):
        image = self.source_image(asset)
        if masks:
            image = image.copy()
            draw = ImageDraw.Draw(image)
            for x, y, w, h in masks:
                draw.rectangle((x, y, x+w, y+h), fill=WHITE)
        if crop:
            x, y, w, h = crop
            image = image.crop((x, y, x+w, y+h))
        x, y, w, h = box
        ratio = min(w/image.width, h/image.height)
        image = image.resize((round(image.width*ratio), round(image.height*ratio)), Image.Resampling.LANCZOS)
        self.image.paste(image, (round(x+(w-image.width)/2), round(y+(h-image.height)/2)))

    def path(self, points, progress=1, color=BLUE, width=4, dashed=False, arrow=True, pulse=False):
        lengths = [math.dist(a, b) for a, b in zip(points, points[1:])]
        total = sum(lengths)
        remaining = total*max(0, min(1, progress))
        tip = points[0]
        angle = 0
        for a, b, length in zip(points, points[1:], lengths):
            if remaining <= 0:
                break
            fraction = min(1, remaining/length) if length else 1
            tip = (a[0]+(b[0]-a[0])*fraction, a[1]+(b[1]-a[1])*fraction)
            angle = math.atan2(b[1]-a[1], b[0]-a[0])
            if dashed:
                shown = length*fraction
                for d in range(0, round(shown), 24):
                    end = min(shown, d+12)
                    p = (a[0]+math.cos(angle)*d, a[1]+math.sin(angle)*d)
                    q = (a[0]+math.cos(angle)*end, a[1]+math.sin(angle)*end)
                    self.draw.line((p, q), fill=color, width=width)
            else:
                self.draw.line((a, tip), fill=color, width=width)
            remaining -= length
        if progress > 0 and arrow:
            ends = [(tip[0]-17*math.cos(angle+offset), tip[1]-17*math.sin(angle+offset)) for offset in (-.45, .45)]
            self.draw.line((ends[0], tip, ends[1]), fill=color, width=width)
        if pulse and progress > 0:
            self.draw.ellipse((tip[0]-8, tip[1]-8, tip[0]+8, tip[1]+8), fill=color)

    def dot(self, xy, radius=8, color=BLUE):
        x, y = xy
        self.draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)

    def stage(self, labels, active, y=820):
        positions = [340+i*1240/max(1, len(labels)-1) for i in range(len(labels))]
        self.path([(positions[0], y), (positions[-1], y)], color=PALE, arrow=False, width=3)
        for i, (label, x) in enumerate(zip(labels, positions)):
            self.dot((x, y), 10, BLUE if i <= active else PALE)
            self.text((x, y+26), label, 31, BLUE if i == active else MUTED, center=True)


def adversarial(c, spec, phase):
    stage = spec['stage']
    names = ['Propose', 'Test', 'Revise']
    title = ['Propose a candidate', 'Challenge its assumptions', 'Revise the design'][stage]
    c.text((90, 145), title, 66, serif=True)
    c.source(spec['candidate'], (555, 320, 810, 440), [210, 65, 250, 145], [(112,151,134,16),(181,131,14,14)])
    labels = spec.get('questions', ['Lift', 'Energy', 'Strength', 'Control'])
    positions = [(300, 355), (1620, 355), (300, 615), (1620, 615)]
    targets = [(710, 445), (1210, 445), (710, 560), (1210, 560)]
    for i, (label, pos, target) in enumerate(zip(labels, positions, targets)):
        c.text(pos, label, 43, center=True, color=BLUE if stage == 1 else INK)
        start = (pos[0]+(125 if pos[0]<960 else -125), pos[1]+35)
        c.path([start, target], ease(phase*1.7-i*.16), dashed=stage == 1, pulse=True)
    c.stage(names, stage)


def tradeoff(c, spec, phase):
    c.text((90, 145), 'What does extra lift cost?', 64, serif=True)
    c.source(spec['candidate'], (650, 370, 620, 350), [210, 65, 250, 145], [(112,151,134,16),(181,131,14,14)])
    labels = [('Lift?', (960, 275), [(960, 420), (960, 340)]),
              ('Drag?', (1590, 490), [(1230, 520), (1440, 520)]),
              ('Strength?', (960, 770), [(960, 650), (960, 750)]),
              ('Energy?', (310, 490), [(690, 520), (470, 520)])]
    for i, (text, pos, points) in enumerate(labels):
        c.text(pos, text, 48, BLUE if i == int(phase*3.99) else INK, serif=True, center=True)
        c.path(points, ease(phase*2.1-i*.28), pulse=True)


def composition(c, spec, phase):
    c.text((90, 145), 'Shared inputs. Explicit interfaces.', 64, serif=True)
    c.text((275, 365), 'Design constraints', 43, serif=True, center=True)
    c.text((275, 440), 'Mass · Area · Span', 35, BLUE, center=True)
    c.text((1010, 300), 'Glide model', 45, serif=True, center=True)
    c.text((1010, 650), 'Fin-load model', 45, serif=True, center=True)
    c.text((1630, 650), 'Beam model', 45, serif=True, center=True)
    c.path([(495, 425), (650, 425), (650, 340), (815, 340)], ease(phase*2.2), pulse=True)
    c.text((685, 240), 'mass · area · span', 29, BLUE, center=True)
    c.path([(495, 425), (650, 425), (650, 690), (810, 690)], ease((phase-.12)*2.2), pulse=True)
    c.text((670, 740), 'span', 29, BLUE, center=True)
    c.path([(1210, 690), (1455, 690)], ease((phase-.37)*2.7), dashed=True, color=CORAL, pulse=True)
    c.text((1370, 755), 'load + length\nassumptions', 29, CORAL, center=True)
    if phase > .60:
        c.text((1000, 450), 'Identity mappings preserve\nunits and declared scope', 33, MUTED, center=True)


def experiment(c, spec, phase):
    c.text((90, 145), 'Choose readings that resolve the unknowns', 58, serif=True)
    for i, (label, result) in enumerate([('Load + deflection', 'Separates load and stiffness'),
                                        ('Two deflections', 'Ambiguity remains')]):
        y = 365+i*310
        c.text((115, y), label, 43, serif=True)
        # A schematic beam and readout arrows, without synthetic response data.
        c.draw.line((640, y-20, 640, y+100), fill=INK, width=7)
        c.path([(640, y+65), (1085, y+65)], arrow=False, color=INK, width=6)
        if i == 0:
            c.path([(1070, y-45), (1070, y+38)], ease(phase*2.2), color=BLUE)
            c.path([(1160, y+10), (1160, y+110)], ease((phase-.12)*2.5), color=BLUE)
        else:
            c.path([(1120, y+10), (1120, y+110)], ease(phase*2.2), color=BLUE)
            c.path([(1190, y+10), (1190, y+110)], ease((phase-.12)*2.5), color=BLUE)
        if phase > .35:
            c.text((1295, y+5), result, 32, BLUE if i==0 else CORAL)


def knowledge(c, spec, phase):
    p0, p1 = spec.get('phase_range', [0, 1])
    phase = p0+(p1-p0)*phase
    c.text((90, 145), 'A finding changes what comes next', 64, serif=True)
    c.text((290, 390), 'Simulation result', 44, serif=True, center=True)
    c.text((960, 390), 'Claim + evidence', 44, serif=True, center=True)
    c.text((1630, 390), 'Dependent design', 44, serif=True, center=True)
    c.path([(500, 430), (725, 430)], ease(phase*2.7), pulse=True)
    c.path([(1185, 430), (1420, 430)], ease((phase-.27)*2.7), pulse=True)
    for i, text in enumerate(['Conditions', 'Uncertainty', 'Disagreement']):
        x = 620+i*340
        c.path([(960, 490), (960, 565), (x, 565), (x, 640)], ease((phase-.10-i*.10)*2.5), dashed=i==2, color=CORAL if i==2 else BLUE)
        c.text((x, 675), text, 34, CORAL if i==2 else MUTED, center=True)
    if phase > .52:
        c.text((1630, 480), 'Flag for review', 31, BLUE, center=True)
    if phase > .70:
        c.path([(1615, 565), (1615, 815), (285, 815), (285, 505)], ease((phase-.70)*3.5), color=BLUE, pulse=True)
        c.text((960, 835), 'The next question starts with more knowledge', 32, BLUE, center=True)


def phrase(c, spec, phase):
    c.text((960, 345), 'From a sentence', 90, serif=True, center=True)
    c.path([(600, 515), (1320, 515)], ease(phase*1.8), arrow=False, width=5)
    if phase > .18:
        c.text((960, 575), 'to an organism', 90, BLUE, serif=True, center=True)


def image_reveal(c, spec, phase):
    c.text((90, 145), spec['headline'], 62, serif=True)
    c.source(spec['image'], spec['box'], spec.get('crop'))
    if phase < .55:
        x, y, w, h = spec['reveal_box']
        remaining = 1-ease((phase-.15)/.40)
        c.draw.rectangle((x+w*(1-remaining), y, x+w, y+h), fill=WHITE)
    if phase > .55:
        c.text((1500, 775), 'Recheck\ndependent\ndesigns', 34, BLUE)


LAYOUTS = {'adversarial': adversarial, 'tradeoff': tradeoff,
           'composition': composition, 'experiment': experiment,
           'knowledge': knowledge, 'phrase': phrase, 'image-reveal': image_reveal}


def render(spec, phase, source_image, font):
    canvas = Canvas(source_image, font)
    LAYOUTS[spec['kind']](canvas, spec, max(0, min(1, phase)))
    return canvas.image

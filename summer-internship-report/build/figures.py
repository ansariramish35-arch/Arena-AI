"""All figures for the internship report."""
import math

from reportlab.lib.colors import HexColor, white
from reportlab.graphics.shapes import Wedge, Circle, Line
from diagramkit import (Canvas, finish, NAVY, NAVY_D, GREEN, GREEN_L, GREEN_M,
                        SAND, BLUE_L, GREY, GREY_L, RULE, ORANGE, RED, FB, FI, F)

W = 720  # default canvas width (points) -> renders ~160 mm wide at 300 dpi


# ---------------------------------------------------------------- cover motif
def cover_motif():
    c = Canvas(760, 120, bg=None)
    # three soft arcs suggesting circularity
    c.d.add(Wedge(90, 60, 52, 20, 340, fillColor=GREEN_L, strokeColor=None))
    c.d.add(Wedge(90, 60, 40, 20, 340, fillColor=white, strokeColor=None))
    c.d.add(Wedge(90, 60, 30, 200, 520, fillColor=GREEN_M, strokeColor=None))
    c.d.add(Wedge(90, 60, 22, 200, 520, fillColor=white, strokeColor=None))
    c.text(180, 42, 'SwachhAI', 26, FB, NAVY_D)
    c.text(180, 62, 'AI-guided waste segregation and circularity assistant', 10.5, FI, GREEN)
    c.arrow(180, 84, 560, 84, GREEN, 1.1)
    for i, lab in enumerate(['Perceive', 'Decide', 'Act', 'Learn']):
        x = 190 + i * 95
        c.d.add(Line(x, c._y(84), x, c._y(78), strokeColor=GREEN, strokeWidth=1))
        c.text(x, 96, lab, 8, FB, GREY, 'center')
    finish(c, 'fig_cover_motif.png')


# ------------------------------------------------------- 1. AI / ML nesting
def fig_ai_stack():
    c = Canvas(W, 330)
    layers = [(20, 20, 680, 292, 'ARTIFICIAL INTELLIGENCE',
               'systems that perform tasks we associate with human intelligence', None, NAVY),
              (60, 62, 600, 212, 'MACHINE LEARNING',
               'programmes that learn patterns from data instead of hand-written rules', BLUE_L, NAVY),
              (100, 104, 520, 132, 'DEEP LEARNING',
               'many-layered neural networks for images, speech and language', GREEN_L, GREEN)]
    for x, y, w, h, title, sub, fill, stroke in layers:
        c.rect(x, y, w, h, fill=fill, stroke=stroke, lw=1.1, radius=4)
        c.text(x + 14, y + 20, title, 10, FB, stroke)
        c.text(x + 14, y + 33, sub, 7.8, FI, GREY)
    # innermost nested layer
    c.rect(140, 146, 440, 50, fill=HexColor('#FBF3E4'), stroke=ORANGE, lw=1.1, radius=4)
    c.text(154, 164, 'GENERATIVE AI & LARGE LANGUAGE MODELS', 9.4, FB, ORANGE)
    c.text(154, 177, 'models that produce new text, code, audio or images', 7.6, FI, GREY)
    # the internship's focus cards
    c.card(150, 206, 200, 74, 'Prompt Engineering',
           'how a request is written so that the model answers usefully, safely and in '
           'a predictable shape', BLUE_L, NAVY, 8.6, 7.4, 7)
    c.card(370, 206, 200, 74, 'RAG and Agentic AI',
           'how the model is given real documents to quote and tools to act with, '
           'instead of relying on memory', BLUE_L, NAVY, 8.6, 7.4, 7)
    c.text(360, 300, 'The shaded cards mark where the internship placed its technical focus.',
           7.8, FI, GREY, 'center')
    c.text(20, 316, 'Each ring is a subset of the one around it: all generative AI is AI, but not all AI is generative.',
           7.4, FI, GREY)
    finish(c, 'fig_ai_stack.png')


# ----------------------------------------------- 2. LLM next-token pipeline
def fig_llm_pipeline():
    c = Canvas(W, 250)
    steps = [
        ('Prompt', 'a question or an\nitem description'),
        ('Tokenise', 'text split into\ntokens / sub-words'),
        ('Embed', 'each token becomes\na numeric vector'),
        ('Transformer\nblocks', 'attention weighs the\ncontext of every token'),
        ('Probability\nover vocabulary', 'scores for the most\nlikely next token'),
        ('Generated\nresponse', 'tokens appended until\nthe answer is complete'),
    ]
    bw, gap = 100, 20
    x = 20
    for i, (t, b) in enumerate(steps):
        c.rect(x, 70, bw, 96, fill=BLUE_L if i % 2 == 0 else GREEN_L,
               stroke=NAVY if i % 2 == 0 else GREEN, lw=1.0, radius=3)
        lines = t.split('\n')
        for j, ln in enumerate(lines):
            c.text(x + bw / 2, 90 + j * 12, ln, 8.6, FB, NAVY_D, 'center')
        c.wrap(x + 5, 108 + 4, bw - 10, b, 7.4, F, GREY, leading=9.2, align='center')
        if i < len(steps) - 1:
            c.arrow(x + bw + 2, 118, x + bw + gap - 2, 118, GREEN, 1.0)
        x += bw + gap
    c.arrow(170, 190, 100, 172, GREEN_M, 0.9, dash=[2.5, 2], both=True)
    c.text(196, 186, 'repeat for every new token', 7.6, FI, GREEN)
    c.text(20, 40, 'The model does not "look up" an answer; it predicts the most probable continuation, '
                   'conditioned on the prompt and on the text generated so far.', 8, F, GREY)
    finish(c, 'fig_llm_pipeline.png')


# ---------------------------------------------------------- 3. RAG pipeline
def fig_rag():
    c = Canvas(W, 372)
    c.text(20, 22, 'A \u00b7 BUILD THE KNOWLEDGE INDEX  (done once, then refreshed)', 8.6, FB, GREEN)
    c.rect(20, 30, 680, 1, fill=RULE, stroke=None)
    docs = ['SWM Rules 2016', 'E-Waste Rules 2022', 'Battery Rules 2022', 'CPCB notes',
            'MoHUA / SBM-U guidance', 'BIS resin codes']
    for i, d in enumerate(docs):
        c.card(20 + i * 114, 40, 106, 30, d, fill=GREY_L, stroke=RULE, title_size=7.4, pad=5)
    c.arrow(360, 72, 360, 86, GREY, 1.0)
    c.card(240, 88, 240, 30, 'Split into passages  \u2192  embed  \u2192  store as vectors',
           fill=BLUE_L, stroke=NAVY, title_size=8, pad=7)
    c.arrow(360, 120, 360, 134, GREY, 1.0)
    c.card(258, 136, 204, 26, 'Vector index (retrieval corpus)', fill=NAVY, stroke=NAVY,
           title_size=8, tcolor=white, pad=6)

    c.text(20, 184, 'B \u00b7 ANSWER A QUESTION  (every time a user asks something)', 8.6, FB, GREEN)
    c.rect(20, 192, 680, 1, fill=RULE, stroke=None)
    steps = [('Question', 'plain-language waste question'),
             ('Embed', 'same model turns it into a vector'),
             ('Retrieve', 'nearest passages from the index'),
             ('Re-rank', 'keep the sentences that truly match'),
             ('Compose', 'LLM writes using only those passages'),
             ('Cite / refuse', 'citations attached; refuse if thin')]
    bw, gap = 100, 16
    x = 20
    for i, (t, b) in enumerate(steps):
        fill = GREEN_L if i in (0, 5) else BLUE_L
        stroke = GREEN if i in (0, 5) else NAVY
        c.rect(x, 200, bw, 88, fill=fill, stroke=stroke, lw=1.0, radius=3)
        c.text(x + bw / 2, 218, '%d' % (i + 1), 7.4, FB, stroke, 'center')
        c.text(x + bw / 2, 232, t, 8.4, FB, NAVY_D, 'center')
        c.wrap(x + 6, 240, bw - 12, b, 7.3, F, GREY, leading=9, align='center')
        if i < len(steps) - 1:
            c.arrow(x + bw + 1, 244, x + bw + gap - 1, 244, GREEN, 1.0)
        x += bw + gap
    # elbow from index to Retrieve
    c.line(360, 162, 360, 170, NAVY, 0.9)
    c.line(360, 170, 314, 170, NAVY, 0.9)
    c.arrow(314, 170, 314, 198, NAVY, 0.9)
    c.text(366, 170, 'the same vector space on both sides', 7.2, FI, GREEN)
    c.rect(20, 306, 680, 56, fill=HexColor('#FBF3E4'), stroke=ORANGE, lw=0.9, radius=4)
    c.text(34, 324, 'THE GROUNDING RULE', 7.8, FB, ORANGE)
    c.wrap(34, 330, 616, 'If the best passage scores below the threshold, the assistant does not fall back '
                         'on what the language model \u201cknows\u201d. It says it cannot answer from the '
                         'available documents and offers two better-formed questions instead.',
           7.5, F, NAVY_D, leading=9.2)
    finish(c, 'fig_rag_pipeline.png')


# ----------------------------------------------------------- 4. agent loop
def fig_agent_loop():
    c = Canvas(W, 260)
    c.text(20, 22, 'Agentic AI: the assistant runs a loop, with a person able to stop it', 10, FB, NAVY_D)
    nodes = [('1  PERCEIVE', 'text, photo or voice;\nHinglish and typos accepted', GREEN, GREEN_L),
             ('2  DECIDE', 'classify the item and\nretrieve the applicable rules', NAVY, BLUE_L),
             ('3  ACT', 'disposal protocol, nudge\nand anonymised log entry', ORANGE, SAND),
             ('4  LEARN', 'patterns propose new\ntaxonomy items for review', HexColor('#3E6B8A'), BLUE_L)]
    x = 20
    for i, (t, b, col, fill) in enumerate(nodes):
        c.rect(x, 48, 152, 92, fill=fill, stroke=col, lw=1.1, radius=4)
        c.text(x + 12, 70, t, 8.8, FB, col)
        c.wrap(x + 12, 78, 128, b, 7.6, F, GREY, leading=9.4)
        if i < 3:
            c.arrow(x + 154, 94, x + 174, 94, GREEN, 1.1)
        x += 176

    # return path
    c.line(96, 142, 96, 166, GREY, 0.9)
    c.line(96, 166, 654, 166, GREY, 0.9)
    c.arrow(654, 166, 654, 142, GREEN, 1.0)
    c.line(654, 166, 654, 166, GREY, 0.9)
    c.text(375, 172, 'the next turn starts with what was learned', 7.4, FI, GREY, 'center')

    c.rect(20, 192, 340, 52, fill=GREEN_L, stroke=GREEN, lw=0.9, radius=3)
    c.text(32, 210, 'HUMAN OVERSIGHT', 7.8, FB, GREEN)
    c.wrap(32, 216, 318, 'a named reviewer approves any change to the taxonomy or the rule '
                         'corpus before it reaches a resident', 7.3, F, GREY, leading=9)

    c.rect(374, 192, 326, 52, fill=GREY_L, stroke=RULE, lw=0.8, radius=3)
    c.text(386, 210, 'WHY A LOOP AND NOT A MENU', 7.8, FB, NAVY)
    c.wrap(386, 216, 304, 'real waste resists fixed lists: a toothbrush is not a bottle, and a swollen '
                          'phone battery is a hazard, not e-waste', 7.3, F, GREY, leading=9)
    finish(c, 'fig_agent_loop.png')


# ------------------------------------------------- 5. one-bag contamination
def fig_contamination():
    c = Canvas(W, 300)
    # left: mixed bag
    c.rect(24, 46, 190, 200, fill=HexColor('#FBF1F1'), stroke=RED, lw=1.0, radius=4)
    c.text(119, 66, 'ONE MIXED BAG', 9.4, FB, RED, 'center')
    items = ['vegetable peels', 'milk pouch with residue', 'used battery',
             'broken glass', 'newspaper', 'food-soaked cardboard', 'CFL tube']
    for i, it in enumerate(items):
        c.text(40, 86 + i * 18, '\u2022', 8.5, FB, RED)
        c.text(52, 86 + i * 18, it, 8.2, F, NAVY_D)
    c.arrow(218, 146, 258, 146, RED, 1.2)
    c.text(238, 134, 'collected', 7, FI, GREY, 'center')
    c.text(238, 166, 'together', 7, FI, GREY, 'center')

    # middle: effects
    effects = [('Recyclables rejected', 'wet residue soaks paper and\ncardboard; bales fail quality checks'),
               ('Workers exposed', 'sharps and mercury lamps are\nreached bare-handed'),
               ('Organics buried', 'food waste rots without air,\nproducing methane at the dumpsite')]
    y = 58
    for t, b in effects:
        c.card(268, y, 200, 54, t, b, fill=GREY_L, stroke=RULE, title_size=8.6, body_size=7.4, pad=6)
        y += 66
    c.arrow(474, 146, 512, 146, RED, 1.2)

    # right: result
    c.rect(520, 46, 176, 200, fill=SAND, stroke=ORANGE, lw=1.0, radius=4)
    c.text(608, 66, 'THE COST', 9.4, FB, ORANGE, 'center')
    costs = ['lower value recovered', 'higher MRF rejection rate',
             'injury risk per shift', 'methane for decades',
             'more landfill volume', 'loss of trust in segregation']
    for i, it in enumerate(costs):
        c.text(540, 90 + i * 21, '\u2013', 8.5, FB, ORANGE)
        c.text(552, 90 + i * 21, it, 8.2, F, NAVY_D)
    c.text(24, 268, 'A single mis-sorted item does not stay a single item: it degrades the whole batch it travels in.', 8, FI, GREY)
    finish(c, 'fig_contamination.png')


# --------------------------------------------- 6. eight SWM stream taxonomy
def fig_streams():
    c = Canvas(W, 325)
    c.text(20, 26, 'The eight streams used by the SwachhAI knowledge graph', 10, FB, NAVY_D)
    c.text(20, 40, 'Grouped as they are collected at the household gate; every item in the project\u2019s '
                   'knowledge base maps to exactly one stream.', 8, FI, GREY)
    groups = [
        ('WET', 'green bin', 'food, peels, garden trim, soiled paper', 'banana peel, tea leaves', GREEN, GREEN_L),
        ('DRY', 'blue bin', 'clean plastic, paper, glass, metal, cartons', 'milk pouch, newspaper', NAVY, BLUE_L),
        ('E-WASTE', 'take-back', 'phones, chargers, appliances, cables', 'old charger, dead phone', NAVY, BLUE_L),
        ('HAZARD', 'separate', 'batteries, CFL tubes, paints, acids, sharps*', 'CFL tube, button cell', RED, HexColor('#FBF1F1')),
        ('SANITARY', 'wrapped', 'diapers, sanitary pads, masks', 'used mask, diaper', ORANGE, HexColor('#FBF3E4')),
        ('TEXTILE', 'reuse first', 'clothes, curtains, footwear, bags', 'torn shirt, old shoes', GREEN_M, GREEN_L),
        ('DEBRIS', 'C&D route', 'tiles, concrete, rubble, broken ceramics', 'broken tile, brick', GREY, GREY_L),
        ('REJECT', 'last resort', 'multi-layer laminate, contaminated film', 'chips packet, foil sachet', HexColor('#6B7280'), HexColor('#F1F3F5')),
    ]
    for i, (name, binlab, items, example, stroke, fill) in enumerate(groups):
        col = i % 4
        row = i // 4
        bx = 20 + col * 172
        by = 62 + row * 118
        c.rect(bx, by, 160, 106, fill=fill, stroke=stroke, lw=1.1, radius=4)
        c.rect(bx, by, 160, 24, fill=stroke, stroke=None, radius=4)
        c.rect(bx, by + 14, 160, 10, fill=stroke, stroke=None)
        c.text(bx + 8, by + 16, name, 9, FB, white)
        c.text(bx + 152, by + 16, binlab, 7.2, FI, white, 'right')
        c.wrap(bx + 9, by + 32, 142, items, 8, F, NAVY_D, leading=10.6)
        c.line(bx + 9, by + 74, bx + 151, by + 74, stroke, 0.5, dash=[2, 2])
        c.text(bx + 9, by + 86, 'for example', 6.6, FB, stroke)
        c.wrap(bx + 9, by + 90, 142, example, 7.4, FI, GREY, leading=9)
    c.text(20, 312, '* Sharps are treated as hazardous household waste: wrap, mark, hand over separately.', 7.6, FI, GREY)
    finish(c, 'fig_streams.png')


# --------------------------------------------------------- 7. waste hierarchy
def fig_hierarchy():
    c = Canvas(W, 320)
    c.text(20, 26, 'The waste hierarchy applied to a household decision', 10, FB, NAVY_D)
    c.text(20, 40, 'SwachhAI does not stop at \u201cwhich bin\u201d. Where an item still has life, the guidance '
                   'prefers the higher rung.', 8, FI, GREY)
    rows = [('1  PREVENT', 'buy less, refuse single-use, choose refillable', GREEN),
            ('2  REUSE', 'repair, donate, refill, share \u2014 textiles and furniture', GREEN_M),
            ('3  RECYCLE', 'clean dry waste to kabadiwala or MRF; e-waste to take-back', NAVY),
            ('4  RECOVER', 'home or community composting; energy recovery', HexColor('#3E6B8A')),
            ('5  SAFE DISPOSAL', 'only what cannot be used: reject and hazardous streams', ORANGE)]
    y = 58
    for i, (t, b, col) in enumerate(rows):
        w = 620 - i * 52
        c.rect(20 + i * 26, y, w, 40, fill=col, stroke=None, radius=2)
        c.text(30 + i * 26, y + 16, t, 9, FB, white)
        c.text(30 + i * 26, y + 29, b, 7.6, F, HexColor('#EAF0F5'))
        y += 46
    c.arrow(676, 268, 676, 62, GREY, 0.9)
    c.text(670, 60, 'preferred', 7, FI, GREY, 'right')
    c.text(670, 272, 'last resort', 7, FI, GREY, 'right')
    finish(c, 'fig_waste_hierarchy.png')


# ------------------------------------------------- 8. SwachhAI architecture
def fig_architecture():
    c = Canvas(W, 436)
    # user layer
    c.rect(20, 18, 680, 58, fill=GREEN_L, stroke=GREEN, lw=1.0, radius=4)
    c.text(34, 37, 'PRESENTATION LAYER', 8.6, FB, GREEN)
    users = ['Household resident', 'Student / hosteller', 'Sanitation worker', 'Ward office']
    for i, u in enumerate(users):
        c.card(40 + i * 168, 42, 150, 26, u, fill=white, stroke=GREEN_M, title_size=8, pad=8)
    c.arrow(360, 78, 360, 90, NAVY, 1.1)

    # orchestration
    c.rect(20, 92, 680, 92, fill=BLUE_L, stroke=NAVY, lw=1.0, radius=4)
    c.text(34, 111, 'ORCHESTRATION LAYER  \u2014  one request pipeline for all three modules', 8.6, FB, NAVY)
    steps = [('Normalise', 'lower-case, aliases'), ('Extract', 'item + material clues'),
             ('Route', 'choose the module'), ('Compose', 'guidance card'),
             ('Log', 'anonymised pattern')]
    for i, (t, b) in enumerate(steps):
        x = 34 + i * 134
        c.card(x, 118, 122, 50, t, b, fill=white, stroke=NAVY, title_size=8, body_size=7.2, pad=6)
        if i < 4:
            c.arrow(x + 124, 143, x + 132, 143, NAVY, 0.9)

    # modules
    c.rect(20, 196, 680, 104, fill=HexColor('#FBF3E4'), stroke=ORANGE, lw=1.0, radius=4)
    c.text(34, 215, 'AI MODULE LAYER', 8.6, FB, ORANGE)
    mods = [('M1  Waste Classifier', 'item \u2192 stream + confidence\n+ stepwise protocol'),
            ('M2  Rule Assistant (RAG)', 'question \u2192 grounded, cited\nanswer or refusal'),
            ('M3  Impact Forecaster', 'household inputs \u2192 diversion\n& CO2e estimate')]
    for i, (t, b) in enumerate(mods):
        c.card(40 + i * 214, 222, 200, 64, t, b, fill=white, stroke=ORANGE,
               title_size=8.6, body_size=7.4, pad=7)

    # knowledge
    c.rect(20, 312, 680, 68, fill=GREY_L, stroke=GREY, lw=1.0, radius=4)
    c.text(34, 331, 'KNOWLEDGE & MODEL LAYER', 8.6, FB, GREY)
    kn = [('Knowledge graph', '95 items \u00b7 8 streams'),
          ('Grounding corpus', '20 public rule & science documents'),
          ('Granite-style LLM', 'few-shot prompting + JSON output'),
          ('Coefficient table', 'published, inspectable factors')]
    for i, (t, b) in enumerate(kn):
        c.card(40 + i * 164, 338, 152, 36, t, b, fill=white, stroke=RULE,
               title_size=7.8, body_size=7, pad=5)

    # data & governance
    c.rect(20, 392, 328, 44, fill=white, stroke=NAVY, lw=1.0, radius=4)
    c.text(34, 411, 'DATA LAYER', 8.4, FB, NAVY)
    c.text(34, 426, 'client-side only \u00b7 no uploads \u00b7 no household identifiers', 7.4, F, GREY)
    c.rect(362, 392, 338, 44, fill=white, stroke=GREEN, lw=1.0, radius=4)
    c.text(376, 411, 'GOVERNANCE LAYER', 8.4, FB, GREEN)
    c.text(376, 426, 'human review \u00b7 confidence shown \u00b7 honest refusal', 7.4, F, GREY)

    c.arrow(360, 194, 360, 184, NAVY_D, 0.9)
    c.arrow(360, 308, 360, 300, NAVY_D, 0.9, both=True)
    c.arrow(360, 380, 360, 380, NAVY_D, 0.9)
    c.arrow(360, 384, 360, 392, NAVY_D, 0.9, both=True)
    finish(c, 'fig_architecture.png')


# ------------------------------------------------------- 9. end-to-end flow
def fig_workflow():
    c = Canvas(W, 468)
    c.text(20, 24, 'End-to-end workflow of a single household interaction', 10, FB, NAVY_D)
    c.text(20, 38, 'The same pipeline serves a scanned item, a typed question and a monthly '
                   'impact review.', 8, FI, GREY)

    c.rect(286, 58, 148, 26, fill=NAVY, stroke=None, radius=13)
    c.text(360, 75, 'Resident opens SwachhAI', 8.2, FB, white, 'center')
    c.arrow(360, 84, 360, 92, NAVY, 1.0)
    c.diamond(360, 124, 250, 58, 'What does the resident need?', fill=SAND, stroke=ORANGE, size=8)

    c.arrow(235, 124, 150, 124, ORANGE, 1.0)
    c.arrow(485, 124, 570, 124, ORANGE, 1.0)
    c.text(180, 116, 'an item', 7.6, FI, ORANGE, 'center')
    c.text(540, 116, 'a question', 7.6, FI, ORANGE, 'center')
    c.arrow(360, 153, 360, 168, ORANGE, 1.0)
    c.text(368, 166, 'a review', 7.4, FI, ORANGE)
    c.arrow(150, 126, 150, 176, ORANGE, 1.0)
    c.arrow(570, 126, 570, 176, ORANGE, 1.0)

    c.rect(40, 178, 222, 186, fill=BLUE_L, stroke=NAVY, lw=1.0, radius=4)
    c.text(52, 196, 'M1  CLASSIFICATION PATH', 8.4, FB, NAVY)
    steps1 = ['Normalise text / read photo label', 'Match against 95-item taxonomy',
              'Attach calibrated confidence', 'Compose protocol: safety step first',
              'Show stream colour + impact fact']
    for i, s_ in enumerate(steps1):
        c.card(52, 204 + i * 31, 198, 25, '%d. %s' % (i + 1, s_), fill=white, stroke=RULE,
               title_size=7.6, pad=5)

    c.rect(470, 178, 210, 186, fill=GREEN_L, stroke=GREEN, lw=1.0, radius=4)
    c.text(482, 196, 'M2  GROUNDED ANSWER PATH', 8.4, FB, GREEN)
    steps2 = ['Detect intent: rule question', 'Retrieve top passages from corpus',
              'Re-rank and compose answer', 'Attach numbered citations',
              'Below threshold \u2192 honest refusal']
    for i, s_ in enumerate(steps2):
        c.card(482, 204 + i * 31, 186, 25, '%d. %s' % (i + 1, s_), fill=white, stroke=RULE,
               title_size=7.6, pad=5)

    c.rect(274, 178, 184, 186, fill=HexColor('#FBF3E4'), stroke=ORANGE, lw=1.0, radius=4)
    c.text(286, 196, 'M3  IMPACT REVIEW', 8.4, FB, ORANGE)
    steps3 = ['Read planned quantities', 'Apply published coefficients',
              'Project 12 months', 'Express as familiar equivalents']
    for i, s_ in enumerate(steps3):
        c.card(286, 204 + i * 31, 160, 25, '%d. %s' % (i + 1, s_), fill=white, stroke=RULE,
               title_size=7.4, pad=5)

    c.arrow(151, 364, 300, 400, NAVY, 1.0)
    c.arrow(360, 364, 360, 396, ORANGE, 1.0)
    c.arrow(575, 364, 420, 400, GREEN, 1.0)
    c.rect(258, 402, 204, 28, fill=NAVY_D, stroke=None, radius=3)
    c.text(360, 420, 'Guidance card shown to the resident', 8.2, FB, white, 'center')
    c.arrow(360, 430, 360, 442, NAVY_D, 1.0)
    c.rect(196, 444, 328, 26, fill=GREY_L, stroke=GREY, lw=0.9, radius=3)
    c.text(360, 461, 'Anonymised pattern log  \u2192  quarterly taxonomy review', 7.8, F, GREY, 'center')
    c.arrow(524, 457, 636, 457, GREY, 0.9)
    c.arrow(636, 457, 636, 271, GREY, 0.9, dash=[3, 2])
    c.text(640, 372, 'feeds the', 6.8, FI, GREY)
    c.text(640, 381, 'next review', 6.8, FI, GREY)
    finish(c, 'fig_workflow.png')


# ------------------------------------------------- 10. classifier internals
def fig_classifier():
    c = Canvas(W, 392)
    c.text(20, 24, 'M1 \u00b7 how one item travels through the classifier', 10, FB, NAVY_D)
    c.text(20, 38, 'The resident types or says what they are holding; the system answers with a stream, '
                   'a confidence and four steps.', 8, FI, GREY)
    c.rect(20, 54, 150, 64, fill=GREY_L, stroke=GREY, lw=1.0, radius=4)
    c.text(95, 72, 'INPUT', 7.6, FB, GREY, 'center')
    c.text(95, 90, '\u201cbananna peel\u201d', 9, FI, NAVY_D, 'center')
    c.text(95, 106, 'typo, Hinglish or photo caption', 6.8, F, GREY, 'center')
    c.arrow(172, 86, 194, 86, NAVY, 1.0)

    stages = [('Normalise', 'lower-case the text, map aliases: peel \u2192 food waste, wet'),
              ('Extract', 'item = banana peel; clues = organic, soft, putrescible'),
              ('Match', 'nearest node in the 95-item taxonomy: wet / compost'),
              ('Confidence', 'the few-shot prompt returns 89; the display floor is 75'),
              ('Compose', 'three or four imperative steps, worker-safety step first')]
    y = 54
    for i, (t, b) in enumerate(stages):
        c.rect(196, y, 330, 56, fill=BLUE_L, stroke=NAVY, lw=0.9, radius=3)
        c.text(206, y + 20, '%d  %s' % (i + 1, t), 8.6, FB, NAVY)
        c.wrap(206, y + 26, 310, b, 7.4, F, GREY, leading=9)
        if i < 4:
            c.rect(356, y + 56, 10, 12, fill=NAVY, stroke=None)
            c.text(361, y + 65, '\u25bc', 5.4, F, white, 'center')
        y += 68
    c.arrow(528, 86, 548, 86, NAVY, 1.0)

    # output card
    c.rect(552, 54, 148, 296, fill=white, stroke=GREEN, lw=1.2, radius=4)
    c.rect(552, 54, 148, 26, fill=GREEN, stroke=None, radius=4)
    c.rect(552, 68, 148, 12, fill=GREEN, stroke=None)
    c.text(560, 72, 'OUTPUT CARD', 7.8, FB, white)
    c.text(560, 98, 'banana peel', 9.4, FB, NAVY_D)
    c.text(560, 112, 'STREAM', 6.6, FB, GREEN)
    c.text(560, 124, 'Wet / compost', 8.4, F, NAVY_D)
    c.text(560, 138, 'CONFIDENCE', 6.6, FB, GREEN)
    c.text(560, 155, '89%', 8, FB, GREEN)
    c.rect(560, 160, 120, 7, fill=GREY_L, stroke=RULE, lw=0.5, radius=2)
    c.rect(560, 160, 120 * 0.89, 7, fill=GREEN_M, stroke=None, radius=2)
    c.text(560, 182, 'STEPS', 6.6, FB, GREEN)
    for i, txt in enumerate(['Empty into the green bin', 'Drain excess liquid',
                             'Add to compost or biogas', 'Never mix with dry waste']):
        c.text(560, 195 + i * 12, '\u2022', 6.6, FB, GREEN)
        c.text(568, 195 + i * 12, txt, 7.2, F, NAVY_D)
    c.text(560, 252, 'WHY IT MATTERS', 6.6, FB, GREEN)
    c.wrap(560, 258, 116, 'peels are 70\u201380% water; buried with dry waste they soak '
                          'recyclables and make leachate', 6.9, FI, GREY, leading=8.2)
    c.text(560, 312, 'Not sure? \u2192 rule assistant', 6.6, FB, GREEN)

    # side notes
    c.rect(20, 136, 150, 82, fill=SAND, stroke=ORANGE, lw=0.9, radius=3)
    c.text(28, 152, 'THE 75 FLOOR', 7, FB, ORANGE)
    c.wrap(28, 158, 122, 'if confidence comes back below 75, the item is reported as '
                         '\u201cunknown\u201d and the resident is offered the rule assistant '
                         'instead of a guess', 6.9, F, NAVY_D, leading=8.4)
    c.rect(20, 228, 150, 74, fill=GREY_L, stroke=RULE, lw=0.8, radius=3)
    c.text(28, 244, 'NOT A BLACK BOX', 7, FB, NAVY)
    c.wrap(28, 250, 122, 'every card shows its stream, its confidence and its reason, so the '
                         'decision can be checked', 6.9, F, NAVY_D, leading=8.4)
    c.rect(20, 312, 150, 38, fill=white, stroke=RULE, lw=0.7, radius=3)
    c.wrap(28, 318, 122, 'Photo support was mocked in the project build: the label was typed, '
                         'not read from the image.', 6.6, FI, GREY, leading=8.2)
    finish(c, 'fig_classifier.png')


# --------------------------------------------------------- 11. RAG module
def fig_rag_module():
    c = Canvas(W, 330)
    c.text(20, 24, 'M2 \u00b7 the retrieval-grounded rule assistant', 10, FB, NAVY_D)
    # corpus column
    c.rect(20, 44, 150, 258, fill=GREY_L, stroke=RULE, lw=1.0, radius=4)
    c.text(30, 62, 'CORPUS (20 documents)', 7.8, FB, NAVY)
    docs = ['SWM Rules 2016', 'E-Waste Rules 2022', 'Battery Rules 2022',
            'C&D Rules 2016', 'Plastic Waste Rules', 'CPCB practice notes',
            'MoHUA / SBM-U guides', 'BIS resin codes 1\u20137', 'UNEP / IPCC summaries']
    for i, d in enumerate(docs):
        c.card(30, 70 + i * 24, 130, 20, d, fill=white, stroke=RULE, title_size=7, pad=4)
    c.arrow(172, 172, 200, 172, GREY, 1.0)

    # retrieval
    c.rect(202, 130, 158, 86, fill=BLUE_L, stroke=NAVY, lw=1.0, radius=4)
    c.text(212, 148, 'RETRIEVAL', 8.2, FB, NAVY)
    c.wrap(212, 156, 138, 'question and passages are compared as vectors; the top three '
                          'passages by cosine similarity are kept', 7.3, F, GREY, leading=9)
    c.text(212, 204, 'TF-IDF (demo) \u00b7 embeddings (production)', 6.8, FI, GREY)

    c.arrow(362, 172, 390, 172, NAVY, 1.0)
    # compose
    c.rect(392, 130, 158, 86, fill=HexColor('#FBF3E4'), stroke=ORANGE, lw=1.0, radius=4)
    c.text(402, 148, 'COMPOSE', 8.2, FB, ORANGE)
    c.wrap(402, 156, 138, 'the language model writes an answer using only the retrieved '
                          'sentences and numbers each claim', 7.3, F, GREY, leading=9)
    c.text(402, 204, 'no passage \u2192 no claim', 6.8, FI, GREY)

    c.arrow(552, 172, 580, 172, ORANGE, 1.0)
    # answer
    c.rect(582, 96, 118, 150, fill=white, stroke=GREEN, lw=1.1, radius=4)
    c.rect(582, 96, 118, 22, fill=GREEN, stroke=None, radius=4)
    c.text(588, 111, 'ANSWER + CITATIONS', 7.2, FB, white)
    c.wrap(590, 126, 102, 'Old batteries must never go in a dustbin \u2014 they are '
                          'household hazardous waste [2]. Tape the terminals and return '
                          'them through retail take-back boxes [1]. A swollen cell is a fire '
                          'risk, so isolate it and hand it over urgently.', 7.2, F, NAVY_D, leading=9.4)
    c.line(590, 226, 692, 226, RULE, 0.6)
    c.text(590, 238, 'grounding 93% \u00b7 3 sources shown', 6.6, FI, GREEN)

    # refusal branch
    c.arrow(471, 218, 471, 240, RED, 0.9, dash=[3, 2])
    c.rect(392, 244, 158, 58, fill=HexColor('#FBF1F1'), stroke=RED, lw=0.9, radius=3)
    c.text(402, 260, 'REFUSAL PATH', 7.6, FB, RED)
    c.wrap(402, 266, 138, 'if the best passage scores too low, the system says it does not '
                          'know and offers two better questions', 7, F, GREY, leading=8.6)

    # question input
    c.rect(202, 44, 348, 62, fill=white, stroke=NAVY, lw=1.0, radius=4)
    c.text(212, 62, 'QUESTION', 7.8, FB, NAVY)
    c.text(212, 80, '\u201cWhere should I throw old batteries?\u201d', 8.6, FI, NAVY_D)
    c.text(212, 96, 'any phrasing, any city; municipal bylaws take precedence when they differ',
           6.8, F, GREY)
    c.arrow(376, 108, 376, 128, NAVY, 0.9)
    finish(c, 'fig_rag_module.png')


# ------------------------------------------------------ 12. impact forecaster
def fig_forecaster():
    c = Canvas(W, 330)
    c.text(20, 24, 'M3 \u00b7 from household inputs to a transparent estimate', 10, FB, NAVY_D)
    c.rect(20, 42, 176, 250, fill=BLUE_L, stroke=NAVY, lw=1.0, radius=4)
    c.text(32, 60, 'INPUTS (resident sets)', 8, FB, NAVY)
    sliders = [('Household size', '4 people'), ('Waste per week', '13 kg'),
               ('Segregated today', '30 %'), ('Composted today', '0 %'),
               ('Recycling point nearby', 'yes / no'), ('Composting space', 'yes / no')]
    for i, (t, v) in enumerate(sliders):
        y = 74 + i * 34
        c.text(32, y, t, 7.6, FB, NAVY_D)
        c.text(186, y, v, 7.4, FI, GREY, 'right')
        c.rect(32, y + 5, 154, 6, fill=GREY_L, stroke=RULE, lw=0.4, radius=2)
        c.rect(32, y + 5, 154 * (0.25 + 0.12 * i), 6, fill=GREEN_M, stroke=None, radius=2)
    c.text(32, 274, 'only quantities \u2014 never names or addresses', 6.6, FI, GREY)
    c.arrow(198, 168, 224, 168, NAVY, 1.0)

    # model
    c.rect(226, 82, 178, 196, fill=HexColor('#FBF3E4'), stroke=ORANGE, lw=1.0, radius=4)
    c.text(238, 100, 'COEFFICIENT MODEL', 8, FB, ORANGE)
    c.wrap(238, 106, 130, 'organic share \u00d7 composted mass \u00d7 0.47 kg CO2e per kg, '
                          'plus dry share \u00d7 recycled mass \u00d7 1.1 kg CO2e per kg',
           7.1, F, GREY, leading=8.8)
    c.text(238, 168, 'WHY NOT A TRAINED ML MODEL', 7.2, FB, ORANGE)
    c.wrap(238, 176, 130, 'a household must be able to understand and challenge the '
                          'number; a multiplication can be checked, a network cannot',
           7.1, F, GREY, leading=8.8)
    c.rect(238, 236, 130, 34, fill=white, stroke=RULE, lw=0.6, radius=3)
    c.wrap(244, 240, 118, 'Directional estimates in ranges \u2014 never a certified offset.',
           6.6, FI, NAVY_D, leading=8.4)
    c.arrow(406, 168, 432, 168, ORANGE, 1.0)

    # outputs
    c.rect(434, 42, 266, 250, fill=GREEN_L, stroke=GREEN, lw=1.0, radius=4)
    c.text(448, 60, 'OUTPUTS', 8, FB, GREEN)
    kpis = [('435 kg', 'waste diverted per year'), ('268 kg', 'CO2e avoided per year'),
            ('13 trees', 'equivalent annual absorption'), ('1,400 km', 'petrol driving equivalent')]
    for i, (v, l) in enumerate(kpis):
        y = 76 + i * 40
        c.text(448, y + 12, v, 12, FB, NAVY_D)
        c.text(448, y + 24, l, 7.4, F, GREY)
    c.rect(448, 238, 238, 40, fill=white, stroke=GREEN_M, lw=0.7, radius=3)
    c.text(456, 254, 'SCALE SWITCH', 7, FB, GREEN)
    c.text(456, 268, 'same model, aggregated to a hostel block or a ward', 7, F, GREY)
    c.text(20, 306, 'Worked example: 4 people, 13 kg/week, 30% segregation today, all plan toggles on.', 7.6, FI, GREY)
    finish(c, 'fig_forecaster.png')


# --------------------------------------------- 13. SDG alignment (three rings)
def fig_sdg():
    c = Canvas(W, 372)
    c.text(20, 24, 'How SwachhAI maps to the Sustainable Development Goals', 10, FB, NAVY_D)
    data = [(150, 120, 'SDG 12', 'Responsible Consumption\nand Production', 'PRIMARY', GREEN,
             'Target 12.5 \u2014 substantially reduce\nwaste generation by 2030'),
            (360, 120, 'SDG 11', 'Sustainable Cities\nand Communities', 'SECONDARY', NAVY,
             'Target 11.6 \u2014 reduce the adverse\nenvironmental impact of cities'),
            (570, 120, 'SDG 13', 'Climate Action', 'SECONDARY', HexColor('#3E6B8A'),
             'Target 13.3 \u2014 improve education\nand awareness on climate change')]
    for cx, cy, num, name, tag, col, tgt in data:
        c.d.add(__import__('reportlab').graphics.shapes.Circle(
            cx, c._y(cy), 62, fillColor=GREEN_L if tag == 'PRIMARY' else BLUE_L,
            strokeColor=col, strokeWidth=1.4))
        c.text(cx, cy - 26, num, 11, FB, col, 'center')
        c.wrap(cx - 52, cy - 18, 104, name, 7.4, F, NAVY_D, leading=8.6, align='center')
        c.rect(cx - 32, cy + 74, 64, 15, fill=col, stroke=None, radius=7)
        c.text(cx, cy + 85, tag, 6.6, FB, white, 'center')
        c.wrap(cx - 66, cy + 96, 132, tgt, 7, FI, GREY, leading=8.4, align='center')
    c.line(210, 120, 300, 120, RULE, 0.8, dash=[3, 3])
    c.line(420, 120, 510, 120, RULE, 0.8, dash=[3, 3])
    c.rect(20, 268, 680, 58, fill=GREY_L, stroke=RULE, lw=0.8, radius=4)
    c.text(32, 286, 'ALSO CONTRIBUTES, INDIRECTLY', 7.8, FB, GREY)
    c.wrap(32, 292, 656, 'SDG 8 (decent work \u2014 safer handling for sanitation workers, target 8.8)  \u00b7  '
                         'SDG 3 (good health \u2014 reduced exposure to dumpsite smoke and sharps)  \u00b7  '
                         'SDG 6 (clean water \u2014 less leachate reaching drains)', 7.4, F, GREY, leading=9.4)
    c.text(20, 348, 'The project claims contribution, not attribution: it supports these targets, it does not '
                    'by itself deliver them.', 7.6, FI, GREY)
    finish(c, 'fig_sdg.png')


# --------------------------------------------- 14. responsible AI pillars
def fig_responsible_ai():
    c = Canvas(W, 300)
    c.text(20, 24, 'Responsible AI treated as behaviour, not as a policy paragraph', 10, FB, NAVY_D)
    pillars = [('TRANSPARENCY', 'confidence shown on every card; sources and coefficients published', NAVY),
               ('FAIRNESS', 'Hinglish and typos accepted; shared bins and rented rooms modelled', GREEN),
               ('PRIVACY', 'client-side only \u2014 no uploads, no identifiers, no tracking', HexColor('#3E6B8A')),
               ('ETHICS', 'refuse rather than invent; human safety before recycling purity', ORANGE),
               ('OVERSIGHT', 'a named reviewer approves taxonomy and corpus changes', GREY)]
    w = 130
    for i, (t, b, col) in enumerate(pillars):
        x = 20 + i * 136
        c.rect(x, 44, w, 180, fill=white, stroke=col, lw=1.1, radius=4)
        c.rect(x, 44, w, 30, fill=col, stroke=None, radius=4)
        c.rect(x, 60, w, 14, fill=col, stroke=None)
        c.text(x + w / 2, 64, t, 7.6, FB, white, 'center')
        c.wrap(x + 9, 84, w - 18, b, 7.6, F, NAVY_D, leading=10)
    c.rect(20, 236, 680, 44, fill=GREEN_L, stroke=GREEN, lw=0.8, radius=3)
    c.text(32, 254, 'THE TEST', 7.6, FB, GREEN)
    c.text(32, 268, 'Each of the five is written as an observable behaviour so that a reviewer can '
                    'check whether it happened \u2014 not as an intention.', 7.8, F, NAVY_D)
    finish(c, 'fig_responsible_ai.png')


# ---------------------------------------------------- 15. phased roadmap
def fig_roadmap():
    c = Canvas(W, 250)
    c.text(20, 24, 'A staged path from a campus pilot to city-level analytics', 10, FB, NAVY_D)
    c.line(40, 120, 700, 120, NAVY, 1.2)
    phases = [(90, 'PHASE 1', 'Months 0\u20133', 'Campus pilot', '500 students, 2 hostels;\nbaseline waste audit;\ntaxonomy 95 \u2192 250 items', GREEN),
              (330, 'PHASE 2', 'Months 3\u20139', 'Ward partnership', 'align with ULB routes;\nmultilingual voice input;\ncollection calendars', NAVY),
              (570, 'PHASE 3', 'Months 9\u201318', 'Citizen data layer', 'aggregate-only analytics;\nsociety API; recycler\ntake-back integration', HexColor('#3E6B8A'))]
    for x, tag, when, title, body, col in phases:
        c.d.add(__import__('reportlab').graphics.shapes.Circle(
            x, c._y(120), 5, fillColor=col, strokeColor=white, strokeWidth=1.4))
        c.text(x, 100, tag, 7.6, FB, col, 'center')
        c.text(x, 88, when, 7, FI, GREY, 'center')
        c.rect(x - 82, 140, 164, 74, fill=white, stroke=col, lw=0.9, radius=3)
        c.text(x, 156, title, 8.2, FB, NAVY_D, 'center')
        c.wrap(x - 74, 160, 148, body, 7, F, GREY, leading=8.4, align='center')
    c.text(20, 232, 'Each phase has an exit criterion measured in the field; nothing is claimed as verified '
                    'until the audit data exists.', 7.6, FI, GREY)
    finish(c, 'fig_roadmap.png')


# ------------------------------------------------- 16. stakeholder ecosystem
def fig_ecosystem():
    c = Canvas(W, 300)
    c.text(20, 24, 'Who is involved in the internship, and in what role', 10, FB, NAVY_D)
    c.rect(250, 44, 220, 64, fill=NAVY, stroke=None, radius=4)
    c.text(360, 64, '1M1B', 12.5, FB, white, 'center')
    c.wrap(268, 70, 184, 'One Million for One Billion \u2014 designs and delivers the programme, '
                         'mentors the project and assesses it', 7.2, F, HexColor('#DCE6F0'),
           leading=8.4, align='center')
    boxes = [(30, 140, 190, 68, 'AICTE', 'All India Council for Technical Education \u2014 '
              'lists the internship on the National Internship Portal and co-signs the certificate', GREEN, GREEN_L),
             (265, 140, 190, 68, 'IBM SkillsBuild', 'provides the guided learning plan, digital '
              'badges and the Granite / watsonx technology context', HexColor('#3E6B8A'), BLUE_L),
             (500, 140, 190, 68, 'University of Lucknow', 'Department of CSE \u2014 academic '
              'supervision, evaluation and credit recognition', NAVY, GREY_L)]
    for x, y, w, h, t, b, col, fill in boxes:
        c.card(x, y, w, h, t, b, fill=fill, stroke=col, title_size=9, body_size=7.2, pad=8)
        c.arrow(360, 107, x + w / 2, y - 2, col, 0.9, both=True)
    c.rect(30, 236, 660, 44, fill=SAND, stroke=ORANGE, lw=0.8, radius=3)
    c.text(42, 254, 'STUDENT', 7.8, FB, ORANGE)
    c.text(42, 268, 'Mohammad Ramish Ansari \u00b7 B.Tech CSE, Semester V \u00b7 attends sessions, completes '
                    'the learning plan, and submits the SwachhAI project', 7.8, F, NAVY_D)
    finish(c, 'fig_ecosystem.png')


# ------------------------------------------------------- 17. internship timeline
def fig_timeline():
    c = Canvas(W, 330)
    c.text(20, 24, 'Dates as they appear in the official documents', 10, FB, NAVY_D)
    c.text(20, 38, 'Nothing on this diagram is inferred: each entry comes from a dated line in the '
                   'offer letter, a SkillsBuild certificate, the project document or the completion '
                   'certificate.', 8, FI, GREY)
    c.line(40, 170, 700, 170, RULE, 1.0)
    events = [(70, '27 Jul 2026', 'declaration signed\nand returned'),
              (190, '28 Jul 2026', 'offer letter: internship\nbegins'),
              (330, '01 Aug 2026', 'SkillsBuild plan 1\ncompleted'),
              (455, '05 Aug 2026', 'SkillsBuild plan 2\ncompleted'),
              (580, '14 Sep 2026', 'SwachhAI project\nsubmitted'),
              (680, '22 Sep 2026', 'completion certificate\nissued')]
    for i, (x, d, lab) in enumerate(events):
        up = i % 2 == 0
        col = GREEN if i in (0, 1, 5) else (HexColor('#3E6B8A') if i in (2, 3) else ORANGE)
        c.d.add(Circle(x, c._y(170), 4.2, fillColor=col, strokeColor=white, strokeWidth=1.2))
        if up:
            c.line(x, 166, x, 132, col, 0.7, dash=[2.5, 2.5])
            c.text(x, 126, d, 7.8, FB, col, 'center')
            c.wrap(x - 66, 132, 132, lab, 7, F, GREY, leading=8.6, align='center')
        else:
            c.line(x, 174, x, 196, col, 0.7, dash=[2.5, 2.5])
            c.text(x, 208, d, 7.8, FB, col, 'center')
            c.wrap(x - 66, 214, 132, lab, 7, F, GREY, leading=8.6, align='center')
    c.rect(20, 74, 680, 58, fill=GREY_L, stroke=RULE, lw=0.8, radius=3)
    c.text(32, 92, 'NOTE ON DATES', 7.4, FB, NAVY)
    c.wrap(32, 98, 656, 'The offer letter proposes a six-week window, 28 July to 28 August 2026. The '
                        'completion certificate, which governs this report, records the internship as '
                        'July 2026 to September 2026 and is dated 22 September 2026. The project was '
                        'submitted on 14 September 2026.', 7.5, F, GREY, leading=9)
    c.text(20, 306, 'Timeline drawn to sequence, not to scale.', 7.2, FI, GREY)
    finish(c, 'fig_timeline.png')


# ------------------------------------------------- 18. illustrative mock-up A
def mock_classifier():
    c = Canvas(340, 560)
    c.rect(0, 0, 340, 560, fill=HexColor('#F7F9FA'), stroke=None)
    # phone frame
    c.rect(28, 16, 284, 528, fill=white, stroke=NAVY, lw=1.6, radius=18)
    c.rect(28, 16, 284, 46, fill=NAVY, stroke=None, radius=18)
    c.rect(28, 44, 284, 18, fill=NAVY, stroke=None)
    c.text(48, 44, 'SwachhAI', 12, FB, white)
    c.text(48, 56, 'which bin, in one answer', 6.8, FI, HexColor('#DCE6F0'))
    c.text(292, 44, 'EN', 7, FB, white, 'right')

    c.rect(44, 74, 252, 60, fill=GREY_L, stroke=RULE, lw=0.8, radius=6)
    c.text(56, 90, 'Describe the item', 7.2, FB, GREY)
    c.text(56, 108, 'doodh ka packet', 9.5, FI, NAVY_D)
    c.rect(226, 100, 58, 20, fill=GREEN, stroke=None, radius=4)
    c.text(255, 114, 'ASK', 7.4, FB, white, 'center')

    # result card
    c.rect(44, 144, 252, 214, fill=GREEN_L, stroke=GREEN, lw=1.1, radius=6)
    c.rect(44, 144, 252, 26, fill=GREEN, stroke=None, radius=6)
    c.rect(44, 160, 252, 10, fill=GREEN, stroke=None)
    c.text(56, 162, 'DRY WASTE  \u00b7  BLUE BIN', 8.2, FB, white)
    c.text(56, 186, 'milk pouch (LDPE film)', 9, FB, NAVY_D)
    c.text(56, 200, 'confidence 92%', 7, F, GREY)
    c.rect(56, 206, 228, 6, fill=white, stroke=RULE, lw=0.4, radius=3)
    c.rect(56, 206, 228 * 0.92, 6, fill=GREEN_M, stroke=None, radius=3)
    c.text(56, 224, 'DO THIS', 6.8, FB, GREEN)
    for i, s in enumerate(['Cut open fully and rinse', 'Sun-dry to stop odour',
                           'Bundle with dry waste', 'Hand to blue bin / kabadiwala']):
        c.text(56, 238 + i * 13, '\u2022', 7, FB, GREEN)
        c.text(66, 238 + i * 13, s, 7.4, F, NAVY_D)
    c.rect(56, 296, 228, 48, fill=white, stroke=RULE, lw=0.6, radius=4)
    c.wrap(62, 300, 216, 'WHY: milk pouches are pure LDPE and genuinely recyclable \u2014 '
                         'but only when rinsed and dry.', 6.8, FI, GREY, leading=8.4)
    c.text(56, 352, 'Not sure? Ask the rule assistant \u2192', 6.8, FI, GREEN)

    # chips
    c.text(44, 386, 'QUICK PICKS', 7, FB, GREY)
    chips = ['banana peel', 'CFL tube', 'old charger', 'maggi cup', 'battery', 'torn shirt']
    x, y = 44, 394
    for ch in chips:
        w = 16 + len(ch) * 3.6
        if x + w > 296:
            x, y = 44, y + 22
        c.rect(x, y, w, 17, fill=white, stroke=RULE, lw=0.7, radius=8)
        c.text(x + w / 2, y + 12, ch, 6.6, F, NAVY_D, 'center')
        x += w + 6

    # bottom nav
    c.rect(28, 500, 284, 44, fill=white, stroke=RULE, lw=0.8, radius=1)
    for i, t in enumerate(['Classify', 'Ask', 'Impact']):
        col = GREEN if i == 0 else GREY
        c.text(76 + i * 94, 520, t, 7.2, FB if i == 0 else F, col, 'center')
    c.text(170, 534, 'Illustrative interface mock-up \u2014 not a working application', 6.4, FI, GREY, 'center')
    finish(c, 'fig_mock_classifier.png')


# ------------------------------------------------- 19. illustrative mock-up B
def mock_forecaster():
    c = Canvas(560, 380)
    c.rect(0, 0, 560, 380, fill=white, stroke=None)
    c.rect(0, 0, 560, 36, fill=NAVY, stroke=None)
    c.text(18, 23, 'SwachhAI  \u00b7  Impact Model', 10, FB, white)
    c.text(542, 23, 'illustrative screen', 7, FI, HexColor('#DCE6F0'), 'right')

    # left panel
    c.rect(16, 50, 236, 292, fill=GREY_L, stroke=RULE, lw=0.9, radius=4)
    c.text(28, 68, 'YOUR HOUSEHOLD', 7.6, FB, NAVY)
    rows = [('People', '4'), ('Waste per week', '13 kg'), ('Segregated today', '30 %'),
            ('Composted today', '0 %'), ('Recycling nearby', 'yes'), ('Compost space', 'yes')]
    for i, (k, v) in enumerate(rows):
        y = 84 + i * 26
        c.text(28, y, k, 7.4, F, NAVY_D)
        c.rect(160, y - 9, 78, 14, fill=white, stroke=RULE, lw=0.6, radius=3)
        c.text(238, y, v, 7.2, FB, NAVY, 'right')
    c.rect(28, 246, 210, 82, fill=white, stroke=GREEN, lw=0.8, radius=4)
    c.text(38, 262, 'PLAN TOGGLES', 7, FB, GREEN)
    for i, t in enumerate(['Start home composting', 'Separate dry waste daily',
                           'Find nearest take-back point']):
        c.rect(38, 270 + i * 18, 9, 9, fill=GREEN, stroke=None, radius=1)
        c.line(40, 275 + i * 18, 42, 277 + i * 18, white, 1.1)
        c.line(42, 277 + i * 18, 45.5, 272 + i * 18, white, 1.1)
        c.text(54, 278 + i * 18, t, 7, F, NAVY_D)

    # right panel KPIs
    c.rect(264, 50, 280, 292, fill=GREEN_L, stroke=GREEN, lw=0.9, radius=4)
    c.text(278, 68, 'PROJECTED FOR 12 MONTHS', 7.6, FB, GREEN)
    kpis = [('435 kg', 'newly diverted from landfill'),
            ('268 kg CO2e', 'avoided (modelled)'),
            ('\u2248 13 trees', 'annual absorption equivalent'),
            ('\u2248 1,400 km', 'petrol driving equivalent')]
    for i, (v, l) in enumerate(kpis):
        y = 84 + i * 40
        c.text(278, y + 10, v, 11.5, FB, NAVY_D)
        c.text(278, y + 22, l, 7, F, GREY)
    # bar chart
    c.rect(278, 250, 252, 78, fill=white, stroke=RULE, lw=0.7, radius=3)
    base = 314
    for i, h in enumerate([12, 22, 34, 48, 62]):
        c.rect(292 + i * 44, base - h, 26, h, fill=GREEN_M if i < 4 else GREEN, stroke=None)
    c.line(286, base, 522, base, RULE, 0.7)
    c.text(292, 260, 'kg diverted, months 1\u20135 of the projection', 6.4, FI, GREY)
    c.text(16, 356, 'Illustrative mock-up of the forecaster screen, prepared for this report. The numbers '
                    'are the worked example computed from the published coefficients, not measurements.',
           6.8, FI, GREY)
    finish(c, 'fig_mock_forecaster.png')


# ------------------------------------------------- 20. system context diagram
def fig_context():
    c = Canvas(W, 300)
    c.text(20, 24, 'System context: what SwachhAI talks to, and what it deliberately does not', 10, FB, NAVY_D)
    c.rect(268, 110, 184, 96, fill=NAVY, stroke=None, radius=6)
    c.text(360, 140, 'SwachhAI', 13, FB, white, 'center')
    c.wrap(282, 148, 156, 'classification \u00b7 grounded answers \u00b7 impact estimate',
           7.2, F, HexColor('#DCE6F0'), leading=8.6, align='center')
    nodes = [(40, 60, 'Resident', 'typed or spoken item, question', GREEN, GREEN_L),
             (40, 186, 'Municipal rules', 'public documents used as the ground truth', NAVY, BLUE_L),
             (510, 60, 'Local body', 'optional aggregate stream data (later phase)', HexColor('#3E6B8A'), BLUE_L),
             (510, 186, 'Sanitation worker', 'receives wrapped, marked hazardous items', ORANGE, SAND)]
    for x, y, t, b, col, fill in nodes:
        c.card(x, y, 170, 58, t, b, fill=fill, stroke=col, title_size=8.6, body_size=7.4, pad=7)
        c.arrow(360, 158, x + (170 if x < 300 else 0), y + 28, col, 0.9, both=True)
    c.rect(40, 250, 210, 32, fill=white, stroke=RED, lw=0.8, radius=3, dash=[3, 2])
    c.text(50, 266, 'No photo upload \u00b7 no account \u00b7 no location history', 6.8, F, RED)
    c.rect(268, 250, 240, 32, fill=white, stroke=RED, lw=0.8, radius=3, dash=[3, 2])
    c.text(278, 266, 'No autonomous action on behalf of a household', 6.8, F, RED)
    finish(c, 'fig_context.png')


# ------------------------------------------------- 21. problem root-cause tree
def fig_problem_tree():
    c = Canvas(W, 300)
    c.text(20, 24, 'From observed symptom to addressable cause', 10, FB, NAVY_D)
    c.rect(240, 44, 240, 44, fill=HexColor('#FBF1F1'), stroke=RED, lw=1.0, radius=4)
    c.text(360, 62, 'Mixed household waste reaches', 8.2, FB, RED, 'center')
    c.text(360, 76, 'the collection vehicle', 8.2, FB, RED, 'center')
    causes = [(40, 130, 'Information gap', 'no per-item answer exists at the moment of disposal', NAVY),
              (200, 130, 'Language gap', 'guidance is written in formal English, not in how people speak', GREEN),
              (360, 130, 'Contamination', 'residue on one item spoils a whole dry batch', ORANGE),
              (520, 130, 'Hazard blind spot', 'batteries and sharps look like ordinary rubbish', RED)]
    for x, y, t, b, col in causes:
        c.card(x, y, 158, 58, t, b, fill=white, stroke=col, title_size=8.4, body_size=7.2, pad=7)
        c.arrow(x + 79, y - 2, x + 79, 92, col, 0.9)
    c.rect(40, 222, 638, 54, fill=GREEN_L, stroke=GREEN, lw=1.0, radius=4)
    c.text(52, 240, 'WHAT A DESIGN CAN REALISTICALLY ADDRESS', 7.6, FB, GREEN)
    c.wrap(52, 246, 614, 'the information gap and the language gap directly; contamination and hazard '
                         'exposure indirectly, by changing what leaves the house. Municipal collection, '
                         'transport and processing capacity are outside the scope of a household tool.',
           7.6, F, NAVY_D, leading=9.2)
    finish(c, 'fig_problem_tree.png')


def build_all():
    cover_motif()
    fig_ai_stack()
    fig_llm_pipeline()
    fig_rag()
    fig_agent_loop()
    fig_contamination()
    fig_streams()
    fig_hierarchy()
    fig_architecture()
    fig_workflow()
    fig_classifier()
    fig_rag_module()
    fig_forecaster()
    fig_sdg()
    fig_responsible_ai()
    fig_roadmap()
    fig_ecosystem()
    fig_timeline()
    mock_classifier()
    mock_forecaster()
    fig_context()
    fig_problem_tree()


if __name__ == '__main__':
    build_all()

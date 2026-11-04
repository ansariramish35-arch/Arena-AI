"""Main report chapters 6-10 with references and appendices."""
from model import K, X, E, C, FIGCAP, TABSPEC

CH6 = [
    ('chapter', '6', 'Project Overview: SwachhAI'),

    ('h1', '6.1  Introducing the project'),
    ('p', '<b>SwachhAI</b> is a proposed decision-support assistant that helps an Indian household '
          'put any item into the right waste stream, answers questions about municipal waste rules '
          'from cited public documents, and converts a household\u2019s habits into a visible '
          'estimate of the waste and emissions it avoids. It is not a bin-sorting robot, not a '
          'municipal fleet management system and not a replacement for a collection service. It is '
          'an interface between a confused resident and the rules that already exist.'),
    ('p', 'The name joins <i>swachh</i>, clean, with AI. The project\u2019s one-line statement of '
          'purpose, as recorded in the project document, is to make <i>the right bin the easy '
          'bin</i>. That phrase is the whole design brief: not to educate in the abstract, not to '
          'lecture, but to make the correct action the one that requires the least effort at the '
          'moment of decision.'),
    ('p', 'The scope is deliberately modest. The concept does not change how waste is collected '
          'or processed; it assumes the municipal rules are broadly correct and that collection '
          'exists in some form, and it addresses the step that fails before either of those '
          'matters: the resident\u2019s decision about what goes where.'),
    ('p', 'This chapter introduces the objectives, the problem, the users, the proposed solution '
          'and the sustainable development goals the project contributes to. The technical '
          'description of the three modules follows in '
          + X('Detailed Project Description', 'Chapter 7') + '. As stated in the Abstract, the '
          'project is presented here as a documented design; no working application was built for '
          'this report and none is required for it.'),

    ('h1', '6.2  Project objectives'),
    ('p', 'The project pursued six objectives. Each is written so that it could, in principle, be '
          'shown to have failed \u2014 which is what distinguishes an objective from a hope.'),
    ('numbered', [
        '<b>Remove the guess at the bin.</b> Given an item described in ordinary language \u2014 '
        'including Hinglish, transliteration and misspellings \u2014 return exactly one waste '
        'stream, a stated confidence, and a short disposal protocol.',
        '<b>Make the answer truthful.</b> Where the system is not confident, it must say so rather '
        'than guess; where it answers a policy question, it must answer from cited public '
        'documents and must decline when those documents do not cover the question.',
        '<b>Protect the person who handles the waste.</b> Every protocol for hazardous or sharp '
        'items must lead with a wrap-mark-separate instruction written for the generator, so that '
        'the item never arrives unmarked in a worker\u2019s hands.',
        '<b>Make the benefit visible.</b> Convert a household\u2019s stated habits into an '
        'estimate of kilograms diverted and carbon dioxide equivalent avoided, using published '
        'coefficients that the user can inspect, and label the output as an estimate.',
        '<b>Respect language and circumstance.</b> Accept the way people actually write and speak, '
        'and model shared bins, rented rooms and small homes as normal cases rather than as edge '
        'cases.',
        '<b>Stay inside the household\u2019s privacy.</b> Process input without uploading '
        'photographs, without requiring an account, and without collecting names, addresses or '
        'identifiers.',
    ]),
    ('p', 'Two further requirements shaped the design as much as the objectives. The first was '
          '<b>explainability</b>: a resident must be able to see why the system said what it said, '
          'which is why the classifier displays confidence and the forecaster uses a published '
          'multiplication rather than a trained model. The second was <b>honesty about scope</b>: '
          'the system must not imply that it can settle a compliance question. It offers '
          'decision support for a household, and defers to the local body on any question of law.'),

    ('h1', '6.3  The problem addressed'),
    ('p', 'Chapter 5 established the problem in detail. In one paragraph: Indian households are '
          'expected by the Solid Waste Management Rules, 2016 to segregate waste at source, but '
          'the correct stream for a specific item is often genuinely unclear, the available '
          'guidance is written for regulators rather than residents, and the cost of a wrong '
          'decision is paid downstream \u2014 by a recycler whose bale is rejected, by a '
          'sanitation worker who reaches into a bag containing a broken bulb, and by the '
          'atmosphere in the form of methane from landfilled organics.'),
    ('p', 'SwachhAI addresses the point of decision rather than the point of consequence. The '
          'design bet is that a sufficiently low-effort answer, delivered in the resident\u2019s '
          'own vocabulary at the moment of disposal, changes what leaves the house \u2014 and that '
          'everything downstream improves as a result. That bet is stated as a hypothesis, not as '
          'a result; testing it would require the field pilot described in '
          + X('9.4  Future scope of SwachhAI', 'Section 9.4') + '.'),
    ('p', 'What the project does not address matters equally. It provides no collection, '
          'transport or processing capacity, enforces no rule, and deliberately contains no '
          'mechanism for shaming or ranking a household. It does not resolve conflicts between '
          'municipal bylaws; it defers to the local body. And it does not claim that household '
          'segregation alone solves India\u2019s waste problem \u2014 only that it is a necessary '
          'input that is currently weak.'),

    ('h1', '6.4  Target users'),
    ('p', 'The project defines four user groups. Two are direct users of the assistant, and two '
          'benefit from it without necessarily operating it. Defining all four mattered, because '
          'a design that serves only the first would be a consumer app; a design that serves all '
          'four has to make different choices.'),
    ('table', {
        'key': 'users',
        'widths': [0.20, 0.38, 0.42],
        'header': ['User', 'Situation and need', 'What the design gives them'],
        'rows': [
            ['Urban household head or homemaker',
             'Manages daily kitchen and household disposal; has no time at the bin and no '
             'reliable memory of which item belongs where',
             'A per-item answer in seconds, in ordinary language; a short protocol rather than a '
             'rule; a monthly card showing what changed'],
            ['Student or hosteller',
             'Shares a room and a bin, has almost no space to store segregated waste, and deals '
             'with a specific set of items (food cups, chargers, notebooks, packaging)',
             'Quick-pick entries for hostel items; compact protocols that fit a shared room; '
             'guidance on where to take e-waste on or near campus'],
            ['Sanitation worker (formal and informal)',
             'Handles unmarked sharps, broken glass, acids and mercury-bearing lamps, often with '
             'minimal protective equipment',
             'Resident-side protocols that require wrapping, marking and separate handover before '
             'the item ever reaches a collection round'],
            ['Urban local body and ward waste operations',
             'Receives contaminated loads that make recycling financially difficult, and holds '
             'almost no stream-level data about its own wards',
             'Cleaner inbound streams; in a later phase, anonymised aggregate stream data for '
             'routing, facility planning and tariff design'],
        ],
        'note': 'Personas as defined in the SwachhAI project document; the fourth is a '
                'later-phase user and is not served by the first version of the concept.',
    }),
    ('p', 'One design consequence is worth drawing out. The sanitation worker is listed as a user '
          'even though that worker will never open the application. This is not a rhetorical '
          'gesture: it changes the content of the output. A protocol written only for the '
          'household might say \u201cbatteries go to a take-back point\u201d. A protocol written '
          'with the handler in mind says \u201ctape the terminals, keep the cells in a leak-proof '
          'container, and hand them over separately \u2014 never in the mixed bag\u201d. The second '
          'sentence is longer and it is the one that prevents an injury.'),

    ('h1', '6.5  The proposed solution'),
    ('p', 'SwachhAI is described in the project document as three cooperating modules sharing one '
          'pipeline, rather than as a single model or a single screen. The three modules are '
          'introduced here and described in technical detail in Chapter 7.'),
    ('bullets', [
        '<b>Module 1 \u2014 AI-based waste classification.</b> The resident describes an item in '
        'words (or, in the designed extension, supplies a photograph). The system extracts the item '
        'and its material clues, maps it to exactly one of eight waste streams defined with '
        'reference to the Solid Waste Management Rules, 2016, attaches a calibrated confidence, and '
        'returns a short disposal protocol with a safety step first. Below a confidence of 75 it '
        'returns \u201cunknown\u201d instead of guessing.',
        '<b>Module 2 \u2014 RAG-based waste management assistant.</b> The resident asks a question '
        'in natural language \u2014 \u201cwhere should I throw old batteries?\u201d, \u201cis a '
        'CFL bulb e-waste or hazardous?\u201d The system retrieves passages from a curated corpus '
        'of public documents, composes an answer only from those passages, and attaches numbered '
        'citations. If the best passage scores too low, it declines to answer.',
        '<b>Module 3 \u2014 environmental impact forecaster.</b> The resident sets a few '
        'quantities \u2014 household size, kilograms per week, the fraction currently segregated '
        'and composted \u2014 and switches on the practices they intend to adopt. The system '
        'projects twelve months of diversion and carbon dioxide equivalent avoided using published '
        'coefficients, and expresses the result in familiar equivalents.',
    ]),
    ('p', 'The three modules are not independent features bolted together. They share one input '
          'pipeline, one taxonomy and one privacy contract, and they are designed so that a '
          'failure in one degrades gracefully into another: a low-confidence classification hands '
          'the resident to the rule assistant, and the quantities logged during classification '
          'feed the forecaster. That shared structure is the subject of '
          + X('Detailed Project Description', 'Chapter 7') + '.'),
    ('p', 'AI is not decorative in this design. The problem is <i>linguistic and contextual</i>: '
          'the same item is named differently by different people, rules differ by city, and a '
          'rigid list cannot absorb \u201cdoodh ka packet\u201d, a photograph, or a question about '
          'one\u2019s own municipality. Language understanding, retrieval and prediction are the '
          'capabilities that make the interface possible. A static FAQ page cannot do this job, '
          'which is why the project\u2019s justification for AI is functional rather than '
          'fashionable.'),
    ('figure', 'fig_context.png', FIGCAP('fig_context.png')),

    ('h1', '6.6  Relevance to SDG 11, SDG 12 and SDG 13'),
    ('p', 'The project document aligns SwachhAI with three Sustainable Development Goals and '
          'identifies one as primary. The alignment is stated at the level of specific targets '
          'rather than at the level of goal titles, because a goal title can be claimed by almost '
          'any project while a target can be argued about.'),
    ('table', {
        'key': 'sdg',
        'widths': [0.24, 0.30, 0.46],
        'header': ['Goal and target', 'Relation to the project', 'How the project contributes'],
        'rows': [
            ['SDG 12 \u2014 Responsible Consumption and Production; Target 12.5 '
             '(substantially reduce waste generation through prevention, reduction, recycling and '
             'reuse by 2030)',
             '<b>Primary</b>',
             'The classifier, the rule assistant and the composting and rinsing protocols all '
             'raise prevention, recycling and reuse behaviour at the point where the waste is '
             'generated'],
            ['SDG 11 \u2014 Sustainable Cities and Communities; Target 11.6 (reduce the adverse '
             'per capita environmental impact of cities, with attention to air quality and waste '
             'management)',
             '<b>Secondary</b>',
             'Cleaner separated streams, and in a later phase ward-level stream analytics, support '
             'municipal waste management and reduce dumpsite and burning pollution'],
            ['SDG 13 \u2014 Climate Action; Target 13.3 (improve education, awareness and human '
             'capacity on climate mitigation and adaptation)',
             '<b>Secondary</b>',
             'The forecaster explains landfill methane in plain language and converts a '
             'household\u2019s behaviour into a visible carbon dioxide equivalent figure'],
        ],
        'note': 'Target statements paraphrased from the United Nations Sustainable Development '
                'Goals; see the References.',
    }),
    ('figure', 'fig_sdg.png', FIGCAP('fig_sdg.png')),
    ('p', 'Two further goals are touched indirectly and are recorded in the project document for '
          'completeness: SDG 8, through safer working conditions for sanitation workers, and SDG 3, '
          'through reduced exposure to dumpsite smoke and sharps. The report states its claim '
          'precisely: the project <i>contributes to</i> these targets. It does not deliver them, '
          'and a household tool should not be described as if it did.'),
]

CH7 = [
    ('chapter', '7', 'Detailed Project Description'),

    ('h1', '7.1  The eight waste streams'),
    ('p', 'Every part of SwachhAI depends on one decision made early: the taxonomy. Before a '
          'classifier can classify, and before a corpus can be retrieved, the project has to '
          'decide how many categories exist and what they are called. Too few categories and the '
          'guidance is useless \u2014 \u201cdry waste\u201d does not tell anyone what to do with a '
          'battery. Too many and the system becomes a rulebook that nobody can use at a bin, and '
          'the classifier\u2019s accuracy per category collapses.'),
    ('p', 'The project settled on <b>eight streams</b>, defined with reference to the Solid Waste '
          'Management Rules, 2016 and the separate rules that govern specific material types: '
          '<b>wet</b>, <b>dry</b>, <b>e-waste</b>, <b>hazard</b>, <b>sanitary</b>, '
          '<b>textile</b>, <b>debris</b> and <b>reject</b>. Each of the approximately '
          'ninety-five items in the project\u2019s knowledge base maps to exactly one of these '
          'eight, and the mapping is deliberate rather than incidental: the eight correspond to '
          'the ways in which waste is actually collected and handed over at the household gate, '
          'not to a materials-science classification.'),
    ('figure', 'fig_streams.png', FIGCAP('fig_streams.png')),
    ('table', {
        'key': 'waste',
        'widths': [0.16, 0.44, 0.40],
        'header': ['Stream', 'What belongs here', 'Why the distinction matters'],
        'rows': [
            ['Wet', 'Food waste, vegetable and fruit peels, cooked food residues, garden trimmings, '
                    'soiled paper',
             'Compostable; if mixed with dry waste it soaks and contaminates recyclables'],
            ['Dry', 'Clean plastics and films, paper and cardboard, glass, metals, cartons',
             'Has market value only while clean and dry; the project insists on rinsing and drying '
             'before handover'],
            ['E-waste', 'Phones, chargers, cables, small appliances, batteries inside devices, '
                        'lamps other than CFLs',
             'Governed by the E-Waste (Management) Rules, 2022; must travel through authorised '
             'routes'],
            ['Hazard', 'Batteries, CFL tubes, paints and solvents, acids, sharps, expired '
                       'medicines',
             'Domestic hazardous waste; the safety step for the handler comes first in every '
             'protocol'],
            ['Sanitary', 'Diapers, sanitary pads, masks, contaminated dressings',
             'Must be wrapped before handover; treated separately from wet and dry streams'],
            ['Textile', 'Clothing, curtains, footwear, bags, bedding',
             'Reuse comes before recycling; donation or repair is preferred to the dry bin'],
            ['Debris', 'Tiles, concrete, rubble, broken ceramics, mirrors',
             'Covered by the C&D Waste Management Rules, 2016; should not enter municipal bins'],
            ['Reject', 'Multi-layer laminate packets, foil-lined sachets, heavily contaminated '
                       'film, composite items that cannot be separated',
             'The honest last resort; keeping these out of the dry stream protects the value of '
             'the rest'],
        ],
    }),
    ('p', 'Two aspects of this taxonomy are worth defending. First, <b>textile</b> and '
          '<b>debris</b> are separate streams even though both could be folded into '
          '\u201cdry\u201d. They are separated because the correct action differs: a wearable shirt '
          'should be donated, not binned, and a broken tile must not be put in a municipal bin at '
          'all. Second, <b>reject</b> exists as a stream. A taxonomy that pretends every item is '
          'recyclable produces worse behaviour than one that admits a residual category, because '
          'it pushes laminate packets into the dry stream where they reduce bale quality.'),
    ('p', 'The number <b>ninety-five</b> deserves a note as well. It is the size of the demo '
          'knowledge base, not a claim about the size of the problem; the project\u2019s own '
          'roadmap proposes extending the taxonomy to about 250 items using real user queries from '
          'a campus pilot. The report repeats that number as a description of the design, not as a '
          'measure of coverage.'),

    ('h1', '7.2  Module 1: AI-Based Waste Classification'),

    ('h2', '7.2.1  Purpose'),
    ('p', 'To answer the resident\u2019s question \u2014 <i>where does this go?</i> \u2014 with a '
          'single stream, a stated confidence, and a short sequence of steps that a person can '
          'follow while holding the object. The module exists because the uncertainty in household '
          'segregation is item-specific, and the answer must therefore be item-specific too.'),

    ('h2', '7.2.2  Working concept'),
    ('p', 'The input is an item description in natural language: \u201cdoodh ka packet\u201d, '
          '\u201ctube light\u201d, \u201cbananna peel\u201d, \u201cold charger\u201d. The system '
          'first normalises the text \u2014 lower-casing, splitting into words, and expanding '
          'common aliases so that \u201cdoodh ka packet\u201d, \u201cmilk pouch\u201d and '
          '\u201cmilk packet\u201d converge on the same item. It then extracts the item name and '
          'the material clues around it: \u201cpacket\u201d suggests film, \u201ctube\u201d '
          'suggests glass and mercury, \u201cpeel\u201d suggests organic.'),
    ('p', 'The extracted description is then matched against the taxonomy. The project uses a '
          'Granite-style small language model, prompted with a small number of worked examples, to '
          'perform the match and to explain it. The prompt requires exactly one stream from the '
          'eight, a confidence between 0 and 100, up to four imperative steps, and one factual '
          'note about the material. A deterministic fallback matcher handles the case where the '
          'model output cannot be parsed, and a threshold rule overrides the model when confidence '
          'is below 75: the stream becomes \u201cunknown\u201d and the resident is handed to the '
          'rule assistant instead of being given a guess.'),
    ('p', 'The output is a card, not a sentence. It carries the stream, a colour, the confidence, '
          'the reason, the steps, and an optional impact note. The choice of a structured card '
          'over free text is a deliberate interface decision: it allows the same information to be '
          'rendered on a phone, read aloud, or printed onto a bin label.'),
    ('figure', 'fig_classifier.png', FIGCAP('fig_classifier.png')),

    ('h2', '7.2.3  Technologies involved'),
    ('bullets', [
        'A small instruction-tuned language model of the IBM Granite class, used in a few-shot '
        'prompting configuration',
        'Prompt engineering with a strict JSON output contract, a refusal rule and a tone rule',
        'Alias and normalisation logic (deterministic text processing) in front of the model',
        'A curated taxonomy of approximately ninety-five items across eight streams, with material '
        'clues attached to each',
        'Confidence calibration and a threshold policy applied after the model, not by the model',
    ]),

    ('h2', '7.2.4  Input and expected output'),
    ('table', {
        'key': 'm1',
        'widths': [0.22, 0.78],
        'header': ['Element', 'Description'],
        'rows': [
            ['Input (text)', 'An item description in ordinary language, in English, Hindi '
                             'transliteration or a mixture; typos tolerated'],
            ['Input (image, designed extension)', 'A photograph of the item or of its label. In the '
                                                  'project build this layer was mocked: the label '
                                                  'was typed rather than read from the image, and '
                                                  'the report describes it as a designed, untested '
                                                  'capability'],
            ['Processed fields', 'Item name, material clues, candidate stream, confidence, steps, '
                                 'impact note'],
            ['Expected output', 'A single stream from the eight; a confidence between 0 and 100, '
                                'or the explicit value \u201cunknown\u201d below the threshold; up '
                                'to four imperative steps with the safety step first; one factual '
                                'note'],
            ['Failure behaviour', '\u201cUnknown\u201d plus an offer of the rule assistant; a '
                                  'hazard case always appends a reminder to verify with the local '
                                  'municipal body'],
        ],
    }),

    ('h2', '7.2.5  A practical example'),
    ('callout', '<b>Example \u2014 a typo, a pouch and a tube.</b><br/><br/>'
                '<b>Input:</b> \u201cbananna peel\u201d (misspelt).<br/>'
                '<b>Extraction:</b> item = banana peel; clues = organic, soft, putrescible.<br/>'
                '<b>Result:</b> stream = <b>wet</b>, confidence 89 per cent.<br/>'
                '<b>Steps shown:</b> empty it into the green bin; drain excess liquid; add it to '
                'the compost bin, a community pit or a biogas feed; never mix it with dry '
                'recyclables.<br/>'
                '<b>Impact note:</b> peels are mostly water; buried with dry waste they soak '
                'recyclables and generate leachate.<br/><br/>'
                '<b>Input:</b> \u201cdoodh ka packet\u201d (Hinglish).<br/>'
                '<b>Extraction:</b> item = milk pouch; clues = LDPE film, single layer, liquid '
                'contact.<br/>'
                '<b>Result:</b> stream = <b>dry</b>, confidence 92 per cent.<br/>'
                '<b>Steps shown:</b> cut the pouch open fully and rinse it; sun-dry it to prevent '
                'odour and mould; bundle pouches so that sorters do not miss them; hand them over '
                'with dry waste or to a kabadiwala.<br/><br/>'
                '<b>Input:</b> \u201ctube light\u201d.<br/>'
                '<b>Result:</b> stream = <b>hazard</b>, confidence 94 per cent. The first step is '
                'a safety step: do not break the tube; wrap it, mark it, and hand it over '
                'separately. The card notes that it contains mercury and that it must never enter '
                'a mixed bag.'),
    ('p', 'These three examples are from the project document, which records them as traced '
          'outputs of the demo build. They are reproduced here as <i>illustrations of the intended '
          'behaviour</i>. This report does not present them as independently verified results, and '
          'the confidence values are properties of that build, not of a general model.'),

    ('h1', '7.3  Module 2: RAG-Based Waste Management Assistant'),

    ('h2', '7.3.1  Purpose'),
    ('p', 'The classifier answers \u201cwhich bin\u201d. Many real questions are different: '
          '\u201cIs a CFL bulb e-waste or hazardous?\u201d, \u201cwhere do old batteries go?\u201d, '
          '\u201cdoes my municipality collect e-waste separately?\u201d, \u201cwhat do I do with '
          'expired medicines?\u201d These are questions about rules, and a classifier that guesses '
          'at a rule is worse than no classifier at all. The second module exists to answer them '
          '<b>from documents</b>, with citations, and to decline when the documents do not cover '
          'the question.'),

    ('h2', '7.3.2  Working concept'),
    ('p', 'The module has an offline half and an online half. Offline, a corpus of twenty public '
          'documents is split into passages, each passage is converted into a numeric vector, and '
          'the vectors are indexed. The corpus is deliberately small, public and checkable: the '
          'Solid Waste Management Rules, 2016 and its schedule guidance; the E-Waste (Management) '
          'Rules, 2022 and the Battery Waste Management Rules, 2022; the Construction and '
          'Demolition Waste Management Rules, 2016; the Plastic Waste Management Rules as amended; '
          'CPCB disposal practice notes and landfill advisories; MoHUA and Swachh Bharat Mission '
          'guidance; BIS plastic resin identification codes; and summaries from UNEP and the IPCC.'),
    ('p', 'Online, a question is converted into a vector in the same space, the nearest passages '
          'are retrieved, and a sentence-level re-ranking step keeps the sentences that actually '
          'address the question. The language model is then given those passages and asked to '
          'compose an answer <b>only</b> from them, numbering each claim against the passage it '
          'came from. A guard stage compares the best retrieval score against a threshold; below '
          'it, the system produces a refusal \u2014 an explicit statement that it cannot answer '
          'from the available documents, together with two better-formed questions drawn from the '
          'corpus.'),
    ('figure', 'fig_rag_module.png', FIGCAP('fig_rag_module.png')),
    ('p', 'The refusal path is the most important part of the design and the easiest to omit. A '
          'system that always answers will sometimes answer wrongly, and a wrong answer about '
          'hazardous waste is not a harmless one. The project treats a refusal as a successful '
          'outcome, because it preserves the resident\u2019s ability to trust the answers that '
          'are given.'),

    ('h2', '7.3.3  Technologies involved'),
    ('bullets', [
        'Retrieval-augmented generation, with retrieval, re-ranking and constrained composition '
        'as separate stages',
        'Vector representations of passages and questions; in the demo build a term-frequency '
        'weighting scheme (TF-IDF) was used, and in a production design dense embeddings with a '
        'vector store would replace it \u2014 the same pattern, a different similarity function',
        'A language model of the Granite class, instructed to answer only from the supplied '
        'passages and to cite them',
        'A curated twenty-document corpus of public Indian waste rules and scientific summaries',
        'A grounding threshold that converts an uncertain retrieval into an explicit refusal',
    ]),

    ('h2', '7.3.4  Input and expected output'),
    ('table', {
        'key': 'm2',
        'widths': [0.22, 0.78],
        'header': ['Element', 'Description'],
        'rows': [
            ['Input', 'A natural-language question about waste rules or disposal practice, in any '
                      'phrasing'],
            ['Retrieved evidence', 'The top-ranked passages, each with a source title and a '
                                   'relevance score'],
            ['Expected output', 'A short answer, in at most four points, in which every claim '
                                'carries a numbered citation to a retrieved passage, followed by '
                                'the source list'],
            ['Refusal output', 'An explicit statement that the available documents do not answer '
                               'the question, plus two better-formed questions'],
            ['Failure behaviour', 'No citation means no claim; hazardous-waste answers always '
                                  'advise verifying with the local body, because municipal bylaws '
                                  'vary and take precedence'],
        ],
    }),

    ('h2', '7.3.5  A practical example'),
    ('callout', '<b>Example \u2014 old batteries.</b><br/><br/>'
                '<b>Question:</b> \u201cWhere should I throw old batteries?\u201d<br/>'
                '<b>Retrieved:</b> a passage from the Battery Waste Management Rules, 2022 '
                '(highest relevance), a passage from the Solid Waste Management Rules, 2016 '
                'listing batteries as domestic hazardous waste, and a related passage from the '
                'E-Waste Rules, 2022.<br/>'
                '<b>Answer, as designed:</b> old batteries must never go into a household bin, '
                'because they are domestic hazardous waste [2]. Tape the terminals of lithium '
                'cells, keep them in a leak-proof container, and return them through retail '
                'take-back boxes or an authorised collection point under the Battery Waste '
                'Management Rules, 2022 [1]. Swollen or damaged cells can cause fires in '
                'collection vehicles and facilities, so isolate them and hand them over '
                'urgently [1].<br/><br/>'
                '<b>Contrast \u2014 the refusal:</b> to the question \u201cwhat are the best pizza '
                'toppings?\u201d, the system does not attempt an answer. It reports that the '
                'question is outside the documents it holds and offers two questions it can '
                'answer.<br/><br/>'
                '<i>Reproduced from the project document as an illustration of the intended '
                'behaviour; the citation numbers refer to the retrieved passage list shown to the '
                'user, not to this report\u2019s reference list.</i>'),

    ('h1', '7.4  Module 3: Environmental Impact Forecaster'),

    ('h2', '7.4.1  Purpose'),
    ('p', 'Correct behaviour is invisible. A household that segregates properly has no way of '
          'knowing whether it diverted ten kilograms or a hundred over a year, or what any of it '
          'was worth in climate terms. The third module exists to make the benefit visible, on the '
          'theory \u2014 stated as a hypothesis \u2014 that a household which can see its own '
          'progress maintains the habit longer than one which is merely told that segregation is '
          'good.'),

    ('h2', '7.4.2  Working concept'),
    ('p', 'The resident supplies a small number of quantities: the number of people in the '
          'household, kilograms of waste per week, the percentage currently segregated, the '
          'percentage currently composted, and whether a recycling collection point and composting '
          'space are available. They then switch on the practices they intend to adopt.'),
    ('p', 'The model applies a composition prior \u2014 the project uses a working split of about '
          '55 per cent organic, 25 per cent dry recyclable and 20 per cent reject \u2014 and two '
          'published coefficients: approximately <b>0.47 kg CO<sub>2</sub>e avoided per kilogram '
          'of organics composted</b> instead of landfilled, and approximately <b>1.1 kg '
          'CO<sub>2</sub>e avoided per kilogram of dry material recycled</b>. The result is '
          'expressed in kilograms diverted and kilograms of carbon dioxide equivalent avoided over '
          'twelve months, and then translated into familiar equivalents: the annual absorption of '
          'a mature tree (about 21 kg CO<sub>2</sub> per year) and kilometres driven in a petrol '
          'car (about 0.192 kg CO<sub>2</sub> per kilometre).'),
    ('p', 'Critically, this module is <b>not</b> a trained machine learning model, and that is a '
          'design decision rather than a limitation. A household needs to be able to understand '
          'and challenge its own number. A published multiplication can be inspected, argued with '
          'and corrected; a neural network\u2019s output cannot. Explainability was prioritised '
          'over marginal accuracy, and the coefficients are printed on screen and reproduced in '
          'this report so that the arithmetic can be checked by hand.'),
    ('figure', 'fig_forecaster.png', FIGCAP('fig_forecaster.png')),
    ('table', {
        'key': 'coefficients',
        'widths': [0.42, 0.22, 0.36],
        'header': ['Quantity', 'Value used', 'What it represents'],
        'rows': [
            ['CO<sub>2</sub>e avoided per kg of organics composted rather than landfilled',
             '0.47 kg CO<sub>2</sub>e/kg',
             'Avoided methane formation when organic waste decomposes aerobically instead of '
             'anaerobically in a landfill'],
            ['CO<sub>2</sub>e avoided per kg of dry material recycled',
             '1.1 kg CO<sub>2</sub>e/kg',
             'Avoided emissions from producing material from virgin feedstock'],
            ['Carbon absorbed by a mature tree in a year',
             '21 kg CO<sub>2</sub>/tree/year',
             'Used only to express the result in a familiar unit'],
            ['CO<sub>2</sub> emitted by a petrol car per kilometre',
             '0.192 kg CO<sub>2</sub>/km',
             'Used only to express the result in a familiar unit'],
            ['Working composition of household waste',
             '55% organic, 25% dry, 20% reject',
             'A prior used to split the stated weekly quantity; municipal composition varies'],
        ],
        'note': 'These are the project\u2019s working coefficients, taken from the SwachhAI '
                'project document. They are order-of-magnitude factors drawn from published '
                'life-cycle and inventory literature; they are not measurements made by this '
                'project, and the outputs they produce are directional estimates, not verified '
                'offsets.',
    }),

    ('h2', '7.4.3  Technologies involved'),
    ('bullets', [
        'A transparent coefficient model \u2014 arithmetic over published factors, chosen over a '
        'learned model for explainability',
        'A composition prior for splitting household waste into organic, dry and reject fractions',
        'Unit-conversion logic that expresses results as trees and driving kilometres',
        'Aggregation logic that allows the same model to be applied to a hostel block or a ward '
        'rather than to a single household',
    ]),

    ('h2', '7.4.4  Input and expected output'),
    ('table', {
        'key': 'm3',
        'widths': [0.22, 0.78],
        'header': ['Element', 'Description'],
        'rows': [
            ['Inputs', 'Household size; kilograms of waste per week; percentage currently '
                       'segregated; percentage currently composted; availability of a recycling '
                       'point and of composting space; plan toggles for practices to be adopted'],
            ['Derived quantities', 'Organic, dry and reject mass per week after applying the '
                                   'composition prior; the additional mass diverted under the '
                                   'selected practices'],
            ['Expected output', 'Kilograms diverted per year; kilograms of CO<sub>2</sub>e avoided '
                                'per year; equivalent number of trees; equivalent kilometres of '
                                'petrol driving'],
            ['Scale switch', 'The same model aggregated to a hostel block or a ward, using an '
                             'assumed adoption rate'],
            ['Failure behaviour', 'Outputs are labelled as modelled estimates in ranges; the '
                                  'system never presents them as certified offsets'],
        ],
    }),

    ('h2', '7.4.5  A practical example'),
    ('p', 'The worked example used throughout the project is a family of four generating about '
          'thirteen kilograms of household waste per week, currently segregating about 30 per cent '
          'and composting nothing, who adopt all three proposed practices: home composting, daily '
          'separation of dry waste, and using the nearest take-back point. The arithmetic below '
          'follows the published coefficients and is reproducible with a calculator.'),
    ('table', {
        'key': 'worked',
        'widths': [0.46, 0.18, 0.36],
        'header': ['Step', 'Result', 'How it is obtained'],
        'rows': [
            ['Waste generated per year', '676 kg',
             '13 kg per week \u00d7 52 weeks'],
            ['Organic fraction of that waste', '\u2248 372 kg',
             '55 per cent of 676 kg, using the composition prior'],
            ['Dry recyclable fraction', '\u2248 169 kg',
             '25 per cent of 676 kg'],
            ['Additional organic mass composted under full adoption', '\u2248 372 kg',
             'the organic fraction currently landfilled; assumes composting space is available'],
            ['Additional dry mass recycled', '\u2248 63 kg',
             'the currently unsegregated share of the dry fraction'],
            ['Total newly diverted per year', '\u2248 435 kg',
             'composted organics plus newly recycled dry material'],
            ['Emissions avoided from organics', '\u2248 175 kg CO<sub>2</sub>e',
             '372 kg \u00d7 0.47 kg CO<sub>2</sub>e per kg'],
            ['Emissions avoided from dry recycling', '\u2248 69 kg CO<sub>2</sub>e',
             '63 kg \u00d7 1.1 kg CO<sub>2</sub>e per kg'],
            ['Emissions avoided in total', '\u2248 245 kg CO<sub>2</sub>e',
             'sum of the two components; the project document quotes approximately 268 kg for a '
             'slightly different set of assumptions, and states the result as a range'],
            ['Expressed as tree-years', '\u2248 12 tree-years',
             '245 \u00f7 21 kg CO<sub>2</sub> per tree per year'],
            ['Expressed as driving', '\u2248 1,275 km',
             '245 \u00f7 0.192 kg CO<sub>2</sub> per km'],
        ],
        'note': 'Modelled estimate only. The arithmetic is shown in full so that the assumptions '
                'can be inspected; the inputs are the household\u2019s own stated quantities and '
                'the coefficients are the project\u2019s published factors. No measurement of any '
                'household\u2019s actual diversion was made, and none is claimed.',
    }),
    ('p', 'The example is deliberately kept reproducible. A resident who does not believe the '
          'figure can check the multiplication; a reviewer who doubts the coefficient can ask about '
          'it. That is the standard the project sets for its own claims, and it is the reason the '
          'forecaster was not built as a black box. The same arithmetic scales: applied to a ward '
          'of ten thousand homes with an assumed 36 per cent full adoption, the project document '
          'reports an order of magnitude of roughly 1,560 tonnes diverted per year, which it '
          'characterises as about a truckload a day. That figure is a scale illustration, not a '
          'forecast.'),

    ('h1', '7.5  Conceptual system architecture'),
    ('p', 'The architecture is organised into five layers, each with one responsibility. Reading '
          'it from the top, a resident interacts with the presentation layer; the orchestration '
          'layer turns the input into a routed request; the module layer performs the three '
          'functions described above; the knowledge and model layer supplies the taxonomy, the '
          'corpus, the model and the coefficients; and the data and governance layers state what '
          'is stored and who is accountable.'),
    ('figure', 'fig_architecture.png', FIGCAP('fig_architecture.png')),
    ('p', 'Four architectural decisions are worth naming, because each represents a choice that '
          'could reasonably have gone the other way.'),
    ('bullets', [
        '<b>One pipeline, three modules.</b> The system does not contain three applications. It '
        'contains one input pipeline that routes a request to one of three functions, which is why '
        'normalisation, privacy handling and logging are written once rather than three times.',
        '<b>Deterministic code around a probabilistic core.</b> The language model sits in the '
        'middle of each path, and everything before and after it is ordinary deterministic code: '
        'alias expansion, taxonomy validation, threshold enforcement, JSON parsing, coefficient '
        'arithmetic. The model is never the last word.',
        '<b>A separate knowledge layer.</b> The taxonomy, the corpus and the coefficients are '
        'data, not code. They can be revised quarterly by a reviewer without releasing new '
        'software, which is what makes the human-oversight gate practical.',
        '<b>Client-side by default.</b> The design processes input on the device and stores '
        'nothing centrally, so the privacy position does not depend on a promise about how a '
        'server behaves.',
    ]),
    ('p', 'The architecture is presented at the level of concept, as required for this report. It '
          'is a block diagram of responsibilities and data flow, not an implementation '
          'specification: it does not fix a hosting model, a database product or a model-serving '
          'stack, because those choices belong to a build phase that this project did not '
          'undertake.'),

    ('h1', '7.6  Workflow of a single interaction'),
    ('p', 'The workflow below shows what happens in one turn, from the resident opening the '
          'assistant to the guidance appearing on screen. It is the same pipeline regardless of '
          'whether the resident arrives with an item, a question or a monthly review.'),
    ('figure', 'fig_workflow.png', FIGCAP('fig_workflow.png')),
    ('p', 'Reading the flow left to right, the resident\u2019s intent is detected first; the '
          'request is normalised and, where necessary, the item is extracted; the request is '
          'routed to the classifier, the rule assistant or the forecaster; the selected module '
          'composes a response using the knowledge layer; the response is rendered as a card with '
          'its confidence and its sources; and an anonymised pattern is logged for the quarterly '
          'taxonomy review. Hazardous-waste requests take a variant of this path in which the '
          'safety step is mandatory and the system appends a reminder to verify with the local '
          'body.'),
    ('p', 'Notice what the workflow does not contain: no step in which the system acts on the '
          'world. It classifies, retrieves, composes and logs. It does not order a collection, '
          'contact a recycler, notify a municipality about an individual household or penalise '
          'anyone. The scope of autonomy was set deliberately narrow, and '
          + X('Responsible AI and Sustainability', 'Chapter 8') + ' explains why.'),

    ('h1', '7.7  Illustrative interface mock-ups'),
    ('p', 'Two mock-ups are included to make the design concrete: the classification screen and '
          'the impact forecaster. <b>Both are illustrations prepared for this report.</b> They are '
          'not screenshots of a deployed product, they are not a demonstration of working '
          'software, and the numbers shown are the worked example from '
          + X('Detailed Project Description', 'Chapter 7') + ', not measurements. They are drawn '
          'in the report to communicate layout and information hierarchy, and they should be read '
          'in that spirit.'),
    ('figure', 'fig_mock_classifier.png', FIGCAP('fig_mock_classifier.png'), 64),
    ('figure', 'fig_mock_forecaster.png', FIGCAP('fig_mock_forecaster.png')),
    ('p', 'The classification mock-up shows the four elements that the design treats as '
          'non-negotiable: the stream, stated in words and as a colour; the confidence, stated as '
          'a number and a bar; the steps, with the safety step first; and the reason, in plain '
          'language. The forecaster mock-up shows the two elements it treats as non-negotiable: '
          'the inputs are quantities only, never identifying details, and the outputs are labelled '
          'as projections over twelve months rather than as achievements to date.'),
]

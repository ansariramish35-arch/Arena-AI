"""Main report chapters 8-10, references and appendices."""
from model import K, X, E, C, FIGCAP, TABSPEC

CH8 = [
    ('chapter', '8', 'Responsible AI and Sustainability'),

    ('h1', '8.1  Why this chapter is not an appendix'),
    ('p', 'There is a comfortable way to write about responsible AI: state five principles, affirm '
          'that the project follows them, and move on. That approach produces a paragraph that no '
          'one can disagree with and no one can check. This chapter takes the harder route. It '
          'states each commitment as a behaviour that could be observed, describes what would '
          'happen if the commitment were absent, and then records the limits of what the design '
          'actually achieves.'),
    ('p', 'The reason for the seriousness is the domain. A system that gives household advice about '
          'waste is giving advice about public rules, in a context where a wrong answer can put a '
          'sanitation worker in contact with a broken CFL tube or an unmarked needle. Responsible '
          'AI is not a reputational supplement to this project; it is the condition under which the '
          'project is worth building at all.'),

    ('h1', '8.2  Transparency'),
    ('p', 'Transparency in this design means that the user can see how a conclusion was reached. '
          'Four specific commitments implement it.'),
    ('bullets', [
        '<b>Confidence is always shown.</b> Every classification carries a percentage. A 72 per '
        'cent answer is visibly different from a 96 per cent answer, and below 75 the answer is '
        'not a stream at all but an admission of uncertainty.',
        '<b>Sources are always listed.</b> Every answer from the rule assistant lists the passages '
        'it retrieved, with the source document named, so that a resident can check the claim '
        'against the rule itself.',
        '<b>Coefficients are published.</b> The impact forecaster prints the factors it uses, and '
        'they are reproduced in this report (Table 16). A resident who disagrees with a '
        'coefficient can see exactly which one to argue with.',
        '<b>Mocked layers are labelled.</b> Where the project build simulated a capability \u2014 '
        'image understanding, for instance \u2014 the limitation is stated in the interface and in '
        'this report rather than hidden behind a plausible-looking screen.',
    ]),
    ('p', 'Transparency of this kind costs something. It makes the system look less confident than '
          'a system that simply asserts an answer, and a product team under commercial pressure '
          'would be tempted to hide the confidence bar. The project\u2019s position is that a '
          'user who is told the system is unsure can compensate; a user who is misled cannot.'),

    ('h1', '8.3  Fairness'),
    ('p', 'An AI system is unfair when it works better for some people than for others in ways '
          'that are not justified by the task. In a waste assistant, the most consequential '
          'unfairness would be linguistic: a system that understands polished English and fails on '
          'Hinglish would serve exactly the households who least need help, and abandon the ones '
          'who do.'),
    ('p', 'The design responds with four commitments. It accepts <b>Hinglish, transliteration and '
          'misspellings</b> as first-class inputs, and treats a failure to understand ordinary '
          'spoken language as a defect rather than a user error. It makes <b>no income-coded '
          'assumptions</b>: shared bins, rented rooms, single-room homes and informal settlements '
          'are modelled as normal circumstances, not as exceptions requiring a special flow. It '
          'keeps the <b>knowledge base balanced across all eight streams</b>, so that a question '
          'about an affluent household\u2019s e-waste and a question about reusing cloth receive '
          'comparable depth of guidance. And it frames sanitation workers as people to protect '
          'rather than as people to monitor, which rules out any feature that scores, ranks or '
          'photographs them.'),
    ('p', 'There is an honest limit here. A language model\u2019s competence in a language depends '
          'on its training data, and Hindi, Marathi or Bengali inputs may be handled less reliably '
          'than English ones regardless of what the prompt requests. The project\u2019s fallback '
          'matcher exists partly for this reason, and the roadmap\u2019s second phase explicitly '
          'includes multilingual voice input. The report does not claim that fairness in language '
          'has been achieved; it claims that it has been designed for.'),

    ('h1', '8.4  Privacy'),
    ('p', 'The privacy position of the project is unusually strong for an AI application, and it '
          'is architectural rather than declarative. The demo build was designed to execute '
          'entirely on the client side: no uploads, no storage, no cookies, no tracking. '
          'Photographs, in the designed extension, would never leave the device. The forecaster '
          'asks for quantities and percentages only \u2014 household size, kilograms per week, '
          'segregation share \u2014 and never for a name, an address, a phone number or an '
          'identifier.'),
    ('table', {
        'key': 'privacy',
        'widths': [0.40, 0.20, 0.40],
        'header': ['Data element', 'Handled how', 'Why it is treated this way'],
        'rows': [
            ['Item description typed by the resident', 'Processed on the device; not stored '
             'centrally', 'It is the minimum input needed to answer the question'],
            ['Photograph of an item', 'Designed to be processed on the device; not uploaded',
             'A photograph can reveal a home, a document or a person; upload is unnecessary for '
             'the task'],
            ['Household quantities (size, kg per week, percentages)',
             'Used only to compute an estimate; no identifier attached',
             'Sufficient for the arithmetic; useless for identifying a household on its own'],
            ['Name, address, phone number, location history', 'Not collected at all',
             'Not required by any function of the system'],
            ['Anonymised usage pattern (for example, an unrecognised item name)',
             'Logged without identifiers, for quarterly taxonomy review',
             'The only way the system improves, without knowing who asked'],
            ['Ward-level aggregate (later phase)', 'Aggregate only, with a minimum cohort size',
             'Supports municipal planning without household-level surveillance'],
        ],
    }),
    ('p', 'One distinction deserves emphasis: <b>anonymised</b> is not the same as '
          '<b>unlinkable</b>. A pattern log that records a sequence of unusual item queries could, '
          'in principle, be re-identified if combined with other data. The design mitigates this '
          'by logging the pattern rather than the query, by keeping no account, and by keeping the '
          'logs local wherever possible. It does not claim that the risk is zero, and a production '
          'deployment would need a formal privacy review before any server-side logging was '
          'introduced.'),

    ('h1', '8.5  Ethical use of AI'),
    ('p', 'Three ethical commitments shape the system\u2019s behaviour more than any technical '
          'choice.'),
    ('p', '<b>The honest-refusal contract.</b> Below the grounding threshold, the system says it '
          'does not know, and offers better questions, instead of fabricating a rule. This is the '
          'single most important behaviour in the design, because a fabricated rule about '
          'hazardous waste is not a minor inaccuracy. A system that refuses is less impressive in '
          'a demonstration and considerably safer in a kitchen.'),
    ('p', '<b>Human safety outranks recycling purity.</b> When the two conflict, the guidance '
          'resolves in favour of the person. A mercury-bearing lamp is a hazard before it is a '
          'recycling opportunity, and a swollen battery is a fire risk before it is a material '
          'recovery opportunity. Every hazardous protocol therefore leads with wrap, mark and hand '
          'over separately, rather than with material value.'),
    ('p', '<b>No shame mechanics.</b> The system contains no guilt score, no public ranking and no '
          'comparison with neighbours. Nudges are factual, kind and opt-in. The reason is both '
          'ethical and practical: a resident who feels judged by an application stops using it, '
          'and a waste tool that people stop using has no effect at all. Behaviour change that is '
          'sustained is voluntary.'),

    ('h1', '8.6  Human supervision'),
    ('p', 'The design keeps a person in the loop at precisely the point where an error would '
          'propagate. The system may answer questions, classify items and log anonymised patterns '
          'without human intervention. It may not change its own taxonomy, admit a new document '
          'into its corpus, or alter a coefficient without review. Each of those three is a change '
          'to the system\u2019s beliefs about the world, and a system that can revise its own '
          'beliefs from user traffic alone can drift.'),
    ('p', 'Supervision also has a scope limit that the report states explicitly: <b>the system is '
          'advisory</b>. It supports a household decision; it does not determine regulatory '
          'compliance, it does not replace a municipal instruction, and where a local body\u2019s '
          'bylaws differ from the general rules, the local body takes precedence. Every hazardous '
          'answer therefore closes with a reminder to verify with the local municipal body.'),
    ('p', 'The project document specifies the review cadence as quarterly for the taxonomy and the '
          'corpus, with bias and misuse regression checks at each release. Those are design '
          'intentions for a system in operation; no such reviews were conducted during the '
          'internship, because the system was not in operation.'),

    ('h1', '8.7  Environmental and social benefits'),
    ('p', 'The benefits the project is designed to produce fall into four groups, and it is worth '
          'separating them because they are of different kinds and are evidenced differently.'),
    ('bullets', [
        '<b>Environmental.</b> Organic waste composted instead of landfilled avoids methane '
        'formation; recycling displaces virgin production, which for aluminium saves the great '
        'majority of the energy required from ore; compost returns carbon and nutrients to soil. '
        'These are established mechanisms described in the published literature; the project\u2019s '
        'contribution is behavioural, and its quantitative outputs are modelled.',
        '<b>Social.</b> Sanitation workers encounter marked, wrapped hazardous material instead of '
        'unmarked material; households gain a sense of agency over a problem that usually feels '
        'abstract; rules become readable in everyday language rather than only in legal English.',
        '<b>Economic.</b> Cleaner inbound streams raise the value of recovered material and give '
        'informal recyclers more predictable quality. These are argued mechanisms, not measured '
        'outcomes of this project.',
        '<b>Educational.</b> The forecaster turns landfill methane into a number attached to a '
        'household\u2019s own kitchen, which is itself a form of climate education and aligns with '
        'Target 13.3 of SDG 13.',
    ]),
    ('p', 'The report is careful here. None of these benefits has been demonstrated by this '
          'project. They are the mechanisms the design is built to activate, and the measurement '
          'plan that would test them is described in the project document: correct-sort rates from '
          'waste audits, dry-stream purity at the material recovery facility, worker injury and '
          'exposure incidents per thousand shifts, weekly active households, and modelled '
          'emissions avoidance derived from audited diversion. Until those measurements exist, the '
          'benefits remain claims with a stated basis, not results.'),

    ('h1', '8.8  Limitations of the proposed approach'),
    ('p', 'A design document that lists no limitations is a sales document. The table below records '
          'the limitations that the project itself acknowledges, together with what each one means '
          'for a reader of this report.'),
    ('table', {
        'key': 'limits',
        'widths': [0.28, 0.40, 0.32],
        'header': ['Limitation', 'Why it matters', 'How the project responds, and what remains open'],
        'rows': [
            ['Built for the Indian urban context',
             'Rural practices, different collection systems and other countries are outside its '
             'design assumptions',
             'The scope is stated openly; extension would require new taxonomy and corpus work, not '
             'just translation'],
            ['Municipal bylaws vary by city and take precedence',
             'A generally correct answer can be locally wrong',
             'The corpus is designed to be swappable per city, and every answer defers to the local '
             'body; per-city corpora were not built'],
            ['Demo taxonomy of about 95 items',
             'Real household waste contains far more variety',
             'The roadmap extends to about 250 items from real queries during a campus pilot; '
             'unrecognised items fall to the refusal path in the meantime'],
            ['Image understanding was mocked in the project build',
             'The designed visual capability is not evidence of a working vision system',
             'Stated as a designed extension throughout this report; no accuracy claim is made for '
             'it'],
            ['Estimates are modelled, not measured',
             'A plausible number can be mistaken for a verified one',
             'Outputs are labelled as directional, stated in ranges, and their arithmetic is '
             'published'],
            ['Behaviour change may decay',
             'A tool used for a month and abandoned changes nothing durable',
             'Nudges and progress cards are designed to sustain use; this is untested'],
            ['Language coverage depends on the model',
             'Hindi, Marathi or Bengali input may be handled less reliably than English',
             'Hinglish is explicitly supported and a fallback matcher exists; multilingual support '
             'is a phase-two goal'],
            ['No field deployment or user testing',
             'Every behavioural claim about residents is a hypothesis',
             'The pilot and its measurement plan are specified but were outside the internship\u2019s '
             'scope'],
        ],
    }),
    ('callout', '<b>The most important limitation is scope.</b> SwachhAI addresses one step of a '
                'long municipal chain. Even a perfectly adopted household assistant would leave '
                'collection gaps, transport losses, facility capacity and legacy dumpsites '
                'untouched. The project is worth doing because that one step is currently weak and '
                'because it is the step a household actually controls \u2014 not because household '
                'behaviour is the whole problem.'),
]

CH9 = [
    ('chapter', '9', 'Learning Outcomes and Future Scope'),

    ('h1', '9.1  Knowledge gained during the internship'),
    ('p', 'The clearest way to describe what was learned is to describe what changed in how the '
          'intern now thinks about building software. Four shifts are worth recording, because each '
          'one is a durable change rather than a fact that could be looked up.'),
    ('p', '<b>From accuracy to calibration.</b> Before the internship, a model was good if it was '
          'right often. After it, a model is good if it knows when it is unsure. The classifier\u2019s '
          'confidence display and its 75-point threshold are not cosmetic features; they are the '
          'mechanism by which a resident can decide whether to trust a particular answer. A system '
          'that is 85 per cent accurate and silent about which 15 per cent is wrong is less useful '
          'than one that is 80 per cent accurate and honest about its uncertainty.'),
    ('p', '<b>From generating to grounding.</b> The internship made the difference between a '
          'language model\u2019s memory and a language model\u2019s evidence concrete. Retrieval '
          'changes an AI feature from an assertion into a quotation, and a quotation can be '
          'checked. The design rule that emerged \u2014 no citation, no claim \u2014 is a small '
          'sentence with large architectural consequences.'),
    ('p', '<b>From features to constraints.</b> The most valuable design work on the project was '
          'subtractive. Four modules were considered and three were kept; several features were '
          'rejected because they could not be justified ethically or measured honestly. Learning '
          'to remove a feature that would have looked impressive in a demonstration, because it '
          'would have been unverifiable in practice, was the most professional thing the internship '
          'taught.'),
    ('p', '<b>From code to documentation.</b> The project\u2019s value to an evaluator lies in its '
          'reasoning, which exists only if it is written down. Producing a document that a reader '
          'can follow \u2014 with diagrams, tables, examples and stated limits \u2014 turned out to '
          'be part of the engineering, not a report on it.'),

    ('h1', '9.2  Technical skills developed'),
    ('p', 'The skills below are stated at the level at which they can honestly be claimed after a '
          'six-week programme: working familiarity and applied practice, not mastery.'),
    ('table', {
        'key': 'skills',
        'widths': [0.30, 0.42, 0.28],
        'header': ['Skill', 'How it was practised', 'Level honestly claimed'],
        'rows': [
            ['Prompt design', 'Writing and revising a classifier prompt with a role, a task '
                              'decomposition, a JSON output contract, a refusal rule and a tone '
                              'rule',
             'Working familiarity; not benchmarked'],
            ['Retrieval-augmented design', 'Specifying a corpus, chunking strategy, retrieval, '
                                           're-ranking and a grounding threshold',
             'Design-level understanding; the demo used a term-frequency retrieval approach'],
            ['Responsible-AI review', 'Turning five principles into observable behaviours and '
                                      'reviewing the design against them',
             'Applied practice on one system'],
            ['Policy research', 'Reading primary instruments \u2014 SWM Rules 2016, E-Waste and '
                                'Battery Rules 2022 \u2014 rather than summaries',
             'Competent at locating and citing primary sources'],
            ['Quantitative modelling', 'Building a transparent coefficient model and stating its '
                                       'uncertainty',
             'Competent for order-of-magnitude estimates'],
            ['Systems thinking', 'Separating a long municipal chain into one addressable step and '
                                 'stating what is out of scope',
             'Applied, with supervision'],
            ['Technical communication', 'Block diagrams, workflow diagrams, tables, worked '
                                        'examples and a structured report',
             'Demonstrated by this document'],
            ['Python and data handling', 'Data structures, basic scripting and tabular handling '
                                         'carried over from coursework and prior training',
             'Coursework level'],
        ],
    }),

    ('h1', '9.3  Practical understanding of emerging technologies'),
    ('p', 'Three practical judgements about emerging technology emerged from the work, and they are '
          'more portable than any specific tool.'),
    ('p', '<b>Justify the model, not the fashion.</b> The classifier uses a language model because '
          'the input is language, variable and misspelt. The forecaster does <i>not</i> use a '
          'learned model, because a household needs arithmetic it can check. Both decisions are '
          'about the task; neither is about what is currently interesting. Being able to defend a '
          'decision not to use AI is as much a technical skill as being able to use it.'),
    ('p', '<b>Assume the model will be wrong.</b> Every path in the design has a defined failure '
          'behaviour: unknown instead of a guess, refusal instead of invention, a fallback matcher '
          'instead of a crash, a labelled estimate instead of a false precision. Designing the '
          'failure path first, and building the happy path around it, is the habit that separates '
          'a demonstration from a system.'),
    ('p', '<b>Treat evaluation as part of the design.</b> A claim without a measurement plan is an '
          'opinion. The project document specifies what would be measured \u2014 audit-based '
          'correct-sort rates, dry-stream purity, injury rates per thousand shifts, weekly active '
          'households \u2014 before claiming that anything works. That discipline is what allows '
          'this report to say \u201cmodelled\u201d where it cannot say \u201cmeasured\u201d.'),

    ('h1', '9.4  Future scope of SwachhAI'),
    ('p', 'The project document sets out a phased path, and this report reproduces it as a plan '
          'rather than as a commitment. The organising principle is that each phase must earn the '
          'next one with field evidence: a taxonomy expanded from a campus pilot is more useful '
          'than one expanded from imagination, and a ward partnership is only worth entering once '
          'the tool has survived a smaller test.'),
    ('figure', 'fig_roadmap.png', FIGCAP('fig_roadmap.png')),
    ('table', {
        'key': 'future',
        'widths': [0.20, 0.44, 0.36],
        'header': ['Phase', 'What would be built or done', 'What would have to be true to proceed'],
        'rows': [
            ['Phase 1 \u2014 campus pilot (months 0\u20133)',
             'Deploy to about 500 students and two hostels; run a one-week baseline waste audit; '
             'expand the taxonomy from about 95 to about 250 items using real queries',
             'At least 60 per cent weekly active use and a measurable cut in hostel mixed waste'],
            ['Phase 2 \u2014 ward partnership (months 3\u20139)',
             'Align the streams with the urban local body\u2019s collection routes; add multilingual '
             'voice input and ward collection calendars; deploy the nudge agent',
             'One ward onboarded, and the material recovery facility verifies improved dry-stream '
             'purity'],
            ['Phase 3 \u2014 citizen data layer (months 9\u201318)',
             'Aggregate-only stream analytics on city dashboards; an API for housing societies; '
             'integration with recycler take-back schemes',
             'Verifiable tonnes diverted, published quarterly from audited data'],
        ],
    }),
    ('p', 'Beyond the phased plan, four extensions are technically plausible and are recorded here '
          'as possibilities rather than promises. <b>Vision-based classification</b>, in which a '
          'photograph is read directly instead of a label being typed, would remove the typing '
          'burden but would need a properly labelled training set and an accuracy study before it '
          'could be trusted on hazardous items. <b>Multilingual voice input</b> would widen access '
          'substantially, and is the extension with the clearest equity case. <b>Per-city corpora</b> '
          'would address the limitation that municipal bylaws vary, and could be assembled with '
          'local bodies or student partners in each city. <b>Recycler and kabadiwala integration</b> '
          'would close the loop by telling a resident where to hand material over, rather than only '
          'which stream it belongs to.'),
    ('p', 'One further extension is worth stating because it is often proposed and should be '
          'resisted in this form: a <b>household league table or public ranking</b>. It would '
          'probably increase short-term engagement and it would violate the project\u2019s position '
          'on shame, privacy and dignity. The design keeps progress private to the household and '
          'treats aggregate data as a municipal planning input rather than as a social scoreboard.'),

    ('h1', '9.5  What was not done, and why'),
    ('p', 'Recording absences is as useful as recording achievements, particularly in a report that '
          'will be assessed. No model was trained or fine-tuned; no labelled image dataset was '
          'assembled; no field deployment or user testing was conducted; no municipal partnership '
          'was established; no measurement of diversion, contamination or injury was made; and no '
          'independent evaluation of accuracy was performed.'),
    ('p', 'The reason is scope rather than omission. The internship\u2019s deliverable was a '
          'designed and documented proposal, and the University\u2019s requirement for this report '
          'is an academic record, not a deployed product. Claiming any of the above would have made '
          'the report longer and less true. What the work does provide is a design that states its '
          'assumptions, a set of published coefficients, a measurement plan and an honest list of '
          'limits \u2014 which is the correct starting position for the field work that would '
          'follow.'),
]

CH10 = [
    ('chapter', '10', 'Conclusion'),

    ('h1', '10.1  What the internship was'),
    ('p', 'This report has documented the 1M1B AI for Sustainability Virtual Internship, offered by '
          '1M1B (One Million for One Billion), supported by the All India Council for Technical '
          'Education and delivered in collaboration with IBM SkillsBuild, and certified as '
          'completed over the period July to September 2026. The internship asked for two things '
          'that are usually kept apart: a working understanding of current artificial intelligence '
          'techniques, and a defensible application of them to a real sustainability problem.'),
    ('p', 'The technical content covered machine learning, large language models, the IBM Granite '
          'family, prompt engineering, retrieval-augmented generation, agentic AI and responsible '
          'AI. The project requirement converted that syllabus into a problem: household waste '
          'segregation, where the rules exist, the obligation exists, and the interface between the '
          'two does not.'),

    ('h1', '10.2  What the project proposed'),
    ('p', 'SwachhAI is a decision-support concept with three cooperating modules. A classifier maps '
          'an item described in ordinary language to one of eight waste streams, with a stated '
          'confidence and a short protocol that leads with the safety step. A retrieval-augmented '
          'assistant answers questions about waste rules only from a curated corpus of public '
          'documents, with citations, and refuses when the documents do not cover the question. An '
          'impact forecaster converts a household\u2019s stated habits into a transparent, '
          'checkable estimate of waste diverted and carbon dioxide equivalent avoided, using '
          'published coefficients rather than an opaque model.'),
    ('p', 'The design is united by one argument: AI is justified in this domain because the problem '
          'is linguistic and contextual. Residents are not indifferent; they are unsure, at a '
          'moment when they have four seconds and no reliable memory of which item belongs where. '
          'A static poster cannot resolve an item-specific question in a resident\u2019s own '
          'vocabulary. A system that understands language, retrieves rules and states its own '
          'uncertainty can.'),

    ('h1', '10.3  What was learned'),
    ('p', 'Three lessons will outlast the project. The first is that <b>calibration matters more than raw '
          'accuracy</b> in any system that advises a person: an answer that states its confidence '
          'can be acted on sensibly, while a confident answer that is sometimes wrong cannot. The '
          'second is that <b>grounding converts an assertion into evidence</b>, and evidence can be '
          'checked; the discipline of refusing to answer when the evidence is thin turned out to be '
          'a feature, not a shortfall. The third is that <b>the ethical constraints were the '
          'design</b>: the confidence threshold, the privacy architecture, the refusal path and the '
          'safety-first protocols all exist because someone asked what happens when the system is '
          'wrong, and who is harmed.'),
    ('p', 'The professional lessons were less tidy. Working without supervision means that a '
          'milestone either exists or does not; mentor feedback is worth more than a first idea; '
          'documentation is part of the engineering; and a report is more credible when it states '
          'what it did not do.'),

    ('h1', '10.4  Why the problem matters'),
    ('p', 'India\u2019s municipal waste problem is usually described in tonnes, and the tonnage is '
          'real: the Central Pollution Control Board\u2019s reporting for 2020\u201321 places '
          'generation at roughly 1,60,000 tonnes per day ' + C(1) + '. But the tonnage is a '
          'consequence. The cause is a chain of small decisions, most of them made in kitchens, and '
          'the first of those decisions is which bin. When that decision goes wrong, the cost is '
          'paid three times: by a recycler whose bale is rejected, by a sanitation worker who '
          'reaches into a bag containing a broken tube, and by the atmosphere in the form of '
          'methane from organic waste that was buried instead of composted.'),
    ('p', 'A household assistant does not fix a municipal system. It addresses one step \u2014 the '
          'step that a household controls \u2014 and it does so on the assumption that better '
          'inputs make every downstream stage easier. That assumption is testable, and the project '
          'document specifies how: audits, purity measurements, injury rates, active use. The '
          'honest status of the project is therefore not \u201csolved\u201d but \u201cdesigned, '
          'with a plan to find out\u201d.'),

    ('h1', '10.5  Professional development'),
    ('p', 'The internship changed the kind of engineer this student intends to be. It established '
          'an interest in the part of data and AI work that sits closest to a decision a person '
          'actually makes \u2014 the interface, the uncertainty, the failure path \u2014 and a '
          'working standard for claims: state the basis, show the arithmetic, label the estimate, '
          'and separate design from demonstrated behaviour.'),
    ('p', 'Those habits connect directly to the career direction recorded in the accompanying '
          'résumé: data engineering and data systems. A pipeline that moves data reliably between '
          'systems has the same obligations as a classifier that moves an item into a stream \u2014 '
          'defined contracts, explicit failure behaviour, inspectable outputs and someone '
          'accountable for what happens when the data is wrong. The internship was about waste; the '
          'lesson was about trustworthiness.'),

    ('h1', '10.6  Closing remark'),
    ('p', 'The project was called SwachhAI because the aim was modest and specific: make the right '
          'bin the easy bin. It is a small ambition measured against a national problem, and a '
          'serious one measured against a household. If the design is ever built and tested, the '
          'question that will decide whether it was worth building is not whether the model was '
          'accurate. It is whether a resident, holding a milk pouch in one hand and a phone in the '
          'other, found the answer in time \u2014 and whether the person who collected the bag the '
          'next morning was a little safer for it.'),
]

REFERENCES = [
    (1, 'Central Pollution Control Board, <i>Annual Report 2020\u201321 on Implementation of Solid '
        'Waste Management Rules, 2016</i>, Central Pollution Control Board, Ministry of Environment, '
        'Forest and Climate Change, Government of India.',
     'https://cpcb.nic.in/uploads/MSW/MSW_AnnualReport_2020-21.pdf'),
    (2, 'Ministry of Environment, Forest and Climate Change, <i>Solid Waste Management Rules, '
        '2016</i>, Notification S.O. 1357(E) dated 8 April 2016, Gazette of India.',
     'https://cpcb.nic.in/uploads/MSW/SWM_2016.pdf'),
    (3, 'Ministry of Environment, Forest and Climate Change, <i>Battery Waste Management Rules, '
        '2022</i>, notified 24 August 2022, Gazette of India; see also Press Information Bureau, '
        '\u201cGovernment notifies Battery Waste Management Rules, 2022\u201d, 25 August 2022.',
     'https://www.pib.gov.in/PressReleasePage.aspx?PRID=1854433'),
    (4, 'Ministry of Environment, Forest and Climate Change, <i>Plastic Waste Management Rules, '
        '2016</i>, as amended by the <i>Plastic Waste Management (Amendment) Rules, 2021</i> and '
        'subsequent amendments, Gazette of India.',
     'https://cpcb.nic.in/displaypdf.php?id=cGxhc3RpY3dhc3RlL1BXTV9HYXpldHRlLnBkZg=='),
    (5, 'Ministry of Environment, Forest and Climate Change, <i>E-Waste (Management) Rules, 2022</i>, '
        'Notification G.S.R. 801(E) dated 2 November 2022, in force from 1 April 2023, Gazette of '
        'India.', 'https://cpcb.nic.in/uploads/Projects/E-Waste/e-waste_rules_2022.pdf'),
    (6, 'Ministry of Environment, Forest and Climate Change, <i>Construction and Demolition Waste '
        'Management Rules, 2016</i>, Gazette of India, 2016.',
     'https://cpcb.nic.in/uploads/MSW/CD_Waste_Rules_English.pdf'),
    (7, 'Ministry of Housing and Urban Affairs, <i>Swachh Bharat Mission \u2013 Urban 2.0: Making '
        'Cities Garbage Free</i>, operational guidelines, Government of India, 2021.',
     'https://swachhbharaturban.gov.in/'),
    (8, 'Intergovernmental Panel on Climate Change, \u201cChapter 7: The Earth\u2019s Energy Budget, '
        'Climate Feedbacks and Climate Sensitivity\u201d, in <i>Climate Change 2021: The Physical '
        'Science Basis. Contribution of Working Group I to the Sixth Assessment Report</i>, '
        'Cambridge University Press, 2021, Table 7.15.',
     'https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-7/'),
    (9, 'United Nations Environment Programme, <i>Food Waste Index Report 2024: Think Eat Save '
        '\u2014 Tracking Progress to Halve Global Food Waste</i>, Nairobi, 2024.',
     'https://www.unep.org/resources/publication/food-waste-index-report-2024'),
    (10, 'IBM, \u201cIBM Granite 3.0: open, state-of-the-art enterprise models\u201d, IBM '
         'announcement, October 2024.',
     'https://www.ibm.com/new/announcements/ibm-granite-3-0-open-state-of-the-art-enterprise-models'),
    (11, 'IBM, <i>granite-3.0-8b-instruct model card</i>, IBM watsonx documentation.',
     'https://www.ibm.com/docs/en/watsonx'),
    (12, 'IBM SkillsBuild, digital learning platform, IBM.',
     'https://skillsbuild.org/'),
    (13, '1M1B (One Million for One Billion), programme information for the AI for Sustainability '
         'Virtual Internship.', 'https://www.1m1b.org/'),
    (14, 'All India Council for Technical Education, National Internship Portal.',
     'https://internship.aicte-india.org/'),
    (15, 'Bureau of Indian Standards, <i>IS 14534: Plastics \u2014 Guidelines for the Recovery and '
         'Recycling of Plastics</i>, New Delhi.',
     'https://www.bis.gov.in/'),
    (16, 'United Nations, <i>Transforming our World: The 2030 Agenda for Sustainable Development</i>, '
         'A/RES/70/1, 2015, including Sustainable Development Goals 11, 12 and 13 and their '
         'targets.', 'https://sdgs.un.org/2030agenda'),
    (17, 'Lewis, P., Perez, E., Piktus, A., et al., \u201cRetrieval-Augmented Generation for '
         'Knowledge-Intensive NLP Tasks\u201d, <i>Advances in Neural Information Processing '
         'Systems 33</i>, 2020.', 'https://arxiv.org/abs/2005.11401'),
    (18, 'Vaswani, A., Shazeer, N., Parmar, N., et al., \u201cAttention Is All You Need\u201d, '
         '<i>Advances in Neural Information Processing Systems 30</i>, 2017.',
     'https://arxiv.org/abs/1706.03762'),
    (19, 'University of Lucknow, <i>Guidelines for the Submission of Summer Internship Reports</i>, '
         'Department of Computer Science and Engineering, Lucknow.',
     'https://www.lkouniv.ac.in/'),
    (20, 'Mohammad Ramish Ansari, <i>SwachhAI \u2014 AI for Sustainable Waste Management: Final '
         'Project Deliverable</i>, submitted for the 1M1B AI for Sustainability Virtual Internship, '
         '14 September 2026.', None),
]

APPENDIX = [
    ('chapter', 'A', 'Appendix A: Supporting Documents'),

    ('h1', 'A.1  Purpose of this appendix'),
    ('p', 'This appendix reproduces the supporting documents referred to in the report so that a '
          'reader can verify the particulars stated in Chapters 1 to 3 without taking them on '
          'trust. Three documents are reproduced: the AICTE internship completion certificate, '
          'already included in the preliminary pages and referenced here for completeness; the two '
          'IBM SkillsBuild completion certificates of 1 and 5 August 2026; and a summary of the '
          'AICTE internship offer letter.'),
    ('p', 'The offer letter itself is not reproduced in full. It carries a confidentiality clause, '
          'which this report respects: the summary records only the particulars needed to '
          'establish the internship\u2019s identity, duration and terms, and omits contact '
          'addresses, links, and all course and session content.'),

    ('h1', 'A.2  Internship completion certificate'),
    ('p', 'Issued by 1M1B (One Million for One Billion), supported by AICTE, in collaboration with '
          'IBM SkillsBuild. Signed by the Founder and Chief Mentor of 1M1B and by the Chief '
          'Coordinating Officer of AICTE. Issue date 22 September 2026; AICTE Internship ID '
          'INTERNSHIP_17828984086a44dee80acf6. The certificate records the internship period as '
          'July 2026 to September 2026. A colour copy appears in the preliminary pages of this '
          'report; see also Table 2 for the date analysis.'),
    ('figure', 'certificates/cert_main.png',
     'Internship completion certificate (reproduced from the preliminary pages)'),

    ('h1', 'A.3  IBM SkillsBuild completion certificates'),
    ('p', 'Two SkillsBuild completion certificates were issued during the internship, recording '
          'completion of two learning plans on 1 August 2026 and 5 August 2026. They are not '
          'internship certificates \u2014 that is the document in A.2 \u2014 but they evidence the '
          'guided learning component.'),
    ('figure', 'certificates/cert_ibm_plan1.png',
     'IBM SkillsBuild completion certificate, learning plan PLAN-56138075980A, 1 August 2026 (GMT)'),
    ('figure', 'certificates/cert_ibm_plan2.png',
     'IBM SkillsBuild completion certificate, learning plan PLAN-F60F1D7DADA9, 5 August 2026 (GMT)'),

    ('h1', 'A.4  Summary of the AICTE internship offer letter'),
    ('p', 'The offer letter confirms selection for the 1M1B AI for Sustainability Virtual '
          'Internship, offered by 1M1B in collaboration with AICTE (National Internship Portal) and '
          'co-certified by IBM SkillsBuild. The particulars relevant to this report are:'),
    ('table', {
        'key': 'student',
        'widths': [0.34, 0.66],
        'header': ['Particular', 'Value as recorded in the documents'],
        'rows': [
            ['Student name', 'Mohammad Ramish Ansari'],
            ['Programme and institution', 'B.Tech. Computer Science and Engineering, University of '
                                          'Lucknow, Lucknow \u2014 226 021; third year, '
                                          'Semester V'],
            ['University roll number and faculty supervisor', '[To be entered \u2014 not stated in '
                                                              'the uploaded documents]'],
            ['Internship title', '1M1B | AI for Sustainability Virtual Internship'],
            ['Organising body', '1M1B (One Million for One Billion), supported by AICTE '
                                '(National Internship Portal) and co-certified in collaboration '
                                'with IBM SkillsBuild'],
            ['AICTE Internship ID', 'INTERNSHIP_17828984086a44dee80acf6'],
            ['Duration', 'Proposed: six weeks, 28 July to 28 August 2026 (offer letter). '
                          'Certified: July to September 2026 (completion certificate, issued '
                          '22 September 2026)'],
            ['Project submitted', 'SwachhAI \u2014 final project deliverable, 14 September 2026'],
            ['Remuneration', 'Unpaid internship; no stipend is provided'],
        ],
        'note': 'Square-bracketed items are placeholders: the documents do not state the '
                'university roll number or the faculty supervisor, and this report does not guess '
                'them.',
    }),

    ('h1', 'A.5  How the claims in this report are supported'),
    ('p', 'Because the report deliberately contains no invented results, it is worth stating what '
          'each kind of claim rests on. Student, internship and date particulars come from the '
          'offer letter, the completion certificate, the two SkillsBuild certificates and the '
          'project document, and are stated directly. National statistics come from the CPCB '
          'annual report for 2020\u201321 and are cited by number. Rule and standards content '
          'comes from the Gazette notifications, paraphrased rather than quoted. Greenhouse-gas '
          'and food-waste figures come from IPCC AR6 and the UNEP Food Waste Index Report 2024. '
          'Descriptions of the system\u2019s behaviour describe the design in the project '
          'document, and are illustrated by its recorded examples. Quantities of waste diverted '
          'or emissions avoided are labelled as modelled estimates, with their arithmetic shown '
          'in Table 15. Expected benefits to households, workers and cities are argued mechanisms '
          'accompanied by a measurement plan. No performance, accuracy or testing result is '
          'claimed anywhere in this report, because none was measured.'),

    ('h1', 'A.6  Declaration of academic integrity'),
    ('p', 'The report follows the University of Lucknow\u2019s guidelines for the submission of '
          'summer internship reports: A4 paper, Times New Roman at 12 point for body text, single '
          'line spacing, justified paragraphs, consistent academic margins, Roman numerals for '
          'preliminary pages and Arabic numerals for the main report, and single-sided printing '
          'suitable for spiral binding.'),
    ('p', 'The report contains no source code and describes no executable software product: it '
          'presents a conceptual design documented through descriptions, diagrams, tables and '
          'clearly labelled illustrations. Where the project\u2019s own material describes a '
          'prototype, this report explains its intended design and does not claim to have tested '
          'or verified it. Both interface mock-ups are labelled as illustrations, and no '
          'confidential material or meeting link has been reproduced.'),
]


EVIDENCE = [
    ('h1', 'How the claims in this report are supported'),
    ('p', 'The table below states, for each kind of claim made in this report, what it rests on. It '
          'is included because the report deliberately contains no invented results, and a reader '
          'should be able to see where each statement comes from.'),
    ('table', {
        'key': 'evidence',
        'widths': [0.34, 0.34, 0.32],
        'header': ['Kind of claim', 'Basis', 'Marked in the text as'],
        'rows': [
            ['Student, internship and date particulars',
             'Offer letter, completion certificate, SkillsBuild certificates, project document',
             'Stated directly, with the source named'],
            ['National waste statistics',
             'CPCB annual report for 2020\u201321, cited in the References',
             'Attributed in the sentence and cited by number'],
            ['Rule and standards content',
             'Gazette notifications and CPCB publications, cited in the References',
             'Cited by number; paraphrased, not quoted at length'],
            ['Greenhouse-gas and food-waste figures',
             'IPCC AR6 Working Group I and the UNEP Food Waste Index Report 2024',
             'Cited by number with the value and unit given'],
            ['Behaviour of the proposed system',
             'Design described in the SwachhAI project document',
             'Described as designed or intended behaviour, illustrated by examples'],
            ['Quantities of waste diverted or emissions avoided',
             'Published coefficients applied to stated household inputs',
             'Labelled as modelled or directional estimates, with the arithmetic shown'],
            ['Benefits to households, workers or cities',
             'Plausible mechanisms argued from published practice',
             'Described as expected or intended benefits, with a measurement plan'],
            ['Performance, accuracy or testing results',
             'No such measurement was made during the internship',
             'Not claimed anywhere in this report'],
        ],
    }),
]

"""Main report chapters 1-5."""
from model import K, X, E, C, FIGCAP, TABSPEC

CH1 = [
    ('chapter', '1', 'Introduction'),

    ('h1', '1.1  What a summer internship is for'),
    ('p', 'A summer internship is the part of an engineering degree in which a student stops '
          'studying technology and starts using it on somebody else\u2019s problem. Until that '
          'point, almost every exercise a student completes has three convenient properties: the '
          'question is already framed, the data is already clean, and the answer is already known '
          'to the person who will mark it. Industry does not work that way. A real requirement '
          'arrives incomplete, the data has gaps, several solutions are defensible, and someone '
          'has to decide which one is worth building.'),
    ('p', 'The All India Council for Technical Education (AICTE) treats this gap as a structural '
          'part of technical education rather than an optional extra, and maintains an internship '
          'portal through which students are placed with companies, research organisations and '
          'government programmes. AICTE\u2019s model curriculum and its internship guidelines '
          'treat practical exposure as part of the assessment of a degree programme, and '
          'universities usually require a written report so that the learning can be reviewed by '
          'a faculty member rather than taken on trust. This report is that document.'),
    ('p', 'For a Computer Science and Engineering student, the internship has a second purpose. '
          'Coursework teaches a subject in isolation: a database course teaches normalisation, a '
          'machine learning course teaches gradient descent. An internship teaches the '
          'interaction between subjects \u2014 that a model which is 92 per cent accurate can '
          'still be useless if the interface does not show its confidence, that a service which '
          'is technically correct can still fail if the person using it has four seconds and one '
          'hand free. That interaction is what an employer is actually buying, and it is difficult '
          'to teach in a lecture hall.'),

    ('h1', '1.2  Why internships matter for engineering students'),
    ('p', 'There are four things an internship supplies that a classroom cannot supply on its '
          'own, and all four appear in the work described in this report.'),
    ('bullets', [
        '<b>Contact with a real constraint.</b> The problem chosen for this internship was not '
        'invented for assessment. Household waste segregation in India is a live public problem '
        'with published rules, published shortfalls and an actual person at the end of every '
        'decision. Working on it meant accepting constraints that no assignment imposes.',
        '<b>Exposure to professional tools and vocabulary.</b> The internship introduced IBM '
        'Granite models, retrieval-augmented generation, prompt engineering, agentic design '
        'patterns and responsible-AI review. These are not exotic research topics; they are the '
        'current working vocabulary of applied AI, and meeting them early changes what a student '
        'reads and what a student builds.',
        '<b>Practice at written and visual communication.</b> A technical decision that nobody '
        'else can follow is not yet an engineering decision. The internship required a concept '
        'note, a project document and a presentation, each addressed to a different reader. The '
        'diagrams and tables in this report are a direct result of that requirement.',
        '<b>Practice at judging one\u2019s own claim.</b> The most useful professional habit '
        'gained was the discipline of separating what a system is designed to do from what it has '
        'been shown to do. That distinction appears repeatedly in later chapters, and it is the '
        'reason this report contains no invented test results.',
    ]),
    ('p', 'There is also a plain, practical reason. Internship experience is the first evidence a '
          'student can offer that the degree has been used for something. For a third-year '
          'student preparing for placements, a documented project with a stated problem, a stated '
          'design and a stated set of limits is more persuasive than a list of technologies '
          'studied, because it demonstrates a sequence of decisions rather than a sequence of '
          'topics.'),

    ('h1', '1.3  Artificial intelligence and sustainability'),
    ('p', 'Artificial intelligence and sustainability are usually discussed in two separate '
          'conversations, and the internship was designed to put them in one. The first '
          'conversation is about what AI can do: recognise an image, answer a question in '
          'natural language, forecast a quantity, generate a document. The second is about what '
          'the planet can afford: how much waste is generated, how much of it is recovered, how '
          'much methane escapes from a landfill, and how quickly cities can change behaviour at '
          'the household level.'),
    ('p', 'The connection between them is not automatic. AI systems consume electricity and water '
          'during training and inference, and an AI application that solves a trivial problem is '
          'a net cost. The useful framing, and the one the internship adopted, is narrower: AI is '
          'worth deploying where a problem is <i>linguistic, visual or contextual</i> \u2014 where '
          'a fixed set of rules cannot cover the variety of real inputs, but a learned or '
          'retrieved answer can. Waste segregation is exactly that kind of problem. A printed '
          'poster cannot tell a resident whether a particular milk pouch, with a particular '
          'residue inside it, belongs in the dry bin; a system that understands an item '
          'description and can quote the applicable rule can.'),
    ('p', 'The same reasoning explains why the internship placed responsible AI beside the '
          'technical content rather than after it. A system that tells households what to do with '
          'their waste is making claims about public rules. If it invents a rule, it does not '
          'merely produce a wrong answer; it sends a battery into a bin where a sanitation worker '
          'will reach for it. The design constraint that follows \u2014 answer only from cited '
          'documents, and refuse when the documents do not cover the question \u2014 is a '
          'technical decision with an ethical origin, and it is developed in '
          + X('Project Overview: SwachhAI', 'Chapter 6') + ' and '
          + X('Responsible AI and Sustainability', 'Chapter 8') + '.'),

    ('h1', '1.4  The internship in brief'),
    ('p', 'The internship was the <b>1M1B AI for Sustainability Virtual Internship</b>, offered '
          'by 1M1B (One Million for One Billion), supported by AICTE and delivered in '
          'collaboration with IBM SkillsBuild. It was a virtual, six-week programme built around '
          'guided learning, weekly mentor interaction and a final project that applied AI to a '
          'sustainability problem. The project submitted at the end of the internship was '
          '<b>SwachhAI \u2014 AI-Guided Waste Segregation and Circularity Assistant for '
          'India\u2019s Households</b>.'),
    ('p', 'The programme\u2019s own documents describe its purpose as developing industry-relevant '
          'AI skills in the context of sustainable development: working with AI and machine '
          'learning concepts, large language models, IBM Granite models, retrieval-augmented '
          'generation frameworks and agentic AI systems, and applying them to climate action, '
          'clean energy, waste reduction, biodiversity and sustainable cities. The structure of '
          'the internship, its partners and its schedule are described in '
          + X('Organization and Internship Overview', 'Chapter 2') + '.'),
    ('p', 'This report is deliberately written as documentation rather than as a software '
          'submission. It explains the problem, the technology, the design and the limits of the '
          'proposed concept. It contains no source code, no deployment instructions and no '
          'performance claims, because the deliverable required by the University is an academic '
          'report and because the honest description of an untested design is a design document, '
          'not a product announcement.'),

    ('h1', '1.5  How this report is organised'),
    ('p', 'The report follows the sequence in which the work actually happened. '
          + X('2  Organization and Internship Overview', 'Chapter 2') + ' describes the '
          'organisations, the internship\u2019s objectives and its certified duration. '
          + X('3  Objectives and Learning Outcomes', 'Chapter 3') + ' states what the internship '
          'set out to achieve and what was actually gained. '
          + X('4  Technology Overview', 'Chapter 4') + ' explains the technologies at the level a '
          'third-year student should be able to defend in a viva. '
          + X('5  Problem Statement', 'Chapter 5') + ' establishes why the project was worth '
          'doing. ' + X('6  Project Overview: SwachhAI', 'Chapter 6') + ' introduces the concept '
          'and the users. ' + X('7  Detailed Project Description', 'Chapter 7') + ' is the '
          'technical core: three modules, an architecture and a workflow. '
          + X('8  Responsible AI and Sustainability', 'Chapter 8') + ' examines what could go '
          'wrong and what the design does about it. '
          + X('9  Learning Outcomes and Future Scope', 'Chapter 9') + ' records what was learned '
          'and what would come next, and ' + X('10  Conclusion', 'Chapter 10') + ' closes the '
          'report. References and appendices follow.'),
    ('p', 'Two conventions are used throughout. First, every figure and table is numbered and '
          'referred to by number in the text, and every reference to a chapter in this document '
          'is a working link in the digital edition. Second, any number that is an estimate is '
          'labelled as an estimate at the point where it appears; the report does not repeat a '
          'modelled figure often enough for it to start looking like a measurement.'),
]

CH2 = [
    ('chapter', '2', 'Organization and Internship Overview'),

    ('h1', '2.1  Introduction to 1M1B'),
    ('p', '1M1B stands for <i>One Million for One Billion</i>. It is the organising body of the '
          'internship: the organisation that designed the programme, ran the sessions, assigned '
          'mentors and assessed the final project. Its self-description, as it appears on the '
          'programme\u2019s material, is a mission to mobilise a million young people in India to '
          'create impact at the scale of a billion \u2014 a formulation that explains the name. In '
          'practice, its work with students takes the form of structured programmes that combine '
          'awareness of the Sustainable Development Goals with practical technology skills, '
          'delivered in partnership with industry and with government bodies.'),
    ('p', 'What matters for this report is the shape of the programme rather than the '
          'organisation\u2019s history. The internship was <b>virtual</b>, which meant that '
          'participation did not depend on being in a particular city; it was <b>cohort-based</b>, '
          'which meant that interns progressed through the same milestones at roughly the same '
          'time; and it was <b>project-based</b>, which meant that the certificate depended on '
          'producing a piece of work rather than on attendance alone. The programme\u2019s terms '
          'state that certification requires participation in weekly mentor sessions, completion '
          'of the weekly tasks and milestones, completion of the SkillsBuild learning plan, and '
          'submission of the final project presentation.'),
    ('p', 'The programme was explicitly <b>unpaid</b>: the offer letter states that no stipend or '
          'financial remuneration is provided. This is normal for a learning-oriented, '
          'government-supported programme, and it is recorded because a report should state the '
          'terms under which the work was done.'),

    ('h1', '2.2  The role of AICTE'),
    ('p', 'The All India Council for Technical Education is the statutory body responsible for '
          'the planning and coordinated development of technical education in India. Its '
          'involvement in this internship took three concrete forms, each visible in the '
          'documents reproduced in the appendices.'),
    ('numbered', [
        '<b>Listing and support.</b> The internship was listed on the <b>AICTE National '
        'Internship Portal</b>, which is AICTE\u2019s mechanism for connecting students with '
        'internship opportunities and for recording that the opportunity has been recognised. The '
        'offer letter names the portal explicitly, describing the programme as offered by 1M1B '
        '\u201cin collaboration with AICTE (National Internship Portal)\u201d.',
        '<b>Co-signature on the completion certificate.</b> The certificate reproduced in this '
        'report carries the signatures of the Founder and Chief Mentor of 1M1B and of the Chief '
        'Coordinating Officer of AICTE. The AICTE signature is not decorative; it is the reason '
        'the certificate is usable as evidence for a university requirement.',
        '<b>An internship identity.</b> The certificate records an <b>AICTE Internship ID</b>, '
        '%s, which is the same identifier that appears in the offer letter and in the project '
        'document. That continuity is what makes the three documents traceable to one another.'
        % 'INTERNSHIP_17828984086a44dee80acf6',
    ]),
    ('p', 'For a student, the practical consequence is that the internship is not an informal '
          'arrangement between an individual and a company. It is a recognised activity, recorded '
          'in a national system, with a certificate that a university can accept.'),

    ('h1', '2.3  The role of IBM SkillsBuild'),
    ('p', 'IBM SkillsBuild is IBM\u2019s free digital learning platform. In this internship it '
          'supplied the technical curriculum and the credentialing. The offer letter describes '
          'access to the SkillsBuild platform with more than eighty thousand curated courses, and '
          'lists the technical scope of the programme as AI and machine learning concepts, large '
          'language models, IBM Granite models, retrieval-augmented generation frameworks and '
          'agentic AI systems.'),
    ('p', 'The platform\u2019s role is visible in the certificate structure. Two of the documents '
          'reproduced in this report are IBM SkillsBuild completion certificates, issued on '
          '1 August 2026 and 5 August 2026 for the completion of two learning plans associated '
          'with the internship. They are Completion Certificates of the SkillsBuild learning '
          'system, and they are distinct from the internship completion certificate issued by '
          '1M1B on 22 September 2026. The distinction matters and is stated in '
          + X('2.5  Internship duration and the dates that govern this report', 'Section 2.5')
          + ': a learning-plan certificate records that a module was completed, while the '
          'internship certificate records that the whole programme, including the project, was '
          'completed.'),
    ('p', 'The technology named in the internship\u2019s own material \u2014 IBM Granite \u2014 is '
          'IBM\u2019s family of enterprise foundation models. The internship did not require '
          'training a model; it required understanding what such a model can and cannot be '
          'trusted to do, and how to constrain it with prompts, retrieval and review. That '
          'understanding is the subject of ' + X('Technology Overview', 'Chapter 4') + '.'),
    ('figure', 'fig_ecosystem.png', FIGCAP('fig_ecosystem.png')),
    ('p', 'The figure above shows the five parties involved and what each one contributed. The '
          'student appears at the bottom because that is the honest hierarchy: the programme '
          'supplied structure and access, the technology partners supplied tools and curriculum, '
          'the University supplied the academic frame, and the work itself was done by the '
          'intern.'),

    ('h1', '2.4  Internship objectives and structure'),
    ('p', 'The internship\u2019s objectives can be taken directly from its own documents rather '
          'than reconstructed. The offer letter lists its highlights and its expectations; the '
          'programme structure described below follows that list, grouped into five objectives '
          'for clarity.'),
    ('table', {
        'key': 'objectives',
        'widths': [0.06, 0.40, 0.54],
        'header': ['No.', 'Objective stated for the internship', 'What it required in practice'],
        'rows': [
            ['1', 'Develop industry-relevant AI skills in the context of sustainable development',
             'Working through the SkillsBuild guided learning plan on AI, machine learning, large '
             'language models and IBM Granite, and applying the concepts to a live problem rather '
             'than to a textbook exercise'],
            ['2', 'Explore the intersection of AI and climate action, clean energy, waste '
                  'reduction, biodiversity and sustainable cities',
             'Choosing a specific sustainability problem, researching its published policy and '
             'science context, and justifying why an AI approach is appropriate to it'],
            ['3', 'Design and prototype an AI-powered sustainability solution with expert mentors',
             'Preparing a concept note, developing the modules on paper, presenting them for '
             'mentor feedback, and revising the design in response'],
            ['4', 'Learn directly from AI and emerging-technology professionals',
             'Attending the scheduled live sessions and workshops, and using the mentor sessions '
             'to test design decisions against practitioner judgement'],
            ['5', 'Complete the guided learning modules, self-learning labs, digital badges and '
                  'the final project',
             'Meeting the weekly milestones, completing the two SkillsBuild learning plans, and '
             'submitting the final project document, video and repository as required'],
        ],
        'note': 'Source: AICTE Internship Offer Letter for the 1M1B AI for Sustainability Virtual '
                'Internship (internship ID INTERNSHIP_17828984086a44dee80acf6).',
    }),
    ('p', 'Structurally, the programme ran as a repeating weekly cycle rather than as a single '
          'course. Each week combined self-paced learning on IBM SkillsBuild, one or more live '
          'sessions with mentors, a task or milestone to be completed, and feedback. The final '
          'weeks were given to the project: framing the problem, designing the response, '
          'documenting it and presenting it.'),
    ('table', {
        'key': 'schedule',
        'widths': [0.16, 0.30, 0.54],
        'header': ['Stage', 'Focus', 'What the intern did'],
        'rows': [
            ['Orientation', 'Programme briefing, expectations and terms',
             'Reviewed the offer letter and its terms, confirmed participation, and returned the '
             'signed declaration dated 27 July 2026'],
            ['Weeks 1\u20132', 'Foundations of AI, machine learning and responsible AI',
             'Completed the opening modules of the SkillsBuild learning plan; attended the '
             'scheduled live sessions; began researching sustainability problems'],
            ['Weeks 3\u20134', 'Large language models, IBM Granite, prompt engineering, '
                               'retrieval-augmented generation, agentic AI',
             'Worked through the technical modules; completed the first SkillsBuild learning plan '
             '(certificate dated 1 August 2026); shortlisted the waste-segregation problem'],
            ['Weeks 5\u20136', 'Solution design and project development',
             'Framed the problem statement, defined users, designed the three modules and the '
             'architecture, and prepared the project document; completed the second SkillsBuild '
             'learning plan (certificate dated 5 August 2026)'],
            ['Final phase', 'Project submission and presentation',
             'Submitted the final project document on 14 September 2026 and presented the work; '
             'the internship completion certificate was issued on 22 September 2026'],
        ],
        'note': 'Reconstructed from the internship offer letter, the two IBM SkillsBuild '
                'completion certificates, the SwachhAI project document and the internship '
                'completion certificate. The ordering reflects the programme\u2019s stated '
                'requirements; it does not claim to reproduce the content of any confidential '
                'session.',
    }),
    ('p', 'The sessions themselves are covered by the confidentiality clause of the offer letter, '
          'which prohibits disclosure of course material, session content and project-related '
          'discussions without written approval. This report therefore describes the '
          '<i>structure</i> of the programme and the <i>learning outcomes</i> it produced, and '
          'does not reproduce slides, recordings, internal documents or meeting links.'),

    ('h1', '2.5  Internship duration and the dates that govern this report'),
    ('p', 'Three different documents give three different date ranges, and a report that mixes '
          'them carelessly becomes inaccurate. The three are set out below exactly as they '
          'appear, followed by the reading this report adopts.'),
    ('table', {
        'key': 'dates',
        'widths': [0.30, 0.28, 0.42],
        'header': ['Document', 'Date or period stated', 'What it establishes'],
        'rows': [
            ['AICTE Internship Offer Letter (declaration signed 27 July 2026)',
             '\u201cA period of 6 weeks, from 28th July 2026 to 28th August 2026\u201d',
             'The <b>proposed</b> internship window at the time of selection'],
            ['IBM SkillsBuild completion certificate 1 (PLAN-56138075980A)',
             'Completion date 01 August 2026 (GMT)',
             'Completion of one learning plan within the internship'],
            ['IBM SkillsBuild completion certificate 2 (PLAN-F60F1D7DADA9)',
             'Completion date 05 August 2026 (GMT)',
             'Completion of the second learning plan within the internship'],
            ['SwachhAI final project document',
             'Submission date 14 September 2026',
             'The date on which the project deliverable was submitted'],
            ['Internship completion certificate (the governing document)',
             '\u201cfrom July 2026 to September 2026\u201d; issue date 22.09.2026',
             'The <b>actual certified period</b> of the internship'],
        ],
        'note': 'Where this report states a duration, it follows the completion certificate, '
                'because that is the document which certifies successful completion. The offer '
                'letter\u2019s six-week window is referred to only as the proposed window.',
    }),
    ('callout', '<b>Reading the dates.</b> The offer letter proposed a six-week internship '
                'beginning on 28 July 2026. The completion certificate, issued on 22 September '
                '2026, records that the internship ran from July 2026 to September 2026. Both '
                'statements are accurate about their own moment: the first is a plan, the second '
                'is a record. This report describes the internship as a <b>six-week programme '
                'that ran from July to September 2026</b>, and dates individual events \u2014 the '
                'declaration, the two learning-plan certificates, the project submission and the '
                'final certificate \u2014 exactly as the documents state them.'),
    ('figure', 'fig_timeline.png', FIGCAP('fig_timeline.png')),

    ('h1', '2.6  Learning sessions and activities'),
    ('p', 'Without reproducing restricted material, the activities that shaped this report can be '
          'described at the level of what they asked of the intern. Four kinds of activity '
          'recurred.'),
    ('bullets', [
        '<b>Guided learning.</b> Self-paced modules on the IBM SkillsBuild platform, organised as '
        'learning plans with checkpoints, covering AI and machine learning fundamentals, '
        'generative AI and large language models, prompt engineering, retrieval-augmented '
        'generation, agentic systems and responsible AI. Two plan completions are evidenced by '
        'the SkillsBuild certificates of 1 and 5 August 2026.',
        '<b>Live mentor sessions.</b> Scheduled online sessions with practitioners from 1M1B and '
        'IBM. Their value was less in new facts than in pressure-testing decisions: whether a '
        'problem was narrow enough to be solved, whether a proposed use of a language model was '
        'justified, and whether a claimed benefit could be measured.',
        '<b>Milestone tasks.</b> Weekly deliverables that converted learning into an artefact '
        '\u2014 a problem shortlist, a concept note, a design description, a presentation. The '
        'project document submitted on 14 September 2026 is the final accumulation of these.',
        '<b>The final project.</b> A complete proposal for an AI-assisted sustainability '
        'solution, submitted with a concept note, a short video and a code repository. The '
        'project described in this report is that submission.',
    ]),
    ('p', 'Two aspects of the programme deserve specific mention because they shaped the '
          'project\u2019s character. First, the internship\u2019s material returned repeatedly to '
          '<b>responsible AI</b> \u2014 fairness, transparency, privacy and human oversight were '
          'presented as design requirements rather than as concluding remarks. Second, the '
          'programme asked for a solution to a <i>field</i> problem rather than a demonstration '
          'of a technique. The project could not be \u201ca chatbot\u201d; it had to be a '
          'response to something specific that was failing in the world. That requirement is what '
          'produced the problem statement in ' + X('Problem Statement', 'Chapter 5') + '.'),
]

CH3 = [
    ('chapter', '3', 'Objectives and Learning Outcomes'),

    ('h1', '3.1  Introduction'),
    ('p', 'This chapter separates two things that are often merged in internship reports: what the '
          'internship set out to achieve, and what the intern actually gained. The first is a '
          'statement of intent and can be listed from the programme documents. The second is a '
          'claim about the student and has to be supportable \u2014 which is why each learning '
          'outcome below is tied to something that appears in this report or in an appended '
          'document, rather than to an adjective.'),

    ('h1', '3.2  Technical objectives'),
    ('p', 'The technical objectives were stated in the internship\u2019s own material and are '
          'reproduced with their practical meaning.'),
    ('numbered', [
        '<b>Understand the AI and machine learning pipeline well enough to reason about it.</b> '
        'Not to implement a neural network from scratch, but to understand what a model learns, '
        'what it does not learn, what data it requires and where it fails. This objective is '
        'addressed in ' + X('4.1  Artificial Intelligence and Machine Learning', 'Section 4.1')
        + '.',
        '<b>Understand large language models and the IBM Granite family.</b> How a language model '
        'generates text, why it can produce confident errors, and what an enterprise-oriented, '
        'open model family such as Granite is designed for. See '
        + X('4.2  Large Language Models', 'Section 4.2') + ' and '
        + X('4.3  IBM Granite', 'Section 4.3') + '.',
        '<b>Learn prompt engineering as a design discipline.</b> Writing instructions that '
        'constrain the output format, set a refusal rule and fix the tone, and then testing '
        'whether the model obeys them. See '
        + X('4.4  Prompt Engineering', 'Section 4.4') + '.',
        '<b>Understand retrieval-augmented generation.</b> Why an answer assembled from retrieved '
        'public documents is more trustworthy than an answer drawn from a model\u2019s memory, '
        'and what the retrieval pipeline actually looks like. See '
        + X('4.5  Retrieval-Augmented Generation', 'Section 4.5') + '.',
        '<b>Understand agentic AI.</b> The difference between a single question-and-answer '
        'exchange and a loop that perceives, decides, acts and learns. See '
        + X('4.6  Agentic AI', 'Section 4.6') + '.',
        '<b>Apply all of the above to one sustainability problem.</b> Not five problems. One, '
        'described well enough to be criticised. That application is '
        + X('Project Overview: SwachhAI', 'Chapter 6') + ' and '
        + X('Detailed Project Description', 'Chapter 7') + '.',
    ]),
    ('p', 'A seventh objective emerged during the work and was not in the original list: to '
          'produce technical documentation that a non-specialist could follow. Explaining a '
          'retrieval pipeline to a reader who has not met one is a different skill from building '
          'it, and it is the skill this report exists to demonstrate.'),

    ('h1', '3.3  Professional learning objectives'),
    ('p', 'The programme\u2019s terms set out professional expectations alongside technical ones: '
          'consistent participation, professional conduct, timely deliverables, confidentiality, '
          'ethical compliance and academic integrity. These are not abstract virtues in a virtual '
          'internship; each corresponds to a specific behaviour.'),
    ('bullets', [
        '<b>Working to a schedule without a supervisor in the room.</b> A virtual internship has '
        'no corridor conversations. Milestones either arrive or they do not, and the intern is '
        'responsible for the difference.',
        '<b>Receiving and using criticism.</b> Mentor feedback on an early concept note was the '
        'reason the project shifted from a general \u201cAI for waste\u201d idea to a specific '
        'household decision moment. Accepting that redirection quickly was more valuable than '
        'defending the first idea.',
        '<b>Respecting confidentiality.</b> The offer letter prohibits disclosure of course '
        'material, session content and project discussions. This report deliberately describes '
        'structure and outcomes rather than content, and it does not reproduce meeting links, '
        'internal documents or restricted material.',
        '<b>Using AI tools honestly.</b> The internship explicitly required responsible use of AI '
        'tools. In practice that meant using such tools for drafting and for checking wording, '
        'while keeping the problem framing, the design decisions and the technical claims the '
        'intern\u2019s own.',
        '<b>Documenting work as it happens.</b> A project document written from memory at the end '
        'is a reconstruction. Keeping notes during the design phase is what made the module '
        'descriptions in Chapter 7 possible.',
    ]),

    ('h1', '3.4  Exposure to AI and emerging technology'),
    ('p', 'For a third-year student, the internship\u2019s most valuable contribution was '
          'vocabulary with meaning attached. The table below records the technologies the '
          'internship introduced, and where each one surfaces in the project. The mapping is '
          'the reason the project is coherent rather than a list of buzzwords.'),
    ('table', {
        'key': 'techmap',
        'widths': [0.26, 0.34, 0.40],
        'header': ['Technology', 'What it means, briefly', 'Where it appears in SwachhAI'],
        'rows': [
            ['Artificial intelligence and machine learning',
             'Programmes that perform tasks associated with intelligence, usually by learning '
             'patterns from examples',
             'The classification of an item description into a waste stream'],
            ['Generative AI and large language models',
             'Models that produce new text by predicting likely continuations, conditioned on a '
             'prompt',
             'Understanding free-form item descriptions and composing guidance in plain language'],
            ['IBM Granite',
             'IBM\u2019s family of open, enterprise-oriented foundation models, designed to be '
             'fine-tuned and prompted for business tasks',
             'The model class the classifier and the assistant are designed around'],
            ['Prompt engineering',
             'Designing the instruction, examples, output format and refusal rules given to a '
             'model',
             'The classifier prompt, which fixes a JSON output shape and a confidence threshold'],
            ['Retrieval-augmented generation',
             'Retrieving relevant passages from a document collection and requiring the model to '
             'answer only from them',
             'The rule assistant, which answers waste-rule questions with citations'],
            ['Agentic AI',
             'A loop in which a system perceives, decides, acts and learns, using tools, rather '
             'than answering one question at a time',
             'The overall interaction model, including the pattern log that feeds taxonomy review'],
            ['Responsible AI',
             'Design practices for fairness, transparency, privacy, safety and human oversight',
             'Confidence display, honest refusal, client-side processing and human review gates'],
        ],
    }),
    ('p', 'Two things are worth noting. None of the seven is exotic \u2014 all are in current '
          'industrial use, which is why the internship covered them. And they are layered rather '
          'than parallel: prompting and retrieval are techniques <i>for</i> using a language model, '
          'agentic design is a pattern for <i>organising</i> those uses, and responsible AI is a '
          'set of constraints on all of it. The next chapter explains each layer in turn.'),

    ('h1', '3.5  Skills and knowledge gained'),
    ('p', 'The table below states each outcome with the evidence that supports it. It is '
          'deliberately conservative: where an outcome is a change in understanding rather than a '
          'demonstrable artefact, the evidence is the explanation given in this report, not a '
          'certificate.'),
    ('table', {
        'key': 'outcomes',
        'widths': [0.30, 0.36, 0.34],
        'header': ['Outcome', 'What was actually gained', 'Where it is evidenced'],
        'rows': [
            ['Technical literacy in applied AI',
             'The ability to explain, in plain terms, what a language model does, why it '
             'hallucinates, and what retrieval and prompting change about that',
             'Chapter 4 of this report'],
            ['Design under constraint',
             'Practice at reducing a broad problem to a specific intervention, and at rejecting '
             'features that could not be justified',
             'Chapters 5 to 7'],
            ['Responsible-AI reasoning',
             'The habit of asking, for each capability, what happens when it is wrong, and who is '
             'harmed',
             'Chapter 8; the system disclosure table'],
            ['Policy and standards research',
             'Locating and reading primary sources \u2014 the Solid Waste Management Rules, 2016, '
             'the E-Waste and Battery Waste Rules, 2022 \u2014 instead of relying on summaries',
             'Chapter 5 and the References'],
            ['Quantitative reasoning about impact',
             'Converting behaviour change into a defensible estimate, and stating its uncertainty '
             'instead of hiding it',
             'Section 7.3 and Table 16'],
            ['Technical writing and diagramming',
             'Explaining an architecture to a reader who did not design it, using block diagrams, '
             'workflows and tables',
             'Every figure and table in this report'],
            ['Professional discipline',
             'Meeting milestones without supervision, and separating what was done from what was '
             'intended',
             'Sections 2.5 and 2.6; the appendices'],
        ],
    }),
    ('callout', '<b>What was not gained.</b> It would be easy to overstate this section. The '
                'internship did not make the intern a machine learning engineer: no model was '
                'trained, no dataset was curated and no benchmark was reproduced. What it did '
                'produce is a working understanding of how these systems are assembled, '
                'constrained and supervised \u2014 which is the appropriate outcome for a '
                'six-week programme, and the honest one to record.'),
]

CH4 = [
    ('chapter', '4', 'Technology Overview'),

    ('h1', '4.1  Artificial Intelligence and Machine Learning'),
    ('p', 'Artificial intelligence is the name for the project of getting computers to do things '
          'that would require intelligence if a person did them: recognising a face, '
          'understanding a sentence, choosing a route, recommending a film. Machine learning is '
          'the dominant approach to that project today. Instead of writing rules that describe '
          'how to perform the task, a machine learning system is given examples and adjusts '
          'internal numbers until its outputs match the examples. The rules are discovered, not '
          'written.'),
    ('p', 'The distinction matters for the SwachhAI project. A rule-based waste application would '
          'consist of a long list of item names and their bins. It would work for the items on the '
          'list and fail for everything else \u2014 and household waste is precisely the domain '
          'where \u201ceverything else\u201d dominates. A resident types \u201cdoodh ka '
          'packet\u201d, then \u201cmilk pouch\u201d, then \u201cplastic milk cover\u201d, then '
          '\u201cbananna peel\u201d with a typo. A learned model generalises across these '
          'variations in a way that a list cannot.'),
    ('figure', 'fig_ai_stack.png', FIGCAP('fig_ai_stack.png')),
    ('p', 'Three families of machine learning are worth distinguishing, because they correspond to '
          'three different jobs. <b>Supervised learning</b> learns from labelled examples: here '
          'are ten thousand photographs of waste, each already labelled with its stream, learn to '
          'label new ones. <b>Unsupervised learning</b> looks for structure without labels: here '
          'are a city\u2019s collection records, find the neighbourhoods that behave '
          'differently. <b>Reinforcement learning</b> learns from reward: take this action, '
          'receive this score, improve. The project\u2019s classifier is conceptually a supervised '
          'classification task; the impact forecaster is deliberately <i>not</i> a learned model '
          'at all, for reasons given in ' + X('Project Overview: SwachhAI', 'Chapter 6') + '.'),
    ('p', 'Every learned model carries three properties that a user should know about. It has a '
          '<b>training distribution</b> \u2014 the kind of data it has seen \u2014 and it degrades '
          'outside it; a classifier trained on urban Indian household waste should not be trusted '
          'on hospital waste. It has an <b>error rate</b>, and errors are not uniformly '
          'distributed: a model may be excellent at plastics and poor at composite items. And it '
          'has a <b>confidence</b> that is useful only if it is calibrated, meaning that when the '
          'model says 80 per cent, it is right about eighty times in a hundred. The project\u2019s '
          'decision to display confidence on every classification, and to treat anything below 75 '
          'as \u201cunknown\u201d, follows directly from this third property.'),

    ('h1', '4.2  Large Language Models'),
    ('p', 'A large language model is a machine learning model trained to predict the next token in '
          'a sequence of text. A token is a fragment of a word \u2014 often a whole short word, '
          'sometimes part of a longer one. Training exposes the model to an enormous quantity of '
          'text and adjusts its parameters so that, given any preceding text, it assigns high '
          'probability to continuations that resemble real writing.'),
    ('figure', 'fig_llm_pipeline.png', FIGCAP('fig_llm_pipeline.png')),
    ('p', 'Two consequences of this design matter for the project. First, the model has no '
          'database to consult. When it produces a statement about the Battery Waste Management '
          'Rules, 2022, it is producing a plausible continuation, not retrieving a record. It may '
          'be right because such statements appeared in its training data; it may be wrong in a '
          'way that reads exactly the same. This failure mode is usually called '
          '<b>hallucination</b>, and it is the single most important limitation to design around '
          'in an application that gives advice about public rules.'),
    ('p', 'Second, the model\u2019s behaviour is steerable through the text it is given. That '
          'steering is what prompt engineering does, and it is also what makes '
          'retrieval-augmented generation possible: if the relevant rule text is placed in front '
          'of the model and the model is instructed to answer only from that text, the '
          'probability of a fabricated rule drops sharply \u2014 though, as described in '
          + X('4.5  Retrieval-Augmented Generation', 'Section 4.5') + ', it does not fall to '
          'zero.'),
    ('table', {
        'key': 'genai',
        'widths': [0.28, 0.36, 0.36],
        'header': ['Property', 'What it means', 'How the project responds'],
        'rows': [
            ['Probabilistic output',
             'The same prompt can produce different wording on different runs',
             'The classifier prompt fixes a strict JSON output shape, so the interface always '
             'receives the same fields'],
            ['No guaranteed factual grounding',
             'Statements about rules may be invented and are hard to distinguish from true ones',
             'The rule assistant may answer only from retrieved passages, and must cite them'],
            ['Context window limits',
             'Only a bounded amount of text can be supplied with a question',
             'Retrieval selects a small number of passages rather than pasting whole documents'],
            ['Sensitivity to phrasing',
             'Small changes in the prompt can change the output materially',
             'Prompts are treated as versioned design artefacts and reviewed like code'],
            ['Language bias',
             'Performance is usually weaker in low-resource languages and in transliterated text',
             'The prompt explicitly accepts Hinglish, romanisation and misspellings, and falls '
             'back to a deterministic matcher'],
        ],
    }),

    ('h1', '4.3  IBM Granite'),
    ('p', 'IBM Granite is IBM\u2019s family of foundation models. The family is described by IBM '
          'as open, enterprise-oriented and available under permissive licensing, and it includes '
          'instruction-tuned language models of a few billion parameters, mixture-of-experts '
          'variants, and specialised models for tasks such as code, time series and guardrails. '
          'The models are designed to be adapted by organisations \u2014 prompted, fine-tuned or '
          'grounded in their own data \u2014 rather than used only as a general chatbot.'),
    ('p', 'For a student, three features of this family are more instructive than parameter counts. '
          'First, <b>open weights</b>: the model can be downloaded and run locally, which makes it '
          'possible to study and to build without a permanent connection to a vendor service. '
          'Second, <b>instruction tuning</b>: the models are trained to follow directions in a '
          'structured chat format, which is what makes prompt engineering a meaningful activity '
          'rather than a hopeful one. Third, <b>governance models</b>: the family includes '
          'companion models intended to detect harmful or off-policy content, which reflects the '
          'industrial assumption that a language model is deployed inside a system of checks, not '
          'on its own.'),
    ('p', 'The internship used the Granite family as the reference model class for the project. '
          'This distinction is important for accuracy: SwachhAI is <i>designed around</i> a '
          'Granite-style small instruction-tuned model, and the project document describes the '
          'model layer as \u201cGranite-style\u201d. The project does not claim to have trained, '
          'fine-tuned or benchmarked a Granite model, and this report does not make that claim '
          'either.'),
    ('p', 'Why a small, instruction-tuned model suits this problem is a design argument rather '
          'than a preference. The task is narrow: extract an item and its material clues, choose '
          'one of eight streams, produce a confidence and write four short steps. A very large '
          'general model is unnecessary and expensive per query; a small model that follows a '
          'fixed instruction reliably is sufficient, cheaper, and easier to keep private because '
          'it can run locally.'),

    ('h1', '4.4  Prompt Engineering'),
    ('p', 'Prompt engineering is the practice of designing the text a model receives so that it '
          'produces a useful, predictable and safe output. It is not a trick for circumventing a '
          'model; it is the interface specification of an AI feature. A well-engineered prompt '
          'for a production feature typically specifies five things.'),
    ('numbered', [
        '<b>Role and scope.</b> What the model is, and what it is not. In the project: '
        '\u201cYou are SwachhAI, a municipal solid-waste assistant for Indian households.\u201d',
        '<b>Input description.</b> What the model will receive, including its imperfections. In '
        'the project: an item description in any language or romanisation, possibly with typos or '
        'a photo caption stub.',
        '<b>Task decomposition.</b> The steps to perform, in order. In the project: extract the '
        'item and material clues, map to exactly one of eight streams, calibrate confidence, '
        'produce up to four steps and one fact.',
        '<b>Output contract.</b> The exact shape of the response. In the project: a strict JSON '
        'object with fixed keys, so that the interface can render a card without guessing.',
        '<b>Rules and refusal conditions.</b> What the model must never do, and when it must '
        'decline. In the project: never guess when unsure; below a confidence of 75 the stream '
        'becomes \u201cunknown\u201d; never shame the user; hazardous instructions must mention '
        'wrap, mark and separate.',
    ]),
    ('p', 'Two engineering habits turn prompting from an anecdote into a practice. The first is '
          '<b>few-shot examples</b>: including two or three worked input-output pairs in the '
          'prompt so that the model can imitate the shape and tone of the answer, which is '
          'considerably more reliable than describing the shape in prose. The second is '
          '<b>deterministic post-processing</b>: never trusting the model alone. In the project, '
          'the returned stream is checked against the taxonomy, a confidence below the threshold '
          'is overridden, and a fallback matcher handles the case where the model\u2019s output '
          'cannot be parsed at all. The prompt is the first line of defence; the code around it is '
          'the second.'),
    ('callout', '<b>An example of the discipline.</b> A weak prompt says: \u201cTell the user '
                'which bin to use.\u201d A production prompt says: which streams exist, that '
                'exactly one must be chosen, that confidence below 75 becomes '
                '\u201cunknown\u201d, that the safety step comes first, that the output must be '
                'JSON with five named keys, and that the assistant must never shame the user. The '
                'second version is longer, and it is the version that can be tested.'),

    ('h1', '4.5  Retrieval-Augmented Generation'),
    ('p', 'Retrieval-augmented generation, usually shortened to RAG, is a pattern for making a '
          'language model answer from a specified body of documents rather than from its '
          'parameters. It has two halves. Offline, the documents are split into passages, each '
          'passage is converted into a numeric vector that represents its meaning, and the vectors '
          'are stored in an index. Online, a user\u2019s question is converted into a vector in '
          'the same space, the nearest passages are retrieved, and the model is asked to compose '
          'an answer <i>using only those passages</i>.'),
    ('figure', 'fig_rag_pipeline.png', FIGCAP('fig_rag_pipeline.png')),
    ('p', 'Three details separate a working RAG system from a demonstration. The first is '
          '<b>chunking</b>: passages must be small enough to be specific and large enough to be '
          'meaningful, and they must carry their source title so that a citation can be produced. '
          'The second is <b>re-ranking</b>: vector similarity returns passages that are '
          'topically close, which is not the same as passages that contain the answer, so a '
          'second pass scores individual sentences against the question. The third, and the most '
          'important for this project, is the <b>refusal path</b>: if the best passage scores too '
          'low, the system must say that it cannot answer from the available documents. Without '
          'that path, RAG becomes a machine for attaching citations to guesses.'),
    ('p', 'The appeal of RAG in a public-information context is that it makes an answer '
          '<b>auditable</b>. A resident who reads \u201cbatteries must not go into household '
          'bins\u201d can be shown which document says so, and can check it. It also makes the '
          'system <b>maintainable</b>: when a rule is amended, the corpus is updated and the '
          'answers change, whereas a model\u2019s memorised knowledge cannot be edited in the same '
          'way. The cost is that RAG is only as good as its corpus, which is why the project '
          'states its corpus \u2014 twenty public documents \u2014 openly, and states its absence '
          'of municipal-specific bylaws as a known limit.'),

    ('h1', '4.6  Agentic AI'),
    ('p', 'An agentic system does not merely answer a question; it pursues a goal through a loop. '
          'The loop is usually described in four stages: <b>perceive</b> the situation, '
          '<b>decide</b> what to do, <b>act</b> using available tools, and <b>learn</b> from the '
          'result so that the next iteration is better. The word \u201cagent\u201d is used because '
          'the system takes initiative within its scope rather than waiting to be asked each '
          'individual step.'),
    ('figure', 'fig_agent_loop.png', FIGCAP('fig_agent_loop.png')),
    ('p', 'Agentic design is powerful, and it is also where AI systems become difficult to '
          'supervise, because a loop can amplify a small error. The project keeps the autonomy '
          'narrow and places a person at the only point where the loop could cause wider harm. The '
          'system may classify an item, retrieve a rule, compose guidance and log an anonymised '
          'pattern without asking anyone; it may <i>not</i> change its own taxonomy, admit a new '
          'document or act on behalf of a household. Those changes require human review, which is '
          'shown in the figure as the oversight gate.'),
    ('p', 'This is a defensible pattern for public-interest AI: automate the repetitive, '
          'interactive part of the task, and keep the consequential part under human control. It '
          'also happens to be what the internship\u2019s responsible-AI material argues for, and '
          'it is revisited in ' + X('Responsible AI and Sustainability', 'Chapter 8') + '.'),

    ('h1', '4.7  Responsible AI'),
    ('p', 'Responsible AI is the set of design practices that keep an AI system fair, '
          'transparent, private, safe and accountable. It is often written as a list of '
          'principles, which makes it easy to agree with and hard to implement. The internship\u2019s '
          'material treated it as a set of testable behaviours, and the project followed that '
          'treatment.'),
    ('figure', 'fig_responsible_ai.png', FIGCAP('fig_responsible_ai.png')),
    ('p', 'Five behaviours are treated as requirements in the project. <b>Transparency</b>: every '
          'classification shows its confidence, and every coefficient used in an estimate is '
          'published in plain sight. <b>Fairness</b>: the system accepts Hinglish, transliteration '
          'and misspellings, so that a resident who is more comfortable in Hindi is not excluded '
          'from correct disposal; and it models shared bins and rented rooms rather than assuming '
          'a nuclear household with a garden. <b>Privacy</b>: the design processes input on the '
          'device, uploads no photographs and asks only for quantities, never names or addresses. '
          '<b>Ethics</b>: the system refuses rather than invents, and human safety outranks '
          'recycling purity \u2014 a mercury lamp is a hazard before it is a recycling '
          'opportunity. <b>Oversight</b>: changes to the taxonomy or the corpus pass through human '
          'review.'),
    ('p', 'The feature of this list that a student should notice is that none of the five is '
          'achieved by adding a disclaimer. Each one changes the system\u2019s design: the '
          'confidence threshold exists because of transparency, the client-side architecture '
          'exists because of privacy, and the refusal path exists because of honesty. That is the '
          'difference between responsible AI as a value and responsible AI as an engineering '
          'constraint.'),
    ('callout', '<b>Why this belongs in the technology chapter.</b> It is tempting to treat '
                'responsible AI as a concluding section about ethics. In practice it is a design '
                'input that constrains the architecture as much as performance does, and the '
                'project would be a different system \u2014 easier to build, less defensible '
                '\u2014 without it.'),
]

CH5 = [
    ('chapter', '5', 'Problem Statement'),

    ('h1', '5.1  Waste management in India at a glance'),
    ('p', 'India\u2019s municipal solid waste problem is usually described with two numbers and '
          'one phrase. The numbers are the quantity of waste generated and the fraction of it that '
          'is processed; the phrase is \u201csegregation at source\u201d, which appears in every '
          'policy document on the subject. The Central Pollution Control Board\u2019s annual '
          'report on the implementation of the Solid Waste Management Rules, 2016 for 2020\u201321 '
          'records municipal areas generating about <b>1,60,039 tonnes per day</b> of solid waste, '
          'of which about <b>1,52,750 tonnes per day</b> was collected ' + C(1) + '. Of what was '
          'collected, roughly half was treated and a substantial remainder went to landfill, with '
          'a further quantity accounted for as unprocessed.'),
    ('p', 'These figures should be read with care, and three cautions belong beside them. First, '
          'they are a national aggregate over a reporting year and conceal enormous variation '
          'between states and between cities within a state. Second, the categories in the '
          'reporting \u2014 generated, collected, treated, landfilled \u2014 are not a clean '
          'partition, and different summaries of the same report quote different subsets. Third, '
          'they describe municipal solid waste, which is the stream a household influences '
          'directly, and they do not include construction and demolition debris, e-waste, '
          'battery waste or hazardous industrial waste, each of which has its own rules and its '
          'own reporting.'),
    ('p', 'The statutory frame for household waste is the <b>Solid Waste Management Rules, '
          '2016</b>, notified by the Ministry of Environment, Forest and Climate Change on '
          '8 April 2016 ' + C(2) + '. The rules, among other things, make source segregation a '
          'duty of the waste generator, require local bodies to establish door-to-door collection '
          'and separate streams, address sanitary waste, and require user fees and spot fines for '
          'littering and non-segregation as specified by local bodies. They also sit within a '
          'wider set of instruments: the Plastic Waste Management Rules as amended in 2021, the '
          'E-Waste (Management) Rules, 2022, the Battery Waste Management Rules, 2022, and the '
          'Construction and Demolition Waste Management Rules, 2016.'),
    ('table', {
        'key': 'rules',
        'widths': [0.30, 0.26, 0.44],
        'header': ['Instrument', 'Notified', 'What it means for a household'],
        'rows': [
            ['Solid Waste Management Rules, 2016',
             '8 April 2016 (MoEFCC) ' + C(2),
             'Source segregation is a duty; the generator is expected to hand over segregated '
             'wet, dry and domestic hazardous waste, and to pay user fees and fines as notified '
             'by the local body'],
            ['Plastic Waste Management Rules, 2016 as amended (2021)',
             '2016; amendment 2021 ' + C(4),
             'Thickness and labelling requirements for plastic carry bags; a list of banned '
             'single-use plastic items from 1 July 2022; recycled content conforming to BIS '
             'standards'],
            ['E-Waste (Management) Rules, 2022',
             '2 November 2022, in force 1 April 2023 ' + C(5),
             'Electronic waste must travel through authorised collection and recycling routes; '
             'extended producer responsibility places obligations on producers'],
            ['Battery Waste Management Rules, 2022',
             '24 August 2022 ' + C(3),
             'Waste batteries must be collected, not landfilled or incinerated; producers carry '
             'extended producer responsibility; retail take-back is part of the intended route'],
            ['Construction and Demolition Waste Management Rules, 2016',
             '29 March 2016 ' + C(6),
             'Debris is a separate stream with its own handling; it should not enter municipal '
             'bins'],
        ],
        'note': 'Publication details verified against the Gazette notifications and the '
                'corresponding ministry or CPCB releases; see the References for full entries.',
    }),
    ('p', 'Finally, the policy ambition is not merely to collect waste but to stop treating it as '
          'waste. Swachh Bharat Mission\u2013Urban 2.0, launched on 1 October 2021 for the period '
          'to 1 October 2026, sets the vision of \u201cGarbage Free Cities\u201d and gives '
          'substantial weight to door-to-door collection, source segregation, waste processing and '
          'dumpsite remediation ' + C(7) + '. Source segregation is therefore not a private '
          'lifestyle preference; it is the first step on which the rest of the municipal system '
          'depends.'),

    ('h1', '5.2  The household segregation problem'),
    ('p', 'Why, then, does segregation at source remain uneven? The explanation most often offered '
          'is indifference: people do not care, or will not change. That explanation is '
          'convenient because it locates the problem in other people. The project document '
          'records a different reading, arrived at through observation and interviews, and it is '
          'the reading this report adopts. Residents, by and large, are willing. What they lack is '
          'an answer at the moment they need it.'),
    ('p', 'Consider the actual situation. A resident is standing at a bin with an object in one '
          'hand and perhaps four or five seconds available. The object may be a milk pouch with '
          'residue in it, a CFL tube, a chips packet with a foil lining, a used battery, a '
          'battery-operated toy, a broken ceramic mug, a torn school shirt. For each of these the '
          'correct answer is genuinely uncertain to a non-specialist, and the answers are not '
          'obvious even to an interested person:'),
    ('bullets', [
        '<b>The milk pouch</b> is plastic, so \u201cplastic\u201d suggests recycling \u2014 but a '
        'pouch with milk residue inside will contaminate the batch it is bundled with unless it is '
        'cut open, rinsed and dried.',
        '<b>The CFL tube</b> contains a small amount of mercury, so it is domestic hazardous '
        'waste, not general dry waste \u2014 a distinction that matters to the person who handles '
        'it next.',
        '<b>The chips packet</b> is a multi-layer laminate, which is largely non-recyclable in '
        'practice; it belongs in the reject stream, not with clean plastics.',
        '<b>The battery</b> looks like a small harmless object and is, by the rules, domestic '
        'hazardous waste with a dedicated take-back route ' + C(3) + '.',
    ]),
    ('p', 'A poster at the bin cannot resolve these cases, because the poster must generalise and '
          'these cases are specific. A municipal website can explain the rules, but it explains '
          'them in formal language, in English, at the length of a regulation. What is missing is '
          'not information; it is an <b>interface between the resident and the information</b>, '
          'available in the seconds available, in the language the resident actually uses.'),
    ('figure', 'fig_problem_tree.png', FIGCAP('fig_problem_tree.png')),
    ('p', 'The figure above separates four causes that are often conflated. The <b>information '
          'gap</b> is the absence of a per-item answer at the decision moment. The <b>language '
          'gap</b> is that official guidance is written in formal English while the resident may '
          'think in Hinglish. <b>Contamination</b> is a physical consequence of the first two: '
          'residue on one item spoils a batch. The <b>hazard blind spot</b> is the special case '
          'where a mis-sorted item endangers a person rather than a process. A household tool can '
          'address the first two directly, and influence the second two indirectly. It cannot '
          'address collection capacity, transport, or processing infrastructure, and the project '
          'does not pretend otherwise.'),

    ('h1', '5.3  Recycling and contamination'),
    ('p', 'Contamination is the least visible and most expensive part of the problem. Recycling '
          'is a manufacturing process, and it requires input of predictable quality. When wet '
          'waste, food residue or mixed-material items enter a dry recyclables stream, three '
          'things happen. The contaminated material itself loses value, because a buyer of '
          'recycled fibre or film will not accept material soaked in organic matter. The materials '
          'around it lose value too, because bales are graded as a unit and one wet sack of paper '
          'degrades a bale. And the cost of the loss is not borne by the resident who caused it; '
          'it is borne by the material recovery facility, by the recycler, and eventually by the '
          'municipal budget.'),
    ('figure', 'fig_contamination.png', FIGCAP('fig_contamination.png')),
    ('p', 'The economic consequence is a familiar trap. If inbound dry waste is contaminated, the '
          'recovered material sells for less; if it sells for less, the facility struggles; if the '
          'facility struggles, there is less capacity to accept material; and the material that '
          'cannot be accepted goes to landfill. Better segregation upstream is, in most Indian '
          'cities, a cheaper intervention than new processing capacity downstream, because it '
          'improves the productivity of capacity that already exists. The project makes this '
          'argument as a design motivation, not as a claim of measured effect: no facility data '
          'was collected during the internship.'),

    ('h1', '5.4  Sanitation worker safety'),
    ('p', 'The most serious consequence of mixed waste is not economic. Waste that arrives mixed '
          'arrives unmarked, and unmarked waste is handled by people. Batteries, broken glass, '
          'discarded needles and blades, and mercury-bearing lamps travel inside mixed bags to '
          'collection workers, to waste pickers and to facility staff. The project document '
          'records worker interviews in which needle injuries were described as routine, and it '
          'treats that description as the strongest single argument for resident-side guidance.'),
    ('p', 'This reframes the purpose of a household application. The resident is not the only user '
          'who benefits. A guidance card that tells a household to wrap a broken bulb in paper, '
          'label it, and hand it over separately is written for the generator but it protects the '
          'handler. It is therefore a design principle of the project that <b>the safety step comes '
          'first</b> in every hazardous-waste protocol, before any instruction about recycling or '
          'material value. Human safety outranks material recovery, every time.'),
    ('p', 'The same framing disciplines how the project talks about sanitation workers. They are '
          'beneficiaries to be protected, not a population to be monitored, scored or policed. '
          'That is why the design includes no performance ranking of workers, no photograph-based '
          'monitoring and no household-level surveillance, and why the later-phase analytics '
          'described in ' + X('9.4  Future scope of SwachhAI', 'Section 9.4') + ' are '
          'aggregate-only.'),

    ('h1', '5.5  Environmental and sustainability concerns'),
    ('p', 'A large fraction of Indian household waste is organic \u2014 the project document uses '
          'a 55/25/20 working split of organic, dry recyclable and reject material. When organic '
          'waste is segregated and composted, the carbon in it returns to soil and the process is '
          'aerobic. When the same waste is buried in a mixed landfill, it decomposes without '
          'oxygen and produces methane, a greenhouse gas with a far higher warming effect per '
          'kilogram than carbon dioxide over a hundred-year horizon. The Sixth Assessment Report '
          'of the Intergovernmental Panel on Climate Change gives a hundred-year global warming '
          'potential for non-fossil methane of about <b>27</b> and for fossil methane of about '
          '<b>29.8</b>, relative to carbon dioxide ' + C(8) + '. That is the climate arithmetic '
          'behind a household bin.'),
    ('p', 'Three further environmental consequences follow from mixed waste. Leachate \u2014 the '
          'liquid that drains from decomposing waste \u2014 can carry organic load and heavy '
          'metals into soil and water. Open burning of waste, including at dumpsites, releases '
          'particulate matter and dioxins, and is a recurring public-health complaint near legacy '
          'sites. And the loss of recyclable material forces the production of virgin material, '
          'which for metals and plastics carries a substantial energy penalty compared with '
          'recycling.'),
    ('p', 'The global picture is consistent with the local one. The United Nations Environment '
          'Programme\u2019s Food Waste Index Report 2024 estimated that about <b>1.05 billion '
          'tonnes</b> of food was wasted in 2022 across households, food service and retail, with '
          'households the largest contributor ' + C(9) + '. In a country where a large share of '
          'household waste is food waste, keeping organics out of landfill is simultaneously a '
          'waste problem, an emissions problem and a soil problem.'),
    ('callout', '<b>Scope note.</b> None of the statistics in this chapter were generated by the '
                'project. They are published figures used to establish that the problem is real '
                'and that the design is aimed at a genuine gap. Where the project itself produces '
                'a number \u2014 for example, an estimate of carbon dioxide equivalent avoided '
                '\u2014 that number is explicitly labelled as modelled, and the arithmetic behind '
                'it is published in ' + X('Project Overview: SwachhAI', 'Chapter 6') + '.'),
]

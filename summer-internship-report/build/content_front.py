"""Preliminary pages."""
from model import K, X, E, C, FIGCAP, TABSPEC

STUDENT = 'Mohammad Ramish Ansari'
UNIV = 'University of Lucknow, Lucknow'
DEPT = 'Department of Computer Science and Engineering'
IID = 'INTERNSHIP_17828984086a44dee80acf6'

FRONT = [
    ('cover',),
    ('pagebreak',),
    ('h1_front', 'DECLARATION'),
    ('p', 'I, <b>%s</b>, a student of the third year (Semester V) of the Bachelor of Technology '
          'programme in Computer Science and Engineering at the %s, hereby declare that the '
          'Summer Internship Report titled <b>\u201cSwachhAI: AI-Guided Waste Segregation and '
          'Circularity Assistant for India\u2019s Households\u201d</b> is a record of work carried '
          'out by me during the 1M1B AI for Sustainability Virtual Internship, offered by 1M1B '
          '(One Million for One Billion), supported by the All India Council for Technical '
          'Education (AICTE) and delivered in collaboration with IBM SkillsBuild, during '
          'July to September 2026.' % (STUDENT, UNIV)),
    ('p', 'I further declare that the technical explanations, module descriptions and conceptual '
          'designs presented in this report are my own work, prepared from the public documents '
          'listed in the References and from the guidance provided during the internship. The '
          'report does not reproduce confidential course material, private meeting links or any '
          'restricted content shared by the organising bodies, and it does not present the '
          'proposed design as a tested or deployed product. No part of this report has been '
          'submitted for the award of any other degree or diploma.'),
    ('p', 'Where the report draws on published rules, standards or studies, the source is cited. '
          'Where an estimate is modelled rather than measured, it is described as modelled. The '
          'coloured certificate reproduced in this report is a copy of the certificate issued to '
          'me on 22 September 2026.'),
    ('spacer', 26),
    ('sigblock', [
        ('Place: Lucknow', ''),
        ('Date: ______________', ''),
        ('', ''),
        ('', '%s' % STUDENT),
        ('', 'B.Tech. Computer Science and Engineering'),
        ('', 'Semester V, %s' % UNIV),
    ]),
    ('pagebreak',),
    ('h1_front', 'CERTIFICATE'),
    ('p', 'A colour copy of the internship completion certificate issued by 1M1B, supported by '
          'AICTE and in collaboration with IBM SkillsBuild, follows on the next page. It is '
          'reproduced here exactly as issued, and it is the primary evidence for the completion '
          'of the internship described in this report.'),
    ('p', 'The certificate records that the internship was carried out from <b>July 2026 to '
          'September 2026</b>, that it was issued on <b>22 September 2026</b>, and that it '
          'carries the AICTE Internship ID <b>%s</b>. Supporting certificates from IBM '
          'SkillsBuild, together with the AICTE offer letter, are reproduced in the appendices.'
          % IID),
    ('spacer', 10),
    ('certpage', [
        ('certificates/cert_main.png',
         'Internship completion certificate issued by 1M1B, supported by AICTE, in collaboration '
         'with IBM SkillsBuild (issued 22 September 2026)'),
    ]),
    ('pagebreak',),
    ('h1_front', 'ABSTRACT'),
    ('p', 'This report documents a six-week virtual summer internship carried out under the '
          '<b>1M1B AI for Sustainability Virtual Internship</b>, an AICTE-listed programme '
          'delivered in collaboration with IBM SkillsBuild. The internship combined guided '
          'learning on artificial intelligence with a project requirement: identify a real '
          'sustainability problem and design an AI-assisted response to it. The work described '
          'here was carried out between July and September 2026 and was certified on '
          '22 September 2026.'),
    ('p', 'The project developed during the internship is <b>SwachhAI</b>, a decision-support '
          'concept for household waste segregation in Indian cities. Its starting observation is '
          'simple: most Indian households do not sort their waste, not because they are '
          'indifferent, but because the correct answer for a specific item is rarely available at '
          'the moment it is thrown away. SwachhAI addresses that gap with three cooperating '
          'modules \u2014 a classifier that maps an item to one of eight waste streams with a '
          'stated confidence, a retrieval-augmented rule assistant that answers questions about '
          'municipal waste rules only from cited public documents, and an impact forecaster that '
          'converts a household\u2019s habits into a transparent estimate of waste diverted and '
          'carbon dioxide equivalent avoided.'),
    ('p', 'The report explains the technologies involved in plain technical language: machine '
          'learning, large language models, the IBM Granite family, prompt engineering, '
          'retrieval-augmented generation, agentic AI and responsible AI. It describes the '
          'problem, the users, the conceptual architecture and the three modules through block '
          'diagrams, workflow diagrams, tables and illustrative examples. It states clearly what '
          'the project claims and what it does not, and it distinguishes modelled estimates from '
          'measured results.'),
    ('p', 'No working model was built for this report. The report is an academic document, not a '
          'software deliverable: it explains a design, its reasoning and its limits. The most '
          'important learning recorded is that the hard part of applied AI in the public interest '
          'is not the model. It is deciding when the model should decline to answer, what '
          'evidence an answer must be built from, and who remains accountable when the answer '
          'reaches a person standing at a dustbin with five seconds to spare.'),
    ('spacer', 8),
    ('p', '<b>Keywords:</b> artificial intelligence, large language models, IBM Granite, '
          'retrieval-augmented generation, prompt engineering, agentic AI, responsible AI, '
          'solid waste management, source segregation, circular economy, Sustainable Development '
          'Goals 11, 12 and 13.'),
    ('pagebreak',),
    ('h1_front', 'ACKNOWLEDGEMENT'),
    ('p', 'An internship that begins with a form and a deadline is completed by people. I am '
          'grateful to several of them.'),
    ('p', 'I thank <b>1M1B (One Million for One Billion)</b> for designing a programme that '
          'treated a college student as capable of working on a real problem, and for the mentors '
          'who reviewed progress week after week. I thank the <b>All India Council for Technical '
          'Education (AICTE)</b> for listing and supporting the internship, and the <b>AICTE '
          'National Internship Portal</b> for the infrastructure that made the placement '
          'possible. I thank <b>IBM SkillsBuild</b> for the guided learning plan, the digital '
          'badges, and the grounding in Granite, retrieval-augmented generation and responsible '
          'AI that made the project technically possible.'),
    ('p', 'At the %s, I thank the faculty and staff of the <b>%s</b> for the academic '
          'grounding in data structures, databases, operating systems and programming that this '
          'work leaned on, and for the guidance on this report\u2019s prescribed format.' % (UNIV, DEPT)),
    ('p', 'I thank my family for tolerating a summer of early calls and late drafts, and my '
          'classmates for arguing with me about the design until it improved.'),
    ('p', 'Any error that remains is mine. The interpretations, diagrams and judgement calls '
          'in this report are my own work, prepared within the University\u2019s academic '
          'honesty requirements and the internship\u2019s ethical-use expectations.'),
    ('spacer', 26),
    ('sigblock', [
        ('', ''),
        ('', ''),
        ('', '%s' % STUDENT),
        ('', 'B.Tech. Computer Science and Engineering, Semester V'),
        ('', '%s' % UNIV),
    ]),
    ('pagebreak',),
    ('h1_front', 'TABLE OF CONTENTS'),
    ('toc',),
    ('pagebreak',),
    ('h1_front', 'LIST OF TABLES'),
    ('lot',),
    ('pagebreak',),
    ('h1_front', 'LIST OF FIGURES'),
    ('lof',),
]

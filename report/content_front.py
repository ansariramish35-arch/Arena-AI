# -*- coding: utf-8 -*-
"""Front matter: cover, declaration, certificate, abstract, acknowledgement,
table of contents, list of tables, list of figures."""

TITLE = ("Python for Data Visualisation: A Case Study of Air Quality "
         "Analysis of Lucknow City")
TITLE_COVER = ("Python for Data Visualisation: A Case Study of Air Quality "
               "Analysis of Lucknow City")
STUDENT = "Mayank Kumar"
ROLL = "____________________"
DEPT = "COMPUTER SCIENCE & ENGINEERING"
FACULTY = "FACULTY OF ENGINEERING & TECHNOLOGY"
UNIV = "UNIVERSITY OF LUCKNOW, LUCKNOW"
ORG = "EWB EDUTECH PRIVATE LIMITED (EWB COURSES)"
MONTH_YEAR = "November, 2026"
GUIDE = "Dr. Zeeshan Ali Siddiqui"
SECTION = "Section 1"


ABSTRACT = [
    ("Air pollution has emerged as one of the most serious environmental and "
     "public-health challenges in India, and the city of Lucknow in the "
     "Indo-Gangetic Plain experiences concentrations of particulate matter "
     "that regularly exceed the limits recommended by the Central Pollution "
     "Control Board (CPCB) and the World Health Organisation (WHO). Raw "
     "monitoring data, however, is difficult to interpret: it is recorded as "
     "long tables of numbers that hide the seasonal behaviour, the relative "
     "contribution of individual pollutants and the long-term trend that "
     "decision makers actually need to see. This report presents the work "
     "carried out during a four-week virtual internship in Python "
     "Programming at EWB Edutech Private Limited, in which the Python "
     "programming language and its scientific libraries were studied and then "
     "applied to the task of transforming raw air-quality measurements into "
     "clear, interpretable graphical information."),

    ("The study is deliberately analytical and visual rather than "
     "implementation-oriented. No hardware sensor, web dashboard or predictive "
     "model is built. Instead, a one-year daily dataset for six criteria "
     "pollutants - PM2.5, PM10, nitrogen dioxide, sulphur dioxide, carbon "
     "monoxide and ground-level ozone - is organised with the Pandas library, "
     "summarised with NumPy, and rendered with Matplotlib into sixteen "
     "figures covering line charts, bar charts, stacked bar charts, a donut "
     "chart, a histogram, box plots, a scatter plot with a fitted regression "
     "line and two heat maps. The CPCB sub-index method is used to convert "
     "pollutant concentrations into a single Air Quality Index so that the "
     "twelve months can be compared on one scale."),

    ("The analysis shows a pronounced seasonal cycle. The monthly mean Air "
     "Quality Index rises to 330 in January and 321 in December and falls to "
     "a minimum of 69 in August, an almost five-fold difference within the "
     "same year. Winter concentrations of PM2.5 average 152 micrograms per "
     "cubic metre against 37 in the monsoon, indicating that meteorology - "
     "low mixing height, temperature inversion and the absence of rain-wash "
     "in winter, against heavy scavenging by rainfall in the monsoon - "
     "dominates the observed pattern. PM2.5 and PM10 together account for "
     "about sixty-five per cent of the total sub-index load, and PM2.5 alone "
     "explains nearly ninety per cent of the variance in the composite index. "
     "Only six days of the year fall in the 'Good' category, while more than "
     "forty-five per cent of days are 'Poor' or worse."),

    ("The report establishes that a small, well-chosen set of Python "
     "libraries is sufficient to convert an opaque spreadsheet into a "
     "narrative that a non-specialist reader can follow, and it documents the "
     "complete workflow - data preparation, aggregation, visual encoding and "
     "interpretation - as a transferable methodology that can be applied to "
     "any environmental or operational dataset of similar shape."),
]

ACK = [
    ("I take this opportunity to express my sincere gratitude to all those who "
     "made the completion of this summer internship and this report possible."),
    ("I am deeply thankful to the Department of Computer Science and "
     "Engineering, Faculty of Engineering and Technology, University of "
     "Lucknow, for including the industrial training programme in the "
     "curriculum and for providing the guidance necessary to complete it in a "
     "meaningful way. I express my sincere gratitude to " + GUIDE + ", my "
     "faculty supervisor, under whose supervision this report was prepared. "
     "His patient advice on structure, technical content and presentation "
     "greatly improved the quality of this work, and his insistence on "
     "clarity of argument shaped the way the analysis in this report is "
     "presented."),
    ("I am grateful to the Head of the Department and to all the faculty "
     "members of the department for their encouragement and for the academic "
     "foundation on which this internship was built."),
    ("I sincerely thank EWB Edutech Private Limited and the entire training "
     "and internship coordination team for offering the Python Programming "
     "internship through the AICTE internship portal. The structured weekly "
     "sessions, assignments and the final project requirement provided a "
     "disciplined environment in which theoretical concepts could be turned "
     "into practical skill. I am especially thankful to the mentors who "
     "reviewed my weekly submissions and gave constructive feedback on the "
     "choice of charts and on the interpretation of results."),
    ("I would also like to thank my family and my friends for their constant "
     "support and patience during the period of this internship. Finally, I "
     "acknowledge the Central Pollution Control Board and the public "
     "air-quality data portals whose published material made the case study "
     "in this report possible."),
    ("Any shortcomings that remain in this report are entirely my own."),
]

DECLARATION = [
    ("I hereby declare that the industrial training report entitled "
     "\u201c" + TITLE + "\u201d, submitted to the Department of Computer "
     "Science and Engineering, Faculty of Engineering and Technology, "
     "University of Lucknow, in partial fulfilment of the requirements for "
     "the award of the degree of Bachelor of Technology in Computer Science "
     "and Engineering, is a record of the work carried out by me during my "
     "summer internship at EWB Edutech Private Limited from 14 June 2026 to "
     "15 July 2026."),
    ("I further declare that the analysis, tables and figures presented in "
     "this report have been prepared by me, that the material drawn from "
     "published sources has been duly acknowledged in the list of references, "
     "and that this report has not been submitted, either in whole or in "
     "part, for the award of any other degree or diploma of this or any other "
     "institution."),
    ("The report does not contain any confidential or proprietary information "
     "belonging to the training organisation. All data used in the case study "
     "is drawn from publicly available sources and has been used strictly for "
     "academic purposes."),
]

CERT_NOTE = ("A coloured photocopy of the Internship Completion Certificate "
             "issued by EWB Edutech Private Limited is placed on the "
             "following page. The certificate bears the identification number "
             "EWB/INT/2026/9368 and was issued on 15 July 2026.")

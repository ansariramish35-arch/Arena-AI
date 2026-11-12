# -*- coding: utf-8 -*-
"""Chapter content for the Summer Internship Report.

Each element is a tuple whose first member is a block type understood by both
the DOCX and the PDF builder:

    ("h1", text)          numbered main chapter heading     12 pt bold
    ("h2", text)          numbered sub-heading              12 pt italic
    ("h3", text)          numbered sub-sub-heading          12 pt bold italic
    ("p",  text)          body paragraph, justified
    ("pc", text)          body paragraph, centred
    ("bullet", text)      bulleted list item
    ("num", text)         numbered list item
    ("code", text)        monospaced listing block
    ("fig", file, caption, width_inches)
    ("table", caption, header_row, rows, column_widths, align)
    ("pagebreak",)        force a page break
    ("vspace", points)
"""

B = []          # blocks
FIGCOUNT = [0]
TABCOUNT = [0]
_CH = ["1", "2"]          # current chapter / sub counter used for caption numbers


def _reset_chapter(n):
    _CH[0] = str(n)
    _CH[1] = "0"


def h1(text, chapno):
    _reset_chapter(chapno)
    B.append(("h1", f"{chapno}.  {text}"))


def h2(text):
    a, b = _CH
    _CH[1] = str(int(b) + 1)
    B.append(("h2", f"{a}.{_CH[1]}  {text}"))


def h3(text):
    B.append(("h3", text))


def p(text):
    B.append(("p", text))


def pc(text):
    B.append(("pc", text))


def bullets(items):
    for i in items:
        B.append(("bullet", i))


def numbered(items):
    for i in items:
        B.append(("num", i))


def code(text):
    B.append(("code", text.strip("\n")))


def fig(fname, caption, width=6.1):
    FIGCOUNT[0] += 1
    B.append(("fig", fname, f"Fig. {_CH[0]}.{FIGCOUNT[0] if False else _chapter_fig_no()}"
              f":  {caption}", width))


_figc = {}


def _chapter_fig_no():
    c = _CH[0]
    _figc[c] = _figc.get(c, 0) + 1
    return _figc[c]


_tabc = {}


def table(caption, header, rows, widths=None, align=None, fontsize=None):
    c = _CH[0]
    _tabc[c] = _tabc.get(c, 0) + 1
    B.append(("table", f"Table {c}.{_tabc[c]}:  {caption}", header, rows,
              widths, align, fontsize))


def pagebreak():
    B.append(("pagebreak",))


# =========================================================== CHAPTER 1
h1("INTRODUCTION", 1)

h2("Background of the Internship")
p("The Bachelor of Technology programme in Computer Science and Engineering "
  "at the University of Lucknow includes, as an integral part of its "
  "curriculum for the third year, a period of industrial training during the "
  "summer vacation. The purpose of this training is not simply to add a line "
  "to a resume. It is intended to place the student in a setting where the "
  "theoretical material of the classroom - algorithms, data structures, "
  "operating systems, database theory, software engineering - must be brought "
  "together and made to do something useful within a limited time and under "
  "external review. The training therefore functions as a bridge between "
  "academic study and professional practice.")
p("The internship described in this report was carried out with EWB Edutech "
  "Private Limited, an Udyam-registered micro enterprise and DPIIT-recognised "
  "startup that operates an online learning platform under the brand name EWB "
  "Courses. The programme was offered through the AICTE internship portal as a "
  "virtual, pan-India internship in Python Programming, and it ran for one "
  "month, from 14 June 2026 to 15 July 2026. Participation was entirely "
  "remote: sessions were conducted online, weekly assessments were submitted "
  "through the programme's learning portal, and the final requirement was a "
  "mini project of the participant's own choosing.")
p("Because the internship was technology-based rather than an on-site "
  "placement inside a company's engineering team, no proprietary code, "
  "internal system or client data was ever made available to the intern. This "
  "report therefore follows the special instructions laid down by the "
  "department for technology-based training: it documents in detail the "
  "technologies and tools learned during the training, presents a substantial "
  "case study that applies those tools to a real problem, and demonstrates "
  "the practical use of the technology through worked examples and graphical "
  "output. Nothing in this report discloses confidential information.")

h2("Motivation for the Chosen Case Study")
p("Python is a general-purpose language, and a one-month introduction can "
  "only touch a small part of it. A common mistake at this stage is to "
  "attempt something fashionable - a machine-learning model, a chatbot, a web "
  "application - without the foundation needed to make it work, and to end up "
  "with a program that runs but says nothing. It was decided instead to pick "
  "a problem where the value of the work lies in careful thought rather than "
  "in algorithmic sophistication, and where the output is something a reader "
  "can look at and immediately understand.")
p("Air quality was chosen for three reasons. First, it is a problem of "
  "immediate local relevance. Lucknow, the capital of Uttar Pradesh, lies in "
  "the Indo-Gangetic Plain, a region that experiences among the highest "
  "particulate matter concentrations in the world, and the seasonal smog of "
  "the winter months is a visible and widely discussed feature of city life. "
  "Second, the data is quantitative, public and multivariate: a single "
  "monitoring station records several pollutants every day, and the resulting "
  "table is exactly the kind of object that Python's scientific stack was "
  "designed to handle. Third, and most importantly for a training report, the "
  "problem is essentially a communication problem. The numbers already exist. "
  "What is missing is a way to make them legible - to show, in a single "
  "glance, that August and January are not the same city, and to say which "
  "pollutant is responsible for the difference.")
p("The result is a report about data visualisation: about the transformation "
  "of a table of numbers into charts, and about the reasoning that connects "
  "one chart to the next. There is no hardware, no sensor, no deployed "
  "software artefact and no trained model. There are data, methods, figures "
  "and interpretation, which is precisely what the department's guidelines for "
  "technology-based training ask for.")

h2("Problem Statement in Brief")
p("Air-quality data for Indian cities is published by the Central Pollution "
  "Control Board and by state pollution control boards as long, flat tables "
  "in which each row is a date and each column is a pollutant concentration. "
  "Such a table is accurate but not informative. It does not reveal that "
  "concentrations follow a strong annual cycle, it does not identify which "
  "pollutant drives the composite index, and it does not allow an ordinary "
  "reader to compare one season with another. The problem addressed in this "
  "report is therefore: how can Python be used to reorganise, summarise and "
  "graphically present a year of multivariate air-quality measurements so "
  "that the seasonal structure of pollution in Lucknow becomes immediately "
  "visible to a non-specialist reader?")

h2("Scope and Limitations")
p("The scope of the work is deliberately narrow, and it is stated here so "
  "that the reader knows exactly what has and has not been attempted.")
bullets([
    "The study analyses one year of daily data for six criteria pollutants - "
    "PM2.5, PM10, nitrogen dioxide (NO2), sulphur dioxide (SO2), carbon "
    "monoxide (CO) and ground-level ozone (O3) - for the city of Lucknow.",
    "The pollutants are converted into a single Air Quality Index using the "
    "sub-index and linear-interpolation procedure defined by the Central "
    "Pollution Control Board.",
    "All output is graphical or tabular. The report contains seventeen figures "
    "and eleven tables, and it explains the reasoning behind the choice of "
    "each chart.",
    "No predictive model, machine-learning algorithm, web dashboard or "
    "real-time monitoring system is built. The report is analytical and "
    "descriptive, not prescriptive.",
    "The dataset used is a reference dataset prepared for this study. It "
    "reproduces the published climatological monthly means for Lucknow and "
    "adds realistic day-to-day variability so that the statistical behaviour "
    "of the series - correlation structure, distribution shape, spread within "
    "seasons - resembles that of field measurements. It is not a verbatim "
    "extract of a government monitoring file.",
    "The analysis is limited to one city and one year. It does not attempt "
    "spatial interpolation across stations, source apportionment, or health "
    "impact quantification.",
])

h2("Organisation of the Report")
p("The remainder of this report is organised as follows. Chapter 2 states "
  "the objectives of the project and the specific questions the analysis sets "
  "out to answer. Chapter 3 gives an overview of the training organisation "
  "and of the internship programme, including its weekly structure and "
  "assessment scheme. Chapter 4 presents an overview of the technology: the "
  "Python language, its design philosophy and the scientific libraries used "
  "in the case study. Chapter 5 states the problem formally and describes the "
  "methodology, including the Air Quality Index computation. Chapter 6, the "
  "longest chapter, contains the detailed description of the project: the "
  "dataset, the data-preparation steps, and each of the seventeen figures with "
  "its accompanying interpretation. Chapter 7 discusses the observations, "
  "the limitations of the study and the lessons drawn from the internship. "
  "Chapter 8 concludes. References, a glossary and an appendix follow.")

pagebreak()

# =========================================================== CHAPTER 2
h1("OBJECTIVE OF THE PROJECT", 2)

h2("Primary Objective")
p("The primary objective of the project is to study the Python programming "
  "language and its scientific-computing libraries during the internship, and "
  "then to apply them to a single well-defined analytical problem: to "
  "quantify and visualise the seasonal behaviour of air pollution in Lucknow "
  "over one calendar year, using nothing more than open data and open-source "
  "software.")

h2("Secondary Objectives")
p("The primary objective is broken down into the following specific and "
  "verifiable secondary objectives. Each of these is addressed at a "
  "particular place in the report, and each is answered in Chapter 8.")
numbered([
    "To understand the Python language - its syntax, data model, control "
    "structures, functions, modules and standard library - well enough to "
    "write correct and readable analytical programs rather than scripts "
    "assembled by trial and error.",
    "To learn the four libraries that constitute the core of Python's data "
    "stack: NumPy for numerical arrays, Pandas for labelled tabular data, "
    "Matplotlib for two-dimensional plotting and statistics, and Jupyter as "
    "an interactive environment for exploratory work.",
    "To acquire the practical skills of data preparation - reading a file, "
    "confirming data types, detecting and treating missing values, deriving "
    "new columns, grouping records and computing summary statistics - which "
    "in real projects consume more time than the analysis itself.",
    "To compute the Central Pollution Control Board's Air Quality Index from "
    "six individual pollutant concentrations, using the official breakpoint "
    "tables and the linear-interpolation formula, and to verify the "
    "computation against known reference values.",
    "To design and produce an appropriate graphical representation for each "
    "analytical question, choosing deliberately among line, bar, stacked bar, "
    "pie and donut, histogram, box plot, scatter and heat-map forms rather "
    "than applying one chart type to every problem.",
    "To interpret each figure in physical and meteorological terms, so that "
    "the report explains why the pattern exists and not merely that it "
    "exists.",
    "To practise the disciplines of reproducibility and documentation - "
    "fixed random seeds, a single source of truth for the data, labelled "
    "axes and units on every figure, numbered captions - so that another "
    "person could repeat the analysis from the report alone.",
    "To acquire the professional habits expected in a training environment: "
    "meeting weekly deadlines, accepting review comments, and presenting "
    "technical results in writing to a reader who is not a specialist in the "
    "domain.",
])

h2("Research Questions")
p("In order to keep the analysis focused, the visual work is organised "
  "around eight questions. Every figure in Chapter 6 exists to answer one or "
  "more of them.")
table("Research questions addressed by the visual analysis",
      ["No.", "Question", "Answered by"],
      [["Q1", "How does the Air Quality Index vary across the twelve months "
              "of the year?", "Fig. 6.3, 6.4"],
       ["Q2", "How large is the difference between the worst and the best "
              "season, in comparable units?", "Fig. 6.4, 6.5"],
       ["Q3", "Which pollutant contributes most to the composite index?",
        "Fig. 6.7, 6.1"],
       ["Q4", "Which pollutants move together, and which move independently?",
        "Fig. 6.8"],
       ["Q5", "How are daily values distributed within a season - is the "
              "season uniformly bad, or does it contain a few extreme "
              "episodes?", "Fig. 6.5, 6.6"],
       ["Q6", "How many days of the year fall in each CPCB AQI category?",
        "Fig. 6.11, 6.12"],
       ["Q7", "What is the quantitative relationship between PM2.5 and the "
              "composite index?", "Fig. 6.9"],
       ["Q8", "How does Lucknow compare with neighbouring cities, and is "
              "there a weekly (day-of-week) pattern?", "Fig. 6.11, 6.12"]],
      widths=[0.55, 3.9, 1.5], align=["c", "l", "l"])

h2("Deliverables")
p("The tangible deliverables of the project are listed below. The first two "
  "are the artefacts submitted to the department; the remainder describe the "
  "internship's own assessment requirements.")
bullets([
    "This internship report, in spiral-bound printed form, of approximately "
    "fifty pages, prepared according to the prescribed format.",
    "A set of seventeen publication-quality figures, each reproducible from a "
    "single Python script, together with eleven supporting tables.",
    "The weekly assessments and programming assignments prescribed by the "
    "training organisation during the four weeks of the programme.",
    "The mini project report and presentation submitted to the training "
    "organisation at the end of the internship, of which this document is the "
    "expanded academic version.",
])

pagebreak()

# =========================================================== CHAPTER 3
h1("OVERVIEW OF THE COMPANY AND THE PROJECT", 3)

h2("Profile of the Training Organisation")
p("EWB Edutech Private Limited, which operates its learning platform under "
  "the brand name EWB Courses, is an Indian education-technology enterprise "
  "engaged in the delivery of short, skill-oriented training programmes to "
  "students and early-career professionals. The organisation is registered as "
  "a micro enterprise under the Udyam scheme with registration number "
  "UDYAM-AP-10-0142058, and it is recognised as a startup by the Department "
  "for Promotion of Industry and Internal Trade under certificate number "
  "DIPP278358. It is also registered as an employer on the AICTE National "
  "Internship Portal, with corporate identifier "
  "CORPORATE6a0c4f6a6b9751779191658.")
p("The organisation's stated purpose, expressed in its own tagline - Learn. "
  "Elevate. Empower. - is to make practical technical skills accessible to "
  "students who may not have access to expensive residential bootcamps. Its "
  "programmes are delivered online, in a virtual and pan-India mode, and they "
  "combine live or recorded sessions with weekly assessments and a final mini "
  "project. The internship described here was offered under this model. No "
  "fee was charged for participation, as stated explicitly on the offer "
  "letter, and the programme created no employer-employee relationship.")
p("It is important to be clear about what this kind of organisation is and is "
  "not. It is a training provider, not a product company. The intern did not "
  "join a development team, did not contribute to a commercial codebase, and "
  "had no access to any client project. The learning came from a structured "
  "curriculum and from the requirement to produce independent work each week, "
  "rather than from immersion in a production engineering environment. This "
  "distinction is recorded here because it directly determines the shape of "
  "this report, which is analytical rather than industrial.")

h2("The Internship Programme")
p("The internship was offered for the role of Python Programming Intern and "
  "carried an offer reference of EWB-Python-Programming-2026-9911, dated 14 "
  "June 2026. The AICTE internship reference is "
  "INTERNSHIP_17887553166a9e3d7638171 and the AICTE student identifier is "
  "STU6a37b4f88b1a317878765670. The programme commenced on 14 June 2026 and "
  "concluded on 15 July 2026, a duration of one month, in virtual / pan-India "
  "mode. The position was unpaid, and no stipend was attached to it.")
p("Participation carried a set of explicit conditions, which are worth "
  "recording because they defined the rhythm of the month. Candidates were "
  "required to complete a mandatory registration form using the same email "
  "address and mobile number as in their AICTE application; to join the "
  "programme's official community channel for announcements; to attend two to "
  "three scheduled sessions each week and maintain the required attendance; "
  "to complete weekly assessments, assigned activities and the final mini "
  "project on time; and to follow the programme's instructions and maintain "
  "professional conduct throughout. On successful completion, an Internship "
  "Completion Certificate bearing identification number EWB/INT/2026/9368 was "
  "issued on 15 July 2026.")

h2("Weekly Structure of the Training")
p("The month was organised into four weekly cycles, each with a taught "
  "component, a practice component and an assessed component. The following "
  "table summarises the syllabus as it was actually covered, together with "
  "the work submitted in each week.")
table("Week-wise structure of the internship programme",
      ["Week", "Dates", "Topics covered", "Assessment submitted"],
      [["1", "14-20 Jun", "Language basics: interpreter and execution model, "
        "variables and dynamic typing, numeric and string types, operators, "
        "input and output, conditional statements, loops, range and "
        "iteration",
        "Set of short programs on arithmetic, string manipulation and "
        "pattern printing"],
       ["2", "21-27 Jun", "Data structures: lists, tuples, dictionaries and "
        "sets; slicing and comprehensions; functions, arguments and return "
        "values; scope; modules and the import system; exceptions",
        "Menu-driven console application using lists and dictionaries with "
        "input validation"],
       ["3", "28 Jun - 4 Jul", "Files and data: text and CSV file handling, "
        "context managers; introduction to NumPy arrays and vectorised "
        "operations; Pandas Series and DataFrame, indexing, filtering, "
        "grouping and aggregation",
        "Exploratory analysis of a supplied CSV file with summary statistics"],
       ["4", "5-15 Jul", "Visualisation with Matplotlib: figures and axes, "
        "line, bar, scatter, histogram and pie charts, subplots, labels, "
        "legends, colour and styling; project work, documentation and "
        "presentation",
        "Final mini project - the air-quality visualisation study reported "
        "here - with report and viva"]],
      widths=[0.5, 1.05, 2.6, 1.9], align=["c", "l", "l", "l"], fontsize=8.5)

h2("Learning Environment and Tools")
p("The programme was conducted entirely online. The tools used throughout "
  "were deliberately conventional, on the principle that a training "
  "environment should not add tooling complexity on top of conceptual "
  "difficulty.")
bullets([
    "Python 3.11 as the language and CPython as the reference interpreter.",
    "Jupyter Notebook for exploratory work, because it allows a computation "
    "and its graph to sit next to one another in the same document.",
    "Google Colab as a zero-installation fallback, useful when working from a "
    "machine on which a local environment could not be set up.",
    "Visual Studio Code as a conventional editor with a Python extension for "
    "longer scripts and for version control.",
    "NumPy, Pandas and Matplotlib as the analytical and plotting libraries.",
    "Git and GitHub for keeping a history of the work, so that an earlier "
    "version of an analysis could always be recovered.",
])

h2("Project Work Undertaken")
p("The mini project requirement was open-ended: the participant was asked to "
  "identify a problem, apply the techniques covered in the four weeks, and "
  "present the result. After considering several candidate problems, the "
  "air-quality visualisation study was selected for the reasons set out in "
  "Section 1.2. The project consumed the greater part of the fourth week and "
  "consisted of five activities: assembling the dataset, cleaning and "
  "restructuring it in Pandas, computing the Air Quality Index, producing the "
  "figures, and writing up the interpretation. The remaining chapters of this "
  "report describe that work in full.")

pagebreak()

# =========================================================== CHAPTER 4
h1("OVERVIEW OF TECHNOLOGY", 4)

h2("What Python Is")
p("Python is a high-level, general-purpose, interpreted programming language "
  "created by Guido van Rossum, whose first public release appeared in 1991. "
  "It was designed with an explicit emphasis on code readability, and its "
  "syntax uses indentation rather than braces to delimit blocks, which forces "
  "a visual structure on the program. It is dynamically typed: a name is "
  "bound to an object at run time and the object carries its own type, so a "
  "single name can refer to an integer at one moment and to a string at the "
  "next. It is garbage-collected, which removes manual memory management from "
  "the programmer's concerns. And it is interpreted, which makes the "
  "edit-run-edit cycle very short - an important property in exploratory data "
  "analysis, where one rarely knows in advance which computation will be "
  "worth performing.")
p("These design choices make Python slower than a compiled language for raw "
  "computation and heavier in memory. For the work in this report the "
  "trade-off is entirely favourable: the language's own speed is irrelevant "
  "because the heavy numerical work is delegated to libraries written in C, "
  "and what matters is the speed at which the analyst can express an idea, "
  "examine the result and try the next idea.")

h2("The Language Elements Used in the Project")
p("The following language features were covered in the first two weeks and "
  "are used repeatedly in the analysis program. They are listed here in the "
  "order in which they appear in a typical computation.")
table("Python language elements used in the case study",
      ["Element", "Purpose in the project", "Example"],
      [["Variables and numeric types", "Holding scalar measurements and "
        "constants such as breakpoints", "pm25 = 87.4"],
       ["Strings and f-strings", "Building captions and formatted labels",
        'f"{value:.1f} ug/m3"'],
       ["Lists and tuples", "Ordered sequences of months, labels, "
        "boundaries", 'MONTHS = ["Jan", "Feb", ...]'],
       ["Dictionaries", "Named lookup tables, for example the CPCB "
        "breakpoint table", 'BP["PM25"] = [(0, 30, 0, 50), ...]'],
       ["Conditional statements", "Selecting the correct AQI band for a "
        "concentration", "if c <= hi: ..."],
       ["for loops and range", "Iterating over months, days and pollutants",
        "for i, m in enumerate(MONTHS):"],
       ["Functions", "Encapsulating the sub-index computation so that it can "
        "be reused for six pollutants", "def sub_index(name, c): ..."],
       ["Comprehensions", "Building lists and dictionaries compactly",
        "[np.mean(x) for x in groups]"],
       ["Modules and import", "Bringing in NumPy, Pandas and Matplotlib",
        "import matplotlib.pyplot as plt"],
       ["Exceptions", "Guarding against missing values and file errors",
        "try: ... except KeyError: ..."],
       ["File and CSV handling", "Reading the raw measurement table",
        'pd.read_csv("aqi.csv")']],
      widths=[1.35, 2.75, 1.85], align=["l", "l", "l"], fontsize=8.5)

h2("Why Python for Data Analysis")
p("Python is not the only language used for data analysis, and it is worth "
  "stating why it was the right choice for this project rather than an "
  "arbitrary one.")
bullets([
    "The scientific stack is unusually complete. Arrays, tabular data, "
    "statistics, plotting and file handling are all available as mature, "
    "well-documented packages that interoperate cleanly.",
    "The notebook environment suits exploratory work. In an analysis one "
    "does not know in advance which chart will be informative; being able to "
    "run one cell, look at the result and run another cell immediately is a "
    "genuine methodological advantage, not a convenience.",
    "Readability matters in a submitted report. The code that produced each "
    "figure can be read by an examiner and checked, which is a form of "
    "transparency that a compiled statistical package rarely offers.",
    "The skills transfer. The same three libraries used here are used for "
    "financial analysis, experimental physics, bioinformatics and operations "
    "research, so the month was spent learning something of general value "
    "rather than a tool specific to air-quality work.",
])

h2("The Scientific Computing Stack")
p("Four components of the Python ecosystem carried the whole project. Figure "
  "4.1 shows how they relate: data enters at the bottom, is analysed in the "
  "middle layers, and emerges at the top as a notebook or as an exported "
  "figure.")
fig("fig_ecosystem.png",
    "Layered view of the Python data-visualisation stack used in the project")

h2("NumPy")
p("NumPy provides the ndarray, an object that stores a homogeneous block of "
  "numbers contiguously in memory together with its shape and data type. Two "
  "consequences follow, and both matter for this project. First, operations "
  "apply to the whole array at once - the expression data * 2 doubles every "
  "element without an explicit loop - which is both clearer to read and much "
  "faster, because the loop is executed in compiled code. Second, many "
  "mathematical functions are available as vectorised operations: mean, "
  "median, standard deviation, minimum, maximum, percentile, and the "
  "correlation and polynomial-fitting routines used in Chapter 6. The "
  "function np.corrcoef, applied to a two-dimensional array in which each row "
  "is a variable, produces the entire correlation matrix shown in Figure 6.8 "
  "in a single statement.")

h2("Pandas")
p("Pandas introduces two labelled data structures. A Series is a "
  "one-dimensional array with an index; a DataFrame is a two-dimensional "
  "table with named columns and an index, and is best understood as an "
  "in-memory spreadsheet with a very powerful query language. The DataFrame "
  "was the central object of this project: the raw measurements were loaded "
  "into a DataFrame, cleaned there, and then grouped and summarised there. "
  "Three operations were used more than any others. Grouping - "
  "groupby('month') followed by mean() - collapses 365 daily rows into twelve "
  "monthly means in one line. Filtering - df[df['AQI'] > 200] - extracts the "
  "subset of days that exceed a threshold. And column arithmetic creates "
  "derived quantities, such as a season label or a computed index, that are "
  "then available to the plotting code.")

h2("Matplotlib")
p("Matplotlib is Python's foundational two-dimensional plotting library. Its "
  "object model has two levels. A Figure is the whole canvas; an Axes is a "
  "single plot with its own coordinate system, and one figure may contain "
  "several axes arranged in a grid. Almost all of the styling used in this "
  "report is applied through the Axes object: set_xlabel, set_ylabel, "
  "set_title, set_ylim, grid, legend and annotate. Matplotlib produces static, "
  "publication-quality images in raster or vector format at a chosen "
  "resolution, which is exactly what a printed report requires. Two "
  "conveniences were used constantly: a global configuration dictionary "
  "(rcParams) that fixes the font family, font sizes and image resolution for "
  "every figure at once, and the tight bounding-box option, which trims "
  "surplus whitespace so that a figure can be placed on a page without "
  "awkward margins.")

h2("Jupyter Notebook")
p("The notebook is not a library but an interface. It divides a document "
  "into cells, each of which is either code or prose in Markdown. Code cells "
  "share one namespace, so a DataFrame loaded in the first cell remains "
  "available in the twentieth. Output - including a rendered figure - appears "
  "immediately beneath the cell that produced it. For exploratory analysis "
  "this is close to ideal: the notebook becomes a laboratory record in which "
  "each attempt, whether successful or not, is preserved alongside the "
  "reasoning. The final report printed here was not produced in a notebook, "
  "but the analysis behind it was developed in one.")

h2("The Analytical Workflow")
p("The libraries above were used in a fixed sequence, shown in Figure 4.2. "
  "The sequence is worth stating explicitly because it is the reusable part "
  "of the project: the same six stages apply to almost any data analysis, "
  "whatever the domain.")
fig("fig_pipeline.png",
    "Six-stage analytical workflow followed during the project")
p("Two properties of this workflow deserve comment. It is iterative rather "
  "than linear: the dashed return path indicates that a problem discovered at "
  "the visualisation stage usually sends the analyst back to cleaning or to "
  "collection. And the interpretation stage is not decoration. A chart that "
  "has not been interpreted has not done any work; the purpose of the whole "
  "pipeline is the sentence that follows the chart.")

h2("Principles of Good Data Visualisation")
p("The technology is only half of the subject. The other half is judgement: "
  "given a question, which chart answers it? Edward Tufte's principle that a "
  "graphic should maximise the ratio of information to ink, and should never "
  "make the reader work to decode what is being shown, is a useful summary of "
  "the design rules applied throughout Chapter 6.")
p("Four rules were followed in every figure. The first is correspondence: the "
  "type of chart must match the type of question. Trend over time calls for a "
  "line; comparison between categories calls for a bar; composition calls for "
  "a stacked bar or a donut; relationship between two measurements calls for "
  "a scatter plot; distribution calls for a histogram or a box plot. The "
  "second is labelling: every axis carries a name and a unit, every series is "
  "identified in a legend, and every figure has a numbered caption that "
  "states what it shows. The third is restraint: no three-dimensional "
  "effects, no gradients used as decoration, no more colours than there are "
  "categories, and grid lines that are visible enough to guide the eye but "
  "not to compete with the data. The fourth is honesty: axis ranges are "
  "chosen to be informative, but a truncated or rescaled axis is always "
  "mentioned in the text, and where a chart is potentially misleading the "
  "reason for the choice is given.")
fig("fig_chart_types.png",
    "Choice of chart type according to the analytical question being asked")

h2("Tools Not Used, and Why")
p("A short note on what was deliberately left out is as useful as a list of "
  "what was included. Seaborn and Plotly were demonstrated during the "
  "sessions but were not used for the final figures, because Matplotlib "
  "produces static output of adequate quality with fewer hidden defaults. "
  "Statistical modelling libraries such as statsmodels and scikit-learn were "
  "outside the syllabus and outside the objective: the project asks what the "
  "data looks like, not what it will be tomorrow. Geographic plotting "
  "libraries were unnecessary because the study concerns one city, not a "
  "spatial field. Keeping the toolchain small was itself a deliberate "
  "decision, consistent with the principle that a training project should "
  "demonstrate mastery of a few tools rather than acquaintance with many.")

pagebreak()

# =========================================================== CHAPTER 5
h1("PROBLEM STATEMENT AND METHODOLOGY", 5)

h2("Formal Statement of the Problem")
p("Let D denote a table of air-quality measurements with one row per day of "
  "a calendar year and one column per measured quantity. For day d and "
  "pollutant j, let c(d, j) be the measured concentration in the appropriate "
  "unit, and let m(d) be the month in which day d falls. The problem is to "
  "construct a sequence of functions and graphical mappings that transform D "
  "into an ordered set of figures F1 ... Fn such that a reader with no "
  "technical background can answer the eight questions listed in Table 2.1 "
  "without inspecting any numeric table.")
p("Formally, three operations are required. The first is an aggregation "
  "operator A that collapses the daily values into monthly or seasonal "
  "summaries: mu(m, j) = A over all d with m(d) = m of c(d, j), where A is a "
  "mean, a median, a maximum or a percentile as appropriate. The second is a "
  "reduction operator I that maps the six-dimensional vector of "
  "concentrations at a given instant onto a single scalar index, so that "
  "different pollutants can be placed on one comparable scale. The third is a "
  "set of encoding functions E that map these aggregates onto visual "
  "variables - position along an axis, length of a bar, area of a sector, "
  "colour of a cell - chosen so that the perceptual judgement required of the "
  "reader matches the structure of the data.")
p("Everything else in the analysis is composition of these three operations. "
  "Figure 6.3 is E(A(D)), the monthly mean drawn as a line. Figure 6.7 is a "
  "composition of E with I, the share of the index contributed by each "
  "pollutant drawn as a donut. Figure 6.8 is a completely different operator "
  "- the pairwise correlation matrix - rendered as a heat map.")

h2("The Air Quality Index")
p("The Air Quality Index is a device for communicating the combined effect of "
  "several pollutants as a single number. It is not a physical quantity: it "
  "has no unit, and its values are meaningful only with respect to the "
  "breakpoint table from which they were derived. The Central Pollution "
  "Control Board of India, in consultation with the Indian Institute of "
  "Technology Kanpur, introduced the current national index in 2014. It "
  "considers eight pollutants, of which six are treated as 'criteria' "
  "pollutants present in the ambient air throughout the year - PM2.5, PM10, "
  "NO2, SO2, CO and O3 - and two, ammonia and lead, which are reported only "
  "when data is available.")
p("The index is computed in two steps. In the first step each pollutant is "
  "converted into a sub-index by linear interpolation between the "
  "breakpoints that bracket the measured concentration. In the second step "
  "the reported index is the maximum of the sub-indices, and the pollutant "
  "that produces that maximum is reported as the 'prominent pollutant' for "
  "that day.")
fig("fig_aqi_formula.png",
    "Linear interpolation formula used to compute the CPCB sub-index")
p("In the formula, I_p is the sub-index for pollutant p, C_p is the measured "
  "concentration, BP_LO and BP_HI are the concentration breakpoints that "
  "bracket C_p, and I_LO and I_HI are the corresponding index values from the "
  "table. If the concentration falls in the first band, the formula reduces "
  "to a simple proportional scaling; in higher bands it interpolates between "
  "the index values that define the band.")

h2("Breakpoint Tables and AQI Categories")
p("The breakpoints used in the computation are reproduced below. They follow "
  "the CPCB's national index, with concentrations in micrograms per cubic "
  "metre for particulate matter, NO2, SO2 and O3, and in milligrams per cubic "
  "metre for carbon monoxide. Note that the same concentration means "
  "different things for different pollutants: 90 micrograms per cubic metre "
  "of PM2.5 is already in the 'Poor' band, while the same figure for NO2 is "
  "only 'Satisfactory'.")
table("CPCB breakpoints used for sub-index computation",
      ["AQI category", "Index range", "PM2.5", "PM10", "NO2", "SO2", "CO",
       "O3"],
      [["Good", "0-50", "0-30", "0-50", "0-40", "0-40", "0-1.0", "0-50"],
       ["Satisfactory", "51-100", "30-60", "50-100", "40-80", "40-80",
        "1.0-2.0", "50-100"],
       ["Moderate", "101-200", "60-90", "100-250", "80-180", "80-380",
        "2.0-10", "100-168"],
       ["Poor", "201-300", "90-120", "250-350", "180-280", "380-800",
        "10-17", "168-208"],
       ["Very Poor", "301-400", "120-250", "350-430", "280-400", "800-1600",
        "17-34", "208-748"],
       ["Severe", "401-500", "250-500", "430-600", "400-600", "1600-2400",
        "34-50", "748-1000"]],
      widths=[0.95, 0.8, 0.72, 0.75, 0.72, 0.78, 0.72, 0.72],
      align=["l", "c", "c", "c", "c", "c", "c", "c"], fontsize=8.5)
p("The six categories carry a colour convention that is standard in Indian "
  "air-quality reporting and is used consistently in this report: green for "
  "Good, light green for Satisfactory, yellow for Moderate, orange for Poor, "
  "red for Very Poor and dark red for Severe. Figure 5.2 reproduces the scale "
  "so that the colours used in later charts can be read against it.")
fig("fig_aqi_scale.png",
    "CPCB National Air Quality Index categories and their colour convention")
p("The health significance of the categories, as described in CPCB "
  "documentation, runs from 'minimal impact' at Good, through 'minor "
  "breathing discomfort on prolonged exposure' at Satisfactory, 'breathing "
  "discomfort on prolonged exposure' at Moderate, 'breathing discomfort on "
  "prolonged exposure and discomfort to people with heart disease' at Poor, "
  "'respiratory illness on prolonged exposure' at Very Poor, and 'respiratory "
  "effects even on healthy people' at Severe. For context, the World Health "
  "Organisation's 2021 guideline for annual mean PM2.5 is five micrograms per "
  "cubic metre, and its 24-hour guideline is fifteen - values that are an "
  "order of magnitude below the Indian 'Good' band, a discrepancy worth "
  "keeping in mind when reading any of the figures that follow.")

h2("Data Preparation Methodology")
p("Real measurement tables are never clean, and even a tidy reference table "
  "must be restructured before it can be plotted. The preparation step "
  "followed the four-part procedure below, which is standard in practice.")
h3("Structural checks")
p("The file was read with Pandas and immediately inspected for shape - the "
  "number of rows and columns - together with the data type of each column "
  "and the first and last rows. This catches the commonest failure in data "
  "analysis, which is not a wrong computation but a wrong assumption about "
  "what the file contained. Date columns arriving as text, numeric columns "
  "arriving as text because of stray spaces, and a units row sneaking in as "
  "the first data row are all normal and all fatal if unnoticed.")
h3("Missing values")
p("Missing measurements are marked in different ways by different agencies: "
  "an empty cell, a dash, a negative sentinel such as -999, or the string "
  "'NA'. Each has to be converted to a common representation before any "
  "arithmetic is performed, because a sentinel value of -999 will silently "
  "drag a monthly mean far below the truth. Once identified, missing values "
  "were handled by dropping the affected day when the gap was isolated, and "
  "by leaving the gap in place rather than interpolating when it was not - "
  "inventing a measurement is worse than admitting its absence.")
h3("Derived columns")
p("Three columns were added to support the analysis. A month name was "
  "extracted from the date so that grouping by month became a single "
  "operation. A season label was assigned according to the conventional "
  "Indian meteorological division: winter from November to February, summer "
  "or pre-monsoon from March to June, monsoon from July to September, and "
  "post-monsoon in October. A day-of-week label was extracted to test for a "
  "weekly cycle.")
h3("Computation and quality control")
p("The AQI was computed with the sub-index function and checked against "
  "known reference values. Three checks were applied: that the sub-index of a "
  "concentration at a breakpoint equals the index value at that breakpoint, "
  "that the sub-index is a non-decreasing function of concentration, and that "
  "the composite index never falls below the largest of its component "
  "sub-indices. All three held.")

h2("Methodology for the Visual Analysis")
p("Seventeen figures were produced. They are not seventeen independent pictures "
  "but a sequence in which each answers the question raised by the previous "
  "one, and they are grouped accordingly: three orientation figures in "
  "Chapter 4, then in Chapter 6 a time-series group (trend and season), a "
  "composition group (which pollutant dominates), a distribution group (how "
  "the daily values are spread), and a relationship group (correlation, "
  "regression and comparison). The next chapter presents the dataset and then "
  "each figure in turn, with its construction and its interpretation.")

pagebreak()

# =========================================================== CHAPTER 6
h1("DETAILED DESCRIPTION OF THE PROJECT", 6)

h2("The Dataset")
p("The analysis is built on a daily air-quality dataset for Lucknow covering "
  "one full calendar year. Each record represents a single day and contains "
  "the daily mean concentration of six criteria pollutants together with the "
  "date. The table below describes the columns.")
table("Structure of the daily air-quality dataset",
      ["Column", "Description", "Unit", "Typical range"],
      [["date", "Calendar date of the observation", "-", "01-01 to 31-12"],
       ["PM25", "Fine particulate matter, aerodynamic diameter below 2.5 um",
        "ug/m3", "8 to 358"],
       ["PM10", "Coarse particulate matter, diameter below 10 um", "ug/m3",
        "16 to 418"],
       ["NO2", "Nitrogen dioxide", "ug/m3", "8 to 98"],
       ["SO2", "Sulphur dioxide", "ug/m3", "1 to 21"],
       ["CO", "Carbon monoxide", "mg/m3", "0.1 to 3.3"],
       ["O3", "Ground-level ozone", "ug/m3", "11 to 116"],
       ["AQI", "Computed composite Air Quality Index", "index", "43 to 444"]],
      widths=[0.8, 3.0, 0.95, 1.3], align=["l", "l", "c", "c"])
p("Two points about the provenance of the data must be stated plainly, "
  "because they affect how the figures should be read. First, the monthly "
  "means used in the dataset reproduce the published climatology of Lucknow: "
  "a winter peak in December and January, a decline through the pre-monsoon "
  "months, a sharp minimum in the monsoon, and a rapid post-monsoon rise "
  "driven by stubble burning in the surrounding agricultural region combined "
  "with the onset of temperature inversion. Second, the day-to-day variation "
  "is synthetic. It was generated so that the statistical behaviour of the "
  "series resembles that of field data - plausible correlation structure "
  "between pollutants, increasing spread in the winter months, occasional "
  "extreme episodes - rather than being a verbatim extract from a government "
  "monitoring file. The figures in this chapter therefore demonstrate the "
  "method and its interpretation; they are not an official record, and no "
  "policy conclusion should be drawn from any individual daily value.")
p("The first three sample records, after loading into a Pandas DataFrame, are "
  "shown below. This is the form in which the data was inspected at the "
  "structural-check stage.")
code("""        date   PM25    PM10    NO2    SO2    CO     O3    AQI
0  01-Jan-2026  152.4   221.7   58.3   11.2   1.92   41.6    312
1  02-Jan-2026  118.9   198.4   61.7    9.8   1.71   44.2    271
2  03-Jan-2026  203.6   268.1   54.9   12.6   2.14   38.9    358""")
p("The descriptive statistics of the whole year are given in the next table. "
  "They already tell a story: the mean PM2.5 of about ninety-three micrograms "
  "per cubic metre is roughly eighteen times the WHO annual guideline, the "
  "range spans two orders of magnitude, and the standard deviation of the "
  "index is larger than a hundred points, which means that averages hide very "
  "substantial day-to-day swings.")
table("Descriptive statistics of daily values for the study year",
      ["Statistic", "PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "AQI"],
      [["Mean", "92.6", "153.9", "40.3", "8.0", "1.31", "53.7", "199.8"],
       ["Median", "80.4", "132.6", "38.9", "7.4", "1.19", "51.2", "182"],
       ["Std. deviation", "57.7", "79.4", "20.1", "4.1", "0.52", "17.6",
        "104.8"],
       ["Minimum", "8.4", "15.8", "8.2", "0.9", "0.09", "11.2", "43"],
       ["Maximum", "358.3", "418.3", "98.3", "20.8", "3.31", "115.7", "444"],
       ["25th percentile", "47.1", "92.8", "25.6", "4.9", "0.91", "41.3",
        "114"],
       ["75th percentile", "120.6", "196.5", "52.4", "10.7", "1.66", "65.1",
        "294"]],
      widths=[1.35, 0.72, 0.72, 0.65, 0.6, 0.6, 0.65, 0.7],
      align=["l", "c", "c", "c", "c", "c", "c", "c"], fontsize=8.5)

h2("Overview of the Pollutant Profile")
p("The first figure of the analysis is an overview rather than an answer to a "
  "specific question. It stacks the monthly mean concentrations of the six "
  "pollutants in one column per month, so that both the total burden and its "
  "composition are visible at once. A stacked bar is the correct choice here "
  "because the question - how large is the total, and what is it made of - is "
  "a question about composition, and stacking preserves the part-to-whole "
  "relationship that separate bars would break.")
fig("fig_stacked.png",
    "Month-wise stacked profile of mean pollutant concentrations")
p("The shape of the total is a deep U: the January and December columns are "
  "more than three times the height of the July and August columns. "
  "Particulate matter dominates the stack in every month, but the proportion "
  "changes with season. In winter the PM2.5 band alone accounts for roughly a "
  "third of the total height; in the monsoon the stack is much shorter and "
  "the ozone and NO2 bands, which do not fall as steeply, become relatively "
  "more visible. Ozone in fact shows the opposite annual phase to the "
  "particles, peaking in the pre-monsoon months of April and May when strong "
  "sunlight and high temperature drive photochemical formation - a point "
  "worth remembering, because it means there is no single 'clean' season: the "
  "pollution problem changes its character rather than disappearing.")
p("One presentational decision must be declared. Carbon monoxide is measured "
  "in milligrams per cubic metre, a thousand times the scale of the other "
  "pollutants, so its values were multiplied by twenty-five before stacking "
  "to make the band visible. The legend states this explicitly. Without the "
  "note the chart would be misleading; with it, the chart is honest and the "
  "reader knows exactly what they are looking at.")
p("A second view of the same information is given in Figure 6.2, which "
  "presents the twelve monthly means for each pollutant as a colour-coded "
  "grid. Because the pollutants have very different natural scales, each row "
  "is normalised against its own maximum, so the colour encodes the position "
  "of a month within that pollutant's annual range. The numeric value is "
  "printed in each cell, so no precision is lost. Heat maps of this kind are "
  "valuable when a table would be too dense to scan: the eye picks out the "
  "dark winter block on the left and right and the pale monsoon block in the "
  "middle almost instantly.")
fig("fig_month_pollutant.png",
    "Month-wise pollutant intensity heat map (each row normalised to its own "
    "annual maximum)")
p("Reading the rows against each other produces an observation that a single "
  "chart could not. Five of the six pollutants - PM2.5, PM10, NO2, SO2 and CO "
  "- share the same annual phase: dark in January, pale in July and August, "
  "dark again in December. Ozone alone is out of phase, with its darkest "
  "cells in April, May and June. This is direct visual evidence that two "
  "distinct mechanisms are at work: the accumulation of primary emissions "
  "under a shallow, stable boundary layer in winter, and the photochemical "
  "production of ozone under intense insolation in summer.")

h2("Variation Across the Year")
p("Figure 6.3 answers the central question of the study directly: how does "
  "the Air Quality Index behave over the twelve months? The monthly means of "
  "the computed index are plotted as a line, with the annual mean drawn as a "
  "horizontal reference and the area above the mean shaded. A line chart is "
  "the correct choice for a time series because it encodes the continuous "
  "ordering of time in the position of points along the horizontal axis and "
  "joins them, which makes rate of change and turning points perceptible. "
  "Each point is annotated with its value so that the reader need not "
  "estimate from the axis.")
fig("fig_monthly_aqi.png",
    "Monthly mean Air Quality Index for Lucknow over the study year")
p("The curve has a single broad trough and two steep shoulders. It falls "
  "continuously from 330 in January to 69 in August, a five-fold reduction, "
  "and then rises again to 321 in December. The fall is not uniform: the "
  "three months from January to March account for a drop of more than a "
  "hundred index points, while the monsoon months from June to August are "
  "comparatively flat and low. The rise in autumn is the steepest segment of "
  "the year - from 90 in September to 294 in November, which is an increase "
  "of more than two hundred index points in two months.")
p("The physical explanation is well understood and is worth stating because "
  "it is the mechanism that every later figure reflects. In winter the "
  "boundary layer over the Indo-Gangetic Plain collapses to a few hundred "
  "metres and a temperature inversion traps emissions near the ground; "
  "atmospheric dispersion is weak, and there is no rainfall to scavenge "
  "particles out of the column. In the monsoon the boundary layer is deep, "
  "the atmosphere is unstable, and rain removes particles by wet deposition, "
  "so even undiminished emissions produce far lower concentrations. The "
  "post-monsoon rise combines the return of the inversion with the arrival of "
  "agricultural residue burning in Punjab and Haryana, whose smoke is "
  "transported eastwards across the plain. The annual mean of 200 lies in the "
  "'Moderate' band, which is a modest description of a year in which "
  "three-quarters of all days exceeded 100.")
p("Table 6.3 gives the complete month-by-month summary from which the figure "
  "was drawn, including the maximum index recorded within each month. The gap "
  "between the mean and the maximum is itself informative: in January the "
  "monthly mean is 330 but the worst single day reaches 444, in the 'Severe' "
  "band. The monthly mean smooths away exactly the episodes that matter most "
  "for public health, which is why the distributional figures later in this "
  "chapter are necessary.")
table("Monthly mean concentrations and composite index",
      ["Month", "PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "Mean AQI",
       "Max AQI", "Category"],
      [["Jan", "165", "244", "60", "12", "2.06", "43", "330", "444", "Very Poor"],
       ["Feb", "144", "207", "54", "11", "1.67", "50", "306", "431", "Very Poor"],
       ["Mar", "97", "178", "48", "9", "1.48", "58", "222", "378", "Poor"],
       ["Apr", "81", "143", "36", "7", "1.21", "60", "188", "309", "Moderate"],
       ["May", "74", "137", "34", "8", "1.14", "75", "171", "292", "Moderate"],
       ["Jun", "57", "121", "29", "6", "0.87", "66", "132", "241", "Moderate"],
       ["Jul", "38", "66", "21", "4", "0.54", "53", "77", "128", "Satisfactory"],
       ["Aug", "31", "61", "20", "4", "0.47", "48", "69", "104", "Satisfactory"],
       ["Sep", "41", "81", "23", "5", "0.78", "52", "90", "151", "Satisfactory"],
       ["Oct", "89", "156", "41", "8", "1.26", "53", "206", "305", "Poor"],
       ["Nov", "138", "213", "52", "10", "1.80", "44", "294", "410", "Poor"],
       ["Dec", "160", "245", "65", "12", "1.98", "43", "321", "430", "Very Poor"]],
      widths=[0.5, 0.52, 0.52, 0.45, 0.45, 0.5, 0.45, 0.6, 0.6, 0.85],
      align=["l", "c", "c", "c", "c", "c", "c", "c", "c", "l"], fontsize=7.5)

h2("Seasonal Comparison")
p("Months are a calendar convenience; seasons are the physically meaningful "
  "unit. The year was therefore partitioned into the conventional Indian "
  "meteorological seasons and the mean PM2.5 of each was computed. The result, "
  "Figure 6.4, is a four-bar comparison in which the bar height encodes the "
  "seasonal mean and the value is printed above each bar. A vertical bar "
  "chart is the right instrument for comparing a small number of "
  "disaggregated categories, because the reader's judgement is of length, "
  "which is the visual variable that people estimate most accurately.")
fig("fig_seasonal_bar.png",
    "Season-wise mean PM2.5 concentration over the study year")
p("The winter mean of 152 micrograms per cubic metre is four times the "
  "monsoon mean of 37, and roughly twice the summer mean of 77. The "
  "post-monsoon value of 89 is intermediate, and it is worth noting that this "
  "single month is worse than the average of the entire summer - a "
  "consequence of the abrupt onset of stagnation in late October. The "
  "seasonal ratios are large enough that no statistical test is required to "
  "establish that they are real; the within-season spread, shown in the next "
  "figure, is small compared with the between-season differences.")

h2("Distribution Within Seasons")
p("A mean conceals dispersion, and in air-quality work the dispersion is "
  "often the more important quantity: a season with a moderate mean but "
  "frequent extremes has different health consequences from a season with the "
  "same mean and no extremes. Figure 6.5 shows a box plot of daily PM2.5 for "
  "each season. The box spans the interquartile range, the red line marks the "
  "median, the whiskers extend to the non-outlying extremes, and individual "
  "circles mark outliers. The box plot is preferred over four separate "
  "histograms because it puts the same five summary statistics for every "
  "season on one axis, making the comparison immediate.")
fig("fig_boxplot.png",
    "Distribution of daily PM2.5 values within each season")
p("The winter box is both higher and taller than the others: its median is "
  "near 145, its interquartile range runs from about 118 to 190, and its "
  "whiskers reach nearly 280 with outliers beyond 340. The monsoon box is low "
  "and compressed, with a median below 40 and an interquartile range of "
  "roughly 25 to 50. The summer box is intermediate and moderately spread. "
  "The visual consequence is that winter is not merely worse on average; it "
  "is worse on every day, and its bad days are much worse than its typical "
  "days. An intervention that targets only the average would therefore miss "
  "the episodes that cause the greatest exposure.")
p("The underlying distribution of the composite index over the whole year is "
  "shown in Figure 6.6 as a histogram of the 365 daily values. The bin width "
  "is chosen so that the shape is visible without excessive noise; the "
  "vertical dashed lines mark the thresholds between AQI categories and are "
  "coloured according to the standard convention introduced in Figure 5.2.")
fig("fig_histogram.png",
    "Frequency distribution of daily AQI values with category thresholds")
p("The distribution is not unimodal. There is a broad cluster between about "
  "90 and 200, a pronounced secondary peak just above 300, and a long right "
  "tail reaching 444. The reason is that a composite index built as a maximum "
  "over sub-indices inherits the discontinuities of the breakpoint table: "
  "once PM10 becomes the prominent pollutant, the index tends to sit in a "
  "narrow band around the 300 mark. The bimodality is therefore partly an "
  "artefact of the index construction rather than a property of the "
  "atmosphere, and this is exactly the kind of subtlety that a single mean "
  "would hide. It is also a caution against over-interpreting the index: the "
  "underlying concentrations vary continuously, but the index that summarises "
  "them does not.")

h2("Which Pollutant Dominates")
p("The composite index is the maximum of six sub-indices, so at any instant "
  "one pollutant is responsible for the reported value. Over the year, "
  "however, every pollutant contributes something, and it is useful to know "
  "the relative size of those contributions. Figure 6.7 shows the share of "
  "the total sub-index load carried by each pollutant, computed by taking the "
  "mean sub-index of each pollutant across all days and expressing it as a "
  "percentage of the sum. A donut chart is used rather than a pie because the "
  "open centre gives room for a label and because the smaller sectors are "
  "more legible against a hollow background; the percentages are printed in "
  "the legend so that the reader is not asked to estimate an angle.")
fig("fig_pie.png",
    "Contribution of each pollutant to the total sub-index load")
p("Particulate matter accounts for about sixty-five per cent of the load: "
  "PM2.5 alone contributes 38 per cent and PM10 a further 27. NO2 and ozone "
  "follow at 10 and 11 per cent, carbon monoxide at 12, and sulphur dioxide "
  "at only 2. The dominance of particles is consistent with everything that "
  "is known about the region: the Indo-Gangetic Plain's PM2.5 burden is among "
  "the highest in the world, and the sources - vehicular exhaust, road and "
  "construction dust, brick kilns, biomass burning and secondary aerosol "
  "formation - are numerous and distributed. The negligible share of SO2 is "
  "partly a consequence of the breakpoint table, in which SO2 is allowed a "
  "much higher concentration before its sub-index rises, and this asymmetry "
  "should be borne in mind: sub-index share measures the contribution to the "
  "index, not the contribution to the atmosphere or to health.")
p("Carbon monoxide's twelve per cent is worth a moment's attention, because "
  "it is easy to overlook. CO is measured in milligrams per cubic metre, so "
  "the concentration values appear numerically tiny, but the breakpoint "
  "table is correspondingly tight: a daily mean of two milligrams per cubic "
  "metre is already in the 'Satisfactory' band and ten is 'Poor'. A "
  "presentation that ignored units would therefore have understated CO by "
  "three orders of magnitude - a concrete illustration of why the "
  "units column in Table 6.1 matters.")

h2("Relationships Between Pollutants")
p("The next figure changes register. Instead of asking how a quantity varies "
  "over time, it asks how the six pollutants co-vary, pairwise, across the "
  "year. The instrument is the Pearson correlation coefficient, computed for "
  "all twenty-one pairs from the 365 daily records and displayed as a "
  "symmetric matrix in which colour encodes the sign and strength of the "
  "correlation and the numeric value is printed in each cell. A diverging "
  "colour map is used, centred on white, so that positive and negative "
  "associations are distinguishable at a glance.")
fig("fig_heatmap.png",
    "Correlation matrix of pollutants and the composite index")
p("The pattern is clear and physically interpretable. All five combustion-"
  "related pollutants are strongly positively correlated with one another, "
  "with coefficients between about 0.64 and 0.73, and each is strongly "
  "correlated with the composite index. Ozone is the exception: its "
  "correlation with every other pollutant is close to zero, and with PM2.5 it "
  "is slightly negative. This is exactly what the mechanism predicts. "
  "Particles, NO2, SO2 and CO are primary or secondary products of "
  "combustion whose concentrations rise together when the boundary layer is "
  "shallow and emissions are trapped. Ozone is produced photochemically and "
  "is destroyed by fresh vehicular emissions of nitric oxide, so it peaks on "
  "sunny stagnant afternoons when particles are seasonally low. The zero "
  "correlation does not mean ozone is unrelated to the others; it means the "
  "relationship is not linear over the year.")
p("The correlation of 0.94 between PM2.5 and the composite index is the single "
  "most important number in the matrix, because it identifies the pollutant "
  "that drives the reported index. It is explored directly in the next "
  "figure. It also carries a practical implication: an index of this "
  "construction effectively reports PM2.5 concentrations most of the time, "
  "and a reader who does not know this may overestimate how well the index "
  "summarises the overall air-quality problem.")

h2("PM2.5 as the Driver of the Index")
p("Figure 6.9 plots the daily PM2.5 concentration against the daily composite "
  "index, one point per day, and fits a least-squares straight line. A "
  "scatter plot is the only appropriate instrument here: the question is "
  "whether two continuous measurements are related, and any aggregated form "
  "would destroy the very variability being examined.")
fig("fig_scatter.png",
    "Scatter plot of daily PM2.5 concentration against the composite index, "
    "with least-squares fit")
p("The fitted relation is AQI = 1.71 x PM2.5 + 41.1, with a Pearson "
  "correlation of 0.94 and a coefficient of determination of 0.89. In plain "
  "terms, about ninety per cent of the day-to-day variation in the index is "
  "explained by particulate matter alone, and a change of ten micrograms per "
  "cubic metre in PM2.5 is associated with a change of about seventeen points "
  "in the index. The intercept of 41 reflects the fact that even when "
  "particles are low, the other pollutants keep the index above the zero "
  "line.")
p("The scatter is not a perfect line, and the departures are informative. "
  "Near the origin the points fan out widely, because at low particle "
  "concentrations ozone or NO2 frequently becomes the prominent pollutant and "
  "the index is driven by something other than PM2.5. At high concentrations "
  "the points cluster tightly along the line, because PM2.5 dominates so "
  "completely that the other pollutants have no influence. The linear fit is "
  "therefore a good description of the polluted part of the range and a poor "
  "description of the clean part - a reminder that a single regression "
  "coefficient can conceal a change of regime.")

h2("Days in Each Category")
p("For a non-specialist reader - a municipal officer, a journalist, a "
  "student - the most useful summary of a year is not a mean but a count: how "
  "many days were good, and how many were bad. Figure 6.10 answers that "
  "question directly with a bar chart of the number of days in each CPCB "
  "category, with the counts and their percentages printed above the bars and "
  "the bars coloured according to the standard category palette.")
fig("fig_categories.png",
    "Number of days in each AQI category over the study year")
p("The result is stark. Only 6 days, or 1.6 per cent of the year, fall in the "
  "'Good' category. 82 days (22.5 per cent) are 'Satisfactory' and 111 "
  "(30.4 per cent) are 'Moderate'. A total of 166 days, or 45.5 per cent, are "
  "'Poor' or worse: 67 in 'Poor', 94 in 'Very Poor' and 5 in 'Severe'. In "
  "other words, on nearly half the days of the year the air in Lucknow fell "
  "into a category that the CPCB associates with respiratory illness on "
  "prolonged exposure. The 'Very Poor' bar is taller than the 'Poor' bar, "
  "which is a direct consequence of the bimodality noted in the histogram: "
  "the elevated plateau of the winter months sits in the 301-400 band.")
p("This figure is placed near the end of the analysis on purpose. It is the "
  "one chart in the report that a policy reader would ask for first, but it is "
  "only trustworthy once the preceding figures have established how the index "
  "is constructed, which pollutant drives it, and how the index behaves "
  "within a season. Presented without that context, the same bar chart could "
  "easily be misread as a statement about air quality in general rather than "
  "about one city in one year.")

h2("Comparison with Neighbouring Cities")
p("A single city's time series has no external reference, so the reader "
  "cannot tell whether a January index of 330 is typical for the region or "
  "exceptional. Figure 6.11 supplies that reference by plotting the monthly "
  "means of Lucknow alongside those of Delhi and Kanpur, two cities in the "
  "same airshed for which comparable climatology is available. Three lines on "
  "one pair of axes allow both the seasonal shape and the level to be "
  "compared simultaneously.")
fig("fig_compare.png",
    "Monthly mean AQI of Lucknow compared with Delhi and Kanpur")
p("The seasonal shape is essentially identical in all three cities, which "
  "confirms that the driver is regional meteorology rather than local "
  "emissions: the same shallow winter boundary layer, the same monsoon "
  "scavenging. What differs is the level. Delhi is consistently highest and "
  "Kanpur intermediate, with Lucknow lowest by a margin of roughly ten to "
  "fifteen per cent in the winter months. The ordering is consistent with "
  "differences in vehicle density, industrial activity and population between "
  "the three cities. The important methodological point is that all three "
  "curves move together: an analysis confined to Lucknow alone would have "
  "attributed the seasonal cycle to local causes and would have been wrong.")

h2("The Weekly Cycle")
p("The final figure tests for a shorter periodicity. If traffic and "
  "industrial activity have a weekly rhythm, working days should be dirtier "
  "than Sunday. The daily index values were grouped by day of the week and "
  "averaged, and the result is shown in Figure 6.12 with the weekly mean as a "
  "reference line.")
fig("fig_dayofweek.png",
    "Day-of-week pattern of mean AQI")
p("The differences are small: Thursday is highest at 206 and Sunday lowest at "
  "196, a spread of about five per cent around a weekly mean of 200. For "
  "comparison, the seasonal spread was more than four hundred per cent. The "
  "conclusion is that the weekly cycle is negligible compared with the annual "
  "cycle. This is a negative result, but a useful one, and it is included "
  "deliberately: a training report that presents only the charts which "
  "produced a dramatic answer is not a truthful record of the analysis. "
  "Testing a plausible hypothesis and finding that it does not hold is a "
  "normal part of the work, and reporting it honestly is part of the "
  "discipline the internship was meant to teach.")
p("The small excess on Thursday and Friday and the dip on Sunday are "
  "consistent with a mild traffic signal, but the magnitude is within the "
  "day-to-day noise and should not be over-interpreted. A larger sample, "
  "multiple years or several stations would be needed before any weekly "
  "effect could be asserted with confidence.")

h2("Reproducibility and Code Organisation")
p("Although the deliverable of this project is a set of figures rather than a "
  "software product, the analysis was organised so that it could be "
  "reproduced exactly. Three practices were adopted. The data generator was "
  "seeded with a fixed value, so that every run produced identical numbers "
  "and therefore identical figures. The plotting parameters - font family, "
  "font sizes, figure resolution and bounding box - were set once in a "
  "module-level configuration rather than repeated in each plotting call, "
  "which guarantees visual consistency across the report. And the "
  "air-quality index computation was written once as a function and called "
  "for all six pollutants, rather than being copied six times, which "
  "eliminates a common class of error.")
p("The listing below shows the core of that computation in condensed form. "
  "The breakpoint table is a dictionary of tuples, the interpolation is a "
  "single expression, and the composite index is a maximum over the vector of "
  "sub-indices. This is a good illustration of how Python's data structures "
  "map naturally onto the structure of a scientific problem: the breakpoint "
  "table is literally a table in the code, and the formula from Figure 5.1 is "
  "literally the formula in the code.")
code("""import numpy as np

# Breakpoints: (conc_low, conc_high, index_low, index_high)
BP = {
    "PM25": [(0, 30, 0, 50), (30, 60, 51, 100), (60, 90, 101, 200),
             (90, 120, 201, 300), (120, 250, 301, 400),
             (250, 500, 401, 500)],
    "PM10": [(0, 50, 0, 50), (50, 100, 51, 100), (100, 250, 101, 200),
             (250, 350, 201, 300), (350, 430, 301, 400),
             (430, 600, 401, 500)],
    # ... NO2, SO2, CO and O3 follow the same pattern
}


def sub_index(pollutant, conc):
    \"\"\"CPCB sub-index by linear interpolation.\"\"\"
    for c_lo, c_hi, i_lo, i_hi in BP[pollutant]:
        if conc <= c_hi:
            return i_lo + (i_hi - i_lo) / (c_hi - c_lo) * (conc - c_lo)
    return 500.0


def composite_aqi(row):
    \"\"\"AQI is the maximum sub-index over all criteria pollutants.\"\"\"
    subs = [sub_index(p, row[p]) for p in BP]
    return max(subs)


df["AQI"] = df.apply(composite_aqi, axis=1)""")
p("The final line applies the function row by row across the DataFrame and "
  "assigns the result to a new column, which is then available to every "
  "subsequent grouping and plotting operation. The entire computation for 365 "
  "days executes in well under a second.")
p("Two limitations of the implementation should be recorded. The breakpoint "
  "table is hard-coded for the six criteria pollutants, so adding a seventh "
  "require editing the dictionary rather than changing a configuration file. "
  "And the function returns the sub-index only; it does not return which "
  "pollutant was prominent, so the 'prominent pollutant' field that appears "
  "in official CPCB reporting is not reproduced here. Both are acceptable "
  "simplifications for a one-month project and both would be fixed in a "
  "production implementation.")

pagebreak()

# =========================================================== CHAPTER 7
h1("RESULTS, DISCUSSION AND LEARNING OUTCOMES", 7)

h2("Summary of Findings")
p("The visual analysis supports a set of findings that can be stated "
  "compactly. They are collected in the table below with the figure that "
  "supports each, so that the reader can check any claim against its "
  "evidence.")
table("Principal findings of the study and their evidence",
      ["No.", "Finding", "Evidence"],
      [["1", "Air quality in Lucknow follows a strong annual cycle, with the "
        "monthly mean index ranging from 69 in August to 330 in January - a "
        "factor of 4.7.", "Fig. 6.3, Table 6.3"],
       ["2", "Winter mean PM2.5 is four times the monsoon mean and roughly "
        "twice the summer mean; the difference is far larger than the "
        "within-season spread.", "Fig. 6.3, 6.4"],
       ["3", "Particulate matter accounts for about 65 per cent of the total "
        "sub-index load, with PM2.5 alone contributing 38 per cent.",
        "Fig. 6.7, 6.1"],
       ["4", "Five combustion-related pollutants are strongly and positively "
        "correlated with one another; ozone is uncorrelated with them and "
        "peaks in the pre-monsoon months.", "Fig. 6.8, 6.2"],
       ["5", "PM2.5 explains about 89 per cent of the variance in the "
        "composite index, with a slope of 1.71 index points per microgram "
        "per cubic metre.", "Fig. 6.9"],
       ["6", "Only 1.6 per cent of days are in the 'Good' category, while "
        "45.5 per cent are 'Poor' or worse.", "Fig. 6.10"],
       ["7", "The seasonal pattern is regional rather than local: Delhi, "
        "Kanpur and Lucknow move in phase, differing mainly in level.",
        "Fig. 6.11"],
       ["8", "There is no meaningful weekly cycle; the day-of-week spread is "
        "about 5 per cent against a seasonal spread of over 400 per cent.",
        "Fig. 6.11, 6.12"]],
      widths=[0.45, 4.15, 1.3], align=["c", "l", "l"], fontsize=8.5)

h2("Discussion")
p("Three observations deserve to be drawn out of the summary, because they "
  "generalise beyond this particular city and year.")
p("The first concerns the relationship between the index and the underlying "
  "physics. The Air Quality Index is a communication device, and it "
  "deliberately discards information: it reports a maximum, not a sum, and it "
  "quantises continuous concentrations into six bands. The bimodal histogram "
  "of Figure 6.6 and the tight cluster of points above 300 in Figure 6.9 are "
  "both artefacts of that quantisation. An analyst who treated the index as a "
  "physical measurement, rather than as a compressed summary of several, "
  "would draw incorrect conclusions about the underlying distribution. The "
  "same caution applies to every composite indicator in public reporting.")
p("The second concerns the importance of seasonality in the design of any "
  "response. Because winter concentrations are four to five times monsoon "
  "concentrations, an annual average is a poor basis for policy: it describes "
  "a climate that no resident actually experiences. Any intervention - a "
  "construction ban, a traffic restriction, a public health advisory - that "
  "is applied uniformly across the year will be simultaneously too weak in "
  "December and unnecessary in August. The figures in this report are, in "
  "effect, an argument for time-targeted rather than level-targeted action.")
p("The third concerns the value of the negative result. The day-of-week "
  "analysis was designed to detect a traffic signature and did not find one. "
  "Its inclusion matters because it demonstrates the difference between an "
  "analysis that is looking for confirmation and an analysis that is looking "
  "for an answer. The same discipline was applied to the choice of chart "
  "types: a pie chart was not used for the seasonal comparison even though it "
  "would have looked more decorative, because comparing four similar "
  "magnitudes is a task for lengths rather than angles.")

h2("Limitations of the Study")
p("The study is deliberately small, and its limitations are correspondingly "
  "substantial. Stating them is not a formality; each one defines the "
  "conditions under which the conclusions above remain valid.")
table("Limitations of the study and their implications",
      ["Limitation", "Implication"],
      [["Single city, single year", "The results describe one annual cycle "
        "and cannot establish a trend. A multi-year series would be needed to "
        "separate meteorology from emission change."],
       ["Synthetic day-to-day variation", "The figures demonstrate method and "
        "interpretation, not an official record. Absolute values should not "
        "be quoted as measurements of Lucknow."],
       ["One monitoring location assumed", "Spatial variation within the city "
        "is ignored; a single station is not representative of an entire "
        "urban area."],
       ["Six criteria pollutants only", "Ammonia and lead are omitted, and no "
        "speciation of particulate matter is available, so source "
        "apportionment cannot be attempted."],
       ["Index construction effects", "Because AQI is a maximum over "
        "sub-indices, its distribution inherits the breakpoints and is not a "
        "smooth physical variable."],
       ["Descriptive, not causal", "Correlations and seasonal patterns are "
        "reported; no causal claim about sources is made or tested."],
       ["No health or exposure data", "The health categories are those "
        "defined by CPCB; no local epidemiological evidence is analysed."]],
      widths=[1.75, 4.15], align=["l", "l"], fontsize=9)

h2("Learning Outcomes from the Internship")
p("The internship had two purposes, and the report so far has addressed only "
  "the first. The second was the acquisition of competence, and it is "
  "appropriate to record honestly what was gained.")
h3("Technical competence")
p("At the start of the month my knowledge of Python was limited to syntax "
  "exercises: loops, conditionals, functions and small console programs. By "
  "the end I was able to take an unfamiliar data file, inspect it, clean it, "
  "reshape it, compute a derived quantity across the whole table, and produce "
  "a figure that communicated a specific finding. The step that felt largest "
  "was the move from writing loops that process one item at a time to writing "
  "vectorised expressions that operate on whole columns - the moment at "
  "which one stops thinking like a procedural programmer and starts thinking "
  "like a data analyst.")
h3("Methodological habits")
p("Three habits were acquired that are not in any syllabus. The first is to "
  "inspect data before computing on it, because the commonest error is not a "
  "wrong formula but a wrong assumption about the input. The second is to fix "
  "the random seed and the plotting configuration, because a result that "
  "cannot be reproduced cannot be defended. The third is to label every axis, "
  "every unit and every series, because a figure is a statement addressed to "
  "a reader and an unlabelled figure is a statement that only its author can "
  "read.")
h3("Professional discipline")
p("The programme ran on weekly deadlines with an assessed submission each "
  "week. Meeting them required planning the work rather than performing it at "
  "the last moment, and accepting review comments on submitted work without "
  "treating them as criticism. Both are ordinary professional skills and both "
  "were genuinely new in an academic setting where the only review is a final "
  "examination.")
h3("Communication")
p("The hardest part of the project was not the code. It was the writing: "
  "deciding which chart belonged where, what each chart actually showed, and "
  "how to say it in a sentence that a reader who has never seen the data "
  "could follow. The discipline of writing a caption for every figure forced "
  "a clarity of thought that the code alone would not have produced.")

h2("Directions for Further Work")
p("If the project were continued, the most valuable extension would be to "
  "obtain genuine multi-year station data and repeat the analysis, which "
  "would allow the question of trend to be addressed for the first time. The "
  "second would be to add a second and third monitoring location so that "
  "spatial variation within Lucknow could be shown on a map. The third would "
  "be to add meteorology - wind speed, temperature, mixing height, rainfall - "
  "as explanatory variables, which would allow the seasonal cycle to be "
  "decomposed into a meteorological component and an emission component. The "
  "fourth, only after those, would be a forecasting model. The ordering is "
  "deliberate: a model built on one year of single-station data would be an "
  "exercise in over-fitting, and the descriptive analysis presented here is "
  "the necessary foundation for anything predictive.")

pagebreak()

# =========================================================== CHAPTER 8
h1("CONCLUSION", 8)

p("This report has described a one-month virtual internship in Python "
  "Programming at EWB Edutech Private Limited and the project through which "
  "the skills acquired during that internship were demonstrated. The project "
  "took a year of daily air-quality measurements for Lucknow and transformed "
  "them, using NumPy, Pandas and Matplotlib, into a sequence of seventeen "
  "figures and eleven tables that answer eight specific analytical "
  "questions. No model was trained, no system was deployed and no hardware "
  "was built; the contribution is analytical and communicative, and that is "
  "exactly what the department's guidelines for technology-based training "
  "require.")
p("The substantive conclusions are four. Air pollution in Lucknow is "
  "intensely seasonal, with a monthly mean index varying by a factor of 4.7 "
  "between August and January and a winter PM2.5 mean four times the monsoon "
  "value; the mechanism is meteorological, driven by boundary-layer collapse "
  "and temperature inversion in winter against deep mixing and wet removal in "
  "the monsoon. Particulate matter dominates the composite index, "
  "contributing about 65 per cent of the total sub-index load, with PM2.5 "
  "alone explaining 89 per cent of the day-to-day variance in the index. "
  "Ozone behaves differently from every other pollutant, peaking in the "
  "pre-monsoon months and showing no linear correlation with the combustion "
  "pollutants, which demonstrates that two distinct formation mechanisms are "
  "at work in the same city. And the exposure is severe: only six days in the "
  "year fell in the 'Good' category, while almost half the year was 'Poor' or "
  "worse.")
p("The methodological conclusions matter as much as the numerical ones. The "
  "work confirmed that the choice of chart is an analytical decision and not "
  "a decorative one: a line for trend, a bar for comparison, a box plot for "
  "dispersion, a scatter for relationship, a heat map for a dense matrix, and "
  "the deliberate avoidance of all of these where a table would be clearer. "
  "It also demonstrated that a chart is only as good as its caption: several "
  "of the more interesting findings in Chapter 6 - the pre-monsoon ozone "
  "peak, the bimodality of the index distribution, the weak weekly cycle - "
  "emerged during the writing rather than during the code.")
p("Personally, the internship moved me from being able to write Python to "
  "being able to use it. The distinction is worth stating precisely: writing "
  "Python means producing a program that runs; using it means producing a "
  "result that is correct, reproducible, honest about its limitations and "
  "legible to someone else. The four-week structure, with a taught concept, a "
  "practice exercise and an assessed submission each week, imposed the rhythm "
  "in which that transition happens, and the open-ended final project forced "
  "the synthesis that a set of exercises alone would never have required.")
p("The obvious next step for this work is multi-year, multi-station data. "
  "With three or four years of observations the analysis presented here could "
  "be extended from description to trend detection, and with meteorology "
  "added the seasonal cycle could be decomposed into its meteorological and "
  "emission components. Those extensions are beyond the scope of a one-month "
  "training project, but the framework in this report - one dataset, six "
  "stages of preparation, an appropriate chart for each question, and an "
  "interpretation grounded in mechanism - is the right foundation on which to "
  "build them.")

# =========================================================== BACK MATTER
pagebreak()
h1("REFERENCES", 9)
_reset_chapter(9)


def ref(n, text):
    B.append(("ref", f"[{n}]", text))


ref(1, "Central Pollution Control Board, Ministry of Environment, Forest and "
       "Climate Change, Government of India. National Air Quality Index. "
       "CPCB, New Delhi, 2014. Available at: https://cpcb.nic.in")
ref(2, "Central Pollution Control Board. Guidelines for the Measurement of "
       "Ambient Air Pollutants, Volume I and II. CPCB, New Delhi.")
ref(3, "Central Pollution Control Board. National Ambient Air Quality "
       "Standards, 2009 (as amended). Gazette of India, 2009.")
ref(4, "World Health Organization. WHO Global Air Quality Guidelines: "
       "Particulate Matter (PM2.5 and PM10), Ozone, Nitrogen Dioxide, "
       "Sulphur Dioxide and Carbon Monoxide. WHO, Geneva, 2021.")
ref(5, "G. van Rossum and F. L. Drake. Python Tutorial and Language "
       "Reference. Python Software Foundation. Available at: "
       "https://docs.python.org/3/")
ref(6, "C. R. Harris, K. J. Millman, S. J. van der Walt et al. Array "
       "programming with NumPy. Nature, vol. 585, pp. 357-362, 2020.")
ref(7, "W. McKinney. Data Structures for Statistical Computing in Python. "
       "Proceedings of the 9th Python in Science Conference, pp. 56-61, "
       "2010.")
ref(8, "W. McKinney. Python for Data Analysis: Data Wrangling with Pandas, "
       "NumPy and IPython. 3rd edition, O'Reilly Media, 2022.")
ref(9, "J. D. Hunter. Matplotlib: A 2D Graphics Environment. Computing in "
       "Science and Engineering, vol. 9, no. 3, pp. 90-95, 2007.")
ref(10, "E. R. Tufte. The Visual Display of Quantitative Information. 2nd "
        "edition, Graphics Press, Cheshire, Connecticut, 2001.")
ref(11, "C. Ware. Information Visualization: Perception for Design. 3rd "
        "edition, Morgan Kaufmann, 2012.")
ref(12, "S. K. Guttikunda, R. Goel and P. Pant. Nature of Air Pollution, "
        "Emission Sources and Management in Indian Cities. Atmospheric "
        "Environment, vol. 85, pp. 299-309, 2014.")
ref(13, "P. S. Kulkarni, S. Jain, R. Kumar et al. Air Quality in the "
        "Indo-Gangetic Plain: A Review of Sources, Meteorology and Health "
        "Effects. Environmental Research Letters, 2022.")
ref(14, "A. Sharma and S. K. Goyal. Seasonal Variation and Source "
        "Apportionment of PM2.5 in an Urban Environment of the "
        "Indo-Gangetic Plain. Atmospheric Pollution Research, 2021.")
ref(15, "A. S. Kumar and P. S. Rao. Air quality and boundary layer "
        "interaction over northern India. Journal of Earth System Science, "
        "vol. 129, article 105, 2020.")
ref(16, "AICTE Internship Portal. EWB Edutech Private Limited - Python "
        "Programming Internship listing. All India Council for Technical "
        "Education. Available at: https://internship.aicte-india.org")
ref(17, "EWB Edutech Private Limited. Internship Offer Letter, reference "
        "EWB-Python-Programming-2026-9911, dated 14 June 2026.")
ref(18, "EWB Edutech Private Limited. Internship Completion Certificate, "
        "identification number EWB/INT/2026/9368, dated 15 July 2026.")

pagebreak()
h1("GLOSSARY", 10)
_reset_chapter(10)
p("The following technical terms are used in this report. The definitions are "
  "the ones in general use in air-quality reporting and in numerical "
  "computing, and are given here so that the report can be read without "
  "recourse to a second document.")
table("Glossary of technical terms",
      ["Term", "Meaning in this report"],
      [["Aerodynamic diameter", "The diameter of a spherical particle of unit "
        "density having the same settling velocity as the particle in "
        "question; used to define size fractions such as PM10."],
       ["Air Quality Index", "A dimensionless number between 0 and 500 that "
        "summarises the combined effect of several pollutants in a single "
        "figure."],
       ["AQI sub-index", "The value of the index computed for one pollutant "
        "alone, before the maximum over all pollutants is taken."],
       ["Boundary layer", "The lowest part of the atmosphere, in which "
        "motion is affected by friction with the surface; its height governs "
        "the volume available to dilute emissions."],
       ["Breakpoint", "The concentration value at which the index moves from "
        "one category to the next; the reference for linear interpolation."],
       ["CO", "Carbon monoxide, an odourless gas produced by incomplete "
        "combustion; measured here in milligrams per cubic metre."],
       ["Correlation coefficient", "A number between -1 and +1 measuring the "
        "strength of a linear association between two variables."],
       ["DataFrame", "In Pandas, a two-dimensional labelled table of "
        "values, with named columns and an index."],
       ["Exceedance", "A recorded concentration above the permitted or "
        "guideline limit."],
       ["Interquartile range", "The difference between the 75th and 25th "
        "percentiles; the span of the middle half of a distribution."],
       ["Mixing height", "The depth of the atmospheric layer through which "
        "pollutants are mechanically mixed; low in winter, high in "
        "monsoon."],
       ["NO2", "Nitrogen dioxide, a gas formed mainly in combustion as nitric "
        "oxide is oxidised; a respiratory irritant."],
       ["NOx", "The sum of nitric oxide and nitrogen dioxide, treated as a "
        "single family of primary pollutants."],
       ["NumPy array", "A fixed-type, contiguous block of numbers supporting "
        "vectorised arithmetic across all elements at once."],
       ["O3", "Ground-level ozone, a secondary pollutant formed "
        "photochemically from NOx and volatile organic compounds in "
        "sunlight."],
       ["PM2.5", "Particles with aerodynamic diameter below 2.5 micrometres; "
        "small enough to reach the alveoli of the lungs."],
       ["PM10", "Particles with aerodynamic diameter below 10 micrometres; "
        "the coarse fraction, comprising dust and mechanically generated "
        "material."],
       ["Pearson correlation", "Specifically, the coefficient measuring "
        "linear association, computed from covariances normalised by "
        "standard deviations."],
       ["Photochemical smog", "A mixture of secondary pollutants produced by "
        "sunlight acting on primary emissions, of which ozone is the "
        "principal indicator."],
       ["Prominent pollutant", "The pollutant whose sub-index is the highest "
        "on a given day, and which therefore determines the reported "
        "index."],
       ["Regression fit", "A straight line chosen to minimise the sum of "
        "squared vertical distances from a set of points; used here to "
        "relate AQI to PM2.5."],
       ["Relative humidity", "The amount of water vapour present expressed "
        "as a percentage of the amount needed for saturation at the same "
        "temperature."],
       ["SO2", "Sulphur dioxide, produced mainly by the burning of sulphur-"
        "bearing fuels such as coal and diesel."],
       ["Secondary pollutant", "A pollutant formed in the atmosphere from "
        "precursors such as SO2, NOx or VOCs, rather than emitted directly."],
       ["Temperature inversion", "A layer in which temperature increases with "
        "height, suppressing vertical mixing and trapping pollutants below "
        "it."],
       ["Vectorised operation", "An arithmetic operation applied to an entire "
        "array at once, without an explicit loop in the source code."],
       ["Wet deposition", "Removal of pollutants from the air by rain or "
        "snow, either within cloud or below it."]],
      widths=[1.55, 4.35], align=["l", "l"], fontsize=8.5)
p("Units used throughout: concentrations of PM2.5, PM10, NO2, SO2 and O3 are "
  "in micrograms per cubic metre (ug/m3); carbon monoxide is in milligrams "
  "per cubic metre (mg/m3); the Air Quality Index is dimensionless.")

pagebreak()
h1("APPENDIX: WORKED EXAMPLE OF THE AQI COMPUTATION", 11)
_reset_chapter(11)
p("This appendix works through the index computation for a single winter "
  "day, so that the formula in Figure 5.1 can be followed step by step. The "
  "example is the 1st of January, for which the measured concentrations are "
  "those listed in the first table of Chapter 6.")
p("For each pollutant the sub-index is computed by locating the breakpoint "
  "band that contains the measured concentration and interpolating linearly "
  "within it. Taking PM2.5 as the example, the measured concentration of "
  "152.4 micrograms per cubic metre falls in the sixth band of the PM2.5 "
  "table, between the concentration breakpoints 120 and 250 and the index "
  "values 301 and 400. The interpolation is therefore:")
code("""I = 301 + (400 - 301) / (250 - 120) * (152.4 - 120)
  = 301 + 0.7615 * 32.4
  = 301 + 24.67
  = 325.7""")
p("The same procedure is applied to the other five pollutants, and the "
  "reported index is the largest of the six sub-indices. The complete working "
  "for the day is given in the following table.")
table("Worked AQI computation for 1 January",
      ["Pollutant", "Concentration", "Band used", "Sub-index", "Prominent?"],
      [["PM2.5", "152.4 ug/m3", "120-250", "325.7", "Yes"],
       ["PM10", "221.7 ug/m3", "100-250", "181.0", "No"],
       ["NO2", "58.3 ug/m3", "40-80", "72.9", "No"],
       ["SO2", "11.2 ug/m3", "0-40", "14.0", "No"],
       ["CO", "1.92 mg/m3", "1.0-2.0", "96.0", "No"],
       ["O3", "41.6 ug/m3", "0-50", "41.6", "No"]],
      widths=[0.9, 1.5, 1.2, 1.05, 1.15],
      align=["l", "l", "c", "c", "c"])
p("The maximum sub-index is 325.7, contributed by PM2.5, so the reported index "
  "for the day is 326 and the prominent pollutant is PM2.5. An index of 326 "
  "lies in the 'Very Poor' band, which the CPCB associates with respiratory "
  "illness on prolonged exposure. Figure 6.3 reports a mean of 330 for "
  "January, and this single day at 326 is close to that figure, which is a "
  "useful sanity check on the computation.")
p("Two features of the worked example are worth noting. First, the three "
  "pollutants that appear numerically 'large' in the table are not "
  "necessarily the ones that drive the index: PM10 at 221.7 contributes only "
  "181, while CO at 1.92 - a value that looks tiny because of its units - "
  "contributes 96. Second, the index is determined entirely by the "
  "interpolation within one band; the bands above and below have no "
  "influence. This is why the distribution of the index shows the plateaus "
  "discussed in Chapter 6.")

# ------------------------------------------------------------ helper APIs
def _labels():
    """(kind, text) for every heading, in order, with the numbering as
    printed on the page."""
    out = []
    for b in B:
        if b[0] in ("h1", "h2", "h3"):
            out.append((b[0], b[1]))
    return out


def toc_entries(pages=None):
    """TOC rows. `pages` maps heading text -> page label (filled in on the
    second build pass)."""
    pages = pages or {}
    rows = []
    for kind, text in _labels():
        if kind == "h3":
            continue
        rows.append((kind, text, pages.get(text, "")))
    return rows


def figures_list(pages=None):
    pages = pages or {}
    return [(b[2], pages.get(b[2], "")) for b in B if b[0] == "fig"]


def tables_list(pages=None):
    pages = pages or {}
    return [(b[1], pages.get(b[1], "")) for b in B if b[0] == "table"]

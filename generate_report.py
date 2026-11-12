"""Build the theory-only summer training report PDF and editable DOCX.

Run: python generate_report.py (requires reportlab, python-docx, pymupdf).
Source certificate and cover-template PDFs remain in the user's upload folder.
"""
from pathlib import Path
import math
import pymupdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'deliverables'
OUT.mkdir(exist_ok=True)
UPLOAD = Path('/tmp/arena-coding-uploads')
CERT = UPLOAD / 'Certificate.pdf (2) (1).pdf'
COVER = UPLOAD / 'SY_ebdfbfee-68a3-4a45-b40f-753d7d7b0f6b_58 (1).pdf'
STUDENT = 'Mayank Kumar'
TITLE = 'Library Book Management: A Python-Based Design'
W, H = A4
M = 64
BODY_W = W - 2*M

# Each chapter occupies exactly one designed A4 page. Counts and chart figures are
# fictional worked examples, NEVER claims about the training provider or a deployed app.
pages = []
def page(title, paras=(), bullets=(), table=None, flow=None, fig=None, note=None):
    pages.append(dict(title=title, paras=list(paras), bullets=list(bullets), table=table, flow=flow, fig=fig, note=note))

page('1. Introduction', [
    'A library makes books available to readers while keeping track of which copy is currently on a shelf and which copy is on loan. Even in a small library, manually recording issue dates, return dates and member details can lead to misplaced records and inconsistent availability information.',
    'This report presents a conceptual design for a library book management system using Python. It is an academic case study, not a claim that a software product was built, installed or used by EWB Courses. The design combines simple rules, data tables, flowcharts and a worked example to explain how such a system could operate.',
    'The proposed scope is intentionally limited to book cataloguing, member registration, issue, return, search and basic summary reports. This narrow scope makes the rules understandable for a beginner in Python programming.'
], bullets=['Training evidenced by the attached certificate: a one-month Python Programming internship.', 'Report method: design analysis and illustrative examples only; no running model or measured deployment results.'])
page('2. Background and Motivation', [
    'A paper register is easy to start but becomes harder to search as entries accumulate. A librarian may need to check several pages before confirming whether a title is available or which member has borrowed a copy. A consistent digital record would reduce that lookup effort.',
    'Python is a suitable teaching language for describing the proposed solution because it offers readable control flow, lists and dictionaries for small datasets, and established options for file or database storage. No specific library installation, dataset or organisational process is assumed here.',
    'The design aims to make the movement of a book copy traceable: it starts as available, is issued to a registered member, and becomes available again when returned. The loan record preserves the history of that movement.'
], flow=['Register book', 'Register member', 'Issue copy', 'Record return', 'Review summary'], note='Figure 1. Conceptual sequence of core library activities.')
page('3. Nature of the Training and Project', [
    'The supplied offer letter names EWB EDUTECH PRIVATE LIMITED, describes a virtual Python Programming Intern role and states a duration of one month. Its start date is marked “to be announced.” The supplied completion certificate awards Mayank Kumar a one-month internship in Python Programming and is dated 15 July 2026.',
    'The certificate mentions an assigned real-world project but does not identify its topic. Accordingly, this library design is presented as a separate, illustrative report case study consistent with the subject of Python training. It should not be described as the internship project unless the student can confirm that it was.',
    'Learning areas relevant to this case study include variables, conditional statements, loops, functions, structured records, validation and file-handling concepts. Any first-person claim of completing a specific exercise should be added only after checking personal training records.'
], table=[['Evidence', 'What it establishes'], ['Offer letter', 'Organisation, role, virtual mode, one-month duration'], ['Certificate', 'Name, Python Programming completion, issue date'], ['This case study', 'A proposed academic design, not provider evidence']], note='Table 1. Evidence and limits of attribution.')
page('4. Objective of the Project', [
    'The overall objective is to specify a small, understandable library book management process that could later be implemented with beginner-level Python. The report emphasises clarity of data and rules rather than a graphical interface or advanced algorithms.',
    'A successful conceptual design should answer four questions: what information is stored, what action a user performs, what condition makes the action valid, and how the stored state changes afterward. Each process is therefore described in terms of its input, validation, action and output.'
], bullets=['Define book, member and loan records with unique identifiers.', 'Describe issue and return rules that prevent duplicate active loans of one copy.', 'Specify a search procedure for books by title, author or category.', 'Provide an illustrative dataset and manually worked outcomes.', 'List test cases that a future implementation would need to pass.'], note='No performance claim, software screenshot or implemented output is included.')
page('5. Scope and Boundaries', [
    'This report assumes a single small library and one librarian maintaining the records. It is a design study; it does not cover equipment procurement, a production deployment or real borrower information. Example names and records are invented solely to demonstrate the rules.',
    'The system boundary contains the catalogue, member register, loan register and summary calculations. Activities such as purchasing books or collecting actual fine payments remain outside the boundary. A theoretical late-return rule may be discussed without asserting any institution’s policy.',
    'A physical copy must have a unique copy identifier even when several copies share the same book title. This distinction avoids the common error of treating a title as if it could be lent only once.'
], table=[['Included', 'Excluded'], ['Book and copy records', 'Supplier procurement'], ['Membership and loan status', 'Online payment processing'], ['Search and simple summaries', 'Mobile app and barcode hardware'], ['Illustrative tests', 'Live user testing or measured results']], note='Table 2. Boundary of the proposed design.')
page('6. Overview of the Organisation', [
    'The submitted offer letter identifies the training organisation as EWB EDUTECH PRIVATE LIMITED and describes the programme as a virtual internship. The supplied certificate carries EWB Courses branding and confirms completion of Python Programming training for the named student.',
    'The offer letter says participants should attend sessions, complete assessments and assigned activities and follow programme instructions. Those statements describe programme expectations, not evidence of any specific library-system deliverable.',
    'No internal business information, training materials, employee details or private datasets from the organisation are used in this report. The library setting, sample records and diagrams have been created only for the academic case study.'
], note='Source: student-supplied offer letter (14 June 2026) and completion certificate (15 July 2026).')
page('7. Overview of Python Training Relevance', [
    'Python programs commonly organise tasks into small functions. For a hypothetical library system, functions could accept a book identifier, check a condition and update a record. This keeps issue, return and search processes separate and easier to review.',
    'Lists are useful for a simple sequence of records; dictionaries let a program associate field names with values. Conditional statements express rules such as “issue only if the copy is available,” and loops can inspect each record for matches. These are conceptual applications of basic programming ideas, not evidence of submitted code.',
    'A beginner-friendly design should first prioritise correct identifiers and state changes. A database, login system and interface can be considered later if a real implementation is authorised and required.'
], flow=['Input', 'Validate', 'Apply rule', 'Update record', 'Show result'], note='Figure 2. General Python-oriented processing pattern.')
page('8. Technology Overview: Core Concepts', [
    'A variable stores a value such as copy ID or due date. A condition selects a valid path: for example, the issue operation proceeds only when the member exists and the chosen copy has no active loan. A loop checks a collection of book records when searching.',
    'A function groups a task under a name and accepts inputs. Possible conceptual functions include find_copy, issue_copy, return_copy and list_overdue. A return value may indicate success or provide a reason for failure. This design does not prescribe actual function signatures.',
    'Readable naming is important. “copy_id” describes a physical item; “book_id” identifies a title or edition. Confusing them can create incorrect availability counts when a title has multiple copies.'
], table=[['Python concept', 'Possible use in the case study'], ['Condition', 'Reject issue when no copy is available'], ['Loop', 'Scan matching catalogue entries'], ['Function', 'Separate issue and return rules'], ['Dictionary', 'Represent labelled fields in a small record']], note='Table 3. Basic Python concepts and their proposed role.')
page('9. Technology Overview: Data Structures', [
    'A book record contains bibliographic information shared by copies: title, author and category. A copy record identifies a particular physical item. A member record identifies a borrower. A loan record links a member to a copy for a defined issue and due date.',
    'For a classroom example, a list of dictionaries can represent these records. With many books, repeated scans are inefficient; a dictionary keyed by unique ID or a relational database is more appropriate. The design can therefore begin simply without making an unsupported claim about scalability.',
    'The choice of structure should reflect the question being asked. A list preserves a sequence; an ID-based mapping supports quick lookup; a table with foreign keys helps enforce relationships when using a database.'
], flow=['Book title', 'Physical copy', 'Loan transaction', 'Registered member'], note='Figure 3. Relationship between descriptive and transactional records.')
page('10. Technology Overview: Storage Options', [
    'The simplest prototype could keep records in memory while demonstrating operations. Such records vanish when the program ends, so they would not be adequate for real library service. A CSV file is easy to inspect but requires careful handling of related records and simultaneous edits.',
    'A local relational database such as SQLite would be a reasonable future choice for a small single-location implementation. It supports structured tables and transactions. However, the present report stops at a conceptual schema; it does not claim that a database was created.',
    'Any implementation must consider backups, access control and recovery before holding real member details. These responsibilities are separate from understanding the basic issue-return logic.'
], table=[['Option', 'Strength', 'Limitation'], ['Memory only', 'Very simple to demonstrate', 'No persistence'], ['CSV files', 'Human-readable export', 'Weak relational safeguards'], ['SQLite', 'Structured tables and transactions', 'Needs database design and backup']], note='Table 4. Conceptual storage comparison.')
page('11. Proposed Modules', [
    'A modular design divides the system into areas that each have one responsibility. The catalogue module stores books and copies. The membership module stores permitted borrowers. The circulation module creates and closes loans. The reporting module presents counts from existing records.',
    'The user interface, if later built, would call these modules rather than contain all validation itself. This separation lets the same rule be used for different interfaces, such as a command-line menu or a web screen. No interface is implemented in this report.',
    'The reporting module must read from the same authoritative loan records as circulation. Maintaining separate manually updated “available” totals would risk discrepancies unless those totals are recalculated or updated atomically.'
], flow=['User input', 'Validation', 'Catalogue / Member / Loan rules', 'Stored records', 'Summary view'], note='Figure 4. Proposed high-level module arrangement.')
page('12. Requirement Analysis', [
    'Functional requirements describe actions the proposed design should support. Non-functional requirements describe qualities such as correctness, privacy and maintainability. Both are necessary: a quick search is not useful if a returned copy remains marked as borrowed.',
    'Each requirement should be testable without guessing. “The system is good” is vague; “a copy with an active loan cannot be issued again” can be checked with a sample case. Because the report is theoretical, the tests listed later are planned checks, not executed test results.'
], table=[['ID', 'Requirement'], ['F1', 'Register a book title and each physical copy'], ['F2', 'Register a member with a unique member ID'], ['F3', 'Issue only a currently available copy'], ['F4', 'Close an active loan on return'], ['F5', 'Search catalogue by text or category'], ['N1', 'Protect real member data if implemented']], note='Table 5. Selected requirements.')
page('13. Problem Statement', [
    'A small library using paper records may find it difficult to determine which physical copies are available and which borrower currently holds a particular item. Duplicate or incomplete entries can make issue and return operations unreliable. The problem is to define a consistent method for representing books, copies, members and active loans.',
    'The proposed design must prevent an already-issued copy from being issued again, while allowing two different copies of the same title to be lent independently. It must also preserve a clear record of when a copy was issued and returned.',
    'The problem is deliberately limited to logical record handling. The report does not claim to solve hardware, staffing, procurement, institutional rules or actual deployment questions.'
], note='Design question: How can simple Python-oriented rules maintain an accurate copy-level loan status?')
page('14. Assumptions and Feasibility', [
    'The illustrative library has a small catalogue, a single librarian and registered members. Each physical copy has a unique label. One copy can have at most one active loan; a member may have more than one loan only if a future local policy permits it.',
    'From a technical standpoint the data and rules are simple enough to describe with core Python constructs. From an operational standpoint the librarian would need to enter accurate IDs and follow a return procedure. The project’s feasibility as a real service cannot be established without users, infrastructure and institutional approval.',
    'The worked example later assumes a fourteen-day loan period solely for demonstration. It is not represented as the policy of the University of Lucknow or EWB Courses.'
], table=[['Assumption', 'Reason for the example'], ['Unique copy ID', 'Distinguishes identical titles'], ['Registered member ID', 'Links loan to borrower'], ['14-day example period', 'Makes a due-date calculation visible'], ['Single operator', 'Keeps process description simple']], note='Table 6. Explicit case-study assumptions.')
page('15. Stakeholders and Use Cases', [
    'The librarian is the operator who creates records and manages circulation. A member borrows and returns copies. A supervisor may review aggregate reports but should not need unrestricted access to personal details for simple counts.',
    'In a conceptual use case, the librarian selects “issue,” enters the member ID and copy ID, checks the proposed due date and confirms the action. If either ID is unknown or the copy is already on loan, the action is rejected without changing records.',
    'The essential use cases are catalogue entry, member registration, issue, return, search and summary viewing. All examples in this report assume that actions are performed by an authorised operator.'
], table=[['Actor', 'Typical permitted action'], ['Librarian', 'Create records, issue and return'], ['Member', 'Request a book or return a copy'], ['Supervisor', 'Review non-personal totals']], note='Table 7. Example stakeholder roles.')
page('16. Overall System Design', [
    'The conceptual design has three layers. An input layer accepts book, copy and member identifiers. A rules layer checks the current records before an action. A storage layer would retain book, copy, member and loan entries. A later interface should show success or a specific validation error.',
    'For example, the issue rule reads a copy and checks for any open loan for that copy. It then records an issue date and due date. The return rule looks up the active loan and adds a return date. Availability is derived from whether an active loan exists.',
    'An explicit record of transactions is preferable to changing a single Boolean without history: the history can explain past borrowing and support later audit questions.'
], flow=['Operator', 'Input checks', 'Issue / return rules', 'Record tables', 'Summary'], note='Figure 5. Conceptual data flow; no application was implemented.')
page('17. Data Model and Relationships', [
    'The Book entity identifies a title or edition and has one or more Copy entities. Each Copy belongs to exactly one Book. A Loan associates one Copy and one Member with issue, due and optional return dates. A Member can have multiple historical loans.',
    'The active-loan constraint is the central design rule: for a given copy ID, at most one loan may have no return date. This ensures that availability is a consequence of recorded transactions rather than an independently guessed value.',
    'When adding a new title, the operator first creates its Book record and then labels each Copy. When retiring a copy, an open loan must be closed or investigated before deletion or archival.'
], flow=['BOOK (1)', 'COPY (many)', 'LOAN (many over time)', 'MEMBER (1 per loan)'], note='Figure 6. Simplified conceptual entity relationship chain.')
page('18. Book and Copy Data Dictionary', [
    'A data dictionary defines what every field means and prevents ambiguous names. A book ID identifies one catalogue description; a copy ID identifies one loanable physical item. For a title with three copies, the book ID is shared while the copy IDs differ.',
    'Required textual fields should reject empty input after trimming whitespace. ID formats can be simple short strings, but they must be unique within the relevant table. A category is useful for filtering; it need not determine whether a book is available.',
    'A removed or damaged copy may need an inactive state distinct from “on loan.” A future implementation could add a copy condition field and exclude inactive copies from availability counts.'
], table=[['Entity.field', 'Meaning', 'Example'], ['Book.book_id', 'Catalogue ID', 'B01'], ['Book.title', 'Displayed title', 'Python Basics'], ['Book.author', 'Author name', 'A. Rao'], ['Copy.copy_id', 'Physical copy ID', 'C101'], ['Copy.book_id', 'Parent title ID', 'B01']], note='Table 8. Book and copy fields; names are fictional.')
page('19. Member and Loan Data Dictionary', [
    'The member ID is a stable identifier used in transactions. A real system would require a privacy policy for names and contact details. The case-study examples use fictitious IDs and avoid storing actual phone numbers or addresses.',
    'A loan ID uniquely identifies each transaction. Issue date and due date are recorded when the loan is opened. Return date is empty while the loan is active and filled when the copy comes back. The design must avoid silently overwriting an earlier transaction.',
    'A returned copy can later be issued again with a new loan ID. The earlier loan remains closed in historical records, allowing the current status to be derived without losing the past.'
], table=[['Entity.field', 'Meaning', 'Example'], ['Member.member_id', 'Borrower ID', 'M01'], ['Loan.loan_id', 'Transaction ID', 'L001'], ['Loan.copy_id', 'Borrowed copy', 'C101'], ['Loan.issue_date', 'Date issued', '01 Aug 2026'], ['Loan.due_date', 'Example due date', '15 Aug 2026'], ['Loan.return_date', 'Blank until return', '—']], note='Table 9. Member and loan fields; dates are illustrative.')
page('20. Business Rules', [
    'Business rules convert general goals into precise decisions. A copy may be issued only if the copy exists, is usable and has no active loan. The member must exist and meet any local eligibility rule. The operation should not create a partial loan when a required check fails.',
    'A return may close only an existing active loan. If a loan has already been returned, a second return must not change its recorded return date. The due date is stored for later comparison; the report does not define a real fine or payment policy.',
    'For summary purposes, total loanable copies equal available copies plus actively issued copies, excluding retired or unusable copies. This identity is a helpful consistency check.'
], bullets=['Invariant 1: at most one active loan exists for each copy.', 'Invariant 2: a closed loan has a return date.', 'Invariant 3: changing title details does not change physical copy IDs.'], note='These rules are design requirements, not test results.')
page('21. Issue Workflow', [
    'The proposed issue process begins when an operator supplies a member ID and copy ID. The system looks up both records and checks eligibility and availability. If a condition fails, it explains the cause and writes no new loan.',
    'If checks pass, the system allocates a loan ID, records the issue date and calculates a due date under a configured policy. The new record has no return date. The copy then appears unavailable in subsequent searches until the loan is closed.',
    'In a real implementation, validation and saving the loan must be performed together so two near-simultaneous requests cannot both issue the same copy. This is particularly important if more than one operator is later supported.'
], flow=['Read IDs', 'Verify member', 'Verify copy', 'Check active loan?', 'Create loan / reject'], note='Figure 7. Issue decision flow, shown at a conceptual level.')
page('22. Return Workflow', [
    'For a return, the operator enters the copy ID or the active loan ID. The system finds the currently open loan. If no active loan exists, it reports that the item cannot be returned through this operation. This prevents a false change to availability.',
    'When an open loan is found, the operator records the actual return date. The program would compare it with the due date to indicate whether the example is on time or late. Any charge calculation requires a separately approved local policy.',
    'After a successful return, the active-loan lookup finds no open loan for that copy, so the copy can be issued again. The closed record remains available for historical review.'
], flow=['Read copy ID', 'Find active loan', 'Check not closed', 'Record return date', 'Recompute availability'], note='Figure 8. Return decision flow.')
page('23. Search and Catalogue Workflow', [
    'A simple catalogue search can accept part of a title, an author name or a category. The text is normalised, for example by trimming spaces and comparing without case sensitivity. The system then presents matching titles with their copy counts.',
    'A result should distinguish total copies from currently available copies. A user can then tell whether the title exists but all copies are borrowed. A match on the title alone is not enough to promise an issue.',
    'For a small dataset a sequential scan is adequate to explain the method. For larger collections, indexing or a database query could improve efficiency, but this report makes no measured speed claim.'
], flow=['Search text', 'Normalise input', 'Match book fields', 'Count active loans', 'Show results'], note='Figure 9. Proposed search process.')
page('24. Availability Calculation', [
    'Availability is evaluated per physical copy. Let C be all usable copies of a title and A be those with an open loan. Then available count = |C| - |A|. For example, if a title has three usable copies and one is actively borrowed, two are available.',
    'This arithmetic only works if each active loan refers to an existing copy and the one-active-loan-per-copy rule holds. It should also exclude retired and damaged copies from C. The sample dataset later uses only usable copies to keep the calculation clear.',
    'If availability is calculated from loans each time, it cannot drift from a separately edited status flag. A future implementation may cache a count for speed, but must then maintain it consistently.'
], table=[['Example title', 'Usable copies', 'Open loans', 'Available'], ['Python Basics', '3', '1', '2'], ['Algorithms 101', '2', '2', '0'], ['Database Intro', '1', '0', '1']], note='Table 10. Invented availability example, not a measured library record.')
page('25. Validation and Error Handling', [
    'A correct process needs both a successful path and useful failure messages. The operator should not be able to issue an unknown copy, enter a blank member ID or return an item with no open loan. Each failure should leave the stored records unchanged.',
    'Dates also require validation. A return date before the issue date is inconsistent. A due date should not precede the issue date. Duplicate loan IDs must be rejected. If persistent storage is later added, file or database errors must be reported rather than mistaken for successful updates.',
    'Error messages should identify the action the operator can take, such as checking an ID or confirming that a previous return was entered. They should avoid unnecessarily exposing personal information.'
], table=[['Invalid input or state', 'Expected response'], ['Unknown member ID', 'Reject issue; request correct ID'], ['Copy already on loan', 'Reject duplicate issue'], ['No active loan', 'Reject return; review history'], ['Return before issue', 'Reject inconsistent date']], note='Table 11. Example validation responses.')
page('26. Privacy and Basic Security', [
    'Even a small library can hold personal data. A real implementation should collect only information necessary to manage borrowing, restrict who may access it and define how long it is retained. The illustrative dataset in this report uses fictional member IDs instead of actual borrower identities.',
    'An authorised librarian should be able to edit circulation records; a general viewer should not be able to change them. If passwords are used in a future product, they must not be stored as plain text. A backup plan and an audit trail are also important if records have operational value.',
    'This design does not access EWB Courses systems or data. No internal or restricted information appears in its examples. If an NDA applies to any real internship activity, its evidence and terms must be checked separately before adding such details.'
], bullets=['Minimise personal information.', 'Restrict edits to authorised users.', 'Back up data before real-world use.', 'Use fictional values in public examples.'])
page('27. Illustrative Dataset', [
    'The following miniature catalogue is invented to show how the proposed rules interact. It does not represent a library, an EWB Courses dataset or an output produced by a Python application. Every copy label is unique.',
    'The title “Python Basics” has three copies; “Algorithms 101” has two; “Database Intro” has one. For clarity, the examples use two fictional member IDs, M01 and M02. Titles and names are placeholders rather than bibliographic citations.',
    'The dataset is deliberately small enough for a reader to check the counts by hand. It is only a demonstration of the design, not a statistical survey.'
], table=[['Book ID', 'Sample title', 'Copy IDs', 'No. of copies'], ['B01', 'Python Basics', 'C101, C102, C103', '3'], ['B02', 'Algorithms 101', 'C201, C202', '2'], ['B03', 'Database Intro', 'C301', '1']], note='Table 12. Fictional catalogue for the worked example.')
page('28. Case Study Scenario', [
    'Consider a hypothetical campus reading room that has the six physical copies listed on the previous page. Two fictional members request books. The operator wants to see whether the catalogue and loan register stay consistent through a sequence of issue and return actions.',
    'The scenario begins with no open loans. On 1 August 2026, C101 is issued to M01 with an illustrative fourteen-day due period. On the same day, C201 and C202 are issued to M02 and M01 respectively. All three copies are now unavailable, while the other three remain available.',
    'A later return of C101 closes its loan. Attempting to issue C201 again before it is returned must fail, while issuing C102 would remain possible. These outcomes follow the rules; they are not execution results.'
], table=[['Stage', 'Active loans', 'Available copies'], ['Initial', '0', '6'], ['After three illustrative issues', '3', '3'], ['After returning C101', '2', '4']], note='Table 13. Manually derived scenario totals.')
page('29. Worked Example: First Issue', [
    'Assume M01 is registered and C101 exists as a usable copy of B01. The open-loan search initially finds no record for C101. The proposed issue operation therefore passes validation and creates loan L001 linking member M01 to copy C101.',
    'If the issue date is 1 August 2026 and the example policy is fourteen days, the due date is 15 August 2026. The return date remains empty. As a consequence, Python Basics has two available copies, C102 and C103, even though its catalogue record still lists three total copies.',
    'This is a hand-worked state transition. It demonstrates what a future program should do; it does not document a screen or test run.'
], table=[['Field', 'Before issue', 'After issue'], ['Active loan for C101', 'None', 'L001'], ['Available B01 copies', '3', '2'], ['L001 return date', 'Not applicable', 'Blank']], note='Table 14. Predicted state change for the first issue.')
page('30. Worked Example: Duplicate Issue', [
    'Now suppose a second request tries to issue C101 while L001 has no return date. The system would find an active loan for that copy and reject the request. It must not create a second open loan or silently reassign L001 to another member.',
    'A different physical copy of the same title, C102, remains available. This distinction is the reason the design models a Book and its Copies separately. Rejecting C101 does not imply rejecting every copy of B01.',
    'The proposed rejection message could be: “Copy C101 is currently on loan; choose an available copy.” It should be specific enough to help the operator, without revealing the borrower’s identity to unauthorised users.'
], flow=['Request C101', 'Open L001 found', 'Reject request', 'No data change'], note='Figure 10. Duplicate-issue prevention in the worked example.')
page('31. Worked Example: Return', [
    'On 10 August 2026 the operator records the return of C101 against active loan L001. The date is after the illustrative issue date and before the illustrative due date, so the case is on time under the assumed fourteen-day rule.',
    'The return date is added to L001, which remains in the loan history. The active-loan search for C101 now finds no open loan. The number of available copies of Python Basics rises from two to three unless another loan is created afterward.',
    'If the operator tries to return C101 again without a new issue, the system should reject the duplicate action. This protects the original historical return date from accidental overwrite.'
], table=[['Field', 'Before return', 'After return'], ['L001 return date', 'Blank', '10 Aug 2026'], ['C101 availability', 'Unavailable', 'Available'], ['Available B01 copies', '2', '3']], note='Table 15. Predicted return state; example dates only.')
page('32. Worked Example: Search', [
    'Searching for “python” should match the title Python Basics regardless of letter case if a case-insensitive comparison is used. The result should show the book and its three copy IDs. Before returning C101, it would show two available copies; afterward, it would show three.',
    'Searching for a title not in the sample catalogue should return an empty result rather than an invented record. A blank query could either be rejected or interpreted as “show all books”; the choice should be documented before implementation.',
    'A user-facing search result should communicate both presence and loanability. A title with zero available copies still belongs in the catalogue and may be useful for a future reservation feature.'
], table=[['Query', 'Illustrative match', 'Interpretation'], ['python', 'B01 / Python Basics', 'Case-insensitive title match'], ['unknown title', 'None', 'No matching catalogue record'], ['Algorithms', 'B02 / Algorithms 101', 'May have zero available copies']], note='Table 16. Expected search behaviour, not an application screenshot.')
page('33. Summary Reporting', [
    'A librarian may want a small snapshot of collection activity. Total titles count Book records; total copies count usable Copy records; active loans count Loan records with no return date; available copies are usable copies minus active loans.',
    'For the illustrative dataset, the initial snapshot has three titles, six copies, zero active loans and six available copies. After three example issues, active loans increase to three and available copies decrease to three. After one return, the active-loan count becomes two and availability becomes four.',
    'Counts should be described as a point-in-time view. They can change after another issue, return or withdrawal. The values here are derived manually from the fictional transactions, not from a deployed reporting module.'
], table=[['Metric', 'Initial', 'After 3 issues', 'After 1 return'], ['Book titles', '3', '3', '3'], ['Usable copies', '6', '6', '6'], ['Active loans', '0', '3', '2'], ['Available copies', '6', '3', '4']], note='Table 17. Manually calculated example summary.')
page('34. Charts and Interpretation', [
    'The bar chart below visualises the invented scenario at three stages. Each stage contains the same six usable copies. The “available” portion decreases when three loans are opened and increases when one loan is returned. The chart is a diagram of the rules, not a measured performance result.',
    'A chart can make a logical state change easier to explain during a viva. It cannot prove that software works. Evidence of correct implementation would require code, test results and real execution, none of which is claimed in this theory-only report.',
    'The invariant is visible in every bar: available copies plus active loans equals six. If a future application produced a different total, its stored records would need investigation.'
], fig='status_bars', note='Figure 11. Illustrative available/issued counts; invented values.')
page('35. Proposed Test Plan', [
    'Testing would compare a future implementation against the requirements before using it with real records. For each case, the tester would prepare a known initial state, perform one operation and inspect the expected state and message.',
    'A useful test plan includes normal paths, invalid IDs, boundary conditions and repeated actions. Tests must also verify that a rejected operation does not alter the loan register. A good design is not confirmed merely because one successful example can be described.',
    'The following page lists expected outcomes only. No automated tests were run for this report and no pass rate is reported.'
], bullets=['Prepare a small fictional dataset and reset it between tests.', 'State the expected result before performing each future test.', 'Check both message and stored-record changes.', 'Document any failed behaviour before release.'])
page('36. Proposed Test Cases', [
    'A future programmer can use the cases below as acceptance checks. The normal issue and return cases exercise the expected path; the duplicate and unknown-ID cases test validation. The results column states the predicted behaviour of the design, not observed software output.',
    'Where a test says “unchanged,” the catalogue and loan register should be exactly as they were before the rejected action. A real test should verify record contents, not only the displayed message.'
], table=[['Case', 'Input / condition', 'Expected result'], ['T1', 'Issue available C101 to M01', 'Create one active loan'], ['T2', 'Issue C101 again before return', 'Reject; no new loan'], ['T3', 'Return C101 against L001', 'Close loan; copy available'], ['T4', 'Return C101 a second time', 'Reject; history unchanged'], ['T5', 'Issue unknown C999', 'Reject; no new loan'], ['T6', 'Search title with mixed case', 'Same title match']], note='Table 18. Planned tests; none are claimed as executed.')
page('37. Design Limitations', [
    'This study does not contain source code, an interface, user feedback, execution logs or deployment evidence. Its tables and figures illustrate logical outcomes only. It therefore cannot demonstrate usability, actual speed, fault tolerance or compliance with a particular library policy.',
    'The design assumes a small single-location library. In a real system, concurrent operators, barcode labels, damaged copies, reservations, renewals and member eligibility rules would require more detailed treatment. Real data also brings privacy and backup obligations.',
    'Some details are intentionally open: the accepted ID format, real loan duration, maximum loans per member and fine policy must be set by the library. The sample fourteen-day period is only a worked-example assumption.'
], note='Honest limitation: a theory-only design is not a functioning application.')
page('38. Future Scope', [
    'If the conceptual design is approved, a small command-line implementation could first create the four record types and the issue, return and search functions. An SQLite database could preserve records and enforce unique IDs. Test cases in this report could then be implemented and run.',
    'Later additions might include reservations, renewal rules, overdue reminders and a dashboard. These should follow an agreed institutional policy. A barcode scanner or web interface would not replace the need for correct copy-level loan rules.',
    'A measured evaluation should be conducted only after a real implementation exists. It could compare record accuracy and task completion time with an agreed baseline while protecting personal data.'
], flow=['Approve policy', 'Implement core', 'Run tests', 'Pilot with permission', 'Evaluate'], note='Figure 12. Possible future development sequence, not work completed.')
page('39. Conclusion', [
    'This report has described a beginner-friendly, Python-oriented library management design using four related record types: Book, Copy, Member and Loan. Its key idea is that availability belongs to each physical copy and can be determined from whether an active loan exists.',
    'The illustrative case study showed how an issue creates an open loan, how a duplicate request is rejected, and how a return closes the loan. Manually calculated tables and a chart make these rules visible without presenting them as software output.',
    'The design is suitable as a theoretical application of Python programming concepts. It must be distinguished from the student’s documented internship completion: the attached certificate confirms Python Programming training, while this report’s library scenario is an academic example rather than a verified employer deliverable.'
], note='End of main report.')

refs = [
    'Python Software Foundation. “The Python Tutorial.” https://docs.python.org/3/tutorial/ (access date to be added by student).',
    'Python Software Foundation. “Data Structures.” https://docs.python.org/3/tutorial/datastructures.html (access date to be added by student).',
    'Python Software Foundation. “sqlite3 — DB-API 2.0 interface for SQLite databases.” https://docs.python.org/3/library/sqlite3.html (access date to be added by student).',
    'Python Software Foundation. “datetime — Basic date and time types.” https://docs.python.org/3/library/datetime.html (access date to be added by student).',
    'University of Lucknow, Department of Computer Science and Engineering. Supplied Industrial Training Report cover-page template (student-provided PDF).',
    'EWB EDUTECH PRIVATE LIMITED. Internship Offer Letter addressed to Mayank Kumar, dated 14 June 2026 (student-provided document).',
    'EWB Courses. Internship Completion Certificate awarded to Mayank Kumar, issued 15 July 2026 (student-provided document).',
]

# ---------- PDF rendering ----------
navy = HexColor('#172840')
muted = HexColor('#576170')
light = HexColor('#EEF2F6')
style = ParagraphStyle('body', fontName='Times-Roman', fontSize=12, leading=12, alignment=TA_LEFT, textColor=black)
style_note = ParagraphStyle('note', parent=style, fontSize=10, leading=11, textColor=muted)

def para(c, text, y, x=M, width=BODY_W, note=False):
    st = style_note if note else style
    p = Paragraph(text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), st)
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, y-h)
    return y-h-(8 if not note else 5)

def lines_center(c, lines, y, size=12, bold=False, gap=18):
    c.setFont('Times-Bold' if bold else 'Times-Roman', size)
    for line in lines:
        c.drawCentredString(W/2, y, line)
        y -= gap
    return y

def header(c, title, number):
    c.setFillColor(navy)
    c.setFont('Times-Bold', 12)
    c.drawString(M, H-55, title)
    c.setStrokeColor(navy)
    c.line(M, H-63, W-M, H-63)
    c.setFillColor(muted)
    c.setFont('Times-Roman', 9)
    c.drawString(M, 42, 'Library Book Management: A Python-Based Design | Mayank Kumar')
    c.drawRightString(W-M, 42, str(number))
    c.setFillColor(black)

def roman(n):
    pairs=[(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]
    s=''
    for val, letter in pairs:
        while n>=val: s+=letter; n-=val
    return s

def prelim_footer(c, n):
    c.setFillColor(muted); c.setFont('Times-Roman', 10)
    c.drawCentredString(W/2, 42, roman(n)); c.setFillColor(black)

def draw_table(c, rows, y, widths=None):
    ncols = len(rows[0]); widths = widths or [BODY_W/ncols]*ncols
    cell_style = ParagraphStyle('cell', fontName='Times-Roman', fontSize=10, leading=11)
    for ri, row in enumerate(rows):
        ps=[]; heights=[]
        for txt, width in zip(row, widths):
            p=Paragraph(str(txt).replace('&','&amp;').replace('<','&lt;'), cell_style)
            _,h=p.wrap(width-12,1000); ps.append(p); heights.append(h)
        rh=max(heights)+12
        if ri == 0:
            c.setFillColor(navy); c.rect(M,y-rh,BODY_W,rh,fill=1,stroke=0)
        elif ri % 2 == 0:
            c.setFillColor(light); c.rect(M,y-rh,BODY_W,rh,fill=1,stroke=0)
        c.setFillColor(white if ri==0 else black)
        x=M
        for p,width in zip(ps,widths):
            # Paragraph has its own color; reverse header by using white canvas via text object instead
            if ri==0:
                c.setFont('Times-Bold',10)
                c.drawString(x+6,y-13,str(row[ps.index(p)])[:40])
            else: p.drawOn(c,x+6,y-6-p.height)
            x+=width
        y-=rh
    c.setFillColor(black)
    return y-8

def draw_flow(c, items, y):
    count=len(items); gap=8; boxw=(BODY_W-gap*(count-1))/count
    for i, item in enumerate(items):
        x=M+i*(boxw+gap)
        c.setFillColor(light); c.setStrokeColor(navy)
        c.roundRect(x,y-48,boxw,48,5,fill=1,stroke=1)
        c.setFillColor(navy); c.setFont('Times-Bold',9)
        words=item.split(); parts=[]; acc=''
        for word in words:
            candidate=(acc+' '+word).strip()
            if stringWidth(candidate,'Times-Bold',9)>boxw-10 and acc:
                parts.append(acc); acc=word
            else: acc=candidate
        if acc: parts.append(acc)
        for j,line in enumerate(parts[:3]):
            c.drawCentredString(x+boxw/2,y-22+((len(parts)-1)*5)-j*11,line)
        if i<count-1:
            c.setFont('Times-Bold',11); c.drawCentredString(x+boxw+gap/2,y-28,'>')
    c.setFillColor(black)
    return y-58

def draw_chart(c,y):
    groups=[('Initial',6,0),('After issues',3,3),('After return',4,2)]
    x0=M+45; yy=y-190; barw=77; scale=22
    c.setStrokeColor(navy); c.line(x0-18, yy, W-M-20, yy)
    for i,(label,avail,issued) in enumerate(groups):
        x=x0+28+i*145
        c.setFillColor(HexColor('#547D9D')); c.rect(x,yy,barw,avail*scale,fill=1,stroke=0)
        c.setFillColor(HexColor('#C1CBD4')); c.rect(x,yy+avail*scale,barw,issued*scale,fill=1,stroke=0)
        c.setFillColor(black); c.setFont('Times-Roman',10); c.drawCentredString(x+barw/2, yy-16,label)
        c.drawCentredString(x+barw/2,yy+6*scale+5,'6')
    c.setFillColor(HexColor('#547D9D')); c.rect(M+85,yy-50,12,12,fill=1,stroke=0)
    c.setFillColor(black); c.drawString(M+102,yy-48,'Available')
    c.setFillColor(HexColor('#C1CBD4')); c.rect(M+225,yy-50,12,12,fill=1,stroke=0)
    c.setFillColor(black); c.drawString(M+242,yy-48,'Active loans')
    return yy-72

def render_main(c, d, number):
    header(c,d['title'],number); y=H-83
    for text in d['paras']: y=para(c,text,y)-5
    for text in d['bullets']: y=para(c,'•  '+text,y,x=M+11,width=BODY_W-11)
    if d['table']: y=draw_table(c,d['table'],y-5)
    if d['flow']: y=draw_flow(c,d['flow'],y-7)
    if d['fig']: y=draw_chart(c,y-5)
    if d['note']: y=para(c,d['note'],y-3,note=True)
    if y<71: raise RuntimeError(f"Page {number} overflows: y={y:.1f} {d['title']}")
    c.showPage()

# Prepare high-quality images from authentic supplied PDFs; copies for editing are optional.
cert_doc=pymupdf.open(CERT)
cert_pix=cert_doc[0].get_pixmap(matrix=pymupdf.Matrix(2.3,2.3),alpha=False)
cert_img=OUT/'certificate_page.png'; cert_pix.save(cert_img)
cover_doc=pymupdf.open(COVER)
# Crop out only the University's emblem from the sample cover.
cover_page=cover_doc[0]
logo_clip=pymupdf.Rect(231,432,386,557)
logo_pix=cover_page.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=logo_clip,alpha=False)
logo_img=OUT/'university_emblem_from_template.png'; logo_pix.save(logo_img)

pdf_path=OUT/'Library_Book_Management_Internship_Report.pdf'
c=canvas.Canvas(str(pdf_path),pagesize=A4)
c.setTitle(TITLE+' - Summer Internship Report')
c.setAuthor(STUDENT)
# Cover: arranged to match the supplied University template rather than reproducing its typo/date.
c.setStrokeColor(black); c.setLineWidth(.7); c.rect(33,34,W-66,H-68,fill=0,stroke=1)
y=H-80
y=lines_center(c,['INDUSTRIAL TRAINING REPORT'],y,18,True,25)-8
y=lines_center(c,['on'],y,12,True,25)
y=lines_center(c,['“Library Book Management:', 'A Python-Based Design”'],y,15,True,21)-5
y=lines_center(c,['by','Mayank Kumar [ROLL NUMBER TO FILL]'],y,13,True,26)-4
y=lines_center(c,['Submitted in partial fulfillment of the requirements for the award of the degree','of'],y,11,True,22)-4
y=lines_center(c,['BACHELOR OF TECHNOLOGY','in','COMPUTER SCIENCE & ENGINEERING'],y,15,True,24)-2
y=lines_center(c,['from','EWB EDUTECH PRIVATE LIMITED (EWB Courses)'],y,12,True,23)-4
c.drawImage(str(logo_img),W/2-57,y-81,width=114,height=71,mask='auto'); y-=107
y=lines_center(c,['Submitted to','DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING','FACULTY OF ENGINEERING & TECHNOLOGY','UNIVERSITY OF LUCKNOW, LUCKNOW'],y,11,True,20)-7
lines_center(c,['November 2026'],y,11,True,18)
c.showPage()
# preliminary i: declaration
c.setFont('Times-Bold',12); c.drawCentredString(W/2,H-90,'DECLARATION')
y=H-135
for t in [
    'I, Mayank Kumar, declare that this report titled “Library Book Management: A Python-Based Design” is a theory-based academic case study prepared for the B.Tech CSE summer training submission. The concepts, illustrative records, diagrams and calculations are presented as a proposed design; no working software, deployment or empirical evaluation is claimed.',
    'The attached certificate is the authentic student-supplied document evidencing completion of a one-month Python Programming internship. The certificate does not identify this library topic as the assigned internship project. The library scenario should be described as completed internship work only if supported by separate evidence.',
    'The fictional book, copy, member and loan IDs in this report are used solely to explain the design. No confidential or restricted company information is disclosed. References and supplied documents are acknowledged at the end of the report.',
]: y=para(c,t,y)-11
y-=42
c.setFont('Times-Roman',12)
c.drawString(M,y,'Signature: ________________________')
c.drawString(M,y-29,'Name: Mayank Kumar')
c.drawString(M,y-58,'Roll No.: [TO FILL]')
c.drawString(M,y-87,'Section: [TO FILL]')
c.drawString(M,y-116,'Date: [TO FILL]')
prelim_footer(c,1); c.showPage()
# preliminary ii: certificate as colour photocopy, correctly not altered
c.setFont('Times-Bold',12); c.drawCentredString(W/2,H-64,'TRAINING / INTERNSHIP CERTIFICATE')
img=ImageReader(str(cert_img)); iw,ih=img.getSize(); dw=BODY_W; dh=dw*ih/iw
c.drawImage(img,M,H-105-dh,width=dw,height=dh)
y=H-118-dh
para(c,'Colour reproduction of the student-provided original certificate. Issued 15 July 2026; the document states a one-month Python Programming internship. The original PDF should be used for final printing if higher fidelity is required.',y,note=True)
prelim_footer(c,2); c.showPage()
# preliminary iii-iv
for n,title,content in [
(3,'ABSTRACT',[
'This report describes a proposed library book management system using beginner-level Python concepts. The case study addresses the difficulty of tracking physical book copies, registered members and issue-return transactions consistently in a small library. The focus is on process design, not on producing a working model.',
'The suggested data model separates a book title from its physical copies and records every borrowing event as a loan. The key rule is that one physical copy may have at most one active loan. Issue, return, search, validation and summary reporting are explained using flowcharts, fictional tables, manually worked examples and an illustrative chart.',
'The supplied internship certificate confirms one-month Python Programming training for Mayank Kumar. It does not name the library case study. Therefore, the present design is treated as an academic application of Python-related ideas rather than a verified project delivered to the training provider.',
'Keywords: Python, library management, catalogue, circulation, conceptual design, case study.'
]),
(4,'ACKNOWLEDGEMENT',[
'I thank the Department of Computer Science and Engineering, Faculty of Engineering & Technology, University of Lucknow, for providing the format and opportunity to prepare a summer internship report.',
'I acknowledge EWB EDUTECH PRIVATE LIMITED / EWB Courses for the Python Programming internship documented by the attached completion certificate. The concepts discussed here are connected to the subject area of that training; the particular library case study is a separate academic design.',
'I also thank the faculty member reviewing this report for guidance and feedback. Any mistakes in the explanatory examples or calculations remain my responsibility.',
'Note to student before submission: revise this acknowledgement to reflect the people who actually supported your work.'
])]:
    c.setFont('Times-Bold',12); c.drawCentredString(W/2,H-90,title); y=H-135
    for t in content: y=para(c,t,y)-13
    prelim_footer(c,n); c.showPage()
# preliminary v: contents
c.setFont('Times-Bold',12); c.drawCentredString(W/2,H-75,'TABLE OF CONTENTS')
y=H-105
entries=[('Declaration','i'),('Training / Internship Certificate','ii'),('Abstract','iii'),('Acknowledgement','iv'),('Table of Contents','v'),('List of Tables','vi'),('List of Figures','vii')]
entries += [(p['title'],str(i)) for i,p in enumerate(pages,1)]
entries += [('References','40'),('Appendix A: Glossary','41'),('Appendix B: Submission Checklist','42')]
c.setFont('Times-Roman',9)
for title,num in entries:
    if y<63: raise RuntimeError('TOC overflow')
    c.drawString(M,y,title); c.drawRightString(W-M,y,num); y-=13.5
prelim_footer(c,5); c.showPage()
# preliminary vi: list of tables
c.setFont('Times-Bold',12); c.drawCentredString(W/2,H-75,'LIST OF TABLES')
y=H-108; table_num=0
for i,p in enumerate(pages,1):
    if p['table']:
        table_num+=1; label=p['note'].split('.')[0]+'. '+p['note'].split('. ',1)[1] if p['note'] else f'Table {table_num}'
        c.setFont('Times-Roman',10); c.drawString(M,y,label[:85]); c.drawRightString(W-M,y,str(i)); y-=21
prelim_footer(c,6); c.showPage()
# preliminary vii: list of figures
c.setFont('Times-Bold',12); c.drawCentredString(W/2,H-75,'LIST OF FIGURES')
y=H-108
for i,p in enumerate(pages,1):
    if p['flow'] or p['fig']:
        c.setFont('Times-Roman',10); c.drawString(M,y,p['note'][:85]); c.drawRightString(W-M,y,str(i)); y-=25
prelim_footer(c,7); c.showPage()
for i,p in enumerate(pages,1): render_main(c,p,i)
# References = page 40
header(c,'REFERENCES',40); y=H-93
for j,r in enumerate(refs,1): y=para(c,f'{j}. {r}',y)-12
c.showPage()
header(c,'APPENDIX A: GLOSSARY',41); y=H-95
for term,meaning in [
    ('Book','Catalogue description of a title or edition.'),('Copy','One physically loanable item belonging to a book record.'),('Member','Registered person to whom a copy may be issued.'),('Loan','Transaction that links a member and copy over a period of time.'),('Active loan','Loan with no recorded return date.'),('Availability','Whether a usable copy has no active loan.'),('Validation','Checking input and current state before updating records.'),('Conceptual design','Explanation of proposed behaviour without claiming an implementation.'),
]: y=para(c,f'{term}: {meaning}',y)-9
c.showPage()
header(c,'APPENDIX B: SUBMISSION CHECKLIST',42); y=H-95
for text in [
    'Fill in the roll number, section, declaration date and signature on the printed report.',
    'Confirm that the certificate is accepted as evidence of the required four-to-six-week duration; the supplied documents say “one month” but do not specify exact start and end dates.',
    'If the department asks for a specific internship project, verify whether this separate academic case study is acceptable. The supplied certificate does not name this library project.',
    'Add genuine details of actual training activities only if personally verified. Do not describe the diagrams or expected tests as screenshots of a running model.',
    'Print all pages on one side only, use a colour print for the certificate page and spiral-bind the report.',
    'Submit by 16 November 2026: Section 1 to Dr. Zeeshan Ali Siddiqui; Section 2 to Dr. Sakshi Srivastava. Confirm your section before submission.',
]: y=para(c,'[  ]  '+text,y)-12
c.showPage(); c.save()

# ---------- Editable DOCX with matching content and manual page breaks ----------
doc=Document(); sec=doc.sections[0]
sec.page_height=Inches(11.69); sec.page_width=Inches(8.27)
sec.top_margin=Inches(.85); sec.bottom_margin=Inches(.7)
sec.left_margin=Inches(.9); sec.right_margin=Inches(.9)
styles=doc.styles
for name in ['Normal','Title','Heading 1']:
    st=styles[name]; st.font.name='Times New Roman'; st.font.size=Pt(12)
    st.paragraph_format.line_spacing=1.0
    st.paragraph_format.space_after=Pt(7)
styles['Heading 1'].font.bold=True
styles['Heading 1'].paragraph_format.space_before=Pt(0)
styles['Title'].font.bold=True

def addp(txt='', center=False, bold=False, italic=False):
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    r=p.add_run(txt); r.bold=bold; r.italic=italic
    return p

def breakpage(): doc.add_page_break()
for s in ['INDUSTRIAL TRAINING REPORT','on','“'+TITLE+'”','by',STUDENT+' [ROLL NUMBER TO FILL]','Submitted in partial fulfillment of the requirements for the award of the degree','of','BACHELOR OF TECHNOLOGY','in','COMPUTER SCIENCE & ENGINEERING','from','EWB EDUTECH PRIVATE LIMITED (EWB Courses)']:
    addp(s,center=True,bold=True)
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run().add_picture(str(logo_img),width=Inches(1.25))
for s in ['Submitted to','DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING','FACULTY OF ENGINEERING & TECHNOLOGY','UNIVERSITY OF LUCKNOW, LUCKNOW','November 2026']:addp(s,center=True,bold=True)
prelim_section=doc.add_section(WD_SECTION_START.NEW_PAGE)
prelim_section.footer.is_linked_to_previous=False
prelim_section.footer.paragraphs[0].alignment=WD_ALIGN_PARAGRAPH.CENTER
prelim_section.footer.paragraphs[0].add_run('')
pgtype=OxmlElement('w:pgNumType');pgtype.set(qn('w:fmt'),'lowerRoman');pgtype.set(qn('w:start'),'1')
prelim_section._sectPr.append(pgtype)
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE')
prelim_section.footer.paragraphs[0]._p.append(field)
addp('DECLARATION',center=True,bold=True)
for s in [
'I, Mayank Kumar, declare that this report titled “Library Book Management: A Python-Based Design” is a theory-based academic case study prepared for the B.Tech CSE summer training submission. The concepts, illustrative records, diagrams and calculations are presented as a proposed design; no working software, deployment or empirical evaluation is claimed.',
'The attached certificate is the authentic student-supplied document evidencing completion of a one-month Python Programming internship. The certificate does not identify this library topic as the assigned internship project. The library scenario should be described as completed internship work only if supported by separate evidence.',
'The fictional book, copy, member and loan IDs in this report are used solely to explain the design. No confidential or restricted company information is disclosed. References and supplied documents are acknowledged at the end of the report.'] :addp(s)
for s in ['Signature: ________________________','Name: Mayank Kumar','Roll No.: [TO FILL]','Section: [TO FILL]','Date: [TO FILL]']:addp(s)
breakpage();addp('TRAINING / INTERNSHIP CERTIFICATE',center=True,bold=True)
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run().add_picture(str(cert_img),width=Inches(6.4))
addp('Colour reproduction of the student-provided original certificate. Issued 15 July 2026; it states a one-month Python Programming internship.',italic=True)
breakpage()
for title,content in [
('ABSTRACT',[
'This report describes a proposed library book management system using beginner-level Python concepts. The case study addresses the difficulty of tracking physical book copies, registered members and issue-return transactions consistently in a small library. The focus is on process design, not on producing a working model.',
'The suggested data model separates a book title from its physical copies and records every borrowing event as a loan. The key rule is that one physical copy may have at most one active loan. Issue, return, search, validation and summary reporting are explained using flowcharts, fictional tables, manually worked examples and an illustrative chart.',
'The supplied internship certificate confirms one-month Python Programming training for Mayank Kumar. It does not name the library case study. Therefore, the present design is treated as an academic application of Python-related ideas rather than a verified project delivered to the training provider.',
'Keywords: Python, library management, catalogue, circulation, conceptual design, case study.'
]),('ACKNOWLEDGEMENT',[
'I thank the Department of Computer Science and Engineering, Faculty of Engineering & Technology, University of Lucknow, for providing the format and opportunity to prepare a summer internship report.',
'I acknowledge EWB EDUTECH PRIVATE LIMITED / EWB Courses for the Python Programming internship documented by the attached completion certificate. The concepts discussed here are connected to the subject area of that training; the particular library case study is a separate academic design.',
'I also thank the faculty member reviewing this report for guidance and feedback. Any mistakes in the explanatory examples or calculations remain my responsibility.',
'Note to student before submission: revise this acknowledgement to reflect the people who actually supported your work.'
])]:
    addp(title,center=True,bold=True)
    for t in content:addp(t)
    breakpage()
addp('TABLE OF CONTENTS',center=True,bold=True)
for title,n in entries:
    p=addp(f'{title}  ..........  {n}')
    p.paragraph_format.space_after=Pt(0)
    p.paragraph_format.line_spacing=1.0
    for run in p.runs:run.font.size=Pt(9)
breakpage();addp('LIST OF TABLES',center=True,bold=True)
for i,p in enumerate(pages,1):
    if p['table']:addp(f"{p['note']}  ..........  {i}")
breakpage();addp('LIST OF FIGURES',center=True,bold=True)
for i,p in enumerate(pages,1):
    if p['flow'] or p['fig']:addp(f"{p['note']}  ..........  {i}")
main_section=doc.add_section(WD_SECTION_START.NEW_PAGE)
main_section.footer.is_linked_to_previous=False
main_section.footer.paragraphs[0].alignment=WD_ALIGN_PARAGRAPH.CENTER
pgtype=OxmlElement('w:pgNumType');pgtype.set(qn('w:fmt'),'decimal');pgtype.set(qn('w:start'),'1')
main_section._sectPr.append(pgtype)
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE')
main_section.footer.paragraphs[0]._p.append(field)
for i,d in enumerate(pages,1):
    addp(d['title'],bold=True)
    for s in d['paras']: addp(s)
    for s in d['bullets']: addp('•  '+s)
    if d['table']:
        rows=d['table']; t=doc.add_table(rows=0,cols=len(rows[0]));t.style='Table Grid';t.alignment=WD_TABLE_ALIGNMENT.CENTER
        for row in rows:
            cells=t.add_row().cells
            for cell,text in zip(cells,row): cell.text=str(text)
    if d['flow']: addp('  →  '.join(d['flow']),center=True,bold=True)
    if d['fig']:
        # Extract only the original illustrative vector chart from the finished PDF.
        pdf_view=pymupdf.open(pdf_path)
        chart_page=pdf_view[8+i-1]
        chart_crop=chart_page.get_pixmap(matrix=pymupdf.Matrix(2,2),clip=pymupdf.Rect(80,245,525,505),alpha=False)
        chart_img=OUT/'illustrative_chart.png';chart_crop.save(chart_img)
        p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(chart_img),width=Inches(5.9))
        pdf_view.close()
    if d['note']: addp(d['note'],italic=True)
    breakpage()
addp('REFERENCES',bold=True)
for j,r in enumerate(refs,1):addp(f'{j}. {r}')
breakpage();addp('APPENDIX A: GLOSSARY',bold=True)
for term,meaning in [('Book','Catalogue description of a title or edition.'),('Copy','One physically loanable item belonging to a book record.'),('Member','Registered person to whom a copy may be issued.'),('Loan','Transaction that links a member and copy over time.'),('Active loan','Loan with no return date.'),('Availability','Whether a usable copy has no active loan.'),('Validation','Checking input and state before updating records.'),('Conceptual design','Proposed behaviour without claiming an implementation.')]:addp(f'{term}: {meaning}')
breakpage();addp('APPENDIX B: SUBMISSION CHECKLIST',bold=True)
for s in ['Fill roll number, section, date and signature.','Check acceptance of one-month certificate for four-to-six-week requirement; exact dates are not shown.','Confirm that a separate academic case study is acceptable.','Do not present proposed tests as executed tests or diagrams as software screenshots.','Print single-sided, certificate in colour, and spiral-bind.','Submit by 16 November 2026 to the faculty member designated for your section.']:addp('☐  '+s)
# The editable file uses Roman numbering for preliminaries and restarts at 1
# for the main report; verify layout in the chosen word processor before printing.
doc.save(OUT/'Library_Book_Management_Internship_Report.docx')
for temporary_image in (cert_img, logo_img, OUT/'illustrative_chart.png'):
    temporary_image.unlink(missing_ok=True)
print(f'Created {pdf_path} and DOCX; main pages={len(pages)} total PDF pages={8+len(pages)+3}')

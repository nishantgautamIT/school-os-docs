from pathlib import Path
import json
import argparse

base = Path(__file__).parent
modules = []
def add(id, group, title, desc, persona, stage, steps, tables, endpoints, guard, preview, action, result):
    modules.append(dict(id=id,group=group,title=title,description=desc,persona=persona,stage=stage,
        steps=[dict(title=s[0],layer=s[1],detail=s[2]) for s in steps],tables=tables,endpoints=endpoints,
        guard=guard,preview=preview,action=action,result=result))

add('overview','Start here','Platform overview','One connected school platform, with a small initial deployment and clear boundaries for growth.','School administrator','Foundation',[
 ('React web app','Frontend','Staff, parents and students use role-specific screens. Static assets can be served independently of the API.'),
 ('Node / NestJS API','Backend','Authenticate the session, resolve school membership and invoke the relevant business module.'),
 ('PostgreSQL transaction','Database','Authoritative records, tenant isolation, business constraints and applicable balanced ledger postings.'),
 ('Durable job + outbox','Worker','Run imports, PDFs, images, ZIPs and AI away from ordinary request handling. Retry external effects with idempotency.'),
 ('S3 + providers','External','Private media, message delivery and payments use replaceable adapters. Their statuses are reconciled.'),
 ('Role-specific result','Frontend','Show completed records or job status. Scale API, workers and database independently when measured demand requires it.')],
 ['tenant-scoped modules','PostgreSQL records + outbox','private S3 objects'],['/v1/* → authenticated module handlers','/v1/jobs/:id → job status'],
 'A modular monolith first. No measured capacity guarantee. Keep CPU-heavy work in workers and database transactions short.',
 'dashboard','Open operations summary','The dashboard shows a combined operations snapshot using illustrative school data.')

add('identity','School foundation','Identity & permissions','One account, verified memberships, and precise staff, parent and student access.','School administrator','Foundation',[
 ('Sign in','Frontend','User completes the established authentication flow; the browser receives a secure session.'),
 ('Resolve membership','Backend','Derive tenant and role from the authenticated account. Never trust a school ID from a form alone.'),
 ('Check resource access','Backend','Verify class assignments, guardian links or accounting roles in addition to the tenant.'),
 ('Scoped transaction','Database','Set tenant context transaction-locally; enforce RLS with a restricted runtime role.'),
 ('Audit + response','Database','Record privileged changes and return only permitted data. Keep migration privileges separate.')],
 ['users','memberships','guardian_links','audit_events'],['POST /v1/auth/session','GET /v1/me/memberships','PATCH /v1/memberships/:id'],
 'Cross-school access returns 403; a parent sees only children with verified links. Support impersonation requires explicit audited access.',
 'roles','Review access','A sample role review is recorded. No real account permissions were changed.')

add('students','School foundation','All students & profiles','A searchable student dashboard with combined filters, individual profiles, verified guardians and academic-year history.','School administrator / assigned teacher','Foundation',[
 ('Search and combine filters','Frontend','Choose academic year, class, section, admission state, attendance band and fee state; search by name or admission number. Preserve filters when opening and returning from a profile.'),
 ('Authorise then filter records','Backend','School admins see own-tenant students; teachers see assigned classes/subjects; parents see verified children. Apply scope before filters, counts, sorting and pagination. Validate filter fields and cap page size.'),
 ('Save identity and enrolment','Database','Keep student identity stable; add year-specific enrolment instead of overwriting prior years.'),
 ('Verify guardian invitation','Worker','Queue the invitation through the authorised channel. A pending invitation is not verified access.'),
 ('Open scoped student profile','Frontend','Show permitted identity, guardians, attendance, homework, published report cards, library, fee records and history. Field-level restrictions still apply; preserve previous academic years. Import preview reports invalid and duplicate rows.')],
 ['students','guardians','guardian_links','enrolments','student_profile_projections'],['GET /v1/students?year=&class=&section=&status=&attendance=&fees=&search=&sort=&cursor=','GET /v1/students/:id/profile','GET /v1/students/:id/history','POST /v1/students/import-preview','POST /v1/students','POST /v1/guardian-invitations'],
 'Filtering is not authorisation. Enforce tenant, assignment/guardian scope and field permissions on rows, counts, profiles and exports. A name or phone match cannot grant access to another child.',
 'students','Validate import','The sample import has 3 valid records and 1 duplicate admission number to review.')

add('academics','School foundation','Classes, staff & calendar','Academic years, sections, subjects, teacher assignments and school holidays.','School administrator','Foundation',[
 ('Configure school year','Frontend','Define dates, classes, sections, subjects and holiday exceptions in Asia/Kolkata.'),
 ('Check dates and roles','Backend','Validate ranges, unique sections and allowed teaching assignments.'),
 ('Save academic structure','Database','Scope class and teacher relationships to the school and academic year.'),
 ('Propagate calendar change','Worker','Invalidate affected draft schedules and notify staff to review conflicts.'),
 ('Show assignments','Frontend','Teachers see their permitted classes. Calendar changes do not rewrite already recorded lessons.')],
 ['academic_years','classes','sections','subjects','teacher_assignments','calendar_days'],['POST /v1/academic-years','PUT /v1/teacher-assignments','PATCH /v1/calendar'],
 'Keep event dates, teaching dates and upload dates distinct. Preserve historical enrolment and delivered-lesson records.',
 'academics','Validate calendar','The sample calendar has no overlapping term dates. One draft plan needs review after a holiday change.')

add('admissions','School foundation','Admissions','Track an enquiry through review, approval and student enrolment without duplicate entry.','Admissions staff','Core',[
 ('Receive application','Frontend','Record the enquiry, requested class and parent contact with required notices.'),
 ('Review checklist','Backend','Check authorised access and completion of the school-defined document checklist.'),
 ('Approve admission','Database','Create student and enrolment once, with a link back to the application.'),
 ('Create authorised dues','Backend','If applicable, invoke the fee service using the approved school schedule; do not collect into the SaaS company account.'),
 ('Confirm to family','Worker','Queue an approved message and invitation. Keep fee, application and message statuses separate.')],
 ['applications','application_documents','students','enrolments'],['POST /v1/applications','POST /v1/applications/:id/approve'],
 'Approval retries cannot create duplicate students or invoices. Private documents use signed, permission-checked access.',
 'admissions','Review application','The illustrative application is ready for a staff decision; no student record has been created.')

add('attendance','Daily school','Attendance','Fast classroom marking with corrections, parent notices and catch-up triggers.','Teacher','Core',[
 ('Mark the assigned class','Frontend','Select a school-local date and mark each student present, absent or on approved leave.'),
 ('Validate teacher + version','Backend','Check class assignment and handle simultaneous updates or retried saves.'),
 ('Commit attendance','Database','Enforce one daily record per enrolled student; retain correction history.'),
 ('Create notice / catch-up event','Worker','Queue school-policy notices and a reviewed catch-up task. Notification failures do not undo attendance.'),
 ('Confirm class and parent views','Frontend','Show saved attendance and the relevant child view without exposing the whole class.')],
 ['attendance','attendance_changes','enrolments','outbox_events'],['PUT /v1/classes/:id/attendance/:date','POST /v1/attendance/:id/corrections'],
 'Use dates in the school timezone. A stale update must resolve a conflict rather than overwrite an unexplained correction.',
 'attendance','Save attendance','Attendance saved in this demo. An absent student now has a catch-up task; no parent message was sent.')

add('fees','Daily school','School fees & receipts','Student dues, partial payments, allocations and audited corrections.','School accountant','Core',[
 ('Issue approved schedule','Frontend','Generate student dues from the accepted fee schedule and concessions.'),
 ('Create invoice + posting','Backend','Call the accounting posting service with exact amounts and a unique posting reference.'),
 ('Receive payment evidence','External','Validate a signed provider event or enter authorised cash/bank evidence.'),
 ('Allocate and reconcile','Database','Deduplicate events, allocate funds to dues and record overpayments/refunds separately.'),
 ('Receipt and parent balance','Frontend','Expose the verified receipt and remaining balance; message delivery does not determine paid status.')],
 ['student_invoices','payments','allocations','journal_entries','refunds'],['POST /v1/student-invoices','POST /v1/webhooks/payments','GET /v1/children/:id/fees'],
 'School fees belong to the school accounting entity. A browser success screen is not payment verification.',
 'fees','Review reconciliation','The sample payment is allocated to October dues. A ₹500 difference remains flagged for review.')

add('learning','Daily school','Homework, assessment & reports','Connect assigned work, teacher feedback and school-approved report formats.','Teacher','Core',[
 ('Assign work or assessment','Frontend','Select class, subject, due date, rubric and approved resources.'),
 ('Authorise teaching scope','Backend','Validate the teacher assignment and audience.'),
 ('Store submissions and results','Database','Separate submission/completion from assessed understanding; preserve revisions.'),
 ('Teacher review + release','Backend','Publish results only after the required review; generate reports as background jobs.'),
 ('Child and parent access','Frontend','Show only the linked child’s published feedback and next step.')],
 ['assignments','submissions','assessments','results','report_versions'],['POST /v1/assignments','POST /v1/results/:id/publish','POST /v1/report-jobs'],
 'No AI-generated grade is automatically final. Do not make all-class marks visible to a parent.',
 'learning','Publish reviewed task','The sample assignment is published for Class 6-A. Published feedback remains teacher-controlled.')

add('syllabus','Daily school','AI syllabus planning','Turn a reviewed syllabus into a feasible teaching calendar and track actual coverage.','Teacher','AI pilot',[
 ('Confirm source and topics','Frontend','Upload authorised material and confirm extracted topics, durations and teaching constraints.'),
 ('Reserve AI allowance','Backend','Check entitlement and atomically reserve the school’s token/spend budget.'),
 ('Generate draft content','Worker','Call an eligible staff-workflow provider, validate structured output and reconcile actual usage.'),
 ('Schedule deterministically','Backend','Fit available periods, holidays, dependencies and revision; show capacity shortfalls.'),
 ('Teacher approve + version','Database','Save a reviewed plan. Maintain actual taught coverage separately.'),
 ('Publish relevant plan','Frontend','Share class/subject information and approved learning support with families.')],
 ['curriculum_documents','topics','plan_versions','scheduled_lessons','coverage_updates','ai_usage'],['POST /v1/plans/generate','POST /v1/plans/:id/approve','POST /v1/coverage'],
 'LLM suggestions do not guarantee calendar feasibility. Provider age/eligibility terms must be confirmed before use.',
 'syllabus','Validate plan','The sample plan fits 28 teaching periods, including 4 revision periods. It is ready for teacher approval.')

add('messaging','Daily school','Bulk parent messaging','Send a notice to all school parents together, an academic year, a class or selected parents; preview the audience before delivery.','School administrator / authorised teacher','Core',[
 ('Choose all parents or a group','Frontend','School admin selects all school parents, academic year, class/section, event audience or selected guardians. Teachers only receive their assigned audiences.'),
 ('Verify facts + language + consent','Backend','Keep names, amounts and dates as trusted template fields. Store English/Hindi reviewed content versions and parent language preferences. An AI translation is a draft until staff approve it. Check channel preferences and staff authority.'),
 ('Save recipient snapshot','Database','Deduplicate verified guardians within this tenant; version approved content and recipient/channel snapshot. Display eligible contacts, excluded channels and estimated usage before approval.'),
 ('Deliver from outbox','Worker','Respect quiet hours, quotas, provider templates and idempotency. Retry transient failures.'),
 ('Reconcile delivery and keep history','External','Retain sender/approver, approved version, audience, schedule, channel attempts, failures and timestamps. Provider delivered/read, portal read and task completion are distinct states. Corrections preserve earlier versions.')],
 ['announcements','announcement_versions','announcement_translations','recipient_snapshots','delivery_attempts','preferences','announcement_reads'],['POST /v1/campaigns/preview','POST /v1/campaigns/:id/approve','GET /v1/campaigns','GET /v1/campaigns/:id/delivery','GET /v1/me/notices','POST /v1/webhooks/messages'],
 'All-school broadcasts require school-admin permission. Teachers stay within assigned audiences. Every parent gets a private delivery; recipient contacts are never exposed to other parents. Read receipts do not prove task completion.',
 'messaging','Preview broadcast','A sample bulk notice is previewed. No actual message is sent.')

add('inventory','Resources & finance','Inventory & stock','Trace stock from receipt through locations, consumption, returns and stock checks.','Storekeeper','Required',[
 ('Select item and location','Frontend','Review on-hand quantity, unit and proposed movement.'),
 ('Validate source + units','Backend','Check the approved receipt/request and exact unit conversion.'),
 ('Lock and record movement','Database','Prevent concurrent over-issue; append the movement and update the controlled balance projection.'),
 ('Post applicable finance','Backend','Invoke the authorised valuation/expense rule inside the same transaction when needed.'),
 ('Queue shortage follow-up','Worker','Create a reviewed replenishment suggestion; do not order or silently adjust stock.')],
 ['items','locations','stock_movements','stock_balances','stock_counts'],['POST /v1/stock-movements','GET /v1/stock-balances','POST /v1/stock-counts'],
 'History is corrected through authorised linked adjustments. A stock-count scan must not automatically check in a library loan.',
 'inventory','Record sample issue','A sample issue of 5 notebooks is recorded locally; the demo on-hand count changes from 120 to 115.')

add('assets','Resources & finance','Equipment & custody','Know which unit is with whom, in what condition, and under which financial policy.','Storekeeper','Required',[
 ('Scan tagged unit','Frontend','Find an individual laptop/projector/instrument by its school tag.'),
 ('Check availability and role','Backend','Ensure it is usable and the receiving custodian is authorised.'),
 ('Record custody transaction','Database','Append assignment/return/transfer with condition and acknowledgement.'),
 ('Maintain financial policy','Backend','Separate physical custody from capitalisation/depreciation and authorised disposal.'),
 ('Update reminders','Worker','Notify the custodian about due return or approved maintenance tasks.')],
 ['resource_units','asset_details','custody_history','maintenance_records'],['POST /v1/assets/:id/assign','POST /v1/assets/:id/return','GET /v1/assets/:id/history'],
 'Assigning a device does not automatically expense it. Lost/damaged disposition needs an authorised decision.',
 'assets','Assign equipment','Projector PRJ-014 is assigned to the sample teacher until 16 October; this is local demonstration state.')

add('library','Resources & finance','Library & circulation','One title, many physical copies, each with an accession identity and loan history.','Librarian','Required',[
 ('Scan copy + borrower','Frontend','Use a unique accession/barcode, not just the title ISBN.'),
 ('Check circulation rules','Backend','Verify borrower, limits, copy condition, hold eligibility and calendar-based due date.'),
 ('Lock and open one loan','Database','Commit at most one active loan per copy and record current custody.'),
 ('Create return task','Worker','Publish a due-date action for the verified family. Charges require an approved separate policy.'),
 ('Reconcile return / stock check','Backend','Close the loan on authorised return, preserve ownership and resolve exceptions.')],
 ['book_editions','book_copies','loans','holds','circulation_policies'],['POST /v1/library/loans','POST /v1/library/loans/:id/return','GET /v1/library/catalogue'],
 'A book on loan is still owned by the school. Loans do not automatically create a sale or reduce its financial value.',
 'library','Issue copy','Copy LIB-001 is on loan to the sample borrower. Available copies decrease; owned copies stay unchanged.')

add('procurement','Resources & finance','Procurement & approvals','Connect department requests, budgets, suppliers, orders and partial/rejected deliveries.','School administrator','Required',[
 ('Raise department request','Frontend','Choose required items, quantities, need-by date and justification.'),
 ('Budget and approval check','Backend','Check the accounting entity/cost centre, approval limits and commitments.'),
 ('Order selected quotation','Database','Record authorised supplier terms and ordered quantities without treating the order as paid.'),
 ('Inspect partial delivery','Backend','Keep accepted, rejected and outstanding quantities distinct; tag/accession accepted resources once.'),
 ('Match bill and payment','Backend','Compare invoice to order/receipts, resolve tolerances and invoke accounting/reconciliation.')],
 ['purchase_requests','quotes','purchase_orders','goods_receipts','supplier_invoices'],['POST /v1/purchase-requests','POST /v1/purchase-orders/:id/approve','POST /v1/goods-receipts'],
 'Receipt retries cannot duplicate books or ledger postings. Mismatched invoices remain exceptions instead of silently changing the order.',
 'procurement','Review receipt match','The sample order received 18 accepted and 2 rejected copies. The supplier bill needs review before payment.')

add('accounting','Resources & finance','Accounting & reconciliation','An authoritative posting service with balanced entries, allocations, reversals and period close.','School accountant','Required',[
 ('Submit source document','Frontend','Review invoice/receipt/payment, accounting entity, period and exact amounts.'),
 ('Validate posting policy','Backend','Check role, approved account mappings, source version and open period.'),
 ('Post balanced journal','Database','Atomically enforce debit=credit, unique posting reference and immutable posted entries.'),
 ('Allocate / reconcile','Backend','Link payables, receivables and bank evidence. Track advances and refunds distinctly.'),
 ('Review and close period','Frontend','Generate reports in jobs; accountant checks source/subledger agreement before locking the period.')],
 ['accounts','journal_entries','journal_lines','allocations','reconciliations','fiscal_periods'],['POST /v1/accounting/postings','POST /v1/reconciliations','POST /v1/periods/:id/close'],
 'A balanced trial balance alone does not prove correct accounting. Tax/reporting policies require institution-specific accountant review.',
 'accounting','Check journal balance','Sample journal totals agree at ₹7,200 debit and credit. Source and reconciliation checks remain required.')

add('gallery','Events & media','Event galleries','An event/date home for approved school photos, with private storage and scoped publication.','School administrator','Required',[
 ('Create event + audience','Frontend','Choose event dates, campus/year, cover and approved parent/class audience.'),
 ('Authorise upload','Backend','Reserve quota and issue a short-lived upload permission for a server-generated object key.'),
 ('Upload directly to S3','External','Send binary files to private object storage; never place storage credentials in the browser.'),
 ('Verify + create thumbnails','Worker','Check ownership, type, size and image dimensions; process in bounded jobs.'),
 ('Review and publish','Database','Publish approved media only. Save event dates separately from upload timestamps.'),
 ('Browse authorised album','Frontend','Serve lazy-loaded thumbnails to the permitted audience; public publication is a separate decision.')],
 ['school_events','event_audiences','media_assets','media_versions'],['POST /v1/events','POST /v1/media/upload-intents','POST /v1/events/:id/publish'],
 'S3 prefixes are organisational labels, not access control. Private gallery and public marketing consent are distinct.',
 'gallery','Preview parent album','The approved sample event album is available in the parent preview. No real media was uploaded.')

add('packages','Events & media','Expiring download packages','Share an event ZIP with the right parents through a revocable, expiring application link.','School administrator','Required',[
 ('Select approved event media','Frontend','Choose audience, compressed/original quality and share expiry.'),
 ('Build versioned package','Worker','Stream a bounded ZIP, record checksum/file list/size and upload privately. Reuse it for identical audiences.'),
 ('Create parent-specific grants','Database','Store hashed opaque tokens, audience, expiry and revocation. Send only after the package is ready.'),
 ('Parent opens app link','Backend','Verify login, guardian/event membership, current permission, expiry and package state.'),
 ('Mint temporary download','External','Issue a short-lived signed S3 URL no longer than the remaining share lifetime.'),
 ('Expire / revoke / clean up','Worker','Stop new authorisations and apply package retention independently of original gallery retention.')],
 ['event_packages','package_files','share_grants','access_audit','delivery_attempts'],['POST /v1/events/:id/packages','POST /v1/packages/:id/shares','GET /v1/share/:token','POST /v1/shares/:id/revoke'],
 'Already issued object URLs can remain valid briefly. A downloaded file cannot be recalled. A link click does not prove a full download.',
 'packages','Create demo package','A demo ZIP record is ready and a 24-hour parent grant is previewed. No real archive or message was created.')

add('parent','Family & learning','Parent dashboard & inbox','A dashboard for verified children: school notices, homework, attendance, fees, published results, library and event actions.','Parent','Core',[
 ('Open dashboard and choose child','Frontend','Show the parent notice inbox and a child switcher containing only verified links. Display homework, attendance, fees, published results, library and event tasks.'),
 ('Resolve guardian access','Backend','Verify links and query only permitted fee, library, form, event and learning tasks.'),
 ('Read notices and source records','Database','Load the approved English/Hindi notice version for parent preference, with an explicit fallback if unavailable. Persist per-parent read history. Task completion comes from its source module, not an LLM or read receipt.'),
 ('Perform the relevant action','Backend','Route consent, review or payment to that module with its own permission and validation.'),
 ('Refresh and digest','Worker','Update task projections and queue preferences-aware reminders without duplicating completed tasks.')],
 ['guardian_links','tasks','task_sources','preferences','announcement_reads'],['GET /v1/me/dashboard','GET /v1/me/notices','POST /v1/me/notices/:id/read','GET /v1/me/family-actions','GET /v1/children/:id','POST /v1/tasks/:id/actions'],
 'Payments, borrowing and media permission remain separate source records. Read-only parents cannot alter academic results.',
 'parent','Review consent','A sample event consent is marked reviewed locally. No school permission record was updated.')

add('catchup','Family & learning','Absence catch-up','Teacher-approved packs based on what was actually taught, shared with absent children.','Teacher','Pilot',[
 ('Attendance creates candidate','Database','Find absence and actual delivered lesson/assignment references.'),
 ('Assemble class-session pack','Worker','Reuse reviewed resources rather than generate new AI text per child.'),
 ('Teacher reviews','Frontend','Confirm summary, worksheet and intended work; correct the pack before release.'),
 ('Assign permitted children','Backend','Check enrolment/audience and create the relevant family task.'),
 ('Submit and review','Frontend','Record work completion separately from teacher judgement of understanding.')],
 ['attendance','coverage_updates','catchup_packs','assignments','submissions'],['POST /v1/catchup-packs','POST /v1/catchup-packs/:id/approve'],
 'An unrecorded delivered lesson should prompt teacher input instead of presenting an invented summary.',
 'catchup','Approve catch-up pack','The sample fractions catch-up pack is approved for the selected absence audience.')

add('resourceplanning','Family & learning','Resource-aware lessons','Check real school resources before a planned learning activity.','Teacher','Pilot',[
 ('Define lesson requirements','Frontend','Choose the approved activity, class size and required book/equipment/consumable quantities.'),
 ('Check live availability','Backend','Query available copies, custody and stock, excluding already reserved resources.'),
 ('Reserve atomically','Database','Prevent conflicting reservations; preserve consumable versus reusable rules.'),
 ('Review alternatives / shortage','Frontend','Show grouping choices and shortages; AI suggestions require staff review.'),
 ('Create approved request','Backend','Prepare a budget-controlled procurement request without autonomously ordering or charging parents.')],
 ['lesson_requirements','reservations','stock_balances','book_copies','purchase_requests'],['POST /v1/lessons/:id/resource-check','POST /v1/resource-reservations'],
 'Availability must be checked again when reserving. An AI draft cannot override a purchasing approval limit.',
 'resourceplanning','Check resources','18 of 30 required reading copies are available. Review rotating groups or request 12 more copies.')

add('reading','Family & learning','Borrow–read–return','Guide reading using available school books and human-reviewed activities.','Student','Pilot',[
 ('Browse approved choices','Frontend','Filter by language/interest and show actual local availability.'),
 ('Reserve eligible copy','Backend','Use circulation policy and a fair hold queue; no duplicate competing allocations.'),
 ('Borrow via librarian','Database','Open the authoritative copy loan; recommendation does not itself issue a book.'),
 ('Reflect on reading','Frontend','Submit a short school-produced/licensed reflection or drawing.'),
 ('Review and return','Backend','Teacher reviews work; librarian closes the loan. Update parent due tasks separately.')],
 ['book_editions','holds','loans','reading_reflections'],['GET /v1/reading/choices','POST /v1/library/holds','POST /v1/reading/reflections'],
 'A returned book does not prove comprehension. Recommendations and quizzes are existing product categories, not established unique features.',
 'reading','Reserve a book','A sample hold is placed for an available title. Librarian checkout is still required.')

add('homeprompts','Family & learning','Parent learning prompts','A short, practical conversation connected to the child’s current lesson.','Parent','Pilot',[
 ('Select taught topic','Database','Use the recorded lesson and teacher-selected learning goal.'),
 ('Draft class-level prompt','Worker','Use a template or eligible staff AI workflow; avoid child-specific prompts when not needed.'),
 ('Teacher approve language','Frontend','Review the original and translation, with a simple example/check cue.'),
 ('Deliver chosen digest','Worker','Send through the family’s preferred channel and timing.'),
 ('Collect optional feedback','Frontend','Record usefulness feedback without interpreting it as verified attainment.')],
 ['learning_prompts','approval_versions','language_preferences','feedback'],['POST /v1/learning-prompts','POST /v1/learning-prompts/:id/approve'],
 'Protect dates/facts in translations. Parents are not required to become tutors; self-reported completion is not assessed learning.',
 'homeprompts','Show conversation prompt','The sample parent prompt is displayed in English with an optional reviewed Hindi version.')

add('doubts','Family & learning','Questions & doubt sessions','A topic-linked question inbox and reviewed answers before autonomous student tutoring.','Student','Pilot',[
 ('Submit private question','Frontend','Link a question to the subject/topic and assigned teacher.'),
 ('Validate scope','Backend','Check enrolment, allowed attachments and staff response ownership.'),
 ('Group for teacher review','Worker','Suggest duplicate groups or draft a staff response under eligible provider terms.'),
 ('Answer or schedule session','Frontend','Teacher publishes the answer or books an agreed doubt session.'),
 ('Share anonymised FAQ','Backend','Share only reviewed class answers; preserve private question visibility.')],
 ['questions','question_groups','teacher_answers','doubt_sessions'],['POST /v1/questions','POST /v1/questions/:id/answers','POST /v1/doubt-sessions'],
 'Student-facing AI is a future eligibility/evaluation gate. The present workflow never promises instant unreviewed answers.',
 'doubts','Submit question','Your sample question is queued for the assigned teacher; no AI answer is generated.')

add('portfolios','Family & learning','Progress & portfolios','Teacher-verified evidence of learning across terms, visible to the family.','Parent','Later',[
 ('Select work evidence','Frontend','Teacher attaches a permitted sample and rubric/learning-goal reference.'),
 ('Check audience and rights','Backend','Validate the child, teacher scope and media visibility.'),
 ('Store versioned feedback','Database','Preserve feedback revisions and assessment context.'),
 ('Publish to family','Backend','Release approved evidence and a useful next action.'),
 ('Review goal progress','Frontend','Show human-reviewed evidence, not an opaque automatically invented proficiency score.')],
 ['portfolio_entries','rubrics','feedback_versions','media_assets'],['POST /v1/portfolio-entries','POST /v1/portfolio-entries/:id/publish'],
 'Portfolio media permissions are separate from public event photos. This category already exists in other apps.',
 'portfolios','View learning evidence','The sample work and teacher feedback are displayed for the linked child.')

add('kits','Family & learning','Class kit readiness','Prepare activities with supplies, school loans and clear family acknowledgements.','Parent','Later',[
 ('Teacher approves kit','Frontend','Define required materials, school-provided items and any reusable loans.'),
 ('Reserve available stock','Backend','Check real quantities and equipment custody.'),
 ('Create family checklist','Database','Separate school-provided items from family acknowledgements and optional purchases.'),
 ('Record issue or approved sale','Backend','Use stock/custody or sales/accounting rules as appropriate.'),
 ('Track readiness and return','Frontend','Display missing items, staff contact and due return tasks.')],
 ['kit_templates','kit_allocations','reservations','custody_history'],['POST /v1/kits','GET /v1/children/:id/kit-readiness'],
 'Do not turn every activity into mandatory in-app shopping. Lending and selling need different records and permissions.',
 'kits','Acknowledge checklist','The sample activity checklist is acknowledged; no order or payment was placed.')

add('meetings','Family & learning','Meetings & follow-through','Book a suitable slot and record agreed parent/teacher next actions.','Parent','Later',[
 ('Choose permitted staff slot','Frontend','Show available appointments for the linked child.'),
 ('Reserve slot transaction','Database','Prevent concurrent double booking and enforce teacher capacity.'),
 ('Prepare private context','Backend','Expose only authorised questions, evidence and relevant tasks.'),
 ('Confirm and remind','Worker','Send confirmation with cancellation/reschedule policy.'),
 ('Record follow-up','Frontend','Teacher and family review agreed actions and their true completion.')],
 ['meeting_slots','appointments','meeting_notes','followup_tasks'],['POST /v1/appointments','POST /v1/appointments/:id/reschedule'],
 'A meeting note is private. Prevent overbooking and define staff response expectations.',
 'meetings','Book demo slot','A sample appointment is reserved for 16 October at 3:30 PM IST; no live calendar was changed.')

add('clearance','Family & learning','Year-end obligations','Reconcile books, equipment, finance and paperwork with manual dispute resolution.','School administrator','Later',[
 ('Request current obligations','Backend','Read authoritative open loans, custody, approved charges and paperwork.'),
 ('Build scoped checklist','Database','Attach a resolution owner and distinguish disputed or unverified records.'),
 ('Parent/staff review','Frontend','Allow correction requests and supporting context.'),
 ('Resolve in source module','Backend','Return/correct/allocate through the original service rather than override a dashboard status.'),
 ('Refresh completion','Frontend','Show verified resolution with history. Keep educational-access decisions outside automatic checklist logic.')],
 ['obligation_views','disputes','loans','custody_history','allocations'],['GET /v1/children/:id/obligations','POST /v1/disputes'],
 'Unresolved records must not automatically exclude a child or impose penalties. School policy and authorised human review apply.',
 'clearance','Review discrepancy','The sample disputed charge has a staff resolution owner and remains open for review.')

add('accessibility','Family & learning','Accessible family experience','Text-first, mobile-friendly screens that work with realistic parent devices and languages.','Parent','Core',[
 ('Set family preferences','Frontend','Choose language, digest timing and low-data image mode.'),
 ('Save verified preference','Backend','Check family membership and protect shared-device session behaviour.'),
 ('Select compact content','Database','Read approved text and thumbnail versions; retain original facts.'),
 ('Deliver optimised assets','External','Fetch small thumbnails/packs, with explicit byte sizes and permitted downloads.'),
 ('Complete source action','Backend','Online financial/stock actions remain server-validated; offline reading is not offline authority.')],
 ['preferences','media_versions','approved_translations'],['PUT /v1/me/preferences','GET /v1/me/digest'],
 'Do not assume all parents own a personal smartphone. Validate screen-reader, keyboard, language and shared-device use.',
 'accessibility','Apply low-data mode','Low-data preview is enabled: text remains visible and image thumbnails are reduced in the demo.')

add('subscriptions','Business & operations','SaaS subscriptions','Your school-customer billing, entitlements and metered allowances.','Platform administrator','Core',[
 ('Choose school plan','Frontend','Display scope, usage limits and separately charged media/messages/AI.'),
 ('Create SaaS invoice','Backend','Keep your company’s subscription accounting separate from school fees.'),
 ('Verify payment/mandate','External','Use signed provider evidence or authorised manual reconciliation.'),
 ('Update entitlement state','Database','Deduplicate events, reconcile provider state and apply trial/active/grace/restricted/cancelled policy.'),
 ('Enforce server-side limits','Backend','Check API/jobs before spending; use atomic quota reservations and safe export/grace policy.')],
 ['saas_plans','school_subscriptions','saas_invoices','usage_meters'],['POST /v1/subscriptions','POST /v1/webhooks/saas-billing','GET /v1/usage'],
 'Illustrative prices are hypotheses. Never promise unlimited AI, messages or media delivery under a small fixed subscription.',
 'subscriptions','Review usage allowance','The sample school has 7.4 GB of a 10 GB illustrative storage allowance used. No payment was requested.')

add('reports','Business & operations','Reports, imports & exports','Reliable background reports with signed downloads and accepted opening balances.','School administrator','Required',[
 ('Select report/import scope','Frontend','Choose dates, entity, filters and output format with permission-aware previews.'),
 ('Validate request + quota','Backend','Check export privileges, bounded inputs and tenant scope.'),
 ('Run durable job','Worker','Stream/page data and produce a private result. Heavy jobs cannot monopolise the API.'),
 ('Reconcile report totals','Database','For accounting/opening imports, validate control totals and source links.'),
 ('Authorise result download','Frontend','Expose job status and a temporary download only after rechecking access.')],
 ['report_jobs','import_batches','validation_errors','private_exports'],['POST /v1/report-jobs','POST /v1/imports/preview','GET /v1/jobs/:id'],
 'Export permission can change during a job; recheck at download. Accountant sign-off is required for opening financial data.',
 'reports','Generate sample report','A sample report job is marked ready locally. The production job would create a private, scoped file.')

add('operations','Business & operations','Security, recovery & scaling','Protect school boundaries, recover records and grow only around measured bottlenecks.','Platform administrator','Foundation',[
 ('Observe scoped service health','Backend','Track latency, event-loop delay, DB queries, lock waits, queue age, memory and storage usage.'),
 ('Limit and isolate workloads','Backend','Bound pools/concurrency and apply tenant/job quotas so one import or gallery cannot starve others.'),
 ('Backup and restore','Worker','Encrypt offsite database backups; test metadata and object references with a documented restore.'),
 ('Scale the affected layer','Backend','Separate workers, increase/separate database or replicate stateless API when measurements justify it.'),
 ('Review access and recovery','Frontend','Audit privileged actions, patch dependencies and verify the intended recovery window.')],
 ['audit_events','operational_metrics','backup_runs','restore_checks'],['GET /v1/operations/health','POST /v1/restore-check-jobs'],
 'Example latency/capacity targets must be measured. A single initial VM has one failure domain and does not imply high availability.',
 'operations','Review recovery checks','The illustrative recovery checklist is displayed. No live backup or system operation was performed.')


add('isolation','School foundation','Tenant isolation & roles','A strict school boundary, plus role and resource permissions inside each tenant.','Platform / school administrator','Foundation',[
 ('Authenticated request','Frontend','The React client sends a session. A URL, subdomain or submitted tenant ID is never sufficient authority.'),
 ('Membership + permission guards','Backend','Node checks verified membership in the requested tenant, then role/permission and child/class/resource scope. Default deny.'),
 ('Scoped database transaction','Database','Use a restricted non-owner runtime role, forced row security where appropriate and transaction-local tenant context.'),
 ('Constraints + private resources','Database','Same-tenant foreign keys, one-source queries and scoped file keys prevent mixed-school records. Downloads recheck access.'),
 ('Scoped jobs + audit','Worker','Workers bind the tenant from the trusted stored job and validate access. Cache keys, exports and event recipients include tenant scope.'),
 ('Denied or permitted result','Backend','Cross-tenant requests return 403/404 under policy. Platform admins manage the control plane; tenant data access needs an explicit audited support grant.')],
 ['tenants','memberships','roles','role_permissions','guardian_links','teacher_assignments','support_grants','audit_events'],
 ['JWT/session → membership → permission → resource scope','BEGIN → SET LOCAL tenant context → scoped queries → COMMIT','GET /v1/tenants/:tenantId/students → verify membership first'],
 'The school admin has full functional access within their own tenant. Teachers are scoped by academic year, class/section and subject. No role can cross a tenant boundary without verified membership or an explicit audited support grant.',
 'isolation','Run access scenario','The local scenario displays the expected authorisation decision. No live backend request is made.')
modules.insert(1, modules.pop())

add('consent','Family & learning','Consent & forms','Versioned school forms and separate parent-only/public media permissions.','Parent','Core',[
 ('Staff publishes a scoped form','Frontend','Specify purpose, event/class audience, deadline and the version parents are reviewing.'),
 ('Verify parent and audience','Backend','Check tenant membership, guardian link and eligibility for this child/event.'),
 ('Record explicit response','Database','Store form version, response, actor and timestamp. Parent-only and public media permissions are separate.'),
 ('Update source task','Backend','Complete the corresponding action only after the response is accepted; preserve corrections/withdrawals.'),
 ('Apply publication rules','Worker','Recheck media permission before package creation and access. Invalidate affected grants when policy requires it.')],
 ['form_versions','form_responses','consent_records','event_audiences','share_grants'],
 ['GET /v1/me/forms','POST /v1/forms/:id/responses','POST /v1/consent/:id/withdraw'],
 'Viewing or opening a message is not consent. A photo-sharing decision does not grant unrelated public or AI-use permissions.',
 'consent','Review sample response','The sample parent-only response is reviewed locally. No live school consent record is changed.')
position=next(i for i,m in enumerate(modules) if m['id']=='parent')+1
modules.insert(position, modules.pop())


add('exams','Daily school','Exams & conduct','Plan exams within a school/year/class/subject scope and record who conducted them and who attended.','Exam coordinator','Required',[
 ('Define the exam scope','Frontend','Choose academic year, term, classes/sections, subjects and approved schedule.'),
 ('Validate related scopes','Backend','Verify the coordinator permission and that class, subject, candidates and exam belong to the same tenant/year.'),
 ('Assign exam responsibilities','Database','Record paper setter, reviewer, exam approver and invigilator assignments with effective dates.'),
 ('Conduct and record attempts','Frontend','An authorised invigilator records attendance/session evidence. Each student attempt is linked to the exam.'),
 ('Mark, review and release','Backend','Use assigned marking and result permissions. Retain conduct, attempt, correction and publication history.')],
 ['exams','exam_subjects','exam_candidates','exam_assignments','exam_sessions','exam_attendance','student_attempts'],
 ['POST /v1/exams','POST /v1/exams/:id/assignments','POST /v1/exams/:id/sessions','GET /v1/exams/:id/attempts'],
 'A teacher sees only authorised year/class/subject exams. Conducted-by staff and student attempts are different records; neither can be inferred from paper authorship.',
 'exams','Review conduct record','The sample conduct record identifies the invigilator, attended/absent students and marking assignment. No live exam was changed.')

add('papers','Daily school','Question papers & review','A versioned paper workflow recording who set, reviewed, approved and released each exam paper.','Assigned paper setter / reviewer','Required',[
 ('Assigned setter drafts','Frontend','Only an assigned teacher/setter creates the paper for the permitted subject, class and exam.'),
 ('Save private version','Database','Record author, revision, file hash, tenant/year/class/subject/exam and private object reference.'),
 ('Submit to assigned reviewer','Backend','Check permissions and lock the submitted version. Review comments reference that exact version.'),
 ('Approve or request changes','Frontend','Record reviewer, decision, timestamp and comments. A configured independent review requires a different actor.'),
 ('Lock and release securely','Backend','School admin or authorised exam approver locks the approved version. Distribution follows the exam release window.'),
 ('Append immutable history','Database','Retain setter/reviewer/approver/download events and replacement versions. Do not overwrite the earlier approved paper.')],
 ['paper_versions','paper_assignments','paper_reviews','paper_approvals','paper_release_rules','audit_events'],
 ['POST /v1/exams/:id/papers','POST /v1/papers/:id/submit','POST /v1/papers/:id/reviews','POST /v1/papers/:id/approve'],
 'Draft/review papers are private to authorised exam staff. Parents/students cannot download unreleased papers. Full school-admin access does not remove version history or audit controls.',
 'papers','Submit paper for review','Paper version 3 is submitted to the assigned reviewer. The exact author, version and submission event are retained in the sample history.')

add('reportcards','Daily school','Student, class & year reports','Report cards per student with class/section and academic-year views controlled by role.','Teacher / school administrator','Required',[
 ('Enter assigned subject marks','Frontend','Subject teachers enter marks/feedback only for their authorised exam/year/class assignments.'),
 ('Validate result inputs','Backend','Check ranges, rubric, absent/exempt states, weightings and allowed corrections.'),
 ('Calculate and version','Database','Store exact results and deterministic totals; keep calculation rule and source versions.'),
 ('Review and publish','Backend','Class teacher/exam reviewer checks the configured scope; school admin or authorised approver releases the report version.'),
 ('Serve permitted level','Frontend','School admin can see all tenant student/class/year views. Teachers see assigned scope; parents/students see only their own published reports.'),
 ('Audit changes and exports','Worker','Generate scoped PDFs and record who entered, reviewed, corrected, published or downloaded each report.')],
 ['result_entries','result_versions','grade_rules','report_versions','report_publications','audit_events'],
 ['PUT /v1/exams/:id/subject-results','GET /v1/students/:id/report-cards','GET /v1/classes/:id/results','GET /v1/academic-years/:id/results'],
 'A subject teacher cannot browse unrelated classes or silently edit published marks. Report-card release and later corrections require permission, reason and version history.',
 'reportcards','Review report scope','The sample report shows the selected student, class or academic-year view. Actual access is checked in Node and PostgreSQL.')

add('examaudit','Daily school','Exam history & audit','Trace paper authorship, review, conduct, attempts, marking and publication by actor and version.','School administrator / authorised exam staff','Required',[
 ('Open a scoped exam history','Frontend','Select tenant-authorised year, class, subject and exam.'),
 ('Authorise audit visibility','Backend','School admin can inspect own-school history; exam staff have only their assigned scope.'),
 ('Read append-only events','Database','Each event identifies actor, role/assignment snapshot, action, time, source version and change reason.'),
 ('Separate responsibilities','Frontend','Show setter, reviewer, approver, invigilator, marker and publisher independently, plus student attendance/attempts.'),
 ('Export with audit','Worker','Generate a permission-scoped history file and record the export. Do not expose paper contents in routine audit logs.')],
 ['audit_events','paper_versions','paper_reviews','exam_sessions','student_attempts','result_versions'],
 ['GET /v1/exams/:id/history','GET /v1/papers/:id/history','POST /v1/exams/:id/history-export'],
 'Ordinary school-admin permissions do not erase historical evidence. Preserve who did what, when, on which version, and why a result or paper changed.',
 'examaudit','Inspect audit trail','The sample history separates the setter, reviewer, approver, invigilator, marker and report publisher. No records are edited.')
new_exam_modules=modules[-4:]
del modules[-4:]
position=next(i for i,m in enumerate(modules) if m['id']=='learning')+1
modules[position:position]=new_exam_modules

add('productui','Design review','Product UI & design review','Review design drawbacks, role-specific navigation and the proposed admin, teacher and parent interface.','Product reviewer','Design direction',[
 ('Choose the role and task','Frontend','Start from school-admin operations, a teacher\'s daily class work, or a parent\'s child/actions view. Show only relevant navigation.'),
 ('Resolve permitted context','Backend','Server supplies tenant, academic-year and class/child scope. Hiding navigation is usability; authorisation remains server-side.'),
 ('Use consistent UI patterns','Frontend','Readable type, labelled forms, one primary action, predictable list/detail navigation and filters preserved when returning to a list.'),
 ('Design every workflow state','Frontend','Define loading, empty, validation-error, stale/conflict, offline and success states. Avoid a false success before the server acknowledges a write.'),
 ('Validate with real users','Frontend','Test common tasks with school admins, teachers and parents on desktop and budget phones, in Hindi and English; complete keyboard, screen-reader and responsive checks.')],
 ['role navigation definitions','localized UI dictionaries','saved filter preferences','server permission claims'],['GET /v1/me/dashboard','GET /v1/students','GET /v1/me/notices'],
 'This is a heuristic design review and proposed interface, not a user-tested product or proof of accessibility conformance. Role switching and workflow-state toggles are review controls only.',
 'productui','Review UI direction','The proposed UI direction is selected for review. No application settings were changed.')

add('schoolonboarding','Platform administration','School onboarding & SaaS billing','Your platform-admin tool for school details, billing accounts, contracts, subscription and maintenance charges, invoices and renewals.','Platform administrator / billing operator','Foundation',[
 ('Create the school customer account','Frontend','Capture school/legal name, address, campus details, authorised school owner, billing contact and invoice details. Keep customer account and login membership as distinct records.'),
 ('Record commercial terms','Backend','Choose plan, billing frequency, subscription fee, maintenance amount/frequency, optional setup fee, trial and effective dates. Version negotiated prices and contract terms rather than overwriting history.'),
 ('Store the contract and approvals','Database','Keep private signed contract versions, file metadata/hash, signatory references and commercial approval audit. Separate the drafted agreement from an accepted/signed contract.'),
 ('Provision tenant and first admin','Worker','After activation prerequisites, idempotently create the school tenant and individual school-admin user/membership. Assign a school code and school-scoped, case-insensitive unique username. Never use a shared administrator password.'),
 ('Set up the school-admin password','Backend','Prefer a hashed, expiring, single-use setup token bound to the intended user, recipient and tenant. The verified owner chooses a password. An optional server-generated temporary password expires and permits only password replacement before school access. Store only an adaptive password hash; audit issuance/activation without logging secrets.'),
 ('Create and reconcile SaaS invoices','Backend','Generate separately itemised subscription, maintenance and setup charges on their actual schedules. Use integer minor currency units; apply tax only from validated billing configuration. Reconcile payment callbacks idempotently.'),
 ('Manage renewal and commercial history','Frontend','Track active/trial/overdue/suspended states, invoice/payment/credit history and renewal dates. Apply the contract-defined grace, cancellation and proration policy with auditable changes.')],
 ['school_customers','billing_accounts','contract_versions','plans','subscription_versions','maintenance_charge_schedules','saas_invoices','saas_invoice_lines','saas_payments','tenant_provisioning_jobs','users','memberships','user_login_aliases','credential_setup_tokens','audit_events'],['POST /platform/school-customers','POST /platform/school-customers/:id/contracts','POST /platform/school-customers/:id/terms','POST /platform/school-customers/:id/activate','POST /platform/school-customers/:id/admin-accounts','POST /platform/admin-accounts/:id/reissue-setup','POST /auth/setup/complete','POST /auth/login','GET /platform/school-customers/:id/invoices','GET /v1/me/school-billing'],
 'The platform control plane holds your customer contracts and SaaS revenue. It does not grant access to school student records or school accounting. Schools see only their own authorised billing account. Contract versions, fee changes and payment events remain auditable.',
 'schoolonboarding','Validate onboarding draft','The sample onboarding draft is validated locally. No school, account, contract, invoice or payment was created.')

add('schoolwebsite','Public school website','School website & enquiries','One branded public website per school, seeded from onboarding: banner, school details, academics, approved event photos, contact information and admission enquiries.','School administrator / public visitor','Core',[
 ('Seed the website draft at onboarding','Backend','Create the tenant website draft from the school name, contact details and a unique slug. Use the shared template; do not create another deployment or copy private records into the public site.'),
 ('Complete school content and branding','Frontend','School admin edits banner/name, introduction, academics, contact details and approved public event selections. Use structured fields, a bounded template and reviewed localised content.'),
 ('Validate and approve public content','Backend','Require authorised school-admin membership and a provisioned tenant. Validate required information, unique slug and media-publication permission. Parent-only galleries and internal documents never become public automatically.'),
 ('Publish a versioned public snapshot','Worker','Render a cacheable HTML/public-data snapshot and approved media derivatives. Atomically activate the new revision after generation succeeds. A failed publish leaves the previous published version available.'),
 ('Serve the school-specific pages','Frontend','Resolve the published site from the route or verified hostname. Load Home, About, Academics, Events and Contact from that school’s published revision; keep management pages behind login.'),
 ('Capture and manage an enquiry','Backend','Derive the tenant from the published site route, validate minimal contact fields and contact permission, apply abuse protection and idempotency, then save a private admission lead. Authorised school staff track follow-up history.'),
 ('Edit, republish or unpublish with audit','Database','Draft edits do not alter the live revision. Record who published what and when. Invalidate page/media caches on authorised unpublish; previously saved public photos cannot be recalled.')],
 ['school_sites','site_drafts','site_revisions','site_pages','site_public_media','site_domains','admission_enquiries','enquiry_events','audit_events'],['GET /schools/:slug/:page','POST /schools/:slug/enquiries','GET /v1/website/draft','PUT /v1/website/draft','POST /v1/website/publish','POST /v1/website/unpublish','GET /v1/admission-enquiries','PATCH /v1/admission-enquiries/:id'],
 'A public school site exposes only an approved published projection. No student register, private gallery, question paper, enquiry contact list or tenant-admin API becomes public. Website publication and school login permissions are separate.',
 'schoolwebsite','Review school website','This local preview demonstrates public pages, a website editor and enquiry follow-up. It does not publish a real website or send messages.')

template=(base/'template.html').read_text()
encoded=json.dumps(modules,ensure_ascii=False).replace('</','<\\/')
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=base.parent/'school-architecture-review.html')
output=parser.parse_args().output
output.write_text(template.replace('/*MODULE_DATA*/[]',encoded)
    .replace('/*SCHOOL_WEBSITE_CODE*/',(base/'school-website.js').read_text())
    .replace('/*SCHOOL_WEBSITE_CSS*/',(base/'school-website.css').read_text()))
print(f'Created {output.name}: {len(modules)} functions, {sum(len(m["steps"]) for m in modules)} flow steps')

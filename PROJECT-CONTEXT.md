# SchoolOS — project context and handoff

Updated 21 October 2026.

## Purpose and current state

Build an India-only subscription school platform that connects administration, teaching, families, physical resources and school finance. Each school also gets a public advertising website on the same platform. Start with inexpensive shared infrastructure; increase spending after paid usage and measured operational needs. The developer is experienced. Independent private schools are a proposed starting segment, not a confirmed customer segment.

This is a documentation and prototype repository. No production Node/React application, database, credential store, messaging service or hosting deployment has been built. The HTML contains local illustrative records and interactions.

## Stack and deployment direction

Use React + Vite + TypeScript for the responsive portal; Node.js + TypeScript + NestJS/Fastify for the API; PostgreSQL for durable records; pg-boss and a separate Node worker for jobs; private S3 object storage for media and generated exports. Start as a modular monolith with a shared template and deployment. Do not start with per-school servers, microservices, Kubernetes or a mandatory Redis service. Public school pages use a published HTML/data projection rendered by the existing Node worker and cached independently of the private portal.

Initial infrastructure allowance remains the earlier approximately ₹2,000–₹4,000/month pilot scenario, excluding substantial message delivery, media downloads, support and tax effects. It is not a fresh quote or a capacity guarantee. Provider prices, terms and child-facing AI eligibility need rechecking before purchasing or launching. Subscription prices are not final; the editable calculator includes older core-only assumptions.

## Isolation and identity

One school customer initially corresponds to one tenant. Enforce verified membership, role and class/subject/guardian scope in the server, backed by PostgreSQL row security, restricted runtime roles, same-tenant relationships and transaction-local tenant context. Apply the boundary to counts, filters, files, jobs, exports and caches. Never trust a browser-supplied tenant or child ID.

The platform admin manages customer accounts, commercial contracts, SaaS invoices and activation; this does not automatically grant detailed access to school records. School admin has full functional own-school access; teachers have assigned academic scopes; accountants, librarians and storekeepers have module rights; parents see verified children; students see permitted own records. Audit history and financial controls remain even for school admins.

Create the first individual school admin during provisioning. Login can use school code and a school-scoped username. Prefer an expiring, single-use setup invitation; an initial temporary password must expire and force replacement after intended-owner verification before normal access. Store password hashes, never plaintext. Existing-user recovery goes to the verified owner. Separate users preserve accountability; do not share one school-wide password.

## Connected workflows

- Student identity stays stable across years, with separate enrolments, report versions and class/subject assignments. The directory combines filters, search and pagination; profiles and counts remain permission-scoped.
- Exams preserve setter, paper version, reviewer, approver, invigilator, student attempt, marker and publisher. Draft papers/answer keys stay private until authorised release.
- Bulk messages target all own-school parents, year/class groups, event audiences or selected guardians; teachers are limited to assigned audiences. Deduplicate recipients, approve content and language, snapshot recipients, queue delivery and retain separate provider/read/task states.
- Parent dashboard combines notices, linked-child attendance, homework, fees, published results, books, consent, meetings and approved event packages. English/Hindi require reviewed interface/content dictionaries; only selected prototype screens are bilingual today.
- Procurement links requests, budgets, orders, partial/rejected receipts, invoice matching and accounting. Consumables use quantities; equipment uses unit/custody records; library copies use accession and loan histories. A loan changes availability, not ownership. Full accounting requires balanced journals, correction/reversal history, reconciliation and controlled period close.
- Event galleries are private by default. Moderated audience-specific ZIP packages use expiring application grants, verified parent sessions and short-lived object URLs. Already downloaded copies cannot be recalled.
- School onboarding stores customer details, contracts, negotiated subscription and maintenance schedules, optional setup fee, invoices and renewals. Your SaaS revenue and school student-fee/accounting ledgers are separate.
- The public school website is seeded as a draft during school creation. School admin completes public details, previews and publishes. Pages include Home, About, Academics, Events and Contact/enquiry; private Parent/Staff login remains separate. Publish a versioned public snapshot; edits do not alter the live revision until republished. Public marketing photo selection requires separate approval. Enquiries become private admissions leads with follow-up history. No separate deployment per school is required.

## AI and differentiation

Begin with teacher-approved syllabus/calendar planning, message drafts, reviewed translation, absence catch-up, resource-aware lessons and question clustering. Later evaluate student-facing doubt support under appropriate provider terms and quality controls. AI does not determine balances, grades, permissions or journal entries. Reuse class-level material, enforce per-tenant budgets/quotas and keep deterministic workflows available when AI fails.

Attendance, fees, messaging, translation and portfolios already exist in competitor categories. Differentiation is a hypothesis: connect actual lessons, available books/equipment, procurement and useful parent actions. Desk research does not establish global uniqueness or verified learning improvement. No vendors were demoed and no school-user study has been performed.

## Delivery order and release evidence

Build tenant/identity/audit foundations, school onboarding and public-site publishing, core records/attendance/homework/parent access, messaging/exams/reporting, resource/procurement/accounting modules, then media delivery and AI extensions. The complete scope is not a short MVP or a fixed delivery-date promise.

Release tests must include cross-school and unrelated-child access, teacher scope, token expiry/reuse, duplicate provisioning, repeated payment events, concurrent book lending/stock operations, balanced accounting, unpublished paper protection, public/private media separation, failed-publish rollback, enquiry tenant routing, backup restore and realistic peak load. UI rendering checks do not prove backend isolation or accounting correctness.

## Reviewed sections

01. **Platform overview** — One connected school platform, with a small initial deployment and clear boundaries for growth.
02. **Tenant isolation & roles** — A strict school boundary, plus role and resource permissions inside each tenant.
03. **Identity & permissions** — One account, verified memberships, and precise staff, parent and student access.
04. **All students & profiles** — A searchable student dashboard with combined filters, individual profiles, verified guardians and academic-year history.
05. **Classes, staff & calendar** — Academic years, sections, subjects, teacher assignments and school holidays.
06. **Admissions** — Track an enquiry through review, approval and student enrolment without duplicate entry.
07. **Attendance** — Fast classroom marking with corrections, parent notices and catch-up triggers.
08. **School fees & receipts** — Student dues, partial payments, allocations and audited corrections.
09. **Homework, assessment & reports** — Connect assigned work, teacher feedback and school-approved report formats.
10. **Exams & conduct** — Plan exams within a school/year/class/subject scope and record who conducted them and who attended.
11. **Question papers & review** — A versioned paper workflow recording who set, reviewed, approved and released each exam paper.
12. **Student, class & year reports** — Report cards per student with class/section and academic-year views controlled by role.
13. **Exam history & audit** — Trace paper authorship, review, conduct, attempts, marking and publication by actor and version.
14. **AI syllabus planning** — Turn a reviewed syllabus into a feasible teaching calendar and track actual coverage.
15. **Bulk parent messaging** — Send a notice to all school parents together, an academic year, a class or selected parents; preview the audience before delivery.
16. **Inventory & stock** — Trace stock from receipt through locations, consumption, returns and stock checks.
17. **Equipment & custody** — Know which unit is with whom, in what condition, and under which financial policy.
18. **Library & circulation** — One title, many physical copies, each with an accession identity and loan history.
19. **Procurement & approvals** — Connect department requests, budgets, suppliers, orders and partial/rejected deliveries.
20. **Accounting & reconciliation** — An authoritative posting service with balanced entries, allocations, reversals and period close.
21. **Event galleries** — An event/date home for approved school photos, with private storage and scoped publication.
22. **Expiring download packages** — Share an event ZIP with the right parents through a revocable, expiring application link.
23. **Parent dashboard & inbox** — A dashboard for verified children: school notices, homework, attendance, fees, published results, library and event actions.
24. **Consent & forms** — Versioned school forms and separate parent-only/public media permissions.
25. **Absence catch-up** — Teacher-approved packs based on what was actually taught, shared with absent children.
26. **Resource-aware lessons** — Check real school resources before a planned learning activity.
27. **Borrow–read–return** — Guide reading using available school books and human-reviewed activities.
28. **Parent learning prompts** — A short, practical conversation connected to the child’s current lesson.
29. **Questions & doubt sessions** — A topic-linked question inbox and reviewed answers before autonomous student tutoring.
30. **Progress & portfolios** — Teacher-verified evidence of learning across terms, visible to the family.
31. **Class kit readiness** — Prepare activities with supplies, school loans and clear family acknowledgements.
32. **Meetings & follow-through** — Book a suitable slot and record agreed parent/teacher next actions.
33. **Year-end obligations** — Reconcile books, equipment, finance and paperwork with manual dispute resolution.
34. **Accessible family experience** — Text-first, mobile-friendly screens that work with realistic parent devices and languages.
35. **SaaS subscriptions** — Your school-customer billing, entitlements and metered allowances.
36. **Reports, imports & exports** — Reliable background reports with signed downloads and accepted opening balances.
37. **Security, recovery & scaling** — Protect school boundaries, recover records and grow only around measured bottlenecks.
38. **Product UI & design review** — Review design drawbacks, role-specific navigation and the proposed admin, teacher and parent interface.
39. **School onboarding & SaaS billing** — Your platform-admin tool for school details, billing accounts, contracts, subscription and maintenance charges, invoices and renewals.
40. **School website & enquiries** — One branded public website per school, seeded from onboarding: banner, school details, academics, approved event photos, contact information and admission enquiries.

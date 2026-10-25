# SchoolOS documentation

Product research, architecture and interactive prototypes for an India-focused, multi-tenant school management SaaS with a public website for each school.

**Status:** documentation and browser-local prototypes. The executable backend is maintained separately in [campus-core-api](https://github.com/nishantgautamIT/campus-core-api), a private repository with PostgreSQL migrations, tenant isolation and API health checks. The database foundation is merged. Identity code is extracted in an unmerged draft in `tenant-user-service`; F02 product integration remains deferred. F04 core school provisioning is implemented for review; public websites/enquiries belong in `campus-engagement-api`. Operations, engagement and gateway repositories are scaffolded, with their features pending. Prototype controls do not create real users, send messages, take payments or publish websites.

## Start here

- [Core provisioning schema and validation](previews/school-core-provisioning.html) — first executable core business slice;20 local/fresh checks.

- [Service ownership and revised sequence](previews/school-service-boundaries.html) — identity plus three business services and a common gateway; core provisioning started.

- [Authentication and school membership design](previews/school-authentication-design.html) — F02 library decision and security review requirements, recorded before implementation.

- [Implementation plan and ordered acceptance criteria](previews/school-implementation-plan.html) — new design deliverables remain HTML.
- [Executable backend service](https://github.com/nishantgautamIT/campus-core-api) — Node 24, PostgreSQL and integration checks.
- [Full database design catalogue](previews/school-database-design.html) — broader roadmap, not an executable release migration.

- [Complete project context and scope](PROJECT-CONTEXT.md)
- [Current backend and integration blueprint](docs/architecture/integrated-school-backend-blueprint.md)
- [Interactive architecture and UI review](previews/school-architecture-review.html) — 40 sections, flows, sample screens and proposed records/APIs. Download/open the HTML locally; GitHub displays its source.
- [Parent and child feature research](docs/research/parent-and-child-feature-research.md)
- [Original market research](docs/research/school-saas-research-and-blueprint.md) — historical core-only assumptions are superseded where the current scope differs.
- [Editable cost model](previews/school-saas-cost-model.html) — planning scenarios, not live provider quotes; defaults still reflect the earlier narrow core offering.

## Product boundaries

- Platform administration: school customers, contracts, subscription and maintenance schedules, invoices, renewals and initial school-admin setup.
- Private school portal: tenant/role isolation, student profiles and filters, attendance, homework, exams, paper review/audit, report cards, parents, inventory, library, procurement and accounting.
- Public school website: school creation seeds a draft; school admin completes details, previews and publishes. Home, About, Academics, Events and Contact/enquiry pages use the school's published branding and content. Private galleries and student records do not become public.
- AI roadmap: teacher-reviewed syllabus planning, communication, catch-up and resource-aware learning, with per-school spending limits.

Selected review sections: **04** students/profiles, **15** bulk messages/history, **23** bilingual parent dashboard, **38** role-specific UI review, **39** onboarding/billing/login setup, **40** public school website/editor/enquiry inbox.

## Repository layout

- `docs/research/`: desk research and feature opportunities, with cited sources and limitations.
- `docs/architecture/`: current system design and release requirements.
- `previews/`: self-contained browser HTML deliverables.
- `assets/previews/`: illustrative screenshots; older screenshots preserve earlier review states.
- `source/architecture-review/`: Python generator, HTML template and embedded public-website JS/CSS.
- `source/canvas/`: optional original Canvas source; requires a compatible `cursor/canvas` host.
- `scripts/`: artifact validation scripts.
Backend source, executable migrations and CI live in the separate [campus-core-api repository](https://github.com/nishantgautamIT/campus-core-api). This repository keeps design/research HTML and prototype sources.

The public-site campus/event pictures in the prototype are illustrations, not images of an actual school. Sample student names, contacts, amounts and dates are fictional examples. The repository contains no production credentials or school data.

## Open and rebuild

The self-contained files in `previews/` open directly in a browser without dependencies. An optional local HTTP preview is:

```sh
python3 -m http.server 8877 --bind 127.0.0.1 --directory previews
```

Open `http://127.0.0.1:8877/school-architecture-review.html`. Stop the server when finished.

Rebuild the review using Python 3; no Python packages are required:

```sh
python3 source/architecture-review/build.py --output previews/school-architecture-review.html
```

Validate using Node.js; no npm packages are required:

```sh
node scripts/check-review.cjs
node scripts/check-cost-model.cjs
```

## Limits and next work

Research was performed from official sources; no vendor demos, private quotes or school-user study were conducted. Differentiation, prices, infrastructure provisions and delivery timelines are hypotheses or planning assumptions. Recheck time-sensitive provider pricing, terms and child-facing AI eligibility before launch.

The chosen stack is React/Vite/TypeScript, Node/NestJS/Fastify, PostgreSQL, pg-boss workers and private S3 storage. Use the approved identity/core/operations/engagement split with a common gateway; keep related domain modules within their service. Operational release evidence must include tenant/guardian/teacher isolation, token expiry/reuse, concurrent stock/library operations, payment idempotency, accounting integrity, public/private media separation and a successful restore drill.

import { Callout, Code, Divider, Grid, H1, H2, H3, Link, Pill, Row, Stack, Stat, Table, Text, TextInput, useCanvasState, useHostTheme } from 'cursor/canvas';

const sources = {
  fedena: 'https://fedena.com/pricing-and-plans',
  teachmint: 'https://www.teachmint.com/en-us/features/school-erp',
  entab: 'https://www.entab.in/entab-one.html',
  mcb: 'https://www.myclassboard.com/erp/',
  bexra: 'https://www.bexratech.com/',
  frappe: 'https://github.com/frappe/education',
  aws: 'https://aws.amazon.com/lightsail/pricing/',
  payments: 'https://razorpay.com/blog/razorpay-payment-gateway-pricing-explained/',
};
const money = (n: number) => '₹' + Math.round(n).toLocaleString('en-IN');
const clean = (s: string, max = 1000000) => Math.min(max, Math.max(0, Number(s) || 0));

export default function SchoolSaaSPlan() {
  const theme = useHostTheme();
  const [tab, setTab] = useCanvasState('school-saas-tab', 'Decision');
  const [schools, setSchools] = useCanvasState('school-saas-schools', '3');
  const [price, setPrice] = useCanvasState('school-saas-price', '2499');
  const [fixed, setFixed] = useCanvasState('school-saas-fixed', '1500');
  const [support, setSupport] = useCanvasState('school-saas-support', '500');
  const [ai, setAi] = useCanvasState('school-saas-ai', '100');
  const [students, setStudents] = useCanvasState('school-saas-students', '500');
  const [messages, setMessages] = useCanvasState('school-saas-messages', '22');
  const [rate, setRate] = useCanvasState('school-saas-rate', '0.15');
  const [fee, setFee] = useCanvasState('school-saas-fee', '2.36');
  const n = Math.floor(clean(schools, 10000));
  const revenue = n * clean(price);
  const gateway = revenue * clean(fee, 100) / 100;
  const messaging = n * Math.floor(clean(students)) * clean(messages) * clean(rate, 100);
  const baseline = clean(fixed) + n * (clean(support) + clean(ai)) + gateway;
  const surplus = revenue - baseline;
  const inputStyle = { width: 120 };
  const field = (label: string, value: string, setter: (s: string) => void) => <Stack gap={4}><Text size="small">{label}</Text><TextInput type="number" value={value} onChange={setter} style={inputStyle}/></Stack>;
  return <Stack gap={18} style={{padding: 24, maxWidth: 1120, margin: '0 auto'}}>
    <Text tone="secondary" size="small">INDIA · BOOTSTRAPPED SAAS · RESEARCHED 14 OCTOBER 2026</Text>
    <H1>School management: build for a paid pilot</H1>
    <Row gap={8} wrap>{['Decision', 'Market', 'Architecture', 'Inventory & library', 'Gallery & sharing', 'Parent features', 'Economics', 'Roadmap'].map(t => <Pill key={t} active={tab === t} onClick={() => setTab(t)}>{t}</Pill>)}</Row>
    <Divider/>
    {tab === 'Decision' && <Stack gap={16}>
      <Grid columns="repeat(auto-fit, minmax(170px, 1fr))" gap={16}>
        <Stat value="TypeScript" label="Language across app and jobs"/>
        <Stat value="PostgreSQL" label="Primary relational database"/>
        <Stat value="$12/mo" label="Proposed 2 GB live-pilot VM"/>
      </Grid>
      <H2>React and Node with integrated school operations</H2>
      <Text>React + Vite frontend; Node.js / NestJS with Fastify; PostgreSQL; pg-boss workers; private S3 media. One modular backend and a measured path to separate workers and API replicas.</Text>
      <Text>Suggested initial customer: independent private schools with 200–1,000 students, one district, one board and one language pair. Validate the segment with owners, staff and parents.</Text>
      <Callout tone="info" title="Sell outcomes that can be demonstrated">Fast migration, reliable attendance and fee records, teacher-approved syllabus plans, and clear parent updates. Treat proposed prices and targets as experiments.</Callout>
      <H3>Proposed first offer</H3>
      <Text>₹2,499 was the core-only price hypothesis. Test a separately scoped operations bundle, for example ₹4,999/month, for full procurement/accounting and library. Migration/support and media delivery need their own provisions.</Text>
      <Text tone="secondary">Plan roughly ₹2,000–₹4,000/month for a controlled Node pilot before substantial media delivery. The $12 2 GB VM is a limited starting candidate; $24 4 GB offers headroom. Neither has been load-tested.</Text>
      <Link href={sources.aws}>Verified VM pricing</Link>
    </Stack>}
    {tab === 'Market' && <Stack gap={16}>
      <H2>A crowded market with several pricing models</H2>
      <Table headers={['Product', 'Observed offer', 'Price evidence']} rows={[
        [<Link href={sources.fedena}>Fedena</Link>, 'Broad modular ERP', '$999 / $1,399 / $1,699 yearly on retrieved USD page; India quote needed'],
        [<Link href={sources.teachmint}>Teachmint</Link>, 'Integrated administration and academics', 'No numeric price verified'],
        [<Link href={sources.entab}>Entab One</Link>, 'Broad suite, apps and support', 'Custom price by school size'],
        [<Link href={sources.mcb}>MyClassboard</Link>, 'ERP, communication and AI assessments', 'No numeric price verified'],
        [<Link href={sources.bexra}>Bexra</Link>, 'Budget portal and school identity', '₹5/student/month advertised; quote scope'],
        [<Link href={sources.frappe}>Frappe Education</Link>, 'Open-source implementation alternative', 'GPL v3; hosting and maintenance extra'],
      ]}/>
      <Text>Inference: AI alone is insufficient differentiation. Validate migration, language support, teacher adoption, total annual spending and renewal intent with 10 schools.</Text>
      <Text tone="secondary">Desk research of vendor pages; no private quotes, market-share verification or school interviews performed.</Text>
    </Stack>}
    {tab === 'Architecture' && <Stack gap={16}>
      <H2>One application, with explicit tenant boundaries</H2>
      <div style={{background: theme.fill.tertiary, padding: 18, color: theme.text.primary}}>
        <Stack gap={12}>
          <Text weight="semibold">Admin / teacher / parent PWA</Text>
          <Text>↓ HTTPS reverse proxy</Text>
          <Text weight="semibold">React → Node / NestJS: school records · procurement · inventory · library · accounting · events · SaaS billing</Text>
          <Text>↓ PostgreSQL records + durable jobs → Node worker</Text>
          <Text>Worker → paid AI · email · WhatsApp/SMS</Text>
          <Text>Private S3 + event packages · parent audience/expiry checks · signed payment webhooks · encrypted offsite backups</Text>
        </Stack>
      </div>
      <Grid columns="repeat(auto-fit, minmax(240px, 1fr))" gap={20}>
        <Stack gap={8}><H3>Data design</H3><Text>School IDs on tenant records; same-tenant foreign keys. Preserve academic-year enrolment history. Store money in paise and audit financial corrections.</Text></Stack>
        <Stack gap={8}><H3>Authorisation</H3><Text>Membership-derived tenant context, restricted runtime DB role, row security, guardian links and teacher assignments. Scope jobs, exports and files.</Text></Stack>
      </Grid>
      <Text><Code>PostgreSQL → managed PostgreSQL</Code> later is a deployment upgrade. The initial codebase can remain in place.</Text>
      <Text>AI calendar planning: confirm topics → apply calendar constraints → draft → validate → teacher approve → publish → track actual coverage.</Text>
      <Text>Keep requests bounded, transactions short and API state durable. Index tenant/date and resource lookups; generate reports, ZIPs and thumbnails in workers. Replicate the API only after measuring its bottleneck.</Text>
    </Stack>}
    {tab === 'Inventory & library' && <Stack gap={16}>
      <H2>Shared procurement, distinct resource rules</H2>
      <Table headers={['Resource', 'Track', 'Financial rule']} rows={[
        ['Consumables', 'Quantity, unit, location, receipt and issues', 'Approved stock/expense policy'],
        ['Equipment', 'Unit tag, custody, condition and maintenance', 'Asset/expense classification and depreciation policy'],
        ['Library', 'Edition plus unique accession/barcode per copy', 'Borrowing changes custody; no automatic GL posting'],
      ]}/>
      <Text>Request → budget/approval → quotation → purchase order → accepted/rejected receipt → tag/accession → invoice matching → payment → bank reconciliation.</Text>
      <Text>One authoritative accounting posting service. Balanced journals, exact amounts, duplicate protection, immutable posted records, linked reversals and period locks.</Text>
      <Text tone="secondary">Existing ERPs already offer these modules. Validate end-to-end traceability, exceptions and staff effort through demos and pilots.</Text>
      <Row wrap gap={12}><Link href="https://fedena.com/feature-tour/school-inventory-management-system">Fedena inventory</Link><Link href="https://docs.frappe.io/erpnext/purchase-invoice">ERPNext invoice reference</Link><Link href="https://koha-community.org/manual/latest/en/html/cataloging.html">Koha reference</Link></Row>
    </Stack>}
    {tab === 'Gallery & sharing' && <Stack gap={16}>
      <H2>Event/date albums with expiring parent packages</H2>
      <Text>Metadata in PostgreSQL; original images, thumbnails and versioned ZIPs in private S3. Event date and upload date are separate.</Text>
      <Text>Staff select approved media/audience → bounded ZIP worker → parent-specific application link → verified parent/audience/expiry/revocation → short-lived signed download.</Text>
      <Text>Reuse one binary package for the same approved audience. Changing media permissions invalidates affected packages/grants. Link expiry is separate from event-gallery retention.</Text>
      <Callout tone="info" title="Expiry and revocation">Stop new download authorisations immediately. An already issued object URL can remain usable briefly; previously downloaded files cannot be recalled.</Callout>
      <Text>Cost illustration: a 500 MB package downloaded by 300 parents is about 150 GB of delivery, before retries. Budget downloads as well as stored bytes.</Text>
      <Link href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html">S3 access behaviour</Link>
    </Stack>}
    {tab === 'Parent features' && <Stack gap={16}>
      <H2>Prioritise connected, useful workflows</H2>
      <Table headers={['Feature', 'Priority', 'What to measure']} rows={[
        ['Parent actions across verified children', 'Build first', 'Missed tasks and staff follow-ups'],
        ['Event packages and accessible delivery', 'Build first', 'Preparation effort, support failures, bytes'],
        ['Catch-up from actual classwork', 'Prototype', 'Teacher effort and intended-work completion'],
        ['Resource-aware lesson planning', 'Prototype', 'Shortages and duplicate purchases'],
        ['Borrow–read–return', 'After reliable circulation', 'Participation, returns, reviewed reflections'],
        ['Learning prompts, questions and portfolios', 'Validate next', 'Parent usefulness and teacher reuse'],
      ]}/>
      <Text>Translation, portfolios, photos, reading quizzes and integrated forms/payments are already offered in the market. The exact cross-module opportunities need comparative demos before claiming uniqueness.</Text>
      <Row wrap gap={12}><Link href="https://www.classdojo.com/teachers/">ClassDojo</Link><Link href="https://www.parentsquare.com/platform/parent-and-community-engagement/">ParentSquare</Link><Link href="https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit/parental-engagement">Engagement evidence</Link></Row>
    </Stack>}
    {tab === 'Economics' && <Stack gap={16}>
      <H2>Adjust the assumptions before choosing a price</H2>
      <Text tone="secondary">Defaults are the original core-only scenario. For the expanded product, revise support/price and include gallery storage, requests and downloads in your cost provisions.</Text>
      <Row wrap gap={16}>{field('Schools', schools, setSchools)}{field('₹ subscription / school', price, setPrice)}{field('₹ fixed infra / month', fixed, setFixed)}{field('₹ support / school', support, setSupport)}{field('₹ AI / school', ai, setAi)}{field('Effective checkout fee %', fee, setFee)}</Row>
      <Grid columns="repeat(auto-fit, minmax(170px, 1fr))" gap={16}>
        <Stat value={money(revenue)} label="Monthly recurring revenue"/>
        <Stat value={money(baseline)} label="Modelled costs before messaging"/>
        <Stat value={money(surplus)} label="Surplus before omitted costs" tone={surplus >= 0 ? 'success' : 'warning'}/>
      </Grid>
      <Text tone="secondary">Support is an editable monetary provision. Excludes acquisition, founder development time, accounting, tax on your revenue, discounts, refunds and other overhead. Fixed infra input should include its own tax/FX provision.</Text>
      <Divider/>
      <H3>Why message delivery should be separate</H3>
      <Row wrap gap={16}>{field('Students / school', students, setStudents)}{field('Messages / student / month', messages, setMessages)}{field('Illustrative ₹ / delivery', rate, setRate)}</Row>
      <Table headers={['Scenario', 'Monthly result']} rows={[
        ['Message delivery cost across schools', money(messaging)],
        ['Delivery billed separately at cost: SaaS surplus', money(surplus)],
        ['Delivery absorbed by SaaS: surplus', money(surplus - messaging)],
      ]}/>
      <Text>₹0.15 is an assumption, not a verified WhatsApp tariff. Enter a live category/provider quote including relevant fees. Do not assume all notices receive a utility rate.</Text>
      <Text>Checkout default: 2% plus 18% GST on that fee = 2.36%. For an illustrative 2% + 0.99% recurring fee, set 3.5282%. Negotiated methods vary.</Text>
      <Link href={sources.payments}>Official payment-fee explanation</Link>
    </Stack>}
    {tab === 'Roadmap' && <Stack gap={16}>
      <H2>Staged full-scope rollout; provisional 16–24 weeks</H2>
      <Table headers={['Window', 'Deliver', 'Exit evidence']} rows={[
        ['Discovery', 'Accountant, librarian and school workflow review', 'Accepted policies, scope and pilot price'],
        ['Foundation', 'Tenancy, roles, import and academic structure', 'Isolation and opening-record verification'],
        ['Resources', 'Stock, assets, copies and circulation', 'Concurrent-loan/stock checks'],
        ['Finance', 'Procurement, matching, posting and reconciliation', 'Balanced posting and accountant-reviewed close'],
        ['Parent/media', 'Event packages, expiring links and action centre', 'Audience/expiry and bounded-job checks'],
        ['Rollout', 'Gradual live pilot, recovery and performance', 'Repeatable close and renewal evidence'],
      ]}/>
      <Text tone="secondary">Assumes one experienced full-time developer and fast feedback. Development schedule is an estimate. Student tutoring follows retention, provider eligibility and teacher evaluation.</Text>
      <H3>Upgrade triggers</H3>
      <Text>Persistent memory pressure → larger VM. Delayed jobs → separate worker. Unacceptable recovery window or operational burden → managed PostgreSQL and point-in-time recovery. Measure peak attendance load before expanding.</Text>
    </Stack>}
    <Divider/>
    <Text size="small" tone="secondary">Current details: integrated-school-backend-blueprint.md and parent-and-child-feature-research.md. The original blueprint is retained as a core-only scenario. No school application has been implemented or deployed.</Text>
  </Stack>;
}

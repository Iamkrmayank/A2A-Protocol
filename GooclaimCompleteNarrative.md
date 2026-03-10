# GOOCLAIM — The Complete Narrative Script
> *Internal Clarity Document | March 2026*


---

# CHAPTER 1 — EK SIMPLE SAWAAL SE SHURU KARO

Socho — tumhara ek family member hospital mein admit hai.

Cashless claim file kiya hai. TPA ko pre-authorization deni hai.

Ab tum wait kar rahe ho.

Ek ghante ke baad tumne call kiya TPA ko — *"Kab milegi authorization?"*
Agent bola — *"Processing mein hai."*

Do ghante baad — phir call kiya.
*"Abhi system check kar rahe hain."*

Teen ghante baad — hospital ke desk ne call kiya.
*"Authorization nahi aayi. Patient ka discharge rok diya hai."*

---

**Yahi problem hai. Aur yeh sirf tumhare saath nahi hua.**

IRDAI ke data ke mutabiq — India mein **13.12% pre-authorizations** IRDAI ke mandated 1-hour window mein process nahi hoti.
*(Source: Finance Minister Lok Sabha reply, December 1, 2025)*

Matlab har 100 cashless claims mein se **13 mein yahi hota hai** — delay, confusion, manual follow-up.

Aur FY 2024-25 mein akele **2,57,790 health insurance complaints** file hue.
*(Source: Lok Sabha reply, December 2025)*

**Yeh problem ek case ki nahi hai. Yeh ek broken system ki hai.**

---

# CHAPTER 2 — SYSTEM AAJ KIS TARAH KAM KARTA HAI

## Seedha samajhte hain — ek health claim ka safar

Maan lo tumne ek planned surgery ke liye hospital mein admit kiya.

```
STEP 1 — Hospital pre-auth request bhejta hai TPA ko
         Email se. Ya portal se. Ya fax se. Ya phone se.
         Koi standard nahi hai.

STEP 2 — TPA ke agent ko yeh manually check karna padta hai
         Apne CMS (Claims Management System) mein jaata hai
         Policy details check karta hai
         Documents verify karta hai
         Pehle se agar kuch missing hai — hospital ko call karta hai

STEP 3 — Hospital ko pending documents bhejna padta hai
         Agent ko pata nahi — ek baar mein sab documents maango
         Pehle 2 documents maange. Phir yaad aaya 3rd bhi chahiye.
         Phir 4th. Yahi "piecemeal document request" hai.
         IRDAI ne explicitly BAN kiya hai yeh — phir bhi hota hai.
         (Source: IRDAI Health Dept FAQs)

STEP 4 — TPA approve karta hai ya query raise karta hai
         Agar query hai — phir se cycle
         Hospital ko call karo. Documents maango. Wait karo.

STEP 5 — Patient discharge ke time — final authorization chahiye
         IRDAI ka mandate — 3 ghante mein final auth
         Reality — manual process, phone calls, waiting

STEP 6 — Settlement
         TPA hospital ko directly pay karta hai
         Ya patient reimbursement claim file karta hai
         30 din mein settle hona chahiye — IRDAI mandate
         (Source: IRDAI General Regulations)
```

**Yeh poora process — ek bhi step automated nahi hai.**

TPA ke agent ko manually check karna hai.
Hospital ko manually call karna hai.
Patient ko manually wait karna hai.
Aur koi bhi — kisi ko bhi — real-time status nahi deta.

---

## Sirf health nahi — yeh motor mein bhi hai

Tumhari car accident ho gayi.

```
Garage ne surveyor ke liye request kiya.
Surveyor kab aayega? Koi nahi jaanta.
IRDAI ka mandate — 24 ghante mein surveyor allocate ho.
15 din mein report aani chahiye.
Reality — Excel sheet, phone calls, WhatsApp messages.
(Source: IRDAI Master Circular 2024, BusinessToday June 2024)
```

## Property mein bhi yahi hai

```
Flood damage claim file kiya.
Vendor/assessor ka wait.
Documents ki list — ek baar mein nahi milti.
Status — zero visibility.
```

**Yeh pattern har jagah hai.**

Health. Motor. Property. Life.
India. Southeast Asia. Latin America. Middle East. Africa.

**Har jagah ek hi root cause hai:**

> *Koi intelligent operating layer nahi hai. Kahin bhi nahi.*

---

# CHAPTER 3 — MARKET KITNA BADA HAI

Ab yeh sirf ek operational problem nahi hai — yeh ek massive market opportunity hai.

## India ka size

India mein FY 2023-24 mein:
- **2.69 crore** health claims process hue *(Source: IRDAI Annual Report 2023-24)*
- **₹88,101 crore** claim payments hue *(Source: IRDAI Annual Report 2023-24)*
- **69%** of ALL insurance claims TPAs ke through gaye *(Source: IRDAI Annual Report 2024-25)*

Matlab — India mein insurance claims ka core engine **TPAs hain**. Yeh log ek massive operation chalate hain. Aur yeh operation abhi bhi manually run ho raha hai.

India ka TPA market:
- **$13.70 Billion** aaj (2024) *(Source: IMARC Group, November 2024)*
- **$22.42 Billion** 2033 tak *(Source: IMARC Group, November 2024)*
- **5.6% CAGR** growth rate *(Source: IMARC Group, November 2024)*

India ka Health Insurance market:
- **$15.06 Billion** GWP (2024) *(Source: Grand View Research, 2025)*
- **20.9% CAGR** — yeh sector bahut fast grow kar raha hai *(Source: Grand View Research, 2025)*

Non-life insurance (health + motor + property):
- **₹2.90 Trillion** total premium *(Source: Business Standard, December 2024)*
- **₹1.72 Trillion** net incurred claims *(Source: IRDAI Annual Report 2023-24)*

## Global ka size

Ab yeh problem sirf India mein nahi hai.

**Southeast Asia** — same broken system. WhatsApp dominant channel.
**Latin America** — same ops model. No intelligent layer.
**Middle East + Africa** — same fragmentation. No solution.

Yeh **5 billion logon** ka market hai.

Aur koi bhi global player abhi yeh serve nahi kar sakta.

Kyun? Kyunki global players jo hain — jaise **Avallon** (YC-backed, $4.6M seed, US + Europe) — woh English-only hain, clean modern APIs ke liye bane hain, US/Europe ke adjuster-centric model ke liye hain.

India mein? 32 languages hain. Legacy systems hain. WhatsApp dominant hai. IRDAI compliance hai. Yeh Avallon serve nahi kar sakta.
*(Source: BusinessWire / Y Combinator, November 2025)*

> **"Avallon US ke liye build kar raha hai. Gooclaim baaki sab ke liye."**

---

# CHAPTER 4 — TOH GOOCLAIM KYA HAI

Main pehle bata deta hoon — **Gooclaim kya NAHI hai:**

- WhatsApp bot nahi hai
- Healthcare company nahi hai
- TPA nahi hai
- Ek AI chatbot nahi hai
- Ek India-only product nahi hai

**Gooclaim ek Claims Operating System hai.**

Isko samjhne ka sabse aasaan tarika:

---

Socho Windows ya macOS — ek operating system jo tumhare computer ke upar baitha hai. Tum directly hard drive se baat nahi karte. Tum directly processor se baat nahi karte. OS sab kuch manage karta hai — beech mein.

**Gooclaim wahi kaam karta hai — claims ke liye.**

```
LEFT SIDE                    MIDDLE                    RIGHT SIDE
(Jahan sach rehta hai)      (Gooclaim OS)             (Kaise pahunchta hai)

CMS / TPA Systems    ──▶                       ──▶    WhatsApp
Document Vault       ──▶    GOOCLAIM OS        ──▶    Voice / IVR
Knowledge & Rules    ──▶    (Reads everything  ──▶    Email
Identity / RBAC      ──▶     Processes it      ──▶    Chat Widget
CRM / Ticketing      ──▶     Decides           ──▶    SMS
Hospital HMS         ──▶     Acts)             ──▶    (App — future)
Analytics / SIEM     ──▶                       ──▶
AI Agents (32 lang)  ──▶
```

**Left side** — yahan sach rehta hai. Claim ka status, documents, policy details, rules.
**Middle** — Gooclaim OS. Yeh sab kuch read karta hai, process karta hai, decide karta hai.
**Right side** — delivery. Kaise stakeholder tak pahunchata hai — WhatsApp, voice, email.

**Sabse important baat:**
- WhatsApp sirf ek channel hai — product nahi
- Healthcare sirf pehla vertical hai — identity nahi
- India sirf pehla market hai — end goal nahi

**Product hai — woh engine jo beech mein baitha hai.**

---

# CHAPTER 5 — HEALTHCARE KYU CHOOSE KIYA? WHATSAPP KYU CHOOSE KIYA?

Yeh sabse important question hai. Aur iska jawab logic mein hai — instinct mein nahi.

---

## Healthcare Kyun? — 5 Reasons

### Reason 1 — Sabse bada pain point, verified data ke saath

Health insurance mein claims ka volume sabse zyada hai.
2.69 crore claims. ₹88,101 crore. 69% TPAs se.
*(Source: IRDAI Annual Report 2023-24)*

Aur pain bhi sabse zyada hai — kyunki health claims time-sensitive hain. Agar motor claim mein delay ho — inconvenience hai. Agar health claim mein delay ho — patient hospital mein ruk jaata hai. Stakes bahut high hain.

### Reason 2 — Regulatory pressure sabse strong hai

IRDAI ne health ke liye strictest mandates lagaye hain:
- Pre-auth: **1 ghante mein** *(Source: IRDAI Master Circular, May 29, 2024)*
- Discharge: **3 ghante mein** *(Source: IRDAI Master Circular, May 29, 2024)*
- Breach penalty: **insurer ke shareholder funds se** pay karna padta hai

Yeh mandatory compliance hai — optional nahi. Iska matlab har TPA ko yeh solve karna HI padega. Gooclaim iska direct solution hai.

### Reason 3 — "Cashless Everywhere" ne game change kar diya

January 2024 mein IRDAI aur General Insurance Council ne "Cashless Everywhere" launch kiya.
*(Source: IRDAI / General Insurance Council, January 2024)*

Pehle — cashless sirf network hospitals mein.
Ab — **kisi bhi hospital mein** cashless possible.

Iska matlab? TPA ko ab un hospitals se bhi coordinate karna hai jahan koi integration hai hi nahi. Coordination burden 3 guna badh gaya. Yeh directly Gooclaim ki zaroorat create karta hai.

### Reason 4 — Parties sabse zyada hain

Health claim mein:
**Patient → Hospital → TPA → Insurer → Regulator (IRDAI)**

Itne saare parties, itna coordination, itna scope — yahi hai jahan ek OS sabse zyada value deta hai.

### Reason 5 — Workflow generic hai — verticals mein port hoga

Jo engine hum health ke liye bana rahe hain:
- Status fetch → generic
- Document request → generic
- Query resolution → generic
- Audit trail → generic

**Sirf templates aur variables badlenge — motor ke liye, property ke liye, life ke liye.**

Yeh rebuild nahi hoga. Config change hoga.

---

## WhatsApp Kyun? — 5 Reasons

### Reason 1 — India mein already dominant hai

WhatsApp ke India mein **535 million** active users hain.
Patients already WhatsApp use kar rahe hain.
Hospitals already WhatsApp use kar rahe hain.
TPAs already WhatsApp use kar rahe hain.

Naya behavior sikhana nahi padta. Existing behavior pe build karo.

### Reason 2 — Insurance sector mein already proven hai

**Future Generali** aur **Bharti AXA** ne WhatsApp se claims processing shuru ki hai. Yeh experiment nahi hai — yeh proven channel hai India ke insurance sector mein.

### Reason 3 — November 2024 se service conversations free hain

WhatsApp Business API mein service conversations — matlab inbound + customer-initiated — **free aur unlimited** ho gaye November 2024 se.

Cost structure completely change ho gayi. Scale pe cost exponentially nahi badhega.

### Reason 4 — Template-first = zero hallucination risk

WhatsApp pe WABA (WhatsApp Business API) templates use hote hain — pre-approved, structured messages.

Iska matlab — AI kuch bhi galat nahi bol sakta. System sirf wahi bolega jo template mein hai aur CMS se data aaya hai.

IRDAI ke liye perfect. TPA procurement ke liye perfect. Zero legal risk.

### Reason 5 — Entry point hai — product identity nahi

WhatsApp se start karna ek strategic wedge hai. Ek baar TPA ka trust gain ho gaya, ek baar integration ho gayi — hum voice add karenge, email add karenge, chat widget add karenge.

**Pehla channel WhatsApp hai. Baaki sab aayenge.**

---

# CHAPTER 6 — GOOCLAIM MVP KYA SOLVE KARTA HAI AAJ

MVP mein teen live workflows hain. Simple, specific, powerful.

---

## RW1 — Claim Status

**Aaj kya hota hai:**
Patient ya hospital WhatsApp pe message karta hai — "Mera claim kahan tak pahuncha?"
TPA agent ko manually CMS open karna padta hai. Status check karna padta hai. Reply karna padta hai.
Har din TPA ko hundreds of such calls/messages aate hain.

**Gooclaim kya karta hai:**
Patient claim ID bhejta hai WhatsApp pe.
Gooclaim automatically TPA ke CMS se real-time status fetch karta hai.
Structured, compliant update turant bheji jaati hai.
**Zero manual agent involvement. Full audit trail.**

---

## RW2 — Pending Documents

**Aaj kya hota hai:**
TPA agent claim dekhta hai — kuch documents missing hain.
Ek document maangta hai. Patient bhejta hai. Phir agent dekhta hai — "ek aur chahiye." Phir aur ek. Yahi "piecemeal" problem hai — IRDAI ne explicitly ban kiya hai.
*(Source: IRDAI Health Dept FAQs)*

**Gooclaim kya karta hai:**
System claim check karta hai — **ek hi baar mein** saare pending documents identify karta hai.
WhatsApp pe ek clear, structured list bheji jaati hai.
IRDAI compliant — no piecemeal. Full audit trail.

---

## RW3 — Query Reason

**Aaj kya hota hai:**
TPA ne claim pe query raise ki. Patient ko koi nahi bata raha kyun.
Patient call karta hai. Hold pe rakha jaata hai. Kabhi callback nahi aata.

**Gooclaim kya karta hai:**
System CMS se query reason fetch karta hai.
Clear language mein patient ko explain karta hai — **"Aapka claim query mein hai kyunki [reason]. Aapko yeh karna hai: [next steps]."**
Ticket automatically create hota hai escalation ke liye agar zaroorat ho.

---

## Teen workflows. Simple. Powerful.

Yeh sirf ek chatbot nahi hai jo scripted answers deta hai.
Yeh ek system hai jo **CMS se real data laata hai**, compliance rules follow karta hai, audit trail rakhta hai, aur TPA ke ops load ko dramatically reduce karta hai.

---

# CHAPTER 7 — EXISTING SOLUTIONS SE GOOCLAIM ACHA KYU HAI

Ab seedha comparison karte hain.

---

## Comparison 1 — Gooclaim vs Generic Chatbots (Dialogflow, Freshchat bots, etc.)

| Sawaal | Generic Chatbot | Gooclaim |
|--------|----------------|----------|
| Claim ka real-time status de sakta hai? | ❌ No — CMS se connected nahi | ✅ Yes — directly CMS se fetch |
| IRDAI compliant responses? | ❌ No guardrails | ✅ Forbidden phrase filter built-in |
| Audit trail for regulator? | ❌ Basic logs at best | ✅ Immutable audit trail, every action |
| Hallucination rokta hai? | ❌ AI can make things up | ✅ No-source-no-answer rule — if data nahi toh answer nahi |
| Multi-tenant TPA support? | ❌ Single tenant typically | ✅ Full tenant isolation |
| DPDP consent compliance? | ❌ Not built-in | ✅ Consent captured per interaction |
| Kill switch for infosec? | ❌ No | ✅ Instant halt capability |

**Verdict:** Generic chatbot answers deta hai. Gooclaim **claims OS** hai — truth layer ke saath, compliance ke saath, audit ke saath.

---

## Comparison 2 — Gooclaim vs TPA ke Existing Portal/System

| Sawaal | TPA Ka Apna Portal | Gooclaim |
|--------|-------------------|---------|
| Patient ko WhatsApp pe reach karta hai? | ❌ Portal pe aana padta hai | ✅ Jahan patient already hai |
| Hospital staff ke liye easy? | ❌ Login, navigate, wait | ✅ WhatsApp message = instant |
| Multiple channels? | ❌ Sirf portal | ✅ WhatsApp now + Voice/Email soon |
| 32 Indian languages? | ❌ English/Hindi only mostly | ✅ 32 languages via AI agents |
| Compliance automation? | ❌ Manual | ✅ Built-in |
| Integration with HMS/CRM? | ❌ Siloed | ✅ Connects everything |

**Verdict:** TPA portal ek tool hai. Gooclaim **OS hai** — portal ko replace nahi karta, **uske upar baitha hai**.

---

## Comparison 3 — Gooclaim vs Manual Ops (Human Agents)

| Sawaal | Manual Agent | Gooclaim |
|--------|-------------|---------|
| 24/7 available? | ❌ Business hours only | ✅ Always on |
| Consistent responses? | ❌ Depends on agent | ✅ Same answer every time |
| Audit trail? | ❌ Memory + notes | ✅ Every action logged |
| Scale karta hai? | ❌ Linear — zyada load = zyada headcount | ✅ 10x claims = same cost |
| IRDAI mandates track karta hai? | ❌ Excel + reminders | ✅ Automated SLA tracking |
| Tier-1 queries handle karta hai? | ✅ Yes but costly | ✅ Yes — much cheaper |

**Verdict:** Human agents complex cases ke liye important hain. Gooclaim **tier-1 load eliminate karta hai** — repetitive queries — taaki agents sirf complex cases pe focus karein.

---

## Comparison 4 — Gooclaim vs Avallon (Nearest Global Competitor)

| Dimension | Avallon | Gooclaim |
|-----------|---------|---------|
| Market | US + Europe only | India + Emerging Markets |
| Languages | English only | 32 Indian languages |
| Distribution | Clean REST APIs, modern systems | WhatsApp-first, legacy system support |
| Model | Adjuster-centric | TPA/Insurer ops-centric |
| Compliance | US/EU regulations | IRDAI, DPDP, NHCX ready |
| Funding | $4.6M seed, YC-backed | India-first, emerging market focus |
| Entry | ❌ Cannot enter India | ✅ Born in India |

*(Source: BusinessWire / Y Combinator, November 2025)*

**Verdict:** Avallon US ke liye. Gooclaim baaki duniya ke liye. **Yeh overlap hi nahi hai.**

---

# CHAPTER 8 — GOOCLAIM AAGE KAHAN JAYEGA

Abhi hum Phase 1 mein hain — **Template OS**. Controlled, compliant, zero AI risk.

Lekin yeh sirf shuruwat hai.

---

## Phase 2 — AI-Assisted Agent (Post Pilot)

*"AI suggest karta hai. Human approve karta hai. System seekhta hai."*

Phase 1 mein hum sab data collect kar rahe hain — har claim, har action, har outcome. Audit trail mein.

Phase 2 mein yeh data AI ko train karega:
- AI dekhega — "Is type ke claim mein, yeh document request 87% cases mein resolve karta hai"
- Agent ko suggest karega — "Yeh karo"
- Agent approve karega — action hoga
- Outcome feed hoga — AI aur smarter hoga

**Channels badhenge:** Voice Agent + Email Agent + Chat Widget add honge.
**Verticals badhenge:** Motor claims + Property claims add honge.
**Intelligence badhegi:** Denial patterns surface honge. TAT breach prediction hogi.

---

## Phase 3 — Fully Agentic Claims OS

*"Autonomous end-to-end claims execution. Har channel. Har vertical. Har language."*

Yeh woh state hai jahan:
- **WhatsApp Agent** — intake, documents, status, escalation
- **Voice Agent** — inbound + outbound calls, 32 languages, auto-summary post call
- **Email Agent** — unified inbox, contextual replies, claim linking
- **Chat Agent** — web widget on TPA portal
- **Escalation Agent** — human handoff with full context packet

Write-back bhi aayega — lekin sirf human approval ke baad, kill switch ke saath, post-3 months.

**32 Indian Languages:**
Hindi, Bengali, Telugu, Marathi, Tamil, Gujarati, Kannada, Malayalam, Odia, Punjabi, Assamese — aur baaki sab.

Har Indian citizen serve hoga. Koi language barrier nahi.

---

## The Protocol — Sabse Bada Long-term Play

Yeh woh cheez hai jo Gooclaim ko ek product se ek **platform** aur phir ek **standard** banayegi.

Socho — jab hum 10 TPAs ke saath integrate ho jayenge, hum dekh lenge:
- Har CMS mein claim_id alag naam se hota hai
- Har doc vault mein document types alag hain
- Har insurer portal ka format alag hai
- Same logic 20 baar rebuild karna padta hai

Isi pain se ek **Claims Interoperability Protocol** banega.

**What OCPI did for EV charging across 60+ countries.**
**What ONDC did for open commerce in India.**
**Gooclaim Protocol can do for claims.**

**Sequencing:**
```
Abhi      →  Custom integrations — fast, observe pain
3-6 month →  Internal connector framework emerge hoga
Year 1 end →  Draft protocol spec — real data se
Post-pilot →  GitHub pe publish — naam + version tag
             (IP established. Even incomplete spec = timestamp)
Year 2     →  Open-source. Community. Industry adoption.
```

**Protocol kyu important hai:**
1. **IP Moat** — Published spec = Gooclaim standard-setter hai
2. **Distribution** — Jo bhi protocol adopt kare, Gooclaim ko use karna padega
3. **Defensibility** — Product copy ho sakta hai. Protocol with adoption — nahi.

---

# CHAPTER 9 — COMPLIANCE AK FEATURE NAHI — YEH MOAT HAI

Bahut saari companies compliance ko ek burden samajhti hain.

**Gooclaim ke liye yeh sabse bada competitive advantage hai.**

TPAs generic bots nahi khareedte. Woh khareedte hain Gooclaim — kyunki:

| Compliance Feature | Kya Karta Hai | Kyu TPA Ke Liye Matter Karta Hai |
|-------------------|--------------|----------------------------------|
| No-source-no-answer | Bina verified data ke kuch nahi bolega | "AI galat nahi bolega" — infosec approved |
| Forbidden phrase filter | "Approved", "rejected", "guaranteed" kabhi nahi bolega | Unauthorized adjudication impossible |
| Kill switch | Instant halt of everything | Procurement requirement cleared |
| Immutable audit trail | Har action logged with timestamp, actor, version | IRDAI audit mein koi panic nahi |
| DPDP consent layer | Consent captured per interaction | India's data protection law = compliant |
| Tenant isolation | Har TPA ka data alag | Cross-customer data exposure = impossible |
| Verification tiers | Identity verify hoti hai before sensitive data | PII kabhi galat party ko nahi jaati |
| NHCX-ready architecture | National health claims exchange compatible | Future-proof on government rails |

> **"TPA ka CISO isko approve kar sakta hai. TPA ka compliance team isko sign off kar sakti hai. Yahi enterprise unlock hai."**

---

# CHAPTER 9A — EXISTING COMPANIES KYA KAR RAHE HAIN — AUR GOOCLAIM DIFFERENT KYU HAI

Ab seedha baat karte hain — market mein koi nahi hai kya? Hain. Toh phir Gooclaim kyun?

Har competitor ko honestly dekho — kya karta hai, kahan ruk jaata hai, aur woh gap kahan hai jo Gooclaim fill karta hai.

---

## PLAYER 1 — MEDI ASSIST (India's Largest TPA)

**Kya hain:** India ka sabse bada health TPA. FY24 mein ₹19,050 crore premium manage kiya. 8 million claims process kiye. 12,000 corporate clients. 11,000+ network hospitals.
*(Source: Medi Assist News, November 2024)*

**Kya kar rahe hain technically:**
- AI system jo hospital discharge time predict karta hai aur fraud detect karta hai
- MAtrix aur MAven — internal digital platforms
- NHCX integration complete kar li (National Health Claims Exchange)
- FY25 mein ₹723 crore operating revenue, 28.5% profit growth
*(Source: Medi Assist News, May 2025)*

**Lekin kahan ruk jaate hain:**
```
❌ Stakeholder communication abhi bhi portal-based hai
   Patient ko login karna padta hai — WhatsApp pe nahi milta
❌ Status updates SMS/email se aate hain — reactive, not proactive
❌ Hospital ko pre-auth ke liye email karna padta hai: cashless@mediassist.in
   Koi real-time orchestration nahi
❌ Reimbursement mein original hard copies 15 din mein courier karni padti hain
   2026 mein bhi physical documents
❌ They ARE the TPA — woh apna ops modernize kar rahe hain
   Lekin unke paas COMPETITOR TPAs ko serve karne ka incentive nahi
```

**Gooclaim ka angle:**
> Medi Assist ek TPA hai jo internally modernize ho raha hai. Gooclaim ek OS hai jo **har TPA** ke upar baitha hai — Medi Assist ke competitors bhi Gooclaim ko use kar sakte hain. Yeh ek horizontal platform hai, vertical player nahi.

---

## PLAYER 2 — ARTIVATIC.AI (India AI Insurtech Platform)

**Kya hain:** AI-based insurtech platform. 2017 mein founded. RenewBuy group ka part. Bangalore-based.
*(Source: Tracxn / Crunchbase, 2024)*

**Kya kar rahe hain technically:**
- **ALFRED** — AI claims automation system: auto-adjudication, fraud detection, 160+ parameters per claim
- Claim settlement in 20-30 minutes — 90% TAT reduction claimed
*(Source: BusinessToday, June 2024)*
- **AUSIS** — AI underwriting with 2500+ rules
- **700+ AI insurance APIs** via INFRD platform
- Serving carriers, brokers, TPAs across India, Middle East

**Lekin kahan ruk jaate hain:**
```
❌ B2B API platform hai — insurer/TPA ke internal decisioning ke liye
   Patient ya hospital directly interact nahi karta
❌ Claims adjudication + fraud detection focus hai
   Stakeholder communication, status visibility, TAT tracking — nahi
❌ Revenue sirf ₹7.59 crore FY24 — still early stage commercially
   (Source: Tracxn, 2024)
❌ WhatsApp channel — nahi
❌ 32 Indian languages — nahi
❌ Multi-tenant TPA ops console — nahi
❌ IRDAI compliance guard (forbidden phrases, kill switch) — nahi
```

**Gooclaim ka angle:**
> Artivatic ek **decisioning tool** hai — AI se adjudication fast karna. Gooclaim ek **workflow orchestration OS** hai — intake se settlement tak, har stakeholder ke liye, har channel pe. Yeh complementary bhi ho sakte hain — Artivatic ka ALFRED andar decision leta hai, Gooclaim bahar communication aur workflow manage karta hai.

---

## PLAYER 3 — NEUTRINOS (Global Insurance Automation Platform)

**Kya hain:** Singapore-based, Bangalore office. Insurance ke liye AI-powered business automation platform. 2015 mein founded. Everest Group PEAK Matrix mein Major Contender (2023). Celent ne "Technology Standout in Life Insurance Claims Administration" rakha February 2026.
*(Source: Neutrinos PR, February 2026 + Everest Group, April 2024)*

**Kya kar rahe hain technically:**
- Full-stack intelligent automation: underwriting + claims + distribution
- Low-code platform — insurers khud workflows build karein
- October 2024: New platform launch — omnichannel support including WhatsApp, email, SMS
- AI-Native "Coreless System of Execution" — September 2025 launch
- Clients: Prudential Financial (US), insurers across North America, Middle East, APAC
*(Source: Neutrinos website + PRNewswire, September 2025)*

**Lekin kahan ruk jaate hain:**
```
❌ Low-code platform — TPA ki IT team ko khud configure karna padta hai
   Gooclaim plug-and-play hai, Neutrinos implementation-heavy hai
❌ Global platform — India-specific compliance nahi
   IRDAI mandates, DPDP, NHCX, "Cashless Everywhere" — unke templates mein nahi
❌ Adjuster + carrier centric — TPA ops model ke liye nahi bana
❌ Enterprise-only pricing — small/mid TPAs ke liye accessible nahi
❌ 32 Indian languages, WhatsApp-first India distribution — nahi
❌ India market focus — minimal. US/Middle East primary markets.
```

**Gooclaim ka angle:**
> Neutrinos ek powerful **enterprise automation foundry** hai — insurer khud kuch bhi build kar sakta hai. Gooclaim ek **purpose-built Claims OS** hai — ready-to-deploy, India-specific, TPA-first. Ek general tool vs. ek vertical specialist.

---

## PLAYER 4 — AVALLON (US, YC-Backed — Nearest Vision Competitor)

**Kya hain:** New York-based. Y Combinator Spring 2025 cohort. $4.6 million seed raised November 2025, led by Frontline Ventures + YC + 1984 + Liquid2.
*(Source: BusinessWire, November 6, 2025)*

**Kya kar rahe hain technically:**
- AI agents jo insurance claims tasks automate karte hain — intake to resolution
- Voice AI — intake calls, status queries, billing questions handle karta hai
- Document processing — medical reports, invoices, unstructured docs
- Data entry automation — CMS mein structured data populate karta hai
- Integrates with existing CMS, IVR platforms, data warehouses
- Revenue 10x during YC cohort. Live with 400+ adjuster TPA (Athens Administrators, US)
*(Source: BusinessWire + AlleyWatch, November 2025)*

**Lekin kahan ruk jaate hain:**
```
❌ US + Europe ONLY — ye unka explicit focus hai
   India mein aa hi nahi sakte — reasons below:

❌ English-only system
   India mein 32 languages — Avallon serve nahi kar sakta

❌ Clean REST APIs assume karta hai
   India ke TPA CMS legacy portals — Excel exports, SFTP feeds
   Avallon ka approach India mein work nahi karega

❌ Adjuster-centric model
   US mein "adjuster" hota hai — India mein TPA ops agent
   Completely different workflow, different accountability structure

❌ IRDAI compliance — zero
   "Cashless Everywhere", DPDP consent, NHCX compatibility — Avallon ne kabhi
   suna hi nahi hai yeh regulations

❌ WhatsApp-first distribution — nahi
   India mein 535 million WhatsApp users — Avallon SMS/email/voice only

❌ India market presence — zero
   No customers, no integrations, no regulatory knowledge
```

**Gooclaim ka angle:**
> Yeh sabse important comparison hai. Avallon woh company hai jo **same vision** ke saath build kar rahi hai — Claims OS with AI agents. Lekin woh US ke liye hai. Gooclaim baaki duniya ke liye hai. **Geographic + language + regulatory + distribution gap itna bada hai ki yeh overlap hi nahi hai.**

> *"Avallon is building for the US. Gooclaim is building for everyone else."*

---

## PLAYER 5 — NHCX / ABDM (Government Digital Rail)

**Kya hain:** National Health Claims Exchange — Government of India ka initiative. National Health Authority ke under. Digital claims exchange infrastructure.

**Kya kar rahe hain:**
- Digital rail — standard format mein claims data exchange
- July 2024 tak sirf **34 insurers + TPAs onboarded**
*(Source: MoHFW GOI, July 2024)*
- ABDM ke saath integration — health ID, health records

**Lekin kahan ruk jaate hain:**
```
❌ Infrastructure hai — product nahi
   NHCX claims ka format standardize karta hai
   Lekin workflow orchestration, stakeholder communication,
   TAT tracking, document chasing — yeh sab nahi karta

❌ Adoption abhi minimal hai — 34 entities only (July 2024)
   Thousands of hospitals and TPAs still outside

❌ Government pace — slow rollout, compliance-driven
   Not a commercial product competing with Gooclaim

✅ OPPORTUNITY: Gooclaim NHCX-ready architecture build kar raha hai
   Jab NHCX fully scale hoga — Gooclaim uske upar baitha hoga
   Government rail + Private intelligence layer = powerful combo
```

**Gooclaim ka angle:**
> NHCX competitor nahi hai — **infrastructure partner** hai. Gooclaim NHCX ke upar baitha OS hai. Jaise UPI ke upar PhonePe/Paytm baithe hain — NHCX ke upar Gooclaim.

---

## THE COMPLETE COMPETITIVE MAP

```
COMPANY          TYPE              FOCUS              INDIA-READY?   GOOCLAIM OVERLAP?
─────────────────────────────────────────────────────────────────────────────────────
Medi Assist      TPA (Customer)    Internal ops       ✅ India-only   ❌ They're the CUSTOMER
Artivatic        AI Decisioning    Underwriting/fraud ✅ India        🟡 Partial (decisioning only)
Neutrinos        Low-code Platform Enterprise insurers ⚠️ Minimal    🟡 Partial (general tool)
Avallon          Claims OS (Vision) US adjusters      ❌ Cannot enter ❌ Zero overlap
NHCX/ABDM        Govt Infrastructure Health exchange  ✅ India-only   ✅ We ride on top
─────────────────────────────────────────────────────────────────────────────────────

VERDICT:
No one is building a WhatsApp-first, India-IRDAI-compliant, multi-tenant
TPA Claims OS with 32 languages and multi-vertical portability.
That is Gooclaim's uncontested space.
```

---

## WHY GOOCLAIM IS DIFFERENT — THE 6 GAPS NO ONE IS FILLING

```
GAP 1 — CHANNEL GAP
─────────────────────────────────────────────────────────────────────
Everyone builds portals. No one is WhatsApp-first.
India ke 535 million WhatsApp users ko koi serve nahi kar raha
claims workflow pe — properly, with real CMS data, with compliance.

GAP 2 — COMPLIANCE GAP
─────────────────────────────────────────────────────────────────────
IRDAI mandates, DPDP, NHCX, "Cashless Everywhere" — India-specific.
Global players don't know this. Local players don't have the OS layer.
Gooclaim: compliance-by-design from Day 1.

GAP 3 — ORCHESTRATION GAP
─────────────────────────────────────────────────────────────────────
Artivatic does decisioning. Neutrinos does automation.
No one does end-to-end workflow orchestration ACROSS all parties:
Patient ↔ Hospital ↔ TPA ↔ Insurer — with one OS managing all.

GAP 4 — LANGUAGE GAP
─────────────────────────────────────────────────────────────────────
32 Indian languages. Every patient deserves to be served in their language.
No existing player — TPA or tech — is solving this at workflow level.

GAP 5 — HORIZONTAL TPA GAP
─────────────────────────────────────────────────────────────────────
Medi Assist modernizes itself. That's internal.
No horizontal OS exists that ANY TPA can plug into —
regardless of their CMS, their size, their state.
Gooclaim is that horizontal layer.

GAP 6 — EMERGING MARKET GAP
─────────────────────────────────────────────────────────────────────
Avallon is the closest vision-level competitor.
They explicitly serve US + Europe.
India + SE Asia + LatAm + Middle East + Africa = 5 billion people.
Zero sophisticated Claims OS exists for them.
This is Gooclaim's territory by default.
```

---

# CHAPTER 10 — POORI STORY EK BAAR MEIN

Bade simple words mein:

**Problem:**
Insurance claims mein koi intelligent layer nahi hai. Sab manually hota hai. TPAs, hospitals, patients — sab ek doosre ko phone karte rehte hain. Data ek jagah hai. Channels doosri jagah hain. Koi coordination nahi. Result: delays, errors, penalties, complaints.

Yeh problem India mein hai. Southeast Asia mein hai. Har emerging market mein hai.
**2.69 crore claims. ₹88,101 crore. 13.12% breach rate. 2,57,790 complaints. Yeh scale hai.**

---

**Our Insight:**
Is problem ka solution ek chatbot nahi hai. Ek portal nahi hai. Ek messaging bridge nahi hai.

Solution ek **Operating System** hai — jo sab systems ke upar baitha ho, data read kare, workflows run kare, compliance ensure kare, aur har channel pe deliver kare.

---

**MVP:**
Hum healthcare se start kar rahe hain — kyunki wahan pain sabse zyada hai, regulations strictest hain, aur "Cashless Everywhere" ne complexity 3x kar di hai.

WhatsApp se start kar rahe hain — kyunki 535 million Indians already wahan hain, insurance mein proven hai, aur November 2024 se service conversations free hain.

Teen workflows live hain: Claim Status, Pending Docs, Query Reason. Template-based. Zero hallucination. Full compliance. Full audit trail.

---

**Why Better:**
Generic chatbot se better — kyunki hum CMS se real data laate hain.
Manual agents se better — kyunki hum 24/7 consistent hain aur scale karte hain.
TPA portals se better — kyunki hum jahan patient hai wahan jaate hain.
Avallon se better — kyunki woh India mein aa hi nahi sakta.

---

**Future:**
Phase 2: AI suggests, human approves, system learns.
Phase 3: Fully agentic — voice, email, chat, 32 languages, all verticals.
Protocol: Claims interoperability standard — Gooclaim's biggest long-term play.

---

**The Moat:**
Deep integrations + 32-language AI + India compliance packs + outcome learning on crores of real claims + protocol standard.

Yeh 3 saal mein replicate nahi hota.

---

> **"Har insurance claim in emerging markets suffers from the same problem: human middleware. Gooclaim replaces that middleware — starting with India and WhatsApp, in 32 languages, building toward a fully agentic Claims OS for 5 billion people that no global player can serve."**

---

# VERIFIED SOURCES — COMPLETE LIST

| # | Source | Kya Data | Kahan Use Hua |
|---|--------|---------|--------------|
| 1 | IRDAI Annual Report 2023-24 | 2.69 crore claims, ₹88,101 crore paid | Ch 1, 3 |
| 2 | IRDAI Annual Report 2024-25 | 69% claims via TPAs | Ch 1, 3 |
| 3 | Finance Minister Lok Sabha reply, Dec 1 2025 | 86.88% TAT compliance, 2,57,790 complaints | Ch 1, 3 |
| 4 | IRDAI Master Circular, May 29 2024 | 1-hour pre-auth, 3-hour discharge mandate | Ch 2, 5 |
| 5 | IRDAI Health Dept FAQs | No piecemeal docs, 30-day settlement | Ch 2, 6 |
| 6 | IRDAI General Regulations | Settlement within 30 days of last document | Ch 2 |
| 7 | IRDAI Master Circular 2024 + BusinessToday June 2024 | Motor surveyor TAT mandates | Ch 2 |
| 8 | IRDAI / General Insurance Council, January 2024 | Cashless Everywhere initiative | Ch 5 |
| 9 | IMARC Group, November 2024 | TPA market $13.7B → $22.4B, 5.6% CAGR | Ch 3 |
| 10 | Grand View Research, 2025 | Health Insurance $15.06B GWP, 20.9% CAGR | Ch 3 |
| 11 | Business Standard / IRDAI AR 2023-24 | Non-life ₹2.90T premium, ₹1.72T claims | Ch 3 |
| 12 | BusinessWire, November 6 2025 | Avallon — $4.6M seed, YC Spring 2025, US+Europe, 10x revenue | Ch 3, 9A |
| 13 | YCombinator.com + AlleyWatch, November 2025 | Avallon: AI agents for calls/docs/data entry, 400+ adjuster TPA live | Ch 9A |
| 14 | MoHFW GOI, July 2024 | NHCX — 34 insurers/TPAs onboarded only | Ch 9A |
| 15 | BusinessToday, June 2024 | Motor claims TAT mandates | Ch 2 |
| 16 | Medi Assist News, November 2024 | Medi Assist: ₹19,050 crore premium FY24, 8M claims, 12,000 clients | Ch 9A |
| 17 | Medi Assist News, May 2025 | Medi Assist FY25: ₹723 crore revenue, 28.5% profit growth | Ch 9A |
| 18 | Tracxn + Crunchbase, 2024 | Artivatic: ₹7.59 crore revenue FY24, acquired by RenewBuy 2022 | Ch 9A |
| 19 | BusinessToday, June 2024 | Artivatic ALFRED: 90% TAT reduction, 20-30 min claim settlement | Ch 9A |
| 20 | Everest Group PEAK Matrix, April 2024 | Neutrinos: Major Contender in low-code insurance platforms | Ch 9A |
| 21 | PRNewswire / Neutrinos, September 2025 | Neutrinos AI-Native Coreless System of Execution launch | Ch 9A |
| 22 | The Tribune / PRNewswire, February 2026 | Neutrinos: Technology Standout in Celent Life Insurance Claims | Ch 9A |

---

*Gooclaim Internal Narrative — March 2026*
*Simple words. Verified sources. Complete story.*


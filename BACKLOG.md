# 📋 Moovv Fit — Master Cross-Repo Backlog

> **Canonical Backlog Mirror** synchronized with Linear (`moovv-fit` workspace).  
> **Last Synced:** `2026-11-06 10:21 UTC` • **Total Open Backlog Issues:** `83`  
> *To refresh this document automatically, run: `./scripts/linear-backlog.py --sync`*

---

## 🎯 Habit-Building Guide: Managing & Exploring the Backlog

To stay on top of the backlog without UI friction, use **Option 1** (terminal CLI) or **Option 4** (conversational pairing with the agent):

### ⚡ Option 1: Backlog CLI Explorer (`./scripts/linear-backlog.py`)
Run directly from anywhere in the repository:
```bash
# 1. Quick cross-repo overview in your terminal
./scripts/linear-backlog.py

# 2. Filter by specific repository domain
./scripts/linear-backlog.py -r mobile      # iOS / Android app backlog
./scripts/linear-backlog.py -r backend     # Node / Lambda / DB backlog
./scripts/linear-backlog.py -r web         # Clinic OS & Physio Portal backlog
./scripts/linear-backlog.py -r landing     # Landing page & funnel backlog

# 3. Filter by urgency across all repos
./scripts/linear-backlog.py -p urgent      # Only Urgent tickets
./scripts/linear-backlog.py -p high        # High priority tickets

# 4. Deep-dive into any specific ticket
linear issue view CORE-113

# 5. Refresh this static BACKLOG.md snapshot
./scripts/linear-backlog.py --sync
```

### 💬 Option 4: Conversational Prompts with the Agent
When pair-programming with Antigravity or Kiro, you don't need to leave chat:
- **Querying**:
  - *"Show me the mobile backlog"*
  - *"What urgent tasks are pending in backend?"*
  - *"What landing page items do we have?"*
- **Capturing on the Fly**:
  - *"Backlog this: [idea or task description]"* → The agent calls `linear issue create --state Backlog` immediately and reports the new ticket ID.
- **Periodic Snapshot Updates**:
  - *"Update the master BACKLOG.md snapshot"* → The agent runs the sync command and updates this file.

---

## 📊 Backlog Summary by Repository

| Domain | Submodule Path | Issues | Primary Focus |
|---|---|:---:|---|
| **📱 Mobile (iOS & Android)** | [`repos/apps/mobile`](repos/apps/mobile) | **15** | Flutter rehabilitation app, assessment engine, routine player, and pain tracking. |
| **⚙️ Backend Core API & Database** | [`repos/backend/node`](repos/backend/node) | **12** | Node/TypeScript Lambda API, Prisma ORM, Cognito auth, and clinical data models. |
| **🌐 Web Portals (Clinic OS & Admin)** | [`repos/apps/web`](repos/apps/web) | **6** | React 19 clinical portal, appointment booking, patient queue, and chat. |
| **🚀 Landing & Patient Acquisition** | [`repos/apps/landing`](repos/apps/landing) | **4** | Static marketing sites, physician lead funnels, and store/PWA onboarding. |
| **🧪 Autonomous Simulator & Test Harness** | [`repos/platform/simulator`](repos/platform/simulator) | **2** | E2E multi-persona automated test harness, websocket synthetic testing. |
| **🎨 Design System Tokens & UI** | [`repos/platform/design-system`](repos/platform/design-system) | **1** | Svelte 5 / Tailwind v4 canonical components and tokens. |
| **📚 Documentation Portals** | [`repos/docs/technical`](repos/docs/technical) | **1** | Partner developer documentation and clinical specifications. |
| **☁️ Platform Infrastructure & Cross-Repo** | [`repos/infra/cdk`](repos/infra/cdk) | **42** | Shared CDK stacks, CloudFront routing, DNS, auth pools, and cross-cutting platform epics. |

---

## 📦 Detailed Backlog Breakdown

### 📱 Mobile (iOS & Android) (15 issues)
**Path:** [`repos/apps/mobile`](repos/apps/mobile)  
*Flutter rehabilitation app, assessment engine, routine player, and pain tracking.*

| ID | Priority | Title | Team |
|---|:---:|---|:---:|
| [CORE-116](https://linear.app/moovv-fit/issue/CORE-116/shift-mobility-assessments-from-manual-self-tests-to-video-based) | `Urgent` | Shift mobility assessments from manual self-tests to video-based assessments | `CORE` |
| [CORE-105](https://linear.app/moovv-fit/issue/CORE-105/integrate-review-by-physio-cta-sheet-and-razorpay-checkout-indian) | `Urgent` | Integrate 'Review by Physio' CTA sheet and Razorpay checkout (₹499 regular / ₹299 promo) | `CORE` |
| [CORE-104](https://linear.app/moovv-fit/issue/CORE-104/add-amber-unreviewed-by-physio-banner-and-educational-disclaimer-to) | `Urgent` | Add amber 'Unreviewed by Physio' banner and educational disclaimer to routine view | `CORE` |
| [CORE-103](https://linear.app/moovv-fit/issue/CORE-103/update-discomfort-pain-flow-for-free-unreviewed-plan-generation-and) | `Urgent` | Update 'Discomfort / Pain' flow for free unreviewed plan generation and video viewing | `CORE` |
| [CORE-123](https://linear.app/moovv-fit/issue/CORE-123/support-international-e164-phone-selector-and-multi-country-auth-in) | `High` | Support International E.164 Phone Selector & Multi-Country Auth in Mobile | `CORE` |
| [CORE-119](https://linear.app/moovv-fit/issue/CORE-119/de-hardcode-mobile-trial-copy-and-support-dynamic-campaign-ingress) | `High` | De-hardcode mobile trial copy and support dynamic campaign ingress | `CORE` |
| [CORE-108](https://linear.app/moovv-fit/issue/CORE-108/display-green-approved-by-physio-badge-upon-clinician-verification) | `High` | Display green 'Approved by Physio' badge upon clinician verification | `CORE` |
| [CORE-107](https://linear.app/moovv-fit/issue/CORE-107/enforce-maximum-2-active-self-serve-plans-limit-ui-gate-with-archive) | `High` | Enforce maximum 2 active self-serve plans limit UI gate with archive dialog | `CORE` |
| [CORE-106](https://linear.app/moovv-fit/issue/CORE-106/implement-performance-and-better-mobility-pre-created-plan-catalog) | `High` | Implement Performance and Better Mobility pre-created plan catalog with home screen addition | `CORE` |
| [CORE-102](https://linear.app/moovv-fit/issue/CORE-102/implement-talk-to-physio-at-home-lead-capture-and-teleconsultation) | `High` | Implement 'Talk to Physio' At-Home lead capture and Teleconsultation timeslot picker | `CORE` |
| [CORE-101](https://linear.app/moovv-fit/issue/CORE-101/implement-4-card-pathway-routing-selector-on-plans-landing-view) | `High` | Implement 4-card pathway routing selector on Plans landing view | `CORE` |
| [CORE-100](https://linear.app/moovv-fit/issue/CORE-100/route-new-user-logins-directly-to-plans-discovery-page) | `High` | Route new user logins directly to Plans discovery page | `CORE` |
| [CORE-93](https://linear.app/moovv-fit/issue/CORE-93/mobile-firebase-cloud-messaging-fcm-remote-push-notifications) | `High` | [Mobile] Firebase Cloud Messaging (FCM) Remote Push Notifications Implementation | `CORE` |
| [CORE-89](https://linear.app/moovv-fit/issue/CORE-89/mobile-audit-and-modernize-github-actions-workflows) | `High` | [Mobile] Audit & modernize GitHub Actions workflows | `CORE` |
| [CORE-94](https://linear.app/moovv-fit/issue/CORE-94/mobile-post-launch-framework-and-dependency-upgrades) | `Medium` | [Mobile] Post-Launch Framework & Dependency Upgrades | `CORE` |

### ⚙️ Backend Core API & Database (12 issues)
**Path:** [`repos/backend/node`](repos/backend/node)  
*Node/TypeScript Lambda API, Prisma ORM, Cognito auth, and clinical data models.*

| ID | Priority | Title | Team |
|---|:---:|---|:---:|
| [CORE-113](https://linear.app/moovv-fit/issue/CORE-113/implement-plan-review-status-state-machine-unreviewed-pending-physio) | `Urgent` | Implement plan review status state machine (UNREVIEWED, PENDING_PHYSIO_REVIEW, APPROVED_BY_PHYSIO) | `CORE` |
| [CORE-112](https://linear.app/moovv-fit/issue/CORE-112/implement-dual-queue-triage-dispatch-pain-clinical-queue-vs-wellness) | `Urgent` | Implement dual-queue triage dispatch (PAIN_CLINICAL_QUEUE vs WELLNESS_PERFORMANCE_QUEUE) | `CORE` |
| [CORE-111](https://linear.app/moovv-fit/issue/CORE-111/implement-razorpay-order-creation-and-webhook-verification-for-indian) | `Urgent` | Implement Razorpay order creation and webhook verification for ₹499/₹299 review package | `CORE` |
| [CORE-109](https://linear.app/moovv-fit/issue/CORE-109/deprecate-7-day-trial-paywall-expiry-suspension-cron) | `Urgent` | Deprecate 7-day trial paywall expiry suspension cron | `CORE` |
| [CORE-122](https://linear.app/moovv-fit/issue/CORE-122/implement-phase-1-global-checkout-via-razorpay-international-and) | `High` | Implement Phase 1 Global Checkout via Razorpay International & Adapter Pattern | `CORE` |
| [CORE-120](https://linear.app/moovv-fit/issue/CORE-120/integrate-customerio-startup-program-as-unified-omnichannel-messaging) | `High` | Integrate Customer.io (Startup Program) as Unified Omnichannel Messaging Engine | `CORE` |
| [CORE-118](https://linear.app/moovv-fit/issue/CORE-118/implement-physio-capacity-and-review-inventory-throttling-engine) | `High` | Implement Physio Capacity & Review Inventory Throttling Engine | `CORE` |
| [CORE-117](https://linear.app/moovv-fit/issue/CORE-117/implement-dynamic-campaign-and-promotion-management-service) | `High` | Implement Dynamic Campaign & Promotion Management Service | `CORE` |
| [CORE-110](https://linear.app/moovv-fit/issue/CORE-110/implement-max-free-active-plans-2-validation-in-plan-activation) | `High` | Implement MAX_FREE_ACTIVE_PLANS = 2 validation in plan activation service | `CORE` |
| [CORE-96](https://linear.app/moovv-fit/issue/CORE-96/backend-re-enable-and-validate-platform-e2e-tests-on-staging) | `High` | [Backend] Re-enable & Validate Platform E2E Tests on Staging | `CORE` |
| [CORE-95](https://linear.app/moovv-fit/issue/CORE-95/backend-expand-unit-and-integration-test-coverage-to-80percent) | `High` | [Backend] Expand Unit & Integration Test Coverage to 80% | `CORE` |
| [CORE-97](https://linear.app/moovv-fit/issue/CORE-97/backend-implement-unified-v1-api-versioning-strategy-adr-014) | `Medium` | [Backend] Implement Unified /v1/ API Versioning Strategy (ADR-014) | `CORE` |

### 🌐 Web Portals (Clinic OS & Admin) (6 issues)
**Path:** [`repos/apps/web`](repos/apps/web)  
*React 19 clinical portal, appointment booking, patient queue, and chat.*

| ID | Priority | Title | Team |
|---|:---:|---|:---:|
| [CLINIC-45](https://linear.app/moovv-fit/issue/CLINIC-45/implement-clinician-plan-review-workbench-exercise-swap-clinical-notes) | `Urgent` | Implement clinician plan review workbench (exercise swap, clinical notes, and 1-click approval) | `CLINIC` |
| [CLINIC-43](https://linear.app/moovv-fit/issue/CLINIC-43/build-dual-tab-triage-interface-in-clinic-os-pain-clinical-queue-vs) | `Urgent` | Build dual-tab triage interface in Clinic OS (PAIN_CLINICAL_QUEUE vs WELLNESS_PERFORMANCE_QUEUE) | `CLINIC` |
| [CLINIC-47](https://linear.app/moovv-fit/issue/CLINIC-47/build-zoho-crm-and-whatsapp-attribution-webhook-pipeline) | `High` | Build Zoho CRM & WhatsApp Attribution Webhook Pipeline | `CLINIC` |
| [CLINIC-46](https://linear.app/moovv-fit/issue/CLINIC-46/build-30-day-asynchronous-chat-messaging-interface-between) | `High` | Build 30-day asynchronous chat messaging interface between physiotherapist and patient | `CLINIC` |
| [CLINIC-44](https://linear.app/moovv-fit/issue/CLINIC-44/implement-duty-physiotherapist-teleconsultation-timeslot-availability) | `High` | Implement duty physiotherapist teleconsultation timeslot availability and calendar scheduling | `CLINIC` |
| [CORE-99](https://linear.app/moovv-fit/issue/CORE-99/web-evaluate-and-extract-shared-ui-components-to-moovvdesign-system) | `Medium` | [Web] Evaluate and extract shared UI components to @moovv/design-system | `CORE` |

### 🚀 Landing & Patient Acquisition (4 issues)
**Path:** [`repos/apps/landing`](repos/apps/landing)  
*Static marketing sites, physician lead funnels, and store/PWA onboarding.*

| ID | Priority | Title | Team |
|---|:---:|---|:---:|
| [CORE-126](https://linear.app/moovv-fit/issue/CORE-126/release-revert-apple-review-pending-flag-in-store-linksjs-once-app) | `High` | [Release] Revert APPLE_REVIEW_PENDING flag in store-links.js once App Store approves new bundle ID | `CORE` |
| [CORE-88](https://linear.app/moovv-fit/issue/CORE-88/landing-align-github-actions-with-canonical-actions-and-tag-dispatch) | `High` | [Landing] Align GitHub Actions with canonical actions & tag dispatch | `CORE` |
| [CORE-115](https://linear.app/moovv-fit/issue/CORE-115/implement-in-home-consultation-lead-routing-webhook-and-ops) | `Medium` | Implement in-home consultation lead routing webhook and ops notification | `CORE` |
| [CORE-114](https://linear.app/moovv-fit/issue/CORE-114/update-landing-page-hero-copy-for-free-exercise-streaming-and-paid) | `Medium` | Update landing page hero copy for free exercise streaming and paid physio review | `CORE` |

### 🧪 Autonomous Simulator & Test Harness (2 issues)
**Path:** [`repos/platform/simulator`](repos/platform/simulator)  
*E2E multi-persona automated test harness, websocket synthetic testing.*

| ID | Priority | Title | Team |
|---|:---:|---|:---:|
| [CORE-98](https://linear.app/moovv-fit/issue/CORE-98/simulator-fix-staging-payment-bypass-and-demo-phone-range-in-backend) | `High` | [Simulator] Fix Staging Payment Bypass & DEMO_PHONE_RANGE in Backend IaC | `CORE` |
| [CORE-91](https://linear.app/moovv-fit/issue/CORE-91/simulator-upgrade-github-actions-workflow-versions) | `High` | [Simulator] Upgrade GitHub Actions workflow versions | `CORE` |

### 🎨 Design System Tokens & UI (1 issues)
**Path:** [`repos/platform/design-system`](repos/platform/design-system)  
*Svelte 5 / Tailwind v4 canonical components and tokens.*

| ID | Priority | Title | Team |
|---|:---:|---|:---:|
| [CORE-90](https://linear.app/moovv-fit/issue/CORE-90/design-system-modernize-ci-workflows-with-canonical-actions) | `High` | [Design System] Modernize CI workflows with canonical actions | `CORE` |

### 📚 Documentation Portals (1 issues)
**Path:** [`repos/docs/technical`](repos/docs/technical)  
*Partner developer documentation and clinical specifications.*

| ID | Priority | Title | Team |
|---|:---:|---|:---:|
| [CORE-92](https://linear.app/moovv-fit/issue/CORE-92/docs-modernize-documentation-ci-workflows) | `High` | [Docs] Modernize documentation CI workflows | `CORE` |

### ☁️ Platform Infrastructure & Cross-Repo (42 issues)
**Path:** [`repos/infra/cdk`](repos/infra/cdk)  
*Shared CDK stacks, CloudFront routing, DNS, auth pools, and cross-cutting platform epics.*

| ID | Priority | Title | Team |
|---|:---:|---|:---:|
| [CORE-121](https://linear.app/moovv-fit/issue/CORE-121/infra-track-spamhaus-dbl-delisting-for-moovvfit-st7326681) | `Urgent` | [Infra] Track Spamhaus DBL delisting for moovv.fit (ST7326681) | `CORE` |
| [CORE-85](https://linear.app/moovv-fit/issue/CORE-85/dev-005-add-clinical-red-flag-triage-hard-stops-for-pregnancy-and) | `Urgent` | [DEV-005] Add clinical red-flag triage hard stops for pregnancy and acute fractures in mobile onboarding | `CORE` |
| [CLINIC-8](https://linear.app/moovv-fit/issue/CLINIC-8/dipp-startup-certification-and-aws-activate-credits-recovery) | `Urgent` | DIPP Startup Certification & AWS Activate Credits Recovery | `CLINIC` |
| [CLINIC-2](https://linear.app/moovv-fit/issue/CLINIC-2/headless-video-player-sdk-and-streaming-endpoints) | `Urgent` | Headless Video Player SDK & Streaming Endpoints | `CLINIC` |
| [CORE-11](https://linear.app/moovv-fit/issue/CORE-11/enforce-o1-bodypartactiveplan-laterality-lock) | `Urgent` | Enforce O(1) BodyPartActivePlan Laterality Lock | `CORE` |
| [CORE-9](https://linear.app/moovv-fit/issue/CORE-9/implement-production-pgbouncer-rds-proxy-connection-pooling) | `Urgent` | Implement Production PgBouncer / RDS Proxy Connection Pooling | `CORE` |
| [CORE-87](https://linear.app/moovv-fit/issue/CORE-87/cross-repo-cicd-and-github-actions-modernization-and-dual-org) | `High` | [Cross-Repo] CI/CD & GitHub Actions Modernization and Dual-Org Deployment Alignment | `CORE` |
| [CORE-84](https://linear.app/moovv-fit/issue/CORE-84/abr-add-multi-rendition-hls-output-sdhdfull-hd) | `High` | ABR: Add multi-rendition HLS output (SD/HD/FULL_HD) | `CORE` |
| [CLINIC-5](https://linear.app/moovv-fit/issue/CLINIC-5/whatsapp-adherence-tracking-and-care-plan-recall-workflows) | `High` | WhatsApp Adherence Tracking & Care Plan Recall Workflows | `CLINIC` |
| [CLINIC-6](https://linear.app/moovv-fit/issue/CLINIC-6/session-package-billing-and-razorpay-webhooks-zoho-suite) | `High` | Session Package Billing & Razorpay Webhooks (Zoho Suite) | `CLINIC` |
| [CLINIC-4](https://linear.app/moovv-fit/issue/CLINIC-4/inbound-voice-and-whatsapp-triage-flow-twilioretell-zoho-crm) | `High` | Inbound Voice & WhatsApp Triage Flow (Twilio/Retell + Zoho CRM) | `CLINIC` |
| [CLINIC-1](https://linear.app/moovv-fit/issue/CLINIC-1/kinetic-age-physio-roster-bulk-db-ingestion) | `High` | Kinetic Age Physio Roster Bulk DB Ingestion | `CLINIC` |
| [CORE-16](https://linear.app/moovv-fit/issue/CORE-16/concurrency-and-double-booking-slot-race-condition-assertions) | `High` | Concurrency & Double-Booking Slot Race Condition Assertions | `CORE` |
| [CORE-13](https://linear.app/moovv-fit/issue/CORE-13/human-in-the-loop-hitl-verification-queue-and-48h-sla-escalation) | `High` | Human-in-the-Loop (HITL) Verification Queue & 48h SLA Escalation | `CORE` |
| [CORE-12](https://linear.app/moovv-fit/issue/CORE-12/decouple-four-bucket-entitlement-engine) | `High` | Decouple Four-Bucket Entitlement Engine | `CORE` |
| [CORE-8](https://linear.app/moovv-fit/issue/CORE-8/consolidate-170-sam-lambdas-to-ecs-fargate-fastifynode-20) | `High` | Consolidate 170+ SAM Lambdas to ECS Fargate (Fastify/Node 20) | `CORE` |
| [CORE-82](https://linear.app/moovv-fit/issue/CORE-82/content-gap-50-exercises-from-ka-mapping-have-no-video-equivalent) | `Medium` | Content Gap: 50 exercises from KA mapping have no video equivalent | `CORE` |
| [CORE-81](https://linear.app/moovv-fit/issue/CORE-81/crashlytics-test-healthcheck) | `Medium` | [Crashlytics] Test Healthcheck | `CORE` |
| [CORE-60](https://linear.app/moovv-fit/issue/CORE-60/qa-knee-to-wall-ankle-test-option-3-clinical-pose-inaccuracy) | `Medium` | [QA] Knee-to-Wall Ankle Test - Option 3: Clinical / Pose Inaccuracy | `CORE` |
| [CORE-57](https://linear.app/moovv-fit/issue/CORE-57/epic-self-test-illustration-qa-and-clinical-remediation) | `Medium` | [EPIC] Self-Test Illustration QA & Clinical Remediation | `CORE` |
| [CORE-58](https://linear.app/moovv-fit/issue/CORE-58/qa-knee-to-wall-ankle-test-option-1-clinical-pose-inaccuracy) | `Medium` | [QA] Knee-to-Wall Ankle Test - Option 1: Clinical / Pose Inaccuracy | `CORE` |
| [CORE-59](https://linear.app/moovv-fit/issue/CORE-59/qa-knee-to-wall-ankle-test-option-3-clinical-pose-inaccuracy) | `Medium` | [QA] Knee-to-Wall Ankle Test - Option 3: Clinical / Pose Inaccuracy | `CORE` |
| [CLINIC-42](https://linear.app/moovv-fit/issue/CLINIC-42/clinic-portal-complete-feature-gaps-vs-landing-page-promises) | `Medium` | Clinic Portal: Complete feature gaps vs landing page promises | `CLINIC` |
| [CORE-30](https://linear.app/moovv-fit/issue/CORE-30/replace-ai-generated-mobility-test-illustrations-with-standardized) | `Medium` | Replace AI-Generated Mobility Test Illustrations with Standardized Visuals | `CORE` |
| [CLINIC-9](https://linear.app/moovv-fit/issue/CLINIC-9/field-sales-playbook-and-tracking-for-2-medical-representatives) | `Medium` | Field Sales Playbook & Tracking for 2 Medical Representatives | `CLINIC` |
| [CLINIC-7](https://linear.app/moovv-fit/issue/CLINIC-7/pincode-and-locality-mapping-for-home-visit-dispatch) | `Medium` | Pincode & Locality Mapping for Home Visit Dispatch | `CLINIC` |
| [CLINIC-3](https://linear.app/moovv-fit/issue/CLINIC-3/specialization-based-provider-slot-routing-and-emergency-handoff) | `Medium` | Specialization-Based Provider Slot Routing & Emergency Handoff | `CLINIC` |
| [CORE-17](https://linear.app/moovv-fit/issue/CORE-17/scaffold-deterministic-persona-state-machine-engine) | `Medium` | Scaffold Deterministic Persona State-Machine Engine | `CORE` |
| [CORE-15](https://linear.app/moovv-fit/issue/CORE-15/admin-staging-review-ui-for-enriched-metadata) | `Medium` | Admin Staging Review UI for Enriched Metadata | `CORE` |
| [CORE-14](https://linear.app/moovv-fit/issue/CORE-14/batch-enrichment-of-300-exercise-jsons-via-claude-sonnet-45) | `Medium` | Batch Enrichment of 300+ Exercise JSONs via Claude Sonnet 4.5 | `CORE` |
| [CORE-10](https://linear.app/moovv-fit/issue/CORE-10/replace-3-5s-web-portal-polling-with-push-events) | `Medium` | Replace 3-5s Web Portal Polling with Push Events | `CORE` |
| [CORE-86](https://linear.app/moovv-fit/issue/CORE-86/consolidate-custom-exercise-videos-under-moovv-fit-content-production) | `Low` | Consolidate custom exercise videos under moovv-fit-content-production bucket | `CORE` |
| [CORE-83](https://linear.app/moovv-fit/issue/CORE-83/data-link-existing-videos-to-sh-018-and-sh-030-exercise-ids) | `Low` | Data: Link existing videos to SH_018 and SH_030 exercise IDs | `CORE` |
| [CORE-62](https://linear.app/moovv-fit/issue/CORE-62/evaluate-stainless-sdk-generation-for-partner-video-sdk-api) | `Low` | Evaluate Stainless SDK generation for Partner Video SDK API | `CORE` |
| [CLINIC-10](https://linear.app/moovv-fit/issue/CLINIC-10/long-term-physical-ai-and-computer-vision-roadmap-phase-2-and-3-vision) | `Low` | Long-Term Physical AI & Computer Vision Roadmap (Phase 2 & 3 Vision) | `CLINIC` |
| [CLINIC-11](https://linear.app/moovv-fit/issue/CLINIC-11/cross-border-telehealth-and-compliance-blueprint-uk-hcpc-and-gcc) | `Low` | Cross-Border Telehealth & Compliance Blueprint (UK HCPC & GCC) | `CLINIC` |
| [CLINIC-12](https://linear.app/moovv-fit/issue/CLINIC-12/practice-management-and-os-benchmark-analysis-cortexa-and-spry-pt) | `Low` | Practice Management & OS Benchmark Analysis (Cortexa & SPRY PT) | `CLINIC` |
| [CORE-67](https://linear.app/moovv-fit/issue/CORE-67/annual-apple-distribution-certificate-and-profile-renewal-sept-2027) | `No priority` | Annual Apple Distribution Certificate & Profile Renewal (Sept 2027) | `CORE` |
| [CORE-64](https://linear.app/moovv-fit/issue/CORE-64/automate-testflight-external-beta-review-submission-via-async-linux) | `No priority` | Automate TestFlight External Beta Review Submission via Async Linux Job | `CORE` |
| [CORE-63](https://linear.app/moovv-fit/issue/CORE-63/future-scope-real-time-exercise-recommendation-engine-with-jev) | `No priority` | [Future Scope] Real-Time Exercise Recommendation Engine with Jev | `CORE` |
| [CORE-61](https://linear.app/moovv-fit/issue/CORE-61/featadmin-future-integration-embed-self-test-qa-and-assessment-catalog) | `No priority` | [FEAT/ADMIN] Future Integration: Embed Self-Test QA & Assessment Catalog into moovv-fit-web Admin Portal | `CORE` |
| [CLINIC-41](https://linear.app/moovv-fit/issue/CLINIC-41/kineticage-partner-integration-source-documents) | `No priority` | KineticAge Partner Integration — Source Documents | `CLINIC` |

---
*Generated automatically via `scripts/linear-backlog.py --sync` on 2026-11-06 10:21 UTC.*

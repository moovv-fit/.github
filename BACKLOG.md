# 📋 Moovv Fit — Master Cross-Repo Backlog

> **Canonical Backlog Mirror** synchronized with Linear (`moovv-fit` workspace).  
> **Last Synced:** `2026-11-13 07:04 UTC` • **Total Open Backlog Issues:** `95`  
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

### 🛠️ Spec Implementation Roadmap
For prioritized implementation order of Kiro specs with dependency tracking, see **[docs/SPEC-ROADMAP.md](docs/SPEC-ROADMAP.md)**.

---

## 📊 Backlog Summary by Repository

| Domain | Submodule Path | Issues | Primary Focus |
|---|---|:---:|---|
| **📱 Mobile (iOS & Android)** | [`repos/apps/mobile`](repos/apps/mobile) | **6** | Flutter rehabilitation app, assessment engine, routine player, and pain tracking. |
| **⚙️ Backend Core API & Database** | [`repos/backend/node`](repos/backend/node) | **10** | Node/TypeScript Lambda API, Prisma ORM, Cognito auth, and clinical data models. |
| **🌐 Web Portals (Clinic OS & Admin)** | [`repos/apps/web`](repos/apps/web) | **3** | React 19 clinical portal, appointment booking, patient queue, and chat. |
| **🚀 Landing & Patient Acquisition** | [`repos/apps/landing`](repos/apps/landing) | **2** | Static marketing sites, physician lead funnels, and store/PWA onboarding. |
| **🧪 Autonomous Simulator & Test Harness** | [`repos/platform/simulator`](repos/platform/simulator) | **1** | E2E multi-persona automated test harness, websocket synthetic testing. |
| **🎨 Design System Tokens & UI** | [`repos/platform/design-system`](repos/platform/design-system) | **1** | Svelte 5 / Tailwind v4 canonical components and tokens. |
| **📚 Documentation Portals** | [`repos/docs/technical`](repos/docs/technical) | **1** | Partner developer documentation and clinical specifications. |
| **☁️ Platform Infrastructure & Cross-Repo** | [`repos/infra/cdk`](repos/infra/cdk) | **71** | Shared CDK stacks, CloudFront routing, DNS, auth pools, and cross-cutting platform epics. |

---

## 📦 Detailed Backlog Breakdown

### 📱 Mobile (iOS & Android) (6 issues)
**Path:** [`repos/apps/mobile`](repos/apps/mobile)  
*Flutter rehabilitation app, assessment engine, routine player, and pain tracking.*

| ID | Priority | Title | Team |
|---|:---:|---|:---:|
| [CORE-102](https://linear.app/moovv-fit/issue/CORE-102/implement-talk-to-physio-at-home-lead-capture-and-teleconsultation) | `High` | Implement 'Talk to Physio' At-Home lead capture and Teleconsultation timeslot picker | `CORE` |
| [CORE-89](https://linear.app/moovv-fit/issue/CORE-89/mobile-audit-and-modernize-github-actions-workflows) | `High` | [Mobile] Audit & modernize GitHub Actions workflows | `CORE` |
| [CORE-94](https://linear.app/moovv-fit/issue/CORE-94/mobile-post-launch-framework-and-dependency-upgrades) | `Medium` | [Mobile] Post-Launch Framework & Dependency Upgrades | `CORE` |
| [CORE-173](https://linear.app/moovv-fit/issue/CORE-173/mobile-cicd-sentry-release-steps-use-unset-version-output-no-web) | `Low` | [Mobile CI/CD] Sentry release steps use unset version output; no web source maps | `CORE` |
| [CORE-195](https://linear.app/moovv-fit/issue/CORE-195/mobile-remove-otpphone-debugprint-in-cognito-servicedart-and-redact) | `No priority` | [Mobile] Remove OTP/phone debugPrint in cognito_service.dart and redact query strings in Dio logger | `CORE` |
| [CORE-193](https://linear.app/moovv-fit/issue/CORE-193/mobile-send-session-on-otp-consent-revoke-and-gate-international-otp) | `No priority` | Mobile: send session on OTP consent revoke and gate international OTP to India until ENABLE_MULTI_CHANNEL_OTP | `CORE` |

### ⚙️ Backend Core API & Database (10 issues)
**Path:** [`repos/backend/node`](repos/backend/node)  
*Node/TypeScript Lambda API, Prisma ORM, Cognito auth, and clinical data models.*

| ID | Priority | Title | Team |
|---|:---:|---|:---:|
| [CORE-208](https://linear.app/moovv-fit/issue/CORE-208/fixci-unit-tests-fail-on-main-after-core-135-phase-2-unmocked-dbclient) | `High` | fix(ci): unit tests fail on main after CORE-135 Phase 2 (unmocked db/client env validation) | `CORE` |
| [CORE-96](https://linear.app/moovv-fit/issue/CORE-96/backend-re-enable-and-validate-platform-e2e-tests-on-staging) | `High` | [Backend] Re-enable & Validate Platform E2E Tests on Staging | `CORE` |
| [CORE-95](https://linear.app/moovv-fit/issue/CORE-95/backend-expand-unit-and-integration-test-coverage-to-80percent) | `High` | [Backend] Expand Unit & Integration Test Coverage to 80% | `CORE` |
| [CORE-187](https://linear.app/moovv-fit/issue/CORE-187/email-template-management-ses-s3-for-transactional-customerio-for) | `Medium` | Email Template Management: SES + S3 for Transactional, Customer.io for Marketing | `CORE` |
| [CORE-152](https://linear.app/moovv-fit/issue/CORE-152/chorebackend-clean-up-deprecated-trial-expiration-cron-and-enable) | `Medium` | chore(backend): clean up deprecated trial expiration cron and ENABLE_TRIAL_EXPIRATION flag | `CORE` |
| [CORE-131](https://linear.app/moovv-fit/issue/CORE-131/engine-codify-recommendation-engine-ecr-and-lambda-infrastructure-into) | `Medium` | [Engine] Codify Recommendation Engine ECR and Lambda Infrastructure into CDK | `CORE` |
| [CORE-97](https://linear.app/moovv-fit/issue/CORE-97/backend-implement-unified-v1-api-versioning-strategy-adr-014) | `Medium` | [Backend] Implement Unified /v1/ API Versioning Strategy (ADR-014) | `CORE` |
| [CORE-198](https://linear.app/moovv-fit/issue/CORE-198/rollout-multi-channel-otp-enable-multi-channel-otp-staging-then-prod) | `No priority` | [Rollout] Multi-channel OTP: ENABLE_MULTI_CHANNEL_OTP staging then prod with mobile release | `CORE` |
| [CORE-196](https://linear.app/moovv-fit/issue/CORE-196/auth-save-preferred-otp-channel-to-user-profile-after-auth-n12) | `No priority` | [Auth] Save preferred OTP channel to user profile after auth (N12) | `CORE` |
| [CORE-194](https://linear.app/moovv-fit/issue/CORE-194/backendproduct-pdr-017-opt-out-path-outside-any-login-flow-eg-signed) | `No priority` | [Backend/Product] PDR-017 opt-out path outside any login flow (e.g. signed link) | `CORE` |

### 🌐 Web Portals (Clinic OS & Admin) (3 issues)
**Path:** [`repos/apps/web`](repos/apps/web)  
*React 19 clinical portal, appointment booking, patient queue, and chat.*

| ID | Priority | Title | Team |
|---|:---:|---|:---:|
| [CLINIC-46](https://linear.app/moovv-fit/issue/CLINIC-46/build-30-day-asynchronous-chat-messaging-interface-between) | `High` | Build 30-day asynchronous chat messaging interface between physiotherapist and patient | `CLINIC` |
| [CLINIC-44](https://linear.app/moovv-fit/issue/CLINIC-44/implement-duty-physiotherapist-teleconsultation-timeslot-availability) | `High` | Implement duty physiotherapist teleconsultation timeslot availability and calendar scheduling | `CLINIC` |
| [CORE-99](https://linear.app/moovv-fit/issue/CORE-99/web-evaluate-and-extract-shared-ui-components-to-moovvdesign-system) | `Medium` | [Web] Evaluate and extract shared UI components to @moovv/design-system | `CORE` |

### 🚀 Landing & Patient Acquisition (2 issues)
**Path:** [`repos/apps/landing`](repos/apps/landing)  
*Static marketing sites, physician lead funnels, and store/PWA onboarding.*

| ID | Priority | Title | Team |
|---|:---:|---|:---:|
| [CORE-126](https://linear.app/moovv-fit/issue/CORE-126/release-revert-apple-review-pending-flag-in-store-linksjs-once-app) | `High` | [Release] Revert APPLE_REVIEW_PENDING flag in store-links.js once App Store approves new bundle ID | `CORE` |
| [CORE-115](https://linear.app/moovv-fit/issue/CORE-115/implement-in-home-consultation-lead-routing-webhook-and-ops) | `Medium` | Implement in-home consultation lead routing webhook and ops notification | `CORE` |

### 🧪 Autonomous Simulator & Test Harness (1 issues)
**Path:** [`repos/platform/simulator`](repos/platform/simulator)  
*E2E multi-persona automated test harness, websocket synthetic testing.*

| ID | Priority | Title | Team |
|---|:---:|---|:---:|
| [CORE-98](https://linear.app/moovv-fit/issue/CORE-98/simulator-fix-staging-payment-bypass-and-demo-phone-range-in-backend) | `High` | [Simulator] Fix Staging Payment Bypass & DEMO_PHONE_RANGE in Backend IaC | `CORE` |

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

### ☁️ Platform Infrastructure & Cross-Repo (71 issues)
**Path:** [`repos/infra/cdk`](repos/infra/cdk)  
*Shared CDK stacks, CloudFront routing, DNS, auth pools, and cross-cutting platform epics.*

| ID | Priority | Title | Team |
|---|:---:|---|:---:|
| [CORE-219](https://linear.app/moovv-fit/issue/CORE-219/customerio-integration-review-findings-pr-59-follow-up) | `Urgent` | Customer.io integration review findings (PR #59 follow-up) | `CORE` |
| [CORE-121](https://linear.app/moovv-fit/issue/CORE-121/infra-track-spamhaus-dbl-delisting-for-moovvfit-st7326681) | `Urgent` | [Infra] Track Spamhaus DBL delisting for moovv.fit (ST7326681) | `CORE` |
| [CLINIC-8](https://linear.app/moovv-fit/issue/CLINIC-8/dipp-startup-certification-and-aws-activate-credits-recovery) | `Urgent` | DIPP Startup Certification & AWS Activate Credits Recovery | `CLINIC` |
| [CORE-11](https://linear.app/moovv-fit/issue/CORE-11/enforce-o1-bodypartactiveplan-laterality-lock) | `Urgent` | Enforce O(1) BodyPartActivePlan Laterality Lock | `CORE` |
| [CORE-9](https://linear.app/moovv-fit/issue/CORE-9/implement-production-pgbouncer-rds-proxy-connection-pooling) | `Urgent` | Implement Production PgBouncer / RDS Proxy Connection Pooling | `CORE` |
| [CORE-213](https://linear.app/moovv-fit/issue/CORE-213/ci-release-please-prerelease-pr-overwrites-production-release-pr) | `High` | [CI] Release Please: prerelease PR overwrites production release PR (shared branch) | `CORE` |
| [CORE-202](https://linear.app/moovv-fit/issue/CORE-202/ses-from-address-ssm-parameter-hand-created-must-be-removed-before-cdk) | `High` | SES from-address SSM parameter: hand-created, must be removed before CDK creates it | `CORE` |
| [CORE-190](https://linear.app/moovv-fit/issue/CORE-190/auth-pdr-017-whatsapp-consent-infrastructure) | `High` | [Auth] PDR-017 WhatsApp Consent Infrastructure | `CORE` |
| [CORE-164](https://linear.app/moovv-fit/issue/CORE-164/infra-post-migration-7-day-observation-and-legacy-rds-termination) | `High` | [Infra] Post-Migration 7-Day Observation & Legacy RDS Termination Checklist | `CORE` |
| [CORE-142](https://linear.app/moovv-fit/issue/CORE-142/tech-debt-fix-auth-handler-references-in-global-auth-channels-spec) | `High` | [Tech Debt] Fix auth handler references in global-auth-channels spec | `CORE` |
| [CORE-141](https://linear.app/moovv-fit/issue/CORE-141/tech-debt-fix-users-vs-user-profile-table-references-in-specs) | `High` | [Tech Debt] Fix users vs user_profile table references in specs | `CORE` |
| [CORE-139](https://linear.app/moovv-fit/issue/CORE-139/spec-e2e-simulation-platform-multi-persona-test-harness) | `High` | [Spec] E2E Simulation Platform: Multi-Persona Test Harness | `CORE` |
| [CORE-133](https://linear.app/moovv-fit/issue/CORE-133/infra-codify-shared-data-layer-and-rds-database-stack) | `High` | [Infra] Codify Shared Data Layer & RDS Database Stack | `CORE` |
| [CORE-132](https://linear.app/moovv-fit/issue/CORE-132/infra-codify-shared-network-stack-vpc-subnets-security-groups) | `High` | [Infra] Codify Shared Network Stack (VPC, Subnets, Security Groups) | `CORE` |
| [CORE-130](https://linear.app/moovv-fit/issue/CORE-130/infra-adopt-legacy-cognito-mobile-pool-a-via-cdk-import) | `High` | [Infra] Adopt Legacy Cognito Mobile Pool A via cdk import | `CORE` |
| [CORE-129](https://linear.app/moovv-fit/issue/CORE-129/infra-unmanaged-cloud-infrastructure-adoption-and-migration-adr-001) | `High` | [Infra] Unmanaged Cloud Infrastructure Adoption & Migration (ADR-001) | `CORE` |
| [CORE-87](https://linear.app/moovv-fit/issue/CORE-87/cross-repo-cicd-and-github-actions-modernization-and-dual-org) | `High` | [Cross-Repo] CI/CD & GitHub Actions Modernization and Dual-Org Deployment Alignment | `CORE` |
| [CORE-84](https://linear.app/moovv-fit/issue/CORE-84/abr-add-multi-rendition-hls-output-sdhdfull-hd) | `High` | ABR: Add multi-rendition HLS output (SD/HD/FULL_HD) | `CORE` |
| [CLINIC-51](https://linear.app/moovv-fit/issue/CLINIC-51/web-update-and-ci-enable-the-playwright-e2e-suite-for-the-clinical-and) | `High` | [Web] Update and CI-enable the Playwright E2E suite for the clinical & admin portals | `CLINIC` |
| [CLINIC-5](https://linear.app/moovv-fit/issue/CLINIC-5/whatsapp-adherence-tracking-and-care-plan-recall-workflows) | `High` | WhatsApp Adherence Tracking & Care Plan Recall Workflows | `CLINIC` |
| [CLINIC-6](https://linear.app/moovv-fit/issue/CLINIC-6/session-package-billing-and-razorpay-webhooks-zoho-suite) | `High` | Session Package Billing & Razorpay Webhooks (Zoho Suite) | `CLINIC` |
| [CLINIC-4](https://linear.app/moovv-fit/issue/CLINIC-4/inbound-voice-and-whatsapp-triage-flow-twilioretell-zoho-crm) | `High` | Inbound Voice & WhatsApp Triage Flow (Twilio/Retell + Zoho CRM) | `CLINIC` |
| [CLINIC-1](https://linear.app/moovv-fit/issue/CLINIC-1/kinetic-age-physio-roster-bulk-db-ingestion) | `High` | Kinetic Age Physio Roster Bulk DB Ingestion | `CLINIC` |
| [CORE-16](https://linear.app/moovv-fit/issue/CORE-16/concurrency-and-double-booking-slot-race-condition-assertions) | `High` | Concurrency & Double-Booking Slot Race Condition Assertions | `CORE` |
| [CORE-13](https://linear.app/moovv-fit/issue/CORE-13/human-in-the-loop-hitl-verification-queue-and-48h-sla-escalation) | `High` | Human-in-the-Loop (HITL) Verification Queue & 48h SLA Escalation | `CORE` |
| [CORE-12](https://linear.app/moovv-fit/issue/CORE-12/decouple-four-bucket-entitlement-engine) | `High` | Decouple Four-Bucket Entitlement Engine | `CORE` |
| [CORE-8](https://linear.app/moovv-fit/issue/CORE-8/consolidate-170-sam-lambdas-to-ecs-fargate-fastifynode-20) | `High` | Consolidate 170+ SAM Lambdas to ECS Fargate (Fastify/Node 20) | `CORE` |
| [CORE-207](https://linear.app/moovv-fit/issue/CORE-207/mobile-add-widget-tests-and-device-testing-for-video-assessment) | `Medium` | [Mobile] Add widget tests and device testing for video assessment feature | `CORE` |
| [CORE-204](https://linear.app/moovv-fit/issue/CORE-204/backend-add-server-side-rom-score-validation-for-video-assessments) | `Medium` | [Backend] Add server-side ROM score validation for video assessments | `CORE` |
| [CORE-200](https://linear.app/moovv-fit/issue/CORE-200/mobile-integrate-app-links-package-for-deep-link-utm-capture-on) | `Medium` | Mobile: Integrate app_links package for deep link UTM capture on iOS/Android | `CORE` |
| [CORE-192](https://linear.app/moovv-fit/issue/CORE-192/mobile-integrate-app-links-package-for-native-deep-link-utm-capture) | `Medium` | [Mobile] Integrate app_links package for native deep link UTM capture | `CORE` |
| [CORE-162](https://linear.app/moovv-fit/issue/CORE-162/backend-single-fcm-token-deletion-endpoint-for-device-specific) | `Medium` | [Backend] Single FCM token deletion endpoint for device-specific deregistration | `CORE` |
| [CORE-158](https://linear.app/moovv-fit/issue/CORE-158/physical-ai-personal-health-coach-agent-behavioral-guidance) | `Medium` | [Physical AI] Personal Health Coach Agent - Behavioral Guidance | `CORE` |
| [CORE-157](https://linear.app/moovv-fit/issue/CORE-157/physical-ai-health-domain-expert-agent-medical-knowledge-integration) | `Medium` | [Physical AI] Health Domain Expert Agent - Medical Knowledge Integration | `CORE` |
| [CORE-156](https://linear.app/moovv-fit/issue/CORE-156/physical-ai-data-scientist-agent-longitudinal-health-analytics) | `Medium` | [Physical AI] Data Scientist Agent - Longitudinal Health Analytics | `CORE` |
| [CORE-140](https://linear.app/moovv-fit/issue/CORE-140/tech-debt-rename-adr-025-to-adr-027-third-party-integration) | `Medium` | [Tech Debt] Rename ADR-025 to ADR-027 (Third-Party Integration Abstraction) | `CORE` |
| [CORE-134](https://linear.app/moovv-fit/issue/CORE-134/infra-codify-iam-release-roles-github-oidc-and-shared-storage-stacks) | `Medium` | [Infra] Codify IAM Release Roles, GitHub OIDC & Shared Storage Stacks | `CORE` |
| [CORE-82](https://linear.app/moovv-fit/issue/CORE-82/content-gap-50-exercises-from-ka-mapping-have-no-video-equivalent) | `Medium` | Content Gap: 50 exercises from KA mapping have no video equivalent | `CORE` |
| [CORE-81](https://linear.app/moovv-fit/issue/CORE-81/crashlytics-test-healthcheck) | `Medium` | [Crashlytics] Test Healthcheck | `CORE` |
| [CLINIC-49](https://linear.app/moovv-fit/issue/CLINIC-49/sdk-treatment-plan-import-api-phase-2) | `Medium` | [SDK] Treatment Plan Import API (Phase 2) | `CLINIC` |
| [CLINIC-48](https://linear.app/moovv-fit/issue/CLINIC-48/sdk-partner-plan-management-and-billing-dashboard-phase-2) | `Medium` | [SDK] Partner Plan Management & Billing Dashboard (Phase 2) | `CLINIC` |
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
| [CORE-206](https://linear.app/moovv-fit/issue/CORE-206/backend-add-sql-batch-insert-comment-for-kinematic-frame-handler) | `Low` | [Backend] Add SQL batch insert comment for kinematic frame handler | `CORE` |
| [CORE-205](https://linear.app/moovv-fit/issue/CORE-205/backend-add-endpoint-level-rate-limiting-for-kinematic-telemetry-api) | `Low` | [Backend] Add endpoint-level rate limiting for kinematic telemetry API | `CORE` |
| [CORE-201](https://linear.app/moovv-fit/issue/CORE-201/docs-mark-core-119-complete-in-backlog-plan-and-update-marketing-infra) | `Low` | Docs: Mark CORE-119 complete in backlog plan and update marketing-infra spec | `CORE` |
| [CORE-86](https://linear.app/moovv-fit/issue/CORE-86/consolidate-custom-exercise-videos-under-moovv-fit-content-production) | `Low` | Consolidate custom exercise videos under moovv-fit-content-production bucket | `CORE` |
| [CORE-83](https://linear.app/moovv-fit/issue/CORE-83/data-link-existing-videos-to-sh-018-and-sh-030-exercise-ids) | `Low` | Data: Link existing videos to SH_018 and SH_030 exercise IDs | `CORE` |
| [CLINIC-50](https://linear.app/moovv-fit/issue/CLINIC-50/sdk-exercise-alias-management-phase-3) | `Low` | [SDK] Exercise Alias Management (Phase 3) | `CLINIC` |
| [CORE-62](https://linear.app/moovv-fit/issue/CORE-62/evaluate-stainless-sdk-generation-for-partner-video-sdk-api) | `Low` | Evaluate Stainless SDK generation for Partner Video SDK API | `CORE` |
| [CLINIC-10](https://linear.app/moovv-fit/issue/CLINIC-10/long-term-physical-ai-and-computer-vision-roadmap-phase-2-and-3-vision) | `Low` | Long-Term Physical AI & Computer Vision Roadmap (Phase 2 & 3 Vision) | `CLINIC` |
| [CLINIC-11](https://linear.app/moovv-fit/issue/CLINIC-11/cross-border-telehealth-and-compliance-blueprint-uk-hcpc-and-gcc) | `Low` | Cross-Border Telehealth & Compliance Blueprint (UK HCPC & GCC) | `CLINIC` |
| [CLINIC-12](https://linear.app/moovv-fit/issue/CLINIC-12/practice-management-and-os-benchmark-analysis-cortexa-and-spry-pt) | `Low` | Practice Management & OS Benchmark Analysis (Cortexa & SPRY PT) | `CLINIC` |
| [CORE-203](https://linear.app/moovv-fit/issue/CORE-203/auth-self-asserted-whatsapp-consent-grant-activate-only-after-otp) | `No priority` | [Auth] Self-asserted WhatsApp consent grant: activate only after OTP verify (blocks enabling WhatsApp) | `CORE` |
| [CORE-197](https://linear.app/moovv-fit/issue/CORE-197/infra-host-aasa-and-assetlinksjson-enable-associated-domains-device) | `No priority` | [Infra] Host AASA and assetlinks.json, enable Associated Domains, device-check deep links (N7) | `CORE` |
| [CORE-67](https://linear.app/moovv-fit/issue/CORE-67/annual-apple-distribution-certificate-and-profile-renewal-sept-2027) | `No priority` | Annual Apple Distribution Certificate & Profile Renewal (Sept 2027) | `CORE` |
| [CORE-64](https://linear.app/moovv-fit/issue/CORE-64/automate-testflight-external-beta-review-submission-via-async-linux) | `No priority` | Automate TestFlight External Beta Review Submission via Async Linux Job | `CORE` |
| [CORE-63](https://linear.app/moovv-fit/issue/CORE-63/future-scope-real-time-exercise-recommendation-engine-with-jev) | `No priority` | [Future Scope] Real-Time Exercise Recommendation Engine with Jev | `CORE` |
| [CORE-61](https://linear.app/moovv-fit/issue/CORE-61/featadmin-future-integration-embed-self-test-qa-and-assessment-catalog) | `No priority` | [FEAT/ADMIN] Future Integration: Embed Self-Test QA & Assessment Catalog into moovv-fit-web Admin Portal | `CORE` |
| [CLINIC-41](https://linear.app/moovv-fit/issue/CLINIC-41/kineticage-partner-integration-source-documents) | `No priority` | KineticAge Partner Integration — Source Documents | `CLINIC` |

---
*Generated automatically via `scripts/linear-backlog.py --sync` on 2026-11-13 07:04 UTC.*

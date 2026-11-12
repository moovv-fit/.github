# 🛠️ Kiro Spec Implementation Roadmap

> **Prioritized implementation order** for all Kiro-format specs across the platform.  
> Each spec is tracked as a Linear issue. Dependencies are explicit — downstream specs should not start until their upstream dependencies complete.

## Implementation Phases

### Phase 0: Clinical Triage & Review (Urgent)
*Critical clinical workflow features for physio efficiency and patient safety.*

| Order | Linear Issue | Spec | Repo | Dependencies | Effort | Status |
|:---:|---|---|---|---|:---:|:---:|
| 0.1 | [CLINIC-43](https://linear.app/moovv-fit/issue/CLINIC-43) | [triage-interface](../repos/apps/web/.agents/specs/triage-interface/) | `apps/web` | — | `M` | 📋 Spec Created |
| 0.2 | [CLINIC-45](https://linear.app/moovv-fit/issue/CLINIC-45) | [plan-review-workbench](../repos/apps/web/.agents/specs/plan-review-workbench/) | `apps/web` | CLINIC-43 | `L` | 📋 Spec Created |
| 0.3 | [CORE-85](https://linear.app/moovv-fit/issue/CORE-85) | [clinical-red-flag-triage](../repos/apps/mobile/.agents/specs/clinical-red-flag-triage/) | `apps/mobile` | — | `M` | 📋 Spec Created |

> **Rationale**: CLINIC-43 and CLINIC-45 enable physio plan review workflow (PDR-001 HITL gate). CORE-85 enforces clinical safety boundaries (PDR-001 exclusions: pregnancy, acute fractures).

### Phase 1: Revenue & Payment Foundation (Weeks 1-3)
*Critical path for international expansion and financial compliance.*

| Order | Linear Issue | Spec | Repo | Dependencies | Effort | Status |
|:---:|---|---|---|---|:---:|:---:|
| 1.1 | [CORE-122](https://linear.app/moovv-fit/issue/CORE-122) | [payment-gateway-abstraction](../repos/backend/node/.agents/specs/payment-gateway-abstraction/) | `backend/node` | — | `L` | ✅ Phase 1 Done |
| 1.2 | [CORE-135](https://linear.app/moovv-fit/issue/CORE-135) | [financial-ledger](../repos/backend/node/.agents/specs/financial-ledger/) | `backend/node` | CORE-122 | `XL` | ✅ Phase 1 Done |

> **Phase 1 Merged**: PR #57 (2026-11-09) — Interface, RazorpayAdapter, Factory, Handler migration, LedgerService, Prisma schema, seed accounts.
> **Phase 2**: Webhook→ledger integration (Razorpay, Apple IAP), reconciliation reporting, integration tests. No external dependencies.
> **Phase 3**: Zoho Books sync worker. Depends on CLINIC-47 (shared OAuth patterns).

### Phase 2: Global Auth & Partner Platform (Weeks 2-4)
*Enables multi-country expansion and B2B video SDK revenue.*

| Order | Linear Issue | Spec | Repo | Dependencies | Effort |
|:---:|---|---|---|---|:---:|
| 2.1 | [CORE-123](https://linear.app/moovv-fit/issue/CORE-123) | [global-auth-channels](../repos/backend/node/.agents/specs/global-auth-channels/) | `backend/node` | — | `M` |
| 2.2 | [CLINIC-2](https://linear.app/moovv-fit/issue/CLINIC-2) | [partner-video-sdk](../repos/backend/node/.agents/specs/partner-video-sdk/) | `backend/node` | — | `L` |

### Phase 3: CRM & Marketing Infrastructure (Weeks 4-6)
*Backend services must complete before mobile/web consumers.*

| Order | Linear Issue | Spec | Repo | Dependencies | Effort |
|:---:|---|---|---|---|:---:|
| 3.1 | [CLINIC-47](https://linear.app/moovv-fit/issue/CLINIC-47) | [crm-gateway-zoho](../repos/backend/node/.agents/specs/crm-gateway-zoho/) | `backend/node` | — | `M` |
| 3.2 | [CORE-120](https://linear.app/moovv-fit/issue/CORE-120) | [marketing-infra-backend](../repos/backend/node/.agents/specs/marketing-infra-backend/) | `backend/node` | CLINIC-47 | `M` |
| 3.3 | [CORE-119](https://linear.app/moovv-fit/issue/CORE-119) | [marketing-infra](../repos/apps/mobile/.agents/specs/marketing-infra/) | `apps/mobile` | CORE-120 | `S` |

### Phase 4: Free Content & Engagement (Weeks 5-7)
*Growth lever — backend before mobile consumer.*

| Order | Linear Issue | Spec | Repo | Dependencies | Effort | Status |
|:---:|---|---|---|---|:---:|:---:|
| 4.1 | [CORE-136](https://linear.app/moovv-fit/issue/CORE-136) | [free-content-backend](../repos/backend/node/.agents/specs/free-content-backend/) | `backend/node` | — | `M` | ✅ Done |
| 4.2 | [CORE-137](https://linear.app/moovv-fit/issue/CORE-137) | [free-content-mobile](../repos/apps/mobile/.agents/specs/free-content-mobile/) | `apps/mobile` | CORE-136 | `M` | 🔓 Unblocked |

> **CORE-136 Merged**: PR #54 (2026-11-09) — Free content access, physio review tier, promotions, product catalog.

### Phase 5: Platform Quality & Testing (Ongoing)
*Horizontal capabilities that support all other specs.*

| Order | Linear Issue | Spec | Repo | Dependencies | Effort |
|:---:|---|---|---|---|:---:|
| 5.1 | [CORE-139](https://linear.app/moovv-fit/issue/CORE-139) | [e2e-simulation-platform](../repos/platform/simulator/.agents/specs/e2e-simulation-platform/) | `platform/simulator` | — | `L` |
| 5.2 | [CORE-138](https://linear.app/moovv-fit/issue/CORE-138) | [ios-release-pipeline](../repos/apps/mobile/.agents/specs/ios-release-pipeline/) | `apps/mobile` | — | `M` |

## Dependency Graph

```
CLINIC-43 (triage-interface) ──► CLINIC-45 (plan-review-workbench)

CORE-85 (clinical-red-flag-triage) ──► (standalone clinical safety)

CORE-122 (payment-gateway) ──► CORE-135 (financial-ledger)

CLINIC-47 (crm-zoho) ──► CORE-120 (marketing-backend) ──► CORE-119 (marketing-mobile)

CORE-136 (free-content-backend) ──► CORE-137 (free-content-mobile)

CORE-123 (global-auth) ──► (enables all international features)
CLINIC-2 (partner-video-sdk) ──► (standalone B2B revenue)
CORE-139 (e2e-simulation) ──► (validates all specs)
```

## Effort Key

| Size | Estimate | Typical Scope |
|:---:|:---:|---|
| `S` | 1-2 days | Single service, <5 files |
| `M` | 3-5 days | Multi-file, requires integration testing |
| `L` | 1-2 weeks | Cross-cutting, multiple services, DB migrations |
| `XL` | 2-3 weeks | Major architectural change, data migration |

## Spec Locations Quick Reference

```
repos/
├── apps/web/.agents/specs/
│   ├── plan-review-workbench/     → CLINIC-45
│   └── triage-interface/          → CLINIC-43
├── apps/mobile/.agents/specs/
│   ├── clinical-red-flag-triage/  → CORE-85
│   ├── free-content-mobile/       → CORE-137
│   ├── ios-release-pipeline/      → CORE-138
│   └── marketing-infra/           → CORE-119
├── backend/node/.agents/specs/
│   ├── crm-gateway-zoho/          → CLINIC-47
│   ├── financial-ledger/          → CORE-135
│   ├── free-content-backend/      → CORE-136
│   ├── global-auth-channels/      → CORE-123
│   ├── marketing-infra-backend/   → CORE-120
│   ├── partner-video-sdk/         → CLINIC-2
│   └── payment-gateway-abstraction/ → CORE-122
└── platform/simulator/.agents/specs/
    └── e2e-simulation-platform/   → CORE-139
```

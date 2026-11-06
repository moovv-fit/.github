# 🛠️ Kiro Spec Implementation Roadmap

> **Prioritized implementation order** for all Kiro-format specs across the platform.  
> Each spec is tracked as a Linear issue. Dependencies are explicit — downstream specs should not start until their upstream dependencies complete.

## Implementation Phases

### Phase 1: Revenue & Payment Foundation (Weeks 1-3)
*Critical path for international expansion and financial compliance.*

| Order | Linear Issue | Spec | Repo | Dependencies | Effort |
|:---:|---|---|---|---|:---:|
| 1.1 | [CORE-122](https://linear.app/moovv-fit/issue/CORE-122) | [payment-gateway-abstraction](../repos/backend/node/.agents/specs/payment-gateway-abstraction/) | `backend/node` | — | `L` |
| 1.2 | [CORE-135](https://linear.app/moovv-fit/issue/CORE-135) | [financial-ledger](../repos/backend/node/.agents/specs/financial-ledger/) | `backend/node` | CORE-122 | `XL` |

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

| Order | Linear Issue | Spec | Repo | Dependencies | Effort |
|:---:|---|---|---|---|:---:|
| 4.1 | [CORE-136](https://linear.app/moovv-fit/issue/CORE-136) | [free-content-backend](../repos/backend/node/.agents/specs/free-content-backend/) | `backend/node` | — | `M` |
| 4.2 | [CORE-137](https://linear.app/moovv-fit/issue/CORE-137) | [free-content-mobile](../repos/apps/mobile/.agents/specs/free-content-mobile/) | `apps/mobile` | CORE-136 | `M` |

### Phase 5: Platform Quality & Testing (Ongoing)
*Horizontal capabilities that support all other specs.*

| Order | Linear Issue | Spec | Repo | Dependencies | Effort |
|:---:|---|---|---|---|:---:|
| 5.1 | [CORE-139](https://linear.app/moovv-fit/issue/CORE-139) | [e2e-simulation-platform](../repos/platform/simulator/.agents/specs/e2e-simulation-platform/) | `platform/simulator` | — | `L` |
| 5.2 | [CORE-138](https://linear.app/moovv-fit/issue/CORE-138) | [ios-release-pipeline](../repos/apps/mobile/.agents/specs/ios-release-pipeline/) | `apps/mobile` | — | `M` |

## Dependency Graph

```
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
├── backend/node/.agents/specs/
│   ├── crm-gateway-zoho/          → CLINIC-47
│   ├── financial-ledger/          → CORE-135
│   ├── free-content-backend/      → CORE-136
│   ├── global-auth-channels/      → CORE-123
│   ├── marketing-infra-backend/   → CORE-120
│   ├── partner-video-sdk/         → CLINIC-2
│   └── payment-gateway-abstraction/ → CORE-122
├── apps/mobile/.agents/specs/
│   ├── free-content-mobile/       → CORE-137
│   ├── ios-release-pipeline/      → CORE-138
│   └── marketing-infra/           → CORE-119
└── platform/simulator/.agents/specs/
    └── e2e-simulation-platform/   → CORE-139
```

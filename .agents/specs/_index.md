# Spec Index

> **Auto-generated** — All specs across submodules, symlinked for unified access.
> 
> Last updated: 2026-11-13

## Active Specs

### Backend (`repos/backend/node`)

| Spec | Linear | Status | Description |
|------|--------|--------|-------------|
| [crm-gateway-zoho](./crm-gateway-zoho/) | [CLINIC-47](https://linear.app/moovv-fit/issue/CLINIC-47) | ✅ Done | Zoho CRM integration via MessagingGateway |
| [financial-ledger](./financial-ledger/) | [CORE-135](https://linear.app/moovv-fit/issue/CORE-135) | ✅ Done | Double-entry financial ledger (ADR-030) |
| [free-content-backend](./free-content-backend/) | [CORE-136](https://linear.app/moovv-fit/issue/CORE-136) | ✅ Done | PDR-016 backend: trial removal, review status, plan limits |
| [global-auth-channels](./global-auth-channels/) | [CORE-123](https://linear.app/moovv-fit/issue/CORE-123) | ✅ Done | Multi-channel OTP (SMS/WhatsApp/Email) |
| [marketing-infra-backend](./marketing-infra-backend/) | [CORE-120](https://linear.app/moovv-fit/issue/CORE-120) | ✅ Done | FCM token endpoints, MessagingGateway, Customer.io |
| [messaging-gateway](./messaging-gateway/) | — | 🚧 Active | Provider-agnostic messaging abstraction |
| [payment-gateway-abstraction](./payment-gateway-abstraction/) | [CORE-122](https://linear.app/moovv-fit/issue/CORE-122) | ✅ Done | Multi-provider payment abstraction |
| [testing-strategy-backend](./testing-strategy-backend/) | — | 📋 Draft | Backend testing patterns and E2E strategy |

### Mobile (`repos/apps/mobile`)

| Spec | Linear | Status | Description |
|------|--------|--------|-------------|
| [clinical-red-flag-triage-mobile](./clinical-red-flag-triage-mobile/) | [CORE-85](https://linear.app/moovv-fit/issue/CORE-85) | 🚧 Active | Clinical safety boundaries (PDR-001 exclusions) |
| [free-content-mobile](./free-content-mobile/) | [CORE-137](https://linear.app/moovv-fit/issue/CORE-137) | ✅ Done | PDR-016 mobile: trial UI removal, review banners, plan limits |
| [ios-release-pipeline-mobile](./ios-release-pipeline-mobile/) | [CORE-138](https://linear.app/moovv-fit/issue/CORE-138) | ✅ Done | Fastlane Match, TestFlight, StoreKit IAP |
| [marketing-infra-mobile](./marketing-infra-mobile/) | [CORE-119](https://linear.app/moovv-fit/issue/CORE-119) | ✅ Done | FCM setup, push channels, soft-ask flow |

### Web (`repos/apps/web`)

| Spec | Linear | Status | Description |
|------|--------|--------|-------------|
| *No active specs* | — | — | See [SPEC-ROADMAP.md](../../../docs/SPEC-ROADMAP.md) for planned work |

### Infra (`repos/infra/cdk`)

| Spec | Linear | Status | Description |
|------|--------|--------|-------------|
| *No active specs* | — | — | Infrastructure specs managed via ADRs |

### Platform (`repos/platform/simulator`)

| Spec | Linear | Status | Description |
|------|--------|--------|-------------|
| e2e-simulation-platform | [CORE-139](https://linear.app/moovv-fit/issue/CORE-139) | 📋 Backlog | Multi-persona E2E test harness |

---

## Status Legend

| Status | Meaning |
|--------|---------|
| 📋 Draft | Requirements defined, not yet implementing |
| 📋 Backlog | Planned but not started |
| 🚧 Active | Implementation in progress |
| ✅ Done | All tasks complete, awaiting PDR absorption |
| 🗄️ Archived | PDR created, spec deleted |

---

## Naming Convention

```
{feature}-{domain}
```

Examples:
- `free-content-backend` — Backend implementation of free content feature
- `free-content-mobile` — Mobile implementation of same feature
- `clinical-red-flag-triage-mobile` — Mobile-only clinical safety feature

---

## Adding a New Spec

1. Create spec in submodule: `repos/{domain}/.agents/specs/{feature}-{domain}/`
2. Add `requirements.md`, `design.md`, `tasks.md`
3. Create Linear issue with label `spec`
4. Run `spec-sync` hook or manually symlink to master `.agents/specs/`
5. Update this index

---

## References

- [SPEC-ROADMAP.md](../../../docs/SPEC-ROADMAP.md) — Implementation phases and dependencies
- [spec-lifecycle.md](../steering/spec-lifecycle.md) — Completion and PDR absorption process
- [Product Manifest](../../../repos/docs/product/docs/product/manifest.md) — PDR index

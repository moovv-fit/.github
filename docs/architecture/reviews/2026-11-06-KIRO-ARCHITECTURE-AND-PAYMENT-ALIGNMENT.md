# Discussion & Architecture Review: Payment Strategy, Product Catalog Abstraction, and Codebase Alignments

**Author**: Orchestrator Agent (via Antigravity)  
**Target Audience**: Kiro (Lead Architect / Backend & Mobile Steering)  
**Date**: 2026-11-06  
**Status**: For Discussion & Alignment  

---

## 1. Executive Summary

This document consolidates our architectural review of the recent specs and Architecture Decision Records (ADRs) across `repos/backend/node` and `repos/apps/mobile`.

While the **Interface → Adapter → Factory** pattern codified across Messaging, CRM, Payments, and OTP is clean and uniform, we need to address:
1. **Five concrete codebase discrepancies** (including an ADR numbering collision, incorrect table names, and handler misattributions).
2. **Product Catalog & SKU Abstraction**: Moving away from hardcoded SKUs and prices toward a multi-channel catalog model.
3. **Payment Strategy Evaluation**: Deciding between writing a full homegrown payment/subscription engine from scratch versus adopting an established payment orchestration library or mobile entitlement SDK (e.g. Hyperswitch, RevenueCat).

---

## 2. Codebase Discrepancies & Required Fixes

### 2.1 ADR Collision & Index Restoration (ADR-025 → ADR-027)
- **Issue**: `ADR-025-SDK-API-DOCUMENTATION.md` (accepted on 2026-11-02) and `ADR-026-SSM-GITHUB-CREDENTIALS.md` already exist in `repos/backend/node/docs/architecture/adr/`.
- **Conflict**: The newly added `ADR-025-THIRD-PARTY-INTEGRATION-ABSTRACTION.md` collided with ADR-025. In `repos/backend/node/docs/architecture/adr/README.md`, lines 27 and 29 duplicated the new entry, overwriting the SDK documentation ADR and omitting ADR-026.
- **Action**:
  - Rename `ADR-025-THIRD-PARTY-INTEGRATION-ABSTRACTION.md` → **`ADR-027-THIRD-PARTY-INTEGRATION-ABSTRACTION.md`**.
  - In `README.md`, restore `025` (SDK API Documentation), keep `026` (SSM GitHub Credentials), and append `027` (Third-Party Integration Abstraction).
  - Update cross-references in all specs from `ADR-025` to `ADR-027`.

### 2.2 Table & Model Names: `users` vs `user_profile`
- **Issue**: In [`marketing-infra-backend`](../../repos/backend/node/.agents/specs/marketing-infra-backend/) (`user_device_tokens`), [`free-content-backend`](../../repos/backend/node/.agents/specs/free-content-backend/) (CORE-121 Promotions), and [`crm-gateway-zoho`](../../repos/backend/node/.agents/specs/crm-gateway-zoho/), SQL migrations reference `REFERENCES users(id) ON DELETE CASCADE` and models import `User.ts`.
- **Reality**: In this PostgreSQL database, the user table is named **`user_profile`** (singular) and the model is [`src/database/models/core/UserProfile.ts`](file:///mnt/workspace/src/moovv-fit/repos/backend/node/src/database/models/core/UserProfile.ts). There is no `users` table or `User` model. Running those migrations will fail with `relation "users" does not exist`.
- **Action**: Update all migration schemas to `REFERENCES user_profile(id)` and update Sequelize models to import `UserProfile`.

### 2.3 Auth OTP Architecture: API Gateway Handlers vs Cognito Triggers
- **Issue**: [`global-auth-channels`](../../repos/backend/node/.agents/specs/global-auth-channels/) (§3.6) references `cognito-define-auth-challenge.ts` and `cognito-create-auth-challenge.ts`.
- **Reality**: Those files do not exist in this backend repo. In Moovv, phone auth is handled via API Gateway Lambda endpoints:
  - [`src/handlers/auth-initiate.ts`](file:///mnt/workspace/src/moovv-fit/repos/backend/node/src/handlers/auth-initiate.ts): Generates and stores OTP via `generateAndStoreOtp()`, sends SMS via `sendNotification('OTP', ...)`, and passes the OTP to Cognito via `ClientMetadata` for Custom Auth challenge verification.
  - [`src/handlers/auth-resend-otp.ts`](file:///mnt/workspace/src/moovv-fit/repos/backend/node/src/handlers/auth-resend-otp.ts): Handles resends and rate limits.
  - Phone validation in [`src/shared/utils/phoneValidation.ts`](file:///mnt/workspace/src/moovv-fit/repos/backend/node/src/shared/utils/phoneValidation.ts) currently enforces India-only (`+91`) and returns `COUNTRY_NOT_SUPPORTED` for other country codes.
- **Action**: Update the spec so the `OtpChannel` abstraction (SMS, WhatsApp, Email) plugs directly into `auth-initiate.ts`, `auth-resend-otp.ts`, and `phoneValidation.ts`.

### 2.4 Existing Payment Handlers: Domain-Separated vs Unified
- **Issue**: [`payment-gateway-abstraction`](../../repos/backend/node/.agents/specs/payment-gateway-abstraction/) and [`free-content-backend`](../../repos/backend/node/.agents/specs/free-content-backend/) reference generic `create-razorpay-order.ts` and `razorpay-webhook.ts`.
- **Reality**: Orders are currently split across two separate business domains:
  - **Platform Subscriptions**: `patient-create-platform-sub-order.ts` + `patient-platform-sub-razorpay-webhook.ts`
  - **Telehealth**: `patient-create-telehealth-order.ts` + `patient-telehealth-razorpay-webhook.ts`
- **Action**: Clarify whether `PaymentGateway` wraps these existing domain handlers as-is, or whether CORE-150 explicitly consolidates them into a unified payment order service.

### 2.5 CRM Event Hook Handlers
- **Issue**: [`crm-gateway-zoho`](../../repos/backend/node/.agents/specs/crm-gateway-zoho/) references `cognito-post-confirmation.ts` for patient registration and `clinic-registration.ts` for clinic creation.
- **Reality**:
  - Patient creation occurs on first login verification in [`src/handlers/auth-verify.ts`](file:///mnt/workspace/src/moovv-fit/repos/backend/node/src/handlers/auth-verify.ts) (`UserProfile.create` when `isNewUser = true`).
  - Clinic creation occurs in [`src/handlers/org-create-clinic.ts`](file:///mnt/workspace/src/moovv-fit/repos/backend/node/src/handlers/org-create-clinic.ts).
- **Action**: Target `auth-verify.ts` and `org-create-clinic.ts` as the trigger points for emitting `CrmGateway` events.

---

## 3. Product Catalog, Multi-Channel SKUs & Pricing Abstraction

### 3.1 The Problem: Hardcoded SKUs and Coupled Payment Rails
Right now:
- [`free-content-backend`](../../repos/backend/node/.agents/specs/free-content-backend/) (CORE-121 Promotions) models `eligible_products` as a raw `JSONB` array of strings (e.g. `['PHYSIO_REVIEW']`).
- [`free-content-mobile`](../../repos/apps/mobile/.agents/specs/free-content-mobile/) (CORE-104) hardcodes the CTA: `"Get Physio Review — ₹299"`.
- The checkout assumes a single path: Mobile App → direct Razorpay order.

In reality, Moovv products (Physio Reviews, Fit Subscriptions, Telehealth consultations) must be sold across **multiple channels**, each requiring different payment rails and store compliance:
- **Mobile (iOS)**: In-app digital goods require Apple In-App Purchase (StoreKit), or compliant web checkout links.
- **Mobile (Android)**: Requires Google Play Billing or external gateway where permitted.
- **Web Patient Portal**: Direct Razorpay (India) / Stripe (International).
- **WhatsApp / Conversational**: Dynamic payment links via Razorpay / Stripe.
- **Clinic Portal (B2B2C)**: Corporate billing, internal credits, or invoicing.

### 3.2 Proposed Architecture: Product Catalog & Channel Mapping

#### A. Data-Driven Product Catalog (`Product` / `ProductSku`)
```typescript
interface ProductSku {
  sku: string;                    // e.g. 'SKU_PHYSIO_REVIEW_ASYNC'
  name: string;
  itemType: 'ONE_TIME_SERVICE' | 'RECURRING_SUBSCRIPTION' | 'CREDIT_PACK';
  basePrices: Record<string, number>; // { INR: 49900, USD: 1999 } (in smallest currency unit)
  fulfillmentType: 'ENQUEUE_PHYSIO_REVIEW' | 'ACTIVATE_SUBSCRIPTION' | 'BOOK_TELEHEALTH';
  metadata: {
    title: string;
    description: string;
    slaHours: number;
    requiresPlanId: boolean;
  };
  isActive: boolean;
}
```

#### B. Channel-Aware Payment Resolution (`PaymentGatewayFactory`)
The factory should resolve the payment adapter not merely by a static environment variable, but based on `(channel, region, sku)`:
```typescript
export interface PaymentContext {
  channel: 'MOBILE_IOS' | 'MOBILE_ANDROID' | 'WEB_PORTAL' | 'WHATSAPP' | 'CLINIC_DESK';
  country: string; // ISO 3166-1 alpha-2 (e.g. 'IN', 'US')
  sku: string;
}

// In PaymentGatewayFactory:
export async function getPaymentGatewayForChannel(context: PaymentContext): Promise<PaymentGateway> {
  if (context.channel === 'MOBILE_IOS' && isDigitalGood(context.sku)) {
    return new AppleIapAdapter();
  }
  if (context.channel === 'WEB_PORTAL') {
    return context.country === 'IN' ? new RazorpayAdapter() : new StripeAdapter();
  }
  // Default fallback
  return new RazorpayAdapter();
}
```

#### C. Dynamic Product Resolution Endpoint for Frontends
Introduce `GET /api/v1/products/:sku?channel=MOBILE_APP&currency=INR&promoCode=WELCOME50`:
- Evaluates active promotions dynamically via `promotionService` (CORE-121).
- Returns display metadata (localized title, strike-through original price, final discounted price, badge text).
- Returns the supported payment gateway identifier and required purchase attributes (e.g., `planId`).
- **Eliminates hardcoded prices and gateway assumptions from mobile and web apps.**

---

## 4. Payment Management & Ledgering: Homegrown vs Library Evaluation

### 4.1 How Payments Work in Moovv Today
Payments do not exclusively live in Razorpay. Moovv maintains database records in:
- `PlatformSubscriptionPaymentOrder.ts`
- `TelehealthPaymentOrder.ts`
- `CustomerPlatformSubscription.ts`
- `Invoice.ts`

However, **lifecycle state, dunning, retry state machines, renewal schedules, and refunds** currently lean heavily on Razorpay-specific webhooks and dashboard features. There is no unified ledger across different payment rails (e.g. Razorpay vs. Apple IAP vs. Stripe).

### 4.2 Homegrown Abstraction vs Established Solutions

| Approach | Architecture | Pros | Cons & Risks |
|---|---|---|---|
| **Option 1: Homegrown Adapter (Current ADR-027)** | Hand-roll `PaymentGateway`, `RazorpayAdapter`, `StripeAdapter`, custom webhook reconciler, and retry queues. | Zero software licensing fees; tailored specifically to our schema. | **High engineering overhead**: multi-currency tax, subscription dunning, proration, and store compliance (Apple/Google) take months to harden. |
| **Option 2: Open-Source Orchestrator (Hyperswitch by Juspay)** | Self-hosted, high-performance open-source routing engine in AWS. Unified API over Razorpay, Stripe, UPI, Cards, etc. | Native India + Global routing; unified dashboard; eliminates multi-gateway code drift; zero vendor lock-in. | Requires hosting a containerized service in VPC; does not natively handle mobile app store receipt validation. |
| **Option 3: Hybrid / Cross-Platform Entitlements (RevenueCat / Chargebee)** | Use RevenueCat for mobile store compliance (iOS StoreKit + Android Play Billing + Web), or Chargebee for subscription lifecycle. | Solves mobile app store review rejections, receipt validation, and cross-platform entitlements via clean Flutter SDK out of the box. | Small revenue share above threshold; requires webhook integration back to internal database. |

### 4.3 Recommendations
1. **Strictly Scope the Homegrown Abstraction**: If building in-house for MMR, keep `PaymentGateway` as a **thin transport adapter** (`createOrder`, `verifyWebhook`) rather than trying to build a full subscription state/dunning engine in Lambda.
2. **Account for App Store Policies**: If selling digital services inside the iOS/Android app, evaluate a dedicated entitlement layer (like RevenueCat) or provide web-based checkout links to avoid app rejection under Apple Guideline 3.1.1.

---

## 5. Physio Review Checkout Classification (CORE-111 / CORE-121)

For the ₹499/₹299 paid physio review, we evaluate three checkout paths:

1. **Option A: Extend Telehealth Pipeline (`patient-create-telehealth-order.ts`)**
   - *Risk*: Telehealth orders are coupled to real-time calendar slots and synchronous bookings. Physio Review is an **asynchronous** clinical review queue (24h/48h SLA per PDR-016). Not recommended.
2. **Option B: Dedicated Plan Review Order Pipeline (`patient-create-plan-review-order.ts`)**
   - *Approach*: Lightweight order endpoint linked directly to `planId`. Upon webhook receipt, transitions `ExercisePlan.reviewStatus` → `PENDING_PHYSIO_REVIEW` and enqueues into clinical queues.
   - *Verdict*: Clean domain boundary; low risk.
3. **Option C: Unified Checkout via `PaymentGateway` (CORE-150)**
   - *Approach*: Dogfood the new `PaymentGateway` directly: `PaymentGateway.createOrder({ itemType: 'PLAN_REVIEW', itemId: planId, amount, promoCode })`.
   - *Verdict*: Architecturally superior and matches the new design principles.

---

## 6. Action Items & Next Steps for Kiro

1. [CORE-140](https://linear.app/moovv-fit/issue/CORE-140) **Rename ADR**: Change `ADR-025-THIRD-PARTY-INTEGRATION-ABSTRACTION.md` to `ADR-027` and fix `docs/architecture/adr/README.md`.
2. [CORE-141](https://linear.app/moovv-fit/issue/CORE-141) **Update Database Schema References**: Update `users` → `user_profile` in [`marketing-infra-backend`](../../repos/backend/node/.agents/specs/marketing-infra-backend/), [`free-content-backend`](../../repos/backend/node/.agents/specs/free-content-backend/), and [`crm-gateway-zoho`](../../repos/backend/node/.agents/specs/crm-gateway-zoho/).
3. [CORE-142](https://linear.app/moovv-fit/issue/CORE-142) **Fix Auth Handler References**: Align [`global-auth-channels`](../../repos/backend/node/.agents/specs/global-auth-channels/) with `auth-initiate.ts` and `phoneValidation.ts` instead of Cognito challenge triggers.
4. [ ] **Adopt Product Catalog & Dynamic Resolution**: Incorporate dynamic SKU pricing and channel mapping into [`payment-gateway-abstraction`](../../repos/backend/node/.agents/specs/payment-gateway-abstraction/) and [`free-content-mobile`](../../repos/apps/mobile/.agents/specs/free-content-mobile/).
5. [ ] **Confirm Payment Gateway Scope for MMR**: Align on thin transport adapter vs. external orchestrator evaluation.


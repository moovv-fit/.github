# ADR-003: AWS Platform Cost Optimization, Secrets Elimination, and RDS Right-Sizing

**Status**: ✅ Current  
**Last Updated**: 2026-11-10  
**Context / Issues**: CORE-159, CORE-161  

## Context

A comprehensive infrastructure spend and resource utilization audit was conducted across the Moovv Fit production AWS account (`855246887543`, `ap-south-1` Mumbai) for Q3/Q4 2026. The baseline gross monthly spend was ~$112.36/mo (absorbed by AWS promotional credits at $0.00 net). The audit identified four primary areas of operational waste and technical debt before credits expire:

1. **Over-Provisioned RDS Database ($78.10/mo — 69.4% of spend):**
   A legacy unmanaged PostgreSQL 17.10 instance (`moovvfit-database-1`) was provisioned on `db.t3.small` with 300 GB GP3 storage. Actual business data across all databases totaled **~95.5 MB (0.093 GB)**. Over 99.9% of the disk was empty. GP3 disks cannot be downsized in-place.
2. **Orphaned EC2 Compute & EBS ($16.25/mo):**
   A `t3.micro` instance (`i-095b6d239adcda6de`, "moov fit stage") had been completely idle (0.28% CPU) since a September 9 database migration, with an unmanaged root volume and open security group.
3. **Bloated ECR Container Registry (~24.1 GB across 101 images):**
   Historical commit hashes and untagged builds from June/July 2026 were consuming 24.1 GB of container storage with no automated lifecycle expiry.
4. **AWS Secrets Manager Monthly Fees ($0.80/mo):**
   Two secrets (`/moovv-fit/docs/google-client-secret`, `/moovv-fit/docs/azure-client-secret`) incurred $0.40/month per secret.

## Decision

Execute an end-to-end platform infrastructure consolidation, eliminate all Secrets Manager recurring costs, purge obsolete container images, and right-size the platform PostgreSQL database into a CDK-managed construct prior to the upcoming mobile App Store release.

---

### Key Architectural Changes

### 1. EC2 & Orphaned Volume Decommissioning
- Terminated instance `i-095b6d239adcda6de`.
- Purged attached root EBS volume `vol-0754bbddc6d02a431`, deleted orphan SG `sg-0866b193387c1710d` (`launch-wizard-1`), and permanently removed transient EBS snapshot `snap-08e16f754d7fb3ae8`.
- **Immediate Savings:** ~$16.25/mo.

### 2. ECR Container Lifecycle Policy Automation
- Purged 94 untagged/historical image digests across 4 repositories, shrinking container storage from **24.1 GB down to 1.39 GB (94% reduction)**.
- Codified automated ECR lifecycle policies retaining only active production/staging tags (`prod`, `staging`, `health-prod`, `health-staging`, `latest`) and expiring untagged builds after 1 day.

### 3. $0.00 Secrets Management via SSM Parameter Store
- Migrated Partner Developer Docs OAuth client secrets from AWS Secrets Manager to SSM Parameter Store `SecureString` (`/moovv-fit/docs/*`).
- Updated CDK deployment in `repos/docs/technical` (PR #3) to resolve secrets at synth time.
- Permanently deleted all Secrets Manager secrets, bringing total secrets in account `855246887543` to **0**.
- **Immediate Savings:** $0.80/mo ($0.00 ongoing secrets overhead).

### 4. Right-Sized CDK DatabaseStack (CORE-161)
- Codified `DatabaseStack` in `repos/infra/cdk` (PR #12).
- Engine: PostgreSQL 17.10 (ARM64 on Graviton2 `db.t4g.small` at ~$30.40/mo vs $38.00/mo x86).
- Storage: Downsized from 300 GB down to **20 GB GP3** with a **100 GB autogrow ceiling** (~$2.30/mo vs $34.50/mo).
- Master Password: Stored in SSM Parameter Store at `/moovv-fit/shared/db/master-password:1` (`SecureString`) and passed via CloudFormation dynamic reference (zero Secrets Manager fee).
- Network & Security: Default VPC public subnets (accessible by non-VPC Lambdas with $0 NAT Gateway overhead), custom Parameter Group enforcing `rds.force_ssl = 1`.
- Data Migration: Automated pre-migration snapshot (`moovvfit-pre-migration-safety-snapshot`), dumped and restored all 4 user databases (`moovv_fit_production`, `moovv_fit_staging`, `moovvfit_db`, `moovfit-stage-db`) with **100% row count parity**.
- Atomic Cutover: Updated 6 connection strings in SSM with `?connection_limit=1`.
- Verified API latency: **3 ms** database ping on production and staging.
- Decommissioning Phase: Legacy instance `moovvfit-database-1` **stopped** on a 7-day observation countdown before final termination.

---

## Cost Impact Summary

| Resource Category | Pre-Audit Baseline | Post-Optimization | Monthly Gross Reduction |
|---|---|---|:---:|
| **RDS Compute (`t3.small` → `t4g.small`)** | $38.00/mo | $30.40/mo | **-$7.60/mo** |
| **RDS Storage (300 GB → 20 GB GP3)** | $34.50/mo | $2.30/mo | **-$32.20/mo** |
| **EC2 Compute (`t3.micro`)** | $10.44/mo | $0.00/mo | **-$10.44/mo** |
| **EBS Storage & Snapshots** | $5.81/mo | $0.00/mo | **-$5.81/mo** |
| **Amazon ECR Storage (24.1 GB → 1.39 GB)** | $2.41/mo | $0.14/mo | **-$2.27/mo** |
| **AWS Secrets Manager (2 secrets → 0)** | $0.80/mo | $0.00/mo | **-$0.80/mo** |
| **TOTAL GROSS PLATFORM RUN-RATE** | **~$112.36/mo** | **~$53.24/mo** | **-$59.12/mo (52.6% reduction)** |

---

## References
- Notion Executive Review: [AWS Infrastructure Review under MoovvFit HQ](https://app.notion.com/p/AWS-Infrastructure-Utilization-Monthly-Spend-Review-Q3-Q4-2026-41482a257d2381a5aa19f3fb50ddffd7)
- Linear Audit Tracking: [CORE-159](https://linear.app/moovv-fit/issue/CORE-159/infra-aws-infrastructure-utilization-and-monthly-spend-review-with-cto)
- Linear RDS Right-Sizing: [CORE-161](https://linear.app/moovv-fit/issue/CORE-161/infra-cdk-managed-rds-right-sizing-and-migration-300gb-20gb-gp3-pre)
- Docs Secrets PR: [moovv-fit-docs#3](https://github.com/moovv-fit/moovv-fit-docs/pull/3)
- Infra RDS CDK PR: [moovv-fit-infra#12](https://github.com/moovv-fit/moovv-fit-infra/pull/12)
- Repo ADR: `repos/infra/cdk/docs/architecture/adr/ADR-008-RIGHT-SIZED-PLATFORM-RDS-ARCHITECTURE.md`
- Runbook: `repos/infra/cdk/docs/runbooks/RDS-MIGRATION-AND-DECOMMISSIONING-RUNBOOK.md`

# Agent Directive: Add CloudFront OAC Bucket Policy for docs.moovv.fit

> **Linear Ticket:** [CORE-143](https://linear.app/moovv-fit/issue/CORE-143/infrabackend-add-allowdocscloudfrontoac-to-moovv-fit-content-bucket)  
> **Priority:** Urgent (`P1`)  
> **Target Submodule:** `repos/backend/node`  
> **Status:** Top of Backlog (`CORE` Team)

---

## 1. Problem Statement & Root Cause

### Context
Static documentation assets build and deploy successfully via the `Deploy Moovv Docs` workflow ([moovv-fit-docs](file:///mnt/workspace/src/moovv-fit/repos/docs/technical/.github/workflows/deploy.yml)) to `s3://moovv-fit-content-production/docs/`. CloudFront distribution `E2WG3BOVZTWBQK` is pointed to origin path `/docs` on that bucket.

However, visiting `https://docs.moovv.fit` returns:
```http
HTTP/2 403 Forbidden
server: AmazonS3
x-cache: Error from cloudfront
via: 1.1 <id>.cloudfront.net (CloudFront)
```

### Root Cause
Amazon S3 evaluates the bucket policy of `moovv-fit-content-production` on every CloudFront Origin Access Control (OAC) request. When an S3 bucket is private, any object request not explicitly permitted by the bucket policy results in a `403 AccessDenied` from S3.

The central bucket policy defined in [repos/backend/node/lib/stacks/core-stack.ts](file:///mnt/workspace/src/moovv-fit/repos/backend/node/lib/stacks/core-stack.ts#L320-L355) currently grants access only to:
- `AllowAppCloudFrontOAC`: `web/*` and `reports/*` for the App Platform distribution (`E1GQFT37ETXXA3`)
- `AllowLandingCloudFrontOAC`: `web/landing/*` for the Landing Site distribution (`EEEPV3BXEHZLK`)

**It is missing an `AllowDocsCloudFrontOAC` statement permitting `docs/*` for the Docs distribution (`E2WG3BOVZTWBQK`).**

---

## 2. Immediate Direct Hotfix (CLI)

Run the following command with administrative AWS credentials (e.g. `AWS_PROFILE=moovv-fit-ujwal-admin` or `arn:aws:iam::855246887543:role/moovv-fit-github-actions-release-role`) to unblock the live documentation portal immediately:

```bash
# 1. Fetch the existing policy
aws s3api get-bucket-policy \
  --bucket moovv-fit-content-production \
  --query Policy \
  --output text > /tmp/bucket-policy.json

# 2. Append the Docs CloudFront OAC statement into the Statement array
python3 -c '
import json

with open("/tmp/bucket-policy.json") as f:
    policy = json.load(f)

docs_statement = {
    "Sid": "AllowDocsCloudFrontOAC",
    "Effect": "Allow",
    "Principal": {
        "Service": "cloudfront.amazonaws.com"
    },
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::moovv-fit-content-production/docs/*",
    "Condition": {
        "StringEquals": {
            "AWS:SourceArn": "arn:aws:cloudfront::855246887543:distribution/E2WG3BOVZTWBQK"
        }
    }
}

# Remove existing statement if already present to avoid duplication
policy["Statement"] = [s for s in policy.get("Statement", []) if s.get("Sid") != "AllowDocsCloudFrontOAC"]
policy["Statement"].append(docs_statement)

with open("/tmp/bucket-policy-updated.json", "w") as f:
    json.dump(policy, f, indent=2)
'

# 3. Apply the updated policy back to the bucket
aws s3api put-bucket-policy \
  --bucket moovv-fit-content-production \
  --policy file:///tmp/bucket-policy-updated.json

# 4. Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id E2WG3BOVZTWBQK \
  --paths "/*"
```

---

## 3. Permanent Codebase Implementation (CDK)

In `repos/backend/node`:

### File: `lib/stacks/core-stack.ts`
Locate the CloudFront OAC bucket policy section (around line 340) and add the `AllowDocsCloudFrontOAC` statement:

```typescript
      // Docs CloudFront distribution needs access to docs/*
      const docsDistributionId = 
        this.config.cloudfront?.docsDistributionId || 
        (environment === 'production' ? 'E2WG3BOVZTWBQK' : undefined);

      if (docsDistributionId) {
        (this.contentBucket as s3.Bucket).addToResourcePolicy(
          new iam.PolicyStatement({
            sid: 'AllowDocsCloudFrontOAC',
            effect: iam.Effect.ALLOW,
            principals: [new iam.ServicePrincipal('cloudfront.amazonaws.com')],
            actions: ['s3:GetObject'],
            resources: [this.contentBucket.arnForObjects('docs/*')],
            conditions: {
              StringEquals: {
                'AWS:SourceArn': `arn:aws:cloudfront::${this.account}:distribution/${docsDistributionId}`,
              },
            },
          })
        );
      }
```

### File: `lib/config/environments.ts` (or relevant config file)
Ensure `docsDistributionId` is mapped in the cloudfront config:
```typescript
cloudfront: {
  // ...
  docsDistributionId: 'E2WG3BOVZTWBQK',
}
```

---

## 4. Verification & Testing

Verify that public traffic can access the documentation site:

```bash
# Check root page
curl -sI https://docs.moovv.fit | grep -E "HTTP/|server|x-cache"

# Check static index
curl -sI https://docs.moovv.fit/index.html | grep -E "HTTP/|server|x-cache"

# Expected response:
# HTTP/2 200
# server: AmazonS3
# x-cache: Miss from cloudfront / Hit from cloudfront
```

---

## 5. Linear Backlog Synchronization

After successfully applying and verifying the fix:

```bash
# Move Linear issue CORE-143 to Done
linear issue update CORE-143 --state completed

# Refresh master cross-repo BACKLOG.md snapshot
./scripts/linear-backlog.py --sync
```

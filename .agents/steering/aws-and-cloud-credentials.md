---
inclusion: auto
name: AWS and Cloud Credentials
description: "Platform-wide AWS authentication, IAM Identity Center (SSO) profiles, headless login, and credential management."
---

# AWS and Cloud Credentials & Authentication

> **Scope**: Standardized AWS connectivity, SSO profile usage, credential refresh workflows, and cloud environment targeting for all AI agents and developers across the Moovv Fit ecosystem.

---

## ☁️ Standard AWS Profiles & Accounts

All Moovv Fit cloud resources (CDK stacks, S3 release assets, Lambda dispatcher, Spot runner Golden AMIs, SSM Parameter Store) reside in AWS Account `855246887543` in the primary region `ap-south-1` (Mumbai), with global auth/IAM Identity Center anchored in `us-east-1`.

| Profile Name | SSO Role | Primary Use | Who / What Uses It |
| :--- | :--- | :--- | :--- |
| **`moovv-fit-ujwal-admin`** | `AdministratorAccess` | **Primary dev/admin access** for all interactive tasks: CDK synth/diff/deploy, S3 asset inspection, SSM parameter lookup, manual Spot runner runs | AI Agents, Developers, Devbox terminal |
| **`moovv-fit-worker`** | `AdministratorAccess` | **Headless automation profile** for ephemeral CI runners, automated scripts, and scheduled bakes | Ephemeral Spot runners, background worker scripts |

### Profile Configuration (`~/.aws/config`)
```ini
[sso-session moovv-fit]
sso_start_url = https://moovv-fit.awsapps.com/start
sso_region = us-east-1
sso_registration_scopes = sso:account:access
sso_session_duration = 12h

[profile moovv-fit-ujwal-admin]
sso_session = moovv-fit
sso_account_id = 855246887543
sso_role_name = AdministratorAccess
region = ap-south-1
output = json

[profile moovv-fit-worker]
sso_session = moovv-fit
sso_account_id = 855246887543
sso_role_name = AdministratorAccess
region = ap-south-1
output = json
```

---

## 🔑 Authentication Workflow for Agents

### 1. Headless Devbox Login (Device Code Flow)
Remote virtual machines and devboxes do **not** have a local GUI browser. Running a bare `aws sso login` will fail or hang attempting to launch a browser.
Agents and developers must ALWAYS use `--use-device-code`:

```bash
aws sso login --profile moovv-fit-ujwal-admin --use-device-code
```
This prints a verification URL (`https://device.sso.us-east-1.amazonaws.com/`) and a one-time code for browser authorization.

### 2. Setting Default Profile in Shell Sessions
To avoid passing `--profile` to every command or tool:
```bash
export AWS_PROFILE=moovv-fit-ujwal-admin
export AWS_DEFAULT_REGION=ap-south-1
```

### 3. Verifying Active Session
Before executing cloud operations (CDK commands, S3 queries, SSM updates), verify token validity:
```bash
aws sts get-caller-identity --profile moovv-fit-ujwal-admin
```
Expected output:
```json
{
    "UserId": "AROA4N...:ujwal",
    "Account": "855246887543",
    "Arn": "arn:aws:sts::855246887543:assumed-role/AWSReservedSSO_AdministratorAccess_.../ujwal"
}
```

---

## 🛠️ Credential Expiration & Recovery

When AWS CLI or SDK calls encounter:
- `ExpiredToken: The security token included in the request is expired`
- `The SSO session associated with this profile has expired or is invalid`
- `UnauthorizedException`

**Agent Action Protocol:**
1. Do not invent mock keys or edit `.aws/credentials` manually.
2. Run `aws sso login --profile moovv-fit-ujwal-admin --use-device-code`.
3. If token cache is corrupted:
   ```bash
   rm -rf ~/.aws/sso/cache/*
   aws sso login --profile moovv-fit-ujwal-admin --use-device-code
   ```
4. For tools/scripts that cannot parse SSO profiles directly, export temporary STS credentials using the helper:
   ```bash
   eval $(.agents/skills/aws-sso-helper/scripts/export-creds.sh moovv-fit-ujwal-admin)
   ```
5. Refer to `.agents/skills/aws-sso-helper/SKILL.md` for comprehensive diagnosis.


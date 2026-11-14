---
name: aws-sso-helper
description: Diagnoses and refreshes AWS IAM Identity Center (SSO) login tokens across workspaces without requiring a browser on the remote host.
inclusion: auto
---

# AWS SSO Helper

Use this skill whenever AWS CLI calls fail due to expired credentials or missing tokens.

## When to Use

- `ExpiredToken` or `UnauthorizedAccess` errors from AWS CLI
- `The SSO session associated with this profile has expired` messages
- Fresh VM/container setups needing initial authentication
- Switching between AWS accounts or profiles

## Remote VM Authentication

On headless environments (EC2, remote dev containers, SSH sessions), use device code flow:

```bash
aws sso login --profile <profile-name> --use-device-code
```

This outputs a URL and code. Open the URL on any browser (local machine, phone), enter the code, and authenticate.

### Common Profiles

```bash
# Moovv Fit admin access
aws sso login --profile moovv-fit-ujwal-admin --use-device-code

# Default profile (if configured)
aws sso login --use-device-code
```

## Verification

After login, verify credentials are active:

```bash
# Check current identity
aws sts get-caller-identity --profile <profile-name>

# List available profiles
aws configure list-profiles

# Test specific service access
aws s3 ls --profile <profile-name>
```

## Troubleshooting

### Token Expired During Long Session

SSO tokens typically expire after 8-12 hours. Re-run the login command:

```bash
aws sso login --profile <profile-name> --use-device-code
```

### "Profile not found" Error

Check if the profile exists in `~/.aws/config`:

```bash
grep -A5 "\[profile <profile-name>\]" ~/.aws/config
```

If missing, add the SSO configuration:

```ini
[profile my-profile]
sso_start_url = https://my-sso-portal.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
region = us-east-1
output = json
```

### Cache Corruption

Clear the SSO cache and re-authenticate:

```bash
rm -rf ~/.aws/sso/cache/*
aws sso login --profile <profile-name> --use-device-code
```

### Multiple Accounts

When working with multiple AWS accounts, each profile maintains its own token. Switch between them without logging out:

```bash
# Login to first account
aws sso login --profile account-a --use-device-code

# Login to second account (first remains valid)
aws sso login --profile account-b --use-device-code

# Use specific profile for commands
aws s3 ls --profile account-a
aws ec2 describe-instances --profile account-b
```

## Environment Variables

For scripts that don't support `--profile`, export credentials:

```bash
# Use the helper script
eval $(~/.agents/skills/aws-sso-helper/scripts/export-creds.sh <profile-name>)

# Or manually export
export AWS_PROFILE=<profile-name>
```

## Scripts

### `scripts/check-sso-status.sh`

Validates SSO session status and prompts for re-authentication if needed.

### `scripts/export-creds.sh`

Exports temporary credentials as environment variables for tools that don't support SSO profiles natively.

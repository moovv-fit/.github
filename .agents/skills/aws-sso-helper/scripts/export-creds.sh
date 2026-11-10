#!/usr/bin/env bash
#
# export-creds.sh - Export AWS SSO credentials as environment variables
#
# Usage: eval $(export-creds.sh [profile-name])
#
# This script retrieves temporary credentials from an active SSO session
# and outputs them as export statements for tools that don't support
# AWS SSO profiles natively (Docker, Terraform with certain backends, etc.)
#
# Prerequisites:
#   - Active SSO session (run: aws sso login --profile <profile> --use-device-code)
#   - jq installed for JSON parsing

set -euo pipefail

PROFILE="${1:-${AWS_PROFILE:-default}}"

# Redirect all logging to stderr so stdout only contains export statements
log_error() {
    echo "[ERROR] $1" >&2
}

log_info() {
    echo "[INFO] $1" >&2
}

# Check for jq
if ! command -v jq &>/dev/null; then
    log_error "jq is required but not installed. Install with: sudo apt install jq"
    exit 1
fi

# Verify SSO session is active
if ! aws sts get-caller-identity --profile "${PROFILE}" &>/dev/null; then
    log_error "SSO session for profile '${PROFILE}' is expired or invalid"
    log_error "Run: aws sso login --profile ${PROFILE} --use-device-code"
    exit 1
fi

# Extract SSO configuration from profile
CONFIG_FILE="${AWS_CONFIG_FILE:-$HOME/.aws/config}"

get_profile_value() {
    local key="$1"
    awk -v profile="[profile ${PROFILE}]" -v key="${key}" '
        $0 == profile { found=1; next }
        found && /^\[/ { found=0 }
        found && $1 == key { gsub(/^[^=]+=[ \t]*/, ""); print; exit }
    ' "${CONFIG_FILE}"
}

SSO_ACCOUNT_ID=$(get_profile_value "sso_account_id")
SSO_ROLE_NAME=$(get_profile_value "sso_role_name")
SSO_REGION=$(get_profile_value "sso_region")
REGION=$(get_profile_value "region")

if [[ -z "${SSO_ACCOUNT_ID}" || -z "${SSO_ROLE_NAME}" ]]; then
    log_error "Could not extract SSO configuration from profile '${PROFILE}'"
    exit 1
fi

# Find the cached SSO access token
SSO_CACHE_DIR="$HOME/.aws/sso/cache"
ACCESS_TOKEN=""

for cache_file in "${SSO_CACHE_DIR}"/*.json; do
    if [[ -f "${cache_file}" ]]; then
        # Check if token is not expired
        EXPIRY=$(jq -r '.expiresAt // empty' "${cache_file}" 2>/dev/null || true)
        if [[ -n "${EXPIRY}" ]]; then
            EXPIRY_EPOCH=$(date -d "${EXPIRY}" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "${EXPIRY}" +%s 2>/dev/null || echo 0)
            NOW_EPOCH=$(date +%s)
            if [[ ${EXPIRY_EPOCH} -gt ${NOW_EPOCH} ]]; then
                ACCESS_TOKEN=$(jq -r '.accessToken // empty' "${cache_file}" 2>/dev/null || true)
                if [[ -n "${ACCESS_TOKEN}" ]]; then
                    break
                fi
            fi
        fi
    fi
done

if [[ -z "${ACCESS_TOKEN}" ]]; then
    log_error "No valid SSO access token found in cache"
    log_error "Run: aws sso login --profile ${PROFILE} --use-device-code"
    exit 1
fi

# Get role credentials
CREDS=$(aws sso get-role-credentials \
    --account-id "${SSO_ACCOUNT_ID}" \
    --role-name "${SSO_ROLE_NAME}" \
    --access-token "${ACCESS_TOKEN}" \
    --region "${SSO_REGION:-us-east-1}" \
    --output json 2>/dev/null)

if [[ -z "${CREDS}" ]]; then
    log_error "Failed to retrieve role credentials"
    exit 1
fi

# Extract credentials
AWS_ACCESS_KEY_ID=$(echo "${CREDS}" | jq -r '.roleCredentials.accessKeyId')
AWS_SECRET_ACCESS_KEY=$(echo "${CREDS}" | jq -r '.roleCredentials.secretAccessKey')
AWS_SESSION_TOKEN=$(echo "${CREDS}" | jq -r '.roleCredentials.sessionToken')

# Output export statements
log_info "Credentials exported for profile '${PROFILE}' (valid for ~1 hour)"

cat <<EOF
export AWS_ACCESS_KEY_ID='${AWS_ACCESS_KEY_ID}'
export AWS_SECRET_ACCESS_KEY='${AWS_SECRET_ACCESS_KEY}'
export AWS_SESSION_TOKEN='${AWS_SESSION_TOKEN}'
export AWS_DEFAULT_REGION='${REGION:-us-east-1}'
EOF

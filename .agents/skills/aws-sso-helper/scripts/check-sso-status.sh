#!/usr/bin/env bash
#
# check-sso-status.sh - Validate AWS SSO session and prompt for re-auth if needed
#
# Usage: check-sso-status.sh [profile-name]
#
# Exit codes:
#   0 - Session is valid
#   1 - Session expired or invalid (re-auth needed)
#   2 - Profile not found or configuration error

set -euo pipefail

PROFILE="${1:-${AWS_PROFILE:-default}}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if profile exists
if ! aws configure list-profiles 2>/dev/null | grep -q "^${PROFILE}$"; then
    log_error "Profile '${PROFILE}' not found in AWS configuration"
    echo ""
    echo "Available profiles:"
    aws configure list-profiles 2>/dev/null | sed 's/^/  - /'
    exit 2
fi

# Check if this is an SSO profile
if ! grep -A10 "\[profile ${PROFILE}\]" ~/.aws/config 2>/dev/null | grep -q "sso_"; then
    log_warn "Profile '${PROFILE}' does not appear to be an SSO profile"
    echo "This script is designed for AWS IAM Identity Center (SSO) profiles."
    exit 2
fi

# Test credentials by calling STS
echo "Checking SSO session for profile: ${PROFILE}"
echo ""

if aws sts get-caller-identity --profile "${PROFILE}" &>/dev/null; then
    IDENTITY=$(aws sts get-caller-identity --profile "${PROFILE}" --output json 2>/dev/null)
    ACCOUNT=$(echo "${IDENTITY}" | grep -o '"Account": "[^"]*"' | cut -d'"' -f4)
    ARN=$(echo "${IDENTITY}" | grep -o '"Arn": "[^"]*"' | cut -d'"' -f4)
    
    log_info "SSO session is active"
    echo ""
    echo "  Account: ${ACCOUNT}"
    echo "  ARN:     ${ARN}"
    echo ""
    exit 0
else
    log_error "SSO session has expired or is invalid"
    echo ""
    echo "To re-authenticate, run:"
    echo ""
    echo "  aws sso login --profile ${PROFILE} --use-device-code"
    echo ""
    exit 1
fi

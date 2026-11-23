"""
CONTROL TEST: MFA enforcement

Control supported
  SOC 2 CC6.1 (logical access security)
  ISO/IEC 27001:2022 Annex A 8.5 (secure authentication)

What the control requires
  Users who can access company systems must authenticate with more than
  a password. Privileged accounts (admins) matter most.

Evidence checked
  A user export (CSV) with each user's role, status and mfa_enabled flag.
  Sample data is used here. In practice, export this from your identity
  provider (for example Okta or Google Workspace).

Pass / fail
  PASS: every active user has MFA enabled.
  FAIL: one or more active users do not. Failures are listed, and
  admin accounts are flagged as higher risk.

Limitations
  This checks that MFA is turned on for the account. It does not prove
  the user has finished enrolling a device, or that MFA is enforced on
  every application. Suspended users are skipped because they cannot sign in.

Built with AI assistance. Written by a GRC practitioner learning to code.
"""

import csv
import sys
from datetime import date


def load_users(path):
    """Read the user export and return a list of rows."""
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def run_test(users):
    """Return the active users who do NOT have MFA enabled."""
    failures = []
    for user in users:
        if user["status"] != "active":
            continue  # suspended accounts cannot sign in, so skip them
        if user["mfa_enabled"].strip().lower() != "true":
            failures.append(user)
    return failures


def main(path):
    users = load_users(path)
    active = [u for u in users if u["status"] == "active"]
    failures = run_test(users)

    print(f"MFA enforcement test, run on {date.today()}")
    print(f"Active users checked: {len(active)}")

    if not failures:
        print("RESULT: PASS. All active users have MFA enabled.")
        return 0

    print(f"RESULT: FAIL. {len(failures)} active user(s) without MFA:")
    for u in failures:
        note = "  <- HIGH RISK (admin)" if u["role"] == "admin" else ""
        print(f"  - {u['email']} ({u['role']}){note}")
    return 1


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/sample_users.csv"
    sys.exit(main(csv_path))

"""
CONTROL TEST: Stale user accounts

Controls supported
  SOC 2 CC6.2 (prompt removal of access)
  ISO/IEC 27001:2022 Annex A 5.16 (identity management)
  ISO/IEC 27001:2022 Annex A 5.18 (access rights)

What the controls require
  Accounts that are no longer needed should be found and removed or
  disabled promptly, so unused access does not stay open.

Evidence checked
  A login activity export (CSV) with each user's role, status and last
  login date. Sample data is used here. In practice, export this from your
  identity provider (for example Okta or Google Workspace).

Pass / fail
  PASS: every active user has logged in within the allowed number of days.
  FAIL: one or more active users have not. Users who have never logged in
  are also listed. Admin accounts are flagged as higher risk.

Threshold
  90 days is set below as MAX_INACTIVE_DAYS. This is a policy choice, not a
  number taken from SOC 2 or ISO 27001. Change it to match the company's
  access control policy.

Limitations
  Last login only shows when someone signed in, not whether the access is
  still needed. A person who logs in often may still hold access they should
  not have. Suspended accounts are skipped, but a separate check should
  confirm they are removed once they are no longer needed.

Built with AI assistance. Written by a GRC practitioner learning to code.
"""

import csv
import sys
from datetime import date

MAX_INACTIVE_DAYS = 90  # policy choice, change to match your policy


def load_users(path):
    """Read the login activity export and return a list of rows."""
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def days_since_login(user, as_of):
    """Return days since last login, or None if the user never logged in."""
    value = user["last_login"].strip()
    if value == "":
        return None
    return (as_of - date.fromisoformat(value)).days


def run_test(users, as_of):
    """Return active users who are stale or have never logged in."""
    failures = []
    for user in users:
        if user["status"] != "active":
            continue  # suspended accounts are skipped
        days = days_since_login(user, as_of)
        if days is None or days > MAX_INACTIVE_DAYS:
            failures.append((user, days))
    return failures


def main(path, as_of):
    users = load_users(path)
    active = [u for u in users if u["status"] == "active"]
    failures = run_test(users, as_of)

    print(f"Stale accounts test, as of {as_of}")
    print(f"Threshold: {MAX_INACTIVE_DAYS} days without login")
    print(f"Active users checked: {len(active)}")

    if not failures:
        print("RESULT: PASS. All active users logged in recently.")
        return 0

    print(f"RESULT: FAIL. {len(failures)} stale active user(s):")
    for user, days in failures:
        if days is None:
            detail = "never logged in"
        else:
            detail = f"{days} days since last login"
        note = "  <- HIGH RISK (admin)" if user["role"] == "admin" else ""
        print(f"  - {user['email']} ({user['role']}): {detail}{note}")
    return 1


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/sample_login_activity.csv"
    if len(sys.argv) > 2:
        as_of_date = date.fromisoformat(sys.argv[2])
    else:
        as_of_date = date.today()
    sys.exit(main(csv_path, as_of_date))

"""
CONTROL TEST: Access review evidence

Controls supported
  SOC 2 CC6.3 (modifying or removing access based on roles)
  ISO/IEC 27001:2022 Annex A 5.18 (access rights)

What the controls require
  Access rights are reviewed regularly, and access that is no longer
  appropriate is changed or removed.

Evidence checked
  A record of access reviews (CSV) with one row per in-scope system:
  the date of the last review, who reviewed it, who signed it off, and how
  many access removals were requested and completed. Sample data is used
  here. In practice, take this from the compliance platform or ticketing
  system where reviews are recorded.

Pass / fail
  Each system is checked for four things:
    1. It has a review date, and the review is within the allowed days.
    2. A reviewer is named.
    3. A sign-off (approved_by) is recorded.
    4. Every requested access removal has been completed.
  PASS: every system passes all four.
  FAIL: any system fails one or more. Each reason is listed.

Threshold
  90 days is set below as MAX_DAYS_SINCE_REVIEW (quarterly). This is a
  policy choice, not a number taken from SOC 2 or ISO 27001. Change it to
  match the company's access control policy.

Limitations
  This proves a review was recorded and signed off. It does not prove the
  review was careful. A reviewer who approves everything without reading it
  would still pass. A real audit would also sample the reviews and check
  that the lists reviewed were complete and accurate. The test also does not
  check that the reviewer is independent of the person who owns the system.

Built with AI assistance. Written by a GRC practitioner learning to code.
"""

import csv
import sys
from datetime import date

MAX_DAYS_SINCE_REVIEW = 90  # policy choice, change to match your policy


def load_reviews(path):
    """Read the access review records and return a list of rows."""
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def check_system(row, as_of):
    """Return a list of reasons this system fails. Empty list means pass."""
    reasons = []

    review_date = row["last_review_date"].strip()
    if review_date == "":
        reasons.append("no review recorded")
    else:
        days = (as_of - date.fromisoformat(review_date)).days
        if days > MAX_DAYS_SINCE_REVIEW:
            reasons.append(f"review is {days} days old")

    if row["reviewer"].strip() == "" and review_date != "":
        reasons.append("no reviewer named")

    if row["approved_by"].strip() == "" and review_date != "":
        reasons.append("no sign-off recorded")

    requested = row["removals_requested"].strip()
    completed = row["removals_completed"].strip()
    if requested != "":
        open_items = int(requested) - int(completed or 0)
        if open_items > 0:
            reasons.append(f"{open_items} requested removal(s) not completed")

    return reasons


def main(path, as_of):
    rows = load_reviews(path)

    print(f"Access review evidence test, as of {as_of}")
    print(f"Threshold: review within {MAX_DAYS_SINCE_REVIEW} days")
    print(f"Systems checked: {len(rows)}")

    failed = []
    for row in rows:
        reasons = check_system(row, as_of)
        if reasons:
            failed.append((row["system"], reasons))

    if not failed:
        print("RESULT: PASS. All systems have a current, signed-off review.")
        return 0

    print(f"RESULT: FAIL. {len(failed)} system(s) with gaps:")
    for system, reasons in failed:
        print(f"  - {system}: " + "; ".join(reasons))
    return 1


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/sample_access_reviews.csv"
    if len(sys.argv) > 2:
        as_of_date = date.fromisoformat(sys.argv[2])
    else:
        as_of_date = date.today()
    sys.exit(main(csv_path, as_of_date))

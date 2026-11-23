# grc-control-tests

Small, readable control tests for SOC 2 and ISO/IEC 27001:2022, written to show how a control can be checked with evidence from a system instead of a screenshot.

## About this project

I work in GRC and I am learning to code. I built these tests with AI assistance (Claude) and worked through each script until I could explain it myself. I care more about whether a test proves what a control requires than about how advanced the code is, so each test states its control, its evidence, and its limits.

All data in this repo is made-up sample data. No real company systems are used.

## Tests

| Test | Controls | Status |
|---|---|---|
| MFA enforcement | SOC 2 CC6.1, ISO 27001 Annex A 8.5 | Done |
| Stale user accounts | SOC 2 CC6.2, ISO 27001 Annex A 5.16 and 5.18 | Done |
| Access review evidence | SOC 2 CC6.3, ISO 27001 Annex A 5.18 | Done |

## How to run the tests

You need Python 3 installed.

```
python3 tests/test_mfa_enforcement.py
python3 tests/test_stale_accounts.py data/sample_login_activity.csv 2026-11-23
python3 tests/test_access_review_evidence.py data/sample_access_reviews.csv 2026-11-23
```

The MFA test reads `data/sample_users.csv`, skips suspended users, and lists any active user without MFA. Admin accounts are flagged as higher risk. It prints PASS or FAIL.

## What the MFA test does not prove

It checks that MFA is turned on for an account. It does not prove the person finished enrolling a device, or that MFA is enforced on every application. A real version would pull the user list from an identity provider such as Okta or Google Workspace and be paired with a check on enrollment.

## Why I built it

Continuous control testing means evidence comes from source systems and each test has to match what the control says. I wanted to practice writing tests that do that, starting small.
# grc-control-tests
Continuous control tests mapped to SOC 2 and ISO 27001, with sample data

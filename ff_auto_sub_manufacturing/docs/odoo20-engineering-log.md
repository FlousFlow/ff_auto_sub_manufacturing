# Odoo 20 Engineering Log

## 2026-11-22 — Single-purpose automatic child manufacturing

- Reduced the addon to one behavior: parent MO confirmation creates linked child
  MOs for raw components with normal manufacturing BoMs.
- Removed custom fields, setup warnings, refresh actions, scheduler UI and custom
  views. Odoo's native child-MO and traceability UI remains in place.
- Child creation uses Odoo's native manufacture rule and keeps the parent raw
  move, production group and duplicate prevention links.
- Tested on the disposable local Odoo 20 database with focused addon tests.

## 2026-11-22 — Verification

- Static Python compilation and manifest parsing passed.
- Focused addon suite passed: 3 tests, 0 failures, 0 errors.
- The selected native `mrp:TestProcurement` suite ran 28 tests; 4 assertions
  expect the pre-addon behavior (no extra child MO), so they fail by design under
  this requested automatic-child behavior. No Python exception or installation
  error occurred.

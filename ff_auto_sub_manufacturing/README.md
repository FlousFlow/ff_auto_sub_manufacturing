# Flous Flow Auto Sub-Manufacturing

## Purpose

This addon has one responsibility: when a manufacturing order is confirmed, it
automatically creates a child manufacturing order for every raw component that
has a normal manufacturing BoM.

The child order is created through Odoo's native manufacture rule and is linked
to the parent raw move and production group. Odoo therefore keeps responsibility
for BoM selection, quantities, reservations, traceability, cancellation and
valuation.

Components without a normal manufacturing BoM are ignored and continue through
Odoo's normal stock or purchase flow.

## Installation

Install `ff_auto_sub_manufacturing` from an Odoo addons path. The module adds no
menus, scheduled actions, custom buttons or configuration screens.

## Compatibility and permissions

- Odoo 20 Community; depends only on `mrp`.
- Uses the current user's normal Manufacturing permissions and does not add ACLs
  or record rules.
- No external services, credentials, cron jobs or database migrations are used.

## Business limits

The component must have a normal (manufacture) BoM. Existing stock is respected
through Odoo's native move quantities, and an existing active child order is not
duplicated. The package has been tested on a disposable local database; Apps
review, production load, multi-company, serial/lot valuation and backorders are
not claimed as certified here.

## Testing boundary

The tests cover automatic creation, parent/child linkage, idempotency and
ignoring components without a manufacturing BoM. Full valuation, lot/serial,
backorder and multi-company scenarios should still be tested in a disposable
database before production deployment.

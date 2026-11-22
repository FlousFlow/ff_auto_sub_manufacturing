# Flous Flow Auto Sub-Manufacturing

## What problem does it solve?

In standard manufacturing, a finished-product BoM can contain a component that
is also manufactured. Users may then have to create the component's manufacturing
order manually before they can complete the parent order.

This addon automates exactly that missing step.

## How it works

1. A user creates or opens a normal Odoo Manufacturing Order (MO) for the final
   product.
2. The final product BoM contains one or more raw components.
3. The user confirms the parent MO.
4. The addon checks each raw component. If that component has a normal
   manufacturing BoM, Odoo creates a child MO for the required quantity.
5. Odoo links the child finished move to the parent raw move and keeps the
   production-group relationship. The child order is therefore visible through
   Odoo's native traceability and manufacturing links.

### Practical example

For a **Chair** MO:

- Chair BoM: 1 Seat + 4 Legs + 8 Screws.
- Seat has its own normal BoM: fabric + foam + board.
- Legs have no manufacturing BoM and are purchased/stocked.

When the Chair MO is confirmed, the addon automatically creates a child MO for
the Seat. It does not create a manufacturing order for Legs or Screws because
they have no manufacturing BoM.

## What the addon does

- Creates child MOs automatically at parent-MO confirmation.
- Supports multiple manufactured components in the same parent BoM.
- Uses the component's normal BoM and the warehouse's native Manufacture rule.
- Links the child finished move to the exact parent raw move.
- Preserves Odoo production groups, quantities, UoM conversion and traceability.
- Prevents an active child MO from being duplicated when the confirmation flow
  is retried.

## What it deliberately does not do

- It does not add a new menu, dashboard, wizard, button or settings screen.
- It does not add a cron job or require a user to run a scheduler.
- It does not manufacture components that have no normal manufacturing BoM.
- It does not silently change routes, orderpoints, warehouses or stock levels.
- It does not replace Odoo's reservation, valuation, accounting or cancellation
  logic.

## Configuration

Only standard Odoo MRP configuration is required:

1. Install the **Manufacturing (MRP)** application.
2. Create a normal manufacturing BoM for every component that should be made
   internally.
3. Make sure the warehouse has its standard Manufacture rule (created by Odoo
   with the warehouse configuration).
4. Add the manufactured component to the parent product's normal BoM.

No addon-specific configuration is required.

## Installation

Copy the `ff_auto_sub_manufacturing` folder into an Odoo addons path, update the
Apps list, and install the module. It depends only on `mrp` and adds no access
rights or record rules; normal Odoo Manufacturing permissions apply.

## Compatibility

- Odoo 20 Community.
- Dependency: `mrp` only.
- Multi-company behavior follows the company and warehouse selected on the
  parent MO.
- No external service, credential, API key or scheduled job is used.

## Technical design

The addon inherits `mrp.production.action_confirm()`. After Odoo confirms the
parent's native stock moves, the addon builds native procurements for qualifying
manufactured components and calls Odoo's native Manufacture stock rule. It does
not call `mrp.production.create()` or `stock.move.create()` directly. This keeps
standard Odoo links and business rules as the source of truth.

## Testing and known boundaries

The included tests cover automatic child creation, parent/child move linkage,
production-group linkage, idempotency and ignoring components without a BoM.
Focused local tests pass. Production-load testing, Apps review, serial/lot
valuation, backorders and complex multi-company scenarios still require
validation in the target environment.

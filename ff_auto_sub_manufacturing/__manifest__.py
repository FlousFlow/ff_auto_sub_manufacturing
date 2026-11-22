{
    'name': 'Flous Flow - Auto Sub-Manufacturing',
    'summary': 'Automatically create linked child manufacturing orders',
    'description': """
Flous Flow Auto Sub-Manufacturing
================================

Automatically creates linked child manufacturing orders when a parent
manufacturing order is confirmed and one or more raw components are themselves
manufactured products with normal BoMs. This removes the manual step of creating
the component MOs before producing the final product.

Example: a Chair MO contains a Seat and Legs. If Seat has its own manufacturing
BoM, confirming the Chair MO creates a child MO for Seat, links the child's
finished move to the Chair raw move, and preserves Odoo's native production
group and traceability. Components without a manufacturing BoM are left to the
normal stock or purchase flow.

The addon has no custom menus, scheduled actions, configuration screens or
external services. It extends Odoo's native MRP confirmation flow and delegates
BoM selection, UoM conversion, reservations, procurement, cancellation,
valuation and accounting to Odoo.
    """,
    'version': '20.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',
    'author': 'Flous Flow',
    'website': 'https://flousflow.com',
    'license': 'LGPL-3',
    'depends': ['mrp'],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}

{
    'name': 'Flous Flow - Auto Sub-Manufacturing',
    'summary': 'Automatically create linked child manufacturing orders',
    'description': """
Flous Flow Auto Sub-Manufacturing
================================

When a manufacturing order is confirmed, automatically creates a linked child
manufacturing order for each raw component that has a normal manufacturing BoM.
Odoo's native MRP procurement remains responsible for the child order and stock
move links.
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

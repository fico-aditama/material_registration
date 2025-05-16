{
    'name': 'Material Registration',
    'version': '14.0.1.0.0',
    'summary': 'Module for registering materials for sale',
    'description': """
        This module allows for the registration of materials with the following details:
        - Material Code
        - Material Name
        - Material Type (Fabric, Jeans, Cotton)
        - Material Buy Price
        - Related Supplier
    """,
    'category': 'Inventory',
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'depends': ['base', 'stock','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/material_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
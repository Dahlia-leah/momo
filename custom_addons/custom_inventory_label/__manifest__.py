{
    'name': 'Custom Inventory Label',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Custom labels for inventory management',
    'description': """
        This module provides custom labels for stock picking operations, 
        including product and material details.
    """,

    'depends': [
        'stock',  # Keep stock as a dependency
        # Remove 'report' temporarily if not required
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

# -*- coding: utf-8 -*-
{
    'name': "test_modulo_1",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
aplica un descuento del 10% por cada 1000$ en el total
    """,

    'author': "Binhex",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale'],

    # always loaded
    'data': [
    
        'views/sale_order_view.xml',
        
    ],

   
}


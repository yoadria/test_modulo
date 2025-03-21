# -*- coding: utf-8 -*-
{
    'name': "Magento prueba",

    'summary': "extraer datos de una bbdd externa e introducir los datos en odoo",

    'description': """
Se requiere la generación de productos desde bbdd externa.
Se tienen que generar los productos por duplicado, el primero es el nuevo y adicionalmente se
debe generar una copia que es el de segunda mano.
El original tiene el código de barras proporcionado en la bbdd en la columna EAN13 y
la copia el mismo pero con el sufijo "OKA", el de segunda mano se debe generar con una etiqueta "Segunda Mano"
y exento de impuestos.
    """,

    'author': "Binhex",
    

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Connector',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['connector','base', 'product'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/ir_model_access.xml',
        'views/views.xml',
        #'data/update_products.xml',
    ],

}


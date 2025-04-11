{
    "name": "Magento prueba",
    "summary": "extraer datos de una bbdd externa e introducir los datos en odoo",
    "author": "Binhex",
    "license": "AGPL-3",
    "website": "https://github.com/yoadria/test_modulo",
    "category": "Connector",
    "version": "17.0.1.0.0",
    # any module necessary for this one to work correctly
    "depends": ["connector", "base", "product"],
    "data": [
        # 'security/ir.model.access.csv',
        # 'security/ir_model_access.xml',
        "views/views.xml",
        #'data/update_products.xml',
    ],
}

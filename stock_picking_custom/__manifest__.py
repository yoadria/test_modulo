{
    'name': 'Stock Picking Custom',
    'version': '0.1',
    'category': 'Inventory',
    'depends': ['stock'],
    'athor': 'Binhex',
    'description': """
    Crear un módulo desde cero que amplíe stock.picking,
    añadiendo mejoras en la gestión de transferencias de inventario.""",
    'data': [
        'views/stock_picking_custom_views.xml',
        'views/stock_move_line_custom_views.xml',
    ],
}

{
    'name': "Connector Canalocio - Product Sync",

    'summary': """
    Sincronizar y duplicar productos de una base de datos externa (Canalocio)""",

    'description': """
    Características principales:
    - Creación/actualización automática de productos desde una fuente externa
    - Generación dual de productos (variantes nuevas + de segunda mano)
    - Gestión de códigos de barras:
      * Producto original: EAN13 desde la fuente
      * Variante de segunda mano: Código de barras original + sufijo "OKA"

    Aspectos técnicos:
    - Soporta actualizaciones incrementales mediante el parámetro datefrom
    - Restricción única en códigos de barras para evitar duplicados
    """,

    'author': "Binhex",
    'category': 'Connector',
    'version': '17.0.1.0.0',

    'depends': ['connector', 'product'],

    'data': [
        'views/canalocio_view.xml',
        'data/sync_DB.xml',
    ],



}


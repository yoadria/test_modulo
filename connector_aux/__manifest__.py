{
    "name": "Import Products from Canalocio",
    "summary": """
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
    "author": "Binhex",
    "category": "Connector",
    "version": "17.0.1.0.0",
    "website": "https://github.com/yoadria/test_modulo",
    "license": "LGPL-3",
    "depends": ["stock", "sale", "connector_importer", "account"],
    "external_dependencies": {"python": ["requests"]},
    "data": [
        "data/import_url.xml",
        "data/import_type.xml",
        "data/import_backend_data.xml",
        "data/tag_second_hand.xml",
        "data/recordset_data.xml",
    ],
}

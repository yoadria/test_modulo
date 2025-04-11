# Copyright 2025 r.perez@binhex.cloud
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Connector Importer Canal",
    "summary": """Connector Importer for Canal Ocio Store""",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "author": "Binhex",
    "website": "https://github.com/yoadria/test_modulo",
    "depends": [
        "product",
        "account",
        "connector_importer",
    ],
    "category": "Connector",
    "external_dependencies": {"python": ["requests"]},
    "data": [
        "data/product_tag_data.xml",
        "data/import_type_data.xml",
        "data/import_backend_data.xml",
        "data/import_source_data.xml",
        "data/import_recordset_data.xml",
    ],
}

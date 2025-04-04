from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class CanalocioMapper(Component):
    _name = "canalocio.mapper"
    _inherit = "importer.mapper.dynamic"
    _apply_on = "product.product"
    _mapper_usage = "importer.mapper"
    direct = [
        ("titulo", "name"),
        ("ean13", "barcode"),
        ("id", "default_code"),
    ]

    required = {
        "titulo": "name",
        "ean13": "barcode",
        "tipo": "categ_id",
    }

    @mapping
    def tipo(self, record):
        ProductCategory = self.env["product.category"]
        tipo = record.get("tipo")
        category = ProductCategory.search(
            [("name", "=", tipo)]
        ) or ProductCategory.create({"name": tipo})
        return {"categ_id": category.id}

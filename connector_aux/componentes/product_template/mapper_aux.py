from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping


class ProductTemplateMapper(Component):
    _name = "product.template.mapper"
    _inherit = "importer.mapper.dynamic"
    _apply_on = "product.template"
    _mapper_usage = "importer.mapper"

    direct = [
        ("titulo", "name"),
        ("ean13", "barcode"),
        ("id", "default_code"),
        ("sinopsis", "description_sale"),
        ("pvp", "list_price"),
        ("pvd", "standard_price"),
        ("peso", "weight"),
        ("caratula", "image_1920"),
        # ("tipo", "categ_id"),
    ]
    required = {
        "titulo": "name",
        "ean13": "barcode",
        "tipo": "categ_id",
    }

    defaults = [("sale_ok", True)]

    @mapping
    def tipo(self, record):
        ProductCategory = self.env["product.category"]
        tipo = record.get("tipo")
        category = ProductCategory.search(
            [("name", "=", tipo)]
        ) or ProductCategory.create({"name": tipo})
        return {"categ_id": category.id}

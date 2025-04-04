from odoo.fields import Command

from odoo.addons.component.core import Component


class CanalocioRecordHandler(Component):
    """Interact w/ odoo canal ocio importable product records."""

    _name = "canalocio.handler"
    _inherit = "importer.odoorecord.handler"
    _apply_on = "product.product"

    def odoo_post_create(self, odoo_record, values, orig_values):
        """Post-create hook for odoo product.product records."""

        product_template = odoo_record.product_tmpl_id
        record_copy = product_template.with_context(create_product_product=True).copy(
            default={
                "name": product_template.name,
                "default_code": f"OKA{product_template.default_code}",
                "barcode": f"OKA{product_template.barcode}",
            }
        )
        snd_hand_tag = self.env.ref("connector_importer_canal.product_tag_second_hand")
        record_copy.write(
            {
                "product_tag_ids": [Command.set(snd_hand_tag.ids)],
                "taxes_id": [Command.clear()],
            }
        )

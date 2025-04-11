from odoo.fields import Command

from odoo.addons.component.core import Component


class ProducTemplateHandler(Component):
    """Interact w/ odoo product.template records."""

    _name = "product.template.handler"
    _inherit = "importer.odoorecord.handler"
    _apply_on = "product.template"

    def _prepare_second_hand_product(self, odoo_record):
        product_template = odoo_record
        default = {
            "name": product_template.name,
            "default_code": f"{product_template.default_code}OKA",
            "barcode": f"{product_template.barcode}OKA",
        }
        return product_template, default

    def odoo_pre_create(self, values, origin_values):
        """intervenimos para convertir la imagen en base64
        y controlar los numero decimales"""
        from ...utils.utils_tools import (
            decimal_control,
            parse_imgbase64,
        )

        # import wdb; wdb.set_trace()
        # se convierte url en imagen si se puede
        img = values.get("image_1920")
        img_base64 = parse_imgbase64(img)
        values["image_1920"] = img_base64 or False

        for num in ["list_price", "standard_price", "weight"]:
            if num in values:
                values[num] = decimal_control(values[num])

    def odoo_post_create(self, odoo_record, values, orig_values):
        """Post-create hook for odoo product.template records."""

        # Create a new second-hand product template
        product_template, default_values = self._prepare_second_hand_product(
            odoo_record
        )
        record_copy = product_template.with_context(create_product_product=True).copy(
            default=default_values
        )
        snd_hand_tag = self.env.ref("connector_aux.tag_segunda_mano")
        record_copy.write(
            {
                "product_tag_ids": [Command.set(snd_hand_tag.ids)],
                "taxes_id": [Command.clear()],
            }
        )

    def odoo_pre_write(self, odoo_record, values, orig_values):
        from ...utils.utils_tools import (
            decimal_control,
            parse_imgbase64,
        )

        # import wdb; wdb.set_trace()
        # se convierte url en imagen si se puede
        img = values.get("image_1920")
        img_base64 = parse_imgbase64(img)
        values["image_1920"] = img_base64 or False

        for num in ["list_price", "standard_price", "weight"]:
            if num in values:
                values[num] = decimal_control(values[num])

    def odoo_post_write(self, odoo_record, values, orig_values):
        """Post-write hook for odoo product.product records."""

        product_template, default_values = self._prepare_second_hand_product(
            odoo_record
        )
        product_template = odoo_record
        second_hand_product_template = self.env["product.template"].search(
            [("default_code", "=", default_values.get("default_code"))], limit=1
        )
        updated_values = product_template.copy_data(default=default_values)[0]
        second_hand_product_template.write(updated_values)

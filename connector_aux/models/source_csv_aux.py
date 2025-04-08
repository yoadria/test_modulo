import copy
import logging

from odoo import models
from odoo.fields import Command

from ..utils.import_utils import HTTPCSVReader

_logger = logging.getLogger(__name__)


class CSVAuxSource(models.Model):
    _inherit = "import.source.csv"

    _csv_reader_klass = HTTPCSVReader

    # @property
    # def _config_summary_fields(self):
    #     _fields = super()._config_summary_fields
    #     return _fields + [
    #         "csv_path",
    #     ]

    def prueba(self):
        _logger.info(">>>>>>>>>>>> Prueba <<<<<<<<<<<<<<<<")

        lines = list(self._get_lines())  # Read all lines into a list
        if lines:
            _logger.info(">>>>>>>> Prueba contenido completo <<<<<<<<<<<<<")
            for line in lines:
                self.with_delay().procces_product(line)

        else:
            _logger.info(">>>>>>>>>> Prueba no hay líneas <<<<<<<<<<")

        _logger.info(">>>>>> Prueba fin <<<<<<<<<<<<<")

    def _generate_csv_reader(self, reader_args):
        res = super()._generate_csv_reader(reader_args)
        if self.csv_path:
            self.csv_delimiter = res.delimiter
            self.csv_quotechar = res.quotechar
        return res

    def procces_product(self, row):
        """crear o actualizar producto."""
        _logger.info(f"Iniciando creacion del producto >>>>> {row}")

        barcode = row.get("ean13", "")

        if not barcode or not barcode.isdigit():
            return

        # Mapeo de productos
        main_product = {
            "name": row.get("titulo", "Sin nombre"),
            "barcode": barcode,
            "default_code": row.get("id", ""),
            "list_price": row.get("pvp", "0.0"),
            "standard_price": row.get("pvd", "0.0"),
            "weight": row.get("peso", "0.0"),
            "sale_ok": True,
            "detailed_type": "product",
        }

        tag_segunda_mano = self.env.ref("connector_aux.tag_segunda_mano")
        second_hand = copy.deepcopy(main_product)
        second_hand["barcode"] += "OKA"
        second_hand["default_code"] += "OKA"
        second_hand["taxes_id"] = [Command.clear()]
        second_hand["product_tag_ids"] = [Command.set(tag_segunda_mano.ids)]

        existing_prodcut = self.env["product.template"].search(
            [("barcode", "=", barcode)], limit=1
        )
        existing_prodcut_second_hand = self.env["product.template"].search(
            [("barcode", "=", second_hand["barcode"])], limit=1
        )
        if existing_prodcut:
            existing_prodcut.write(main_product)
        else:
            self.env["product.template"].create(main_product)

        if existing_prodcut_second_hand:
            existing_prodcut_second_hand.write(second_hand)
        else:
            self.env["product.template"].create(second_hand)

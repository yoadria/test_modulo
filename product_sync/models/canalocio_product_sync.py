import copy
import csv
import io
import logging

import requests

from odoo import fields, models

_logger = logging.getLogger(__name__)


class CanalocioSync(models.Model):
    _name = "canalocio.sync"
    _description = ""

    location = fields.Char(string="URL de Conexion", required=True)
    # data = fields.Text(string="CSV Data")

    def action_fetch_data(self):
        """Conectarse a la URL y obtener los datos CSV a patir de su descarga."""
        timeout = 10

        response = requests.get(
            self.location, stream=True, timeout=timeout
        )  # Usamos la URL almacenada en el modelo
        response.raise_for_status()
        csv_data = io.StringIO(response.text)

        csv_reader = csv.DictReader(csv_data, delimiter=";")
        data = [dict(row) for row in csv_reader]

        list_create = []

        # BATCH_SIZE = 2000

        counter = 0
        # Ahora guardamos los productos
        for row in data:
            if counter >= 20:
                break
            # Aquí puedes procesar cada fila
            counter += 1

            barcode = row.get("ean13", "")

            if not barcode or not barcode.isdigit():
                continue

            try:
                price = row.get("pvp", "").replace(",", "")
            except Exception:
                price = 0.0

            url_imagen = row.get("caratula")
            imagen_base64 = self.imagen_a_base64(url_imagen)

            # Crear productos
            main_product = {
                "name": row.get("titulo", "Sin nombre"),
                "barcode": barcode,
                "list_price": price,
                "image_1920": imagen_base64,
            }

            second_hand = copy.deepcopy(main_product)
            second_hand["barcode"] += "OKA"
            second_hand["taxes_id"] = [(6, 0, [])]
            second_hand["default_code"] = "Segunda Mano"

            existing_prodcut = self.env["product.template"].search(
                [("barcode", "=", barcode)], limit=1
            )
            existing_prodcut_second_hand = self.env["product.template"].search(
                [("barcode", "=", second_hand["barcode"])], limit=1
            )
            if existing_prodcut:
                existing_prodcut.write(main_product)
            else:
                list_create.append(main_product)

            if existing_prodcut_second_hand:
                existing_prodcut_second_hand.write(second_hand)
            else:
                list_create.append(second_hand)

        # Insertar restantes
        if list_create:
            self.env["product.template"].create(list_create)

    def sync_db(self):
        """Actualizar los productos desde la fuente Canalocio."""
        # falta manejar exepciones de backend por si da mas de una URL
        try:
            backend = self.env["canalocio.sync"].search([])
            _logger.info(backend.location)

        except Exception:
            _logger.info("error al actualizar automaticamente")

    def imagen_a_base64(self, url):
        import base64

        timeout = 10
        try:
            response = requests.get(url, stream=True, timeout=timeout)
            response.raise_for_status()
            img_base64 = base64.b64encode(response.content).decode()
            return img_base64
        except requests.exceptions.RequestException as e:
            _logger.info(f"Error al obtener imagen: {e}")
            return None
        except Exception as e:
            _logger.info(f"Error desconocido: {e}")
            return None

    def prueba(self):
        """funcion conectada al boton prueba"""
        # try:

        #     # default_lang =  self.env['res.lang'].\
        # _lang_get(self.env.company.partner_id.lang)
        #     lang_code = self.env.company.partner_id.lang or 'en_US'
        #     lang = self.env['res.lang']._lang_get(lang_code)
        #     precio = '1,222.99'
        #     precio_final = lang._parse_float(precio)

        #     product = {
        #         "name": 'producto prueba',
        #         "list_price": precio_final
        #     }
        #     self.env["product.template"].create(product)
        #     _logger.info(lang)
        # except Exception as e:
        #     _logger.info(f"Error desconocido: {e}")

        # default_lang =  self.env['res.lang'].\
        # _lang_get(self.env.company.partner_id.lang)
        import locale

        # import wdb; wdb.set_trace()

        usage_lang = self.env.user.lang
        locale.setlocale(locale.LC_ALL, f"{usage_lang}.UTF-8")
        precio = "1.222,99"
        try:
            precio_final = locale.atof(precio)
        except ValueError:
            precio_final = float(precio.replace(".", "").replace(",", "."))

        product = {"name": "producto prueba", "list_price": precio_final}
        self.env["product.template"].create(product)

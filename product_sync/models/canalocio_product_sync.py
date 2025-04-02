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
    lang_id = fields.Many2one(
        "res.lang",  # Relación con el modelo res.lang
        string="Idioma",
        default=lambda self: self.env["res.lang"].search(
            [("code", "=", self.env.user.lang)], limit=1
        ),
    )

    def action_fetch_data(self):
        """Conectarse a la URL y obtener los datos CSV a patir de su descarga."""
        try:
            _logger.info("Iniciando descarga de datos")

            timeout = 30
            BATCH_SIZE = 5

            response = requests.get(
                self.location, stream=True, timeout=timeout
            )  # Usamos la URL almacenada en el modelo
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            _logger.info(f"Error al conectar con la URL: {e}")
            raise e
        except Exception as e:
            _logger.info(f"Error desconocido: {e}")
            raise e

        csv_data = io.StringIO(response.text)
        csv_reader = csv.DictReader(csv_data, delimiter=";")

        data = list(csv_reader)
        for i in range(0, len(data), BATCH_SIZE):
            batch = data[i : i + BATCH_SIZE]
            self.with_delay().process_batch(batch)
            # Aquí puedes procesar cada lote de 300 filas
            break

    def process_batch(self, batch):
        """Procesar un lote de productos."""
        _logger.info("Iniciando procesamiento de lote")

        # Ahora guardamos los productos
        for row in batch:
            # row = dict(row)

            barcode = row.get("ean13", "")

            if not barcode or not barcode.isdigit():
                continue

            try:
                pvp = row.get("pvp", "").replace(",", "")
            except Exception:
                pvp = 0.0
            try:
                pvd = row.get("pvd", "").replace(",", "")
            except Exception:
                pvd = 0.0

            try:
                peso = row.get("peso", "").replace(",", "")
            except Exception:
                peso = 0.0

            if row.get("estado") == "disponible":
                sale_ok = True
            else:
                sale_ok = False

            # url_imagen = row.get("caratula")
            # imagen_base64 = self.imagen_a_base64(url_imagen)
            # imagen_base64 = self.with_delay().imagen_a_base64(url_imagen)

            # Crear productos
            main_product = {
                "name": row.get("titulo", "Sin nombre"),
                "barcode": barcode,
                "list_price": pvp,
                "standard_price": pvd,
                "weight": peso,
                "sale_ok": sale_ok,
                "detailed_type": "product",
                # "image_1920": imagen_base64,
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
                self.env["product.template"].create(main_product)

            if existing_prodcut_second_hand:
                existing_prodcut_second_hand.write(second_hand)
            else:
                self.env["product.template"].create(second_hand)

        _logger.info(f"Lote procesado correctamente, {len(batch)} filas procesadas")

    def sync_db(self):
        """Actualizar los productos desde la fuente Canalocio."""
        try:
            _logger.info("Empieza sincronisacion de productos")
            backend = self.env["canalocio.sync"].search([])
            for ref in backend:
                if "www.canalocio.es" in ref.location:
                    # ref.action_fetch_data()
                    ref.with_delay(channel="root.canalocio_sync").action_fetch_data()
        except Exception as e:
            _logger.info("Error al sincronizar productos")
            _logger.info(f"Error: {e}")

    def imagen_a_base64(self, url):
        import base64

        timeout = 30
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

    def queue_job_demo(self):
        # self.process_1()
        # self.process_2()
        # self.process_3()
        _logger.info("Iniciando cola de trabajos")
        self.with_delay().process_1()

        self.with_delay().process_2()

        self.with_delay().process_3()

        _logger.info("Cola de trabajos finalizada")

    def process_1(self):
        product = {"name": "Producto de prueba 1"}
        self.env["product.template"].create(product)
        _logger.info("Proceso 1 completado")

    def process_2(self):
        product = {"name": "Producto de prueba 2"}
        self.env["product.template"].create(product)
        _logger.info("Proceso 2 completado")

    def process_3(self):
        product = {"name": "Producto de prueba 3"}
        self.env["product.template"].create(product)
        _logger.info("Proceso 3 completado")

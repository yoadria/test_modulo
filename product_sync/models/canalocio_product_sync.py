from odoo import fields, models, api
from odoo.exceptions import UserError
import requests
import csv
import logging
import copy
import io

_logger = logging.getLogger(__name__)


class CanalocioSync(models.Model):
    _name = "canalocio.sync"
    _description = ""

    location = fields.Char(string="URL de Conexion", required=True)
    # data = fields.Text(string="CSV Data")




    # def action_fetch_data(self):
    #     """Conectarse a la URL y obtener los datos CSV."""
    #     try:
    #         response = requests.get(
    #             self.location, stream=True
    #         )  # Usamos la URL almacenada en el modelo
    #         response.raise_for_status()

    #         csv_reader = csv.DictReader(
    #             response.iter_lines(decode_unicode=True), delimiter=";"
    #         )
    #         list_create = []
    #         products_update = {}

    #         BATCH_SIZE = 2000

    #         # Cargar TODOS los códigos de barras existentes en una sola consulta
    #         existing_barcodes = set(
    #             self.env["product.template"].search_read(
    #                 [("barcode", "!=", False)], ["barcode"]
    #             )
    #         )
    #         existing_barcodes = {prod["barcode"] for prod in existing_barcodes}
    #         counter = 0
    #         # Ahora guardamos los productos
    #         for row in csv_reader:
    #             if counter >= 1:
    #                 break
    #             # Aquí puedes procesar cada fila
    #             counter += 1
    #             barcode = row.get("ean13", "")
    #             if not barcode or not barcode.isdigit():
    #                 continue

    #             try:
    #                 price = row.get("pvp", "").replace(",", "")
    #             except:
    #                 price = 0.0

    #             # Crear productos
    #             main_product = {
    #                 "name": row.get("titulo", "Sin nombre"),
    #                 "barcode": barcode,
    #                 "list_price": price,
    #             }

    #             second_hand = copy.deepcopy(main_product)
    #             second_hand["barcode"] += "OKA"
    #             second_hand["taxes_id"] = [(6, 0, [])]
    #             second_hand["default_code"] = "Segunda Mano"

    #             #  Verificar existencia en `existing_barcodes`
    #             if barcode not in existing_barcodes:
    #                 list_create.append(main_product)
    #                 existing_barcodes.add(
    #                     barcode
    #                 )  # Lo agregamos al set para evitar duplicados en esta ejecución
    #             else:
    #                 # se añade el producto existente al diccionario de actualisacion

    #                 products_update[main_product["barcode"]] = {
    #                     "name": main_product["name"],
    #                     "barcode": main_product["barcode"],
    #                     "list_price": main_product["list_price"],
    #                 }

    #             if second_hand["barcode"] not in existing_barcodes:
    #                 list_create.append(second_hand)
    #                 existing_barcodes.add(second_hand["barcode"])

    #             #  Insertar en lotes grandes para mejorar rendimiento
    #             if len(list_create) >= BATCH_SIZE:
    #                 self.env["product.template"].create(list_create)
    #                 list_create = []

    #             print(f"dentro del bucle crear >> {list_create}\nactualizar >> {products_update}")

    #         # Insertar restantes
    #         if list_create:
    #             self.env["product.template"].create(list_create)

    #         # if products_update:
    #         #     self.update_product(products_update)

    #     except Exception as e:
    #         _logger.error("Error crítico: %s", str(e))
    #         raise UserError(f"Falló la sincronización: {str(e)}")

    def update(self):
        try:
            import wdb; wdb.set_trace()
            # Buscar el registro por el campo 'location'
            url = "http://www.canalocio.es/export_info.php?key=onan&val=834jds2k,23WZjd92Pas2S$2&datefrom=2024-08-01&outfile=1"
            backend = self.env["canalocio.sync"].search(
                [("location", "=", url)], limit=1
            )

            if not backend:

                raise UserError(
                    "No se encontró el registro de Magento Backend con la URL proporcionada."
                )
            # Llamar al método 'action_fetch_data' de ese registro
            #backend.action_fetch_data()

            backend_aux = self.env["canalocio.sync"].search([])
            print(backend_aux)

        except Exception:
            print("error al actualizar automaticamente")

    def update_product(self, new_products):
        # old_products = {
        # prod["id"]: {"name": prod["name"], "barcode": prod["barcode"], "list_price": prod["list_price"]}
        # for prod in self.env["product.template"].search_read(
        #     [("barcode", "!=", False)], ["id", "name", "barcode", "list_price"]
        # )
        # }
        print (">>>>>>>>>>>> Dentro de actualizar <<<<<<<<<<<<<<<")
        old_products = {
            prod["barcode"]: {
                "id": prod["id"],
                "name": prod["name"],
                "barcode": prod["barcode"],
                "list_price": prod["list_price"]
            }
            for prod in self.env["product.template"].search_read(
                [("barcode", "!=", False)], [ "name", "barcode", "list_price"]
            )
        }

        # for v in list(old_products.items())[:5]:
        #     print (v)
        #     print()

        counter = 0

        for barcode, new_data in new_products.items():
            # if counter >= 1:
            #     break
            # # Aquí puedes procesar cada fila
            # counter += 1
            # Verificar si el producto principal existe en old_products
            if barcode in old_products:
                old_product = old_products[barcode]
                product = self.env["product.template"].browse(old_product["id"])

                # Verificar si también existe el producto de segunda mano (con OKA)
                barcode_ok = barcode + 'OKA'
                if barcode_ok in old_products:
                    old_product_ok = old_products[barcode_ok]
                    product_ok = self.env["product.template"].browse(old_product_ok["id"])

                    # Actualizar ambos productos si los valores han cambiado
                    updates = {}
                    if old_product["name"] != new_data["name"]:
                        updates["name"] = new_data["name"]
                    if old_product["list_price"] != new_data["list_price"]:
                        updates["list_price"] = new_data["list_price"]

                    # Si se encontraron cambios, actualizar el producto principal
                    if updates:
                        product.write(updates)

                    # Actualizar el producto de segunda mano (OKA) si es necesario
                    updates_ok = {}
                    if old_product_ok["name"] != new_data["name"]:
                        updates_ok["name"] = new_data["name"]
                    if old_product_ok["list_price"] != new_data["list_price"]:
                        updates_ok["list_price"] = new_data["list_price"]

                    # Si se encontraron cambios, actualizar el producto de segunda mano
                    if updates_ok:
                        product_ok.write(updates_ok)


    # def _create_product(self, product_data):
    #     """
    #     Crea un producto en product.template usando los datos proporcionados.

    #     :param product_data: Diccionario con los valores del producto, ejemplo:
    #                         {'name': 'Matrix Revolutions', 'barcode': '7321930178229'}
    #     """
    #     try:
    #         # Verificar que los campos esenciales están presentes
    #         name = product_data.get("name", "Producto sin nombre")  # Valor por defecto si no hay 'name'
    #         barcode = product_data.get("barcode", None)  # Puede ser None si no tiene código de barras
    #         if not barcode or barcode == 'OKA':
    #             return False

    #         # Crear el producto
    #         product_vals = {
    #             "name": name,
    #             "barcode": barcode,
    #             'list_price': product_data.get('list_price', 0.0),
    #         }

    #         if 'OKA' in barcode: # no añadirle los impuestos si es de segunda mano
    #             product_vals['taxes_id'] = [(6, 0, [])]  # Lista vacía de impuestos
    #             product_vals['default_code'] = 'Segunda Mano'

    #         self.env["product.template"].create(product_vals)
    #         return True

    #     except Exception:
    #         return False

    # def get_producto(self, data):
    #     """
    #     Busca un producto en 'product.template' por su código de barras.

    #     :param data: String con el código de barras del producto.
    #     :return: Registro de 'product.template' si se encuentra, o false si no existe.
    #     """
    #     try:
    #         producto = self.env['product.template'].search([
    #             ('barcode', '=', data)  # Busca solo por código de barras exacto
    #         ], limit=1)

    #         if producto:
    #             return producto
    #         else:
    #             return False

    #     except Exception:
    #         return False


    def action_fetch_data(self):
        """Conectarse a la URL y obtener los datos CSV."""

        response = requests.get(
            self.location, stream=True
        )  # Usamos la URL almacenada en el modelo
        response.raise_for_status()
        csv_data = io.StringIO(response.text)

        csv_reader = csv.DictReader(
            csv_data, delimiter=";"
        )
        data = [dict(row) for row in csv_reader]

        list_create = []
        products_update = {}

        BATCH_SIZE = 2000

        # Cargar TODOS los códigos de barras existentes en una sola consulta
        existing_barcodes_raw = self.env["product.template"].search_read(
            [("barcode", "!=", False)], ["barcode"]
        )

        # Verificar el contenido de existing_barcodes_raw
        # _logger.info(f"existing_barcodes_raw: {existing_barcodes_raw}")

        # Asegúrate de que es una lista de diccionarios y que contienen la clave 'barcode'
        existing_barcodes = {prod["barcode"] for prod in existing_barcodes_raw if isinstance(prod, dict) and "barcode" in prod}

        counter = 0
        # Ahora guardamos los productos
        for row in data:
            # if counter >= 1:
            #     break
            # # Aquí puedes procesar cada fila
            # counter += 1

            barcode = row.get("ean13", "")

            if not barcode or not barcode.isdigit():
                continue

            try:
                price = row.get("pvp", "").replace(",", "")
            except:
                price = 0.0

            url_imagen = row.get("bigcaratula")
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

            #  Verificar existencia en `existing_barcodes`
            if barcode not in existing_barcodes:
                list_create.append(main_product)
                existing_barcodes.add(
                    barcode
                )  # Lo agregamos al set para evitar duplicados en esta ejecución
            else:
                # se añade el producto existente al diccionario de actualisacion

                products_update[main_product["barcode"]] = {
                    "name": main_product["name"],
                    "barcode": main_product["barcode"],
                    "list_price": main_product["list_price"],
                }

            if second_hand["barcode"] not in existing_barcodes:
                list_create.append(second_hand)
                existing_barcodes.add(second_hand["barcode"])

            #  Insertar en lotes grandes para mejorar rendimiento
            if len(list_create) >= BATCH_SIZE:
                self.env["product.template"].create(list_create)
                list_create = []

            #print(f"dentro del bucle crear >> {list_create}\nactualizar >> {products_update}")

        # Insertar restantes
        if list_create:
            self.env["product.template"].create(list_create)

        if products_update:
            self.update_product(products_update)


    def prueba_imagen(self):
        import base64
        import wdb; wdb.set_trace()
        url = 'http://www.canalocio.es/getimage.php?pass=expzln3569&img=/images/269404.jpg'
        url2 = 'http://www.canalocio.es/getimage.php?pass=expzln3569&img=/caratulas/269404.jpg'
        response = requests.get(url2)
        response.raise_for_status()
        img_base64 = base64.b64encode(response.content).decode()

        producto = self.env['product.template'].search([('barcode', '=', '12345678')], limit=1)
        print(producto.name)
        producto.write({'image_1920': img_base64})

    def imagen_a_base64(self, url):
        import base64
        try:
            response = requests.get(url)
            response.raise_for_status()
            img_base64 = base64.b64encode(response.content).decode()
            return img_base64
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener imagen: {e}")
            return None
        except Exception as e:
            print(f"Error desconocido: {e}")
            return None

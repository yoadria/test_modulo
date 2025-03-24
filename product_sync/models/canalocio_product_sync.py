from odoo import fields, models, api
from odoo.exceptions import UserError
import requests
import csv
import logging
import copy

_logger = logging.getLogger(__name__)

class CanalocioSync(models.Model):
    _name = 'canalocio.sync'
    _description = ''

    location = fields.Char(string='URL de Conexion', required=True)
    #data = fields.Text(string="CSV Data")



    def action_fetch_data(self):
        """Conectarse a la URL y obtener los datos CSV."""
        try:
            response = requests.get(self.location, stream=True)  # Usamos la URL almacenada en el modelo
            response.raise_for_status()


            csv_reader = csv.DictReader(response.iter_lines(decode_unicode=True), delimiter=';')
            list_create = []


            BATCH_SIZE =2000

            # Cargar TODOS los códigos de barras existentes en una sola consulta
            existing_barcodes = set(self.env['product.template'].search_read([('barcode', '!=', False)], ['barcode']))
            existing_barcodes = {prod['barcode'] for prod in existing_barcodes}

            # Ahora guardamos los productos
            for row in csv_reader:
                barcode = row.get('ean13', '')
                if not barcode or not barcode.isdigit():
                    continue

                try:
                    price = row.get('pvp', '').replace(',', '')
                except:
                    price = 0.0

                 # Crear productos
                main_product = {
                    'name': row.get('titulo', 'Sin nombre'),
                    'barcode': barcode,
                    'list_price': price,
                }

                second_hand = copy.deepcopy(main_product)
                second_hand['barcode'] += 'OKA'
                second_hand['taxes_id'] = [(6, 0, [])]
                second_hand['default_code'] = 'Segunda Mano'

                #  Verificar existencia en `existing_barcodes`
                if barcode not in existing_barcodes:
                    list_create.append(main_product)
                    existing_barcodes.add(barcode)  # Lo agregamos al set para evitar duplicados en esta ejecución

                if second_hand['barcode'] not in existing_barcodes:
                    list_create.append(second_hand)
                    existing_barcodes.add(second_hand['barcode'])

                #  Insertar en lotes grandes para mejorar rendimiento
                if len(list_create) >= BATCH_SIZE:
                    self.env['product.template'].create(list_create)
                    list_create = []



            # Insertar restantes
            if list_create:
                self.env['product.template'].create(list_create)


        except Exception as e:
            _logger.error("Error crítico: %s", str(e))
            raise UserError(f"Falló la sincronización: {str(e)}")


    def update(self):
        try:
            # Buscar el registro por el campo 'location'
            url = 'http://www.canalocio.es/export_info.php?key=onan&val=834jds2k,23WZjd92Pas2S$2&datefrom=2024-08-01&outfile=0'
            backend = self.env['canalocio.sync'].search([('location', '=', url)], limit=1)

            if not backend:

                raise UserError("No se encontró el registro de Magento Backend con la URL proporcionada.")
            # Llamar al método 'action_fetch_data' de ese registro
            backend.action_fetch_data()
        except Exception:
            print('error al actualizar automaticamente')


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




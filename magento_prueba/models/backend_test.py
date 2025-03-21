from odoo import fields, models, api
from odoo.exceptions import UserError
import requests
import csv


class MagentoBackendTest(models.Model):
    _name = 'magento.backend.test'
    _inherit = 'connector.backend'
    _description = 'Magento Backend Test'

    location = fields.Char(string='URL de Conexion', required=True)
    #data = fields.Text(string="CSV Data")
    

    @api.model
    def _select_versions(self):
        return [('1.0', 'Version 1.0')]

    versions = fields.Selection(
        selection='_select_versions', required=False, default='1.0'
    )

       
    def action_fetch_data(self):
        """Conectarse a la URL y obtener los datos CSV."""
        response = requests.get(self.location)  # Usamos la URL almacenada en el modelo
        list_product_error=[]
        if response.status_code == 200:
            # Leer el CSV de manera incremental
            csv_reader = csv.DictReader(response.text.splitlines(), delimiter=';')  

            # Contador para limitar el número de productos procesados
            product_count = 0
            

            # Ahora guardamos los productos
            for row in csv_reader:
                # detener despues de procesar 5 productos
                # product_count += 1
                # if product_count > 50:
                #     break 
                
                
                # se mapea el diccionario para hacer la correlacion de los campos adecuada
                product_data = {
                    'name': row.get('titulo', ''),  # Usar get para evitar errores si el campo no existe
                    'barcode': row.get('ean13', ''),
                    'list_price': row.get('pvp', '')
                }
                
                # si el codigo de barra esta bacio se salta al siguiente producto
                if not product_data['barcode'] or not product_data['barcode'].strip():
                    product_count -=1
                    continue
                # se comprueba si el producto existe
                if self.get_producto(product_data['barcode']): 
                    # producto existe hacer comprovaciones de actualizacion
                    product_count -= 1
                else:
                    # se crea el producto
                    if self._create_product(product_data):
                        second_hand = product_data['barcode'] + 'OKA'
                        product_data['barcode'] = second_hand
                        self._create_product(product_data)
                    else: 
                        list_product_error.append(product_data)
                        print(row)
                        
            print(list_product_error)    
                    
        else:
            raise Exception(f"Error al obtener datos de la URL: {response.text}")
        
 

    def _create_product(self, product_data):
        """
        Crea un producto en product.template usando los datos proporcionados.
        
        :param product_data: Diccionario con los valores del producto, ejemplo:
                            {'name': 'Matrix Revolutions', 'barcode': '7321930178229'}
        """
        try:
            # Verificar que los campos esenciales están presentes
            name = product_data.get("name", "Producto sin nombre")  # Valor por defecto si no hay 'name'
            barcode = product_data.get("barcode", None)  # Puede ser None si no tiene código de barras
            if not barcode or barcode == 'OKA':
                #print(f"❌ No se puede crear el producto sin código de barras: {product_data}")
                return False
            
            # Crear el producto
            product_vals = {
                "name": name,
                "barcode": barcode,
                'list_price': product_data.get('list_price', 0.0).replace(",", ""),
            }
            
            if 'OKA' in barcode: # no añadirle los impuestos si es de segunda mano
                product_vals['taxes_id'] = [(6, 0, [])]  # Lista vacía de impuestos
            
            

            product = self.env["product.template"].create(product_vals)
            #print(f"✅ Producto creado: {product.name} con código de barras {product.barcode} precio: {product.list_price}")
            return True
        except Exception:
            #print(f"❌ Error al crear el producto: {product_data}")
            return False
            



    def get_producto(self, data):
        """
        Busca un producto en 'product.template' por su código de barras.

        :param data: String con el código de barras del producto.
        :return: Registro de 'product.template' si se encuentra, o false si no existe.
        """
        producto = self.env['product.template'].search([
            ('barcode', '=', data)  # Busca solo por código de barras exacto
        ], limit=1)

        if producto:
            # print(f"✅ Producto encontrado: {producto.name} (Barcode: {producto.barcode})")
            return producto
        else:
                    print(f"❌ No se encontró ningún producto con el código de barras {data}.")
                    return False

    def update(self):
        try:
            # Buscar el registro por el campo 'location'
            url = 'http://www.canalocio.es/export_info.php?key=onan&val=834jds2k,23WZjd92Pas2S$2&datefrom=2024-08-01&outfile=0'
            backend = self.env['magento.backend.test'].search([('location', '=', url)], limit=1)

            if not backend:
                raise UserError("No se encontró el registro de Magento Backend con la URL proporcionada.")

            # Llamar al método 'action_fetch_data' de ese registro
            backend.action_fetch_data()
        except Exception:
            print('error al actualizar automaticamente')
            
            

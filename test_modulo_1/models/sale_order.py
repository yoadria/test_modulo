from odoo import api, fields, models


# creamos la clase de nuestro modelo 
class SaleOrder(models.Model):
    _inherit = 'sale.order' # la clase es heredada de sale.order

    order_descuento = fields.Float(
        string='Descuento', # este sera el nombre del campo en la vista
        default=0.0, # valor por defecto del campo
        compute='_get_descuento',  # la funcion que se ejecutara para obtener el valor
        store=True, # almacenar el valor en la base de datos
        help='descuento por la venta' # proporciona un texto de ayuda para el campo
    )
    total_modificado = fields.Monetary(string="Total con descuento", store=True, compute='_compute_total_modificado', tracking=4)


    # estamos que dependemos del campo 'amount_total'(un campo de sale.order) que cada vez que se modifique haga la siguiente funcion
    @api.depends('amount_total')  
    def _get_descuento(self):
        for sale in self:
            sale.order_descuento = (sale.amount_total // 1000) * 100

    @api.depends('amount_total', 'order_descuento')
    def _compute_total_modificado(self):
        for sale in self:
            sale.total_modificado = sale.amount_total - sale.order_descuento
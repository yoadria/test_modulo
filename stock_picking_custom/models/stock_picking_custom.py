from odoo import api, fields, models

class StockPickingCustom(models.Model):
    _inherit = 'stock.picking'

    # Un campo de selección que permita asignar una prioridad a la transferencia. Debe tener al menos tres opciones: Baja, Media y Alta.
    priority_level = fields.Selection(
        selection=[
            ('low', 'Low'),
            ('normal', 'Normal'),
            ('high', 'High'),
        ],
        string='Priority Level',
        default='normal',
        help='The priority level of the picking.',
    )
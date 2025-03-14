from odoo import api, fields, models

class StockMoveLineCustom(models.Model):
    _inherit = 'stock.move.line'

    
    confirmed_by = fields.Many2one(
        comodel_name='res.users',
        string='Confirmed By',
        redaonly=True,
        help='The user who confirmed the picking.',
    )

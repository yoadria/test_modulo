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

    confirmed_by = fields.Many2one(
        comodel_name='res.users',
        string='Confirmed By',
        redaonly=True,
        help='The user who confirmed the picking.',
    )

    def button_validate(self):
        res = super().button_validate()
        self.confirmed_by = self.env.user  # Guarda el usuario actual
        for move in self.move_line_ids:
            move.confirmed_by = self.env.user

        print(f"El usuario >>>>> {self.confirmed_by.name} <<<<<<< confirmó la transferencia")
        return res
# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class test_modulo_2(models.Model):
#     _name = 'test_modulo_2.test_modulo_2'
#     _description = 'test_modulo_2.test_modulo_2'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class CurrencyExchangeRate(models.TransientModel):
    _name = 'currency.exchange.rate'
    _description = 'Currency Exchange Rate'


    moneda_origen_ids = fields.Many2one('res.currency', string='Moneda Origen', required=True)
    moneda_destino_ids = fields.Many2one('res.currency', string='Moneda Destino', required=True)
    fecha_tasa = fields.Date(string='Fecha de Tasa')
    tasa_cambio = fields.Float(string="Tasa de Cambio", readonly=True)

    @api.onchange('moneda_origen_ids', 'moneda_destino_ids')
    def _onchange_calcular_tasa(self):
        if self.moneda_origen_ids and self.moneda_destino_ids:
            print('moneda de origen >>> %s <<< ' % self.moneda_origen_ids.name)
            print('moneda de destino >>> %s <<< ' % self.moneda_destino_ids.name)
            if self.moneda_origen_ids.rate > 0 and self.moneda_destino_ids.rate > 0:
                self.tasa_cambio = self.moneda_destino_ids.rate / self.moneda_origen_ids.rate
            else:
                self.tasa_cambio = 0.0  # Para evitar errores si la tasa es 0
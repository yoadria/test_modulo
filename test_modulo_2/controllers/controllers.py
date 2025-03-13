# -*- coding: utf-8 -*-
# from odoo import http


# class TestModulo2(http.Controller):
#     @http.route('/test_modulo_2/test_modulo_2', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_modulo_2/test_modulo_2/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_modulo_2.listing', {
#             'root': '/test_modulo_2/test_modulo_2',
#             'objects': http.request.env['test_modulo_2.test_modulo_2'].search([]),
#         })

#     @http.route('/test_modulo_2/test_modulo_2/objects/<model("test_modulo_2.test_modulo_2"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_modulo_2.object', {
#             'object': obj
#         })


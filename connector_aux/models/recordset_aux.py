from odoo import models


class RecordSetAux(models.Model):
    _inherit = "import.recordset"

    # def import_recordset(self):
    #     """obtenemos el objeto import.source.csv y llamamos al método prueba"""

    #     # source_csv = self.env["import.source.csv"]
    #     # .search([("id", "=", self.source_id)])
    #     # job = source_csv.with_delay().prueba
    #     # if source_csv:
    #     #     job()
    #     #     return

    #     # Llama al método original de la clase padre

    #     super().import_recordset()

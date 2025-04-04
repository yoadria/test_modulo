from odoo import models

from ..utils.canalocio_import import HTTPCSVReader


class CanalocioCSVSource(models.Model):
    _inherit = "import.source.csv"

    _csv_reader_klass = HTTPCSVReader

    @property
    def _config_summary_fields(self):
        _fields = super()._config_summary_fields
        return _fields + [
            "csv_path",
        ]

    def _generate_csv_reader(self, reader_args):
        res = super()._generate_csv_reader(reader_args)
        if self.csv_path:
            self.csv_delimiter = res.delimiter
            self.csv_quotechar = res.quotechar
        return res

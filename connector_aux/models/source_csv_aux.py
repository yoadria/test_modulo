import logging

from odoo import models

from ..utils.import_utils import HTTPCSVReader

_logger = logging.getLogger(__name__)


class CSVAuxSource(models.Model):
    _inherit = "import.source.csv"

    _csv_reader_klass = HTTPCSVReader

    @property
    def _config_summary_fields(self):
        _fields = super()._config_summary_fields
        return _fields + [
            "csv_path",
        ]

    def prueba(self):
        _logger.info(">>>>>>>>>>>> Prueba <<<<<<<<<<<<<<<<")

        lines = list(self._get_lines())  # Read all lines into a list
        if lines:
            _logger.info(">>>>>>>> Prueba contenido completo <<<<<<<<<<<<<")
            for line in lines:
                _logger.info(line)

        else:
            _logger.info(">>>>>>>>>> Prueba no hay líneas <<<<<<<<<<")

        _logger.info(">>>>>> Prueba fin <<<<<<<<<<<<<")

    def _generate_csv_reader(self, reader_args):
        res = super()._generate_csv_reader(reader_args)
        if self.csv_path:
            self.csv_delimiter = res.delimiter
            self.csv_quotechar = res.quotechar
        return res

# Author: Rolando Pérez Rebollo
# Copyright 2025 Binhex
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from urllib.parse import urlparse

import requests

from odoo.addons.connector_importer.utils.import_utils import (
    CSVReader,
    csv_content_to_file,
    guess_csv_metadata,
)

# En esta seccion se obtiene de la url dentro del csv_path de la clase CSVSource
# el contenido del csv y se lo pasa a la clase CSVReader para que lo procese
# y lo convierta a un archivo csv para que pueda ser leido por el lector de csv
# de odoo.


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except Exception:
        return False


class HTTPCSVReader(CSVReader):
    """CSVReader with support for HTTP URLs."""

    def __init__(self, filepath=None, chunk_size=8192, **kwargs):
        if filepath and is_valid_url(filepath):
            # Use streaming for memory efficiency
            with requests.get(
                filepath,
                stream=True,
                timeout=30,
                headers={"Accept-Encoding": "gzip, deflate"},
            ) as response:
                response.raise_for_status()

                # Leemos el contenido de los chunks
                content = b""

                count = 0
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if count == 10:
                        break
                    count += 1
                    content += chunk

                if content:
                    content = csv_content_to_file(content)
                    content = self._normalize_line_endings(content)
                    meta = guess_csv_metadata(content)
                    kwargs.update(
                        {
                            k: v
                            for k, v in meta.items()
                            if k in ("delimiter", "quotechar")
                        }
                    )
                kwargs["filedata"] = content
                filepath = None

        super().__init__(filepath=filepath, **kwargs)

    def _normalize_line_endings(self, content):
        """Reemplaza todas las variantes de finales de línea con el estándar \n."""
        # Finales de línea comunes a reemplazar
        # (incluyendo \x85 que es el carácter de NUEVA LÍNEA)
        line_endings = [
            b"\x85",  # Next Line
        ]

        # Primero convierte todos los finales de línea a \n
        for ending in line_endings:
            content = content.replace(ending, b"\n")

        return content

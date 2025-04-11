import base64
import logging

import requests

_logger = logging.getLogger(__name__)


def parse_imgbase64(url):
    timeout = 50
    try:
        response = requests.get(url, stream=True, timeout=timeout)
        response.raise_for_status()
        img_base64 = base64.b64encode(response.content).decode()
        return img_base64
    except requests.exceptions.RequestException as e:
        _logger.info(f"Error al obtener imagen: {e}")
        return None
    except Exception as e:
        _logger.info(f"Error desconocido: {e}")
        return None


def decimal_control(num):
    try:
        return num.replace(",", "")
    except Exception:
        return "0.0"

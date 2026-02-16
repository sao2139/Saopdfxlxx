import pdfplumber
import re
from typing import Dict
from config.settings import PATRONES_BUSQUEDA

class PDFExtractor:
    """Motor lógico de extracción de datos."""

    @staticmethod
    def _clean_text(text: str) -> str:
        """Limpia espacios y saltos de línea."""
        if not text: return "No encontrado"
        return " ".join(text.split())

    def process_file(self, file_path: str) -> Dict[str, str]:
        """Abre un PDF y extrae la data basada en la configuración."""
        data = {}
        try:
            with pdfplumber.open(file_path) as pdf:
                # Solo procesamos la primera página por eficiencia
                page_obj = pdf.pages[0]
                text = page_obj.extract_text() or ""

                # Iteramos sobre los patrones definidos en settings.py
                # 1. Nombre
                match_nom = re.search(PATRONES_BUSQUEDA["nombre"], text, re.IGNORECASE)
                data['Nombre'] = self._clean_text(match_nom.group(1)) if match_nom else "N/A"

                # 2. Dirección (DOTALL permite saltos de línea)
                match_dir = re.search(PATRONES_BUSQUEDA["direccion"], text, re.DOTALL | re.IGNORECASE)
                data['Dirección'] = self._clean_text(match_dir.group(1)) if match_dir else "N/A"

                # 3. Fecha
                match_fecha = re.search(PATRONES_BUSQUEDA["fecha"], text)
                data['Fecha'] = self._clean_text(match_fecha.group(1)) if match_fecha else "N/A"

                return data
        except Exception as e:
            return {"Error": str(e)}
# Patrones Regex para extracción inteligente
PATRONES_BUSQUEDA = {
    "nombre": r"(?:Señor|Señora)\s+([A-Z\s]+)(?:,?\s+mediante|,)",
    "direccion": r"Dirección:\s*(.*?)(?=\n\s*Valor Asegurado|Valor Asegurado)",
    "fecha": r"([A-Za-z\s]+,\s+\d{1,2}\s+de\s+[A-Za-z]+\s+de\s+\d{4})"
}

# Configuración de la Ventana
APP_TITLE = "SaoPdfxlxx - Enterprise Lite"
APP_SIZE = "900x650"
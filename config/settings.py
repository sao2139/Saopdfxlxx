# Definición de patrones de Búsqueda (Regex)
PATRONES_BUSQUEDA = {
    # Busca texto en mayúsculas después de "Señor"
    "nombre": r"(?:Señor|Señora)\s+([A-Z\s]+)(?:,?\s+mediante|,)",
    
    # Busca dirección usando Lookahead para detenerse antes de "Valor Asegurado"
    "direccion": r"Dirección:\s*(.*?)(?=\n\s*Valor Asegurado|Valor Asegurado)",
    
    # Busca fechas estándar
    "fecha": r"([A-Za-z\s]+,\s+\d{1,2}\s+de\s+[A-Za-z]+\s+de\s+\d{4})"
}

# Configuración de apariencia
APP_TITLE = "SaoPdfxlxx - Enterprise"
APP_SIZE = "900x650"
THEME_COLOR = "green"  # Acorde a tu logo
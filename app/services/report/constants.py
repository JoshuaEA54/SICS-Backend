from pathlib import Path

_APP_DIR = Path(__file__).resolve().parent.parent.parent

TEMPLATE_DIR = _APP_DIR / "templates" / "report"
LOGO_PATH = _APP_DIR / "static" / "report" / "logo.png"

BAND_CONFIG = {
    "red": {
        "label": "Nivel crítico",
        "description": "Cumplimiento crítico — requiere mejoras urgentes.",
        "color": "#b91c1c",
        "bg": "#fee2e2",
        "border": "#fca5a5",
    },
    "amber": {
        "label": "Nivel deficiente",
        "description": "Cumplimiento deficiente — hay áreas de mejora relevantes.",
        "color": "#b45309",
        "bg": "#fef3c7",
        "border": "#fcd34d",
    },
    "lightGreen": {
        "label": "Nivel aceptable",
        "description": "Cumplimiento aceptable — mantener y mejorar.",
        "color": "#15803d",
        "bg": "#dcfce7",
        "border": "#86efac",
    },
    "darkGreen": {
        "label": "Nivel óptimo",
        "description": "Cumplimiento óptimo — excelente gestión de seguridad.",
        "color": "#166534",
        "bg": "#bbf7d0",
        "border": "#4ade80",
    },
}


def get_band(percentage: float) -> str:
    if percentage < 50:
        return "red"
    if percentage < 70:
        return "amber"
    if percentage < 90:
        return "lightGreen"
    return "darkGreen"

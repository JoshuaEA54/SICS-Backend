"""seed controls catalog

Revision ID: 20260412_0003
Revises: 20260412_0002
Create Date: 2026-04-12 00:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260412_0003"
down_revision: str | None = "20260412_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ── Standards ────────────────────────────────────────────────

    standards_table = sa.table(
        "standards",
        sa.column("id", sa.Integer()),
        sa.column("name", sa.String()),
    )

    op.bulk_insert(
        standards_table,
        [
            {"id": 1, "name": "ISO27001"},
            {"id": 2, "name": "ISO27002_2022"},
            {"id": 3, "name": "ISO27005"},
            {"id": 4, "name": "ISO27701"},
            {"id": 5, "name": "NIST_CSF_v1.1"},
            {"id": 6, "name": "LEY8968_CR"},
        ],
    )

    # ── Control groups ───────────────────────────────────────────

    control_groups_table = sa.table(
        "control_groups",
        sa.column("id", sa.String()),
        sa.column("name", sa.String()),
        sa.column("description", sa.Text()),
        sa.column("criticality", sa.String()),
    )

    op.bulk_insert(
        control_groups_table,
        [
            {
                "id": "G01",
                "name": "Gobierno y gestión de la seguridad",
                "description": "Política general de seguridad roles responsabilidades mejora continua",
                "criticality": "high",
            },
            {
                "id": "G02",
                "name": "Gestión de riesgos",
                "description": "Identificación análisis tratamiento y aceptación de riesgos",
                "criticality": "high",
            },
            {
                "id": "G03",
                "name": "Gestión de activos y clasificación de la información",
                "description": "Inventario propietarios clasificación y manejo de activos e información",
                "criticality": "high",
            },
            {
                "id": "G04",
                "name": "Control de acceso e identidad (IAM)",
                "description": "Gestión de usuarios privilegios autenticación y accesos remotos",
                "criticality": "high",
            },
            {
                "id": "G05",
                "name": "Uso aceptable y concienciación",
                "description": "Políticas de uso capacitación concienciación y responsabilidades del personal",
                "criticality": "medium",
            },
            {
                "id": "G06",
                "name": "Criptografía y protección de la información",
                "description": "Cifrado en reposo y tránsito gestión de llaves y protección de respaldos",
                "criticality": "high",
            },
            {
                "id": "G07",
                "name": "Seguridad operacional y hardening",
                "description": "Configuración segura antimalware firewalls y operación de sistemas",
                "criticality": "high",
            },
            {
                "id": "G08",
                "name": "Gestión de vulnerabilidades y parches",
                "description": "Escaneo de vulnerabilidades parcheo y gestión de obsolescencia",
                "criticality": "high",
            },
            {
                "id": "G09",
                "name": "Registro monitoreo y detección",
                "description": "Logs monitoreo alertas y detección de eventos de seguridad",
                "criticality": "medium",
            },
            {
                "id": "G10",
                "name": "Gestión de incidentes de seguridad",
                "description": "Detección respuesta notificación y lecciones aprendidas",
                "criticality": "high",
            },
            {
                "id": "G11",
                "name": "Continuidad del negocio y respaldos",
                "description": "Backups continuidad operativa recuperación ante desastres y pruebas",
                "criticality": "high",
            },
            {
                "id": "G12",
                "name": "Proveedores y terceros",
                "description": "Evaluación de proveedores cláusulas de seguridad y transferencia de datos",
                "criticality": "high",
            },
            {
                "id": "G13",
                "name": "Protección de datos personales",
                "description": "Medidas técnicas y organizativas para datos personales y sensibles",
                "criticality": "high",
            },
            {
                "id": "G14",
                "name": "Consentimiento derechos y retención",
                "description": "Consentimiento informado retención eliminación y derechos ARCO",
                "criticality": "high",
            },
            {
                "id": "G15",
                "name": "Desarrollo seguro y control de cambios",
                "description": "Seguridad en el desarrollo control de cambios pruebas y versiones",
                "criticality": "medium",
            },
            {
                "id": "G16",
                "name": "Seguridad física y ambiental",
                "description": "Control de acceso físico energía climatización y protección ambiental",
                "criticality": "medium",
            },
        ],
    )

    # ── Controls ─────────────────────────────────────────────────

    controls_table = sa.table(
        "controls",
        sa.column("id", sa.String()),
        sa.column("group_id", sa.String()),
        sa.column("name", sa.String()),
        sa.column("description", sa.Text()),
    )

    op.bulk_insert(
        controls_table,
        [
            {"id": "CC-GOV-01", "group_id": "G01", "name": "Política de seguridad de la información", "description": "Existe una política formal aprobada y comunicada"},
            {"id": "CC-GOV-02", "group_id": "G01", "name": "Roles y responsabilidades", "description": "Roles de seguridad definidos y asignados"},
            {"id": "CC-GOV-03", "group_id": "G01", "name": "Revisión del ISMS", "description": "Revisión periódica del sistema de gestión"},
            {"id": "CC-RISK-01", "group_id": "G02", "name": "Identificación de riesgos", "description": "Identificación sistemática de riesgos de seguridad"},
            {"id": "CC-RISK-02", "group_id": "G02", "name": "Análisis y valoración", "description": "Análisis y valoración documentada de riesgos"},
            {"id": "CC-RISK-03", "group_id": "G02", "name": "Tratamiento de riesgos", "description": "Planes de tratamiento definidos y aprobados"},
            {"id": "CC-ASSET-01", "group_id": "G03", "name": "Inventario de activos", "description": "Inventario actualizado de activos de información"},
            {"id": "CC-ASSET-02", "group_id": "G03", "name": "Clasificación de la información", "description": "Clasificación según sensibilidad"},
            {"id": "CC-AC-01", "group_id": "G04", "name": "Gestión de usuarios", "description": "Proceso formal de altas bajas y cambios"},
            {"id": "CC-AC-02", "group_id": "G04", "name": "Autenticación fuerte", "description": "Uso de MFA en accesos críticos"},
            {"id": "CC-AC-03", "group_id": "G04", "name": "Privilegios mínimos", "description": "Principio de menor privilegio"},
            {"id": "CC-HR-01", "group_id": "G05", "name": "Uso aceptable", "description": "Política de uso aceptable firmada"},
            {"id": "CC-HR-02", "group_id": "G05", "name": "Capacitación", "description": "Capacitación periódica en seguridad"},
            {"id": "CC-CRYP-01", "group_id": "G06", "name": "Cifrado de datos", "description": "Datos cifrados en reposo y tránsito"},
            {"id": "CC-CRYP-02", "group_id": "G06", "name": "Gestión de llaves", "description": "Gestión segura de llaves criptográficas"},
            {"id": "CC-OPS-01", "group_id": "G07", "name": "Hardening de sistemas", "description": "Configuración segura de sistemas"},
            {"id": "CC-OPS-02", "group_id": "G07", "name": "Protección antimalware", "description": "Uso de antimalware actualizado"},
            {"id": "CC-VULN-01", "group_id": "G08", "name": "Escaneo de vulnerabilidades", "description": "Escaneos periódicos documentados"},
            {"id": "CC-VULN-02", "group_id": "G08", "name": "Gestión de parches", "description": "Parches aplicados oportunamente"},
            {"id": "CC-LOG-01", "group_id": "G09", "name": "Registro de eventos", "description": "Logs habilitados y protegidos"},
            {"id": "CC-INC-01", "group_id": "G10", "name": "Gestión de incidentes", "description": "Proceso formal de respuesta a incidentes"},
            {"id": "CC-BCP-01", "group_id": "G11", "name": "Respaldos", "description": "Respaldos periódicos y probados"},
            {"id": "CC-BCP-02", "group_id": "G11", "name": "DRP", "description": "Plan de recuperación ante desastres"},
            {"id": "CC-SUP-01", "group_id": "G12", "name": "Evaluación de proveedores", "description": "Evaluación de seguridad de proveedores"},
            {"id": "CC-PRIV-01", "group_id": "G13", "name": "Protección de datos personales", "description": "Medidas técnicas y organizativas para datos personales"},
            {"id": "CC-PRIV-02", "group_id": "G13", "name": "Acceso restringido a datos", "description": "Acceso limitado a datos personales"},
            {"id": "CC-CONS-01", "group_id": "G14", "name": "Gestión de consentimiento", "description": "Consentimiento informado documentado"},
            {"id": "CC-CONS-02", "group_id": "G14", "name": "Retención y eliminación", "description": "Retención y eliminación conforme a política"},
            {"id": "CC-DEV-01", "group_id": "G15", "name": "Desarrollo seguro", "description": "Prácticas de desarrollo seguro"},
            {"id": "CC-PHYS-01", "group_id": "G16", "name": "Control de acceso físico", "description": "Acceso físico restringido a áreas críticas"},
        ],
    )

    # ── Control standard refs ────────────────────────────────────
    # standard_id map: ISO27001=1, ISO27002_2022=2, ISO27005=3, ISO27701=4, NIST_CSF_v1.1=5, LEY8968_CR=6

    control_standard_refs_table = sa.table(
        "control_standard_refs",
        sa.column("id", sa.Integer()),
        sa.column("control_id", sa.String()),
        sa.column("standard_id", sa.Integer()),
        sa.column("ref_code", sa.String()),
    )

    op.bulk_insert(
        control_standard_refs_table,
        [
            # ── ISO27001 (standard_id=1) ──────────────────────────
            {"id": 1,   "control_id": "CC-GOV-01",  "standard_id": 1, "ref_code": "5.2"},
            {"id": 2,   "control_id": "CC-GOV-01",  "standard_id": 1, "ref_code": "A.5.1.1"},
            {"id": 3,   "control_id": "CC-GOV-02",  "standard_id": 1, "ref_code": "5.3"},
            {"id": 4,   "control_id": "CC-GOV-02",  "standard_id": 1, "ref_code": "A.6.1.1"},
            {"id": 5,   "control_id": "CC-GOV-03",  "standard_id": 1, "ref_code": "9.3"},
            {"id": 6,   "control_id": "CC-RISK-01", "standard_id": 1, "ref_code": "6.1.2"},
            {"id": 7,   "control_id": "CC-RISK-02", "standard_id": 1, "ref_code": "6.1.2"},
            {"id": 8,   "control_id": "CC-RISK-03", "standard_id": 1, "ref_code": "6.1.3"},
            {"id": 9,   "control_id": "CC-ASSET-01","standard_id": 1, "ref_code": "8.1"},
            {"id": 10,  "control_id": "CC-ASSET-01","standard_id": 1, "ref_code": "A.8.1.1"},
            {"id": 11,  "control_id": "CC-ASSET-02","standard_id": 1, "ref_code": "A.8.2.1"},
            {"id": 12,  "control_id": "CC-AC-01",   "standard_id": 1, "ref_code": "9.2.1"},
            {"id": 13,  "control_id": "CC-AC-01",   "standard_id": 1, "ref_code": "A.9.2.1"},
            {"id": 14,  "control_id": "CC-AC-02",   "standard_id": 1, "ref_code": "A.9.4.2"},
            {"id": 15,  "control_id": "CC-AC-03",   "standard_id": 1, "ref_code": "A.9.1.2"},
            {"id": 16,  "control_id": "CC-HR-01",   "standard_id": 1, "ref_code": "7.2.2"},
            {"id": 17,  "control_id": "CC-HR-01",   "standard_id": 1, "ref_code": "A.7.2.2"},
            {"id": 18,  "control_id": "CC-HR-02",   "standard_id": 1, "ref_code": "7.2.2"},
            {"id": 19,  "control_id": "CC-HR-02",   "standard_id": 1, "ref_code": "A.7.2.2"},
            {"id": 20,  "control_id": "CC-CRYP-01", "standard_id": 1, "ref_code": "A.10.1.1"},
            {"id": 21,  "control_id": "CC-CRYP-02", "standard_id": 1, "ref_code": "A.10.1.2"},
            {"id": 22,  "control_id": "CC-OPS-01",  "standard_id": 1, "ref_code": "A.12.1.2"},
            {"id": 23,  "control_id": "CC-OPS-02",  "standard_id": 1, "ref_code": "A.12.2.1"},
            {"id": 24,  "control_id": "CC-VULN-01", "standard_id": 1, "ref_code": "A.12.6.1"},
            {"id": 25,  "control_id": "CC-VULN-02", "standard_id": 1, "ref_code": "A.12.6.1"},
            {"id": 26,  "control_id": "CC-LOG-01",  "standard_id": 1, "ref_code": "A.12.4.1"},
            {"id": 27,  "control_id": "CC-INC-01",  "standard_id": 1, "ref_code": "A.16.1.1"},
            {"id": 28,  "control_id": "CC-BCP-01",  "standard_id": 1, "ref_code": "A.17.1.1"},
            {"id": 29,  "control_id": "CC-BCP-02",  "standard_id": 1, "ref_code": "A.17.1.2"},
            {"id": 30,  "control_id": "CC-SUP-01",  "standard_id": 1, "ref_code": "A.15.1.1"},
            {"id": 31,  "control_id": "CC-PRIV-01", "standard_id": 1, "ref_code": "A.18.1.4"},
            {"id": 32,  "control_id": "CC-PRIV-02", "standard_id": 1, "ref_code": "A.9.4.1"},
            {"id": 33,  "control_id": "CC-CONS-01", "standard_id": 1, "ref_code": "A.18.1.4"},
            {"id": 34,  "control_id": "CC-CONS-02", "standard_id": 1, "ref_code": "A.18.1.3"},
            {"id": 35,  "control_id": "CC-DEV-01",  "standard_id": 1, "ref_code": "A.14.2.1"},
            {"id": 36,  "control_id": "CC-PHYS-01", "standard_id": 1, "ref_code": "A.11.1.1"},
            # ── ISO27002_2022 (standard_id=2) ─────────────────────
            {"id": 37,  "control_id": "CC-GOV-01",  "standard_id": 2, "ref_code": "5.1"},
            {"id": 38,  "control_id": "CC-GOV-02",  "standard_id": 2, "ref_code": "5.2"},
            {"id": 39,  "control_id": "CC-GOV-03",  "standard_id": 2, "ref_code": "5.36"},
            {"id": 40,  "control_id": "CC-GOV-03",  "standard_id": 2, "ref_code": "5.37"},
            {"id": 41,  "control_id": "CC-RISK-01", "standard_id": 2, "ref_code": "5.4"},
            {"id": 42,  "control_id": "CC-RISK-02", "standard_id": 2, "ref_code": "5.4"},
            {"id": 43,  "control_id": "CC-RISK-03", "standard_id": 2, "ref_code": "5.5"},
            {"id": 44,  "control_id": "CC-ASSET-01","standard_id": 2, "ref_code": "5.9"},
            {"id": 45,  "control_id": "CC-ASSET-02","standard_id": 2, "ref_code": "5.12"},
            {"id": 46,  "control_id": "CC-ASSET-02","standard_id": 2, "ref_code": "5.13"},
            {"id": 47,  "control_id": "CC-AC-01",   "standard_id": 2, "ref_code": "5.16"},
            {"id": 48,  "control_id": "CC-AC-01",   "standard_id": 2, "ref_code": "5.18"},
            {"id": 49,  "control_id": "CC-AC-02",   "standard_id": 2, "ref_code": "5.17"},
            {"id": 50,  "control_id": "CC-AC-03",   "standard_id": 2, "ref_code": "5.18"},
            {"id": 51,  "control_id": "CC-HR-01",   "standard_id": 2, "ref_code": "5.10"},
            {"id": 52,  "control_id": "CC-HR-01",   "standard_id": 2, "ref_code": "6.2"},
            {"id": 53,  "control_id": "CC-HR-02",   "standard_id": 2, "ref_code": "6.3"},
            {"id": 54,  "control_id": "CC-OPS-01",  "standard_id": 2, "ref_code": "8.9"},
            {"id": 55,  "control_id": "CC-OPS-02",  "standard_id": 2, "ref_code": "8.7"},
            {"id": 56,  "control_id": "CC-VULN-01", "standard_id": 2, "ref_code": "8.8"},
            {"id": 57,  "control_id": "CC-VULN-02", "standard_id": 2, "ref_code": "8.8"},
            {"id": 58,  "control_id": "CC-LOG-01",  "standard_id": 2, "ref_code": "8.15"},
            {"id": 59,  "control_id": "CC-LOG-01",  "standard_id": 2, "ref_code": "8.16"},
            {"id": 60,  "control_id": "CC-INC-01",  "standard_id": 2, "ref_code": "5.24"},
            {"id": 61,  "control_id": "CC-INC-01",  "standard_id": 2, "ref_code": "5.26"},
            {"id": 62,  "control_id": "CC-INC-01",  "standard_id": 2, "ref_code": "5.27"},
            {"id": 63,  "control_id": "CC-INC-01",  "standard_id": 2, "ref_code": "5.28"},
            {"id": 64,  "control_id": "CC-BCP-01",  "standard_id": 2, "ref_code": "8.13"},
            {"id": 65,  "control_id": "CC-BCP-02",  "standard_id": 2, "ref_code": "8.14"},
            {"id": 66,  "control_id": "CC-SUP-01",  "standard_id": 2, "ref_code": "5.19"},
            {"id": 67,  "control_id": "CC-SUP-01",  "standard_id": 2, "ref_code": "5.20"},
            {"id": 68,  "control_id": "CC-SUP-01",  "standard_id": 2, "ref_code": "5.23"},
            {"id": 69,  "control_id": "CC-PRIV-01", "standard_id": 2, "ref_code": "5.34"},
            {"id": 70,  "control_id": "CC-PRIV-02", "standard_id": 2, "ref_code": "5.15"},
            {"id": 71,  "control_id": "CC-PRIV-02", "standard_id": 2, "ref_code": "5.16"},
            {"id": 72,  "control_id": "CC-PRIV-02", "standard_id": 2, "ref_code": "5.18"},
            {"id": 73,  "control_id": "CC-DEV-01",  "standard_id": 2, "ref_code": "8.25"},
            {"id": 74,  "control_id": "CC-PHYS-01", "standard_id": 2, "ref_code": "7.1"},
            {"id": 75,  "control_id": "CC-PHYS-01", "standard_id": 2, "ref_code": "7.2"},
            # ── ISO27005 (standard_id=3) ──────────────────────────
            {"id": 76,  "control_id": "CC-RISK-01", "standard_id": 3, "ref_code": "Risk identification"},
            {"id": 77,  "control_id": "CC-RISK-02", "standard_id": 3, "ref_code": "Risk analysis"},
            {"id": 78,  "control_id": "CC-RISK-02", "standard_id": 3, "ref_code": "Risk evaluation"},
            {"id": 79,  "control_id": "CC-RISK-03", "standard_id": 3, "ref_code": "Risk treatment"},
            {"id": 80,  "control_id": "CC-RISK-03", "standard_id": 3, "ref_code": "Risk acceptance"},
            {"id": 81,  "control_id": "CC-GOV-03",  "standard_id": 3, "ref_code": "Monitoring and review"},
            # ── ISO27701 (standard_id=4) ──────────────────────────
            {"id": 82,  "control_id": "CC-SUP-01",  "standard_id": 4, "ref_code": "7.2 Supplier relationships (PII)"},
            {"id": 83,  "control_id": "CC-PRIV-01", "standard_id": 4, "ref_code": "6.7 Information security aspects of business continuity management (PII)"},
            {"id": 84,  "control_id": "CC-PRIV-01", "standard_id": 4, "ref_code": "6.8 Physical and environmental security (PII)"},
            {"id": 85,  "control_id": "CC-PRIV-02", "standard_id": 4, "ref_code": "6.10 Access control (PII)"},
            {"id": 86,  "control_id": "CC-CONS-01", "standard_id": 4, "ref_code": "7.3 Consent and choice"},
            {"id": 87,  "control_id": "CC-CONS-02", "standard_id": 4, "ref_code": "7.4 Privacy by design and privacy by default"},
            # ── NIST_CSF_v1.1 (standard_id=5) ────────────────────
            {"id": 88,  "control_id": "CC-GOV-01",  "standard_id": 5, "ref_code": "ID.GV-1"},
            {"id": 89,  "control_id": "CC-GOV-02",  "standard_id": 5, "ref_code": "ID.GV-2"},
            {"id": 90,  "control_id": "CC-GOV-03",  "standard_id": 5, "ref_code": "ID.GV-4"},
            {"id": 91,  "control_id": "CC-RISK-01", "standard_id": 5, "ref_code": "ID.RA-1"},
            {"id": 92,  "control_id": "CC-RISK-02", "standard_id": 5, "ref_code": "ID.RA-2"},
            {"id": 93,  "control_id": "CC-RISK-03", "standard_id": 5, "ref_code": "ID.RA-3"},
            {"id": 94,  "control_id": "CC-ASSET-01","standard_id": 5, "ref_code": "ID.AM-1"},
            {"id": 95,  "control_id": "CC-ASSET-02","standard_id": 5, "ref_code": "ID.AM-5"},
            {"id": 96,  "control_id": "CC-AC-01",   "standard_id": 5, "ref_code": "PR.AC-1"},
            {"id": 97,  "control_id": "CC-AC-02",   "standard_id": 5, "ref_code": "PR.AC-7"},
            {"id": 98,  "control_id": "CC-AC-03",   "standard_id": 5, "ref_code": "PR.AC-4"},
            {"id": 99,  "control_id": "CC-HR-01",   "standard_id": 5, "ref_code": "PR.AT-1"},
            {"id": 100, "control_id": "CC-HR-02",   "standard_id": 5, "ref_code": "PR.AT-2"},
            {"id": 101, "control_id": "CC-CRYP-01", "standard_id": 5, "ref_code": "PR.DS-1"},
            {"id": 102, "control_id": "CC-CRYP-02", "standard_id": 5, "ref_code": "PR.DS-7"},
            {"id": 103, "control_id": "CC-OPS-01",  "standard_id": 5, "ref_code": "PR.IP-1"},
            {"id": 104, "control_id": "CC-OPS-02",  "standard_id": 5, "ref_code": "PR.IP-12"},
            {"id": 105, "control_id": "CC-VULN-01", "standard_id": 5, "ref_code": "DE.CM-8"},
            {"id": 106, "control_id": "CC-VULN-02", "standard_id": 5, "ref_code": "PR.IP-3"},
            {"id": 107, "control_id": "CC-LOG-01",  "standard_id": 5, "ref_code": "DE.CM-1"},
            {"id": 108, "control_id": "CC-INC-01",  "standard_id": 5, "ref_code": "RS.RP-1"},
            {"id": 109, "control_id": "CC-BCP-01",  "standard_id": 5, "ref_code": "RC.RP-1"},
            {"id": 110, "control_id": "CC-BCP-02",  "standard_id": 5, "ref_code": "RC.IM-1"},
            {"id": 111, "control_id": "CC-SUP-01",  "standard_id": 5, "ref_code": "ID.SC-1"},
            {"id": 112, "control_id": "CC-PRIV-01", "standard_id": 5, "ref_code": "PR.DS-5"},
            {"id": 113, "control_id": "CC-PRIV-02", "standard_id": 5, "ref_code": "PR.AC-4"},
            # ── LEY8968_CR (standard_id=6) ────────────────────────
            {"id": 114, "control_id": "CC-ASSET-01","standard_id": 6, "ref_code": "Art. 10 (Seguridad de los datos)"},
            {"id": 115, "control_id": "CC-ASSET-02","standard_id": 6, "ref_code": "Art. 10 (Seguridad de los datos)"},
            {"id": 116, "control_id": "CC-CRYP-01", "standard_id": 6, "ref_code": "Art. 10 (Seguridad de los datos)"},
            {"id": 117, "control_id": "CC-INC-01",  "standard_id": 6, "ref_code": "Art. 10 (Seguridad de los datos)"},
            {"id": 118, "control_id": "CC-SUP-01",  "standard_id": 6, "ref_code": "Art. 10 (Seguridad de los datos)"},
            {"id": 119, "control_id": "CC-PRIV-01", "standard_id": 6, "ref_code": "Art. 10 (Seguridad de los datos)"},
            {"id": 120, "control_id": "CC-PRIV-02", "standard_id": 6, "ref_code": "Art. 10 (Seguridad de los datos)"},
            {"id": 121, "control_id": "CC-CONS-01", "standard_id": 6, "ref_code": "Art. 5 (Consentimiento informado)"},
            {"id": 122, "control_id": "CC-CONS-02", "standard_id": 6, "ref_code": "Art. 10 (Seguridad de los datos)"},
        ],
    )

    # Reset sequences so future inserts don't collide with seeded IDs
    op.execute(sa.text("SELECT setval(pg_get_serial_sequence('standards', 'id'), MAX(id)) FROM standards"))
    op.execute(sa.text("SELECT setval(pg_get_serial_sequence('control_standard_refs', 'id'), MAX(id)) FROM control_standard_refs"))


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM control_standard_refs"))
    op.execute(sa.text("DELETE FROM controls"))
    op.execute(sa.text("DELETE FROM control_groups"))
    op.execute(sa.text("DELETE FROM standards"))

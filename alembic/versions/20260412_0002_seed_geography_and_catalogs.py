"""seed geography and catalogs

Revision ID: 20260412_0002
Revises: 20260329_0001
Create Date: 2026-04-12 00:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260412_0002"
down_revision: str | None = "20260329_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ── Tablas de referencia ──────────────────────────────────────────────────

    provinces_t = sa.table("provinces",
        sa.column("id", sa.SmallInteger),
        sa.column("name", sa.String),
    )
    cantons_t = sa.table("cantons",
        sa.column("id", sa.SmallInteger),
        sa.column("name", sa.String),
        sa.column("province_id", sa.SmallInteger),
    )
    districts_t = sa.table("districts",
        sa.column("id", sa.SmallInteger),
        sa.column("name", sa.String),
        sa.column("canton_id", sa.SmallInteger),
    )
    sectors_t = sa.table("sectors",
        sa.column("id", sa.SmallInteger),
        sa.column("name", sa.String),
    )
    employee_ranges_t = sa.table("employee_ranges",
        sa.column("id", sa.SmallInteger),
        sa.column("label", sa.String),
    )

    # ── Provincias ────────────────────────────────────────────────────────────

    op.bulk_insert(provinces_t, [
        {"id": 1, "name": "San José"},
        {"id": 2, "name": "Alajuela"},
        {"id": 3, "name": "Cartago"},
        {"id": 4, "name": "Heredia"},
        {"id": 5, "name": "Guanacaste"},
        {"id": 6, "name": "Puntarenas"},
        {"id": 7, "name": "Limón"},
    ])

    # ── Cantones ──────────────────────────────────────────────────────────────
    # IDs secuenciales: San José 1-20, Alajuela 21-36, Cartago 37-44,
    #                   Heredia 45-54, Guanacaste 55-65, Puntarenas 66-76, Limón 77-82

    op.bulk_insert(cantons_t, [
        # San José (province_id=1)
        {"id":  1, "name": "Central",              "province_id": 1},
        {"id":  2, "name": "Escazú",               "province_id": 1},
        {"id":  3, "name": "Desamparados",         "province_id": 1},
        {"id":  4, "name": "Puriscal",             "province_id": 1},
        {"id":  5, "name": "Tarrazú",              "province_id": 1},
        {"id":  6, "name": "Aserrí",               "province_id": 1},
        {"id":  7, "name": "Mora",                 "province_id": 1},
        {"id":  8, "name": "Goicoechea",           "province_id": 1},
        {"id":  9, "name": "Santa Ana",            "province_id": 1},
        {"id": 10, "name": "Alajuelita",           "province_id": 1},
        {"id": 11, "name": "Vázquez De Coronado",  "province_id": 1},
        {"id": 12, "name": "Acosta",               "province_id": 1},
        {"id": 13, "name": "Tibás",                "province_id": 1},
        {"id": 14, "name": "Moravia",              "province_id": 1},
        {"id": 15, "name": "Montes De Oca",        "province_id": 1},
        {"id": 16, "name": "Turrubares",           "province_id": 1},
        {"id": 17, "name": "Dota",                 "province_id": 1},
        {"id": 18, "name": "Curridabat",           "province_id": 1},
        {"id": 19, "name": "Pérez Zeledón",        "province_id": 1},
        {"id": 20, "name": "León Cortés Castro",   "province_id": 1},
        # Alajuela (province_id=2)
        {"id": 21, "name": "Central",              "province_id": 2},
        {"id": 22, "name": "San Ramón",            "province_id": 2},
        {"id": 23, "name": "Grecia",               "province_id": 2},
        {"id": 24, "name": "San Mateo",            "province_id": 2},
        {"id": 25, "name": "Atenas",               "province_id": 2},
        {"id": 26, "name": "Naranjo",              "province_id": 2},
        {"id": 27, "name": "Palmares",             "province_id": 2},
        {"id": 28, "name": "Poás",                 "province_id": 2},
        {"id": 29, "name": "Orotina",              "province_id": 2},
        {"id": 30, "name": "San Carlos",           "province_id": 2},
        {"id": 31, "name": "Zarcero",              "province_id": 2},
        {"id": 32, "name": "Sarchí",               "province_id": 2},
        {"id": 33, "name": "Upala",                "province_id": 2},
        {"id": 34, "name": "Los Chiles",           "province_id": 2},
        {"id": 35, "name": "Guatuso",              "province_id": 2},
        {"id": 36, "name": "Río Cuarto",           "province_id": 2},
        # Cartago (province_id=3)
        {"id": 37, "name": "Central",              "province_id": 3},
        {"id": 38, "name": "Paraíso",              "province_id": 3},
        {"id": 39, "name": "La Unión",             "province_id": 3},
        {"id": 40, "name": "Jiménez",              "province_id": 3},
        {"id": 41, "name": "Turrialba",            "province_id": 3},
        {"id": 42, "name": "Alvarado",             "province_id": 3},
        {"id": 43, "name": "Oreamuno",             "province_id": 3},
        {"id": 44, "name": "El Guarco",            "province_id": 3},
        # Heredia (province_id=4)
        {"id": 45, "name": "Central",              "province_id": 4},
        {"id": 46, "name": "Barva",                "province_id": 4},
        {"id": 47, "name": "Santo Domingo",        "province_id": 4},
        {"id": 48, "name": "Santa Bárbara",        "province_id": 4},
        {"id": 49, "name": "San Rafael",           "province_id": 4},
        {"id": 50, "name": "San Isidro",           "province_id": 4},
        {"id": 51, "name": "Belén",                "province_id": 4},
        {"id": 52, "name": "Flores",               "province_id": 4},
        {"id": 53, "name": "San Pablo",            "province_id": 4},
        {"id": 54, "name": "Sarapiquí",            "province_id": 4},
        # Guanacaste (province_id=5)
        {"id": 55, "name": "Liberia",              "province_id": 5},
        {"id": 56, "name": "Nicoya",               "province_id": 5},
        {"id": 57, "name": "Santa Cruz",           "province_id": 5},
        {"id": 58, "name": "Bagaces",              "province_id": 5},
        {"id": 59, "name": "Carrillo",             "province_id": 5},
        {"id": 60, "name": "Cañas",                "province_id": 5},
        {"id": 61, "name": "Abangares",            "province_id": 5},
        {"id": 62, "name": "Tilarán",              "province_id": 5},
        {"id": 63, "name": "Nandayure",            "province_id": 5},
        {"id": 64, "name": "La Cruz",              "province_id": 5},
        {"id": 65, "name": "Hojancha",             "province_id": 5},
        # Puntarenas (province_id=6)
        {"id": 66, "name": "Central",              "province_id": 6},
        {"id": 67, "name": "Esparza",              "province_id": 6},
        {"id": 68, "name": "Buenos Aires",         "province_id": 6},
        {"id": 69, "name": "Montes De Oro",        "province_id": 6},
        {"id": 70, "name": "Osa",                  "province_id": 6},
        {"id": 71, "name": "Quepos",               "province_id": 6},
        {"id": 72, "name": "Golfito",              "province_id": 6},
        {"id": 73, "name": "Coto Brus",            "province_id": 6},
        {"id": 74, "name": "Parrita",              "province_id": 6},
        {"id": 75, "name": "Corredores",           "province_id": 6},
        {"id": 76, "name": "Garabito",             "province_id": 6},
        # Limón (province_id=7)
        {"id": 77, "name": "Central",              "province_id": 7},
        {"id": 78, "name": "Pococí",               "province_id": 7},
        {"id": 79, "name": "Siquirres",            "province_id": 7},
        {"id": 80, "name": "Talamanca",            "province_id": 7},
        {"id": 81, "name": "Matina",               "province_id": 7},
        {"id": 82, "name": "Guácimo",              "province_id": 7},
    ])

    # ── Distritos ─────────────────────────────────────────────────────────────
    # IDs secuenciales globales (1-479)

    op.bulk_insert(districts_t, [
        # ── San José → Central (canton_id=1) ─────────
        {"id":   1, "name": "Carmen",                    "canton_id":  1},
        {"id":   2, "name": "Merced",                    "canton_id":  1},
        {"id":   3, "name": "Hospital",                  "canton_id":  1},
        {"id":   4, "name": "Catedral",                  "canton_id":  1},
        {"id":   5, "name": "Zapote",                    "canton_id":  1},
        {"id":   6, "name": "San Francisco De Dos Rios", "canton_id":  1},
        {"id":   7, "name": "Uruca",                     "canton_id":  1},
        {"id":   8, "name": "Mata Redonda",              "canton_id":  1},
        {"id":   9, "name": "Pavas",                     "canton_id":  1},
        {"id":  10, "name": "Hatillo",                   "canton_id":  1},
        {"id":  11, "name": "San Sebastián",             "canton_id":  1},
        # ── San José → Escazú (canton_id=2) ──────────
        {"id":  12, "name": "Escazú",                    "canton_id":  2},
        {"id":  13, "name": "San Antonio",               "canton_id":  2},
        {"id":  14, "name": "San Rafael",                "canton_id":  2},
        # ── San José → Desamparados (canton_id=3) ────
        {"id":  15, "name": "Desamparados",              "canton_id":  3},
        {"id":  16, "name": "San Miguel",                "canton_id":  3},
        {"id":  17, "name": "San Juan De Dios",          "canton_id":  3},
        {"id":  18, "name": "San Rafael Arriba",         "canton_id":  3},
        {"id":  19, "name": "San Rafael Abajo",          "canton_id":  3},
        {"id":  20, "name": "San Antonio",               "canton_id":  3},
        {"id":  21, "name": "Frailes",                   "canton_id":  3},
        {"id":  22, "name": "Patarra",                   "canton_id":  3},
        {"id":  23, "name": "San Cristobal",             "canton_id":  3},
        {"id":  24, "name": "Rosario",                   "canton_id":  3},
        {"id":  25, "name": "Damas",                     "canton_id":  3},
        {"id":  26, "name": "Gravilias",                 "canton_id":  3},
        {"id":  27, "name": "Los Guido",                 "canton_id":  3},
        # ── San José → Puriscal (canton_id=4) ────────
        {"id":  28, "name": "Santiago",                  "canton_id":  4},
        {"id":  29, "name": "Mercedes Sur",              "canton_id":  4},
        {"id":  30, "name": "Barbacoas",                 "canton_id":  4},
        {"id":  31, "name": "Grifo Alto",                "canton_id":  4},
        {"id":  32, "name": "San Rafael",                "canton_id":  4},
        {"id":  33, "name": "Candelarita",               "canton_id":  4},
        {"id":  34, "name": "Desamparaditos",            "canton_id":  4},
        {"id":  35, "name": "San Antonio",               "canton_id":  4},
        {"id":  36, "name": "Chires",                    "canton_id":  4},
        # ── San José → Tarrazú (canton_id=5) ─────────
        {"id":  37, "name": "San Marcos",                "canton_id":  5},
        {"id":  38, "name": "San Lorenzo",               "canton_id":  5},
        {"id":  39, "name": "San Carlos",                "canton_id":  5},
        # ── San José → Aserrí (canton_id=6) ──────────
        {"id":  40, "name": "Aserrí",                    "canton_id":  6},
        {"id":  41, "name": "Tarbaca",                   "canton_id":  6},
        {"id":  42, "name": "Vuelta De Jorco",           "canton_id":  6},
        {"id":  43, "name": "San Gabriel",               "canton_id":  6},
        {"id":  44, "name": "Legua",                     "canton_id":  6},
        {"id":  45, "name": "Monterrey",                 "canton_id":  6},
        {"id":  46, "name": "Salitrillos",               "canton_id":  6},
        # ── San José → Mora (canton_id=7) ────────────
        {"id":  47, "name": "Colón",                     "canton_id":  7},
        {"id":  48, "name": "Guayabo",                   "canton_id":  7},
        {"id":  49, "name": "Tabarcia",                  "canton_id":  7},
        {"id":  50, "name": "Piedras Negras",            "canton_id":  7},
        {"id":  51, "name": "Picagres",                  "canton_id":  7},
        {"id":  52, "name": "Jaris",                     "canton_id":  7},
        # ── San José → Goicoechea (canton_id=8) ──────
        {"id":  53, "name": "Guadalupe",                 "canton_id":  8},
        {"id":  54, "name": "San Francisco",             "canton_id":  8},
        {"id":  55, "name": "Calle Blancos",             "canton_id":  8},
        {"id":  56, "name": "Mata De Platano",           "canton_id":  8},
        {"id":  57, "name": "Ipís",                      "canton_id":  8},
        {"id":  58, "name": "Rancho Redondo",            "canton_id":  8},
        {"id":  59, "name": "Purral",                    "canton_id":  8},
        # ── San José → Santa Ana (canton_id=9) ───────
        {"id":  60, "name": "Santa Ana",                 "canton_id":  9},
        {"id":  61, "name": "Salitral",                  "canton_id":  9},
        {"id":  62, "name": "Pozos",                     "canton_id":  9},
        {"id":  63, "name": "Uruca",                     "canton_id":  9},
        {"id":  64, "name": "Piedades",                  "canton_id":  9},
        {"id":  65, "name": "Brasil",                    "canton_id":  9},
        # ── San José → Alajuelita (canton_id=10) ─────
        {"id":  66, "name": "Alajuelita",                "canton_id": 10},
        {"id":  67, "name": "San Josecito",              "canton_id": 10},
        {"id":  68, "name": "San Antonio",               "canton_id": 10},
        {"id":  69, "name": "Concepción",                "canton_id": 10},
        {"id":  70, "name": "San Felipe",                "canton_id": 10},
        # ── San José → Vázquez De Coronado (canton_id=11) ─
        {"id":  71, "name": "San Isidro",                "canton_id": 11},
        {"id":  72, "name": "San Rafael",                "canton_id": 11},
        {"id":  73, "name": "Dulce Nombre De Jesus",     "canton_id": 11},
        {"id":  74, "name": "Patalillo",                 "canton_id": 11},
        {"id":  75, "name": "Cascajal",                  "canton_id": 11},
        # ── San José → Acosta (canton_id=12) ─────────
        {"id":  76, "name": "San Ignacio",               "canton_id": 12},
        {"id":  77, "name": "Guaitil",                   "canton_id": 12},
        {"id":  78, "name": "Palmichal",                 "canton_id": 12},
        {"id":  79, "name": "Cangrejal",                 "canton_id": 12},
        {"id":  80, "name": "Sabanillas",                "canton_id": 12},
        # ── San José → Tibás (canton_id=13) ──────────
        {"id":  81, "name": "San Juan",                  "canton_id": 13},
        {"id":  82, "name": "Cinco Esquinas",            "canton_id": 13},
        {"id":  83, "name": "Anselmo Llorente",          "canton_id": 13},
        {"id":  84, "name": "Leon XII",                  "canton_id": 13},
        {"id":  85, "name": "Colima",                    "canton_id": 13},
        # ── San José → Moravia (canton_id=14) ────────
        {"id":  86, "name": "San Vicente",               "canton_id": 14},
        {"id":  87, "name": "San Jeronimo",              "canton_id": 14},
        {"id":  88, "name": "La Trinidad",               "canton_id": 14},
        # ── San José → Montes De Oca (canton_id=15) ──
        {"id":  89, "name": "San Pedro",                 "canton_id": 15},
        {"id":  90, "name": "Sabanilla",                 "canton_id": 15},
        {"id":  91, "name": "Mercedes",                  "canton_id": 15},
        {"id":  92, "name": "San Rafael",                "canton_id": 15},
        # ── San José → Turrubares (canton_id=16) ─────
        {"id":  93, "name": "San Pablo",                 "canton_id": 16},
        {"id":  94, "name": "San Pedro",                 "canton_id": 16},
        {"id":  95, "name": "San Juan De Mata",          "canton_id": 16},
        {"id":  96, "name": "San Luis",                  "canton_id": 16},
        {"id":  97, "name": "Carara",                    "canton_id": 16},
        # ── San José → Dota (canton_id=17) ───────────
        {"id":  98, "name": "Santa María",               "canton_id": 17},
        {"id":  99, "name": "Jardin",                    "canton_id": 17},
        {"id": 100, "name": "Copey",                     "canton_id": 17},
        # ── San José → Curridabat (canton_id=18) ─────
        {"id": 101, "name": "Curridabat",                "canton_id": 18},
        {"id": 102, "name": "Granadilla",                "canton_id": 18},
        {"id": 103, "name": "Sanchez",                   "canton_id": 18},
        {"id": 104, "name": "Tirrases",                  "canton_id": 18},
        # ── San José → Pérez Zeledón (canton_id=19) ──
        {"id": 105, "name": "San Isidro De El General",  "canton_id": 19},
        {"id": 106, "name": "El General",                "canton_id": 19},
        {"id": 107, "name": "Daniel Flores",             "canton_id": 19},
        {"id": 108, "name": "Rivas",                     "canton_id": 19},
        {"id": 109, "name": "San Pedro",                 "canton_id": 19},
        {"id": 110, "name": "Platanares",                "canton_id": 19},
        {"id": 111, "name": "Pejibaye",                  "canton_id": 19},
        {"id": 112, "name": "Cajon",                     "canton_id": 19},
        {"id": 113, "name": "Baru",                      "canton_id": 19},
        {"id": 114, "name": "Rio Nuevo",                 "canton_id": 19},
        {"id": 115, "name": "Páramo",                    "canton_id": 19},
        # ── San José → León Cortés Castro (canton_id=20) ─
        {"id": 116, "name": "San Pablo",                 "canton_id": 20},
        {"id": 117, "name": "San Andres",                "canton_id": 20},
        {"id": 118, "name": "Llano Bonito",              "canton_id": 20},
        {"id": 119, "name": "San Isidro",                "canton_id": 20},
        {"id": 120, "name": "Santa Cruz",                "canton_id": 20},
        {"id": 121, "name": "San Antonio",               "canton_id": 20},
        # ── Alajuela → Central (canton_id=21) ────────
        {"id": 122, "name": "Alajuela",                  "canton_id": 21},
        {"id": 123, "name": "San José",                  "canton_id": 21},
        {"id": 124, "name": "Carrizal",                  "canton_id": 21},
        {"id": 125, "name": "San Antonio",               "canton_id": 21},
        {"id": 126, "name": "Guácima",                   "canton_id": 21},
        {"id": 127, "name": "San Isidro",                "canton_id": 21},
        {"id": 128, "name": "Sabanilla",                 "canton_id": 21},
        {"id": 129, "name": "San Rafael",                "canton_id": 21},
        {"id": 130, "name": "Rio Segundo",               "canton_id": 21},
        {"id": 131, "name": "Desamparados",              "canton_id": 21},
        {"id": 132, "name": "Turrucares",                "canton_id": 21},
        {"id": 133, "name": "Tambor",                    "canton_id": 21},
        {"id": 134, "name": "Garita",                    "canton_id": 21},
        {"id": 135, "name": "Sarapiquí",                 "canton_id": 21},
        # ── Alajuela → San Ramón (canton_id=22) ──────
        {"id": 136, "name": "San Ramón",                 "canton_id": 22},
        {"id": 137, "name": "Santiago",                  "canton_id": 22},
        {"id": 138, "name": "San Juan",                  "canton_id": 22},
        {"id": 139, "name": "Piedades Norte",            "canton_id": 22},
        {"id": 140, "name": "Piedades Sur",              "canton_id": 22},
        {"id": 141, "name": "San Rafael",                "canton_id": 22},
        {"id": 142, "name": "San Isidro",                "canton_id": 22},
        {"id": 143, "name": "Angeles",                   "canton_id": 22},
        {"id": 144, "name": "Alfaro",                    "canton_id": 22},
        {"id": 145, "name": "Volio",                     "canton_id": 22},
        {"id": 146, "name": "Concepción",                "canton_id": 22},
        {"id": 147, "name": "Zapotal",                   "canton_id": 22},
        {"id": 148, "name": "Peñas Blancas",             "canton_id": 22},
        # ── Alajuela → Grecia (canton_id=23) ─────────
        {"id": 149, "name": "Grecia",                    "canton_id": 23},
        {"id": 150, "name": "San Isidro",                "canton_id": 23},
        {"id": 151, "name": "San José",                  "canton_id": 23},
        {"id": 152, "name": "San Roque",                 "canton_id": 23},
        {"id": 153, "name": "Tacares",                   "canton_id": 23},
        {"id": 154, "name": "Rio Cuarto",                "canton_id": 23},
        {"id": 155, "name": "Puente De Piedra",          "canton_id": 23},
        {"id": 156, "name": "Bolivar",                   "canton_id": 23},
        # ── Alajuela → San Mateo (canton_id=24) ──────
        {"id": 157, "name": "San Mateo",                 "canton_id": 24},
        {"id": 158, "name": "Desmonte",                  "canton_id": 24},
        {"id": 159, "name": "Jesús María",               "canton_id": 24},
        {"id": 160, "name": "Labrador",                  "canton_id": 24},
        # ── Alajuela → Atenas (canton_id=25) ─────────
        {"id": 161, "name": "Atenas",                    "canton_id": 25},
        {"id": 162, "name": "Jesús",                     "canton_id": 25},
        {"id": 163, "name": "Mercedes",                  "canton_id": 25},
        {"id": 164, "name": "San Isidro",                "canton_id": 25},
        {"id": 165, "name": "Concepción",                "canton_id": 25},
        {"id": 166, "name": "San José",                  "canton_id": 25},
        {"id": 167, "name": "Santa Eulalia",             "canton_id": 25},
        {"id": 168, "name": "Escobal",                   "canton_id": 25},
        # ── Alajuela → Naranjo (canton_id=26) ────────
        {"id": 169, "name": "Naranjo",                   "canton_id": 26},
        {"id": 170, "name": "San Miguel",                "canton_id": 26},
        {"id": 171, "name": "San José",                  "canton_id": 26},
        {"id": 172, "name": "Cirrí Sur",                 "canton_id": 26},
        {"id": 173, "name": "San Jerónimo",              "canton_id": 26},
        {"id": 174, "name": "San Juan",                  "canton_id": 26},
        {"id": 175, "name": "El Rosario",                "canton_id": 26},
        {"id": 176, "name": "Palmitos",                  "canton_id": 26},
        # ── Alajuela → Palmares (canton_id=27) ───────
        {"id": 177, "name": "Palmares",                  "canton_id": 27},
        {"id": 178, "name": "Zaragoza",                  "canton_id": 27},
        {"id": 179, "name": "Buenos Aires",              "canton_id": 27},
        {"id": 180, "name": "Santiago",                  "canton_id": 27},
        {"id": 181, "name": "Candelaria",                "canton_id": 27},
        {"id": 182, "name": "Esquipulas",                "canton_id": 27},
        {"id": 183, "name": "La Granja",                 "canton_id": 27},
        # ── Alajuela → Poás (canton_id=28) ───────────
        {"id": 184, "name": "San Pedro",                 "canton_id": 28},
        {"id": 185, "name": "San Juan",                  "canton_id": 28},
        {"id": 186, "name": "San Rafael",                "canton_id": 28},
        {"id": 187, "name": "Carrillos",                 "canton_id": 28},
        {"id": 188, "name": "Sabana Redonda",            "canton_id": 28},
        # ── Alajuela → Orotina (canton_id=29) ────────
        {"id": 189, "name": "Orotina",                   "canton_id": 29},
        {"id": 190, "name": "El Mastate",                "canton_id": 29},
        {"id": 191, "name": "Hacienda Vieja",            "canton_id": 29},
        {"id": 192, "name": "Coyolar",                   "canton_id": 29},
        {"id": 193, "name": "La Ceiba",                  "canton_id": 29},
        # ── Alajuela → San Carlos (canton_id=30) ─────
        {"id": 194, "name": "Quesada",                   "canton_id": 30},
        {"id": 195, "name": "Florencia",                 "canton_id": 30},
        {"id": 196, "name": "Buenavista",                "canton_id": 30},
        {"id": 197, "name": "Aguas Zarcas",              "canton_id": 30},
        {"id": 198, "name": "Venecia",                   "canton_id": 30},
        {"id": 199, "name": "Pital",                     "canton_id": 30},
        {"id": 200, "name": "La Fortuna",                "canton_id": 30},
        {"id": 201, "name": "La Tigra",                  "canton_id": 30},
        {"id": 202, "name": "La Palmera",                "canton_id": 30},
        {"id": 203, "name": "Venado",                    "canton_id": 30},
        {"id": 204, "name": "Cutris",                    "canton_id": 30},
        {"id": 205, "name": "Monterrey",                 "canton_id": 30},
        {"id": 206, "name": "Pocosol",                   "canton_id": 30},
        # ── Alajuela → Zarcero (canton_id=31) ────────
        {"id": 207, "name": "Zarcero",                   "canton_id": 31},
        {"id": 208, "name": "Laguna",                    "canton_id": 31},
        {"id": 209, "name": "Tapesco",                   "canton_id": 31},
        {"id": 210, "name": "Guadalupe",                 "canton_id": 31},
        {"id": 211, "name": "Palmira",                   "canton_id": 31},
        {"id": 212, "name": "Zapote",                    "canton_id": 31},
        {"id": 213, "name": "Brisas",                    "canton_id": 31},
        # ── Alajuela → Sarchí (canton_id=32) ─────────
        {"id": 214, "name": "Sarchí Norte",              "canton_id": 32},
        {"id": 215, "name": "Sarchí Sur",                "canton_id": 32},
        {"id": 216, "name": "Toro Amarillo",             "canton_id": 32},
        {"id": 217, "name": "San Pedro",                 "canton_id": 32},
        {"id": 218, "name": "Rodriguez",                 "canton_id": 32},
        # ── Alajuela → Upala (canton_id=33) ──────────
        {"id": 219, "name": "Upala",                     "canton_id": 33},
        {"id": 220, "name": "Aguas Claras",              "canton_id": 33},
        {"id": 221, "name": "San José o Pizote",         "canton_id": 33},
        {"id": 222, "name": "Bijagua",                   "canton_id": 33},
        {"id": 223, "name": "Delicias",                  "canton_id": 33},
        {"id": 224, "name": "Dos Rios",                  "canton_id": 33},
        {"id": 225, "name": "Yolillal",                  "canton_id": 33},
        {"id": 226, "name": "Canalete",                  "canton_id": 33},
        # ── Alajuela → Los Chiles (canton_id=34) ─────
        {"id": 227, "name": "Los Chiles",                "canton_id": 34},
        {"id": 228, "name": "Caño Negro",                "canton_id": 34},
        {"id": 229, "name": "El Amparo",                 "canton_id": 34},
        {"id": 230, "name": "San Jorge",                 "canton_id": 34},
        # ── Alajuela → Guatuso (canton_id=35) ────────
        {"id": 231, "name": "San Rafael",                "canton_id": 35},
        {"id": 232, "name": "Buenavista",                "canton_id": 35},
        {"id": 233, "name": "Cote",                      "canton_id": 35},
        {"id": 234, "name": "Katira",                    "canton_id": 35},
        # ── Alajuela → Río Cuarto (canton_id=36) ─────
        {"id": 235, "name": "Río Cuarto",                "canton_id": 36},
        # ── Cartago → Central (canton_id=37) ─────────
        {"id": 236, "name": "Oriental",                  "canton_id": 37},
        {"id": 237, "name": "Occidental",                "canton_id": 37},
        {"id": 238, "name": "Carmen",                    "canton_id": 37},
        {"id": 239, "name": "San Nicolás",               "canton_id": 37},
        {"id": 240, "name": "Aguacaliente o San Francisco", "canton_id": 37},
        {"id": 241, "name": "Guadalupe o Arenilla",      "canton_id": 37},
        {"id": 242, "name": "Corralillo",                "canton_id": 37},
        {"id": 243, "name": "Tierra Blanca",             "canton_id": 37},
        {"id": 244, "name": "Dulce Nombre",              "canton_id": 37},
        {"id": 245, "name": "Llano Grande",              "canton_id": 37},
        {"id": 246, "name": "Quebradilla",               "canton_id": 37},
        # ── Cartago → Paraíso (canton_id=38) ─────────
        {"id": 247, "name": "Paraiso",                   "canton_id": 38},
        {"id": 248, "name": "Santiago",                  "canton_id": 38},
        {"id": 249, "name": "Orosi",                     "canton_id": 38},
        {"id": 250, "name": "Cachí",                     "canton_id": 38},
        {"id": 251, "name": "Llanos de Santa Lucía",     "canton_id": 38},
        # ── Cartago → La Unión (canton_id=39) ────────
        {"id": 252, "name": "Tres Rios",                 "canton_id": 39},
        {"id": 253, "name": "San Diego",                 "canton_id": 39},
        {"id": 254, "name": "San Juan",                  "canton_id": 39},
        {"id": 255, "name": "San Rafael",                "canton_id": 39},
        {"id": 256, "name": "Concepción",                "canton_id": 39},
        {"id": 257, "name": "Dulce Nombre",              "canton_id": 39},
        {"id": 258, "name": "San Ramón",                 "canton_id": 39},
        {"id": 259, "name": "Rio Azul",                  "canton_id": 39},
        # ── Cartago → Jiménez (canton_id=40) ─────────
        {"id": 260, "name": "Juan Viñas",                "canton_id": 40},
        {"id": 261, "name": "Tucurrique",                "canton_id": 40},
        {"id": 262, "name": "Pejibaye",                  "canton_id": 40},
        # ── Cartago → Turrialba (canton_id=41) ───────
        {"id": 263, "name": "Turrialba",                 "canton_id": 41},
        {"id": 264, "name": "La Suiza",                  "canton_id": 41},
        {"id": 265, "name": "Peralta",                   "canton_id": 41},
        {"id": 266, "name": "Santa Cruz",                "canton_id": 41},
        {"id": 267, "name": "Santa Teresita",            "canton_id": 41},
        {"id": 268, "name": "Pavones",                   "canton_id": 41},
        {"id": 269, "name": "Tuis",                      "canton_id": 41},
        {"id": 270, "name": "Tayutic",                   "canton_id": 41},
        {"id": 271, "name": "Santa Rosa",                "canton_id": 41},
        {"id": 272, "name": "Tres Equis",                "canton_id": 41},
        {"id": 273, "name": "La Isabel",                 "canton_id": 41},
        {"id": 274, "name": "Chirripó",                  "canton_id": 41},
        # ── Cartago → Alvarado (canton_id=42) ────────
        {"id": 275, "name": "Pacayas",                   "canton_id": 42},
        {"id": 276, "name": "Cervantes",                 "canton_id": 42},
        {"id": 277, "name": "Capellades",                "canton_id": 42},
        # ── Cartago → Oreamuno (canton_id=43) ────────
        {"id": 278, "name": "San Rafael",                "canton_id": 43},
        {"id": 279, "name": "Cot",                       "canton_id": 43},
        {"id": 280, "name": "Potrero Cerrado",           "canton_id": 43},
        {"id": 281, "name": "Cipreses",                  "canton_id": 43},
        {"id": 282, "name": "Santa Rosa",                "canton_id": 43},
        # ── Cartago → El Guarco (canton_id=44) ───────
        {"id": 283, "name": "El Tejar",                  "canton_id": 44},
        {"id": 284, "name": "San Isidro",                "canton_id": 44},
        {"id": 285, "name": "Tobosi",                    "canton_id": 44},
        {"id": 286, "name": "Patio De Agua",             "canton_id": 44},
        # ── Heredia → Central (canton_id=45) ─────────
        {"id": 287, "name": "Heredia",                   "canton_id": 45},
        {"id": 288, "name": "Mercedes",                  "canton_id": 45},
        {"id": 289, "name": "San Francisco",             "canton_id": 45},
        {"id": 290, "name": "Ulloa",                     "canton_id": 45},
        {"id": 291, "name": "Varablanca",                "canton_id": 45},
        # ── Heredia → Barva (canton_id=46) ───────────
        {"id": 292, "name": "Barva",                     "canton_id": 46},
        {"id": 293, "name": "San Pedro",                 "canton_id": 46},
        {"id": 294, "name": "San Pablo",                 "canton_id": 46},
        {"id": 295, "name": "San Roque",                 "canton_id": 46},
        {"id": 296, "name": "Santa Lucía",               "canton_id": 46},
        {"id": 297, "name": "San José de la Montaña",    "canton_id": 46},
        # ── Heredia → Santo Domingo (canton_id=47) ───
        {"id": 298, "name": "Santo Domingo",             "canton_id": 47},
        {"id": 299, "name": "San Vicente",               "canton_id": 47},
        {"id": 300, "name": "San Miguel",                "canton_id": 47},
        {"id": 301, "name": "Paracito",                  "canton_id": 47},
        {"id": 302, "name": "Santo Tomás",               "canton_id": 47},
        {"id": 303, "name": "Santa Rosa",                "canton_id": 47},
        {"id": 304, "name": "Tures",                     "canton_id": 47},
        {"id": 305, "name": "Para",                      "canton_id": 47},
        # ── Heredia → Santa Bárbara (canton_id=48) ───
        {"id": 306, "name": "Santa Bárbara",             "canton_id": 48},
        {"id": 307, "name": "San Pedro",                 "canton_id": 48},
        {"id": 308, "name": "San Juan",                  "canton_id": 48},
        {"id": 309, "name": "Jesús",                     "canton_id": 48},
        {"id": 310, "name": "Santo Domingo",             "canton_id": 48},
        {"id": 311, "name": "Puraba",                    "canton_id": 48},
        # ── Heredia → San Rafael (canton_id=49) ──────
        {"id": 312, "name": "San Rafael",                "canton_id": 49},
        {"id": 313, "name": "San Josecito",              "canton_id": 49},
        {"id": 314, "name": "Santiago",                  "canton_id": 49},
        {"id": 315, "name": "Los Ángeles",               "canton_id": 49},
        {"id": 316, "name": "Concepción",                "canton_id": 49},
        # ── Heredia → San Isidro (canton_id=50) ──────
        {"id": 317, "name": "San Isidro",                "canton_id": 50},
        {"id": 318, "name": "San José",                  "canton_id": 50},
        {"id": 319, "name": "Concepción",                "canton_id": 50},
        {"id": 320, "name": "San Francisco",             "canton_id": 50},
        # ── Heredia → Belén (canton_id=51) ───────────
        {"id": 321, "name": "San Antonio",               "canton_id": 51},
        {"id": 322, "name": "La Ribera",                 "canton_id": 51},
        {"id": 323, "name": "La Asuncion",               "canton_id": 51},
        # ── Heredia → Flores (canton_id=52) ──────────
        {"id": 324, "name": "San Joaquín",               "canton_id": 52},
        {"id": 325, "name": "Barrantes",                 "canton_id": 52},
        {"id": 326, "name": "Llorente",                  "canton_id": 52},
        # ── Heredia → San Pablo (canton_id=53) ───────
        {"id": 327, "name": "San Pablo",                 "canton_id": 53},
        {"id": 328, "name": "Rincon De Sabanilla",       "canton_id": 53},
        # ── Heredia → Sarapiquí (canton_id=54) ───────
        {"id": 329, "name": "Puerto Viejo",              "canton_id": 54},
        {"id": 330, "name": "La Virgen",                 "canton_id": 54},
        {"id": 331, "name": "Las Horquetas",             "canton_id": 54},
        {"id": 332, "name": "Llanuras Del Gaspar",       "canton_id": 54},
        {"id": 333, "name": "Cureña",                    "canton_id": 54},
        # ── Guanacaste → Liberia (canton_id=55) ──────
        {"id": 334, "name": "Liberia",                   "canton_id": 55},
        {"id": 335, "name": "Cañas Dulces",              "canton_id": 55},
        {"id": 336, "name": "Mayorga",                   "canton_id": 55},
        {"id": 337, "name": "Nacascolo",                 "canton_id": 55},
        {"id": 338, "name": "Curubande",                 "canton_id": 55},
        # ── Guanacaste → Nicoya (canton_id=56) ───────
        {"id": 339, "name": "Nicoya",                    "canton_id": 56},
        {"id": 340, "name": "Mansión",                   "canton_id": 56},
        {"id": 341, "name": "San Antonio",               "canton_id": 56},
        {"id": 342, "name": "Quebrada Honda",            "canton_id": 56},
        {"id": 343, "name": "Sámara",                    "canton_id": 56},
        {"id": 344, "name": "Nosara",                    "canton_id": 56},
        {"id": 345, "name": "Belén De Nosarita",         "canton_id": 56},
        # ── Guanacaste → Santa Cruz (canton_id=57) ───
        {"id": 346, "name": "Santa Cruz",                "canton_id": 57},
        {"id": 347, "name": "Bolson",                    "canton_id": 57},
        {"id": 348, "name": "Veintisiete de Abril",      "canton_id": 57},
        {"id": 349, "name": "Tempate",                   "canton_id": 57},
        {"id": 350, "name": "Cartagena",                 "canton_id": 57},
        {"id": 351, "name": "Cuajiniquil",               "canton_id": 57},
        {"id": 352, "name": "Diria",                     "canton_id": 57},
        {"id": 353, "name": "Cabo Velas",                "canton_id": 57},
        {"id": 354, "name": "Tamarindo",                 "canton_id": 57},
        # ── Guanacaste → Bagaces (canton_id=58) ──────
        {"id": 355, "name": "Bagaces",                   "canton_id": 58},
        {"id": 356, "name": "La Fortuna",                "canton_id": 58},
        {"id": 357, "name": "Mogote",                    "canton_id": 58},
        {"id": 358, "name": "Rio Naranjo",               "canton_id": 58},
        # ── Guanacaste → Carrillo (canton_id=59) ─────
        {"id": 359, "name": "Filadelfia",                "canton_id": 59},
        {"id": 360, "name": "Palmira",                   "canton_id": 59},
        {"id": 361, "name": "Sardinal",                  "canton_id": 59},
        {"id": 362, "name": "Belen",                     "canton_id": 59},
        # ── Guanacaste → Cañas (canton_id=60) ────────
        {"id": 363, "name": "Cañas",                     "canton_id": 60},
        {"id": 364, "name": "Palmira",                   "canton_id": 60},
        {"id": 365, "name": "San Miguel",                "canton_id": 60},
        {"id": 366, "name": "Bebedero",                  "canton_id": 60},
        {"id": 367, "name": "Porozal",                   "canton_id": 60},
        # ── Guanacaste → Abangares (canton_id=61) ────
        {"id": 368, "name": "Las Juntas",                "canton_id": 61},
        {"id": 369, "name": "Sierra",                    "canton_id": 61},
        {"id": 370, "name": "San Juan",                  "canton_id": 61},
        {"id": 371, "name": "Colorado",                  "canton_id": 61},
        # ── Guanacaste → Tilarán (canton_id=62) ──────
        {"id": 372, "name": "Tilarán",                   "canton_id": 62},
        {"id": 373, "name": "Quebrada Grande",           "canton_id": 62},
        {"id": 374, "name": "Tronadora",                 "canton_id": 62},
        {"id": 375, "name": "Santa Rosa",                "canton_id": 62},
        {"id": 376, "name": "Líbano",                    "canton_id": 62},
        {"id": 377, "name": "Tierras Morenas",           "canton_id": 62},
        {"id": 378, "name": "Arenal",                    "canton_id": 62},
        # ── Guanacaste → Nandayure (canton_id=63) ────
        {"id": 379, "name": "Carmona",                   "canton_id": 63},
        {"id": 380, "name": "Santa Rita",                "canton_id": 63},
        {"id": 381, "name": "Zapotal",                   "canton_id": 63},
        {"id": 382, "name": "San Pablo",                 "canton_id": 63},
        {"id": 383, "name": "Porvenir",                  "canton_id": 63},
        {"id": 384, "name": "Bejuco",                    "canton_id": 63},
        # ── Guanacaste → La Cruz (canton_id=64) ──────
        {"id": 385, "name": "La Cruz",                   "canton_id": 64},
        {"id": 386, "name": "Santa Cecilia",             "canton_id": 64},
        {"id": 387, "name": "La Garita",                 "canton_id": 64},
        {"id": 388, "name": "Santa Elena",               "canton_id": 64},
        # ── Guanacaste → Hojancha (canton_id=65) ─────
        {"id": 389, "name": "Hojancha",                  "canton_id": 65},
        {"id": 390, "name": "Monte Romo",                "canton_id": 65},
        {"id": 391, "name": "Puerto Carrillo",           "canton_id": 65},
        {"id": 392, "name": "Huacas",                    "canton_id": 65},
        # ── Puntarenas → Central (canton_id=66) ──────
        {"id": 393, "name": "Puntarenas",                "canton_id": 66},
        {"id": 394, "name": "Pitahaya",                  "canton_id": 66},
        {"id": 395, "name": "Chomes",                    "canton_id": 66},
        {"id": 396, "name": "Lepanto",                   "canton_id": 66},
        {"id": 397, "name": "Paquera",                   "canton_id": 66},
        {"id": 398, "name": "Manzanillo",                "canton_id": 66},
        {"id": 399, "name": "Guacimal",                  "canton_id": 66},
        {"id": 400, "name": "Barranca",                  "canton_id": 66},
        {"id": 401, "name": "Monte Verde",               "canton_id": 66},
        {"id": 402, "name": "Isla Del Coco",             "canton_id": 66},
        {"id": 403, "name": "Cóbano",                    "canton_id": 66},
        {"id": 404, "name": "Chacarita",                 "canton_id": 66},
        {"id": 405, "name": "Chira",                     "canton_id": 66},
        {"id": 406, "name": "Acapulco",                  "canton_id": 66},
        {"id": 407, "name": "El Roble",                  "canton_id": 66},
        {"id": 408, "name": "Arancibia",                 "canton_id": 66},
        # ── Puntarenas → Esparza (canton_id=67) ──────
        {"id": 409, "name": "Espíritu Santo",            "canton_id": 67},
        {"id": 410, "name": "San Juan Grande",           "canton_id": 67},
        {"id": 411, "name": "Macacona",                  "canton_id": 67},
        {"id": 412, "name": "San Rafael",                "canton_id": 67},
        {"id": 413, "name": "San Jerónimo",              "canton_id": 67},
        # ── Puntarenas → Buenos Aires (canton_id=68) ─
        {"id": 414, "name": "Buenos Aires",              "canton_id": 68},
        {"id": 415, "name": "Volcán",                    "canton_id": 68},
        {"id": 416, "name": "Potrero Grande",            "canton_id": 68},
        {"id": 417, "name": "Boruca",                    "canton_id": 68},
        {"id": 418, "name": "Pilas",                     "canton_id": 68},
        {"id": 419, "name": "Colinas",                   "canton_id": 68},
        {"id": 420, "name": "Changuena",                 "canton_id": 68},
        {"id": 421, "name": "Biolley",                   "canton_id": 68},
        {"id": 422, "name": "Brunka",                    "canton_id": 68},
        # ── Puntarenas → Montes De Oro (canton_id=69) ─
        {"id": 423, "name": "Miramar",                   "canton_id": 69},
        {"id": 424, "name": "La Unión",                  "canton_id": 69},
        {"id": 425, "name": "San Isidro",                "canton_id": 69},
        # ── Puntarenas → Osa (canton_id=70) ──────────
        {"id": 426, "name": "Puerto Cortés",             "canton_id": 70},
        {"id": 427, "name": "Palmar",                    "canton_id": 70},
        {"id": 428, "name": "Sierpe",                    "canton_id": 70},
        {"id": 429, "name": "Bahía Ballena",             "canton_id": 70},
        {"id": 430, "name": "Piedras Blancas",           "canton_id": 70},
        {"id": 431, "name": "Bahía Drake",               "canton_id": 70},
        # ── Puntarenas → Quepos (canton_id=71) ───────
        {"id": 432, "name": "Quepos",                    "canton_id": 71},
        {"id": 433, "name": "Savegre",                   "canton_id": 71},
        {"id": 434, "name": "Naranjito",                 "canton_id": 71},
        # ── Puntarenas → Golfito (canton_id=72) ──────
        {"id": 435, "name": "Golfito",                   "canton_id": 72},
        {"id": 436, "name": "Puerto Jiménez",            "canton_id": 72},
        {"id": 437, "name": "Guaycara",                  "canton_id": 72},
        {"id": 438, "name": "Pavón",                     "canton_id": 72},
        # ── Puntarenas → Coto Brus (canton_id=73) ────
        {"id": 439, "name": "San Vito",                  "canton_id": 73},
        {"id": 440, "name": "Sabalito",                  "canton_id": 73},
        {"id": 441, "name": "Aguabuena",                 "canton_id": 73},
        {"id": 442, "name": "Limoncito",                 "canton_id": 73},
        {"id": 443, "name": "Pittier",                   "canton_id": 73},
        # ── Puntarenas → Parrita (canton_id=74) ──────
        {"id": 444, "name": "Parrita",                   "canton_id": 74},
        # ── Puntarenas → Corredores (canton_id=75) ───
        {"id": 445, "name": "Corredor",                  "canton_id": 75},
        {"id": 446, "name": "La Cuesta",                 "canton_id": 75},
        {"id": 447, "name": "Canoas",                    "canton_id": 75},
        {"id": 448, "name": "Laurel",                    "canton_id": 75},
        # ── Puntarenas → Garabito (canton_id=76) ─────
        {"id": 449, "name": "Jacó",                      "canton_id": 76},
        {"id": 450, "name": "Tárcoles",                  "canton_id": 76},
        # ── Limón → Central (canton_id=77) ───────────
        {"id": 451, "name": "Limón",                     "canton_id": 77},
        {"id": 452, "name": "Valle La Estrella",         "canton_id": 77},
        {"id": 453, "name": "Rio Blanco",                "canton_id": 77},
        {"id": 454, "name": "Matama",                    "canton_id": 77},
        # ── Limón → Pococí (canton_id=78) ────────────
        {"id": 455, "name": "Guapiles",                  "canton_id": 78},
        {"id": 456, "name": "Jiménez",                   "canton_id": 78},
        {"id": 457, "name": "Rita",                      "canton_id": 78},
        {"id": 458, "name": "Roxana",                    "canton_id": 78},
        {"id": 459, "name": "Cariari",                   "canton_id": 78},
        {"id": 460, "name": "Colorado",                  "canton_id": 78},
        {"id": 461, "name": "La Colonia",                "canton_id": 78},
        # ── Limón → Siquirres (canton_id=79) ─────────
        {"id": 462, "name": "Siquirres",                 "canton_id": 79},
        {"id": 463, "name": "Pacuarito",                 "canton_id": 79},
        {"id": 464, "name": "Florida",                   "canton_id": 79},
        {"id": 465, "name": "Germania",                  "canton_id": 79},
        {"id": 466, "name": "El Cairo",                  "canton_id": 79},
        {"id": 467, "name": "Alegría",                   "canton_id": 79},
        # ── Limón → Talamanca (canton_id=80) ─────────
        {"id": 468, "name": "Bratsi",                    "canton_id": 80},
        {"id": 469, "name": "Sixaola",                   "canton_id": 80},
        {"id": 470, "name": "Cahuita",                   "canton_id": 80},
        {"id": 471, "name": "Telire",                    "canton_id": 80},
        # ── Limón → Matina (canton_id=81) ────────────
        {"id": 472, "name": "Matina",                    "canton_id": 81},
        {"id": 473, "name": "Batán",                     "canton_id": 81},
        {"id": 474, "name": "Carrandi",                  "canton_id": 81},
        # ── Limón → Guácimo (canton_id=82) ───────────
        {"id": 475, "name": "Guácimo",                   "canton_id": 82},
        {"id": 476, "name": "Mercedes",                  "canton_id": 82},
        {"id": 477, "name": "Pocora",                    "canton_id": 82},
        {"id": 478, "name": "Rio Jiménez",               "canton_id": 82},
        {"id": 479, "name": "Duacari",                   "canton_id": 82},
    ])

    # Sincronizar secuencias para que el próximo INSERT auto-incremente correctamente
    op.execute("SELECT setval(pg_get_serial_sequence('provinces', 'id'), MAX(id)) FROM provinces")
    op.execute("SELECT setval(pg_get_serial_sequence('cantons', 'id'), MAX(id)) FROM cantons")
    op.execute("SELECT setval(pg_get_serial_sequence('districts', 'id'), MAX(id)) FROM districts")

    # ── Sectores empresariales ────────────────────────────────────────────────

    op.bulk_insert(sectors_t, [
        {"id":  1, "name": "Banca y Finanzas"},
        {"id":  2, "name": "Educación"},
        {"id":  3, "name": "Salud"},
        {"id":  4, "name": "Tecnología e Innovación"},
        {"id":  5, "name": "Manufactura"},
        {"id":  6, "name": "Comercio y Retail"},
        {"id":  7, "name": "Construcción"},
        {"id":  8, "name": "Telecomunicaciones"},
        {"id":  9, "name": "Gobierno y Sector Público"},
        {"id": 10, "name": "Seguros"},
        {"id": 11, "name": "Energía y Servicios"},
        {"id": 12, "name": "Transporte y Logística"},
        {"id": 13, "name": "Turismo y Hospitalidad"},
        {"id": 14, "name": "Consultoría y Servicios Profesionales"},
    ])
    op.execute("SELECT setval(pg_get_serial_sequence('sectors', 'id'), MAX(id)) FROM sectors")

    # ── Rangos de empleados ───────────────────────────────────────────────────

    op.bulk_insert(employee_ranges_t, [
        {"id": 1, "label": "1-10"},
        {"id": 2, "label": "11-50"},
        {"id": 3, "label": "51-100"},
        {"id": 4, "label": "101-200"},
        {"id": 5, "label": "201-500"},
        {"id": 6, "label": "501-1000"},
        {"id": 7, "label": "1001-5000"},
        {"id": 8, "label": "Más de 5000"},
    ])
    op.execute("SELECT setval(pg_get_serial_sequence('employee_ranges', 'id'), MAX(id)) FROM employee_ranges")


def downgrade() -> None:
    op.execute("DELETE FROM employee_ranges")
    op.execute("DELETE FROM sectors")
    op.execute("DELETE FROM districts")
    op.execute("DELETE FROM cantons")
    op.execute("DELETE FROM provinces")

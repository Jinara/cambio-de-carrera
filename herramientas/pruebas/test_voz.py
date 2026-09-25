"""Pruebas del freno de CV: lo que hace que un CV no suene a nadie.

    python3 -m unittest discover herramientas/pruebas
"""
import sys
import unittest
from pathlib import Path

HERRAMIENTAS = Path(__file__).resolve().parent.parent
RAIZ = HERRAMIENTAS.parent
sys.path.insert(0, str(HERRAMIENTAS))
import chequear  # noqa: E402


def motivos(md):
    return [q for _, _, q in chequear.revisar_cv(md)]


def hay(md, pedazo):
    return any(pedazo in q for q in motivos(md))


CABEZA = "# Ana Pérez\n\n## Experiencia\n\n### Empresa · Puesto\nene-2020 → hoy · Lima\n"


class NombraElPuesto(unittest.TestCase):
    def test_nominalizacion_frena(self):
        for palabra in ["Orientación", "Revisión", "Dictado", "Procesamiento",
                        "Seguimiento", "Asistencia", "Manejo", "Apoyo", "Análisis"]:
            md = CABEZA + f"- {palabra} de cosas en el equipo de 4 personas.\n"
            self.assertTrue(hay(md, "nombra el puesto"), f"no frenó con «{palabra}»")

    def test_verbo_de_decision_pasa(self):
        for palabra in ["Definí", "Diseñé", "Decidí", "Dirigí", "Negocié", "Medí",
                        "Corté", "Reemplacé", "Encontré", "Propuse", "Reduje", "Construí"]:
            md = CABEZA + f"- {palabra} la regla que bajó los quiebres de 9,1% a 6,4%.\n"
            self.assertEqual(motivos(md), [], f"falso positivo con «{palabra}»")

    def test_verbo_flojo_frena(self):
        md = CABEZA + "- Apoyé el piloto de 12 locales.\n"
        self.assertTrue(hay(md, "no dice qué decidiste"))

    def test_negrita_al_principio_no_confunde(self):
        md = CABEZA + "- **Definí** la regla de reposición en 12 locales.\n"
        self.assertEqual(motivos(md), [])

    def test_el_escape_salta_la_linea(self):
        md = CABEZA + "- Certificación ISO 9001 obtenida en 2021. <!-- voz-ok -->\n"
        self.assertEqual(motivos(md), [])


class SoloMiraLaExperiencia(unittest.TestCase):
    def test_publicaciones_no_se_tocan(self):
        md = (CABEZA + "- Definí la regla que se probó en 12 locales.\n"
              "\n## Artículos publicados\n\n"
              "- Ascuña-Durand, K. (2020). «Relative Frequency of Blastocystis».\n"
              "- Stensvold, C. R. (2022). «Further insight into the genetic diversity».\n")
        self.assertEqual(motivos(md), [])

    def test_habilidades_no_se_tocan(self):
        md = (CABEZA + "- Diseñé el tablero que usan 31 personas por semana.\n"
              "\n## Habilidades\n\n- Programación: R · Python · SQL\n")
        self.assertEqual(motivos(md), [])

    def test_lo_de_despues_de_notas_no_cuenta(self):
        md = (CABEZA + "- Definí la regla que se probó en 12 locales.\n"
              "\n<!-- notas -->\n\n## Experiencia\n\n### Otra\n2020\n- Apoyo en cosas.\n")
        self.assertEqual(motivos(md), [])


class BloquesYNumeros(unittest.TestCase):
    def test_bloque_sin_vinetas_frena(self):
        md = (CABEZA + "- Definí la regla que se probó en 12 locales.\n"
              "\n### Instituto · Asistente de investigación\njul-2023 → dic-2023 · Lima\n")
        self.assertTrue(hay(md, "sin ninguna viñeta"))

    def test_ultimo_bloque_sin_vinetas_tambien_frena(self):
        md = CABEZA + "\n### Otro lugar · Puesto\n2019\n"
        self.assertTrue(hay(md, "sin ninguna viñeta"))

    def test_cv_sin_un_solo_numero_frena(self):
        md = CABEZA + "- Definí la regla de reposición para toda la cadena.\n"
        self.assertTrue(hay(md, "ninguna viñeta tiene un número"))

    def test_un_numero_en_alguna_vineta_alcanza(self):
        md = (CABEZA + "- Definí la regla de reposición para toda la cadena.\n"
              "- Dirigí la reunión semanal con los 12 jefes de local.\n")
        self.assertEqual(motivos(md), [])

    def test_cv_vacio_no_explota(self):
        self.assertEqual(motivos("# Ana Pérez\n"), [])


class NoRompeLoDeAntes(unittest.TestCase):
    def test_raya_larga_sigue_frenando(self):
        hallazgos = chequear.buscar("El equipo — que era chico — creció.")
        self.assertTrue(any("raya larga" in q for _, _, q in hallazgos))

    def test_marca_sin_fuente_sigue_frenando(self):
        hallazgos = chequear.buscar("Ahorramos 300 millones [SIN FUENTE].")
        self.assertTrue(any("sin verificar" in q for _, _, q in hallazgos))


class ElEjemploDelRepo(unittest.TestCase):
    """Los CV de Toffy son la referencia de qué está bien. No pueden dar ni un falso positivo."""

    def test_los_cv_del_ejemplo_pasan_limpios(self):
        for ruta in sorted((RAIZ / "ejemplo" / "cv").glob("cv-*.md")) + [RAIZ / "ejemplo" / "04-cv-maestro.md"]:
            with self.subTest(cv=ruta.name):
                self.assertEqual(motivos(ruta.read_text(encoding="utf-8")), [])


if __name__ == "__main__":
    unittest.main()

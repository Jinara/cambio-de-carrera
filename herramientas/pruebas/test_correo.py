"""Pruebas del lector de correo, con un buzón de mentira y un clasificador de mentira. No salen a internet.

    python3 -m unittest discover herramientas/pruebas
"""
import json
import shutil
import sys
import tempfile
import unittest
from datetime import date
from email.message import EmailMessage
from email.utils import format_datetime
from datetime import datetime, timezone
from pathlib import Path

HERRAMIENTAS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERRAMIENTAS))
import correo  # noqa: E402
import vacantes  # noqa: E402

HOY = format_datetime(datetime.now(timezone.utc))


def mensaje(de, asunto, cuerpo, mid):
    m = EmailMessage()
    m["From"], m["Subject"], m["Date"], m["Message-ID"] = de, asunto, HOY, f"<{mid}@example.com>"
    m.set_content(cuerpo)
    return m.as_bytes()


class BuzonFalso:
    """Lo mínimo de imaplib que usa correo.py. Guarda qué se movió y qué se copió."""

    capabilities = ("IMAP4REV1", "MOVE")

    def __init__(self, carpetas):
        self.carpetas = {k: dict(enumerate(v, start=1)) for k, v in carpetas.items()}
        self.actual, self.solo_leer = None, None
        self.movidos, self.copiados, self.creadas = [], [], []

    def select(self, nombre, readonly=False):
        nombre = nombre.strip('"')
        if nombre not in self.carpetas:
            return "NO", [b""]
        self.actual, self.solo_leer = nombre, readonly
        return "OK", [str(len(self.carpetas[nombre])).encode()]

    def create(self, nombre):
        self.creadas.append(nombre.strip('"'))
        return "OK", [b""]

    def uid(self, comando, *args):
        caja = self.carpetas[self.actual]
        if comando == "SEARCH":
            return "OK", [b" ".join(str(u).encode() for u in caja)]
        if comando == "FETCH":
            partes = []
            for u in args[0].split(b","):
                crudo = caja[int(u)]
                if b"HEADER.FIELDS" in args[1].encode():
                    crudo = crudo.split(b"\n\n", 1)[0] + b"\n\n"
                partes.append((f"{int(u)} (UID {int(u)} BODY[] {{{len(crudo)}}}".encode(), crudo))
                partes.append(b")")
            return "OK", partes
        if comando in ("MOVE", "COPY"):
            assert not self.solo_leer, "no se puede mover en modo solo lectura"
            destino = args[1].strip('"')
            (self.movidos if comando == "MOVE" else self.copiados).append((int(args[0]), destino))
            return "OK", [b""]
        raise AssertionError(comando)

    def logout(self):
        pass


def clasificador_falso(prompt):
    """Decide por el asunto, como lo haría Claude, y comprueba que el correo llegue marcado como dato."""
    assert "----- CORREO -----" in prompt and "----- FIN DEL CORREO -----" in prompt
    if "Thank you for applying" in prompt:
        return {"tipo": "acuse", "empresa": "Acme Logística", "puesto": "Product Analyst", "vacante": "acm1",
                "resumen": "Acuse de recibo", "avisos": []}
    if "Update on your application" in prompt:
        return {"tipo": "rechazo", "empresa": "Bodega Uno", "puesto": "Product Owner", "vacante": "",
                "resumen": "No siguen con la postulación", "avisos": []}
    if "Entrevista" in prompt:
        return {"tipo": "entrevista", "empresa": "Canal Dos", "puesto": "Product Analyst", "vacante": "can1",
                "resumen": "Quieren agendar una llamada", "avisos": []}
    if "job alert" in prompt.lower():
        return {"tipo": "alerta", "empresa": "", "puesto": "", "vacante": "", "resumen": "Alerta de LinkedIn",
                "avisos": [{"empresa": "Depósito Tres", "puesto": "Product Analyst", "ubicacion": "Santiago, Chile",
                            "url": "https://www.linkedin.com/jobs/view/4000000001"}]}
    raise AssertionError("se clasificó un correo que no debía salir de la computadora:\n" + prompt[-400:])


class Correo(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        d = {"vacantes": [], "historial": []}
        vacantes.alta(d, {"empresa": "Acme Logística", "puesto": "Product Analyst", "estado": "revisar"})
        vacantes.alta(d, {"empresa": "Bodega Uno", "puesto": "Product Owner", "estado": "postulada",
                          "enviado": "2026-09-01", "notas": "Veredicto: conviene"})
        vacantes.alta(d, {"empresa": "Canal Dos", "puesto": "Product Analyst", "estado": "postulada",
                          "enviado": "2026-09-02"})
        vacantes.guardar(self.dir, d)
        self.config = dict(correo.VACIA, cuenta="toffy@example.com")
        self.buzon = BuzonFalso({"INBOX": [
            mensaje("Acme <no-reply@greenhouse.io>", "Thank you for applying to Acme", "Hola Toffy.", "a1"),
            mensaje("Mamá <mama@example.com>", "¿Vienes el domingo?", "Trae pan. Y mira la entrevista de la tele.", "p1"),
            mensaje("Bodega Uno <talent@bodegauno.example.com>", "Update on your application", "We will not move forward.", "r1"),
            mensaje("Ana de Canal Dos <ana@canaldos.example.com>", "Entrevista Product Analyst", "¿Te sirve el martes?", "e1"),
            mensaje("LinkedIn <jobalerts-noreply@linkedin.com>", "New job alert: Product Analyst", "Depósito Tres...", "l1"),
        ]})
        self.avisos = []

    def tearDown(self):
        shutil.rmtree(self.dir)

    def correr(self, **kw):
        return correo.procesar(self.dir, self.config, correo.RegistroArchivo(self.dir), clasificar=clasificador_falso,
                               conexion=self.buzon, notificar=self.avisos.append, **kw)

    def test_actualiza_el_registro_ordena_la_bandeja_y_avisa_solo_lo_importante(self):
        texto = self.correr()
        d = vacantes.cargar(self.dir)
        por_empresa = {v["empresa"]: v for v in d["vacantes"]}
        self.assertEqual(por_empresa["Acme Logística"]["estado"], "postulada")
        self.assertEqual(por_empresa["Acme Logística"]["enviado"], date.today().isoformat())
        self.assertEqual(por_empresa["Bodega Uno"]["estado"], "rechazada")
        self.assertIn("Veredicto: conviene", por_empresa["Bodega Uno"]["notas"])   # la nota vieja no se pisa
        self.assertEqual(por_empresa["Canal Dos"]["estado"], "respondieron")
        hall = json.loads((self.dir / "barrido" / "hallazgos.json").read_text())
        self.assertEqual([h["empresa"] for h in hall["hallazgos"]], ["Depósito Tres"])

        self.assertEqual(sorted(self.buzon.movidos), [
            (1, "Busqueda laboral/Acuses"), (3, "Busqueda laboral/Rechazos"), (5, "Busqueda laboral/Alertas")])
        self.assertEqual(self.buzon.copiados, [(4, "Busqueda laboral/Responder")])   # queda en la bandeja
        self.assertEqual(len(self.avisos), 1)
        self.assertIn("Canal Dos", self.avisos[0])
        self.assertIn("Para responder", texto)

    def test_no_repite_y_la_prueba_no_toca_nada(self):
        antes = (self.dir / "vacantes.json").read_bytes()
        texto = self.correr(prueba=True)
        self.assertIn("PRUEBA", texto)
        self.assertEqual((self.dir / "vacantes.json").read_bytes(), antes)
        self.assertEqual((self.buzon.movidos, self.buzon.copiados, self.avisos), ([], [], []))

        self.correr()
        historial = len(vacantes.cargar(self.dir)["historial"])
        self.buzon.movidos, self.buzon.copiados = [], []
        self.correr()
        self.assertEqual(len(vacantes.cargar(self.dir)["historial"]), historial)
        self.assertEqual((self.buzon.movidos, self.buzon.copiados), ([], []))

    def test_si_el_clasificador_falla_se_reintenta_la_proxima(self):
        def falla(prompt):
            raise correo.Error("sin conexión")
        texto = correo.procesar(self.dir, self.config, correo.RegistroArchivo(self.dir), clasificar=falla,
                                conexion=self.buzon, notificar=self.avisos.append)
        self.assertIn("se reintentan", texto)
        self.assertEqual(correo.cargar_procesados(self.dir)["ids"], [])

    def test_un_correo_de_una_empresa_que_no_estaba_entra_al_registro(self):
        registro = correo.RegistroArchivo(self.dir)
        efecto = correo.aplicar(registro, {"tipo": "entrevista", "empresa": "Empresa Nueva", "puesto": "PO",
                                           "vacante": "", "resumen": "Llamada", "avisos": []}, "2026-09-17")
        self.assertIn("no estaba en el registro", efecto)
        nueva = registro.vacantes()[-1]
        self.assertEqual((nueva["empresa"], nueva["estado"], nueva.get("enviado")), ("Empresa Nueva", "respondieron", None))

    def test_un_acuse_tardio_no_baja_el_estado(self):
        registro = correo.RegistroArchivo(self.dir)
        registro.cambiar("can1", {"estado": "entrevistando"})
        correo.aplicar(registro, {"tipo": "acuse", "empresa": "Canal Dos", "puesto": "Product Analyst",
                                  "vacante": "can1", "resumen": "Acuse", "avisos": []}, "2026-09-17")
        self.assertEqual(next(v for v in registro.vacantes() if v["id"] == "can1")["estado"], "entrevistando")

    def test_las_alertas_pasan_por_los_filtros_del_barrido(self):
        (self.dir / "barrido.json").write_text(json.dumps({
            "titulos": {"A": ["product analyst"]}, "ubicacion_si": ["chile"], "ubicacion_no": [], "ubicacion_salva": []}))
        registro = correo.RegistroArchivo(self.dir)
        n = registro.hallazgos([
            {"empresa": "Depósito Tres", "puesto": "Product Analyst", "ubicacion": "Santiago, Chile", "url": "https://x.example.com/1"},
            {"empresa": "Otra", "puesto": "Product Analyst", "ubicacion": "New York", "url": "https://x.example.com/2"},
            {"empresa": "Otra", "puesto": "Chef Ejecutivo", "ubicacion": "Santiago, Chile", "url": "https://x.example.com/3"},
        ], "2026-09-17T09:00")
        self.assertEqual(n, 1)

    def test_nombres_de_carpeta_con_tildes(self):
        self.assertEqual(correo.imap_utf7("Trabajos/Búsqueda 2026"), "Trabajos/B&APo-squeda 2026")
        self.assertEqual(correo.imap_utf7("R&D"), "R&-D")


if __name__ == "__main__":
    unittest.main()

"""Pruebas del registro, el barrido y el tablero. No salen a internet.

    python3 -m unittest discover herramientas/pruebas
"""
import http.client
import json
import shutil
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path

HERRAMIENTAS = Path(__file__).resolve().parent.parent
RAIZ = HERRAMIENTAS.parent
sys.path.insert(0, str(HERRAMIENTAS))
import barrido  # noqa: E402
import tablero  # noqa: E402
import vacantes  # noqa: E402

CONFIG = {
    "empresas": [
        {"nombre": "Acme Logística", "board": "greenhouse", "slug": "acme"},
        {"nombre": "Bodega Uno", "board": "lever", "slug": "bodegauno"},
        {"nombre": "Canal Dos", "board": "ashby", "slug": "canaldos"},
        {"nombre": "Depósito Tres", "board": "recruitee", "slug": "deposito"},
    ],
    "titulos": {"A": ["product analyst", "product owner"], "B": ["e-commerce"]},
    "titulos_no": ["senior", "intern"],
    "ubicacion_si": ["chile", "latam", "remote"],
    "ubicacion_no": ["united states", "us", "europe"],
    "ubicacion_salva": ["chile", "latam"],
}

RESPUESTAS = {
    "https://boards-api.greenhouse.io/v1/boards/acme/jobs": {"jobs": [
        {"id": 4001001, "title": "Product Analyst", "location": {"name": "Santiago, Chile"},
         "absolute_url": "https://boards.example.com/acme/jobs/4001001"},
        {"id": 4001002, "title": "Product Analyst", "location": {"name": "Remote, US"},
         "absolute_url": "https://boards.example.com/acme/jobs/4001002"},
        {"id": 4001003, "title": "Senior Product Owner", "location": {"name": "Chile"},
         "absolute_url": "https://boards.example.com/acme/jobs/4001003"},
        {"id": 4001004, "title": "Marketing Analyst", "location": {"name": "Chile"},
         "absolute_url": "https://boards.example.com/acme/jobs/4001004"},
    ]},
    "https://api.lever.co/v0/postings/bodegauno": [
        {"id": "a1b2c3d4-0000", "text": "Product Owner E-commerce", "categories": {"location": "United States, LATAM"},
         "hostedUrl": "https://jobs.example.com/bodegauno/a1b2c3d4-0000"},
    ],
    "https://api.ashbyhq.com/posting-api/job-board/canaldos": {"jobs": [
        {"id": "f00d", "title": "Product Analyst", "location": "New York", "secondaryLocations": [{"location": "Remote (LATAM)"}],
         "jobUrl": "https://jobs.example.com/canaldos/f00d", "isListed": True},
        {"id": "beef", "title": "Product Analyst", "location": "Chile", "jobUrl": "https://jobs.example.com/canaldos/beef",
         "isListed": False},
    ]},
    "https://deposito.recruitee.com/api/offers/": {"offers": [
        {"slug": "product-analyst-chile", "title": "Product Analyst Chile", "location": "Remote job", "country": "Chile",
         "careers_url": "https://deposito.example.com/o/product-analyst-chile"},
        {"slug": "product-analyst-peru", "title": "Product Analyst Perú", "location": "Remote job", "country": "Chile, Perú",
         "careers_url": "https://deposito.example.com/o/product-analyst-peru"},
    ]},
}


def traer_falso(url, timeout=20):
    if url not in RESPUESTAS:
        raise OSError("sin red")
    return json.loads(json.dumps(RESPUESTAS[url]))


def vacio():
    return {"vacantes": [], "historial": []}


class Registro(unittest.TestCase):
    def test_el_historial_guarda_solo_lo_que_cambio(self):
        d = vacio()
        v = vacantes.alta(d, {"empresa": "Acme", "puesto": "Product Analyst"}, "2026-09-01")
        _, reales = vacantes.cambiar(d, v["id"], {"estado": "postulada", "notas": ""}, "2026-09-03")
        self.assertEqual(reales, {"estado": "postulada", "enviado": "2026-09-03"})
        self.assertEqual([h["campo"] for h in d["historial"]], ["alta", "estado", "enviado"])
        _, reales = vacantes.cambiar(d, v["id"], {"estado": "postulada"}, "2026-09-04")
        self.assertEqual(reales, {})

    def test_frena_datos_mal_escritos(self):
        d = vacio()
        with self.assertRaises(vacantes.Error):
            vacantes.alta(d, {"empresa": "Acme", "puesto": "PA", "estado": "enviada"})
        with self.assertRaises(vacantes.Error):
            vacantes.alta(d, {"empresa": "Acme", "puesto": "PA", "enviado": "3/9/2026"})
        with self.assertRaises(vacantes.Error):
            vacantes.alta(d, {"empresa": "Acme"})

    def test_seguimiento_resumen_y_semanas(self):
        d = vacio()
        a = vacantes.alta(d, {"empresa": "Acme", "puesto": "PA", "estado": "postulada", "enviado": "2026-08-20", "carril": "A"})
        b = vacantes.alta(d, {"empresa": "Bodega", "puesto": "PO", "estado": "postulada", "enviado": "2026-09-14", "carril": "A"})
        vacantes.cambiar(d, b["id"], {"estado": "rechazada"}, "2026-09-15")
        self.assertEqual([v["id"] for v in vacantes.seguimiento(d, 14, "2026-09-17")], [a["id"]])
        r = vacantes.resumen(d)
        self.assertEqual((r["enviadas"], r["respondieron"]), (2, 1))
        self.assertEqual(r["por_carril"]["A"], {"enviadas": 2, "respondieron": 1})
        s = vacantes.semanas(d, 8, "2026-09-17")
        self.assertEqual(s[-1], {"desde": "2026-09-14", "enviadas": 1})
        self.assertEqual(sum(x["enviadas"] for x in s), 2)


class Filtros(unittest.TestCase):
    def test_palabras_enteras_y_sin_tildes(self):
        self.assertEqual(barrido.contiene("Marketing Manager", ["ar"]), [])
        self.assertEqual(barrido.contiene("Remote job AR", ["ar"]), ["ar"])
        self.assertEqual(barrido.contiene("Analista de Producto, Perú", ["peru"]), ["peru"])

    def test_ubicacion(self):
        self.assertTrue(barrido.ubicacion_sirve("United States, LATAM", CONFIG))
        self.assertFalse(barrido.ubicacion_sirve("Remote, US", CONFIG))
        self.assertFalse(barrido.ubicacion_sirve("", CONFIG))
        self.assertTrue(barrido.ubicacion_sirve("", dict(CONFIG, ubicacion_si=[])))

    def test_carriles(self):
        self.assertEqual(barrido.carriles_del_titulo("Product Owner E-commerce", CONFIG), ["A", "B"])
        self.assertEqual(barrido.carriles_del_titulo("Senior Product Owner", CONFIG), [])

    def test_board_de_url(self):
        self.assertEqual(barrido.board_de_url("https://job-boards.greenhouse.io/acme/jobs/123"), ("greenhouse", "acme"))
        self.assertEqual(barrido.board_de_url("jobs.lever.co/bodegauno"), ("lever", "bodegauno"))
        self.assertEqual(barrido.board_de_url("https://jobs.ashbyhq.com/canaldos"), ("ashby", "canaldos"))
        self.assertEqual(barrido.board_de_url("https://deposito.recruitee.com/o/algo"), ("recruitee", "deposito"))
        self.assertIsNone(barrido.board_de_url("https://www.example.com/empleos"))


class Barrido(unittest.TestCase):
    def test_encuentra_lo_que_encaja_una_sola_vez(self):
        registro, hallazgos = vacio(), {"hallazgos": [], "corridas": []}
        nuevos, fallos, miradas = barrido.barrer(CONFIG, registro, hallazgos, traer=traer_falso, ahora="2026-09-17T08:00")
        self.assertEqual((fallos, miradas), ([], 4))
        vistos = sorted((h["empresa"], h["puesto"]) for h in nuevos)
        self.assertEqual(vistos, [
            ("Acme Logística", "Product Analyst"),
            ("Bodega Uno", "Product Owner E-commerce"),
            ("Canal Dos", "Product Analyst"),
            ("Depósito Tres", "Product Analyst Chile"),  # la versión de Perú es el mismo puesto
        ])
        otra_vez, _, _ = barrido.barrer(CONFIG, registro, hallazgos, traer=traer_falso)
        self.assertEqual(otra_vez, [])

    def test_no_avisa_lo_que_ya_esta_en_el_registro(self):
        registro = vacio()
        vacantes.alta(registro, {"empresa": "Acme Logística", "puesto": "Otro nombre",
                                 "url": "https://boards.example.com/acme/jobs/4001001?src=li"})
        vacantes.alta(registro, {"empresa": "Canal Dos", "puesto": "Product Analyst - Remote"})
        nuevos, _, _ = barrido.barrer(CONFIG, registro, {"hallazgos": [], "corridas": []}, traer=traer_falso)
        self.assertEqual(sorted(h["empresa"] for h in nuevos), ["Bodega Uno", "Depósito Tres"])

    def test_un_board_caido_no_frena_a_los_demas_y_todos_caidos_es_ciego(self):
        config = dict(CONFIG, empresas=CONFIG["empresas"] + [{"nombre": "Sin Red", "board": "lever", "slug": "sinred"}])
        _, fallos, miradas = barrido.barrer(config, vacio(), {"hallazgos": [], "corridas": []}, traer=traer_falso)
        self.assertEqual((len(fallos), miradas), (1, 4))

        def caido(url, timeout=20):
            raise OSError("sin red")
        nuevos, fallos, miradas = barrido.barrer(CONFIG, vacio(), {"hallazgos": [], "corridas": []}, traer=caido)
        self.assertEqual((nuevos, len(fallos), miradas), ([], 4, 0))
        self.assertIn("No se pudo mirar nada", barrido.reporte([], fallos, 0, 4, "2026-09-17T08:00"))

    def test_pasar_e_ignorar(self):
        registro, hallazgos = vacio(), {"hallazgos": [], "corridas": []}
        nuevos, _, _ = barrido.barrer(CONFIG, registro, hallazgos, traer=traer_falso, ahora="2026-09-17T08:00")
        barrido.decidir(registro, hallazgos, nuevos[0]["id"], "pasar", {}, "2026-09-17")
        barrido.decidir(registro, hallazgos, nuevos[1]["id"], "ignorar")
        self.assertEqual(registro["vacantes"][0]["estado"], "revisar")
        self.assertEqual(registro["vacantes"][0]["url"], nuevos[0]["url"])
        with self.assertRaises(vacantes.Error):
            barrido.decidir(registro, hallazgos, nuevos[0]["id"], "pasar")


class Ejemplo(unittest.TestCase):
    def test_el_ejemplo_es_coherente(self):
        e = RAIZ / "ejemplo"
        registro, hallazgos = vacantes.cargar(e), barrido.cargar_hallazgos(e)
        config, _ = barrido.cargar_config(e)
        ids = {v["id"] for v in registro["vacantes"]}
        for v in registro["vacantes"]:
            vacantes.validar({k: v[k] for k in vacantes.CAMPOS if k in v})
        for h in hallazgos["hallazgos"]:
            self.assertTrue(barrido.carriles_del_titulo(h["puesto"], config), h["puesto"])
            self.assertTrue(barrido.ubicacion_sirve(h["ubicacion"], config), h["ubicacion"])
            if h["estado"] == "pasado":
                self.assertIn(h["vacante"], ids)
        for v in registro["vacantes"]:
            self.assertIn("example.com", v.get("url", "example.com"))


class Tablero(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        shutil.copy(RAIZ / "ejemplo" / "vacantes.json", self.dir / "vacantes.json")
        (self.dir / "barrido").mkdir()
        shutil.copy(RAIZ / "ejemplo" / "barrido" / "hallazgos.json", self.dir / "barrido" / "hallazgos.json")
        shutil.copy(RAIZ / "ejemplo" / "barrido.json", self.dir / "barrido.json")
        self.token = "clave-de-prueba"
        self.levantar(demo=False)

    def levantar(self, demo):
        if getattr(self, "servidor", None):
            self.bajar()
        self.servidor = ThreadingHTTPServer(("127.0.0.1", 0), tablero.BaseHTTPRequestHandler)
        self.puerto = self.servidor.server_address[1]
        self.servidor.RequestHandlerClass = tablero.hacer_handler(
            tablero.Tablero(self.dir, demo=demo), self.token, self.puerto)
        threading.Thread(target=self.servidor.serve_forever, daemon=True).start()

    def bajar(self):
        self.servidor.shutdown()
        self.servidor.server_close()
        self.servidor = None

    def tearDown(self):
        self.bajar()
        shutil.rmtree(self.dir)

    def pedir(self, metodo, ruta, cuerpo=None, **headers):
        h = {"Host": f"127.0.0.1:{self.puerto}", "X-Tablero": self.token}
        if cuerpo is not None:
            h["Content-Type"] = "application/json"
        h.update({k.replace("_", "-"): v for k, v in headers.items()})
        c = http.client.HTTPConnection("127.0.0.1", self.puerto, timeout=10)
        c.request(metodo, ruta, body=json.dumps(cuerpo) if cuerpo is not None else None, headers=h)
        r = c.getresponse()
        datos = r.read()
        c.close()
        return r.status, (json.loads(datos) if r.getheader("Content-Type", "").startswith("application/json") else datos), r

    def test_la_pagina_no_trae_datos_y_la_api_pide_la_clave(self):
        status, pagina, r = self.pedir("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn("default-src 'none'", r.getheader("Content-Security-Policy"))
        self.assertNotIn(b"Tiendas Lumbrera", pagina)
        self.assertEqual(self.pedir("GET", "/api/datos", X_Tablero="otra")[0], 403)
        status, datos, _ = self.pedir("GET", "/api/datos")
        self.assertEqual((status, datos["modo"], datos["hoy"]), (200, "real", "2026-09-17"))

    def test_rechaza_otro_host_otro_origen_y_otro_tipo(self):
        self.assertEqual(self.pedir("GET", "/", Host="evil.example.com")[0], 403)
        self.assertEqual(self.pedir("POST", "/api/alta", {"campos": {"empresa": "X", "puesto": "Y"}},
                                    Origin="http://evil.example.com")[0], 403)
        self.assertEqual(self.pedir("POST", "/api/alta", {"campos": {}}, Content_Type="text/plain")[0], 415)

    def test_los_cambios_llegan_al_archivo(self):
        status, datos, _ = self.pedir("POST", "/api/cambiar", {"id": "kil1", "cambios": {"estado": "respondieron"}})
        self.assertEqual(status, 200)
        guardado = json.loads((self.dir / "vacantes.json").read_text())
        self.assertEqual(next(v for v in guardado["vacantes"] if v["id"] == "kil1")["estado"], "respondieron")
        status, datos, _ = self.pedir("POST", "/api/cambiar", {"id": "kil1", "cambios": {"estado": "ganada"}})
        self.assertEqual(status, 400)
        status, datos, _ = self.pedir("POST", "/api/hallazgo", {"id": "h4", "accion": "pasar"})
        self.assertEqual(status, 200)
        self.assertEqual(datos["mensaje"], "Kilómetro Cero: quedó para revisar")
        self.assertNotIn("h4", [h["id"] for h in datos["hallazgos"]])

    def test_arranca_sin_datos(self):
        vacio_dir = Path(tempfile.mkdtemp())
        try:
            d = tablero.Tablero(vacio_dir).datos()
            self.assertEqual((d["vacantes"], d["hallazgos"], d["ultima_corrida"]), ([], [], None))
            barrido.cmd_barrer(vacio_dir, avisar=False)
            self.assertFalse((vacio_dir / "barrido").exists())
        finally:
            shutil.rmtree(vacio_dir)

    def test_en_modo_demo_no_se_escribe_nada(self):
        antes = (self.dir / "vacantes.json").read_bytes()
        self.levantar(demo=True)
        status, datos, _ = self.pedir("POST", "/api/alta", {"campos": {"empresa": "Nueva", "puesto": "PA"}})
        self.assertEqual((status, datos["modo"]), (200, "demo"))
        self.assertIn("Nueva", [v["empresa"] for v in datos["vacantes"]])
        self.assertEqual((self.dir / "vacantes.json").read_bytes(), antes)


if __name__ == "__main__":
    unittest.main()

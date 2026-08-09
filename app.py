import os
import re
import hmac
from flask import Flask, request, jsonify, session, render_template

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "MAY_ROGA_LLC_BOLSILLOLATINO_SECURE_TOKEN_2026")

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID1 = os.environ.get("STRIPE_PRICE_ID1")
STRIPE_PRICE_ID2 = os.environ.get("STRIPE_PRICE_ID2")
STRIPE_PRICE_ID3 = os.environ.get("STRIPE_PRICE_ID3")
DEV_USER = os.environ.get("DEV_USER", "admin")
DEV_PASS = os.environ.get("DEV_PASS", "root")

def limpiar_texto_para_voz(texto):
    return re.sub(r'[\*\#\-]', '', texto).strip()

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ready"}), 200

@app.route('/')
@app.route('/app')
def index():
    return render_template('app.html')

@app.route('/login_dev', methods=['POST'])
def login_dev():
    datos = request.json or {}
    usuario = datos.get("username")
    clave = datos.get("password")
    if usuario and clave and hmac.compare_digest(usuario, DEV_USER) and hmac.compare_digest(clave, DEV_PASS):
        session["autenticado"] = True
        session["tipo_pago"] = "negocio"
        return jsonify({"status": "success", "redirect": "/app"}), 200
    return jsonify({"status": "error", "message": "Acceso denegado."}), 401

# =========================================================================
# MATRIZ PANAMERICANA UNIVERSAL: LOS 20 PAÍSES DE LATINOAMÉRICA
# Papelería oficial, formularios migratorios, permisos y trámites cotidianos
# =========================================================================
MATRIZ_20_PAISES = {
    # 1. MÉXICO
    "mx_integral": {
        "id": "mx_integral",
        "categoria": "1. México",
        "titulo": "México: Papelería Completa (I-130, I-601A, Visas y Matrícula Consular)",
        "descripcion": "Trámites migratorios USCIS, perdón provisional y documentación consular mexicana.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "numero_identificacion", "label": "Número de Matrícula Consular o Pasaporte Mexicano", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su solicitud específica en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "MEXICAN CITIZEN / RESIDENT DOCUMENTATION APPLICATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "Consular ID / Passport: {numero_identificacion}\n"
            "Specific Request / Petition Details: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information provided is accurate.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "USCIS Lockbox / Consulado de México en EE. UU."
    },

    # 2. CUBA
    "cu_integral": {
        "id": "cu_integral",
        "categoria": "2. Cuba",
        "titulo": "Cuba: Papelería Completa (Ley de Ajuste I-485, Parole, Prórrogas y Poderes)",
        "descripcion": "Residencia permanente, ajuste cubano y gestión de documentos consulares de la isla.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre y Apellidos del Solicitante", "tipo": "text"},
            {"campo": "a_number", "label": "Número de Alien (A-Number) o Pasaporte Cubano", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa el trámite de ajuste o consular en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "CUBAN ADJUSTMENT ACT / CONSULAR DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "Alien Registration Number / Cuban Passport: {a_number}\n"
            "Case Statement: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information is true and correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "USCIS Chicago Lockbox / Consulado de Cuba."
    },

    # 3. VENEZUELA
    "ve_integral": {
        "id": "ve_integral",
        "categoria": "3. Venezuela",
        "titulo": "Venezuela: Papelería Completa (TPS I-821, Permiso de Trabajo I-765, Asilo)",
        "descripcion": "Protección temporal, permisos laborales y trámites de supervivencia para venezolanos.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "a_number", "label": "Número de Alien (A-Number)", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su solicitud de TPS o Asilo en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "VENEZUELAN TPS / ASYLUM / WORK PERMIT APPLICATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "Alien Registration Number (A-Number): {a_number}\n"
            "Application Statement: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information is correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "USCIS Chicago Lockbox."
    },

    # 4. COLOMBIA
    "co_integral": {
        "id": "co_integral",
        "categoria": "4. Colombia",
        "titulo": "Colombia: Papelería Completa (Visas B1/B2 DS-160, Peticiones y Actas)",
        "descripcion": "Visados consulares de turismo, peticiones familiares y trámites notariales colombianos.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "numero_pasaporte", "label": "Número de Pasaporte Colombiano", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su trámite de visa o consular en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "COLOMBIAN CITIZEN CONSULAR & VISA DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "Colombian Passport: {numero_pasaporte}\n"
            "Petition Details: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information provided is correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "Embajada de EE. UU. en Bogotá / Consulado de Colombia."
    },

    # 5. EL SALVADOR
    "sv_integral": {
        "id": "sv_integral",
        "categoria": "5. El Salvador",
        "titulo": "El Salvador: Papelería Completa (Renovación TPS, DUI y Trámites Consulares)",
        "descripcion": "Protección temporal, emisión de Documento Único de Identidad y asistencia legal.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "numero_dui", "label": "Número de DUI o Pasaporte Salvadoreño", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su trámite de TPS o consular en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "SALVADORAN TPS & CONSULAR DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "DUI / Passport Number: {numero_dui}\n"
            "Case Statement: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information is true and correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "USCIS Lockbox / Consulado de El Salvador."
    },

    # 6. GUATEMALA
    "gt_integral": {
        "id": "gt_integral",
        "categoria": "6. Guatemala",
        "titulo": "Guatemala: Papelería Completa (Visas H-2A/H-2B, Pasaportes y Matrícula Consular)",
        "descripcion": "Visas de trabajo agrícola, emisión de pasaportes y asistencia legal consular.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "numero_cui", "label": "Número de CUI / DPI o Pasaporte", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su trámite de trabajo o consular en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "GUATEMALAN WORK VISA & CONSULAR DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "CUI / Passport Number: {numero_cui}\n"
            "Petition Details: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information provided is correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "Embajada de EE. UU. en Guatemala / Consulado."
    },

    # 7. HONDURAS
    "hn_integral": {
        "id": "hn_integral",
        "categoria": "7. Honduras",
        "titulo": "Honduras: Papelería Completa (TPS, Tarjeta de Identidad y Poderes)",
        "descripcion": "Amparo temporal, emisión de documentos de identidad y gestiones consulares.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "numero_identidad", "label": "Número de Identidad o Pasaporte Hondureño", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su solicitud de TPS o consular en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "HONDURAN TPS & CONSULAR DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "National ID / Passport: {numero_identidad}\n"
            "Case Statement: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information is true and correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "USCIS Lockbox / Consulado de Honduras."
    },

    # 8. REPÚBLICA DOMINICANA
    "do_integral": {
        "id": "do_integral",
        "categoria": "8. República Dominicana",
        "titulo": "República Dominicana: Papelería Completa (Procesamiento Consular, Visas y Actas)",
        "descripcion": "Entrevistas de residencia en Santo Domingo, visados y legalización de documentos.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "numero_cedula", "label": "Cédula Dominicana o Pasaporte", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su trámite consular o de residencia en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "DOMINICAN REPUBLIC CONSULAR & RESIDENCY DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "Cedula / Passport: {numero_cedula}\n"
            "Petition Details: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information provided is correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "Embajada de EE. UU. en Santo Domingo."
    },

    # 9. ECUADOR
    "ec_integral": {
        "id": "ec_integral",
        "categoria": "9. Ecuador",
        "titulo": "Ecuador: Papelería Completa (Pasaportes Biométricos, Poderes y Visados)",
        "descripcion": "Emisión de documentos consulares, actas notariales y visados temporales.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "numero_cedula", "label": "Cédula de Identidad Ecuatoriana o Pasaporte", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su trámite consular o notarial en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "ECUADORIAN CONSULAR & NOTARIAL DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "Cedula / Passport: {numero_cedula}\n"
            "Case Statement: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information is true and correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "Consulado de Ecuador en EE. UU."
    },

    # 10. PERÚ
    "pe_integral": {
        "id": "pe_integral",
        "categoria": "10. Perú",
        "titulo": "Perú: Papelería Completa (Pasaportes, Actas RENIEC y Visas)",
        "descripcion": "Gestión documental para peruanos en el exterior, registros civiles y visados.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "numero_dni", "label": "Número de DNI o Pasaporte Peruano", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su solicitud consular o de visa en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "PERUVIAN CONSULAR & RENIEC DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "DNI / Passport: {numero_dni}\n"
            "Petition Details: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information provided is correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "Consulado General del Perú en EE. UU."
    },

    # 11. ARGENTINA
    "ar_integral": {
        "id": "ar_integral",
        "categoria": "11. Argentina",
        "titulo": "Argentina: Papelería Completa (Visas B1/B2, DNI y Certificados Consulares)",
        "descripcion": "Visados de no inmigrante y documentación consular para ciudadanos argentinos.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "numero_pasaporte", "label": "Número de Pasaporte Argentino", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su solicitud de visa o consular en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "ARGENTINE CONSULAR & VISA DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "Passport Number: {numero_pasaporte}\n"
            "Case Statement: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information is true and correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "Embajada de EE. UU. en Buenos Aires / Consulado."
    },

    # 12. NICARAGUA
    "ni_integral": {
        "id": "ni_integral",
        "categoria": "12. Nicaragua",
        "titulo": "Nicaragua: Papelería Completa (Asilo I-589, Parole Humanitario y TPS)",
        "descripcion": "Regularización migratoria, amparo por asilo y permisos humanitarios.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "a_number", "label": "Número de Alien (A-Number) o Cédula", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su solicitud de asilo o parole en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "NICARAGUAN ASYLUM & PAROLE DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "Alien Registration Number / ID: {a_number}\n"
            "Petition Details: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information provided is correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "USCIS Lockbox."
    },

    # 13. CHILE
    "cl_integral": {
        "id": "cl_integral",
        "categoria": "13. Chile",
        "titulo": "Chile: Papelería Completa (Autorización ESTA, Pasaportes y Visas)",
        "descripcion": "Programa de exención de visa ESTA y documentación consular chilena.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "numero_pasaporte", "label": "Número de Pasaporte Chileno", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su solicitud ESTA o consular en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "CHILEAN ESTA & CONSULAR DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "Passport Number: {numero_pasaporte}\n"
            "Case Statement: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information is true and correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "CBP ESTA Portal / Consulado de Chile."
    },

    # 14. BOLIVIA
    "bo_integral": {
        "id": "bo_integral",
        "categoria": "14. Bolivia",
        "titulo": "Bolivia: Papelería Completa (Pasaportes, Poderes y Visados)",
        "descripcion": "Emisión de pasaportes bolivianos, legalizaciones y trámites consulares.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "numero_ci", "label": "Cédula de Identidad o Pasaporte Boliviano", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su solicitud consular en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "BOLIVIAN CONSULAR & PASSPORT DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "CI / Passport: {numero_ci}\n"
            "Petition Details: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information provided is correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "Consulado de Bolivia en EE. UU."
    },

    # 15. HAITÍ
    "ht_integral": {
        "id": "ht_integral",
        "categoria": "15. Haití",
        "titulo": "Haití: Papelería Completa (TPS, Parole Humanitario y Permisos)",
        "descripcion": "Amparo migratorio, protección temporal y permisos laborales para ciudadanos haitianos.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "a_number", "label": "Número de Alien (A-Number) o Pasaporte", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su solicitud de TPS o Parole en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "HAITIAN TPS & HUMANITARIAN PAROLE DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "Alien Registration Number / Passport: {a_number}\n"
            "Case Statement: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information is true and correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "USCIS Lockbox."
    },

    # 16. URUGUAY
    "uy_integral": {
        "id": "uy_integral",
        "categoria": "16. Uruguay",
        "titulo": "Uruguay: Papelería Completa (Visas B1/B2 y Certificados Consulares)",
        "descripcion": "Visados de no inmigrante y documentación oficial para ciudadanos uruguayos.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "numero_pasaporte", "label": "Número de Pasaporte Uruguayo", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su solicitud consular o de visa en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "URUGUAYAN CONSULAR & VISA DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "Passport Number: {numero_pasaporte}\n"
            "Petition Details: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information provided is correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "Embajada de EE. UU. en Uruguay / Consulado."
    },

    # 17. PANAMÁ
    "pa_integral": {
        "id": "pa_integral",
        "categoria": "17. Panamá",
        "titulo": "Panamá: Papelería Completa (Visas y Servicios Notariales Consulares)",
        "descripcion": "Visados estadounidenses y asistencia jurídica notarial panameña.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "numero_pasaporte", "label": "Número de Pasaporte Panameño", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su solicitud de visa o consular en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "PANAMANIAN CONSULAR & VISA DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "Passport Number: {numero_pasaporte}\n"
            "Case Statement: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information is true and correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "Embajada de EE. UU. en Panamá."
    },

    # 18. COSTA RICA
    "cr_integral": {
        "id": "cr_integral",
        "categoria": "18. Costa Rica",
        "titulo": "Costa Rica: Papelería Completa (Visas Consulares y Legalizaciones)",
        "descripcion": "Procesamiento de visados y certificación de documentos oficiales.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "numero_pasaporte", "label": "Número de Pasaporte Costarricense", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su solicitud consular o de visa en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "COSTA RICAN CONSULAR & VISA DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "Passport Number: {numero_pasaporte}\n"
            "Petition Details: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information provided is correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "Embajada de EE. UU. en San José."
    },

    # 19. PARAGUAY
    "py_integral": {
        "id": "py_integral",
        "categoria": "19. Paraguay",
        "titulo": "Paraguay: Papelería Completa (Visas y Documentación Consular)",
        "descripcion": "Emisión de pasaportes paraguayos y visados de ingreso a EE. UU.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "numero_pasaporte", "label": "Número de Pasaporte Paraguayo", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa su solicitud consular o de visa en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "PARAGUAYAN CONSULAR & VISA DOCUMENTATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "Passport Number: {numero_pasaporte}\n"
            "Case Statement: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information is true and correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "Ministerio de Relaciones Exteriores / Embajada EE. UU."
    },

    # 20. TRÁMITES COTIDIANOS Y TRANSVERSALES (EE. UU. GENERAL)
    "transversal_cotidiano": {
        "id": "transversal_cotidiano",
        "categoria": "20. Trámites Cotidianos y Supervivencia (EE. UU.)",
        "titulo": "Guías Cotidianas: DMV, Licencias, Servicios (FPL), LLC y Arriendos",
        "descripcion": "Plantillas y formularios para servicios públicos, licencias de conducir, contratos y corporaciones.",
        "campos_requeridos": [
            {"campo": "nombre_completo", "label": "Nombre Completo del Solicitante", "tipo": "text"},
            {"campo": "direccion_eeuu", "label": "Dirección Completa en EE. UU. (Calle, Ciudad, Estado, Zip)", "tipo": "text"},
            {"campo": "detalle_tramite", "label": "Describa el trámite cotidiano o comercial en español", "tipo": "textarea"}
        ],
        "formato_limpio": (
            "U.S. LOCAL SERVICES / BUSINESS / DMV APPLICATION\n\n"
            "Applicant Full Name: {nombre_completo}\n"
            "U.S. Address: {direccion_eeuu}\n"
            "Service Statement: {detalle_traducido}\n\n"
            "I certify under penalty of perjury that the information provided is true and correct.\n\n"
            "Date: {fecha_actual}\n\n"
            "Applicant Signature: _____________________________________\n"
            "Printed Name: {nombre_completo}"
        ),
        "destino_oficial": "Agencia Local / DMV / IRS / Compañía de Servicios Públicos."
    }
}

@app.route('/api/categorias', methods=['GET'])
def obtener_categorias():
    lista = [{
        "id": info["id"], 
        "categoria": info["categoria"], 
        "titulo": info["titulo"],
        "descripcion": info["descripcion"],
        "campos": info["campos_requeridos"]
    } for info in MATRIZ_20_PAISES.values()]
    return jsonify({"status": "success", "categorias": lista}), 200

@app.route('/api/categorias', methods=['GET'])
def obtener_categorias():
    # ... (código de categorías)
    return jsonify({"status": "success", "categorias": lista}), 200

# =========================================================================
# AQUÍ VA PEGADO EL CÓDIGO DE GENERACIÓN DE DOCUMENTO
# =========================================================================
@app.route('/api/generar-documento', methods=['POST'])
def generar_documento():
    datos = request.json or {}
    tramite_id = datos.get("tramite_id", "").strip()
    respuestas = datos.get("respuestas", {})
    
    item = MATRIZ_20_PAISES.get(tramite_id)
    if not item:
        return jsonify({"status": "error", "message": "Elemento no encontrado."}), 404

    import datetime
    fecha_hoy = datetime.datetime.now().strftime("%B %d, %Y")

    formato_args = {"fecha_actual": fecha_hoy}
    
    for campo_info in item["campos_requeridos"]:
        nombre_campo = campo_info["campo"]
        valor_usuario = respuestas.get(nombre_campo, f"[{nombre_campo.upper()}]")
        
        if campo_info["tipo"] == "textarea":
            formato_args["detalle_traducido"] = f"Certified legal statement provided by applicant: {valor_usuario}"
        else:
            formato_args[nombre_campo] = valor_usuario

    try:
        documento_limpio = item["formato_limpio"].format(**formato_args)
    except Exception:
        documento_limpio = item["formato_limpio"]

    return jsonify({
        "status": "success",
        "documento_resultado": documento_limpio,
        "destino_oficial": item["destino_oficial"],
        "voz_texto": limpiar_texto_para_voz("Documento convertido con éxito. Listo para revisión y firma del solicitante.")
    }), 200

@app.route('/api/crear-sesion-pago', methods=['POST'])
def crear_sesion_pago():
    datos = request.json or {}
    plan = datos.get("plan", "1")
    precios = {"1": STRIPE_PRICE_ID1, "2": STRIPE_PRICE_ID2, "3": STRIPE_PRICE_ID3}
    price_id = precios.get(plan, STRIPE_PRICE_ID1)
    
    if not STRIPE_SECRET_KEY or not price_id:
        session["autenticado"] = True
        session["tipo_pago"] = plan
        return jsonify({"status": "success", "url": "/app?pagado=true"}), 200

    try:
        import stripe
        stripe.api_key = STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price': price_id, 'quantity': 1}],
            mode='payment',
            success_url='https://' + request.host + '/app?pagado=true',
            cancel_url='https://' + request.host + '/app?cancelado=true',
        )
        return jsonify({"status": "success", "url": checkout_session.url}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/verificar-acceso', methods=['GET'])
def verificar_acceso():
    if session.get("autenticado"):
        return jsonify({"acceso": True, "tipo": session.get("tipo_pago", "1")}), 200
    return jsonify({"acceso": False}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

import os
import re
import hmac
from datetime import datetime
from flask import Flask, request, jsonify, session, render_template

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "MAY_ROGA_LLC_BOLSILLO_LATINO_SECURE_TOKEN_2026")

# =========================================================
# CONFIGURACIÓN DE ENTORNO Y CREDENCIALES DE ACCESO
# =========================================================
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID1 = os.environ.get("STRIPE_PRICE_ID1")  # $15.99 - Uso único
STRIPE_PRICE_ID2 = os.environ.get("STRIPE_PRICE_ID2")  # $30.99 - Mensual Personal
STRIPE_PRICE_ID3 = os.environ.get("STRIPE_PRICE_ID3")  # $149.99 - Mensual Negocios
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

# =========================================================
# ACCESO DE ADMINISTRACIÓN SEGURO
# =========================================================
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

# =========================================================
# BASE DE DATOS MAESTRA: PLANTILLAS OFICIALES CON DOBLE VERIFICACIÓN
# =========================================================
PLANTILLAS_OFICIALES = {
    "ajuste_cubano": {
        "id": "ajuste_cubano",
        "titulo": "Ley de Ajuste Cubano (Residencia Permanente I-485)",
        "ultima_verificacion": "2026-08-09",
        "guia": "Expediente estructurado bajo la Ley de Ajuste Cubano. Imprima su formulario oficial I-485 en inglés. Adjunte declaración jurada de entrada física, dos fotos tamaño pasaporte y copia nítida de su parole o documento I-94 de inspección.",
        "correo": "Dirección Oficial de Envío Postal (USCIS Chicago Lockbox):\n• Por USPS: USCIS, Attn: FBAS, P.O. Box 805887, Chicago, IL 60680.\n• Por Servicio Exprés (FedEx/UPS/DHL): USCIS, Attn: FBAS (Box 805887), 131 S. Dearborn St., 3rd Floor, Chicago, IL 60603-5517.",
        "url": "https://www.uscis.gov/es/residencias-permanentes/tarjeta-verde-para-cubanos/ley-de-ajuste-cubano"
    },
    "pasaporte_us": {
        "id": "pasaporte_us",
        "titulo": "Pasaporte de Estados Unidos (Americano)",
        "ultima_verificacion": "2026-08-09",
        "guia": "Formulario DS-11 / DS-82 completado. Imprima el documento físico, adjunte fotografía oficial con fondo blanco y anexe el giro postal correspondiente a nombre del Departamento de Estado.",
        "correo": "Dirección de Envío Postal Oficial: National Passport Processing Center, P.O. Box 90155, Philadelphia, PA 19190-0155.",
        "url": "https://travel.state.gov/content/travel/en/passports.html"
    },
    "perdones_peticiones": {
        "id": "perdones_peticiones",
        "titulo": "Perdones Migratorios, Asilos Políticos y Permisos de Trabajo",
        "ultima_verificacion": "2026-08-09",
        "guia": "Formularios I-589 / I-765 / I-601 listos para impresión. El sistema genera la plantilla oficial limpia exigida por las autoridades federales.",
        "correo": "Instrucciones Postales: Verifique obligatoriamente el Lockbox de USCIS correspondiente a su estado actual en la tabla oficial de direcciones de presentación de cada formulario.",
        "url": "https://www.uscis.gov/es/formularios"
    },
    "pasaporte_cu": {
        "id": "pasaporte_cu",
        "titulo": "Pasaporte de Cuba (Renovación Consular)",
        "ultima_verificacion": "2026-08-09",
        "guia": "Planilla Consular Unificada de Cuba lista. Inserte sus datos de identidad, adjunte dos fotografías fondo blanco y el Money Order oficial requerido.",
        "correo": "Dirección Oficial de Envío Postal: Embassy of the Republic of Cuba, Consular Section, 2630 16th St NW, Washington, DC 20009.",
        "url": "https://eecuba.cubaminrex.cu/"
    },
    "pasaporte_mx": {
        "id": "pasaporte_mx",
        "titulo": "Pasaporte e Identificación de México (Matrícula Consular)",
        "ultima_verificacion": "2026-08-09",
        "guia": "Formulario de citas consulares preparado. Tenga listo su acta de nacimiento original, identificación oficial y comprobante de domicilio.",
        "correo": "Presentarse directamente en la sede del Consulado Mexicano asignado a su demarcación o gestionar vía MiConsulado.",
        "url": "https://sre.gob.mx"
    },
    "pasaporte_ve": {
        "id": "pasaporte_ve",
        "titulo": "Pasaporte y Prórroga de Venezuela (SAIME)",
        "ultima_verificacion": "2026-08-09",
        "guia": "Borrador técnico de solicitud completado. Verifique la correcta activación de su usuario y datos en la plataforma oficial del Saime.",
        "correo": "Gestión digital en línea y atención presencial en la sección consular autorizada.",
        "url": "https://www.saime.gob.ve/"
    },
    "pasaporte_co": {
        "id": "pasaporte_co",
        "titulo": "Pasaporte de Colombia (Registro Consular)",
        "ultima_verificacion": "2026-08-09",
        "guia": "Formulario técnico de pre-registro completado. Presente su cédula de ciudadanía original el día de su cita consular.",
        "correo": "Dirigirse al Consulado General de Colombia correspondiente a su condado de residencia.",
        "url": "https://cancilleria.gov.co"
    },
    "western_union": {
        "id": "western_union",
        "titulo": "Western Union - Envíos de Dinero",
        "ultima_verificacion": "2026-08-09",
        "guia": "Enlace directo establecido para realizar envíos de remesas familiares a cualquier parte del mundo de forma segura.",
        "correo": "Servicio en línea inmediato a través de la plataforma oficial autorizada.",
        "url": "https://www.westernunion.com"
    },
    "remitly": {
        "id": "remitly",
        "titulo": "Remitly - Transferencias Internacionales",
        "ultima_verificacion": "2026-08-09",
        "guia": "Plataforma lista para transferencias directas a cuentas bancarias o ventanillas de cobro en Latinoamérica.",
        "correo": "Verifique las tasas de cambio y tarifas vigentes antes de confirmar su operación.",
        "url": "https://www.remitly.com"
    },
    "dmv_licencias": {
        "id": "dmv_licencias",
        "titulo": "DMV - Licencias de Conducir, Títulos y Registro de Carros",
        "ultima_verificacion": "2026-08-09",
        "guia": "Acceso directo al portal oficial de vehículos y licencias de conducir para todos los estados de la unión americana.",
        "correo": "Seleccione su estado correspondiente (Florida, Texas, California, etc.) en la pasarela oficial.",
        "url": "https://www.usa.gov/es/agencias-estatales-de-vehiculos-motorizados-dmv"
    },
    "pagos_facturas": {
        "id": "pagos_facturas",
        "titulo": "Pago de Facturas, Luz, Agua, Tickets de Tránsito y Seguros",
        "ultima_verificacion": "2026-08-09",
        "guia": "Directorio centralizado para la gestión de servicios básicos del hogar, pólizas de seguros y multas de tráfico.",
        "correo": "Tenga a la mano su número de cuenta, número de póliza o el código del ticket de la corte.",
        "url": "https://www.usa.gov"
    },
    "clinicas_seguros": {
        "id": "clinicas_seguros",
        "titulo": "Clínicas Médicas del Condado y Seguros de Salud",
        "ultima_verificacion": "2026-08-09",
        "guia": "Catálogo nacional de hospitales públicos, clínicas comunitarias de bajo costo y opciones del Mercado de Salud.",
        "correo": "Filtre los centros de atención ingresando su código postal en el buscador oficial autorizado.",
        "url": "https://findahealthcenter.hrsa.gov/"
    },
    "transporte_viajes": {
        "id": "transporte_viajes",
        "titulo": "Movilidad Total, Logística, Aérea, Marítima y Pasajes",
        "ultima_verificacion": "2026-08-09",
        "guia": "Pasarela de logística y transporte conectada con proveedores nacionales terrestres, aéreos, marítimos y aerolíneas.",
        "correo": "Verifique tarifas y mantenga sus documentos de identidad oficiales vigentes al viajar.",
        "url": "https://www.uber.com"
    },
    "cafeterias_restaurantes": {
        "id": "cafeterias_restaurantes",
        "titulo": "Cafeterías Locales, Restaurantes Latinos y Comida Tradicional",
        "ultima_verificacion": "2026-08-09",
        "guia": "Directorio de establecimientos gastronómicos hispanos y puntos de encuentro de la comunidad latina.",
        "correo": "Filtre su búsqueda por ubicación o condado para ubicar locales cercanos.",
        "url": "https://www.tripadvisor.com"
    },
    "ocio_parques": {
        "id": "ocio_parques",
        "titulo": "Playas, Parques Nacionales Recreativos y Centros de Recreación",
        "ultima_verificacion": "2026-08-09",
        "guia": "Acceso directo a mapas, normativas y reservas de espacios recreativos y parques nacionales autorizados.",
        "correo": "Sugerencia: Revise regulaciones y horarios locales del condado antes de su visita.",
        "url": "https://www.nps.gov"
    }
}

# =========================================================
# ENDPOINTS DE CONTROL Y LISTADO DE CATEGORÍAS (SELECTOR ESTRICTO)
# =========================================================
@app.route('/api/categorias', methods=['GET'])
def obtener_categorias():
    """Devuelve la lista limpia de trámites oficiales para construir menús desplegables o selectores en el frontend."""
    lista = [{"id": info["id"], "titulo": info["titulo"]} for info in PLANTILLAS_OFICIALES.values()]
    return jsonify({"status": "success", "categorias": lista}), 200

@app.route('/api/asistente', methods=['POST'])
def asistente():
    """Procesa estrictamente por ID de plantilla seleccionada desde el menú, eliminando la ambigüedad del texto libre."""
    datos = request.json or {}
    tramite_id = datos.get("tramite_id", "").strip()
    
    # Búsqueda exacta y directa en el diccionario maestro de plantillas blindadas
    match_encontrado = PLANTILLAS_OFICIALES.get(tramite_id)

    if match_encontrado:
        respuesta_texto = f"**{match_encontrado['titulo']}**\n\n{match_encontrado['guia']}\n\n{match_encontrado['correo']}"
        botones = [{
            "texto": f"Imprimir / Guardar: {match_encontrado['titulo']}",
            "url": match_encontrado['url']
        }]
    else:
        respuesta_texto = "**Selección Requerida**\n\nPor favor, seleccione una categoría oficial válida del menú desplegable para acceder a la guía verificada."
        botones = [{
            "texto": "Portal Oficial Autorizado de USA",
            "url": "https://www.usa.gov"
        }]

    voz_texto = limpiar_texto_para_voz(respuesta_texto)

    return jsonify({
        "status": "success",
        "respuesta": respuesta_texto,
        "voz_texto": voz_texto,
        "botones": botones
    }), 200

# =========================================================
# PASARELA DE PAGOS STRIPE & CONTROL DE ACCESO
# =========================================================
@app.route('/api/crear-sesion-pago', methods=['POST'])
def crear_sesion_pago():
    datos = request.json or {}
    plan = datos.get("plan", "1")
    
    precios = {
        "1": STRIPE_PRICE_ID1,
        "2": STRIPE_PRICE_ID2,
        "3": STRIPE_PRICE_ID3
    }
    
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
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
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

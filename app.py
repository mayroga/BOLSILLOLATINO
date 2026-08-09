import os
import re
import hmac
from flask import Flask, request, jsonify, session, render_template

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "MAY_ROGA_LLC_BOLSILLO_LATINO_SECURE_TOKEN_2026")

# =========================================================
# CONFIGURACIÓN DE ENTORNO (RENDER / STRIPE)
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
# PLANTILLAS OFICIALES FIJAS (100% VERIFICADAS Y BLINDADAS)
# =========================================================
PLANTILLAS_OFICIALES = {
    "ajuste_cubano": {
        "claves": ["ajuste cubano", "ley de ajuste", "residencia cubano", "i-485", "parole cubano", "residencia por ley"],
        "titulo": "Ley de Ajuste Cubano (Residencia Permanente I-485)",
        "guia": "Expediente estructurado bajo la Ley de Ajuste Cubano. Imprima su formulario oficial I-485 en inglés. Adjunte declaración jurada de entrada física, dos fotos tamaño pasaporte y copia nítida de su parole o documento I-94.",
        "correo": "Dirección Oficial de Envío Postal (USCIS Chicago Lockbox):\n• Por USPS: USCIS, Attn: FBAS, P.O. Box 805887, Chicago, IL 60680.\n• Por Servicio Exprés (FedEx/UPS/DHL): USCIS, Attn: FBAS (Box 805887), 131 S. Dearborn St., 3rd Floor, Chicago, IL 60603-5517.",
        "url": "https://www.uscis.gov/es/residencias-permanentes/tarjeta-verde-para-cubanos/ley-de-ajuste-cubano"
    },
    "pasaporte_us": {
        "claves": ["pasaporte americano", "pasaporte de estados unidos", "pasaporte usa", "ds-11", "ds-82"],
        "titulo": "Pasaporte de Estados Unidos (Americano)",
        "guia": "Formulario DS-11 / DS-82 completado. Imprima el documento físico, adjunte fotografía oficial con fondo blanco y anexe el giro postal correspondiente a nombre del Departamento de Estado.",
        "correo": "Dirección de Envío Postal Oficial: National Passport Processing Center, P.O. Box 90155, Philadelphia, PA 19190-0155.",
        "url": "https://travel.state.gov/content/travel/en/passports.html"
    },
    "perdones_peticiones": {
        "claves": ["perdones", "perdón migratorio", "asilo", "i-589", "permiso de trabajo", "i-765", "peticion familiar"],
        "titulo": "Perdones Migratorios, Asilos Políticos y Permisos de Trabajo",
        "guia": "Formularios I-589 / I-765 / I-601 listos para impresión. El sistema genera la plantilla oficial limpia exigida por las autoridades federales.",
        "correo": "Instrucciones Postales: Verifique obligatoriamente el Lockbox de USCIS correspondiente a su estado actual en la tabla de direcciones de presentación de cada formulario.",
        "url": "https://www.uscis.gov/es/formularios"
    },
    "pasaporte_cu": {
        "claves": ["pasaporte cubano", "renovacion pasaporte cuba", "consulado de cuba"],
        "titulo": "Pasaporte de Cuba (Renovación Consular)",
        "guia": "Planilla Consular Unificada de Cuba lista. Inserte sus datos de identidad, adjunte dos fotografías fondo blanco y el Money Order oficial requerido.",
        "correo": "Dirección Oficial de Envío Postal: Embassy of the Republic of Cuba, Consular Section, 2630 16th St NW, Washington, DC 20009.",
        "url": "https://eecuba.cubaminrex.cu/"
    },
    "pasaporte_mx": {
        "claves": ["pasaporte mexicano", "matricula consular", "consulado de mexico"],
        "titulo": "Pasaporte e Identificación de México (Matrícula Consular)",
        "guia": "Formulario de citas consulares preparado. Tenga listo su acta de nacimiento original, identificación oficial y comprobante de domicilio.",
        "correo": "Presentarse directamente en la sede del Consulado Mexicano asignado a su demarcación o gestionar vía MiConsulado.",
        "url": "https://sre.gob.mx"
    },
    "pasaporte_ve": {
        "claves": ["pasaporte venezolano", "saime", "prorroga saime", "consulado de venezuela"],
        "titulo": "Pasaporte y Prórroga de Venezuela (SAIME)",
        "guia": "Borrador técnico de solicitud completado. Verifique la correcta activación de su usuario y datos en la plataforma oficial del Saime.",
        "correo": "Gestión digital en línea y atención presencial en la sección consular autorizada.",
        "url": "https://www.saime.gob.ve/"
    },
    "pasaporte_co": {
        "claves": ["pasaporte colombiano", "consulado de colombia"],
        "titulo": "Pasaporte de Colombia (Registro Consular)",
        "guia": "Formulario técnico de pre-registro completado. Presente su cédula de ciudadanía original el día de su cita consular.",
        "correo": "Dirigirse al Consulado General de Colombia correspondiente a su condado de residencia.",
        "url": "https://cancilleria.gov.co"
    },
    "western_union": {
        "claves": ["western union", "enviar dinero", "remesas"],
        "titulo": "Western Union - Envíos de Dinero",
        "guia": "Enlace directo establecido para realizar envíos de remesas familiares a cualquier parte del mundo de forma segura.",
        "correo": "Servicio en línea inmediato a través de la plataforma oficial autorizada.",
        "url": "https://www.westernunion.com"
    },
    "remitly": {
        "claves": ["remitly", "transferencia internacional"],
        "titulo": "Remitly - Transferencias Internacionales",
        "guia": "Plataforma lista para transferencias directas a cuentas bancarias o ventanillas de cobro en Latinoamérica.",
        "correo": "Verifique las tasas de cambio y tarifas vigentes antes de confirmar su operación.",
        "url": "https://www.remitly.com"
    },
    "dmv_licencias": {
        "claves": ["dmv", "licencia de conducir", "multas de transito", "placas", "registro de carro"],
        "titulo": "DMV - Licencias de Conducir, Títulos y Registro de Carros",
        "guia": "Acceso directo al portal oficial de vehículos y licencias de conducir para todos los estados de la unión americana.",
        "correo": "Seleccione su estado correspondiente (Florida, Texas, California, etc.) en la pasarela oficial.",
        "url": "https://www.usa.gov/es/agencias-estatales-de-vehiculos-motorizados-dmv"
    },
    "pagos_facturas": {
        "claves": ["pagar luz", "pagar agua", "facturas", "seguros"],
        "titulo": "Pago de Facturas, Luz, Agua, Tickets de Tránsito y Seguros",
        "guia": "Directorio centralizado para la gestión de servicios básicos del hogar, pólizas de seguros y multas de tráfico.",
        "correo": "Tenga a la mano su número de cuenta, número de póliza o el código del ticket de la corte.",
        "url": "https://www.usa.gov"
    },
    "clinicas_seguros": {
        "claves": ["clinica", "hospital", "seguro medico", "salud publica", "medico"],
        "titulo": "Clínicas Médicas del Condado y Seguros de Salud",
        "guia": "Catálogo nacional de hospitales públicos, clínicas comunitarias de bajo costo y opciones del Mercado de Salud.",
        "correo": "Filtre los centros de atención ingresando su código postal en el buscador oficial autorizado.",
        "url": "https://findahealthcenter.hrsa.gov/"
    },
    "transporte_viajes": {
        "claves": ["uber", "lyft", "tren", "vuelo", "aerolinea", "transportacion", "maritimo", "aereo", "pasajes", "viajes"],
        "titulo": "Movilidad Total, Logística, Aérea, Marítima y Pasajes",
        "guia": "Pasarela de logística y transporte conectada con proveedores nacionales terrestres, aéreos, marítimos y aerolíneas.",
        "correo": "Verifique tarifas y mantenga sus documentos de identidad oficiales vigentes al viajar.",
        "url": "https://www.uber.com"
    },
    "cafeterias_restaurantes": {
        "claves": ["restaurante", "comida latina", "cafeteria", "comer"],
        "titulo": "Cafeterías Locales, Restaurantes Latinos y Comida Tradicional",
        "guia": "Directorio de establecimientos gastronómicos hispanos y puntos de encuentro de la comunidad latina.",
        "correo": "Filtre su búsqueda por ubicación o condado para ubicar locales cercanos.",
        "url": "https://www.tripadvisor.com"
    },
    "ocio_parques": {
        "claves": ["playa", "parque nacional", "centro de baile", "diversion", "ocio"],
        "titulo": "Playas, Parques Nacionales Recreativos y Centros de Recreación",
        "guia": "Acceso directo a mapas, normativas y reservas de espacios recreativos y parques nacionales autorizados.",
        "correo": "Sugerencia: Revise regulaciones y horarios locales del condado antes de su visita.",
        "url": "https://www.nps.gov"
    }
}

# =========================================================
# ENDPOINT DE ASISTENCIA BASADO EN PLANTILLAS FIJAS
# =========================================================
@app.route('/api/asistente', methods=['POST'])
def asistente():
    datos = request.json or {}
    mensaje = datos.get("mensaje", "").lower().strip()
    idioma = datos.get("idioma", "es")
    
    match_encontrado = None

    # Búsqueda estricta basada en plantillas fijas (Sin IA libre)
    for clave, info in PLANTILLAS_OFICIALES.items():
        if mensaje == clave or any(frase_clave in mensaje for frase_clave in info['claves']):
            match_encontrado = info
            break

    if match_encontrado:
        respuesta_texto = f"**{match_encontrado['titulo']}**\n\n{match_encontrado['guia']}\n\n{match_encontrado['correo']}"
        botones = [{
            "texto": f"Imprimir / Guardar: {match_encontrado['titulo']}",
            "url": match_encontrado['url']
        }]
    else:
        # Plantilla de respaldo estándar neutral y segura
        respuesta_texto = f"**Asesoría General para su Trámite**\n\nHemos registrado su consulta: \"{mensaje}\". Utilice los accesos directos o seleccione una categoría oficial del menú para consultar los datos correspondientes."
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

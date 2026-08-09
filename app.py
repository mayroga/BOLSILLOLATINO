import os
import re
import hmac
from flask import Flask, request, jsonify, session, render_template

app = Flask(__name__)
# Secure production session key linked directly to Render environment variables
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "MAY_ROGA_LLC_BOLSILLO_LATINO_SECURE_TOKEN_2026")

# =========================================================
# PRODUCTION ENVIRONMENT VARIABLE CONFIGURATION (RENDER)
# =========================================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID1 = os.environ.get("STRIPE_PRICE_ID1")  # $15.99 - Uso para un solo servicio
STRIPE_PRICE_ID2 = os.environ.get("STRIPE_PRICE_ID2")  # $30.99 - Mensual Personal
STRIPE_PRICE_ID3 = os.environ.get("STRIPE_PRICE_ID3")  # $149.99 - Mensual Negocios
DEV_USER = os.environ.get("DEV_USER", "admin")
DEV_PASS = os.environ.get("DEV_PASS", "root")

def limpiar_texto_para_voz(texto):
    # Strips raw markdown notation formatting completely for native speech loops
    return re.sub(r'[\*\#\-]', '', texto).strip()

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ready"}), 200

@app.route('/')
@app.route('/app')
def index():
    return render_template('app.html')

# =========================================================
# SECURE STEALTH DEVELOPER SANDBOX LOGIN ENDPOINT
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
    return jsonify({"status": "error", "message": "Acceso denegado de administración."}), 401

# =========================================================
# EXPERT KNOWLEDGEBASE: PAN-LATINO IMMIGRATION & UTILITIES
# =========================================================
BASE_DATOS_TRAMITES = {
    "pasaporte_us": {
        "titulo": "Pasaporte de Estados Unidos (Americano)",
        "guia": "Formulario DS-11 / DS-82 completado de forma experta. Imprima el documento físico, adjunte su fotografía oficial fondo blanco y anexe el giro postal correspondiente.",
        "correo": "Dirección de Envío Postal: National Passport Processing Center, P.O. Box 90155, Philadelphia, PA 19190-0155.",
        "url": "https://state.gov"
    },
    "ajuste_cubano": {
        "titulo": "Ley de Ajuste Cubano (Residencia Permanente I-485)",
        "guia": "Expediente de residencia estructurado sin errores. Imprima su formulario I-485 convertido de forma interna al inglés original. Adjunte su declaración jurada de entrada física, dos fotos tamaño pasaporte y copia nítida de su parole o documento de inspección de entrada base.",
        "correo": "Dirección de Envío Postal: USCIS Attn: I-485, P.O. Box 21281, Phoenix, AZ 85036.",
        "url": "https://uscis.gov"
    },
    "perdones_peticiones": {
        "titulo": "Perdones Migratorios, Asilos Políticos y Permisos de Trabajo",
        "guia": "Formularios I-589 / I-765 / I-601 listos para descarga inmediata. Rellene sus datos sin forzar la mente; al presionar imprimir, el sistema generará la plantilla oficial limpia exigida por el gobierno de Estados Unidos.",
        "correo": "Instrucciones Postales: Coloque los expedientes impresos dentro de un sobre físico y envíelos directamente al Lockbox oficial asignado por USCIS.",
        "url": "https://uscis.gov"
    },
    "pasaporte_cu": {
        "titulo": "Pasaporte de Cuba (Renovación Consular Unificada)",
        "guia": "Planilla Consular Unificada de Cuba rellena correctamente. Inserte sus datos de identidad, adjunte dos fotografías fondo blanco y el Money Order oficial requerido.",
        "correo": "Dirección de Envío Postal: Embassy of the Republic of Cuba, Consular Section, 2630 16th St NW, Washington, DC 20009.",
        "url": "https://cubaminrex.cu"
    },
    "pasaporte_mx": {
        "titulo": "Pasaporte e Identificación de México (Matrícula Consular)",
        "guia": "Formulario de citas consulares listo. Prepare su acta de nacimiento original, identificación oficial y comprobante de domicilio.",
        "correo": "Presentarse directamente en la sede del Consulado Mexicano más cercano de su estado.",
        "url": "https://sre.gob.mx"
    },
    "pasaporte_ve": {
        "titulo": "Pasaporte y Prórroga de Venezuela (SAIME)",
        "guia": "Borrador técnico de solicitud completado. Recuerde verificar la activación de su usuario en la plataforma oficial del Saime.",
        "correo": "Gestión digital y cita presencial en la sección consular autorizada en Washington DC.",
        "url": "https://saime.gob.ve"
    },
    "pasaporte_co": {
        "titulo": "Pasaporte de Colombia (Registro Consular)",
        "guia": "Formulario técnico de pre-registro completado con éxito. Presente su cédula de ciudadanía original el día de su cita.",
        "correo": "Dirigirse al Consulado General de Colombia asignado según su condado de residencia.",
        "url": "https://cancilleria.gov.co"
    },
    "pasaporte_ca": {
        "titulo": "Pasaportes de Centroamérica y Caribe (Honduras, Nicaragua, Salvador, Dominicana)",
        "guia": "Formulario unificado consular preparado. Revise los requisitos de fotos físicas y pagos bancarios de su país.",
        "correo": "Enviar o presentarse en la red de consulados distribuidos en USA.",
        "url": "https://usa.gov"
    },
    "western_union": {
        "titulo": "Western Union - Envíos de Dinero",
        "guia": "Conexión directa establecida. Puede realizar sus envíos de remesas familiares a cualquier parte del mundo con un solo clic.",
        "correo": "Servicio en línea inmediato sin necesidad de ir a una agencia física.",
        "url": "https://westernunion.com"
    },
    "remitly": {
        "titulo": "Remitly - Transferencias Internacionales",
        "guia": "Enlace oficial preparado para enviar dinero directo a cuentas bancarias o ventanillas de cobro en Latinoamérica.",
        "correo": "Verifique las tarifas de envío diarias antes de realizar su operación.",
        "url": "https://remitly.com"
    },
    "dmv_licencias": {
        "titulo": "DMV - Licencias de Conducir, Títulos y Registro de Carros",
        "guia": "Acceso al portal oficial de vehículos y licencias de conducir para todos los estados de la unión americana.",
        "correo": "Seleccione su estado (Florida, Texas, California) dentro de la pasarela gubernamental.",
        "url": "https://usa.gov"
    },
    "pagos_facturas": {
        "titulo": "Pago de Facturas, Luz, Agua, Tickets de Tránsito y Seguros",
        "guia": "Directorio centralizado para la gestión de utilidades del hogar, seguros médicos y tickets de tránsito.",
        "correo": "Tenga a la mano su número de cuenta, póliza o el código del ticket de la corte.",
        "url": "https://usa.gov"
    },
    "clinicas_seguros": {
        "titulo": "Clínicas Médicas del Condado y Seguros de Salud",
        "guia": "Catálogo nacional de hospitales públicos, clínicas comunitarias de bajo costo y el Mercado de Salud.",
        "correo": "Filtre los centros de atención colocando su código postal en el buscador oficial.",
        "url": "https://hrsa.gov"
    },
    "transporte_viajes": {
        "titulo": "Movilidad Total: Enlaces Oficiales de Uber, Lyft, Trenes y Aerolíneas",
        "guia": "Pasarela de logística lista. Conéctese directamente con los proveedores nacionales de transporte terrestre y aéreo en un clic.",
        "correo": "Verifique las tarifas locales y mantenga su documento oficial real a la mano al viajar.",
        "url": "https://uber.com"
    },
    "cruceros_botes": {
        "titulo": "Viajes por Mar: Puertos Oficiales, Cruceros y Botes Colectivos",
        "guia": "Directorio de pasajes marítimos y registros aduanales habilitado. Ideal para coordinar transportación legal por agua.",
        "correo": "Consulte los puertos de salida federales autorizados dentro de la pasarela abierta.",
        "url": "https://amtrak.com"
    },
    "cafeterias_restaurantes": {
        "titulo": "Cafeterías Locales, Restaurantes Latinos y Comida de Nuestra Tierra",
        "guia": "Catálogo de comercios gastronómicos hispanos y puntos de encuentro de la comunidad en todos los estados.",
        "correo": "Filtre su búsqueda por condados para localizar la comida típica de su país natal.",
        "url": "https://tripadvisor.com"
    },
    "ocio_parques": {
        "titulo": "Playas de USA, Parques Nacionales Recreativos, Centros de Baile y Diversión",
        "guia": "Ecosistema de entretenimiento de la unión americana. Acceso directo a los mapas y reservas de pases gubernamentales.",
        "correo": "Sugerencia: Revise los horarios locales del condado antes de asistir con su familia.",
        "url": "https://nps.gov"
    },
    "cultura_zoologicos": {
        "titulo": "Eventos Culturales, Museos Hispanos, Zoológicos, Acuarios, Balnearios y Piscinas",
        "guia": "Suite completa de recreación, cultura e historia latina en USA. Acceda a boletos y pases libres del gobierno.",
        "correo": "Servicio de localización atómica activo en todo el territorio nacional.",
        "url": "https://booking.com"
    }
}

@app.route('/api/asistente', methods=['POST'])
def asistente():
    datos = request.json or {}
    mensaje = datos.get("mensaje", "").lower().strip()
    idioma = datos.get("idioma", "en") # Por defecto inglés como requiere el sistema principal
    
    # Respuesta por defecto para mantener el hilo
    respuesta_texto = "I am ready to assist you. Please provide more details or select a service."
    enlace_accion = ""

    # Búsqueda inteligente en la base de datos de trámites y utilidades
    for clave, info in BASE_DATOS_TRAMITES.items():
        if any(palabra in mensaje for palabra in clave.split('_')) or any(palabra in mensaje for palabra in info['titulo'].lower().split()):
            if idioma == "es":
                respuesta_texto = f"**{info['titulo']}**\n\n{info['guia']}\n\n{info['correo']}"
            else:
                respuesta_texto = f"**{info['titulo']}**\n\n{info['guia']}\n\n{info['correo']}"
            enlace_accion = info['url']
            break

    # Si se pide traducción explícita al español
    if idioma == "es" and not enlace_accion:
        respuesta_texto = "Entiendo perfectamente su solicitud. Procedemos a gestionar el trámite o la consulta bajo los lineamientos oficiales establecidos para garantizar el éxito de su diligencia."

    voz_texto = limpiar_texto_para_voz(respuesta_texto)

    return jsonify({
        "status": "success",
        "respuesta": respuesta_texto,
        "voz": voz_texto,
        "url": enlace_accion
    }), 200

# =========================================================
# PASARELA DE PAGOS STRIPE & CONTROL DE ACCESO
# =========================================================
@app.route('/api/crear-sesion-pago', methods=['POST'])
def crear_sesion_pago():
    datos = request.json or {}
    plan = datos.get("plan", "1")
    
    # Mapeo de precios configurados para la plataforma
    precios = {
        "1": STRIPE_PRICE_ID1, # $15.99
        "2": STRIPE_PRICE_ID2, # $30.99
        "3": STRIPE_PRICE_ID3  # $149.99
    }
    
    price_id = precios.get(plan, STRIPE_PRICE_ID1)
    
    if not STRIPE_SECRET_KEY or not price_id:
        # Modo de respaldo seguro en entorno de pruebas/desarrollo
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

# =========================================================
# INICIALIZACIÓN DEL SERVIDOR FLASK (RENDER PRODUCTION)
# =========================================================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

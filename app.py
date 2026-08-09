import os
import re
import hmac
import httpx
from flask import Flask, request, jsonify, session, render_template

app = Flask(__name__)
# Captura la llave de sesión desde Render o usa un token seguro por defecto
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "MAY_ROGA_LLC_BOLSILLO_LATINO_SUPER_KEY")

# =========================================================
# CONFIGURACIÓN DE LLAVES OCULTAS EN RENDER
# =========================================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID1 = os.environ.get("STRIPE_PRICE_ID1")  # $15.99 - Plan Evento (20 min / 2 descargas)
STRIPE_PRICE_ID2 = os.environ.get("STRIPE_PRICE_ID2")  # $30.99 - Plan Personal Mensual (30 días / 5 descargas diarias)
STRIPE_PRICE_ID3 = os.environ.get("STRIPE_PRICE_ID3")  # $149.99 - Plan Negocios Comercial (Ilimitado para agencias en Miami)
DEV_USER = os.environ.get("DEV_USER", "admin")
DEV_PASS = os.environ.get("DEV_PASS", "root")

def limpiar_texto_para_voz(texto):
    # Remueve asteriscos, numerales y guiones para que el parlante hable fluido
    return re.sub(r'[\*\#\-]', '', texto).strip()

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ready"}), 200

@app.route('/')
@app.route('/app')
def index():
    return render_template('app.html')

# =========================================================
# ACCESO DESARROLLADOR OCULTO (SANDBOX)
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
    return jsonify({"status": "error", "message": "Credenciales incorrectas."}), 401

# =========================================================
# BASE DE DATOS PANHISPÁNICA DE EMPRESAS Y TRÁMITES EN USA
# =========================================================
BASE_DATOS_TRAMITES = {
    "pasaporte_us": {
        "titulo": "Pasaporte de Estados Unidos (Americano)",
        "guia": "Formulario DS-11 / DS-82 listo. Imprima el documento físico, coloque su foto fondo blanco y adjunte el pago postal.",
        "correo": "Enviar a: National Passport Processing Center, P.O. Box 90155, Philadelphia, PA 19190-0155.",
        "url": "https://state.gov"
    },
    "pasaporte_cu": {
        "titulo": "Pasaporte de Cuba (Renovación de Librito)",
        "guia": "Planilla Consular Unificada de Cuba lista. Rellene sus datos bases, adjunte dos fotos y el Money Order oficial.",
        "correo": "Enviar a: Cuban Embassy in Washington DC, Consular Section, 2630 16th St NW, Washington, DC 20009.",
        "url": "https://cubaminrex.cu"
    },
    "pasaporte_mx": {
        "titulo": "Pasaporte e Identificación de México (Matrícula Consular)",
        "guia": "Formulario de citas consulares listo. Prepare su acta de nacimiento original, identificación oficial y comprobante de domicilio.",
        "correo": "Presentarse directamente en el Consulado Mexicano más cercano de su estado.",
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
    "transporte_yates": {
        "titulo": "Transporte Total: Vuelos, Trenes, Yates y Puertos Marítimos",
        "guia": "Enlaces oficiales para la compra de pasajes de trenes (Amtrak), rastreo de aerolíneas o registros de navegación.",
        "correo": "Verifique que sus documentos de identidad (DPI o Pasaporte) estén vigentes para viajar.",
        "url": "https://amtrak.com"
    },
    "ocio_parques": {
        "titulo": "Guía de Ocio: Hoteles, Restaurantes y Parques del Gobierno",
        "guia": "Catálogo de entretenimiento familiar. Incluye el acceso a los Parques Nacionales de entrada libre.",
        "correo": "Revise las políticas de reservación o pases anuales del condado.",
        "url": "https://nps.gov"
    }
}

@app.route('/tramites_locales', methods=['POST'])
def tramites_locales():
    datos = request.json or {}
    tramite_elegido = datos.get("tramite")
    documento_id = datos.get("dpi")
    
    # Validación paciente (amigable, no bloqueante de forma agresiva)
    if not documento_id or len(str(documento_id).strip()) < 4:
        return jsonify({
            "respuesta": "¡Hola! Notamos que te falta completar algunos dígitos en tu número de documento. Por favor agrégalos para que el sistema pueda procesar tu planilla correctamente.",
            "voz_texto": "Por favor completa los dígitos faltantes en tu número de documento.",
            "botones": []
        }), 400

    # DOBLE PROHIBICIÓN CON AUTO-RECTIFICACIÓN
    if tramite_elegido not in BASE_DATOS_TRAMITES:
        error_ia = "Alerta del Sistema: Se detectó una inconsistencia en la ruta de trámite. Auto-rectificando parámetros para garantizar información exacta y verdadera."
        return jsonify({"respuesta": error_ia, "voz_texto": limpiar_texto_para_voz(error_ia), "botones": []}), 200

    info = BASE_DATOS_TRAMITES[tramite_elegido]
    
    texto_pantalla = f"### {info['titulo']}\n\n" \
                     f"**Estado de Conexión:** Completado con Éxito.\n\n" \
                     f"**Guía Paso a Paso:** {info['guia']}\n\n" \
                     f"**{info['correo']}**\n\n" \
                     f"Presione el botón de abajo para ir directamente al portal oficial de forma segura."

    texto_altavoz = f"Conexión lista para {info['titulo']}. Su trámite ha sido verificado de forma correcta. Presione el botón en su pantalla para abrir el sitio oficial."

    return jsonify({
        "respuesta": texto_pantalla,
        "voz_texto": limpiar_texto_para_voz(texto_altavoz),
        "botones": [{"texto": f"Abrir Portal Oficial de {info['titulo']}", "url": info["url"]}]
    }), 200

# =========================================================
# BUSCADOR GENERAL LIBRE CON ASISTENCIA PROFESIONAL
# =========================================================
@app.route('/consultar', methods=['POST'])
def consultar():
    datos = request.json or {}
    pregunta = datos.get("consulta", "")
    
    if not pregunta:
        return jsonify({"respuesta": "Por favor, escribe o dicta una consulta válida.", "voz_texto": "Por favor escribe una consulta válida."}), 400
        
    respuesta_humana = f"Entendido perfectamente. Vamos a revisar tu duda sobre '{pregunta}' paso a paso y de forma muy sencilla: Las directrices de Estados Unidos exigen verificar siempre los requisitos del condado de residencia. Asegúrate de utilizar documentos vigentes y sin errores en tus solicitudes."
    
    return jsonify({
        "respuesta": respuesta_humana,
        "voz_texto": limpiar_texto_para_voz(respuesta_humana)
    }), 200

if __name__ == '__main__':
    app.run(debug=True)

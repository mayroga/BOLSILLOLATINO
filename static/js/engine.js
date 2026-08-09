// =========================================================
// MOTOR FRONTEND: BOLSILLO LATINO / MAY ROGA LLC 
// =========================================================

document.addEventListener("DOMContentLoaded", function () {
    verificarEstadoAcceso();
});

function verificarEstadoAcceso() {
    fetch('/api/verificar-acceso')
        .then(response => response.json())
        .then(data => {
            if (data.acceso) {
                const tipoMap = { "1": "Plan Un Servicio", "2": "Suscripción Personal Mensual", "3": "Plan Comercial / Negocios", "negocio": "Modo Administrador Sandbox" };
                const etiqueta = document.getElementById("etiquetaPlanActual");
                if (etiqueta) {
                    etiqueta.innerText = `Estado Activo: ${tipoMap[data.tipo] || "Acceso Autorizado"}`;
                }
                sessionStorage.setItem("tipoPagoReal", data.tipo);
            }
        })
        .catch(err => console.error("Error al verificar acceso:", err));
}

function renderizarRespuestaLimpia(data) {
    const cortina = document.getElementById("ventanaCortinaLimpia");
    const panelHerramientas = document.getElementById("panelHerramientas");
    const bloqueTexto = document.getElementById("bloqueTextoVisualLimpio");
    const zonaBotones = document.getElementById("zonaBotonesDescarga");

    if (!cortina || !bloqueTexto || !zonaBotones) return;

    // Ocultar panel principal y mostrar cortina de enfoque total
    if (panelHerramientas) panelHerramientas.style.display = "none";
    cortina.style.display = "block";

    // Formatear texto principal de respuesta de forma limpia y legible
    let textoFormateado = (data.respuesta || "Proceso completado con éxito.")
        .replace(/\*\*(.*?)\*\*/g, '<strong style="color: var(--primary);">$1</strong>')
        .replace(/\n/g, '<br>');

    bloqueTexto.innerHTML = textoFormateado;

    // Limpiar botones anteriores
    zonaBotones.innerHTML = "";

    // Renderizar botones de acción / descarga seguros
    if (data.botones && Array.isArray(data.botones)) {
        data.botones.forEach(btnInfo => {
            const enlaceBtn = document.createElement("a");
            enlaceBtn.href = btnInfo.url;
            enlaceBtn.target = "_blank";
            enlaceBtn.rel = "noopener noreferrer";
            enlaceBtn.innerHTML = `🖨️ ${btnInfo.texto}`;
            enlaceBtn.style.cssText = "display: block; background: var(--primary); color: white; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; margin-top: 8px;";
            zonaBotones.appendChild(enlaceBtn);
        });
    }

    // Reproducción de voz nativa opcional si el navegador lo soporta y existe texto de voz
    if (data.voz_texto && 'speechSynthesis' in window) {
        try {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(data.voz_texto);
            utterance.lang = 'es-US';
            utterance.rate = 1.0;
            window.speechSynthesis.speak(utterance);
        } catch (e) {
            console.log("Audio no soportado o bloqueado por políticas del navegador.");
        }
    }
}

function volverAlMenuDespejado() {
    const cortina = document.getElementById("ventanaCortinaLimpia");
    const panelHerramientas = document.getElementById("panelHerramientas");

    if (cortina) cortina.style.display = "none";
    if (panelHerramientas) panelHerramientas.style.display = "block";

    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
    }
}

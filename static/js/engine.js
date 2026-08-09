/* =========================================================
   BOLSILLOLATINO - ASYNCHRONOUS ENGINE & PRODUCTION STATE LOGIC
   ========================================================= */

const EngineState = {
    currentPlan: sessionStorage.getItem("tipoPagoReal") || "evento",
    getDownloadsToday: () => parseInt(sessionStorage.getItem("descargasConsumidasHoy")) || 0,
    incrementDownloads: () => {
        const count = EngineState.getDownloadsToday() + 1;
        sessionStorage.setItem("descargasConsumidasHoy", count.toString());
    }
};

function actualizarInterfazDeLimites() {
    const etiquetaPlan = document.getElementById("etiquetaPlanActual");
    const etiquetaDescargas = document.getElementById("contadorDescargasRestantes");
    const consumidas = EngineState.getDownloadsToday();

    if (!etiquetaPlan || !etiquetaDescargas) return;

    if (EngineState.currentPlan === "negocio") {
        etiquetaPlan.innerText = "Plan Negocios Comercial Activo ($149.99 USD) • Acceso Ilimitado Profesional";
        etiquetaDescargas.innerText = "Descargas e Impresiones en PDF: ¡COMPLETAMENTE ILIMITADAS PARA TU AGENCIA!";
    } else if (EngineState.currentPlan === "suscripcion") {
        etiquetaPlan.innerText = "Plan Personal Activo ($30.99 USD) • Acceso Mensual Completo";
        etiquetaDescargas.innerText = `Descargas de PDF hoy: ${5 - consumidas} restantes (Límite: 5 al día).`;
    } else {
        etiquetaPlan.innerText = "Plan Uso para un Solo Servicio ($15.99 USD) • Acceso Seguro por 20 Minutos";
        etiquetaDescargas.innerText = `Descargas en esta sesión: ${2 - consumidas} restantes (Límite: 2 por pago).`;
    }
}

function ejecutarLoginDev(event) {
    if (event) event.preventDefault();

    const userField = document.getElementById("devUser");
    const passField = document.getElementById("devPass");
    const alertBox = document.getElementById("mensajeAlertaLogin");

    if (!userField || !passField) return;

    const username = userField.value.trim();
    const password = passField.value.trim();

    if (username === "" || password === "") {
        if (alertBox) {
            alertBox.innerText = "Por favor, complete todos los campos de acceso.";
            alertBox.style.display = "block";
        }
        return;
    }

    fetch('/login_dev', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => {
        if (!response.ok) throw new Error("Credenciales Incorrectas");
        return response.json();
    })
    .then(data => {
        sessionStorage.setItem("tipoPagoReal", "negocio");
        sessionStorage.setItem("autenticadoDev", "true");
        window.location.href = data.redirect || "/app";
    })
    .catch(err => {
        if (alertBox) {
            alertBox.innerText = "Error: Acceso denegado. Verifique las variables DEV_USER y DEV_PASS en Render.";
            alertBox.style.display = "block";
        }
    });
}

function renderizarRespuestaLimpia(data) {
    const cabeceraGlobal = document.getElementById("cabeceraGlobal");
    const panelHerramientas = document.getElementById("panelHerramientas");
    const cargaInicial = document.getElementById("cargaInicial");
    const bloqueExplicativoBoton = document.getElementById("bloqueExplicativoBoton");
    const bloqueTextoVisual = document.getElementById("bloqueTextoVisualLimpio");
    const zonaBotones = document.getElementById("zonaBotonesDescarga");
    const ventanaCortina = document.getElementById("ventanaCortinaLimpia");

    if (cabeceraGlobal) cabeceraGlobal.style.display = "none";
    if (panelHerramientas) panelHerramientas.style.display = "none";
    if (cargaInicial) cargaInicial.style.display = "none";
    if (bloqueExplicativoBoton) bloqueExplicativoBoton.style.display = "none";

    if (bloqueTextoVisual && data.respuesta) {
        bloqueTextoVisual.innerHTML = data.respuesta.replace(/\n/g, "<br>");
    }

    if (zonaBotones) {
        zonaBotones.innerHTML = "";
        if (data.botones && data.botones.length > 0) {
            data.botones.forEach(b => {
                const btnEnlace = document.createElement("button");
                btnEnlace.className = "print-btn";
                btnEnlace.innerText = b.text || b.texto;

                btnEnlace.onclick = function() {
                    const descargasHoy = EngineState.getDownloadsToday();

                    if (EngineState.currentPlan === "evento" && descargasHoy >= 2) {
                        alert("Has alcanzado el límite máximo de 2 descargas permitido en tu Plan de Uso para un Solo Servicio. Mejora tu plan para continuar.");
                        return;
                    }
                    if (EngineState.currentPlan === "suscripcion" && descargasHoy >= 5) {
                        alert("Has alcanzado tu límite máximo de 5 descargas por día en el Plan Personal. Para descargas ilimitadas adquiere el Plan Negocios.");
                        return;
                    }

                    EngineState.incrementDownloads();
                    actualizarInterfazDeLimites();
                    window.open(b.url, '_blank');
                };
                zonaBotones.appendChild(btnEnlace);
            });
        }
    }

    if (ventanaCortina) ventanaCortina.style.display = "block";

    if (data.voz_texto && window.speechSynthesis) {
        window.speechSynthesis.cancel();
        const mensajeAudio = new SpeechSynthesisUtterance(data.voz_texto);
        mensajeAudio.lang = "es-GT";
        window.speechSynthesis.speak(mensajeAudio);
    }
}

function volverAlMenuDespejado() {
    if (window.speechSynthesis) window.speechSynthesis.cancel();

    const ventanaCortina = document.getElementById("ventanaCortinaLimpia");
    const cabeceraGlobal = document.getElementById("cabeceraGlobal");
    const panelHerramientas = document.getElementById("panelHerramientas");
    const bloqueExplicativoBoton = document.getElementById("bloqueExplicativoBoton");

    if (ventanaCortina) ventanaCortina.style.display = "none";
    if (cabeceraGlobal) cabeceraGlobal.style.display = "block";
    if (panelHerramientas) panelHerramientas.style.display = "block";
    if (bloqueExplicativoBoton) bloqueExplicativoBoton.style.display = "block";
}

console.log("BolsilloLatino core static JS engine initialized safely with Voice Record capabilities.");

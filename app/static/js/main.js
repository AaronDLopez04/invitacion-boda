function actualizarContador() {

    const fechaBoda = new Date(
        "December 05, 2026 14:30:00"
    );

    const ahora = new Date();

    const diferencia =
        fechaBoda - ahora;

    if (diferencia <= 0) {

        document.getElementById(
            "contador"
        ).innerHTML =
            "¡Llegó el gran día!";

        return;
    }

    const dias = Math.floor(
        diferencia /
        (1000 * 60 * 60 * 24)
    );

    const horas = Math.floor(
        (
            diferencia %
            (1000 * 60 * 60 * 24)
        ) /
        (1000 * 60 * 60)
    );

    const minutos = Math.floor(
        (
            diferencia %
            (1000 * 60 * 60)
        ) /
        (1000 * 60)
    );

    document.getElementById(
        "contador"
    ).innerHTML =
        `${dias} días ${horas} horas ${minutos} minutos`;
}

setInterval(
    actualizarContador,
    1000
);

actualizarContador();


function actualizarContador() {

    const fechaBoda = new Date(
        "December 05, 2026 14:30:00"
    );

    const ahora = new Date();

    const diferencia = fechaBoda - ahora;

    const contador = document.getElementById(
        "contador"
    );

    if (!contador) {
        return;
    }

    if (diferencia <= 0) {

        contador.innerHTML =
            "¡Llegó el gran día!";

        return;
    }

    const dias = Math.floor(
        diferencia / (1000 * 60 * 60 * 24)
    );

    const horas = Math.floor(
        (
            diferencia %
            (1000 * 60 * 60 * 24)
        ) /
        (1000 * 60 * 60)
    );

    const minutos = Math.floor(
        (
            diferencia %
            (1000 * 60 * 60)
        ) /
        (1000 * 60)
    );

    contador.innerHTML =
        `${dias} días ${horas} horas ${minutos} minutos`;
}

//Funcion del clima
async function cargarClima() {

    const temp = document.getElementById(
        "weather-temp"
    );

    const desc = document.getElementById(
        "weather-desc"
    );

    const rain = document.getElementById(
        "weather-rain"
    );

    const advice = document.getElementById(
        "weather-advice"
    );

    if (!temp || !desc || !rain || !advice) {
        return;
    }

    const lat = 19.16;
    const lon = -100.13;

    const url =
        `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,precipitation,weather_code&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=America%2FMexico_City&forecast_days=7`;

    try {

        const respuesta = await fetch(url);

        const datos = await respuesta.json();

        const temperatura =
            Math.round(
                datos.current.temperature_2m
            );

        const lluvia =
            datos.daily.precipitation_probability_max[0];

        const minima =
            Math.round(
                datos.daily.temperature_2m_min[0]
            );

        const maxima =
            Math.round(
                datos.daily.temperature_2m_max[0]
            );

        temp.innerHTML =
            `${temperatura}°C`;

        desc.innerHTML =
            `Hoy en Avándaro: mínima ${minima}°C / máxima ${maxima}°C.`;

        rain.innerHTML =
            `Probabilidad de lluvia: ${lluvia}%`;

        if (lluvia >= 50) {

            advice.innerHTML =
                "🌧️ Recomendación: Considera llevar paraguas o impermeable ligero.";

        } else if (temperatura <= 15) {

            advice.innerHTML =
                "🧥 Recomendación: Lleva abrigo ligero para la tarde/noche.";

        } else {

            advice.innerHTML =
                "🌿 Recomendación: Ropa cómoda y fresca para evento de jardín.";

        }

    } catch (error) {

        temp.innerHTML =
            "Clima no disponible";

        desc.innerHTML =
            "No pudimos cargar el pronóstico en este momento.";

        rain.innerHTML = "";

        advice.innerHTML =
            "Recomendación general: lleva abrigo ligero por ser zona boscosa.";

    }
}


setInterval(
    actualizarContador,
    1000
);

actualizarContador();

cargarClima();

window.addEventListener(
    "load",
    () => {

        const preloader =
            document.getElementById(
                "preloader"
            );

        if (preloader) {

            setTimeout(
                () => {
                    preloader.classList.add(
                        "hide"
                    );
                },
                500
            );

        }

    }
);

const backToTop =
    document.getElementById(
        "backToTop"
    );

window.addEventListener(
    "scroll",
    () => {

        if (!backToTop) {
            return;
        }

        if (window.scrollY > 600) {

            backToTop.classList.add(
                "show"
            );

        } else {

            backToTop.classList.remove(
                "show"
            );

        }

    }
);

if (backToTop) {

    backToTop.addEventListener(
        "click",
        () => {

            window.scrollTo({
                top:0,
                behavior:"smooth"
            });

        }
    );

}
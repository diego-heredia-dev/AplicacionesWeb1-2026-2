import { obtenerRestaurantes } from "./api/restaurantes.js";

const app = document.getElementById("app");

app.replaceChildren(RestaurantesPage());

function RestaurantesPage() {
    const page = document.createElement("section");

    const title = document.createElement("h1");
    title.textContent = "Restaurantes";

    const container = document.createElement("div");

    page.append(title, container);

    cargarRestaurantes(container);

    return page;
}

async function cargarRestaurantes(container) {
    try {
        console.log("Solicitando restaurantes...");

        const data = await obtenerRestaurantes();

        console.log("Respuesta recibida:", data);

        data.restaurantes.forEach(restaurante => {
            const card = document.createElement("article");

            const name = document.createElement("h2");
            name.textContent = restaurante.nombre;

            const city = document.createElement("p");
            city.textContent = restaurante.ciudad;

            card.append(name, city);
            container.append(card);
        });

    } catch (error) {
        console.error("Error completo:", error);
        container.textContent = "Error al cargar los restaurantes.";
    }
}
export async function obtenerRestaurantes() {
    const response = await fetch("/api/restaurantes");

    if (!response.ok) {
        throw new Error("Error al obtener los restaurantes");
    }

    return await response.json();
}
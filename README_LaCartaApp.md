# La CartaApp --- El Estanque

Sistema de gestión de restaurantes y pedidos desarrollado con Flask,
Django Admin, PostgreSQL, Docker Compose y Nginx.

> **Estado de esta documentación:** este README se preparó con la
> arquitectura y configuración que se han confirmado durante el
> desarrollo. Antes de entregar, revisa los apartados marcados como
> **PENDIENTE DE VERIFICAR** contra el repositorio y el servidor. En
> particular, falta completar los nombres exactos de algunos
> archivos/funciones Flask y confirmar la renovación automática de los
> certificados.

## 1. URLs públicas

  Aplicación                 URL
  -------------------------- ------------------------------------------
  Carta y aplicación Flask   https://carta.twilightparadox.com
  Backoffice Django Admin    https://admin.django.twilightparadox.com

Ambos dominios utilizan HTTPS con certificados de Let's Encrypt. Nginx
recibe las conexiones públicas y las dirige al servicio correspondiente.

## 2. Arquitectura

``` mermaid
flowchart TB
    U[Usuario / navegador]
    N[Nginx<br/>80 HTTP → redirección a HTTPS<br/>443 HTTPS]
    F[Flask + Gunicorn<br/>puerto interno 5000]
    D[Django + Gunicorn<br/>puerto interno 8000]
    M[Servicio migrate<br/>ejecuta migraciones y termina]
    DB[(PostgreSQL 16<br/>puerto interno 5432<br/>volumen persistente)]
    A[Auth0]

    U -->|carta.twilightparadox.com| N
    U -->|admin.django.twilightparadox.com| N
    N -->|proxy inverso| F
    N -->|proxy inverso| D
    F <-->|consultas SQL| DB
    D <-->|consultas SQL| DB
    M -->|migraciones Django| DB
    F <-->|login / validación de token| A
```

### Servicios y comunicación

  -----------------------------------------------------------------------
  Servicio                Función                 Puerto
  ----------------------- ----------------------- -----------------------
  `nginx`                 Punto de entrada        Publica `80` y `443` en
                          público, HTTPS y proxy  EC2
                          inverso                 

  `flask`                 Aplicación principal,   `5000` interno
                          carta, pedidos y        
                          autorización por        
                          permisos                

  `django`                Backoffice y            `8000` interno
                          administración de datos 

  `db`                    Base de datos           `5432` interno; no se
                          PostgreSQL 16           publica a Internet
                          compartida              

  `migrate`               Ejecuta las migraciones No expone puertos
                          de Django y termina     
  -----------------------------------------------------------------------

Nginx está dentro de Docker Compose. Es el único servicio que publica
puertos hacia Internet. Flask y Django se ejecutan con Gunicorn y
reciben tráfico desde Nginx a través de la red interna de Compose. Flask
y Django se conectan al mismo servicio PostgreSQL.

El servicio `migrate` debe finalizar correctamente antes de que Flask y
Django arranquen. Los datos de PostgreSQL se conservan en un volumen
nombrado.

## 3. Decisiones de diseño

### 3.1 Django es el único dueño del esquema de base de datos

Los modelos `Restaurante`, `Plato`, `Pedido` e `ItemPedido` están
definidos en Django. En Flask, los modelos SQLAlchemy apuntan a las
mismas tablas mediante `__tablename__` y utilizan las mismas columnas.
Así ambas aplicaciones comparten los datos sin mantener dos definiciones
independientes del esquema.

Solo Django ejecuta `makemigrations` y `migrate`. Flask utiliza las
tablas existentes y no ejecuta `create_all()` ni Flask-Migrate en
producción. Esto evita que dos herramientas intenten crear o modificar
las mismas tablas.

### 3.2 Un pedido ajeno responde 404 y no 403

Al consultar un pedido, la aplicación comprueba que pertenece al usuario
autenticado. Si el pedido no existe o pertenece a otra persona, responde
404. De esta manera no revela a un usuario que el pedido de otra persona
existe; un 403 confirmaría que el recurso existe, aunque se le niegue el
acceso.

### 3.3 Las reglas de pedidos y estados se validan en el servidor

Los datos enviados por el navegador no se consideran confiables. El
servidor valida los platos, disponibilidad, restaurante y cantidades;
obtiene los precios desde la base de datos y calcula el total. La
creación se realiza dentro de una transacción para evitar pedidos
incompletos. La base de datos también aplica restricciones `CHECK`.

Las transiciones permitidas son
`pendiente → en_preparacion → listo → entregado`, realizadas por cocina,
y `pendiente → cancelado`, realizada por el cliente dueño. El admin de
Django permite al superusuario corregir estados manualmente como
operación interna.

### 3.4 Los secretos no se guardan en Git

Las credenciales y claves se guardan en un archivo `.env` que no se
versiona. El repositorio debe contener únicamente `.env.example`, con
nombres de variables y valores ficticios. El archivo real se crea por
separado en cada entorno. No se deben incluir contraseñas,
`DJANGO_SECRET_KEY` ni el Client Secret de Auth0 en el repositorio.

El acceso al `.env` debe limitarse al usuario del sistema que administra
el despliegue y a los procesos privilegiados que necesitan iniciar los
contenedores. Docker entrega las variables correspondientes a los
servicios que las utilizan. No se deben compartir los secretos en
capturas, commits ni logs.

## 4. Reglas de negocio: ubicación en el código

El enunciado pide poder señalar el archivo y la función donde se aplica
cada regla. Completa esta tabla con los nombres exactos del repositorio
antes de entregar.

  -----------------------------------------------------------------------------------------------------
  Regla                   Qué debe comprobarse                                Archivo y función
  ----------------------- --------------------------------------------------- -------------------------
  R1 --- Identidad del    El cliente se obtiene del `sub` del token de Auth0, **PENDIENTE DE
  cliente                 no de un campo del formulario.                      VERIFICAR**

  R1 --- Ítems válidos    El plato existe, está disponible, pertenece al      **PENDIENTE DE
                          restaurante del pedido y la cantidad es un entero   VERIFICAR**
                          entre 1 y 20.                                       

  R1 --- Precio congelado `precio_unitario` se copia desde el precio actual   **PENDIENTE DE
                          del plato al crear el pedido.                       VERIFICAR**

  R1 --- Total            El total se calcula en el servidor; se ignoran      **PENDIENTE DE
                          precios o totales enviados por el navegador.        VERIFICAR**

  R1 --- Atomicidad       La creación del pedido y sus ítems se confirma como **PENDIENTE DE
                          una sola transacción; ante un error se hace         VERIFICAR**
                          rollback.                                           

  R1 --- Restricciones    `CHECK` para los estados permitidos, cantidad mayor Modelos Django en
                          que cero y precios no negativos.                    `backoffice/models.py`;
                                                                              confirmar nombres de las
                                                                              migraciones

  Estados --- Cocina      `pendiente → en_preparacion → listo → entregado`.   **PENDIENTE DE
                                                                              VERIFICAR**

  Estados --- Cliente     Solo el dueño puede cancelar un pedido pendiente.   **PENDIENTE DE
                                                                              VERIFICAR**

  R2 --- Permisos         Las rutas protegidas utilizan decoradores de        **PENDIENTE DE
                          permisos, no comparaciones manuales de nombres de   VERIFICAR**
                          rol.                                                

  R2 --- Privacidad       Un pedido inexistente o perteneciente a otro        **PENDIENTE DE
                          cliente responde 404.                               VERIFICAR**
  -----------------------------------------------------------------------------------------------------

**Importante:** no dejes las celdas "PENDIENTE DE VERIFICAR" en la
entrega final. Busca las rutas y funciones reales del proyecto y
reemplaza esos textos. No conviene inventar nombres de archivos o
funciones porque el docente puede pedir que los muestres durante la
defensa.

## 5. Secretos y configuración

-   `.env`: contiene los valores reales de configuración y secretos. Se
    crea localmente y en EC2; no se sube al repositorio.
-   `.env.example`: debe estar versionado y contener todas las variables
    que requiere Compose, pero con valores ficticios o marcadores.
-   Auth0: el Client Secret y los datos sensibles de la aplicación se
    leen desde variables de entorno.
-   Django: `DJANGO_SECRET_KEY` se proporciona mediante el entorno.
-   PostgreSQL: usuario y contraseña se proporcionan mediante variables
    de entorno.

**PENDIENTE:** comprobar que `.env` está ignorado por Git (`.gitignore`)
y que no se incluyó ningún secreto en commits anteriores. Un secreto que
ya fue subido debe considerarse expuesto y rotarse; borrarlo en un
commit posterior no elimina el secreto del historial.

## 6. Requisitos previos

Para levantar el proyecto en otra máquina se necesita:

-   Git.
-   Docker Engine o Docker Desktop.
-   Docker Compose v2.
-   Acceso a las credenciales de configuración de Auth0.
-   Para reproducir el despliegue público: un servidor, DNS apuntando al
    servidor y acceso a los puertos 80 y 443.

## 7. Levantar el proyecto desde cero

### 7.1 Obtener el proyecto

``` bash
git clone <URL_DEL_REPOSITORIO>
cd LaCartaApp
```

### 7.2 Crear el archivo de entorno

``` bash
cp .env.example .env
```

Editar `.env` y colocar los valores reales de la máquina. No copiar los
secretos de ejemplo literalmente.

El `.env.example` debe incluir **todas las variables referenciadas por
`docker-compose.yml` y `docker-compose.prod.yml`**, entre ellas las de
PostgreSQL, conexión de base de datos, Flask, Auth0 y Django. Los
nombres exactos deben coincidir con los utilizados en los archivos
Compose y en el código.

### 7.3 Levantar el entorno local

``` bash
docker compose up -d --build
```

Comprobar los servicios:

``` bash
docker compose ps
docker compose logs -f
```

El servicio de migración debe terminar correctamente antes de que Flask
y Django queden disponibles.

### 7.4 Crear un superusuario de Django

``` bash
docker compose exec django python manage.py createsuperuser
```

### 7.5 Preparar Auth0

En Auth0 se debe configurar la aplicación y la API con RBAC y la
inclusión de permisos en el Access Token. Configurar los callback,
logout y web origins para el dominio local correspondiente. Crear
usuarios de prueba con los roles `cliente`, `cocina` y `admin`, y
asignarles los permisos definidos para el proyecto.

### 7.6 Despliegue de producción

El despliegue de EC2 utiliza el archivo `docker-compose.prod.yml` y el
`.env` de producción:

``` bash
docker compose --env-file .env -f docker-compose.prod.yml up -d --build
```

Comprobar:

``` bash
docker compose --env-file .env -f docker-compose.prod.yml ps
docker compose --env-file .env -f docker-compose.prod.yml logs --tail=100
```

Nginx debe publicar los puertos 80 y 443. Los DNS deben apuntar a la IP
pública del servidor y los certificados HTTPS deben estar disponibles
para ambos dominios.

### 7.7 Comandos útiles

``` bash
# Ver estado de los servicios
docker compose --env-file .env -f docker-compose.prod.yml ps

# Ver logs
docker compose --env-file .env -f docker-compose.prod.yml logs --tail=100

# Reiniciar los servicios
docker compose --env-file .env -f docker-compose.prod.yml up -d

# Ejecutar migraciones (normalmente las ejecuta el servicio migrate)
docker compose --env-file .env -f docker-compose.prod.yml run --rm migrate
```

No ejecutar `docker compose down -v` en un entorno con datos que se
quieran conservar: `-v` elimina los volúmenes nombrados.

## 8. Usuarios y datos de prueba

La aplicación utiliza tres usuarios de Auth0, uno por rol: `cliente`,
`cocina` y `admin`. El backoffice de Django utiliza además un
superusuario independiente, creado con `createsuperuser`.

La base de datos de producción fue poblada con datos de prueba. La carga
realizada creó 10 restaurantes, 190 platos, 200 pedidos y 600 ítems de
pedido (1.000 registros en total).

## 9. Pruebas

Ejecutar las pruebas automatizadas desde el entorno de desarrollo:

``` bash
pytest -q
```

El práctico solicita seis pruebas: creación sin sesión, intento de
cocina por parte de cliente, cálculo de total ignorando precios
manipulados, rechazo atómico de platos no disponibles, acceso a pedido
ajeno con 404 y rechazo de una transición inválida de estado.

**PENDIENTE DE VERIFICAR:** confirmar que las seis pruebas existen y
pasan en el repositorio actual. No afirmar que están aprobadas hasta
ejecutar `pytest -q` y revisar el resultado.

## 10. Pendientes y mejoras

Los siguientes puntos deben comprobarse antes de la entrega:

1.  **`.env.example`:** durante el desarrollo se confirmó que todavía no
    estaba creado. Añadirlo al repositorio con todas las variables
    necesarias y valores ficticios.
2.  **Renovación automática de Let's Encrypt:** los certificados HTTPS
    fueron emitidos para ambos subdominios, pero la renovación
    automática quedó pendiente de configurar y comprobar. Configurar el
    timer o cron y probar la renovación.
3.  **Mapa exacto de reglas:** completar la tabla de la sección 4 con
    los archivos y nombres reales de las funciones Flask después de
    revisar el código.
4.  **Pruebas automatizadas:** ejecutar `pytest -q` y registrar
    únicamente el resultado real.
5.  **Seguridad de secretos:** verificar `.gitignore` y el historial de
    Git para confirmar que nunca se subieron `.env`, contraseñas o el
    Client Secret de Auth0.

Como mejora futura, convendría documentar y automatizar la renovación de
certificados, y mantener una prueba de despliegue que compruebe que los
servicios esperan correctamente la finalización de las migraciones.

------------------------------------------------------------------------

## 11. Comprobación rápida para la defensa

-   [ ] La carta y el detalle de restaurantes funcionan sin iniciar
    sesión.
-   [ ] Un cliente puede crear un pedido y consultar solo sus pedidos.
-   [ ] Cocina puede avanzar el estado siguiendo las transiciones
    permitidas.
-   [ ] Un cliente puede cancelar únicamente un pedido pendiente propio.
-   [ ] Un cliente no puede abrir un pedido ajeno; recibe 404.
-   [ ] Django Admin permite filtrar pedidos, buscar clientes y ver
    ítems.
-   [ ] Los totales y precios de los ítems son de solo lectura en Django
    Admin.
-   [ ] PostgreSQL rechaza estados inválidos mediante las restricciones
    de base de datos.
-   [ ] `docker compose ps`, `sudo ss -tlnp` y `sudo nginx -t` muestran
    el despliegue esperado.
-   [ ] `pytest -q` termina correctamente.
-   [ ] Los certificados HTTPS y su renovación automática están
    comprobados.

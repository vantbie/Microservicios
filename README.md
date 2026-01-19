# Desafio de Microservicios

Este repositorio contiene la implementación de un sistema distribuido basado en una arquitectura de microservicios. El proyecto desacopla la lógica de negocio en servicios independientes (Usuarios, Productos, Órdenes) que se comunican con el exterior exclusivamente a través de un API Gateway centralizado, el cual gestiona la seguridad y la resiliencia del sistema.

## 1. Módulo: api_gateway
Esta carpeta contiene el código del servidor principal que actúa como intermediario entre el cliente y los microservicios.

* **app/main.py:**
    Es el punto de entrada de la aplicación Gateway. Inicializa la instancia de FastAPI, configura los middlewares (como CORS) e incluye los enrutadores definidos en la carpeta `routers`.

* **app/auth (Seguridad):**
    Contiene la lógica de protección del sistema.
    * Valida los encabezados `Authorization`.
    * Decodifica y verifica la firma de los tokens JWT.
    * Rechaza cualquier petición que no provenga de un usuario autenticado, protegiendo así a los microservicios internos de accesos no autorizados.

* **app/core (Resiliencia y Configuración):**
    Aquí reside la lógica de infraestructura crítica, específicamente el patrón **Circuit Breaker**.
    * Monitorea la salud de los microservicios externos.
    * Si detecta que un servicio (ej. Productos) está caído o responde lento, corta el tráfico hacia él para evitar tiempos de espera infinitos y fallos en cascada.

* **app/routers (Enrutamiento):**
    Define los endpoints públicos que el cliente consume.
    * No contiene lógica de negocio.
    * Su única función es recibir la petición HTTP, validar los datos con `models` y reenviarla al microservicio correspondiente mediante peticiones HTTP internas.

* **app/models (Esquemas de Datos):**
    Define las clases Pydantic (schemas) que validan la estructura de los datos (JSON) que entran y salen del Gateway. Asegura que si el cliente envía datos incompletos, el error se capture aquí antes de molestar a los microservicios.

## 2. Módulos de Servicio (Users, Products, Orders)
Los directorios `users_service`, `products_service` y `orders_service` comparten una estructura interna idéntica, diseñada para mantener la autonomía.

* **Data-base.db:**
    Es el archivo físico de la base de datos SQLite. Al estar ubicado en la raíz de la carpeta del servicio, se garantiza el aislamiento de datos (ningún otro servicio puede leer este archivo).

* **app/main.py:**
    Punto de entrada del microservicio específico. Levanta un servidor HTTP independiente en un puerto único, listo para escuchar las órdenes del Gateway.

* **app/database (Capa de Persistencia):**
    Maneja la conexión directa con el archivo `.db`.
    * Contiene la configuración de SQLAlchemy (engine y session).
    * Incluye las funciones para crear las tablas automáticamente si no existen al iniciar el servicio.

* **app/models (Modelos ORM):**
    Representa las tablas de la base de datos como clases de Python. Aquí se define la estructura de la información (columnas, tipos de datos, claves primarias) específica de ese dominio de negocio (ej. tabla `Usuarios`, tabla `Pedidos`).

* **app/routers (Lógica de Negocio):**
    Contiene los controladores reales de la aplicación.
    * Aquí se ejecutan las operaciones CRUD (Crear, Leer, Actualizar, Borrar).
    * Es el único lugar donde se realizan consultas directas a la base de datos a través de la sesión definida en `database`.

* **app/__init__.py:**
    Archivos vacíos o de configuración mínima que permiten a Python tratar a los directorios como paquetes importables, facilitando la modularización y las importaciones relativas entre archivos.

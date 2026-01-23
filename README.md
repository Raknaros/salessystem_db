# SalesSystem DB Manager

## Descripción del Proyecto
Sistema integral de gestión de información comercial y financiera desarrollado en Python utilizando el framework Streamlit. Este aplicativo actúa como un puente entre la gestión operativa (Pedidos) y la gestión contable (Facturación y Bancarización), permitiendo la administración eficiente de flujos de datos masivos y la integración con bases de datos relacionales (MySQL y PostgreSQL).

El objetivo principal es optimizar el ciclo de vida del pedido hasta su facturación y cobro, automatizando la generación de "pre-cuadros" y archivos de emisión masiva, reduciendo la carga operativa manual y minimizando errores en la información financiera.

## Arquitectura y Tecnologías

El proyecto sigue una arquitectura modular basada en servicios:

*   **Frontend:** [Streamlit](https://streamlit.io/) (Interfaz de usuario interactiva y reactiva).
*   **Backend Logic:** Python 3.10+.
*   **Manipulación de Datos:** [Pandas](https://pandas.pydata.org/) y [NumPy](https://numpy.org/) para procesamiento vectorial de grandes volúmenes de datos (ETL).
*   **ORM & Base de Datos:** [SQLAlchemy](https://www.sqlalchemy.org/) para la interacción con bases de datos MySQL (Sistema de Ventas) y PostgreSQL (Almacén/Warehouse).
*   **Manejo de Archivos:** `openpyxl` y `XlsxWriter` para la lectura y escritura avanzada de reportes en Excel.
*   **Autenticación:** `streamlit-authenticator` para gestión de sesiones y roles de usuario.

## Estructura del Proyecto

```text
D:/salessystem_db/
├── app.py                  # Punto de entrada de la aplicación (Login y Router)
├── config.yaml             # Configuración de credenciales y cookies
├── models.py               # Modelos de datos (ORM) definidos con SQLAlchemy
├── pages/                  # Módulos de la interfaz gráfica (Vistas)
│   ├── 0_home.py
│   ├── 2_cargar_pedidos.py
│   ├── 3_cargar_cotizaciones.py
│   └── 4_cargar_bancarizaciones.py
├── services/               # Lógica de negocio y acceso a datos
│   ├── Querys.py           # Conexiones a BD y consultas SQL
│   ├── PutPedidos.py       # Lógica de inserción de pedidos
│   ├── PutCotizaciones.py  # Procesamiento de cotizaciones
│   └── ...
└── requirements.txt        # Dependencias del proyecto
```

## Funcionalidades Principales

1.  **Gestión de Pedidos (`pages/2_cargar_pedidos.py`):**
    *   Visualización de pedidos pendientes y en proceso.
    *   Carga manual y masiva (Excel) de nuevos pedidos.
    *   Generación automática de "Pre-cuadros" basada en históricos de venta (`pre_detalle`) y catálogo de productos.

2.  **Gestión de Cotizaciones (`pages/3_cargar_cotizaciones.py`):**
    *   Carga de cotizaciones trabajadas para su integración en el sistema.
    *   Generación de archivos maestros para emisión de facturas ("Cuadro para Emitir"), agrupados por proveedor o pedido.
    *   Cálculo automático de detracciones, retenciones y fechas de vencimiento.

3.  **Bancarización (`pages/4_cargar_bancarizaciones.py`):**
    *   Registro y control de operaciones bancarias para sustento tributario.
    *   Cruce de información entre pagos y facturas relacionadas.

## Configuración e Instalación

### Prerrequisitos
*   Python 3.10 o superior.
*   Acceso a las bases de datos MySQL y PostgreSQL correspondientes.

### Instalación

1.  **Clonar el repositorio o descargar el código fuente.**
2.  **Crear un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuración de Credenciales

El sistema utiliza dos fuentes de configuración:

1.  **`config.yaml`:** Contiene la configuración de usuarios, contraseñas (hasheadas) y parámetros de cookies para la autenticación local.
2.  **Secrets (`.streamlit/secrets.toml`):** Debe contener las credenciales de acceso a las bases de datos. **No incluir este archivo en el control de versiones.**

Formato esperado en `secrets.toml`:
```toml
[DB_USERNAME_SS]
...
```

## Ejecución

Para iniciar el servidor de desarrollo:

```bash
streamlit run app.py
```

La aplicación estará disponible por defecto en `http://localhost:8501`.

## Flujo de Trabajo (Business Logic)

1.  **Pedido:** Se ingresa un requerimiento comercial.
2.  **Pre-cuadro:** El sistema sugiere los ítems a cotizar basándose en el historial del cliente (RUC).
3.  **Cotización:** El usuario completa precios y detalles en Excel y lo carga al sistema.
4.  **Emisión:** Se genera el reporte consolidado para que el área de facturación emita los comprobantes (Facturas/Guías).
5.  **Bancarización:** Se registran los pagos para cerrar el ciclo contable.

## Problemas Conocidos (Known Issues)

*   **Concurrencia en Prefetching:** Se ha detectado un error ocasional `Packet sequence number wrong` al iniciar sesión, relacionado con el uso de hilos secundarios para la pre-carga de datos (`prefetch_data`). Esto se debe a conflictos en el uso compartido de conexiones de base de datos (`pymysql`) entre el hilo principal y el hilo de pre-carga.
    *   *Estado:* En investigación.
    *   *Workaround:* Si el error persiste, se recomienda desactivar temporalmente la función `prefetch_data` en `app.py`.

---
*Nota: Este proyecto maneja información financiera sensible. Asegúrese de cumplir con las políticas de protección de datos y accesos.*

---
---

# SalesSystem DB Manager (English Version)

## Project Description
Comprehensive commercial and financial information management system developed in Python using the Streamlit framework. This application acts as a bridge between operational management (Orders) and accounting management (Invoicing and Bank Reconciliation), enabling efficient administration of massive data flows and integration with relational databases (MySQL and PostgreSQL).

The main objective is to optimize the order lifecycle up to invoicing and collection, automating the generation of "pre-charts" (pre-quotations) and bulk issuance files, reducing manual operational load and minimizing errors in financial information.

## Architecture and Technologies

The project follows a service-based modular architecture:

*   **Frontend:** [Streamlit](https://streamlit.io/) (Interactive and reactive user interface).
*   **Backend Logic:** Python 3.10+.
*   **Data Manipulation:** [Pandas](https://pandas.pydata.org/) and [NumPy](https://numpy.org/) for vector processing of large data volumes (ETL).
*   **ORM & Database:** [SQLAlchemy](https://www.sqlalchemy.org/) for interaction with MySQL (Sales System) and PostgreSQL (Warehouse) databases.
*   **File Handling:** `openpyxl` and `XlsxWriter` for advanced reading and writing of Excel reports.
*   **Authentication:** `streamlit-authenticator` for session and user role management.

## Project Structure

```text
D:/salessystem_db/
├── app.py                  # Application entry point (Login and Router)
├── config.yaml             # Credentials and cookie configuration
├── models.py               # Data models (ORM) defined with SQLAlchemy
├── pages/                  # GUI Modules (Views)
│   ├── 0_home.py
│   ├── 2_cargar_pedidos.py
│   ├── 3_cargar_cotizaciones.py
│   └── 4_cargar_bancarizaciones.py
├── services/               # Business logic and data access
│   ├── Querys.py           # DB connections and SQL queries
│   ├── PutPedidos.py       # Order insertion logic
│   ├── PutCotizaciones.py  # Quotation processing
│   └── ...
└── requirements.txt        # Project dependencies
```

## Main Functionalities

1.  **Order Management (`pages/2_cargar_pedidos.py`):**
    *   Visualization of pending and in-process orders.
    *   Manual and bulk (Excel) loading of new orders.
    *   Automatic generation of "Pre-charts" based on sales history (`pre_detalle`) and product catalog.

2.  **Quotation Management (`pages/3_cargar_cotizaciones.py`):**
    *   Loading of worked quotations for integration into the system.
    *   Generation of master files for invoice issuance ("Issuance Chart"), grouped by supplier or order.
    *   Automatic calculation of deductions (detracciones), withholdings (retenciones), and due dates.

3.  **Bank Reconciliation (`pages/4_cargar_bancarizaciones.py`):**
    *   Registration and control of banking operations for tax support.
    *   Cross-referencing between payments and related invoices.

## Configuration and Installation

### Prerequisites
*   Python 3.10 or higher.
*   Access to the corresponding MySQL and PostgreSQL databases.

### Installation

1.  **Clone the repository or download the source code.**
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Credentials Configuration

The system uses two configuration sources:

1.  **`config.yaml`:** Contains configuration for users, passwords (hashed), and cookie parameters for local authentication.
2.  **Secrets (`.streamlit/secrets.toml`):** Must contain database access credentials. **Do not include this file in version control.**

Expected format in `secrets.toml`:
```toml
[DB_USERNAME_SS]
...
```

## Execution

To start the development server:

```bash
streamlit run app.py
```

The application will be available by default at `http://localhost:8501`.

## Workflow (Business Logic)

1.  **Order:** A commercial requirement is entered.
2.  **Pre-chart:** The system suggests items to quote based on customer history (RUC).
3.  **Quotation:** The user completes prices and details in Excel and uploads it to the system.
4.  **Issuance:** A consolidated report is generated for the billing area to issue vouchers (Invoices/Guides).
5.  **Bank Reconciliation:** Payments are registered to close the accounting cycle.

## Known Issues

*   **Prefetching Concurrency:** An occasional `Packet sequence number wrong` error has been detected upon login, related to the use of secondary threads for data pre-loading (`prefetch_data`). This is due to conflicts in sharing database connections (`pymysql`) between the main thread and the pre-fetch thread.
    *   *Status:* Under investigation.
    *   *Workaround:* If the error persists, it is recommended to temporarily disable the `prefetch_data` function in `app.py`.

---
*Note: This project handles sensitive financial information. Ensure compliance with data protection and access policies.*

# **Proyecto Final: Votaciones Online**

**Equipo:** Los Refugiados

**Miembros:**

- Arleen Maritza Ferro Vasquez  
- Wilson Isaac Mamani Casilla  
- Jazmin Gabriela Perez Villasante  
- Cristhian David Huanca Olazabal  
- Sebastian Andres Mendoza Fernandez  
- Edilson Bonet Mamani Yucra  

---

## Especificación del Proyecto

El propósito de este proyecto es desarrollar una aplicación web de votaciones online que permita a los usuarios participar en procesos electorales de manera segura y eficiente.

### Funcionalidades

- **Interfaz gráfica de usuario**: Utilizando cualquier lenguaje, biblioteca o framework.  
- **Persistencia en bases de datos**: Soporte para MySQL, SQLite, MongoDB u otro sistema de bases de datos.  

### Objetivos

- **Facilitar el voto en línea:** Proporcionar una plataforma intuitiva y accesible para que los votantes puedan emitir su voto desde cualquier lugar y momento.  
- **Promover la transparencia:** Asegurar que todo el proceso sea transparente y verificable, permitiendo a los participantes y organizadores auditar y revisar los resultados.  
- **Mejorar la gestión electoral:** Ofrecer herramientas para la administración y supervisión de las votaciones, simplificando la organización y el conteo de votos.  
- **Garantizar la integridad y seguridad:** Implementar medidas robustas para asegurar que el proceso de votación sea seguro y que los resultados sean precisos y confiables.  

---

## Entregables

### Código Fuente y Documentación

- **Backend:** [Repositorio en GitHub](https://github.com/chuancao26/elecciones_online)  
- **Frontend:** [Repositorio en GitHub](https://github.com/helvetios16/eleccionFT)  

### Planificación de Tareas

La planificación de tareas de implementación se gestiona usando la herramienta Trello. Puedes ver el tablero con todas las tareas del proyecto en el siguiente enlace:  
[Sistema de Elecciones - Trello](https://trello.com/b/dr4vfErF/sistema-de-elecciones)  

### Documentación

- **Documento de requisitos de software actualizado:** [Requisitos](https://docs.google.com/document/d/14P_PVLfjSm_YSb5pkw98cLnqFf8kFPsR/edit?usp=sharing&ouid=103974025895514464791&rtpof=true&sd=true)  
- **Documento de arquitectura de software actualizado:** [Arquitectura](https://docs.google.com/document/d/1cbHVusBtsyzv-eA0EU2F89KYerfHQLAP/edit?usp=sharing&ouid=103974025895514464791&rtpof=true&sd=true)  

---

## Pipeline de Jenkins

### Descripción General

El pipeline de Jenkins está diseñado para automatizar la configuración y despliegue del proyecto. Incluye pasos para la instalación de dependencias, configuración de entornos, ejecución de análisis estáticos, migración de bases de datos y pruebas.

### Etapas del Pipeline

1. **Checkout del Código**
   - Se clonan los repositorios de GitHub para el backend y el frontend.

2. **Configuración del Entorno Virtual**
   - Se crea y activa un entorno virtual de Python para manejar las dependencias del backend.

3. **Instalación con Poetry**
   - Poetry se utiliza para instalar las dependencias definidas en `pyproject.toml`.

4. **Migraciones de Base de Datos**
   - Alembic aplica migraciones para sincronizar el esquema de la base de datos.

5. **Análisis de Código con SonarQube**
   - Se realiza un análisis estático del código usando SonarQube.

6. **Inicio del Servidor Backend**
   - El servidor FastAPI se lanza localmente.

7. **Instalación de Dependencias del Frontend**
   - Bun se utiliza para instalar las dependencias del frontend.

8. **Lanzamiento del Servidor Frontend**
   - Se inicia el servidor de desarrollo para el frontend.

9. **Pruebas Automatizadas**
   - Se ejecutan pruebas unitarias con Pytest.
   - Se realizan pruebas de rendimiento con JMeter.

---

## Requisitos Previos

1. **Herramientas Instaladas:**
   - Python 3.9+  
   - Poetry  
   - Alembic  
   - Jenkins  
   - SonarQube  
   - Bun  
   - Apache JMeter  

2. **Configuración de Jenkins:**
   - Plugin de Git instalado.  
   - Configuración del `tool` para SonarQube (`sonnar-scanner`).  
   - Definir credenciales para acceso a repositorios privados (si aplica).  

---

## Configuración del Proyecto

1. **Clonar los Repositorios**
   ```bash
   git clone https://github.com/chuancao26/elecciones_online
   git clone https://github.com/helvetios16/eleccionFT
2. **Configurar el Backend**
 - Crear y activar un entorno virtual:
   ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    venv\Scripts\activate     # En Windows
 - Instalar dependencias:
   ```bash
      pip install poetry
      poetry install
3. **Configurar el Frontend**
 - instalar las dependencias con Bun:
   ```bash
    bun install 
 - Iniciar el servidor:
   ```bash
   bun dev


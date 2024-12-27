# **Proyecto Final: Votaciones Online**

**Equipo:** Los Refugiados

**Miembros:**

- Arleen Maritza Ferro Vasquez  
- Wilson Isaac Mamani Casilla  
- Jazmin Gabriela Perez Villasante  
- Cristhian David Huanca Olazabal  
- Sebastian Andres Mendoza Fernandez  

---

## Especificación del Proyecto

El propósito de este proyecto es desarrollar una aplicación web de votaciones online que permita a los usuarios participar en procesos electorales de manera segura y eficiente.

### Funcionalidades

- **Interfaz gráfica de usuario**
- **Persistencia en bases de datos**

### Objetivos

- **Facilitar el voto en línea:** Proporcionar una plataforma intuitiva y accesible para que los votantes puedan emitir su voto desde cualquier lugar y momento.  
- **Promover la transparencia:** Asegurar que todo el proceso sea transparente y verificable, permitiendo a los participantes y organizadores auditar y revisar los resultados.  
- **Mejorar la gestión electoral:** Ofrecer herramientas para la administración y supervisión de las votaciones, simplificando la organización y el conteo de votos.  
- **Garantizar la integridad y seguridad:** Implementar medidas robustas para asegurar que el proceso de votación sea seguro y que los resultados sean precisos y confiables.  
#### Home
![image](https://github.com/user-attachments/assets/7800bc9a-11f6-4c9e-9c24-21d04e1a85c0)
#### Registro 
![image](https://github.com/user-attachments/assets/dab8c3e4-a2f5-47ab-8565-c9ceaf0e189c)
#### Login
![image](https://github.com/user-attachments/assets/748dbf87-67f7-41a4-9e9b-934c297dd621)
#### Elector Dashboard
![image](https://github.com/user-attachments/assets/0c8a7aee-659b-4c27-a35d-1ce69e9fd79e)
#### Admin Dashboard
![image](https://github.com/user-attachments/assets/50da105f-e7f5-4702-a87e-290fed3eb808)

---

## Entregables

### Código Fuente y Documentación

- **Backend:** [Repositorio en GitHub](https://github.com/chuancao26/elecciones_online)  
- **Frontend:** [Repositorio en GitHub](https://github.com/helvetios16/eleccionFT)  

### Planificación de Tareas

La planificación de tareas de implementación se gestiona usando la herramienta Projects de Github. Puedes ver el tablero con todas las tareas del proyecto en el siguiente enlace:  
[Sistema de Elecciones - Projects](https://github.com/users/chuancao26/projects/4)  
![image](https://github.com/user-attachments/assets/f9eefc39-2044-4ae6-b874-5ee3c8b10b65)


### Documentación

- **Documento de requisitos de software actualizado:** [Requisitos](https://docs.google.com/document/d/14P_PVLfjSm_YSb5pkw98cLnqFf8kFPsR/edit?usp=sharing&ouid=103974025895514464791&rtpof=true&sd=true)  
- **Documento de arquitectura de software actualizado:** [Arquitectura](https://docs.google.com/document/d/1cbHVusBtsyzv-eA0EU2F89KYerfHQLAP/edit?usp=sharing&ouid=103974025895514464791&rtpof=true&sd=true)  

---

## Tecnologías

### Backend
- **Lenguaje de Programación**: Python 3.10.10
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Migraciones de Base de Datos**: [Alembic](https://alembic.sqlalchemy.org/)
- **Base de Datos**: PostgreSQL
- **Gestor de Paquetes**: [Poetry](https://python-poetry.org/)

### Frontend
- **Framework**: [Astro](https://astro.build/)
- **Estilos CSS**: [TailwindCSS](https://tailwindcss.com/)
- **Gestor de Paquetes**: [Bun](https://bun.sh/)

## Herramientas de Construcción y Pruebas

- **Construcción del Backend**: Poetry facilita la gestión de dependencias y scripts personalizados para la construcción.
- **Construcción del Frontend**: Bun proporciona herramientas rápidas para la instalación de paquetes y scripts de construcción.
- **Pruebas del Backend**: Se recomienda usar `pytest` para escribir y ejecutar pruebas unitarias y de integración.
- **Pruebas del Frontend**: Astro incluye capacidades de pruebas y se pueden extender con bibliotecas como `vitest` o `jest`.


## Pipeline de Jenkins

El proyecto incluye un pipeline de CI/CD configurado para automatizar tareas clave en el desarrollo y despliegue. El pipeline está definido de la siguiente manera:

### Stages del Pipeline

1. **Checkout del Código**: Se clona el repositorio del backend y del frontend desde GitHub.

2. **Configuración del Entorno**:
   - Creación y activación de un entorno virtual con Python.

3. **Instalación de Dependencias con Poetry**:
   - Instalación del gestor de dependencias Poetry.
   - Instalación de las dependencias definidas en `pyproject.toml`.
   ```groovy
     stage('Poetry') {
            steps {
                bat '''
                REM Activar el entorno virtual
                call venv\\Scripts\\activate

                REM Instalar poetry
                pip install poetry

                REM Instalar las dependencias definidas en pyproject.toml
                poetry install
                '''
            }
        }
   ```

4. **Migraciones de Base de Datos**:
   - Ejecución de migraciones de base de datos utilizando Alembic para asegurar que la base de datos esté actualizada.
   - Se ejecuta el comando call venv\Scripts\activate para activar el entorno virtual Python ubicado en la carpeta venv. Esto asegura que se usen las dependencias y configuraciones específicas del proyecto.

   - El comando alembic upgrade head se utiliza para migrar la base de datos a la versión más reciente definida en los archivos de migración de Alembic. Esto aplica los cambios necesarios a la estructura de la base de datos, como la creación, eliminación o modificación de tablas y columnas, de acuerdo con las migraciones definidas.
     ```groovy
        stage('alembic') {
            steps {
                bat '''
                REM Activar el entorno virtual
                call venv\\Scripts\\activate

                REM Migrar la base de datos a la versión más reciente
                alembic upgrade head
                '''
            }
        }
   ```

5. **Ejecución de Pruebas con Pytest**:
   - Ejecución de pruebas unitarias y generación de un reporte de cobertura de código.
   - Utiliza el comando git para clonar el repositorio desde la URL https://github.com/chuancao26/elecciones_online y cambiar a la rama desarrollo_API. Esto asegura que se trabaja con la versión específica del código en desarrollo.
   - Ejecuta el comando call venv\Scripts\activate para habilitar el entorno virtual Python del proyecto, garantizando que las dependencias necesarias estén disponibles.
   - Se utiliza coverage run -m pytest para ejecutar las pruebas definidas en el proyecto con pytest. Además de realizar las pruebas, coverage mide cuánto del código fuente está siendo cubierto por estas pruebas.
   - Ejecuta el comando coverage xml, que produce un archivo XML con los detalles del reporte de cobertura de código. Este archivo puede ser utilizado por otras herramientas para analizar y visualizar la cobertura.
   ```groovy
        stage('pytest') {
            steps {
                git branch: 'desarrollo_API', url: 'https://github.com/chuancao26/elecciones_online'
                bat '''
                REM Activar el entorno virtual
                call venv\\Scripts\\activate

                REM Ejecutar pytest en el archivo de prueba
                coverage run -m pytest
                coverage xml
                '''
            }
        }
   ```

6. **Análisis de Calidad de Código con SonarQube**:
   - Configuración y ejecución del análisis estático del código para detectar errores y medir calidad.
   - -Dsonar.url=http://localhost:9000/: Especifica la URL del servidor de SonarQube donde se subirán los resultados del análisis.
-Dsonar.login=sqa_38f523eff0fe2cc5a1fd3658ae51769277f3bf09: Proporciona el token de autenticación necesario para conectar con el servidor.
-Dsonar.projectKey=eleccion_online: Define una clave única para identificar el proyecto en SonarQube.
-Dsonar.projectName=eleccion_online: Especifica el nombre del proyecto que aparecerá en la interfaz de SonarQube.
-Dsonar.python.coverage.reportPaths=coverage.xml: Proporciona el archivo coverage.xml generado por pytest para analizar la cobertura del código Python.
-Dsonar.sources=.: Indica que el código fuente a analizar está en el directorio actual.
-Dsonar.python.version=3.10.10: Especifica la versión de Python utilizada en el proyecto para que el análisis esté alineado con las configuraciones del entorno.
   ```groovy
        stage("SonarQube Analysis") {
            steps {
                bat """
                    $SCANNER_HOME/bin/sonar-scanner ^
                    -Dsonar.url=http://localhost:9000/ ^
                    -Dsonar.login=sqa_38f523eff0fe2cc5a1fd3658ae51769277f3bf09 ^
                    -Dsonar.projectKey=eleccion_online ^
                    -Dsonar.projectName=eleccion_online ^
                    -Dsonar.python.coverage.reportPaths=coverage.xml ^
                    -Dsonar.sources=. ^
                    -Dsonar.python.version=3.10.10 ^
                """
            }
        }
   ```
![image](https://github.com/user-attachments/assets/762f8cea-4fd4-4d2e-9199-bf1d23b24ab8)

7. **Inicio del Servidor FastAPI**:
   - Inicia el servidor de desarrollo del backend con Uvicorn en segundo plano.
   ```groovy
        stage('Start FastAPi Server') {
            steps {
                script {
                    bat '''
                        call venv\\Scripts\\activate
                        start /B uvicorn app.main:app --reload
                    '''
                }
                sleep time: 10, unit: 'SECONDS'
            }
        }
   ```

8. **Preparación del Frontend**:
   - Clonación del repositorio del frontend y ejecución del comando `bun install` para instalar dependencias.
   ```groovy
        stage('instalacion de dependencias') {
            steps {
                bat '''
                REM Instalar dependencias usando bun
                bun install
                '''
            }
        }
   ```
9. **Pruebas de Rendimiento con JMeter**:
    - Ejecución de pruebas de rendimiento utilizando JMeter y generación de reportes.
   ```groovy
        stage('Jmeter test') {
            steps {
                git branch: 'desarrollo_API', url: 'https://github.com/chuancao26/elecciones_online'
                bat '''
                REM Iniciando JMeter test
                C:\\Users\\USER\\Downloads\\apache-jmeter-5.6.3\\bin\\jmeter -Jmeter.save.saveservice.output_format=xml -n -t "performance_Jmeter.jmx" -l results.jtl
                '''
            }
        }
   ```

10. **Publicación del Reporte de JMeter**:
    - Publicación de los resultados de las pruebas de rendimiento en el pipeline.
   ```groovy
        stage('Publish Jmeter Report') {
            steps {
                perfReport filterRegex: '', sourceDataFiles: '**/*.jtl'
            }
        }
   ```

11. **Verificación de Vulnerabilidades con OWASP Dependency-Check**:
    - Análisis de las dependencias del proyecto para identificar vulnerabilidades de seguridad conocidas.
   ```groovy
        stage('OWASP Dependency-Check Vulnerabilities') {
            steps {
                dependencyCheck additionalArguments: '''
                        -o './'
                        -s './'
                        -f 'ALL'
                        --prettyPrint''', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
                dependencyCheckPublisher pattern: 'dependency-check-report.xml'
            }
        }
   ```

### Definición del Pipeline

```groovy
pipeline {
    agent any

    environment {
        SCANNER_HOME = tool 'sonnar-scanner'
    }

    stages {
        stage('checkout') {
            steps {
                checkout scmGit(branches: [[name: 'desarrollo_API']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/chuancao26/elecciones_online']])
            }
        }

        stage('entorno') {
            steps {
                bat '''
                REM Crear el entorno virtual
                python -m venv venv

                REM Activar el entorno virtual
                venv\\Scripts\\activate
                '''
            }
        }

        stage('Poetry') {
            steps {
                bat '''
                REM Activar el entorno virtual
                call venv\\Scripts\\activate

                REM Instalar poetry
                pip install poetry

                REM Instalar las dependencias definidas en pyproject.toml
                poetry install
                '''
            }
        }

        stage('alembic') {
            steps {
                bat '''
                REM Activar el entorno virtual
                call venv\\Scripts\\activate

                REM Migrar la base de datos a la versión más reciente
                alembic upgrade head
                '''
            }
        }

        stage('pytest') {
            steps {
                git branch: 'desarrollo_API', url: 'https://github.com/chuancao26/elecciones_online'
                bat '''
                REM Activar el entorno virtual
                call venv\\Scripts\\activate

                REM Ejecutar pytest en el archivo de prueba
                coverage run -m pytest
                coverage xml
                '''
            }
        }

        stage("SonarQube Analysis") {
            steps {
                bat """
                    $SCANNER_HOME/bin/sonar-scanner ^
                    -Dsonar.url=http://localhost:9000/ ^
                    -Dsonar.login=sqa_38f523eff0fe2cc5a1fd3658ae51769277f3bf09 ^
                    -Dsonar.projectKey=eleccion_online ^
                    -Dsonar.projectName=eleccion_online ^
                    -Dsonar.python.coverage.reportPaths=coverage.xml ^
                    -Dsonar.sources=. ^
                    -Dsonar.python.version=3.10.10 ^
                """
            }
        }

        stage('Start FastAPi Server') {
            steps {
                script {
                    bat '''
                        call venv\\Scripts\\activate
                        start /B uvicorn app.main:app --reload
                    '''
                }
                sleep time: 10, unit: 'SECONDS'
            }
        }

        stage('front end') {
            steps {
                checkout scmGit(branches: [[name: 'main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/helvetios16/eleccionFT.git']])    
            }
        }

        stage('instalacion de dependencias') {
            steps {
                bat '''
                REM Instalar dependencias usando bun
                bun install
                '''
            }
        }

        stage('lanzamiento-frontend') {
            steps {
                git branch: 'main', url: 'https://github.com/helvetios16/eleccionFT'
                bat '''
                REM Lanzar el servidor de desarrollo del front-end en segundo plano
                start /B bun dev --detach
                '''
                sleep time: 10, unit: 'SECONDS'
            }
        }

        stage('Jmeter test') {
            steps {
                git branch: 'desarrollo_API', url: 'https://github.com/chuancao26/elecciones_online'
                bat '''
                REM Iniciando JMeter test
                C:\\Users\\USER\\Downloads\\apache-jmeter-5.6.3\\bin\\jmeter -Jmeter.save.saveservice.output_format=xml -n -t "performance_Jmeter.jmx" -l results.jtl
                '''
            }
        }

        stage('Publish Jmeter Report') {
            steps {
                perfReport filterRegex: '', sourceDataFiles: '**/*.jtl'
            }
        }

        stage('OWASP Dependency-Check Vulnerabilities') {
            steps {
                dependencyCheck additionalArguments: '''
                        -o './'
                        -s './'
                        -f 'ALL'
                        --prettyPrint''', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
                dependencyCheckPublisher pattern: 'dependency-check-report.xml'
            }
        }
    }
}
```

Este pipeline asegura un flujo de trabajo eficiente y confiable para la integración y despliegue continuo del proyecto.

![image](https://github.com/user-attachments/assets/dd2cff6c-89b5-46a1-9848-9f83edb1ce5e)
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


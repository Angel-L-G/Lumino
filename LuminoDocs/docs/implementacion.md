## Implementación

### Estructura del código

- **Modelo**: Tablas de la base de datos en clases de python.
- **Vista**: Procesador de las peticiones para devolver una respuesta en formato plantilla.
- **Plantilla**: Interfaz para que el usuario pueda interactuar con las distintas funcionalidades.

### Tecnologías y herramientas

- **Lenguajes**: Python (Django).
- **Base de datos**: sqlite 3.
- **Autenticación**: La autenticación del propio django.
- **Cola de mensajes**: Redis.

### Instrucciones de configuración

1. Clonar el repositorio:

```bash
	git clone https://github.com/Angel-L-G/Lumino
```

2. Instalar dependencias:

```bash
	pip install -r requirements.txt
```

3. Configurar el entorno virtual:

```bash
	python -m venv .venv --prompt [Nombre del proyecto]
	source .venv/bin/activate
	# para desactivar el entorno
	deactivate
```

4. Configurar variables de entorno:

```
	EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
```

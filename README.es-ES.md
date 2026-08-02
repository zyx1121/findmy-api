# findmy-api

> Pregunta "dónde está mi AirTag" por HTTP en lugar de abrir la app Find My.

`findmy` · `airtag` · `macos` · `fastapi` · `rest-api`

[![version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fzyx1121%2Ffindmy-api%2Fmain%2Fpyproject.toml&query=%24.tool.poetry.version&label=version&color=111111)](pyproject.toml) &nbsp;[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](#license)

```
$ curl http://127.0.0.1:8000/items
["Keys","iPhone"]

$ curl http://127.0.0.1:8000/items/Keys/location
{"latitude":25.033,"longitude":121.5654,"altitude":12.3,"timestamp":"2024-12-19T10:15:00"}
```

<sub>Lista lo que Find My está rastreando y luego obtiene la última ubicación conocida de un elemento.</sub>

Apple no ofrece una API oficial de Find My: sin clave, sin endpoint, nada. Este proyecto lee el mismo archivo de caché que la app Find My ya escribe en macOS y lo vuelve a servir como un pequeño servicio HTTP local, de modo que cualquier script o aplicación en la red pueda consultar la ubicación o dirección de un elemento en lugar de abrir Find My manualmente.

## Inicio rápido

```bash
git clone https://github.com/zyx1121/findmy-api.git
cd findmy-api
poetry install
poetry run uvicorn findmy_api.main:app --host 0.0.0.0 --port 8000 --reload
```

La documentación interactiva viene incluida: Swagger UI en `/docs`, ReDoc en `/redoc`.

## Qué te ofrece

- **Listar** cada elemento que Find My está rastreando actualmente
- **Localizar** un elemento: latitud, longitud, altitud y cuándo se tomó la posición
- **Resolver** la última dirección conocida de un elemento

## Endpoints

| Método | Ruta | Devuelve |
|--------|------|----------|
| `GET` | `/items` | `list[str]`: nombres de cada elemento encontrado en la caché local |
| `GET` | `/items/{item_name}/location` | `Location`: `latitude`, `longitude`, `altitude`, `timestamp` |
| `GET` | `/items/{item_name}/address` | `Address`: `country`, `administrative_area`, `locality`, `street_name`, `street_address`, `map_item_full_address` |

> [!NOTA]
> Llama a `GET /items` al menos una vez primero. Los nombres de los elementos solo se reconocen en `/location` y `/address` después de que `/items` haya poblado la lista interna de elementos; llamar a cualquiera de los dos endpoints sin haberlo hecho antes devuelve un 404.

## Cómo funciona

macOS escribe la última posición conocida de cada elemento emparejado en `~/Library/Caches/com.apple.findmy.fmipcore/Items.data`. Este servicio carga ese JSON en la primera solicitud y responde las consultas directamente contra él, sin daemon, sin llamadas a los servidores de Apple.

> [!ADVERTENCIA]
>
> - Requisito del sistema: solo compatible con macOS 14.3.1 o anterior. Las versiones más recientes de macOS cifran el archivo de caché y este proyecto no puede analizarlo.
> - Necesita permisos de lectura del sistema de archivos sobre el archivo de caché mencionado.
> - Los datos solo están tan actualizados como la última escritura en la caché de Find My, no hay sondeo en tiempo real.

## Aviso legal

Solo para fines educativos y de investigación. El autor no se hace responsable del uso indebido o daños, no garantiza la exactitud de los datos y no está afiliado con Apple Inc. El uso de este software significa usarlo bajo tu propio riesgo, cumpliendo con los términos de servicio de Apple y respetando la privacidad del usuario y las leyes de protección de datos.

## Contribuir

Se aceptan incidencias y solicitudes de extracción: comienza con [CONTRIBUTING.md](https://github.com/zyx1121/.github/blob/main/CONTRIBUTING.md).

## Licencia

[MIT](LICENSE) · lee un archivo de caché al que Apple nunca quiso que accedieras

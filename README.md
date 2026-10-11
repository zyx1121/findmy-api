<div align="center">

<h1>findmy-api</h1>

<p><strong>Your AirTag and Find My item locations as a local HTTP API on macOS.</strong></p>

[![Python](https://img.shields.io/badge/python-3.12%2B-3776ab?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![macOS](https://img.shields.io/badge/macOS-14.3.1_or_earlier-000000?style=flat-square&logo=apple)](#limits)
[![License](https://img.shields.io/github/license/zyx1121/findmy-api?style=flat-square)](LICENSE)

**English** | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md)

</div>

```console
$ curl http://127.0.0.1:8000/items
["Keys","iPhone"]

$ curl http://127.0.0.1:8000/items/Keys/location
{"latitude":25.033,"longitude":121.5654,"altitude":12.3,"timestamp":"2024-12-19T10:15:00"}
```

Apple has no official Find My API. findmy-api reads the cache file that the Find My app writes on macOS. It serves that data over HTTP, so a script can ask where an item is.

> [!WARNING]
> It works only on macOS 14.3.1 or earlier. Later versions encrypt the cache file, and findmy-api cannot read it.

## Features

- **Lists your items**: the name of every item that Find My tracks.
- **Locates an item**: latitude, longitude, altitude and the time of the last fix.
- **Resolves an address**: the last known street address of an item.

## Quick start

```sh
git clone https://github.com/zyx1121/findmy-api && cd findmy-api
poetry install
poetry run uvicorn findmy_api.main:app --port 8000
```

In a second terminal, run `curl http://127.0.0.1:8000/items`. You should see the names of your Find My items.

## Usage

| Method | Path | Returns |
|--------|------|---------|
| `GET` | `/items` | the names of all items in the cache |
| `GET` | `/items/{name}/location` | `latitude`, `longitude`, `altitude`, `timestamp` |
| `GET` | `/items/{name}/address` | `country`, `administrative_area`, `locality`, `street_name`, `street_address`, `map_item_full_address` |

Call `/items` first after each start. Until then, `/location` and `/address` return 404 for every name. Swagger UI is at `/docs`.

To reach it from other machines, add `--host 0.0.0.0`. The API has no authentication, so do this only on a network that you trust.

## How it works

macOS writes the last known position of each item to `~/Library/Caches/com.apple.findmy.fmipcore/Items.data`. findmy-api reads that file on the first request and keeps it in memory. It sends nothing to Apple.

## Limits

- macOS 14.3.1 or earlier only. Later versions encrypt `Items.data`.
- The data is as old as the last write by the Find My app. Restart the service to read a newer file.
- The user that runs the service must be able to read the cache file.

## For AI agents

Structured facts for coding agents and LLM tools.

```yaml
name: findmy-api
summary: FastAPI service that serves the macOS Find My cache file (Items.data) as JSON over HTTP.
type: service
interfaces:
  cli: none
  mcp: none
  http: http://127.0.0.1:8000 (GET /items, /items/{name}/location, /items/{name}/address, OpenAPI at /openapi.json)
install: poetry install
run: poetry run uvicorn findmy_api.main:app --port 8000
verify: curl -s http://127.0.0.1:8000/items
config: []
secrets: [none, but the responses contain the location of every item, and the API has no authentication]
limits: [macOS 14.3.1 or earlier, reads Items.data once per process, call /items before /location or /address]
```

## Development

```sh
poetry install
poetry run uvicorn findmy_api.main:app --port 8000 --reload
```

Use black and isort, both dev dependencies, to format the code. There is no CI and there are no tests yet.

## Disclaimer

For education and research only. This project is not affiliated with Apple Inc. You are responsible for compliance with Apple's terms and with privacy law.

## License

[MIT](LICENSE)

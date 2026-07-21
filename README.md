# findmy-api

> Ask "where's my AirTag" over HTTP instead of opening the Find My app.

`findmy` · `airtag` · `macos` · `fastapi` · `rest-api`

[![version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fzyx1121%2Ffindmy-api%2Fmain%2Fpyproject.toml&query=%24.tool.poetry.version&label=version&color=111111)](pyproject.toml) &nbsp;[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](#license)

```
$ curl http://127.0.0.1:8000/items
["Keys","iPhone"]

$ curl http://127.0.0.1:8000/items/Keys/location
{"latitude":25.033,"longitude":121.5654,"altitude":12.3,"timestamp":"2024-12-19T10:15:00"}
```

<sub>List what Find My is tracking, then pull one item's last known fix.</sub>

Apple does not ship an official Find My API: no key, no endpoint, nothing. This project reads the same cache file the Find My app already writes to on macOS and re-serves it as a small local HTTP service, so any script or app on the network can ask for an item's location or address instead of opening Find My by hand.

## Quickstart

```bash
git clone https://github.com/zyx1121/findmy-api.git
cd findmy-api
poetry install
poetry run uvicorn findmy_api.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive docs come free: Swagger UI at `/docs`, ReDoc at `/redoc`.

## What it gives you

- **List** every item Find My is currently tracking
- **Locate** an item: latitude, longitude, altitude, and when the fix was taken
- **Resolve** an item's last known street address

## Endpoints

| Method | Path | Returns |
|--------|------|---------|
| `GET` | `/items` | `list[str]`: names of every item found in the local cache |
| `GET` | `/items/{item_name}/location` | `Location`: `latitude`, `longitude`, `altitude`, `timestamp` |
| `GET` | `/items/{item_name}/address` | `Address`: `country`, `administrative_area`, `locality`, `street_name`, `street_address`, `map_item_full_address` |

> [!NOTE]
> Call `GET /items` at least once first. Item names are only recognized by `/location` and `/address` after `/items` has populated the internal item list; calling either endpoint cold returns a 404.

## How it works

macOS writes each paired item's last known position to `~/Library/Caches/com.apple.findmy.fmipcore/Items.data`. This service loads that JSON on first request and answers lookups against it directly, no daemon, no calls out to Apple's servers.

> [!WARNING]
>
> - System requirement: only supports macOS 14.3.1 or earlier. Newer macOS versions encrypt the cache file and this project cannot parse it.
> - Needs local file-system read permission on the cache file above.
> - Data is only as fresh as the last Find My cache write, there is no live polling.

## Disclaimer

For educational and research purposes only. The author takes no responsibility for misuse or damages, makes no guarantee about data accuracy, and is not affiliated with Apple Inc. Using this software means using it at your own risk, complying with Apple's terms of service, and respecting user privacy and data protection laws.

## Contributing

Issues and PRs welcome: start with [CONTRIBUTING.md](https://github.com/zyx1121/.github/blob/main/CONTRIBUTING.md).

## License

[MIT](LICENSE) · reads a cache file Apple never meant you to see

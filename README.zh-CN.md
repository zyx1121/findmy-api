<!-- 翻译自 README.md @ docs/readme-template-v2。只翻译 "For AI agents" 之前的章节，英文版更新时一起改。 -->

<div align="center">

<h1>findmy-api</h1>

<p><strong>把 AirTag 和“查找”里物品的位置，变成 macOS 上的本地 HTTP API。</strong></p>

[![Python](https://img.shields.io/badge/python-3.12%2B-3776ab?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![macOS](https://img.shields.io/badge/macOS-14.3.1_or_earlier-000000?style=flat-square&logo=apple)](#限制)
[![License](https://img.shields.io/github/license/zyx1121/findmy-api?style=flat-square)](LICENSE)

[English](README.md) | [繁體中文](README.zh-TW.md) | **简体中文**

</div>

```console
$ curl http://127.0.0.1:8000/items
["Keys","iPhone"]

$ curl http://127.0.0.1:8000/items/Keys/location
{"latitude":25.033,"longitude":121.5654,"altitude":12.3,"timestamp":"2024-12-19T10:15:00"}
```

Apple 没有官方的“查找”API。findmy-api 读取“查找”App 在 macOS 上写入的缓存文件，再通过 HTTP 提供数据，让程序可以直接查询物品在哪里。

> [!WARNING]
> 只支持 macOS 14.3.1 及更早的版本。之后的版本会加密缓存文件，findmy-api 无法读取。

## 功能

- **列出物品**：“查找”追踪的所有物品名称。
- **查询位置**：纬度、经度、海拔，以及最后一次定位的时间。
- **查询地址**：物品最后已知的街道地址。

## 快速开始

```sh
git clone https://github.com/zyx1121/findmy-api && cd findmy-api
poetry install
poetry run uvicorn findmy_api.main:app --port 8000
```

在另一个终端执行 `curl http://127.0.0.1:8000/items`，应该会看到你在“查找”里的物品名称。

## 使用方法

| 方法 | 路径 | 返回 |
|------|------|------|
| `GET` | `/items` | 缓存里所有物品的名称 |
| `GET` | `/items/{name}/location` | `latitude`、`longitude`、`altitude`、`timestamp` |
| `GET` | `/items/{name}/address` | `country`、`administrative_area`、`locality`、`street_name`、`street_address`、`map_item_full_address` |

每次启动后要先调用一次 `/items`。在那之前，`/location` 和 `/address` 对所有名称都会返回 404。Swagger UI 在 `/docs`。

要让其他机器访问，加上 `--host 0.0.0.0`。这个 API 没有鉴权，只在信任的网络上这样做。

## 工作原理

macOS 会把每个物品最后的位置写入 `~/Library/Caches/com.apple.findmy.fmipcore/Items.data`。findmy-api 在第一次请求时读取这个文件，之后都使用内存里的数据，不会向 Apple 发送任何内容。

## 限制

- 只支持 macOS 14.3.1 及更早的版本，之后的版本会加密 `Items.data`。
- 数据只会和“查找”App 最后一次写入一样新。要读取新文件需要重启服务。
- 运行服务的用户必须能读取缓存文件。

## 其他

给 AI agent 的结构化信息与开发说明见[英文版](README.md#for-ai-agents)。

## 免责声明

仅供教育与研究用途。本项目与 Apple Inc. 无关。使用者需自行遵守 Apple 的条款与隐私相关法律。

## 许可证

[MIT](LICENSE)

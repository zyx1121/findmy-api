<!-- 翻譯自 README.md @ docs/readme-template-v2。只翻 "For AI agents" 以上的章節，英文版更新時一起改。 -->

<div align="center">

<h1>findmy-api</h1>

<p><strong>把 AirTag 和「尋找」裡物品的位置，變成 macOS 上的本機 HTTP API。</strong></p>

[![Python](https://img.shields.io/badge/python-3.12%2B-3776ab?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![macOS](https://img.shields.io/badge/macOS-14.3.1_or_earlier-000000?style=flat-square&logo=apple)](#限制)
[![License](https://img.shields.io/github/license/zyx1121/findmy-api?style=flat-square)](LICENSE)

[English](README.md) | **繁體中文** | [简体中文](README.zh-CN.md)

</div>

```console
$ curl http://127.0.0.1:8000/items
["Keys","iPhone"]

$ curl http://127.0.0.1:8000/items/Keys/location
{"latitude":25.033,"longitude":121.5654,"altitude":12.3,"timestamp":"2024-12-19T10:15:00"}
```

Apple 沒有官方的「尋找」API。findmy-api 讀取「尋找」App 在 macOS 上寫入的快取檔，再透過 HTTP 提供資料，讓程式可以直接問物品在哪裡。

> [!WARNING]
> 只支援 macOS 14.3.1 以前的版本。之後的版本會加密快取檔，findmy-api 讀不到。

## 功能

- **列出物品**：「尋找」追蹤的所有物品名稱。
- **查位置**：緯度、經度、高度，以及最後一次定位的時間。
- **查地址**：物品最後已知的街道地址。

## 快速開始

```sh
git clone https://github.com/zyx1121/findmy-api && cd findmy-api
poetry install
poetry run uvicorn findmy_api.main:app --port 8000
```

在另一個終端機執行 `curl http://127.0.0.1:8000/items`，應該會看到你在「尋找」裡的物品名稱。

## 使用方式

| 方法 | 路徑 | 回傳 |
|------|------|------|
| `GET` | `/items` | 快取裡所有物品的名稱 |
| `GET` | `/items/{name}/location` | `latitude`、`longitude`、`altitude`、`timestamp` |
| `GET` | `/items/{name}/address` | `country`、`administrative_area`、`locality`、`street_name`、`street_address`、`map_item_full_address` |

每次啟動後要先呼叫一次 `/items`。在那之前，`/location` 和 `/address` 對所有名稱都會回 404。Swagger UI 在 `/docs`。

要讓其他機器連線，加上 `--host 0.0.0.0`。這個 API 沒有驗證，只在信任的網路上這樣做。

## 運作方式

macOS 會把每個物品最後的位置寫進 `~/Library/Caches/com.apple.findmy.fmipcore/Items.data`。findmy-api 在第一次請求時讀取這個檔案，之後都用記憶體裡的資料，不會傳任何東西給 Apple。

## 限制

- 只支援 macOS 14.3.1 以前的版本，之後的版本會加密 `Items.data`。
- 資料只會跟「尋找」App 最後一次寫入一樣新。要讀新的檔案得重啟服務。
- 執行服務的使用者必須能讀取快取檔。

## 其他

給 AI agent 的結構化資訊與開發說明在[英文版](README.md#for-ai-agents)。

## 免責聲明

僅供教育與研究用途。本專案與 Apple Inc. 無關。使用者須自行遵守 Apple 的條款與隱私相關法律。

## 授權

[MIT](LICENSE)

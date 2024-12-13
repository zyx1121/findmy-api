# FindMy Items API

A FastAPI-based REST API service for tracking Apple Find My Items location information, including AirTag, AirPods, and other Find My Items.

## Project Background

Apple does not provide an official Find My API interface, primarily due to the following considerations:

- Security: Prevent malicious programs from accessing location information
- Ecosystem: Maintain exclusive connections between Apple devices
- Privacy Protection: Ensure confidentiality of user location data

## Solution

This project implements Find My functionality extension through:

1. Direct reading of Find My cache files in macOS system:

```bash
~/Library/Caches/com.apple.findmy.fmipcore/Items.data
```

2. Converting cache data into standardized API format

3. Providing cross-platform access capability through HTTP protocol

> [!WARNING]
>
> - System Requirements: Only supports macOS 14.3.1 or earlier versions
> - Access Permissions: Requires local file system read permissions
> - Update Frequency: Depends on system cache update cycle

## Environment Requirements

- `Poetry`: Python dependency management tool
- macOS system (14.3.1 or earlier)
- Find My cache file access permissions

## Quick Start

1. Clone the project:

```bash
git clone https://github.com/zyx1121/findmy-api.git
cd findmy-api
```

2. Install dependencies:

```bash
poetry install
```

3. Start the service:

```bash
poetry run uvicorn findmy_api.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Documentation

Two interactive API documentation interfaces are provided:

- Swagger UI: `http://127.0.0.1:8000/docs`

  - Suitable for developer testing and interaction
  - Provides real-time API testing functionality

- ReDoc: `http://127.0.0.1:8000/redoc`

  - Provides clearer documentation reading experience
  - Suitable for API documentation reference

## DISCLAIMER

This project is for educational and research purposes only. The author:

- Takes no responsibility for any misuse or damages
- Does not guarantee the accuracy or reliability of the data
- Is not affiliated with Apple Inc.
- Makes no warranties regarding the use of this software

By using this software, you acknowledge that:

- You are using it at your own risk
- You will comply with Apple's terms of service
- You will respect user privacy and data protection laws
- You understand this is not an official Apple product

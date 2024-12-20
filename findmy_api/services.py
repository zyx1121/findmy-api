import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import HTTPException

from .models import Address, Location

logger = logging.getLogger("uvicorn.error")


class FindMyItem:
    def __init__(self):
        self.items: Dict[str, Optional[Location]] = {}
        self.data_path = os.path.join(
            os.path.expanduser("~"),
            "Library/Caches/com.apple.findmy.fmipcore/Items.data",
        )
        self.raw_data = None

    def _load_data(self) -> None:
        """Load Items.data file"""
        if self.raw_data is not None:
            return

        try:
            with open(self.data_path, "r") as f:
                try:
                    self.raw_data = json.load(f)
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    error_msg = (
                        "Unable to parse Find My data. This might be due to "
                        "encryption in newer macOS versions (>14.3.1). Please "
                        "ensure you're using a compatible macOS version."
                    )
                    logger.error(error_msg)
                    raise HTTPException(status_code=500, detail=error_msg)
        except FileNotFoundError:
            error_msg = "Find My cache file not found. Please ensure Find My is enabled on your system."
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        except PermissionError:
            error_msg = "Permission denied when accessing Find My cache file."
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)

    def _get_item_data(self, name: str) -> dict:
        """Get the data of a specific item"""
        for item in self.raw_data:
            if item.get("name") == name:
                return item
        raise ValueError(f"Cannot find the item: {name}")

    def get_address(self, name: str) -> Address:
        """Get the address of a specific item"""
        if name not in self.items:
            raise ValueError(f"Invalid item name: {name}")

        item_data = self._get_item_data(name)
        address_data = item_data.get("address", {})

        return Address(
            country=address_data.get("country", ""),
            administrative_area=address_data.get("administrativeArea", ""),
            locality=address_data.get("locality", ""),
            street_name=address_data.get("streetName") or "",
            street_address=address_data.get("streetAddress") or "",
            map_item_full_address=address_data.get("mapItemFullAddress", ""),
        )

    def get_location(self, name: str) -> Location:
        """Get the location of a specific item"""
        if name not in self.items:
            raise ValueError(f"Invalid item name: {name}")

        item_data = self._get_item_data(name)
        location_data = item_data.get("location")

        if not location_data:
            raise HTTPException(status_code=404, detail="Cannot find the item location")

        location = Location(
            latitude=float(location_data["latitude"]),
            longitude=float(location_data["longitude"]),
            altitude=float(location_data["altitude"]),
            timestamp=datetime.fromtimestamp(location_data["timeStamp"] / 1000).isoformat(),
        )
        self.items[name] = location
        return location

    def get_system_items(self) -> List[str]:
        """Get all items"""
        self._load_data()
        items = [item["name"] for item in self.raw_data if item.get("name")]
        self.items = {name: None for name in items}
        return items

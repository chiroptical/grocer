import pathlib
import json


def is_dir(path):
    if not path.is_dir():
        raise NotADirectoryError(f"'{path}' is not a directory!")


class Store:
    def __init__(self, store_path):
        self._store_path = pathlib.Path(store_path)
        if not self._store_path.exists():
            self._store_path.mkdir()
        is_dir(self._store_path)

        self._aisles = {}

    def __getitem__(self, aisle):
        if aisle in self._aisles.keys():
            return self._aisles[aisle]
        else:
            self._aisles[aisle] = Aisle(self._store_path, aisle)
            return self._aisles[aisle]


class Aisle:
    def __init__(self, store_path, aisle, primary_key="sku"):
        self._aisle_path = pathlib.Path.joinpath(store_path, aisle)
        if not self._aisle_path.exists():
            self._aisle_path.mkdir()
        is_dir(self._aisle_path)

        self._skus = {}
        self._primary_key = primary_key

    def __setitem__(self, sku, payload):
        self._skus[sku] = SKU(self._aisle_path, sku, payload=payload)

    def __getitem__(self, sku):
        if not sku in self._skus:
            self._skus[sku] = SKU(self._aisle_path, sku)
            return self._skus[sku].get_json()
        else:
            return self._skus[sku].get_json()

    def stock_one(self, payload):
        if not self._primary_key in payload:
            raise KeyError(f"The key '{self._primary_key}' must be in your item")
        sku = payload.pop(self._primary_key)
        self[sku] = payload


class SKU:
    def __init__(self, aisle_path, sku, payload=None):
        self._sku_path = pathlib.Path.joinpath(aisle_path, f"{sku}.json")
        if payload is None:
            if not self._sku_path.is_file():
                raise KeyError(f"'{sku}' is not a SKU in '{aisle_path}'")
        else:
            with open(self._sku_path, "w") as f:
                json.dump(payload, f)

    def get_json(self):
        with open(self._sku_path, "r") as f:
            return json.load(f)

import json
from typing import Dict
import urllib3

from jsonschema import RefResolver, Draft202012Validator
from jsonschema.exceptions import ValidationError

from jsonschema import validate, RefResolver

from multiscale_spatial_image import to_multiscale, MultiscaleSpatialImage
from spatial_image import to_spatial_image
import numpy as np
import zarr

http = urllib3.PoolManager()

def load_schema(version: str = "0.4", strict: bool = False) -> Dict:
    strict_str = ""
    if strict:
        strict_str = "strict_"
    response = http.request("GET", f"https://ngff.openmicroscopy.org/{version}/schemas/{strict_str}image.schema")
    schema = json.loads(response.data.decode())
    return schema

def check_valid_ngff(multiscale: MultiscaleSpatialImage):
    store = zarr.storage.MemoryStore(dimension_separator="/")
    multiscale.to_zarr(store, compute=True)
    zarr.convenience.consolidate_metadata(store)
    metadata = json.loads(store.get(".zmetadata"))["metadata"]
    ngff = metadata[".zattrs"]

    image_schema = load_schema(version="0.4", strict=False)
    strict_image_schema = load_schema(version="0.4", strict=True)
    schema_store = {
        image_schema["$id"]: image_schema,
        strict_image_schema["$id"]: strict_image_schema,
    }
    resolver = RefResolver.from_schema(image_schema, store=schema_store)
    validator = Draft202012Validator(image_schema, resolver=resolver)
    strict_validator = Draft202012Validator(strict_image_schema, resolver=resolver)

    validator.validate(ngff)
    # Need to add NGFF metadata property
    # strict_validator.validate(ngff)


def test_y_x_valid_ngff():
    array = np.random.random((32, 16))
    image = to_spatial_image(array)
    multiscale = to_multiscale(image, [2, 4])

    check_valid_ngff(multiscale)


def test_z_y_x_valid_ngff():
    array = np.random.random((32, 32, 16))
    image = to_spatial_image(array)
    multiscale = to_multiscale(image, [2, 4])

    check_valid_ngff(multiscale)


def test_z_y_x_c_valid_ngff():
    array = np.random.random((32, 32, 16, 3))
    image = to_spatial_image(array)
    multiscale = to_multiscale(image, [2, 4])

    check_valid_ngff(multiscale)


def test_t_z_y_x_c_valid_ngff():
    array = np.random.random((2, 32, 32, 16, 3))
    image = to_spatial_image(array)
    multiscale = to_multiscale(image, [2, 4])

    check_valid_ngff(multiscale)

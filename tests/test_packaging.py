from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files

import pytest

import edcm


def test_public_version_is_declared() -> None:
    assert edcm.__version__ == "0.1.0"


def test_installed_metadata_matches_public_version() -> None:
    """Editable and wheel installs must derive metadata from edcm.__version__."""

    try:
        installed_version = version("edcm")
    except PackageNotFoundError:
        pytest.skip("package metadata is available after editable or wheel installation")

    assert installed_version == edcm.__version__


def test_frozen_canon_data_is_packaged() -> None:
    markers = files("edcm.measurement.canon").joinpath("data", "markers_v1.json")
    assert markers.is_file()

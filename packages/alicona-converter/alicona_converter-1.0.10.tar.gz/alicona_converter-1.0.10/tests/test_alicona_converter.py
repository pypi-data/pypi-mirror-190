#!/usr/bin/env python3.9
"""
Quick test for the alicona-converter-script. This test uses the test data in
test_data.txt.
"""
from pathlib import Path

import alicona_converter as ac


def test_data_conversion(tmp_path: Path) -> None:
    """Test if the data can be converted correctly. The actual data points are
    not tested."""
    test_file = Path("tests/test_data.txt")
    data = ac.SurfaceData(test_file)

    data.write_flow_factor_data(
        tmp_path / "flow_factor.txt",
        E=1., nu=1., yield_pressure=2.)
    assert (tmp_path / "flow_factor.txt").exists()

    data.write_1d_data(
        tmp_path / "one_d.txt")
    assert (tmp_path / "one_d.txt").exists()

    data.write_1d_data_holes(
        tmp_path / "holes.txt")
    assert (tmp_path / "holes.txt").exists()

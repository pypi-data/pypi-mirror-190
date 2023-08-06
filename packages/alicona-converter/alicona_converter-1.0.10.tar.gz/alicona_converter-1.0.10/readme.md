# Alicona Converter
Converter for Surface Data Formats

This script transforms the output format of the optical microscope by Alicona
to different input formats, for example the format used tribo-x.

## Usage

The basic usage is to call the script directly `python alicona_converter.py`
or, if it has been installed by pip, `python -m alicona_converter`.
For more information on the usage, see `python alicona_converter -h`.

## API

This module can also be used to parse Alicona's output format directly to
a numpy array:
```
from alicona_converter import parse_alicona_data

data = parse_alicona_data(filename)
```

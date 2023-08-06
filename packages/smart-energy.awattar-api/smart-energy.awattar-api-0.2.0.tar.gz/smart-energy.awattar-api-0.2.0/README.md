# Awattar API

A python library to access the Awattar Api. Refer also to the [Awattar Energy Price API](https://www.awattar.de/). This repo provides functionality for:

- Getting Energy Price forecast information.

## Installing the library locally

Python 3 is recommended for this project.

```bash
python -m pip install -e .
```

> **This is needed for the first time when working with the library/examples/tests.**

## Example usage

```bash
ENERGY_DATA_API_URL="https://api.awattar.de" python3 examples/simple.py
```

or

```python
from awattar_api.awattar_api import AwattarApi

awattar_api = AwattarApi('provide_api_url')
# or you can define additional optional parameters
# awattar_api = AwattarApi('provide_api_url', timeout=10)

print(awattar_api.get_electricity_price())
```

## Development

### Installing required pip packages

```bash
python pip install -r requirements.txt
pre-commit install -t pre-push
```

### Linting

```bash
pylint awattar_api/*.py tests/*.py examples/*.py
```

### Unit testing

```bash
pytest tests/*.py

# show logs
pytest -o log_cli=true

# code coverage
pytest --durations=10 --cov-report term-missing --cov=awattar_api tests
```

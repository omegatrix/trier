# trycatch

> Utility wrapper class to handle exceptions.

[![PyPI version](https://badge.fury.io/py/trycatch.svg)](https://badge.fury.io/py/trycatch)
[![trycatch CI](https://github.com/omegatrix/trycatch/actions/workflows/build.yaml/badge.svg)](https://github.com/omegatrix/trycatch/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/omegatrix/trycatch/branch/main/graph/badge.svg?token=2M0QOSUPM0)](https://codecov.io/gh/omegatrix/trycatch)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/trycatch)

## Installation
You can [install `trycatch` from PyPI](https://pypi.org/project/trycatch), with `pip`:

```bash
python -m pip install trycatch
```

## Example usage
Instead of using `try except` block you could replace it with `trycatch`.

```py
from trycatch import Try

err, val = Try(lambda: 10 / 0).catch(ZeroDivisionError)

if err:
    # handle error

# do stuff with `val`

# Another way to handle could be
if not err:
  # do stuff with `val`
```

Supports multiple exceptions.
```py
from trycatch import Try

err, file = Try(open, file="doenot_exist.txt").catch(FileNotFoundError, OSError)

if err:
    # handle error

# do stuff with `file`
```

Supports async error handling as well.
```py
import asyncio
from httpx import AsyncClient, HTTPStatusError, Response
from trycatch import Try

def raise_on_4xx_5xx(response):
    response.raise_for_status()

async def main():
    client = AsyncClient(event_hooks={"response": [raise_on_4xx_5xx]})

    # The endpoint responds with a 404 error
    err, response = await Try(client.get, "https://run.mocky.io/v3/201f1fe6-5a3b-49c1-9df7-312951618405").async_catch(HTTPStatusError)

    if err:
        # Handle error

    # do stuff with `response`

asyncio.run(main())
```

## Changelog

Refer to the [CHANGELOG.md](CHANGELOG.md) file.

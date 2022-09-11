import asyncio
from datetime import datetime
from typing import Awaitable, NoReturn

import pytest

from trier import Try, __version__


class CustomException(Exception):
    pass


def divide(first_num: int, second_num: int) -> float:
    return first_num / second_num


async def raise_async_exception() -> Awaitable[NoReturn]:
    await asyncio.sleep(0.5)

    raise CustomException("Async exception")


async def dummy_async_function() -> Awaitable[str]:
    await asyncio.sleep(0.5)

    return "Done"


def test_version():
    assert __version__ == "1.0.4"


def test_trycatch():
    err, val = Try(lambda: "Done").catch(Exception)

    assert err is None
    assert val == "Done"
    assert isinstance(val, str)


def test_trycatch_with_args():
    err, val = Try(divide, 10, 2).catch(ZeroDivisionError)

    assert err is None
    assert val == 5
    assert isinstance(val, float)


def test_trycatch_with_kwargs():
    err, val = Try(divide, first_num=10, second_num=2).catch(ZeroDivisionError)

    assert err is None
    assert val == 5
    assert isinstance(val, float)


def test_trycatch_with_exception():
    err, val = Try(datetime.isoformat, "invalid_datetime").catch(TypeError)

    assert isinstance(err, TypeError)
    assert (
        str(err)
        == "descriptor 'isoformat' for 'datetime.datetime' objects doesn't apply to a 'str' object"
    )
    assert val is None


def test_trycatch_with_multiple_exceptions():
    err, val = Try(divide, "34", 0).catch(ZeroDivisionError, TypeError)

    assert isinstance(err, TypeError)
    assert str(err) == "unsupported operand type(s) for /: 'str' and 'int'"
    assert val is None


def test_trycatch_with_no_callable():
    with pytest.raises(TypeError) as exception_info:
        Try(None).catch(Exception)

    assert str(exception_info.value) == "`func` argument must be a Callable."


def test_trycatch_with_no_exception():
    with pytest.raises(TypeError) as exception_info:
        Try(lambda: "done").catch()

    assert str(exception_info.value) == "At least one Exception required."


@pytest.mark.asyncio
async def test_async_trycatch():
    err, val = await Try(dummy_async_function).async_catch(CustomException)

    assert err is None
    assert val == "Done"
    assert isinstance(val, str)


@pytest.mark.asyncio
async def test_async_trycatch_with_custom_exception():
    err, val = await Try(raise_async_exception).async_catch(CustomException)

    assert isinstance(err, CustomException)
    assert str(err) == "Async exception"
    assert val is None


@pytest.mark.asyncio
async def test_async_trycatch_with_no_exception():
    with pytest.raises(TypeError) as exception_info:
        await Try(lambda: "done").async_catch()

    assert str(exception_info.value) == "At least one Exception required."

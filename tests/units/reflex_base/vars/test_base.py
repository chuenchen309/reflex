"""Tests for reflex_base.vars.base."""

import reflex as rx
from reflex.state import BaseState


def test_computed_var_return_type_checked_only_on_recompute(mocker):
    """The return type of a cached computed var is only validated on recompute.

    Args:
        mocker: Pytest mocker object.
    """

    class ReturnTypeCheckState(BaseState):
        v: int = 0

        @rx.var
        def wrong_typed(self) -> str:
            return self.v  # pyright: ignore [reportReturnType]

    state = ReturnTypeCheckState()
    mock_error = mocker.patch("reflex_base.utils.console.error")
    assert state.wrong_typed == 0
    assert mock_error.call_count == 1
    # Cache hits must not re-run the (potentially deep) type check.
    assert state.wrong_typed == 0
    assert mock_error.call_count == 1
    # Invalidation triggers a recompute, which re-checks the return type.
    state.v = 1
    assert state.wrong_typed == 1
    assert mock_error.call_count == 2


def test_non_cached_computed_var_return_type_checked_every_access(mocker):
    """A cache=False computed var recomputes, and is type-checked, on every access.

    Args:
        mocker: Pytest mocker object.
    """

    class NonCachedReturnTypeCheckState(BaseState):
        v: int = 0

        @rx.var(cache=False)
        def wrong_typed(self) -> str:
            return self.v  # pyright: ignore [reportReturnType]

    state = NonCachedReturnTypeCheckState()
    mock_error = mocker.patch("reflex_base.utils.console.error")
    assert state.wrong_typed == 0
    assert state.wrong_typed == 0
    assert mock_error.call_count == 2


async def test_async_computed_var_return_type_checked_only_on_recompute(mocker):
    """The return type of a cached async computed var is only validated on recompute.

    Args:
        mocker: Pytest mocker object.
    """

    class AsyncReturnTypeCheckState(BaseState):
        v: int = 0

        @rx.var
        async def wrong_typed(self) -> str:
            return self.v  # pyright: ignore [reportReturnType]

    state = AsyncReturnTypeCheckState()
    mock_error = mocker.patch("reflex_base.utils.console.error")
    assert await state.wrong_typed == 0
    assert mock_error.call_count == 1
    # Cache hits must not re-run the (potentially deep) type check.
    assert await state.wrong_typed == 0
    assert mock_error.call_count == 1

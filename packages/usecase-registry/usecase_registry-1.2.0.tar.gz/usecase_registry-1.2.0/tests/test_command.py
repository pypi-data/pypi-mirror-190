"""Tests for command."""
import pytest

from usecase_registry.command import ICommand


class TestICommand:
    """Test definition for ICommand."""

    def test_cannot_be_instantiated(self) -> None:
        """ICommand is an interface an cannot be instantiated."""
        with pytest.raises(TypeError):
            ICommand()  # type:ignore[abstract]

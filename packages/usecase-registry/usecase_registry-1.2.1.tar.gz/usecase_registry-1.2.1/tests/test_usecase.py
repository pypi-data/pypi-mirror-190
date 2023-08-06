"""Test for use case."""
from typing import Type

import pytest
from result import Ok, Result

from usecase_registry import UseCaseRegistry
from usecase_registry.errors import IdentifiedError
from usecase_registry.usecase import IUsecase


class TestIUsecase:
    """Test definition for IUsecase."""

    def test_cannot_be_instantiated(self) -> None:
        """IUsecase is an interface an cannot be instantiated."""
        write_ops_registry = UseCaseRegistry[str](max_length=1)
        result_registry = UseCaseRegistry[None](max_length=0)
        errors_registry = UseCaseRegistry[Type[IdentifiedError]](max_length=0)

        with pytest.raises(TypeError):
            IUsecase(
                write_ops_registry=write_ops_registry,
                result_registry=result_registry,
                errors_registry=errors_registry,
            )  # type:ignore[abstract]

    def test_interface_can_be_extendend(self) -> None:
        """Test interface can be extended."""

        class ConcreteUsecase(IUsecase):
            def __init__(
                self,
                name: str,
                last_name: str,
                write_ops_registry: UseCaseRegistry[str],
                result_registry: UseCaseRegistry[None],
                errors_registry: UseCaseRegistry[Type[IdentifiedError]],
            ) -> None:
                """Construct concrete implementation."""
                self.name = name
                self.last_name = last_name
                super().__init__(write_ops_registry, result_registry, errors_registry)

            def execute(self) -> Result[None, Exception]:
                return Ok()

        write_ops_registry = UseCaseRegistry[str](max_length=1)
        result_registry = UseCaseRegistry[None](max_length=0)
        errors_registry = UseCaseRegistry[Type[IdentifiedError]](max_length=0)
        ConcreteUsecase(
            name="Peter",
            last_name="Parket",
            write_ops_registry=write_ops_registry,
            result_registry=result_registry,
            errors_registry=errors_registry,
        )

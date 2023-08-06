"""Interface for concrete usecases."""
import abc
from typing import Any, Type

from result import Result

from .errors import IdentifiedError
from .registry import UseCaseRegistry


class IUsecase(abc.ABC):
    """Use case interface."""

    def __init__(
        self,
        write_ops_registry: UseCaseRegistry[Any],
        result_registry: UseCaseRegistry[Any],
        errors_registry: UseCaseRegistry[Type[IdentifiedError]],
    ) -> None:
        """Usecase constructor."""
        self.write_ops_registry = write_ops_registry
        self.result_registry = result_registry
        self.errors_registry = errors_registry

    @abc.abstractmethod
    def execute(self) -> Result[None, Exception]:
        """Workflow execution command to complete the usecase."""

"""Version control data plugin definitions"""
from abc import abstractmethod
from pathlib import Path
from typing import TypeVar

from cppython_core.schema import Plugin


class SCM(Plugin):
    """Base class for version control systems"""

    @abstractmethod
    def is_repository(self, path: Path) -> bool:
        """Queries repository status of a path

        Args:
            path: The input path to query

        Returns:
            Whether the given path is a repository root
        """
        raise NotImplementedError()

    @abstractmethod
    def extract_version(self, path: Path) -> str:
        """Extracts the system's version metadata

        Args:
            path: The repository path

        Returns:
            A version
        """
        raise NotImplementedError()


SCMT = TypeVar("SCMT", bound=SCM)

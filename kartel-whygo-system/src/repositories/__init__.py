"""
Repository layer for data access abstraction
"""

from .interfaces import IWhygoRepository, IProgressRepository
from .json_repository import JsonWhygoRepository, JsonProgressRepository

__all__ = [
    'IWhygoRepository',
    'IProgressRepository',
    'JsonWhygoRepository',
    'JsonProgressRepository'
]

"""Port Range Compactor.

Compress a list of individual port numbers into the shortest possible
comma-and-dash range specification.
"""

from .core import compact

__all__ = ["compact"]

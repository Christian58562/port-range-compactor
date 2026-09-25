"""Core implementation for compressing port numbers."""

from __future__ import annotations

from collections.abc import Iterable


def compact(ports: Iterable[int]) -> str:
    """Return a comma-and-dash range specification for *ports*.

    Input ports are expected to be integers in the valid TCP/UDP port range
    (1-65535). Values outside this range raise ``ValueError``. Duplicate
    values are ignored. The output is sorted in ascending numeric order, with
    consecutive runs of three or more ports collapsed into ``start-end``
    ranges. Runs of length two remain as two individual ports because
    ``8000-8001`` is the same number of characters as ``8000,8001`` and the
    latter is considered more conventional for short runs.

    Args:
        ports: An iterable of port numbers.

    Returns:
        The shortest comma-and-dash range specification.

    Raises:
        ValueError: If any port is outside the valid 1-65535 range, or if the
            input contains a non-integer value.
    """
    # Use a set first to remove duplicates, then sort. This is a deliberate
    # choice to keep the implementation clear even though a sorted list of
    # unique values could be built in a single pass; the set makes the
    # deduplication explicit.
    unique_ports = set()
    for port in ports:
        if not isinstance(port, int):
            raise ValueError(f"invalid port: {port!r}")
        if not 1 <= port <= 65535:
            raise ValueError(f"port out of range: {port}")
        unique_ports.add(port)

    if not unique_ports:
        return ""

    sorted_ports = sorted(unique_ports)

    ranges: list[str] = []
    start = prev = sorted_ports[0]

    for port in sorted_ports[1:]:
        if port == prev + 1:
            prev = port
            continue

        ranges.append(_format_range(start, prev))
        start = prev = port

    ranges.append(_format_range(start, prev))
    return ",".join(ranges)


def _format_range(start: int, end: int) -> str:
    """Format a run of consecutive ports as a single range element."""
    if start == end:
        return str(start)
    if end == start + 1:
        # Two consecutive ports are not collapsed because ``start-end`` and
        # ``start,end`` are the same length, and the comma form is more
        # conventional for short ranges.
        return f"{start},{end}"
    return f"{start}-{end}"

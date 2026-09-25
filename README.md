# Port Range Compactor

Compress a list of individual port numbers into the shortest possible comma-and-dash range specification.

```python
from port_range_compactor import compact

ports = [8080, 8081, 8082, 8443, 9090, 9091]
print(compact(ports))
# 8080-8082,8443,9090,9091
```

## Why this exists

Firewall rules, network scanner reports, and infrastructure-as-code configurations often need a human-readable summary of many open ports. Writing out every port individually becomes unreadable when the list is long. This library reduces that list to the shortest conventional notation using commas and dashes, e.g. `80,443,8000-8010`.

The trade-off is strict input validation: every port must be an integer between 1 and 65535. This catches accidental protocol numbers (like 0) or malformed data early, but means the library will not accept strings such as `"80"`. Callers must convert input before calling.

## Awkward edge

Two consecutive ports are **not** collapsed into a range. `[8000, 8001]` becomes `"8000,8001"`, not `"8000-8001"`, because the two forms are exactly the same length and the comma form is more conventional. Ranges of three or more ports are collapsed.

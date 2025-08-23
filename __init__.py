"""Top‑level package for the Bug‑to‑PR Autopilot example.

This file marks ``autopilot_app`` as a Python package so that its
submodules (e.g. ``backend`` and ``agent``) can be imported using
standard dotted notation. Without an ``__init__.py`` file Python
would treat this directory as a namespace package only on Python
versions that support PEP 420. Adding this file ensures consistent
behaviour across environments.
"""

__all__ = [
    "agent",
    "backend",
    "config",
    "frontend",
]
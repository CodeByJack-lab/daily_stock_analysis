# -*- coding: utf-8 -*-
"""HK stock code detection helpers.

Extracted from the (removed) akshare_fetcher module so that callers outside
the A-share data sources can still detect Hong Kong codes after the
A-share fetcher cleanup.
"""

from __future__ import annotations


def _is_hk_code(stock_code: str) -> bool:
    """Return True when *stock_code* looks like a Hong Kong listing code."""
    code = stock_code.strip().lower()
    if code.endswith(".hk"):
        numeric_part = code[:-3]
        return numeric_part.isdigit() and 1 <= len(numeric_part) <= 5
    if code.startswith("hk"):
        numeric_part = code[2:]
        return numeric_part.isdigit() and 1 <= len(numeric_part) <= 5
    return code.isdigit() and len(code) == 5


def is_hk_stock_code(stock_code: str) -> bool:
    """Public wrapper used across the package and downstream services."""
    return _is_hk_code(stock_code)

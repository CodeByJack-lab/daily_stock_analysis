# -*- coding: utf-8 -*-
"""
===================================
数据源策略层 - 包初始化
===================================

本包实现策略模式管理多个数据源，实现：
1. 统一的数据获取接口
2. 自动故障切换
3. 防封禁流控策略

数据源优先级（HK / US only after A-share cleanup）：
1. YfinanceFetcher (Priority 4) - 来自 yfinance 库（US/HK 主力）
2. LongbridgeFetcher (Priority 5) - 长桥 OpenAPI（美股/港股兜底，需配置凭据）
3. FinnhubFetcher                 - 美股，需配置 FINNHUB_API_KEY
4. AlphaVantageFetcher            - 美股，需配置 ALPHAVANTAGE_API_KEY

提示：优先级数字越小越优先，同优先级按初始化顺序排列
"""

from .base import BaseFetcher, DataFetcherManager
from .yfinance_fetcher import YfinanceFetcher
from .longbridge_fetcher import LongbridgeFetcher
from .finnhub_fetcher import FinnhubFetcher
from .alphavantage_fetcher import AlphaVantageFetcher
from .us_index_mapping import is_us_index_code, is_us_stock_code, get_us_index_yf_symbol, US_INDEX_MAPPING
from .stock_code_utils import is_hk_stock_code

__all__ = [
    'BaseFetcher',
    'DataFetcherManager',
    'YfinanceFetcher',
    'LongbridgeFetcher',
    'FinnhubFetcher',
    'AlphaVantageFetcher',
    'is_us_index_code',
    'is_us_stock_code',
    'is_hk_stock_code',
    'get_us_index_yf_symbol',
    'US_INDEX_MAPPING',
]

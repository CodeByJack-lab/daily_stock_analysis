# -*- coding: utf-8 -*-
"""
===================================
平台适配器模块（仅保留 base，其他平台已在 Step 3 清理中移除）
===================================
"""

from bot.platforms.base import BotPlatform

ALL_PLATFORMS = {}

# Backwards-compatible shims for code that still imports the stream/SDK flags.
DINGTALK_STREAM_AVAILABLE = False
FEISHU_SDK_AVAILABLE = False


def start_dingtalk_stream_background() -> bool:  # pragma: no cover - removed
    return False


def start_feishu_stream_background() -> bool:  # pragma: no cover - removed
    return False


__all__ = [
    "BotPlatform",
    "ALL_PLATFORMS",
    "DINGTALK_STREAM_AVAILABLE",
    "FEISHU_SDK_AVAILABLE",
    "start_dingtalk_stream_background",
    "start_feishu_stream_background",
]

# -*- coding: utf-8 -*-
"""
===================================
通知发送层模块
===================================

仅保留 Telegram 渠道（其他渠道已在 Step 2 清理中移除）。
"""

from .telegram_sender import TelegramSender

__all__ = ["TelegramSender"]

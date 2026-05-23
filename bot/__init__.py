# -*- coding: utf-8 -*-
"""
===================================
机器人命令触发系统
===================================

通过命令触发股票分析等功能。Step 3 清理后仅支持 Telegram 渠道。

模块结构：
- models.py: 统一的消息/响应模型
- dispatcher.py: 命令分发器
- commands/: 命令处理器
- platforms/: 平台适配器（仅 base.py 保留）
- handler.py: Webhook 处理器

使用方式：
1. 配置 TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID
2. 启动 WebUI 服务
3. 在 Telegram BotFather 处配置 Webhook URL: http://your-server/bot/telegram
"""

from bot.models import BotMessage, BotResponse, ChatType, WebhookResponse
from bot.dispatcher import CommandDispatcher, get_dispatcher

__all__ = [
    'BotMessage',
    'BotResponse',
    'ChatType',
    'WebhookResponse',
    'CommandDispatcher',
    'get_dispatcher',
]

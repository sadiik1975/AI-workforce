from __future__ import annotations

import asyncio
import json
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from core.config import get_config
from workforce.app import WorkforceApp


LOGGER = logging.getLogger(__name__)


def format_result(result: dict) -> str:
    if result.get("status") == "failed":
        return f"Task failed: {result.get('error', 'Unknown error')}"
    if result.get("status") == "waiting_approval":
        return f"Task {result.get('task_id')} is waiting for approval."
    payload = result.get("result")
    if payload is None:
        return f"Task completed: {result.get('task_id')}"
    if isinstance(payload, str):
        return payload[:3900]
    return json.dumps(payload, indent=2, ensure_ascii=True, default=str)[:3900]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Been Ventures AI Workforce is online. Send me a task.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Send a task such as: Find grants for Been Ventures")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    description = update.message.text.strip()
    if not description:
        return
    if update.effective_chat:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    app = WorkforceApp()
    result = await asyncio.to_thread(app.delegate_task, description)
    await update.message.reply_text(format_result(result))


def build_application(token: str) -> Application:
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return application


async def _poll(token: str) -> None:
    application = build_application(token)
    await application.initialize()
    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)
    await asyncio.Event().wait()


def run_bot() -> None:
    token = get_config().get("telegram_bot_token")
    if not token:
        LOGGER.info("Telegram bot disabled: TELEGRAM_BOT_TOKEN is not configured")
        return
    LOGGER.info("Starting Telegram bot polling")
    asyncio.run(_poll(token))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_bot()
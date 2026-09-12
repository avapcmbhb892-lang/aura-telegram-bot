import os
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

WORKSPACE = Path(os.getenv("AURA_WORKSPACE", "./aura_workspace")).resolve()
WORKSPACE.mkdir(parents=True, exist_ok=True)

def aura_reply(text: str) -> str:
    t = text.lower().strip()
    if any(x in t for x in ["привет", "здравствуй", "здарова"]):
        return "Привет! Я Аура 🌙\nГотова помочь с кодом, файлами и обычными вопросами."
    if "кто ты" in t:
        return "Я Аура — локальный технический помощник."
    if "что ты умеешь" in t:
        return "Могу отвечать на вопросы, помогать с Python, создавать файлы и объяснять ошибки."
    if "калькулятор" in t and ("код" in t or "напиши" in t):
        return """Вот простой Python-калькулятор:

```python
def calculator():
    a = float(input("Первое число: "))
    b = float(input("Операция (+, -, *, /): "))
    op = input("Операция (+, -, *, /): ")

    if op == "+":
        print(a + b)
    elif op == "-":
        print(a - b)
    elif op == "*":
        print(a * b)
    elif op == "/":
        print("На ноль делить нельзя" if b == 0 else a / b)
    else:
        print("Неизвестная операция")

calculator()
```"""
    if "termux" in t:
        return "В Termux я могу помогать с командами, Python-проектами и разбором ошибок."
    if "ошиб" in t:
        return "Пришли текст ошибки и небольшой фрагмент кода — разберём по шагам."
    return "Я Аура 🌙. Напиши конкретную задачу, например: «Напиши Python-код калькулятора»."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌙 AURA AI подключена.\n\n"
        "Напиши задачу обычным сообщением.\n"
        "Например: «Напиши Python-код калькулятора»."
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start — запуск\n/help — помощь\n/status — статус AURA\n\n"
        "Также можно писать обычным текстом."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 AURA работает на Render.\n📁 Рабочая папка: " + str(WORKSPACE))

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        await update.message.reply_text(aura_reply(update.message.text))

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("Переменная BOT_TOKEN не задана.")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
    print("AURA Telegram bot started")
    app.run_polling()

if __name__ == "__main__":
    main()

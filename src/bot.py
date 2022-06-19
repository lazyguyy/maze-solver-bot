import asyncio
import logging
import pathlib
import solver
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Send me a picture of a 2d maze so I can try to solve it."
    )

async def solve_maze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"photo available in {', '.join(map(lambda p: f'{p.width}x{p.height}',  update.message.photo))}")
    file_id = max(update.message.photo, key=lambda p: p.width * p.height)
    print(f"image received: {file_id.file_id}")
    file = await context.bot.get_file(file_id=file_id.file_id)
    photo = await file.download()
    print(photo)
    maze = solver.load_image_as_maze(photo)
    found_solution = solver.solve_maze(maze)
    caption = ["Could not find a solution", "Found a solution"][found_solution]
    print(caption)
    await context.bot.send_photo(update.message.chat_id, photo=open("solution.png", "rb"), caption=caption)

if __name__ == "__main__":
    with open("token") as file:
        token = file.read()
    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', start)
    maze_solver_handler = MessageHandler(filters.PHOTO, solve_maze)
    application.add_handler(start_handler)
    application.add_handler(maze_solver_handler)

    application.run_polling()
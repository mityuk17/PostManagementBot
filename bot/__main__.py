from botloader import bot_loader
from routers import routers_list
from middlewares import EntitiesUpdateMiddleware
import asyncio


if __name__ == "__main__":
    bot_loader.include_routers(routers_list)
    bot_loader.dispatcher.message.middleware(EntitiesUpdateMiddleware())
    asyncio.run(bot_loader.run())
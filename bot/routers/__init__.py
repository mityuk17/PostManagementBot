from routers.general import router as general_router
from routers.channel_creation import router as channel_creation_router
from routers.channel_management import router as channel_management_router
from routers.post_creation import router as post_creation_router
from routers.post_management import router as post_management_router

routers_list = [general_router, channel_creation_router, channel_management_router, post_creation_router, post_management_router]
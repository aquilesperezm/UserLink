import asyncio
from fastapi import FastAPI, Depends, Request
from decouple import config
import uvicorn
from controllers import UserController, PostController, CommentController, TagController, TagsByPostController
import str2bool
from fastapi.middleware.cors import CORSMiddleware
import time
from tools.db import close_connection,Engine,Base,create_all_tables, drop_all_tables

# Importing enviroments vars for wakeup server
# Importing enviroments vars for wakeup server
SERVER_HOSTNAME = config('SERVER_HOSTNAME')
SERVER_PORT = config('SERVER_PORT')
RESET_FACTORY =  str2bool.str2bool(config('RESET_FACTORY'))

# Creating a FastAPI app
# Creating a FastAPI app
app = FastAPI(
    #openapi_tags=tags_metadata,
    title="UserLink - API Documentation",
    description="API endpoints",
    version="0.1",
    #docExpansion="None"
) 

#When 'shutdown' event, launch 'close_connection method'
app.add_event_handler('shutdown',close_connection)   

# 
# 
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserController.user_router)
app.include_router(PostController.post_router)
app.include_router(CommentController.comment_router)
app.include_router(TagController.tag_router)
app.include_router(TagsByPostController.tags_by_post_router)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    print("Time took to process the request and return response is {} sec".format(time.time() - start_time))
    return response

if __name__ == "__main__":
    if RESET_FACTORY:
        print('------------------ droping all tables -------------------- ')
        asyncio.run(drop_all_tables())    
    asyncio.run(create_all_tables())
    uvicorn.run("main:app", host=SERVER_HOSTNAME, port=int(SERVER_PORT), reload=True, use_colors=True)


from fastapi import FastAPI, Request
from decouple import config
import uvicorn
from controllers import UserController, PostController, CommentController, TagController, TagsByPostController
import asyncio
from fastapi.middleware.cors import CORSMiddleware

import time
import tools.database
from tools.database import create_tables
from tools.database import connect_db
from tools.database import disconnect_db
from tools.database import metadata,engine
from str2bool import str2bool
  
SERVER_HOSTNAME = config('SERVER_HOSTNAME')
SERVER_PORT = config('SERVER_PORT')
  
app = FastAPI(
    #openapi_tags=tags_metadata,
    title="UserLink - API Documentation",
    description="API endpoints",
    version="0.1",
    #docExpansion="None"
) 

app.add_event_handler('startup',connect_db)
app.add_event_handler('shutdown',disconnect_db)

async def initial_setup(dropTables=False):     
    await asyncio.create_task(create_tables(dropTables))


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

RESET_DB_FACTORY = str2bool(config('RESET_DB_FACTORY'))
 
if __name__ == "__main__":
    
    asyncio.run(initial_setup(dropTables=RESET_DB_FACTORY)) 
    uvicorn.run("main:app", host=SERVER_HOSTNAME, port=int(SERVER_PORT), reload=True)
    

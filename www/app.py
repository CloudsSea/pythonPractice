import logging; logging.basicConfig(level=logging.INFO)
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web
from jinja2 import Environment, FileSystemLoader

async def index(request):
    return web.Response(body=b'hello,word',content_type='text/html')

def init():
    app = web.Application()
    app.router.add_get('/',index)
    web.run_app(app,host='127.0.0.1',port='9000')

if __name__ == '__main__':
    init()
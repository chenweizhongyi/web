import logging; logging.basicConfig(level=logging.INFO)
import asyncio, os, json, time

from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/')
async def index(request):
    return web.Response(text='haha')

async def init(loop):
    app = web.Application()
    app.router.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner,'127.0.0.1', 9000)
    await site.start()

    # srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    # return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
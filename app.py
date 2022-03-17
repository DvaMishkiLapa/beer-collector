import aiohttp
from sanic import Sanic
from sanic.response import json
import asyncio


app = Sanic(name='beer')
beer_url = "https://random-data-api.com/api/beer/random_beer"

@app.listener('before_server_start')
def init(app, loop):
    app.ctx.httpSession = aiohttp.ClientSession(loop=loop)


@app.listener('after_server_stop')
def finish(app, loop):
    loop.run_until_complete(app.ctx.httpSession.close())
    loop.close()


@app.get("/get_new_beers")
async def get_beer(request):
    tasks = []
    for x in range(5):
        tasks.append(asyncio.ensure_future(get_beer(app.ctx.httpSession, beer_url)))
    beers = await asyncio.gather(*tasks)
    ans = [{k: b[k] for k in ['brand', 'name', 'alcohol']} for b in beers]
    ans.sort(key=extract_alcohol_float)
    return json(ans)


def extract_alcohol_float(beers_list):
    return float(beers_list['alcohol'][:-1])

async def get_beer(session, url):
    async with session.get(url) as resp:
        return await resp.json()


app.run(host="0.0.0.0", port=8000, workers=1, debug=1)

import asyncio

import aiohttp
from prometheus_client import Counter
from sanic import Sanic
from sanic.log import logger
from sanic.response import json
from sanic_openapi import openapi3_blueprint

counter = Counter("sanic_requests_total",
                  "Track the total number of requests",
                  ["method"])


app = Sanic(name='beer')
app.blueprint(openapi3_blueprint)
beer_url = "https://random-data-api.com/api/beer/random_beer"


@app.middleware('request')
async def track_requests(request):
    counter.labels(method=request.method).inc()
    count_request = counter.labels(method=request.method)._value.get()
    logger.debug(f'track_requests inc requests counter: {count_request}')


@app.listener('before_server_start')
def init(app, loop):
    app.ctx.httpSession = aiohttp.ClientSession(loop=loop)


@app.listener('after_server_stop')
def finish(app, loop):
    loop.run_until_complete(app.ctx.httpSession.close())
    loop.close()


@app.get("/get_new_beers")
async def get_beer(request):
    '''
    Метод выгружает асинхронно 5 новых сортов пива, выдает ответ в виде JSON с полями brand, name и alcohol
    '''
    tasks = []
    for x in range(5):
        tasks.append(asyncio.ensure_future(get_beer(app.ctx.httpSession, beer_url)))
    beers = await asyncio.gather(*tasks)
    logger.debug(f'get_beer get dirty beer data. Len: {len(beers)}')
    ans = [{k: b[k] for k in ['brand', 'name', 'alcohol']} for b in beers]
    ans.sort(key=extract_alcohol_float)
    logger.debug(f'get_beer get clear sort beer data. Len: {len(ans)}')
    return json(ans)


@app.get("/stats")
async def get_stats(request):
    '''
    Метод показывает сколько запросов было на сервер (с момента запуска)
    '''
    count_request = counter.labels(method=request.method)._value.get()
    logger.debug(f'count_request get count request: {count_request}')
    return json([{'count_request': count_request}])


def extract_alcohol_float(beers_list):
    out = float(beers_list['alcohol'][:-1])
    logger.debug(f'extract_alcohol_float {beers_list} => {out}')
    return out


async def get_beer(session, url):
    async with session.get(url) as resp:
        return await resp.json()


app.run(host="0.0.0.0", port=8000, workers=1, debug=1)

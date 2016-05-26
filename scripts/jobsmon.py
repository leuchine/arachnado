import asyncio
import json
import logging
import ssl
import websockets


def ssl_ctx_no_validate():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # ctx.verify_mode = ssl.CERT_NONE
    return ctx


@asyncio.coroutine
def subscribe(url, headers, name, command):
    logger = logging.getLogger(name)
    ssl_ctx = ssl_ctx_no_validate()
    print('connecting to socket')
    job_socket = yield from websockets.connect(url, extra_headers=headers)
    # job_socket = yield from websockets.connect(url, ssl=ssl_ctx, extra_headers=headers)

    logger.info('sending request')
    print('sending request')
    yield from job_socket.send(json.dumps(command))
    print('request sent')
    json_response = yield from job_socket.recv()
    while True:
        json_response = yield from job_socket.recv()
        if json_response is None:
            logger.info('Websocket dropped unexpectedly')
            break
        response = json.loads(json_response)
        response["data"]["body"] = ""
        logger.info(response)

    yield from job_socket.close()
    logger.info('Websocket closed')


@asyncio.coroutine
def passive_subscribe(url, headers):
    ssl_ctx = ssl_ctx_no_validate()
    job_socket = yield from websockets.connect(url, extra_headers=headers)
    # job_socket = yield from websockets.connect(url, ssl=ssl_ctx, extra_headers=headers)

    while True:
        json_response = yield from job_socket.recv()
        if json_response is None:
            logging.info('Websocket dropped unexpectedly')
            break
        response = json.loads(json_response)
        logging.info(json_response)

    yield from job_socket.close()
    logging.info('Websocket closed')


if __name__ == '__main__':
    # url = 'wss://54.200.77.2/ws-rpc'
    url = 'ws://127.0.0.1:8888/ws-jobs'
    url = 'ws://127.0.0.1:8888/ws-rpc'
    # url = 'ws://127.0.0.1:8888/ws-updates'
    headers = {'Authorization': 'Basic YWRtaW46bWVtZXhwYXNz'}
    logging.basicConfig(level=logging.INFO)
    jobs_command = {
        'event': 'rpc:request',
        'data': {
            'id':0,
            'jsonrpc': '2.0',
            'method': 'subscribe_to_jobs',
            # 'method': 'jobs.subscribe',
            'params': {
                "include":["127.0.0.1"],
                "exclude":["skip_me"],
            },
        },
    }
    sites_command = {
        'event': 'rpc:request',
        'data': {
            'id':0,
            'jsonrpc': '2.0',
            'method': 'pages.subscribe',
            # 'method': 'jobs.subscribe',
            'params': {
            },
        },
    }
    asyncio.Task(subscribe(url, headers, 'sites', sites_command))
    # asyncio.Task(subscribe(url, headers, 'jobs', jobs_command))
    # asyncio.Task(passive_subscribe(url, headers))
    print("!!!!!!!!!!!!")
    asyncio.get_event_loop().run_forever()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

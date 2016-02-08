# coding: utf-8
from queue import Queue, Empty
from abc import ABCMeta
import asyncio
from aiohttp import web, MsgType
from django.conf import settings
from django.utils.timezone import now
import core.models
import car_connector


def start_server():
    app = web.Application()
    add_routes(app)

    loop = asyncio.get_event_loop()
    handler = app.make_handler()
    f = loop.create_server(handler, '0.0.0.0', settings.WEB_SOCKET_SERVER_PORT)
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(handler.finish_connections(1.0))
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.cleanup())
    loop.close()


def add_routes(app: web.Application):
    app.router.add_route('GET', '/car_command/{car_id}', CarCommandHandler().get_handler)


class WebSocketHandler(metaclass=ABCMeta):
    stop_msg = 'close_ws'
    need_background = False
    stop_background_timeout = 1

    def connect_handler(self, request):
        print('websocket connection started')

    async def process_msg(self, msg_text: str):
        print(msg_text)

    async def background(self, ws: web.WebSocketResponse):
        while not ws.closed:
            print(now())
            await asyncio.sleep(1)
        print('Close background')

    async def get_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        self.connect_handler(request)

        # start background process if needed
        background_task = None
        if self.need_background:
            loop = asyncio.get_event_loop()
            background_task = loop.create_task(self.background(ws))

        # process ws messages
        while not ws.closed:
            await self._receive_msg(ws)

        # stop background
        if background_task:
            background_task.cancel()

        return ws

    async def _receive_msg(self, ws: web.WebSocketResponse):
        msg = await ws.receive()

        if msg.tp == MsgType.text:
            if msg.data == self.stop_msg:
                print('Got stop msg')
                await ws.close()
            else:
                await self.process_msg(msg.data)
        elif msg.tp == MsgType.close:
            print('websocket connection closed')
        elif msg.tp == MsgType.error:
            print('ws connection closed with exception %s' %
                  ws.exception())


class CarCommandHandler(WebSocketHandler):
    need_background = True

    def connect_handler(self, request):
        self.car_id = int(request.match_info['car_id'])
        self.car = core.models.Car.objects.get(id=self.car_id)
        print('websocket connection started for car ID', self.car_id)

        self.command_queue = Queue()

    async def process_msg(self, msg_text: str):
        # print('Got', msg_text, now())
        self.command_queue.put(msg_text)

    async def background(self, ws: web.WebSocketResponse):
        commander = car_connector.Commander(self.car)

        while not ws.closed:
            try:
                command = self.command_queue.get_nowait()
                commander.send_command(command)
                ws.send_str(command)
                # print('Response:', response, now())
                self.command_queue.task_done()
            except Empty:
                await asyncio.sleep(0.01)
        print('Close background for car ID', self.car_id)

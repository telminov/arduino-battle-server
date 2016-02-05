import asyncio
import logging
import concurrent.futures

@asyncio.coroutine
def handle_connection(reader, writer):
    peername = writer.get_extra_info('peername')
    logging.info('Accepted connection from {}'.format(peername))
    while True:
        try:
            data = yield from asyncio.wait_for(reader.readline(), timeout=10.0)
            if data: 
                writer.write(data)
            else:
                logging.info('Connection from {} closed by peer'.format(peername))
                break
        except concurrent.futures.TimeoutError:
            logging.info('Connection from {} closed by timeout'.format(peername))
            break
    writer.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    logging.basicConfig(level=logging.INFO)
    server_gen = asyncio.start_server(handle_connection, port=2007)
    server = loop.run_until_complete(server_gen)
    logging.info('Listening established on {0}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass # Press Ctrl+C to stop
    finally:
        server.close()
        loop.close()
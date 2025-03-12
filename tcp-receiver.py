import asyncio

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connected with {addr}")

    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        print(f"Received from client: {message}")
        writer.write(f"Echo: {message}".encode())
        await writer.drain()

    writer.close()
    await writer.wait_closed()

async def server():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 12345)
    async with server:
        await server.serve_forever()

async def client():
    reader, writer = await asyncio.open_connection("127.0.0.1", 12345)

    for i in range(5):
        message = f"Hello {i}"
        writer.write(message.encode())
        await writer.drain()
        response = await reader.read(100)
        print(f"Received from server: {response.decode()}")

    writer.close()
    await writer.wait_closed()

async def main():
    server_task = asyncio.create_task(server())
    await asyncio.sleep(1)  # Give the server time to start
    await client()

asyncio.run(main())

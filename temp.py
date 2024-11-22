import asyncio
import re
import uuid

from packages.models import Client

host = '5.5.5.1'
port = 14447

global CLIENTS
CLIENTS = {}

async def generateNewClient(writer,reader,username,addr,userid):
    newclient = Client(writer,reader,username, addr)
    CLIENTS[userid] = newclient
    print(CLIENTS[userid])


async def joinEvent(userid):
        for id in CLIENTS:
            writer = CLIENTS[id].writer
            servermessage = f"{CLIENTS[userid].username} a rejoint la chatroom".encode("utf-8")
            writer.write(servermessage)
        return


async def leaveEvent(userid):
    for id in CLIENTS:
        writer = CLIENTS[id].writer
        if CLIENTS[id].username == '':
            CLIENTS[id].username = CLIENTS[userid].writer
        servermessage = f"{CLIENTS[id].username} a quitté la chatroom".encode("utf-8")
        writer.write(servermessage)
    return
    

async def sendAll(message, userid):
    for id in CLIENTS:
        writer = CLIENTS[id].writer
        if id == userid:
            servermessage = f"{CLIENTS[userid].color}{CLIENTS[userid].username} : {message} \033[0m".encode("utf-8")
        else:
            servermessage = f"{CLIENTS[userid].color}Vous avez dit : {message} \033[0m".encode("utf-8")
        writer.write(servermessage)
    return

async def handle_packet(reader, writer):
    userid = uuid.uuid4()
    addr = writer.get_extra_info('peername')   

    while True: # Gestion Pseudo
        data = await reader.read(100)
        message = data.decode('utf-8')
        if not data:
            await asyncio.sleep(0.05)
        if re.match(r'^[a-z0-9_-]{3,15}$', message):
                await generateNewClient(writer,reader,message,addr,userid)
                await joinEvent(userid)
                break
    while True: # Gestion messages
        data = await reader.read(100)
        message = data.decode('utf-8')
        if not data:
            await asyncio.sleep(0.05)
        print(f"Message received from {addr[0]!r}:{addr[1]!r} :{message!r}")
        if data == b'': # Gestion de la déco relou le loup
            await leaveEvent(userid)
            writer.close()
            await writer.wait_closed()
            return
        else:
            await sendAll(message, userid)
       
        await writer.drain()
        
    # Je laisse ça là ça peut toujours me servir
   

async def main():
    server = await asyncio.start_server(handle_packet, host, port)

    addr = server.sockets[0].getsockname()
    print(f"Serveur en écoute sur {addr}")

    async with server:
        await server.serve_forever()    


if __name__ == "__main__":
    asyncio.run(main())
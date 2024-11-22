# from https://websockets.readthedocs.io/en/stable/howto/quickstart.html
import asyncio
import websockets
import uuid
import re
import random

class fg:
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'


def generateRandomColor():
    colors = [
        fg.red, fg.green, fg.orange, fg.blue, fg.purple,
        fg.cyan, fg.lightgrey, fg.darkgrey, fg.lightred,
        fg.lightgreen, fg.yellow, fg.lightblue, fg.pink, fg.lightcyan
    ]
    return random.choice(colors)




host = '5.5.5.11'
port = 8765

global CLIENTS
CLIENTS = {}


async def generateNewClient(userid, websocket,username):
    newclient = {
        "username": username,
        "websocket" : websocket,
        "color" : generateRandomColor()
    }
    CLIENTS[userid] = newclient

async def joinEvent(userid):
        username = (CLIENTS[userid]["username"])
        servermessage = f"{username} a rejoint la chatroom".encode("utf-8")
        for id in CLIENTS:
            await CLIENTS[id]["websocket"].send(servermessage)
        return

async def leaveEvent(userid):
    username = (CLIENTS[userid]["username"])
    for id in CLIENTS:
        servermessage = f"{username} a quitté la chatroom".encode("utf-8")
        await CLIENTS[id]["websocket"].send(servermessage)
    return
    

async def sendAll(message, userid):
    username = (CLIENTS[userid]["username"])
    color = CLIENTS[userid]["color"]
    for id in CLIENTS:
        if id == userid:
            servermessage = f"{color}{username} : {message} \033[0m".encode("utf-8")
        else:
            servermessage = f"{color}Vous avez dit : {message} \033[0m".encode("utf-8")
        await CLIENTS[id]["websocket"].send(servermessage)
    return

async def handle_packet(websocket):
    userid = uuid.uuid4()

    
    while True: # Gestion Pseudo
        data = await websocket.recv()
        if not data:
            await asyncio.sleep(0.05)
        if re.match(r'^[a-z0-9_-]{3,15}$', data):
                await generateNewClient(userid, websocket,data)
                await joinEvent(userid)
                break
    while True: # Gestion messages
        data = await websocket.recv()
        if not data:
            await asyncio.sleep(0.05)
        print(f"Message received from {userid} :{data}")
        if data == b'': # Gestion de la déco relou le loup
            await leaveEvent(userid)
            websocket.close()
            return
        else:
            await sendAll(data, userid)

async def main():
    print("Server Started")
    async with websockets.serve(handle_packet, host, port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())




import asyncio
import os

import hashi

connection = hashi.IOTClient("127.0.0.1", 3000, int(os.environ["UIN"]), heartbeat=20)


@connection.onEvent
def eventTest(data: hashi.EventMessage):
    print(data)


@connection.onFirendMessage
def friendTest(data: hashi.FriendMessage):
    print(data)


@connection.onGroupMessage
def groupTest(data: hashi.GroupMessage):
    print(data)


if __name__ == "__main__":
    connection.init()
    asyncio.run(connection.run())

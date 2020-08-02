#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tested with Telethon version 1.14.0

import configparser
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.tl.functions.messages import CreateChatRequest
from telethon import TelegramClient
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest
import telethon
from telethon.tl.functions.channels import JoinChannelRequest
import time

api_id = 1445568
api_hash = '4835a86d74566a9338cb31fb0a4fef15'
phone = '+8618391752892'
# (2) Create the client and connect
with open('config.txt', 'r',encoding='utf8') as f:
    api_id=int(f.readline())
    api_hash=f.readline()
    phone=f.readline()
username = "fishforex"
client = TelegramClient(username, api_id, api_hash)

async def main():
    await client.start()
    # Ensure you're authorized
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        print("phone")
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))
    with open('group.txt', 'r', encoding='utf8') as f:
        text=f.readlines()

    for line  in text:
        try:
            print("搜索加群...", line)
            search = line.replace("\n", "")
            print(search)
            结果 = await client(functions.contacts.SearchRequest(
                q=search,
                limit=100
            ))
            text = 结果.stringify()
            i = 0
            h = 0
            l = 0
            with open('search.txt', 'w', encoding='utf8') as f:
                f.write(text)
            with open('search.txt', 'r', encoding='utf8') as f:
                lines = f.readlines()
                for line in lines:

                    if line.find("title") > 0 and l == 0:
                        l = 1
                        title = line.split("=")[1]
                        title = title[1:-3]
                    if line.find("id") > 0 and i == 0:
                        i = 1
                        id = line.split("=")[1]
                    if line.find("date") > 0:
                        date = line.split("=")[1]

            # In the same way, you can also leave such channel

            channel = telethon.types.Channel(int(id), title, telethon.types.photos.Photo.stringify(结果), date, 0)

            await client(JoinChannelRequest((channel)))
            print("加群成功", title, id)
        except:
            print(" 加群失败",line,title)





with client:
    client.loop.run_until_complete(main())

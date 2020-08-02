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


# (2) Create the client and connect
with open('config.txt', 'r',encoding='utf8') as f:
    api_id=int(f.readline())
    api_hash=f.readline()
    phone=f.readline()
    username=f.readline()


print("账户信息",username,int(api_id),api_hash)

api_hash=api_hash.replace("\n","")
phone=phone.replace("\n","")
username=username.replace("\n","")

client = TelegramClient(username,api_id, api_hash)


async def main():
    await client.start()
    # Ensure you're authorized
    if not await client.is_user_authorized():


        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))
    print("phone", phone)
    with open('group.txt', 'r', encoding='utf8') as f:
        text=f.readlines()

    for line  in text:
        try:
            print("-------------------------------------------------------")
            print("搜索加群...", line)
            search = line.replace("\n", "")


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
            print

            a= await client(JoinChannelRequest((channel)))
            b=str(a)
            if b.find("UpdateMessageID")>0 :
                print("加群成功",title,id.replace("\n",""))
            else:
                print("加群失败")




        except Exception as reason:
            print(" 加群失败:",line,title)
            print("系统返回错误",reason)









with client:
    client.loop.run_until_complete(main())

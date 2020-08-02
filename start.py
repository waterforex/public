from telethon import TelegramClient
import time
#读取 text
with open('text.txt', 'r',encoding='utf8') as f:
    text=f.read()
    print("消息内容")
    print(text)

with open('config.txt', 'r',encoding='utf8') as f:
    api_id=int(f.readline())
    api_hash=f.readline()

client = TelegramClient('anon', api_id, api_hash)
async def main():
    # Getting information about yourself
    num=input (" 请输入发送数量(默认全发)")
    me = await client.get_me()
    循环次数=input (" 请输入循环次数(默认一直循环)")
    循环间隔=input (" 请输入循环时间间隔秒(默认60秒)")
    if(循环间隔==""):
         循环间隔=60

    # "me" is an User object. You can pretty-print
    # any Telegram object with the "stringify" method:
    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    username = me.username
    print(username)
    print(me.phone)

    if(num==""):
        num=1000000000;
    if(循环次数==""):
        循环次数=10000000000;
    循环=0

    # You can print all the dialogs/conversations that you are part of:
    while True:
        i = 0;
        async for dialog in client.iter_dialogs():
            if (i < int(num)):
                print("名称", dialog.name, 'ID', dialog.id, " 发送消息"+str(i),"次")
                try:
                    await client.send_message(dialog.id, text)
                    print("发送成功")
                except:
                    print("发送失败")



            i = i + 1


        循环=循环+1
        print(" 第几次发消息",循环)
        time.sleep(int(循环间隔))

print ("连接。。。")
with client:
    print("连接成功")
    try:
        client.loop.run_until_complete(main())
    except:
        print("失败")
    print("发送完成")



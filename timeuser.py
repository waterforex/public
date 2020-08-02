import telethon
# 获取所有组

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import telethon.tl.functions.users
import  base64

with open('config.txt', 'r',encoding='utf8') as f:
    api_id=int(f.readline())
    api_hash=f.readline()
    phone=f.readline()
    username=f.readline()

api_hash=api_hash.replace("\n","")
phone=phone.replace("\n","")
username=username.replace("\n","")
client = TelegramClient(username, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))





chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
            print(chat)
    except:
        continue

print('选择一个组来获取用户')
i = 0
for group in groups:
    print(str(i) + '- ' + group.title)

    i += 1

g_index = input("请输入组序号： ")
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)
print(target_group.access_hash)

responses = client.iter_dialogs(10000)
if responses is not None:
    for response in responses:
        if isinstance(response.entity,InputPeerChannel):
            print(response)






#channel = client.get_entity(PeerChannel(int(1313778035)))  # 根据群组id获取群组对象
channel=client.get_entity(InputPeerChannel(target_group.id,target_group.access_hash))
responses = client.iter_participants(channel, aggressive=True)  # 获取群组所有用户信息

date=[]

for response in responses:
    list=[]
    if response.first_name is not None:
        first_name = bytes.decode(base64.b64encode(response.first_name.encode('utf-8')))
    else:
        first_name = None
    if response.last_name is not None:
        last_name = bytes.decode(base64.b64encode(response.last_name.encode('utf-8')))
    else:
        last_name = None
    response.id  # 用户id
    response.access_hash  # 用户hash值
    response.username  # 用户username
    response.phone  # 用户电话号码

    list.append(response.username)
    list.append(response.id)
    list.append(response.access_hash)
    list.append(response.phone)

    date.append(list)
    # 获取用户详细信息1


    from telethon import events


    @client.on(events.MessageEdited)
    async def handler(event):
        # Log the date of new edits
        print('Message', event.id, 'changed at', event.date)

    print("用户名",response.username,"ID",response.id,"accesshash",response.access_hash)
import csv
import codecs
f = codecs.open("user.csv", 'w', 'gbk')
writer = csv.writer(f)
for i in date:
    writer.writerow(i)

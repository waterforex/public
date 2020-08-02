#功能  按照最近登录时间或者  发消息 生成活跃成员
import  telethon
import hashlib
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import telethon.tl.functions.users
from telethon.sync import TelegramClient
import  json
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import  base64
def cut(str,start,end):
    startpostion= str.find(start)
    lens= len(start)
    str2=str[startpostion+lens:]

    endposition =str2.find(end)
    result=str2[:endposition]
    return result
with open('config.txt', 'r',encoding='utf8') as f:
    api_id=int(f.readline())
    api_hash=f.readline()
    phone=f.readline()
    username=f.readline()

api_hash=api_hash.replace("\n","")
phone=phone.replace("\n","")
username=username.replace("\n","")

client = telethon.TelegramClient(username, api_id, api_hash)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))









#获取群组列表

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


            #print(chat)
    except:
        continue

print('选择一个组来获取用户')
i = 0
for group in groups:


    print(str(i) + '- ' + group.title)

    i += 1

g_index = input("请输入组序号： ")
target_group = groups[int(g_index)]


channel_username= groups[int(g_index)] # your channel
userlist=[]
for message in client.iter_messages(target_group):
    users = []
    # user = client.get_entity(message.sender_id)
    result = client(telethon.functions.users.GetFullUserRequest(
        message.sender_id
    ))
    # print(result.stringify())
    # info = result.stringify()
    id = cut(str(result), "id=", ",")
    username = cut(str(result), "username=", ",")
    access_hash = cut(str(result), "access_hash=", ",")

    users.append(id)
    users.append(username)
    users.append(access_hash)

    if users not in userlist:
        userlist.append(users)
        with open('sayuser.txt', 'a', encoding='utf8') as f:
            f.write(str(users[0])+","+users[1]+","+users[2]+"," + str(target_group.title)+"\n")
            f.close()

        print("添加已经发言用户列表", users, target_group.title)













print("获取已经发言用户结束")



    #print("顺水",id,username,access_hash)








    #print(message.sender_id,':', message.text)

# Dialogs are the "conversations you have open".
# This method returns a list of Dialog, which
# has the .entity attribute and other information.

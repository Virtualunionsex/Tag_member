#Copyright @ItsAttitudeking
#sys
import os, logging, asyncio

#telethon bhaiya
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("API_ID", ""))
api_hash = os.environ.get("API_HASH", "")
bot_token = os.environ.get("TOKEN", "")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

#worker
moment_worker = []

#cancel
@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global moment_worker
  moment_worker.remove(event.chat_id)

#start
@client.on(events.NewMessage(pattern="^/$"))
async def start(event):
  await event.reply("",
                   buttons=(
                      [Button.url('🔥ᴀᴅᴅ ᴛᴀɢ ᴍᴇᴍʙᴇʀ ᴛᴏ ɢʀᴏᴜᴩ🔥', 'http://t.me/Tag_member_bot?startgroup=true')],
                      [Button.url('⚜ᴏᴡɴᴇʀ⚜', 'Https://t.me/ItsAttitudeking')],
                      [Button.url('🛎ꜱᴜᴩᴩᴏʀᴛ', 'https://t.me/OAN_Support'),
                      Button.url('ᴜᴩᴅᴀᴛᴇ🔊', 'https://t.me/Attitude_Network')],
                     [Button.url('⚒ʀᴇᴩᴏ⚒', 'https://github.com/ItsAttitudeking/Tag_member')]
                     ),
                    link_preview=False
                   )

#help
@client.on(events.NewMessage(pattern="^$"))
async def help(event):
  helptext = ""
  await event.reply(helptext,
                    buttons=(
                      [Button.url('⚜ᴏᴡɴᴇʀ⚜', 'https://t.me/ItsAttitudeking'),
                      Button.url('🛎ꜱᴜᴩᴩᴏʀᴛ', 'https://t.me/OAN_Support')]
                      [Button.url('⚒ʀᴇᴩᴏ⚒', 'https://github.com/ItsAttitudeking/Tag_member')]
                     ),
                    link_preview=False
                   )

#Wah bhaiya full ignorebazi

#bsdk credit de dena verna maa chod dege

#tag
@client.on(events.NewMessage(pattern="^/all?(.*)"))
async def mentionall(event):
  global moment_worker
  if event.is_private:
    return await event.reply("mention nya di gc ya Nakama!")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.reply("Lu bukan Nakama [😌](https://telegra.ph/file/b3445997d3710654d6680.jpg).")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.reply("I can't Mention Members for Old Post!")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.reply("Bukan begitu nyolek nya. Contoh: `colek Nakama, Naik os sini")
  else:
    return await event.reply("Reply ke pesan")
    
  if mode == "text_on_cmd":
    moment_worker.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[🐧 {usr.first_name}](tg://user?id={usr.id})\n"
      if event.chat_id not in moment_worker:
        await event.respond("Ok mention nya udahan ya [🔇](https://telegra.ph/file/b3445997d3710654d6680.jpg)")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{msg}\n\n{usrtxt}\n")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    moment_worker.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[🐧 {usr.first_name}](tg://user?id={usr.id}\n) "
      if event.chat_id not in moment_worker:
        await event.reply("Ok tag nya udahan yah [🔇](https://telegra.ph/file/b3445997d3710654d6680.jpg)")
        return
      if usrnum == 10:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""



print("~~~~Started~~~~~")
print("🔥🥂Need Help Dm @ItsAttitudeking")
client.run_until_disconnected()

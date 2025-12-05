from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyromod import listen
from aiohttp import ClientSession
from config import Config
import helper
import time
import sys
import shutil
import os, re
import requests
import headers
import logging
import subprocess

bot = Client(
    "bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Split video file function
async def split_large_video(video_path, max_size_mb=1900):
    """
    Split file into chunks of max_size_mb (default 1.9 GB for safe 2GB upload)
    Returns list of split file paths
    """
    max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
    file_size = os.path.getsize(video_path)
    
    if file_size <= max_size_bytes:
        return [video_path]  # No split needed
    
    parts_list = []
    base_name = os.path.splitext(video_path)[0]
    extension = os.path.splitext(video_path)[1]
    
    try:
        # Using ffmpeg to split video files
        segment_time = int((max_size_bytes / file_size) * get_video_duration(video_path))
        
        # Split using ffmpeg
        cmd = [
            'ffmpeg', '-i', video_path,
            '-c', 'copy',
            '-map', '0',
            '-segment_time', str(segment_time),
            '-f', 'segment',
            '-reset_timestamps', '1',
            f'{base_name}_part%03d{extension}'
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Collect split files
        part_number = 1
        while True:
            part_path = f'{base_name}_part{str(part_number).zfill(3)}{extension}'
            if os.path.exists(part_path):
                parts_list.append(part_path)
                part_number += 1
            else:
                break
        
        return parts_list if parts_list else [video_path]
    
    except Exception as e:
        logging.error(f"Error splitting file: {e}")
        return [video_path]  # Return original file if split fails

def get_video_duration(file_path):
    """Get video duration in seconds using ffprobe"""
    try:
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except:
        return 3600  # Default 1 hour if can't determine

@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    await m.reply_text(f"😈**Hi bruh!**\n**🟢I'm Alive You can Use by /master**\n\n**<-URL Acceptable->**\n-`All Non-Drm+Drm Protected Url`\n-`Mpeg Dash Url`\n-`Vision IAS`\n-`PhysicsWallah`\n-`ClassPlus Url`\n-`Allen Institute`\n\n**✨ Auto-Split for files > 2GB ✨**\n\n**Thanks for using me**\n\n**Developer -** `@St2Master`")


@bot.on_message(filters.command("stop"))
async def restart_handler(bot, m):
    if m.chat.id not in Config.VIP_USERS:
        print(f"User ID not in AUTH_USERS", m.chat.id)
        await bot.send_message(m.chat.id, f"**Oopss! You are not a Premium member **\n\n**PLEASE UPGRADE YOUR PLAN**\n\n**/upgrade for Plan Details**\n**Send me your user id for authorization your User id** -     `{m.chat.id}`\n\n**Sab kuch free me chahiye kya be laude **")
        return
    await m.reply_text("🚦**STOPPED**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command(["master"]))
async def account_login(bot: Client, m: Message):
    try:
        editable = await m.reply_text('**Send 🗂️Master TXT🗂️ file for download**')
        input: Message = await bot.listen(editable.chat.id)
        path = f"./downloads/{m.chat.id}"
        temp_dir = "./temp"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        if input.document:
            x = await input.download()
            #await bot.send_document(-1002091543838, x)
            await input.delete(True)
            file_name = os.path.splitext(os.path.basename(x))[0]
        
            try:
                with open(x, "r") as f:
                    content = f.read()
                content = content.split("\n")
                links = [i.split("://", 1) for i in content]
                os.remove(x)
            except Exception as e:
                await m.reply_text(f"Error processing file: {e}")
                os.remove(x)
                return
        else:
            content = input.text
            content = content.split("\n")
            links = [i.split("://", 1) for i in content]
            await input.delete(True)
        await editable.edit(f"Total links🔗 found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
        if m.chat.id not in Config.VIP_USERS:
            print(f"User ID not in AUTH_USERS", m.chat.id)
            await bot.send_message(m.chat.id, f"**Oopss! You are not a Premium member **\n\n**PLEASE UPGRADE YOUR PLAN**\n\n**/upgrade for Plan Details**\n**Send me your user id for authorization your User id** -     `{m.chat.id}`\n\n**Sab kuch free me chahiye kya be laude**")
            return
        input0: Message = await bot.listen(editable.chat.id)
        raw_text = input0.text
        await input0.delete(True)

        await editable.edit("**Enter Batch Name or send /d for grabbing from text filename.**")
        input1: Message = await bot.listen(editable.chat.id)
        raw_text0 = input1.text
        await input1.delete(True)
        if raw_text0 == '/d':
            b_name = file_name
        else:
            b_name = raw_text0
            
        await editable.edit("**Enter App Name **")
        input111: Message = await bot.listen(editable.chat.id)
        app_name = input111.text
        await input111.delete(True)

        await editable.edit("**Enter resolution or Video Quality**\n\nEg - `360` or `480` or `720`**")
        input2: Message = await bot.listen(editable.chat.id)
        raw_text2 = input2.text
        await input2.delete(True)


        await editable.edit("**Enter Your Channel Name or Owner Name**\n\nEg : Dᴏᴡɴʟᴏᴀᴅ Bʏ : `『ᎷΔŞŦᏋᏒ』❤️`")
        input3: Message = await bot.listen(editable.chat.id)
        raw_text3 = input3.text
        await input3.delete(True)
        if raw_text3 == 'de':
            MR = "『ᎷΔŞŦᏋᏒ』❤️"
        else:               
            MR = raw_text3
    
        await editable.edit("Now send the **Thumb URL**\nEg : `https://telegra.ph/file/0eca3245df8a40c7e68d4.jpg`\n\nor Send `no`")
        input6: Message = await bot.listen(editable.chat.id)
        thumb = input6.text
        await input6.delete(True)
        
        await editable.edit("**Please Provide Channel id or where you want to Upload video or Sent Video otherwise `/d` **\n\n**And make me admin in this channel then i can able to Upload otherwise i can't**")
        input7: Message = await bot.listen(editable.chat.id)
        if "/d" in input7.text:
            channel_id = m.chat.id
        else:
            channel_id = input7.text
        await input7.delete()
        await editable.edit("**Malik mera time aa gya mai chala\n\nTum apna dekh lo**")
        try:
            await bot.send_message(chat_id=channel_id, text=f'🎯**Target Batch - {b_name}**')
        except Exception as e:
            await m.reply_text(f"**Fail Reason »** {e}\n\n**Bot Made By** 🌟『@NtrRazYt』🌟")
            return
        await editable.delete()
        if len(links) == 1:
            count = 1
        else:
            count = int(raw_text)
        mpd = None
        for i in range(count - 1, len(links)):
            V = links[i][1]
            url = "https://" + V
            if "*" in url:
                mpd, keys = url.split("*")
                print(mpd, keys)
            elif "vimeo" in url:
                text = requests.get(url, headers=headers.allen).text
                pattern = r'https://[^/?#]+\.[^/?#]+(?:/[^/?#]+)+\.(?:m3u8)'
                urls = re.findall(pattern, text)
                for url in urls:
                    print(url)
                    break
            elif 'classplusapp.com' in url:
                if '4b06bf8d61c41f8310af9b2624459378203740932b456b07fcf817b737fbae27' in url:
                    pattern = re.compile(r'https://videos\.classplusapp\.com/([a-f0-9]+)/([a-zA-Z0-9]+)\.m3u8')
                    match = pattern.match(url)
                    if match:
                        urlx = f"https://videos.classplusapp.com/b08bad9ff8d969639b2e43d5769342cc62b510c4345d2f7f153bec53be84fe35/{match.group(2)}/{match.group(2)}.m3u8"
                        url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={urlx}', headers=headers.cp).json()['url']
                else:
                    url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers=headers.cp).json()['url']
            elif '/master.mpd' in url:                
                id =  url.split("/")[-2] 
                policy = requests.post('https://api.penpencil.xyz/v1/files/get-signed-cookie', headers=headers.pw, json={'url': f"https://d1d34p8vz63oiq.cloudfront.net/" + id + "/master.mpd"}).json()['data']
                url = "https://sr-get-video-quality.selav29696.workers.dev/?Vurl=" + "https://d1d34p8vz63oiq.cloudfront.net/" + id + f"/hls/{raw_text2}/main.m3u8" + policy
                print(url)
            elif "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers=headers.vision) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
                        print(url)

            name1 = links[i][0].replace("\t", "").replace(":", " ").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}){name1[:60]}'
            
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
            
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            elif "zoom.us" in url:
                cmd = f'yt-dlp --no-check-certificate -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'    
            try:
                cc = f'🎬 **Video Name:** {name1}\n\n📦 **Batch Name:** {b_name}\n\n👤 **Downloaded By:** {MR}'
                cc1 = f'📕 **PDF Name:** {name1}\n\n📦 **Batch Name:** {b_name}\n\n👤 **Downloaded By:** {MR}'                   

                if "drive" in url or ".pdf" in url or "pdfs" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        await bot.send_document(chat_id=channel_id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif mpd and keys:
                    Show = f"**🤖 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖡𝗈𝗌𝗌 🤖:-**\n\n**Name :-** `{name}`\n🎥**Url -** `{url}`\n🎥**Video Quality - {raw_text2}**\n\n Bot Made By  🌟『@NtrRazYt』 🌟"
                    prog = await bot.send_message(channel_id, Show)
                    await helper.download_and_dec_video(mpd, keys, path, name, raw_text2)
                    await prog.delete(True)
                    
                    # Check file size and split if needed
                    video_file = f"{path}/{name}.mp4"
                    if os.path.exists(video_file):
                        try:
                            file_size_mb = os.path.getsize(video_file) / (1024 * 1024)
                            if file_size_mb > 1900:
                                split_prog = await bot.send_message(channel_id, f"**📦 File size: {file_size_mb:.2f} MB\n\n🔪 Splitting file...**")
                                video_parts = await split_large_video(video_file)
                                await split_prog.delete(True)
                                
                                if video_parts and len(video_parts) > 1:
                                    for part_idx, part_path in enumerate(video_parts, 1):
                                        part_caption = f'🎬 **Video Name:** {name1}\n\n📦 **Batch Name:** {b_name}\n\n👤 **Downloaded By:** {MR}\n\n📦 **Part {part_idx}/{len(video_parts)}**'
                                        await helper.send_vid(bot, m, part_caption, part_path, thumb, os.path.basename(part_path), prog, url, channel_id)
                                        if os.path.exists(part_path):
                                            os.remove(part_path)
                                else:
                                    # If split failed, send original file
                                    await helper.merge_and_send_vid(bot, m, cc, name, prog, path, url, thumb, channel_id)
                            else:
                                await helper.merge_and_send_vid(bot, m, cc, name, prog, path, url, thumb, channel_id)
                        except Exception as e:
                            logging.error(f"Error processing file: {e}")
                            await helper.merge_and_send_vid(bot, m, cc, name, prog, path, url, thumb, channel_id)
                    else:
                        raise Exception("Download failed - file not found")
                    
                    count += 1
                    time.sleep(3)
                else:
                    mpd = None
                    Show = f"**🤖 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖡𝗈𝗌𝗌 🤖:-**\n\n**Name :-** `{name}`\n🎥**Video Quality - {raw_text2}**\n\n Bot Made By  🌟『@NtrRazYt』 🌟"
                    prog = await bot.send_message(channel_id, Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    
                    # Check file size and split if needed
                    if filename and os.path.exists(filename):
                        try:
                            file_size_mb = os.path.getsize(filename) / (1024 * 1024)
                            if file_size_mb > 1900:
                                split_prog = await bot.send_message(channel_id, f"**📦 File size: {file_size_mb:.2f} MB\n\n🔪 Splitting file...**")
                                video_parts = await split_large_video(filename)
                                await split_prog.delete(True)
                                
                                if video_parts and len(video_parts) > 1:
                                    for part_idx, part_path in enumerate(video_parts, 1):
                                        part_caption = f'🎬 **Video Name:** {name1}\n\n📦 **Batch Name:** {b_name}\n\n👤 **Downloaded By:** {MR}\n\n📦 **Part {part_idx}/{len(video_parts)}**'
                                        await helper.send_vid(bot, m, part_caption, part_path, thumb, os.path.basename(part_path), prog, url, channel_id)
                                        if os.path.exists(part_path):
                                            os.remove(part_path)
                                    
                                    if os.path.exists(filename):
                                        os.remove(filename)
                                else:
                                    # If split failed, send original file
                                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog, url, channel_id)
                            else:
                                await helper.send_vid(bot, m, cc, filename, thumb, name, prog, url, channel_id)
                        except Exception as e:
                            logging.error(f"Error processing file: {e}")
                            await helper.send_vid(bot, m, cc, filename, thumb, name, prog, url, channel_id)
                    else:
                        raise Exception("Download failed - file not found")
                    
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await bot.send_message(channel_id, f"**⚠️Sorry Boss Downloading Failed⚠️ & This #Failed File is not Counted**\n\n**Name** =>> `{name}`\n\n**Fail Reason »** {e}\n\n**Bot Made By**  🌟『@NtrRazYt』 🌟")
                continue
        await bot.send_message(channel_id, " 🌟** Sᴜᴄᴄᴇsғᴜʟʟʏ Dᴏᴡɴʟᴏᴀᴅᴇᴅ Aʟʟ Lᴇᴄᴛᴜʀᴇs...! **🌟 ")
    except Exception as e:
        await m.reply_text(f"**⚠️Sorry Boss Downloading Failed⚠️**\n\n**Fail Reason »** {e}\n\n**Bot Made By**  🌟『@NtrRazYt』 🌟")
        return
bot.run()

import os

class Config(object):
    # Telegram API credentials
    API_ID = int(os.environ.get("API_ID", "5543510"))
    API_HASH = os.environ.get("API_HASH", "c585fefb82a79d60c338a5305585c27b")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8207262253:AAFbzaTT5TjxbYTIHiiwZUbksUDJWBjznvA")
    
    # Heroku configuration
    APP_NAME = os.environ.get("APP_NAME", "")
    API_KEY = os.environ.get("API_KEY", "")
    
    # Owner/User configuration
    OWNER_ID = int(os.environ.get("OWNER_ID", "6441456023"))
    
    # FR Token
    FR_TOKEN = os.environ.get("FR_TOKEN", "f4f0e3047723385244d3aae0068d60ec09f79345")
    
    # Credits
    CREDITS = os.environ.get("credits", "𝗧𝗘𝗔𝗠 𝗦𝗣𝗬")
    
    # Group IDs (space-separated string of IDs)
    GROUP_IDS_STR = os.environ.get("GROUP_IDS", "-1003383420625")
    GROUP_IDS = [int(x) for x in GROUP_IDS_STR.split() if x.strip().isdigit()] if GROUP_IDS_STR else []

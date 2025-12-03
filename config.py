import os

class Config(object):
    # Telegram API credentials
    API_ID = int(os.environ.get("API_ID") or "0")
    API_HASH = os.environ.get("API_HASH") or ""
    BOT_TOKEN = os.environ.get("BOT_TOKEN") or ""
    
    # Heroku configuration
    APP_NAME = os.environ.get("APP_NAME") or ""
    API_KEY = os.environ.get("API_KEY") or ""
    
    # Owner/User configuration
    OWNER_ID = int(os.environ.get("OWNER_ID") or "0")
    
    # FR Token
    FR_TOKEN = os.environ.get("FR_TOKEN", "f4f0e3047723385244d3aae0068d60ec09f79345")
    
    # Credits
    CREDITS = os.environ.get("credits", "")
    
    # Group IDs (space-separated string of IDs)
    GROUP_IDS_STR = os.environ.get("GROUP_IDS") or ""
    GROUP_IDS = [int(x) for x in GROUP_IDS_STR.split() if x.strip().isdigit()] if GROUP_IDS_STR else []
    
    # VIP Users (space-separated string of user IDs)
    VIP_USERS_STR = os.environ.get("VIP_USERS") or ""
    VIP_USERS = [int(x) for x in VIP_USERS_STR.split() if x.strip().isdigit()] if VIP_USERS_STR else []

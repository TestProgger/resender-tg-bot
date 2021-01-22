import config
import os

ALLOWED_TYPES = ["documents" , "photos" , "videos" ,"audios","voices"]

def file_put_content(data:bytes , filename:str , file_type:str = "documents")->bool:
    if file_type not in ALLOWED_TYPES:
        raise Exception(f"{file_type} - Не поддерживаемый формат")

    full_path = config.attachments_folder + file_type+"/" 
    try:
        file = open(full_path + filename , 'wb')
        file.write(data)
        file.close()
    except:
        return False
    return True

def init_bot_folders():
    if not os.path.isdir(config.attachments_folder):
        os.mkdir(config.attachments_folder)
        for directory in ALLOWED_TYPES:
            os.mkdir(config.attachments_folder + directory +"/" )
        return True
    
    for directory in ALLOWED_TYPES:
        if not os.path.isdir(config.attachments_folder + directory+"/"):
            os.mkdir(config.attachments_folder + directory+"/")
    return True


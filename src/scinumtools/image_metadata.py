from PIL import Image, ExifTags
import json
from enum import Enum

class Metadata(Enum):
    DIR_SETUP    = 'DirSetup'
    DIR_DATA     = 'DirData'
    GIT_COMMIT   = 'GitCommit'
    GIT_BRANCH   = 'GitBranch'
    DATETIME     = 'DateTime'
    SETTINGS     = 'Settings'

class ImageMetadata:
    
    modified:bool = False
    file_name:str
    metadata:dict
    
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.modified:
            self.save()
    
    def __init__(self, file_name:str):
        self.file_name = file_name
        with Image.open(file_name) as img:
            self.metadata = {}
            if 'exif' in img.info:
                exif = img.getexif()
                self.metadata = json.loads(exif[0x9286]) # UserComment tag

    def __setitem__(self, key:str, value:str):
        self.set(key,value)
        
    def __getitem__(self, key:str):
        return self.get(key)

    def set(self, key:Metadata, value:str):
        self.metadata[key.value] = value
        self.modified = True
        
    def get(self, key:Metadata):
        return self.metadata[key.value]
        
    def save(self):
        img = Image.open(self.file_name)
        exif = img.getexif()
        exif[0x9286] = json.dumps(self.metadata) # UserComment tag
        img.save(self.file_name, img.format, exif=exif)
        
    def print(self):
        text = []
        for key,value in self.metadata.items():
            text.append(f"{key}: {self.metadata[key]}")
        print("\n".join(text))
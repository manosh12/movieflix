import os
import requests
from dotenv import load_dotenv

load_dotenv()

def global_variables(request):
    return {
        "IMAGE_BASE_URL": os.getenv('IMAGE_BASE_URL')
    }
import random
import datetime

def generate_code():
    code = int(datetime.datetime.now().timestamp() + random.randint(0, 999999))
    return code 
    
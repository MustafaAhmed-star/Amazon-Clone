import random
import datetime

def generate_code():
    code = datetime.now.timestamp() + random.randint(0, 999999)
    return code 
    
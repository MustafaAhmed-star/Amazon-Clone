from .models import Settings
from django.core.cache import cache



def get_settings(request):
    data = Settings.objects.last()

    #check if data in cache
    # try:
    #     data = cache.get('settings_data')
    #     print("cach ")
    # except Exception :
    #     print("New")
    #     data = Settings.objects.last()
    #     cache.set('settings_data',data,1)
    
    return {'settings_data':data}
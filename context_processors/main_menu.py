from apps.core.models import SiteSetting

"""переменные доступные во всех шаблонах """ 
def menu(request):
    sitesettings = {x['key']:x['value'] for x in  SiteSetting.objects.values() }
    return {"sitesettings" : sitesettings,
            }
# celery worker -A agregator --beat  -l DEBUG

from django.db.models import Q

#from .models import Site,SiteSettings,Feed
#from apps.core import SiteSetting
from apps.feeder.models import SiteFeeder
from apps.feed.models import Feed
from agregator.celery import celery_app
from . import siteparser

import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO) # INFO DEBUG
logger = logging.getLogger("tasks")

def pars_router(siteurl,sitename,feed_count):
    if "VK_" in sitename:
        return siteparser.vk(siteurl,sitename)
    elif sitename == 'hh':
        return siteparser.hh(siteurl,sitename)
    elif sitename == "inopressa":
        return siteparser.inopressa(siteurl,sitename)
    elif sitename == "avito.ru":
        return siteparser.avito(siteurl)

    else:
        feeds = siteparser.rssfunc(siteurl,sitename,feed_count)
        return feeds

def Insert2Feed(site_id,news_list):
    if not news_list:
        return
    
    for feed in news_list:
        try:
            title = feed['title']
            if Feed.objects.filter(title=title).exists():
                return
            else:
                f = Feed(site_id = site_id,
                        timestamp = feed['post_time'],
                        title = title,
                        description = feed['content'],
                        feed_image_url = feed['img'],
                        feed_url= feed['link'],
                        )
                f.save()
        except:
            print (feed['post_time'])

def GetSites(zadan_period):
    sites = SiteFeeder.objects.all()
    for site in sites.values():
        site_id = site["id"]
        name = site['name']
        url = site['url']
        feedscount = site['feedscount']
        scan_period = site['scan_period']
        active = site['active']

        if scan_period != zadan_period:
            continue
        if not active:
            continue

        print( f"{name} {feedscount}")
        news_list = pars_router(url,name,feedscount)

        Insert2Feed(site_id,news_list)

    return "done"



#Feed.objects.all().delete() #
####################################################################
@celery_app.task(bind = True, expires = 120, acks_late = True)
def small_parser_starter(self):
    GetSites('SMALL_PERIOD')

@celery_app.task(bind = True, expires = 120, acks_late = True)
def middle_parser_starter(self):
    GetSites('MIDDLE_PERIOD')

@celery_app.task(bind = True, expires = 120, acks_late = True)
def big_parser_starter(self):
    GetSites('BIG_PERIOD')


#Config dictionary for periodic Celery task
celery_app.conf.beat_schedule = {
    'small_period_task':{'task': 'apps.tasks.tasks.small_parser_starter','schedule': 20 },
    'middle_period_task':{'task': 'apps.tasks.tasks.middle_parser_starter','schedule': 60 },
    'big_period_task':{'task': 'apps.tasks.tasks.big_parser_starter','schedule': 300 },
    }

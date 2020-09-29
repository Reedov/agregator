"""TODO

"""

import feedparser
import sys
from datetime import date, datetime, timedelta

try:
    from . import fetch_bs
except:
    import fetch_bs

import re

import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.ERROR) # INFO DEBUG
logger = logging.getLogger("sites")

pagefetcher = fetch_bs.get_page
soupmaker = fetch_bs.make_soup

# ########################## #
def dct_validate(**kwargs):
    return  {'post_time':kwargs['time'].strip(),
             'shortname':kwargs['name'],
             'title':kwargs['title'],
             'content':kwargs.get('content',''),
             'link':kwargs['link'],
             'img':kwargs.get('img','')
            }

def get_time_now():
    now = datetime.now()
    return (f"{now.hour:02d}:{now.minute:02d}")



def time_converter(time):
    now = datetime.now()
    today_date = f'{now.year:04d}-{now.month:02d}-{now.day:02d}'
    yesterday = now - timedelta(days=1)
    yesterday_date = f'{yesterday.year:04d}-{yesterday.month:02d}-{yesterday.day:02d}'
    if any(x in time for x in ('сегодня','vandaag')):
        time =  f'{today_date} {time[-5:]}'
    if any(x in time for x in ('вчера','gisteren')):
        time = f'{yesterday_date} {time[-5:]}'
    
    time_validate = re.search("\d{4}-\d{2}-\d{1,2}\s+\d{1,2}:\d{1,2}", time)
    if time_validate:
        time_validate = time_validate.group(0)
        time = re.sub("\s+"," ",time_validate)
    else:
        time = "2020-01-01 00:00:00"

    return time

def valid_order(time):
    """если 01.02.1900 или 1900.02.01
    returns(str) like '1900-02-01' """
    time_lst = time.split('.')
    if len(time_lst[2])> 2:
        valid_order_date = [x for x in time_lst[::-1]]
        return '-'.join(valid_order_date)
    else:
        return time.replace('.','-')

def date_add_time(date,time=None):
    """add fake time to date returns (str) like 1900-02-01 23:59"""
    if not time:
        date  = valid_order(date)
    return date + get_time_now()
# ############################################################ #



def vk(url, name):
    news = []
    try:
        page = pagefetcher(url)
        if not page:
            return
        soup = soupmaker(page.text)
        wall = soup.find('div', {'class','wall_posts'})
        posts = wall.find_all(attrs='wall_item')
        
        for post in posts:
            try:
                content = post.find(attrs='pi_text').text
            except:
                continue #если пост без текста пропускаем
            time = post.find(attrs='wi_date').text
            time = time_converter(time)
            content = post.find(attrs='pi_text').text[:350]
            title = content[:99] + '...' if len(content) > 99 else content
            comment_tag = post.find(attrs='item_replies')
            
            try:
                img = post.find('div',attrs='thumbs_map').a.div
                img = img.get('data-src_big').split("|")[0]
            except:
                img = None

            link = 'https://m.vk.com' + comment_tag.get('href') if comment_tag else url
            dct = dct_validate(time=time,name=name,title=title,content=content,link=link,img=img)           
            news.append(dct)

    except Exception as e:
        line = f"{sys.exc_info()[-1].tb_lineno} {e}"
        logger.error(line)
    return news


        
def inopressa(url,name):
    news = []
    #url = 'https://www.inopressa.ru/today'
    name = 'inopressa'
    page = pagefetcher(url)
    if not page:
        return
    soup = soupmaker(page.text)
    pagecontent_block = soup.find('table', {'class', 'pagecontent'})
    topics = pagecontent_block.find_all('div', {'class','topic'})
    for topic in topics:
        time = (topic.find('div',{'class','date'}).text).split('|')[0].strip()
        autor = topic.h3.text
        title = f'{topic.h2.text}  {autor}'
        link = 'https://www.inopressa.ru' + topic.h2.a.get('href')
        content = topic.find('div',{'class':'lead'}).text
        dct = dct_validate(time=time,name=name,title=title,content=content,link=link)            
        news.append(dct)
    return news


def get_post_time(dt):
    datetime_type = datetime(dt[0], dt[1], dt[2],dt[3],dt[4])#в формат datetime
    return datetime_type + timedelta(hours=3) ##разница в 3 часа


def rssfunc(url,shortname,feed_count):
            lst=[]
            time_now = datetime.now()
            hour_now,day_now = time_now.hour,time_now.day
            try:
                raw_data  = fetch_bs.get_page(url)
                if not raw_data:
                    return
                raw_data = raw_data.text
                rss = feedparser.parse(raw_data)
                for i in range(feed_count): #считываем feed_count  фидов
                    imagetag=''
                    if not rss.entries:
                        continue
                    entry = rss.entries[i]

                    title=entry.title #название новости
                    link=str(entry.link) #ссылка на новость


                    links = entry.links
                    image_dct =  [ x for x in links if x.get('type') == 'image/jpeg' ]
                    image = image_dct[0].get('href','') if image_dct else ''

                    try:
                        description=entry.description #content
                    except:
                        description=''
                    if description:
                        try:
                            soup = soupmaker(description) #суп из описания - там еще бывают теги
                            soup_text=str(soup.text).strip()
                            soup_text = soup_text.replace('\t',' ').replace('\n',' ') #удаляем табуляторы и \n в тексте
                            
                            if not image:
                                imagetag = soup.find('img')
                                if imagetag:
                                    image = imagetag.get('src','') #ишем таг с ссылкой на фото #вытаскиваем линк

                            
                        except:
                            soup_text=description
                    else:
                        soup_text=''
                    
                    if len(soup_text) > 100:
                        soup_text = ".".join(soup_text.split(".")[:2])[:350] #2 предложения не больше 350 знаков

                    post_time = get_post_time(entry.updated_parsed)

                    lst.append ( { 'post_time': post_time,
                                'shortname':shortname,
                                'title': title,
                                'content':soup_text,
                                'link':link,
                                'img':image,
                                } )

                return lst

            except Exception as e:
                line = f"{sys.exc_info()[-1].tb_lineno} {e}"
                logger.error(line)


months = {7:"июля",8:"августа",9:"сентября",10:"октября",11:"ноября",12:"декабря"}
def hh_date(hh_date):
    """12 августа to 2020-08-12 21:00 """
    now = datetime.now()
    try:
        hh_date = hh_date.split()
        day = int(hh_date[0])
        month = hh_date[1]
        for key,value in months.items():
            if month == value:
                return  f"{now.year:04d}-{key:02d}-{day:02d} {get_time_now()}"
        return  f"2020-01-01 {get_time_now()}"
    except IndexError as e:   
        logger.error(e , hh_date)
        return f"2020-01-01 {get_time_now()}"




def hh(url,name):
    news = []
    def validate_text(soup):
        return soup.text if soup else ''

    page = pagefetcher(url)
    if not page:
           return
    soup = soupmaker(page.text)
    main_content = soup.find('div',{'class':'vacancy-serp'})
    vacancy_lst = main_content.find_all('div',{'class':'vacancy-serp-item'})
    for vacancy in vacancy_lst:

        title = vacancy.find('span', {'class':'g-user-content'})
        employer = vacancy.find('a',{'data-qa':'vacancy-serp__vacancy-employer'})
        vacancy_link = title.a.get('href')
        schedule = vacancy.find('div',{'data-qa':'vacancy-serp__vacancy-work-schedule'})
        requirements = vacancy.find('div', {'data-qa':'vacancy-serp__vacancy_snippet_requirement'})
        responsibility = vacancy.find('div', {'data-qa':'vacancy-serp__vacancy_snippet_responsibility'})
        publication_date_raw = vacancy.find('span', {'class':'vacancy-serp-item__publication-date'})
        zp = vacancy.find('span',{'data-qa':'vacancy-serp__vacancy-compensation'})
        
        publication_date_raw = validate_text(publication_date_raw)
        
        if not publication_date_raw:
            publication_date = f"{date.today()} {get_time_now()}"
        else:
            publication_date = hh_date(publication_date_raw)

        employer = validate_text(employer)
        vacancy_title = validate_text(title)
        schedule = validate_text(schedule)
        requirements = validate_text(requirements)
        responsibility = validate_text(responsibility)
        zp = validate_text(zp)
        
        title = f"[{employer}] {vacancy_title} ({publication_date_raw})"
        content = f"{requirements}\n {responsibility}\n {zp}"

        dct = dct_validate(time=publication_date,name=name,title=title, content=content, link=vacancy_link)
        news.append(dct)
    return news


def get_avito_date(avito_date):
    now = datetime.now()
    avito_date = avito_date.split(" ")
    if len (avito_date ) != 3:
        return 
    for key,value in months.items():
        if avito_date[1] == value:
            return  f"{now.year:04d}-{key:02d}-{avito_date[0]} {avito_date[2]} "

BAN_WORD = "BAN WORD in title"
def avito(url):
    lst = []
    page = pagefetcher(url)
    if not page:
           return
    soup = soupmaker(page.text)
    item_table = soup.find_all('div', {'class':'item_table'})
    for item in item_table:
        title = item.find('a', {'class':'snippet-link'})
        if not title:
            continue
        else:
            title = title.get('title')
            if BAN_WORD in title: 
            	continue

        price = item.find('meta',{'itemprop':'price'})
        price = price.get('content') if price else ''

        address = item.find('span',{'class':'item-address__string'})
        address = address.text.replace('\n',' ') if address else ''

        date = item.find('div',{'class':'snippet-date-info'})
        date = date.get('data-tooltip') if date else ''
        date = get_avito_date(date)

        img = item.find('div',{'class':'item-slider-image'})
        img = img.img if img else None
        img = img.get('src') if img else '' 

        link = item.find('a',{'class':'item-slider'})
        link = f"https://avito.ru{link.get('href')}" if link else ''

        title = f"{title} {price} {address}"        
        dct = dct_validate(name='avito.ru',time = date,title=title,content=title ,img=img,link=link)
        #input (dct)
        lst.append(dct)
    return lst


if __name__ == '__main__':
        import fetch_bs
        import pprint
        pp = pprint.PrettyPrinter(width=41, compact=True)

        h = hh('https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&experience=between1And3&no_magic=true&search_period=7&text=python&schedule=remote&from=cluster_schedule&showClusters=false','hh')
        #h = rssfunc('http://lenta.ru/rss/news','lenta.ru',3)
        #print (get_avito_date("20 сентября 18:38"))
        print (h)
        
        #pp.pprint (h)

        #get_time_now()
        #print (rssfunc('https://tvrain.ru/export/rss/all.xml','tvrain.ru',3))
        #print (rssfunc('http://www.kommersant.ru/RSS/news.xml','kommersant.ru',3))
        #print (bloknot('bl') )
        #print (vodokanal('v'))
        #print (inopressa('i'))
        #print (time_converter("2020-08-17  9:12"))


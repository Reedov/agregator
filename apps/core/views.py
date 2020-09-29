from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger
from apps.agprofile.models import AgProfile
from apps.feed.models import Feed
from apps.feeder.models import SiteFeeder
from apps.oinfo import oinfo

def frontpage(request,site=None):
	FREE_SITES = [1,2,3,4]

	if request.user.is_authenticated:
		profile = get_object_or_404(AgProfile, user=request.user)
		sites_id = [x['id'] for x in profile.subscribe_to.values()]
		sites_filter = sites_id
		
		if not site: # если не приходит id сайта фильтруем по списку
			all_feeds = Feed.objects.filter(site__in=sites_id).order_by('-timestamp')
		else:
			all_feeds = Feed.objects.filter(site=site).order_by('-timestamp')
	else:
		sites_filter = FREE_SITES
		
		if not site:
			all_feeds = Feed.objects.filter(site__in=FREE_SITES).order_by('-timestamp')
		else:
			if site in FREE_SITES:
				all_feeds = Feed.objects.filter(site=site).order_by('-timestamp')
			else:
				all_feeds = []
	
	profile_sites = SiteFeeder.objects.filter(id__in=sites_filter) # список сайтов провиля
	sites = SiteFeeder.objects.all()

	############## пагинатор ###############
	paginator = Paginator(all_feeds, 30)
	page = request.GET.get('page')
	try:
		feeds = paginator.page(page)
	except PageNotAnInteger:
		feeds = paginator.page(1)
	#########################################

	#oinfo(feeds)
	return render(request, 'core/frontpage.html',{'feeds':feeds,'profile_sites':profile_sites, 'sites':sites}) # т.е. то что в 'apps/core/templates/core/frontpage.html'
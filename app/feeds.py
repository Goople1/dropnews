from django.contrib.syndication.views import Feed
#from GianCarlosPrincipal.models import Enlace
 
class LatestEntriesFeed(Feed):
    title = "Police beat site news"
    link = "/rss/"
    description = "Updates on changes and additions to police beat central."
 
    def items(self):
        pass
 #       return Enlace.objects.all().order_by('id')[:10]
 
    def item_title(self, item):
        pass
        #return item.titulo
 
    def item_description(self, item):
        pass
        #return item.enlace
 
    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        pass
        #return item.enlace
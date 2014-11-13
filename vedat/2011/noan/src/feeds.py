from django.contrib.syndication.views import Feed
from packages.models import Package

class PackageFeed(Feed):
    title = "Last updated packages"
    link = "/packages/"
    description = ""

    def items(self):
        return Package.objects.order_by('-last_update')[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.pkgdesc

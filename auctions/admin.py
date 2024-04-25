from django.contrib import admin
from .models import Listing, Comments, Bid, User, Watchlist, ClosedListing

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "starting_bid", "category", "image", "listing_by")
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("on_item", "comment", "comment_by")
class WatchAdmin(admin.ModelAdmin):
    list_display = ("user", "item")

# class ShowWatch(admin.ModelAdmin):
#     fields = ['user', 'item']
#     list_display = ('user', 'get_item')

#     def get_item(self, obj):
#         return "\n".join([p.title for p in obj.item.all()])
    
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Bid)
admin.site.register(User)
admin.site.register(Watchlist)#, ShowWatch)
admin.site.register(ClosedListing)
from django.contrib import admin
from .models import User, Bid, Category, Listing, Comment

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=("username", "first_name", "last_name", "email")
class ListingAdmin(admin.ModelAdmin):
    filter_horizontal = ("categories",)
    list_display = ("title", "price", "owner")

admin.site.register(User, UserAdmin)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment)

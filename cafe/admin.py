from django.contrib import admin
from cafe.models import *


class CafeAdmin(admin.ModelAdmin):
    # admin can see the owner, cafe name and price point of the cafe
    list_display = ('owner', 'name', 'pricepoint')
    # allow the admin to create the slug using the name of the cafe
    prepopulated_fields = {'slug': ('name',)}


class ReviewAdmin(admin.ModelAdmin):
    # admin can see the cafe reviewed, the user who reviewed it and any comment he might have left
    list_display = ('cafe', 'user', 'comments')


class UserProfileInline(admin.TabularInline):
    model = UserProfile


# create an inline to be able to edit the User Profile in the same page as the User
class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]


# Unregister User model
admin.site.unregister(User)
# Register your models here.
admin.site.register(Cafe, CafeAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(User, UserAdmin)

from django.contrib import admin

from .models import User, Post, Follow_data
# Register your models here.

class FollowDataAdmin(admin.ModelAdmin):
    filter_horizontal = ("followers", "follows")

class LikesDataAdmin(admin.ModelAdmin):
    filter_horizontal = ("likes",)

admin.site.register(User)
admin.site.register(Post, LikesDataAdmin)
admin.site.register(Follow_data, FollowDataAdmin)
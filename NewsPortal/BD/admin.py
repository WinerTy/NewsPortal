from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from BD.models import Author, Category, Post, PostCategory, Comment
from django.template.defaultfilters import date


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'type', 'title_truncated', 'created_at')

    def title_truncated(self, obj):
        return ' '.join(obj.title.split()[:4])
    title_truncated.short_description = 'Title'

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])

    def get_authors(self, obj):
        return ", ".join([a.name for a in obj.authors.all()])

    get_categories.short_description = 'Categories'
    get_authors.short_description = 'Authors'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'create_date']
    list_filter = ['user__groups',]
    ordering = ['user__username',]
    search_fields = ('user__username', 'user__date_joined')

    def username(self, obj):
        return obj.user.username
    def email(self, obj):
        return obj.user.email

    def role(self, obj):
        return ', '.join([group.name for group in obj.user.groups.all()])
    def create_date(self,obj):
        data = obj.user.date_joined
        form_date = date(data, 'd/m/Y')
        return form_date


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)



admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
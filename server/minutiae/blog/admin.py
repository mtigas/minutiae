from django.contrib import admin
#from models import PostCategory,BlogPost
from models import BlogPost

#class PostCategoryAdmin(admin.ModelAdmin):
#    model = PostCategory
#
#    save_on_top = True
#    fieldsets = (
#        (None, {'fields': ('name','plural','slug')}),
#    )
#    list_display = ('name','plural','slug')
#    search_fields = ('name','plural')
#    prepopulated_fields = {"slug": ("plural",)}
#
#admin.site.register(PostCategory,PostCategoryAdmin)

class BlogPostAdmin(admin.ModelAdmin):
    model = BlogPost

    save_on_top = True
    fieldsets = (
        ('Content', {'fields': (('title', 'slug'), 'description', 'body')}),
        ('Metadata', {'fields': ('is_live', 'pubdate', 'post_type')}),
    )
    list_display = ('title', 'pubdate', 'post_type', 'is_live')
    list_filter = ('pubdate', 'is_live', 'post_type')
    search_fields = ('title', 'body')
    date_hierarchy = 'pubdate'
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(BlogPost,BlogPostAdmin)

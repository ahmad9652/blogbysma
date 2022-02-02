from django.contrib import admin
from blog import models
from blog.models import blog,blogcomment, contactuser
# Register your models here.

class blogAdmin(admin.ModelAdmin):
    class Media:
        css={
            "all":('css/main.css',)
        }
        js=("js/blog.js",)

# class userblogcreation(models):
#     class Media:
#         css={
#             "all":('css/main.css')
#         }
#         js=('js/blog.js',)
# class userblogpage():
#     pass
admin.site.register(blog,blogAdmin)
admin.site.register(contactuser)
admin.site.register(blogcomment)
# admin.site.register(userblog)
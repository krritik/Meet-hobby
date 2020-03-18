from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(PhoneNumber)
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Group)
admin.site.register(Events)
admin.site.register(HasEvents)
admin.site.register(HasPosts)
admin.site.register(UserInterestedEvents)
admin.site.register(GroupMembers)


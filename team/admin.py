from django.contrib import admin
from .models import UserProfile, Player, Coach, Team, UpcomingMatches, Message, Rating

admin.site.register(UserProfile)
admin.site.register(Player)
admin.site.register(Coach)
admin.site.register(Team)
admin.site.register(UpcomingMatches)
admin.site.register(Message)
admin.site.register(Rating)
from django.contrib import admin
from .models import SearchHistory

class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "count", "last_searched") 
    list_filter = ("user", "city") 

admin.site.register(SearchHistory, SearchHistoryAdmin)
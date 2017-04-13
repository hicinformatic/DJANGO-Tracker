from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Domain, DataAuthorized, Tracked
from .settings import conf
from django.core.cache import cache

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ( 'domain', 'id', 'status', 'counter', )
    readonly_fields = ( 'id', 'status', 'javascript', 'counter', 'create', 'update', )

def loadDatasAuthorized(modeladmin, request, queryset):
    with open(conf['appdir'] + '/moreconf.py', 'w') as f:
        f.write('more = [\n')
        for q in queryset:
            if q.status is True:
                f.write("    '" + q.key + "',\n")
        f.write(']')
        f.closed
        queryset.filter(status=False).update(load=False)
        queryset.filter(status=True).update(load=True)
        DataAuthorized.objects.exclude(id__in=queryset).update(load=False)
        cache.clear()
        modeladmin.message_user(request, _('Authorized data loaded'), 'success')
loadDatasAuthorized.short_description = _('Loads authorized data')
def disableDatasAuthorized(modeladmin, request, queryset):
    with open(conf['appdir'] + '/moreconf.py', 'w') as f:
        queryset.update(status=False, load=True)
        DataAuthorized.objects.exclude(id__in=queryset).update(load=False)
        modeladmin.message_user(request, _('Authorized data disable'), 'success')
disableDatasAuthorized.short_description = _('Disable authorized data')
@admin.register(DataAuthorized)
class DataAuthorizedAdmin(admin.ModelAdmin):
    list_display = ( 'key', 'status', 'load', 'counter', )
    readonly_fields = ( 'create', 'update', 'load', 'counter', )
    actions = [ loadDatasAuthorized, disableDatasAuthorized, ]

@admin.register(Tracked)
class TrackedAdmin(admin.ModelAdmin):
    list_display = ( 'visitor', 'key', 'value', 'domain', 'url', 'title',)
    readonly_fields = ( 'visitor', 'key', 'value', 'domain', 'url', 'title', )
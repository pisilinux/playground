from packages.models import Description, Package, Summary, isA, partOf, License, BuildHost
from packages.models import Distribution, Architecture, Update, XmlHash
from django.contrib import admin

admin.site.register(Description)
admin.site.register(Summary)
admin.site.register(isA)
admin.site.register(partOf)
admin.site.register(License)
admin.site.register(BuildHost)
admin.site.register(Distribution)
admin.site.register(Architecture)
admin.site.register(Update)
admin.site.register(XmlHash)

class DescInLine(admin.StackedInline):
    model = Description
    extra = 2

class SumInLine(admin.StackedInline):
    model = Summary
    extra = 2

class UpdateInLine(admin.TabularInline):
    model = Update
    extra = 1

class PackageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'isA', 'partOf', 'license', 'build_host',
            'distribution', 'architecture', 'installed_size', 'package_size', 'package_hash',
            'package_format', 'homepage', 'packager', 'last_update', 'dependencies', 'uri']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [DescInLine, SumInLine, UpdateInLine]

admin.site.register(Package, PackageAdmin)

from django.contrib import admin

from shop.models import Image, Painting


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class PaintingAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', '_images']
    inlines = [ImageInline]

    # noinspection PyMethodMayBeStatic
    def _images(self, painting):
        return painting.images.count()


admin.site.register(Image)
admin.site.register(Painting, PaintingAdmin)

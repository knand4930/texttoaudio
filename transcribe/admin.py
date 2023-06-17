from django.contrib import admin
from . models import *

# Register your models here.


class PdfAudioReaderAdmin(admin.ModelAdmin):
    list_display = ('username', 'create_at')
    list_filter = ('username', 'create_at')
    search_fields = ('username', 'create_at')
    readonly_fields = ('username', 'create_at')
    
admin.site.register(PdfAudioReader,PdfAudioReaderAdmin)

class TextAudioReaderReciverAdmin(admin.ModelAdmin):
    list_display = ('username', 'create_at')
    list_filter = ('username', 'create_at')
    readonly_fields = ('username', 'create_at')
admin.site.register(TextAudioReaderReciver, TextAudioReaderReciverAdmin)



class TextAudioConverterAdmin(admin.ModelAdmin):
    list_display = ('username', 'create_at')
    list_filter = ('username', 'create_at')
    search_fields = ('username', 'create_at')
    readonly_fields = ('username', 'create_at')
    
admin.site.register(TextAudioConverter,TextAudioConverterAdmin)



class PdfAudioConverterAdmin(admin.ModelAdmin):
    list_display = ('username', 'create_at')
    list_filter = ('username', 'create_at')
    search_fields = ('username', 'create_at')
    readonly_fields = ('username', 'create_at')
    
admin.site.register(PdfAudioConverter,PdfAudioConverterAdmin)




class PdfPageAudioConverterAdmin(admin.ModelAdmin):
    list_display = ('username', 'file', 'create_at')
    list_filter = ('username', 'create_at')
    search_fields = ('username', 'create_at')
    readonly_fields = ('username', 'create_at', 'file')
    
admin.site.register(PdfPageAudioConverter , PdfPageAudioConverterAdmin)



class AudioTextConverterAdmin(admin.ModelAdmin):
    list_display = ('username', 'create_at')
    list_filter = ('username', 'create_at')
    readonly_fields = ('username', 'create_at')
    
    
admin.site.register(AudioTextConverter,AudioTextConverterAdmin)
class AudioTextReciverAdmin(admin.ModelAdmin):
    list_display = ('username', 'txt', 'create_at')
    readonly_fields = ('username', 'txt', 'create_at')
    list_filter = ('username', 'create_at')
admin.site.register(AudioTextReciver, AudioTextReciverAdmin)



class VideoTextConverterAdmin(admin.ModelAdmin):
    list_display = ('username', 'file', 'create_at')
    list_filter = ('username', 'create_at')
    search_fields = ('username', 'create_at')
    readonly_fields = ('username', 'create_at')
    
admin.site.register(VideoTextConverter,VideoTextConverterAdmin)
class VideoTextReciverAdmin(admin.ModelAdmin):
    list_display = ('username', 'txt', 'create_at')
    readonly_fields = ('username', 'txt', 'create_at')
    list_filter = list_filter = ('username', 'create_at')
admin.site.register(VideoTextReciver, VideoTextReciverAdmin)
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.db.models import FileField
from django.contrib.auth.models import User
# from app.extra import ContentTypeRestrictedFileField
# from formatChecker import ContentTypeRestrictedFileField
from django.core.files.storage import FileSystemStorage


# Create your models here.
#https://djangobook.com/mdj2-advanced-models/
class MediaFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if max_length and len(name) > max_length:
            raise(Exception("name's length is greater than max_length"))
        return name

    def _save(self, name, content):
        if self.exists(name):
            # if the file exists, do not call the superclasses _save method
            return name
        # if the file is new, DO call it
        return super(MediaFileSystemStorage, self)._save(name, content)




class PdfAudioReader(models.Model):
    username = models.CharField(max_length=50)
    file = models.FileField(upload_to='pdfaudioreader/')
    page = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)

@receiver(pre_delete, sender=PdfAudioReader)
def mymodel_delete(sender, instance ,**kwargs):
    instance.file.delete(False)
    
    
    

class TextAudioReaderReciver(models.Model):
    username = models.CharField(max_length=50)
    text = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    




class TextAudioConverter(models.Model):
    username = models.CharField(max_length=50)
    file = models.TextField()
    lang = models.CharField(max_length=30)
    create_at = models.DateTimeField(auto_now_add=True)





class PdfAudioConverter(models.Model):
    username = models.CharField(max_length=50)
    file = models.FileField(upload_to='pdfaudioconverter/')
    lang = models.CharField(max_length=30)
    create_at = models.DateTimeField(auto_now_add=True)
    
@receiver(pre_delete, sender=PdfAudioConverter)
def mymodel_delete(sender, instance ,**kwargs):
    instance.file.delete(False)
     
    
    


class PdfPageAudioConverter(models.Model):
    username = models.CharField(max_length=50)
    file = models.FileField(upload_to='pdfpageaudioconverter/')
    pages = models.IntegerField()
    lang = models.CharField(max_length=30)
    create_at = models.DateTimeField(auto_now_add=True)
    

@receiver(pre_delete, sender=PdfPageAudioConverter)
def mymodel_delete(sender, instance ,**kwargs):
    instance.file.delete(False)
    
    
    
    


class AudioTextConverter(models.Model):
    username = models.CharField(max_length=50)
    file = models.FileField(upload_to='audiotextconverter/')
    create_at = models.DateTimeField(auto_now_add=True)

@receiver(pre_delete, sender=AudioTextConverter)
def mymodel_delete(sender, instance ,**kwargs):
    instance.file.delete(False)

class AudioTextReciver(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    txt = models.TextField(default="Your Text")
    create_at = models.DateTimeField(auto_now_add=True)




    
class VideoTextConverter(models.Model):
    username = models.CharField(max_length=50)
    file = models.FileField(upload_to='videotextconverter/')
    create_at = models.DateTimeField(auto_now_add=True)

@receiver(pre_delete, sender=VideoTextConverter)
def mymodel_delete(sender, instance ,**kwargs):
    instance.file.delete(False)
    
class VideoTextReciver(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    txt = models.TextField(default="Your Text")
    create_at = models.DateTimeField(auto_now_add=True)


    

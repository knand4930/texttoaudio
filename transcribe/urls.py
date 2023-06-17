from django.urls import path
from . import views

urlpatterns=[
    path('pdf-audio-reader', views.pdfaudioreader, name='pdfaudioreader'),
    path('', views.textaudioconverter, name='textaudioconverter'),
    path('pdf-audio-converter', views.pdfaudioconverter, name='pdfaudioconverter'),
    path('audio-text-converter', views.audiotextconverter, name='audiotextconverter'),
    path('video-text-converter', views.videotextconverter, name='videotextconverter'),
    path('pdf-page-audio-converter', views.pdfpageaudioconverter, name='pdfpageaudioconverter'),
    path('testing', views.testingaduio, name='testingaduio'),
]
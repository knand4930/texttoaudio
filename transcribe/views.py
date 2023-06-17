import time

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import pyttsx3
from gtts import gTTS
import moviepy.editor as mp
from .models import *
from moviepy.editor import *
import sys
import os
import subprocess
import pdfplumber
from gTTS.templatetags.gTTS import say
import speech_recognition as sr
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import fitz
from django.contrib import messages
import torch
import zipfile
import torchaudio
from glob import glob
from pydub import AudioSegment
from omegaconf import OmegaConf
from payment.models import *
from main.models import *
from datetime import datetime


def pdfaudioreader(request):
    # if request.user.is_authenticated:
    #     profile_pro = Profile.objects.filter(user=request.user).last()
    #     request.session['profile_pro'] = profile_pro.paid
    #     if profile_pro.paid == True:
    #         subscription_type = profile_pro.subscription_type
    #         if subscription_type=='transcribe' or subscription_type=='book_transcribe' or subscription_type=='marketing_transcribe' or subscription_type=='all':
    #
    if request.method == 'POST':
        file = request.FILES.get('file')
        page = request.POST.get('page')

        pobj = PdfAudioReader()
        pobj.file = file
        pobj.page = page
        pobj.save()
        pfile = PdfAudioReader.objects.last()
        pfileurl = str(pfile.file)
        pfileid = pfileurl[1:]
        pages = int(page)

        book = pdfplumber.open(pfileid)
        pages = book.pages[pages]
        text = pages.extract_text()
        data = TextAudioReaderReciver()
        data.text = text
        data.username = request.user
        data.save()
    # storedata = DataStore.objects.filter(paid = True)?
    data = TextAudioReaderReciver.objects.last()
    return render(request, 'pdfaudioreader.html', {'data': data, })
    # return redirect('subscriptions')


def textaudioconverter(request):
    # if(request.user.is_authenticated is False):
    #     return redirect("signin")
    # if request.user.is_authenticated:
    #     profile_pro = Profile.objects.filter(user=request.user).last()
    #     request.session['profile_pro'] = profile_pro.paid
    #     if profile_pro.paid == True:
    #         subscription_type = profile_pro.subscription_type
    #         if subscription_type=='transcribe' or subscription_type=='book_transcribe' or subscription_type=='marketing_transcribe' or subscription_type=='all':
    #
    try:
        textdata = []
        if request.method == 'POST':
            file = request.POST.get('file')
            paobj = TextAudioConverter()
            paobj.file = file
            paobj.lang = 'en-us'
            paobj.username = request.user
            paobj.save()
            pafile = TextAudioConverter.objects.last()
            pafileurl = str(pafile.file)
            textstring = "".join(pafileurl)
            textdata.append(textstring)

        data = " ".join(str(x) for x in textdata)
        story = repr(data)
        obj = say(language='en-us', text=story)

        return render(request, 'textaudioconverter.html', {'obj': obj})
    except Exception as e:
        print(e)
        messages.warning(request, "File Doesn't Support! please input correct PDF File ")

    return render(request, 'textaudioconverter.html')
    # return redirect('subscriptions')


def pdfaudioconverter(request):
    # if(request.user.is_authenticated is False):
    #     return redirect("signin")
    # if request.user.is_authenticated:
    #     profile_pro = Profile.objects.filter(user=request.user).last()
    #     request.session['profile_pro'] = profile_pro.paid
    #     if profile_pro.paid == True:
    #         subscription_type = profile_pro.subscription_type
    #         if subscription_type=='transcribe' or subscription_type=='book_transcribe' or subscription_type=='marketing_transcribe' or subscription_type=='all':
    #
    try:
        textdata = []
        if request.method == 'POST':
            # if filesize == 200:
            file = request.FILES.get('file')

            # else:
            #     messages.warning(request, "File Doesn't Support! please input correct PDF File ")
            #     return render(request, 'pdfaudioconverter.html')
            # lang = request.POST.get('lang')

            if file.size <= 314572800:

                paobj = PdfAudioConverter()
                paobj.file = file
                paobj.lang = 'en-us'
                paobj.username = request.user
                paobj.save()
            else:
                messages.warning(request,
                                 "Your file has been maximum of 300MB !! Please upload minimum size of 300MB !!")
                return render(request, 'pdfaudioconverter.html')

            try:
                pafile = PdfAudioConverter.objects.last()
                pafileurl = str(pafile.file.url)
                pafileid = pafileurl[1:]
                book = fitz.open(pafileid)
            except Exception as e:
                print(e)
                messages.warning(request, "File Doesn't Support! please input correct PDF File")
                return render(request, 'pdfaudioconverter.html')
            textList = []
            for page in book:
                textList += page.getText()

            textstring = "".join(textList)
            textdata.append(textstring)

        data = " ".join(str(x) for x in textdata)
        story = repr(data)
        obj = say(language='en-us', text=story)
        return render(request, 'pdfaudioconverter.html', {'obj': obj})
    except Exception as e:
        print(e)
        messages.warning(request, "File Doesn't Support! please input correct PDF File ")

        # return render(request, 'pdfaudioconverter.html')


def pdfpageaudioconverter(request):
    # if(request.user.is_authenticated is False):
    #     return redirect("signin")
    # if request.user.is_authenticated:
    #     profile_pro = Profile.objects.filter(user=request.user).last()
    #     request.session['profile_pro'] = profile_pro.paid
    #     if profile_pro.paid == True:
    #         subscription_type = profile_pro.subscription_type
    #         if subscription_type=='transcribe' or subscription_type=='book_transcribe' or subscription_type=='marketing_transcribe' or subscription_type=='all':
    #
    try:
        textdata = []
        # pdflang = []
        if request.method == 'POST':

            file = request.FILES.get('file')
            print(file.size)
            pages = request.POST.get('pages')
            # lang = request.POST.get('lang')
            pageid = int(pages)

            if file.size <= 314572800:
                paobj = PdfPageAudioConverter()
                paobj.file = file
                paobj.pages = pages
                paobj.lang = 'en-us'
                paobj.username = request.user
                paobj.save()
            else:
                messages.warning(request,
                                 "Your file has been maximum of 300MB !! Please upload minimum size of 300MB !!")
                return render(request, 'pdfpageaudioconverter.html')

            try:
                pafile = PdfPageAudioConverter.objects.last()
                pafileurl = str(pafile.file.url)
                pafileid = pafileurl[1:]
                book = pdfplumber.open(pafileid)
                pages = book.pages[pageid]
                text = pages.extract_text()
            except Exception as e:
                print(e)
                messages.warning(request, "File Doesn't Support! please input correct PDF File")
                return render(request, 'pdfpageaudioconverter.html')

            textstring = "".join(text)
            textdata.append(textstring)

        data = " ".join(str(x) for x in textdata)
        story = repr(data)
        obj = say(language='en-us', text=story)

        return render(request, 'pdfpageaudioconverter.html', {'obj': obj})
    except Exception as e:
        print(e)
        messages.warning(request, "File Doesn't Support! please input correct PDF File ")

    return render(request, 'pdfpageaudioconverter.html')
    # return redirect('subscriptions')


def audiotextconverter(request):
    # if(request.user.is_authenticated is False):
    #     return redirect("signin")
    # if request.user.is_authenticated:
    #     profile_pro = Profile.objects.filter(user=request.user).last()
    #     request.session['profile_pro'] = profile_pro.paid
    #     if profile_pro.paid == True:
    #         subscription_type = profile_pro.subscription_type
    #         if subscription_type=='transcribe' or subscription_type=='book_transcribe' or subscription_type=='marketing_transcribe' or subscription_type=='all':
    #
    try:
        if request.method == 'POST':
            print(request.FILES['file'].size)
            file = request.FILES.get('file')

            if file.size <= 314572800:
                aobj = AudioTextConverter()
                aobj.username = request.user
                aobj.file = file
                aobj.save()
                audiofile = AudioTextConverter.objects.last()
                adurl = str(audiofile.file.url)
                audioid = adurl[1:]
            else:
                messages.warning(request,
                                 "Your file has been maximum of 300MB !! Please upload minimum size of 300MB !!")
                return render(request, 'audiotextconverter.html')

            try:
                sound = AudioSegment.from_mp3(audioid)
                data = "media/audiotext.wav"
                sound.export(data, format="wav")
            except Exception as e:
                print(e)
                messages.warning(request, "File Doesn't Support! please input correct Audio File")
                return render(request, 'audiotextconverter.html')

            device = torch.device('cpu')

            model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_stt',
                                                   language='en',
                                                   device=device)

            (read_batch, split_into_batches, read_audio, prepare_model_input) = utils
            test_files = glob(data)

            batches = split_into_batches(test_files, batch_size=10)

            input = prepare_model_input(read_batch(batches[0]), device=device)

            output = model(input)

            for example in output:
                txt = decoder(example.cpu())
                print("Txt data are printed :- ", txt)
                data = AudioTextReciver()
                data.username = request.user
                data.txt = txt
                data.save()
        txtdata = AudioTextReciver.objects.last()
        story = str(txtdata.txt)
        return render(request, 'audiotextconverter.html', {"story": story})
    except Exception as e:
        print(e)
        messages.warning(request, "Language Doesn't Support! please input correct Audio File ")

    return render(request, 'audiotextconverter.html')
    # return redirect('subscriptions')


def videotextconverter(request):
    # if(request.user.is_authenticated is False):
    #     return redirect("signin")
    # if request.user.is_authenticated:
    #     profile_pro = Profile.objects.filter(user=request.user).last()
    #     request.session['profile_pro'] = profile_pro.paid
    #     if profile_pro.paid == True:
    #         subscription_type = profile_pro.subscription_type
    #         if subscription_type=='transcribe' or subscription_type=='book_transcribe' or subscription_type=='marketing_transcribe' or subscription_type=='all':
    #

    try:

        if request.method == 'POST':
            file = request.FILES.get('file')
            start_time = time.time()

            if file.size <= 314572800:
                obj = VideoTextConverter()
                obj.username = request.user
                obj.file = file
                obj.save()
                videofile = VideoTextConverter.objects.last()
                vdurl = str(videofile.file.url)
                videoid = vdurl[1:]
            else:
                messages.warning(request,
                                 "Your file has been maximum of 300MB !! Please upload minimum size of 300MB !!")
                return render(request, 'videotextconverter.html')

            try:
                clip = mp.VideoFileClip(videoid)
                audiofile = "audio.wav"
                audio = clip.audio.write_audiofile(audiofile)
            except Exception as e:
                print(e)
                messages.warning(request, "File Doesn't Support! please input correct Video File")
                return render(request, 'videotextconverter.html')

            device = torch.device('cpu')

            model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_stt',
                                                   language='en',
                                                   device=device)

            (read_batch, split_into_batches, read_audio, prepare_model_input) = utils
            test_files = glob(audiofile)

            batches = split_into_batches(test_files, batch_size=10)

            input = prepare_model_input(read_batch(batches[0]), device=device)

            output = model(input)

            for example in output:
                txt = decoder(example.cpu())
                data = VideoTextReciver()
                data.username = request.user
                data.txt = txt
                data.save()
        txtdata = VideoTextReciver.objects.last()
        story = str(txtdata.txt)
        print(story)
        end_time = time.time()
        print(end_time - start_time, "==========================================================================")
        return render(request, 'videotextconverter.html', {'story': story})
    except Exception as e:
        print(e)
        messages.warning(request, "Language Doesn't Support! please input correct Video File ")

    return render(request, 'videotextconverter.html')
    # return redirect('subscriptions')


# def videopdfconverter(request):
#     pass

# https://github.com/eugeniaring/ExtractTextFromVideos/blob/main/extractlog.py


# def send_file(response):

#     img = open('static/gTTs/', 'rb')

#     response = FileResponse(img)

#     return response


def testingaduio(request):
    return render(request, 'test.html')

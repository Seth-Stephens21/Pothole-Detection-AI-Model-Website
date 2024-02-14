from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import os
import cv2
from django.core.files.storage import FileSystemStorage
from Detection.YOLO_Video import video_detection
from django.http import StreamingHttpResponse
import torch
#from .models import ModelWithFileField
# Create your views here.

def index(request):
    return render(request, "Detection/index.html")

def playvideo(request):
    return render(request, "Detection/video.html",{
        "videot" : request.FILES["file"]
    })

def generate_frames(path_x = ''):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
        

def upload_file(request):
    if request.method == "POST":
        
        file = (request.FILES["document"])
        print(file.name)
        print(file.size)
        fs = FileSystemStorage()
        name = fs.save(file.name,file)
        request.session["video_path"] = os.path.join(fs.location,f"{file.name}")

    return StreamingHttpResponse(generate_frames(path_x=request.session["video_path"]), content_type="multipart/x-mixed-replace;boundary=frame")

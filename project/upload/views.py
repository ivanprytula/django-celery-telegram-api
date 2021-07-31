from django.core.files.storage import FileSystemStorage
from django.shortcuts import render


def image_upload(request):
    if request.method == "POST" and request.FILES["image_file"]:
        image_file = request.FILES["image_file"]
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)
        return render(request, "upload/index.html", {
            "image_url": image_url
        })
    return render(request, "upload/index.html")

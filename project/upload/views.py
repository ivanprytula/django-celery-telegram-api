from django.core.files.storage import FileSystemStorage
from django.shortcuts import render


def image_upload(request):
    if request.method == "POST" and request.FILES["image_file"]:
        image_file = request.FILES["image_file"]
        file_system_storage = FileSystemStorage()
        filename = file_system_storage.save(image_file.name, image_file)
        image_url = file_system_storage.url(filename)
        return render(request, "upload/index.html", {
            "image_url": image_url
        })
    return render(request, "upload/index.html")

from django.shortcuts import render

def upload_page(request):
    return render(request , 'upload.html')
    

def mapping_page(request):
    return render(request , 'mapping.html')


def progress_page(request):
    return render(request, 'progress.html')

def data_page(request):
    return render(request, 'data.html')

def history_page(request):
    return render(request, 'history.html')
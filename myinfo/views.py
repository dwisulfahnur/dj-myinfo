from django.http import HttpResponseNotFound
from django.http.request import HttpRequest
from django.shortcuts import render

def index_view(request: HttpRequest):
    return render(request, 'myinfo/index.html')

def callback_form_view(request: HttpRequest):
    code = request.GET.get('code')
    if not code:
        return HttpResponseNotFound("Not Found")
    return render(request, 'myinfo/form.html')

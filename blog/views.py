from django.http import HttpResponse
from django.shortcuts import render




def write_blog_entry(request):
    if request.method == "GET":
        return render(request, "markdown.html")

    content = request.POST["content"]
    print(content)

    return HttpResponse("ok")
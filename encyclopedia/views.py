from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    
    return render(request, "encyclopedia/wiki.html",{
        "content": util.get_entry(title)
    })

def newpage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title.upper() not in [i.upper() for i in util.list_entries()]:
            util.save_entry(title, content)
        else:
            print("Ya existe esa entrada")
    return render(request, "encyclopedia/newpage.html")
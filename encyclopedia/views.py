import random
import re

from django.shortcuts import redirect, render

from . import util
from markdown2 import Markdown

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    _title = util.get_entry(title)
    if bool(_title):
        context = {
            'success': True,
            'title': title,
            'content': markdowner.convert(_title)
        }
        return render(request, "encyclopedia/wiki.html",context)
    else:
        context = {
            'success': False,
            'title': "Página no encontrada",
            'message': "Página no encontrada"
        }
        return render(request, "encyclopedia/wiki.html",context)

def search(request):
    title = request.GET.get("q")

    entries = [i for i in util.list_entries()]
    
    if title in entries:
        context = {
            'success': True,
            'title': title,
            'content': markdowner.convert(util.get_entry(title))
        }
        return render(request, "encyclopedia/wiki.html",context)
    else:
        result = [i for i in entries if title.upper() in i.upper()]
        if not result:
            context = {
                'success': False,
                'title': "Error",
                'message': "No se encontraron coincidencias"
            }
            return render(request, "encyclopedia/wiki.html",context)
        else:
            context = {
                'success': True,
                'title': "Resultados Similares",
                'entries': result
            }
            return render(request, "encyclopedia/wiki.html",context)

  
def newpage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title.upper() not in [i.upper() for i in util.list_entries()]:
            util.save_entry(title, content)
            context = {
                'success': True,
                'title': title,
                'content': markdowner.convert(util.get_entry(title))
            }
            return render(request, "encyclopedia/wiki.html",context)
        else:
            context = {
                'success': False,
                'title': "Error",
                'message': "Ya existe esa entrada"
            }
            return render(request, "encyclopedia/wiki.html",context)
    else:
        return render(request, "encyclopedia/newpage.html")


def randomPage(request):
    if request.method == 'GET':
        entries = util.list_entries()
        rand = random.SystemRandom()
        entry = rand.choice(entries)

        context = {
            'success': True,
            'title': entry,
            'content': markdowner.convert(util.get_entry(entry))
        }

        return render(request, "encyclopedia/wiki.html", context)

def editContet(request, title):
    if request.method == 'GET':
        context ={
            'title': title,
            'content': util.get_entry(title)
        }
        return render(request, 'encyclopedia/edit.html', context)
    else:
        if request.method == 'POST':
            content = request.POST.get("content")
            util.save_entry(title, content)
            context = {
                'success': True,
                'title': title,
                'content': markdowner.convert(util.get_entry(title))
            }
            return render(request, 'encyclopedia/wiki.html', context)
    

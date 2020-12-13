from django.shortcuts import redirect, render
from markdown2 import Markdown

from . import util

# set-up markdown converter
markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, entry):
    markdown = util.get_entry(entry)
    if not markdown:
        return redirect("not-found")
    html = markdowner.convert(util.get_entry(entry))
    return render(request, "encyclopedia/entry.html", {"entry": html})


def notFound(request):
    return render(request, "encyclopedia/entry-not-found.html")

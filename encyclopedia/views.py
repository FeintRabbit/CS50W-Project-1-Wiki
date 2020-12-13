from django.shortcuts import redirect, render
from django.urls import reverse
from markdown2 import Markdown

from . import util

# set-up markdown converter
markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, entry):
    markdown = util.get_entry(entry)
    print(entry)
    if not markdown:
        return redirect("not-found")
    html = markdowner.convert(util.get_entry(entry))
    return render(
        request, "encyclopedia/entry.html", {"title": entry.capitalize(), "html": html}
    )


def notFound(request):
    return render(request, "encyclopedia/entry-not-found.html")


def search(request):
    entries = util.list_entries()
    search = request.GET["q"]

    # if the search term exists, redirect to that page
    if search.lower() in (entry.lower() for entry in entries):
        print("match")
        return redirect(reverse("entry", args=[search]))

    # else return a page of partial matching entries
    results = [entry for entry in entries if search.lower() in entry.lower()]
    print(results)
    return render(
        request, "encyclopedia/search.html", {"results": results, "search": search}
    )

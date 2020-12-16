from django import forms
from django.shortcuts import redirect, render
from django.urls import reverse

from markdown2 import Markdown

import random

print(random.__file__)

from . import util

# set-up markdown converter
markdowner = Markdown()
# https://github.com/trentm/python-markdown2

# Entry form
class EntryForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)


# Edit form
class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


# Routes


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, entry):
    markdown = util.get_entry(entry)
    if not markdown:
        error = f"requested entry '{entry}' was not found."
        return render(request, "encyclopedia/error.html", {"error": error})
    html = markdowner.convert(util.get_entry(entry))
    return render(
        request, "encyclopedia/entry.html", {"title": entry.capitalize(), "html": html}
    )


def search(request):
    entries = util.list_entries()
    search = request.GET["q"]

    # if the search term exists, redirect to that page
    if search.lower() in [entry.lower() for entry in entries]:
        return redirect(reverse("entry", args=[search]))

    # else return a page of partial matching entries
    results = [entry for entry in entries if search.lower() in entry.lower()]
    return render(
        request, "encyclopedia/search.html", {"results": results, "search": search}
    )


def new(request):
    if request.method == "GET":
        form = EntryForm()
        return render(request, "encyclopedia/new.html", {"form": form})

    # if method post
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()

            # check if title exists, error
            if title.lower() in [entry.lower() for entry in entries]:
                error = (
                    f"Page for '{title}' already exists <a href='entry/{title}'>here<a>"
                )
                return render(request, "encyclopedia/error.html", {"error": error})

            # add new entry, take to new page
            util.save_entry(title, content)
            return redirect(reverse("entry", args=[title]))
            # print(title, body, entries)

        error = "an unknown error occured"
        return render(request, "encyclopedia/error.html", {"error": error})


def edit(request, entry):

    if request.method == "GET":
        markdown = util.get_entry(entry)
        form = EditForm(initial={"content": markdown})
        return render(request, "encyclopedia/edit.html", {"title": entry, "form": form})

    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(entry, content)
            return redirect(reverse("entry", args=[entry]))


def rand(request):
    entries = util.list_entries()
    randomEntry = random.choice(entries)
    return redirect(reverse("entry", args=[randomEntry]))


# Errors
# I've tried to create a generic catch-all error page, that can take error message args.
# Not sure this is great design... see 'entry'. It's rendered in place.
# def error(request, error):
#     return render(request, "encyclopedia/error.html", {"error": error})
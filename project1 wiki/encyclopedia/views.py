from django.shortcuts import render, redirect
from django import forms
from random import randint
from markdown2 import markdown
from . import util

class SearchForm(forms.Form):
    q = forms.CharField(label="Search Encyclopedia")

class NewPage(forms.Form):
    title = forms.CharField(label="Title")
    text = forms.CharField(label="Write text here")

class EditPage(forms.Form):
    content = forms.CharField()


# index, show list of all entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# page, use entries and name to check if it exists in HTML and transform markdown content
def page(request, name):

    content = None

    # check if content exists to avoid error message when converting from md to HTML
    entries = util.list_entries()
    for entry in entries:

        if name.lower() == entry.lower():

            content = markdown(util.get_entry(name))

    return render(request, "encyclopedia/page.html", {
        "name": name,
        "entries": util.list_entries(),
        "content": content
    })


# search results, go directly to result if it is a match or show suggestions
def results(request):

    form = SearchForm(request.POST)
    entries = util.list_entries()

    if form.is_valid():
        search = form.cleaned_data["q"]

        for entry in entries:

            if search.lower() == entry.lower():

                return redirect("page", name=search)

    return render(request, "encyclopedia/results.html", {
        "search": search,
        "entries": entries
    })


# new page, return an error message if page with the same title already exists else create new
def new(request):

    entries = util.list_entries()

    if request.method == "POST":

        form = NewPage(request.POST)

        if form.is_valid():

            title = form.cleaned_data["title"]
            content = form.cleaned_data["text"]

            for entry in entries:

                if title.lower() == entry.lower():
                    
                    error = True
                    return render(request, "encyclopedia/new.html", {
                        "error": error
                    })
            
            util.save_entry(title, content)

            return redirect("page", name=title)

    return render(request, "encyclopedia/new.html")


# edit page 
def edit(request, name):

    if request.method == "POST":

        form = EditPage(request.POST)

        if form.is_valid():
            content = form.cleaned_data["content"]

            util.save_entry(name, content)

            return redirect("page", name=name)

    return render(request, "encyclopedia/edit.html", {
        "content": util.get_entry(name)
    })


def random(request):

    #generate list of entries, find a random number in range of that list, find title of entry with that number
    entries = util.list_entries()
    number = randint(0, len(entries)-1)
    title = entries[number]

    return redirect("page", name=title)


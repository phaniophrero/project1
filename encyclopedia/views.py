import random
import markdown2
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

from . import util


def index(request):

    return render(request,  "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

        

# Display Wiki entry

def wiki(request, entry):
    content = util.get_entry(entry)

    if content == None:
        return render(request, "encyclopedia/message.html", {
            "message": "404 - Page not found !"
        })

    markdown = markdown2.markdown(content)

    return render(request, "encyclopedia/wiki.html", {
        "entry": entry,
        "content": markdown
    })



# Add new page

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")

    elif request.method == "POST":
        form = request.POST
        title = form['title']
        content = form['content']

        entries = util.list_entries()


        for entry in entries:
            if title.lower() == entry.lower():
                return render(request, "encyclopedia/message.html", {
                    "error_message": "This entry is already added! Please enter a new entry!"
                })
        util.save_entry(title, content)
        return render(request, "encyclopedia/message.html", {
            "success_message": "Your new page was added successfully!"
        })


# Add edit page functionality

def edit_page(request, entry):
    if request.method == "GET":
        content = util.get_entry(entry)

        return render(request, "encyclopedia/edit_page.html",{
            "title": entry,
            "content": content
        })

    elif request.method == "POST":
        form = request.POST
        title = form['title']
        content = form['content']

        util.save_entry(title, content)

        return HttpResponseRedirect(reverse("wiki:wiki", kwargs={'entry': title}))



# Add random page functionality

def random_page(request):
    entries = util.list_entries()
    page = random.choice(entries)

    return HttpResponseRedirect(reverse("wiki:wiki", kwargs={'entry': page}))



# Add Search functionality

def search(request):
    if request.method == "POST":
        query = request.POST
        query = query['q']

        entries = util.list_entries()
        page = None

        for entry in entries:
            if query.lower() == entry.lower():
                page = entry
                print(f"Match found -", page)

        if page != None:
            return HttpResponseRedirect(reverse("wiki:wiki", kwargs={"entry": page}))

        list = []

        for entry in entries:
            if query.lower() in entry.lower():
                list.append(entry)

        if not list:
            return render(request, "encyclopedia/search_results.html")

        else:
            return render(request, "encyclopedia/search_results.html", {
                "results": list
            })

    else:
        return HttpResponse("Error")





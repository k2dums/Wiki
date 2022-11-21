from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
import random

from . import util
import markdown2

class NewPageForm(forms.Form):
    title=forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Title'}))
    content=forms.CharField(widget=forms.Textarea,label="",help_text="")


def random_page():
    """Returns a page name from list of entries"""
    entries=util.list_entries()
    if not(entries):
        return " "
    random_page=random.randint(0,len(util.list_entries()) -1)
    random_page=util.list_entries()[random_page]
    return random_page
    
def page_content(title):
    """Returns  content of page in HTML given the title of the entry"""
    content=util.get_entry(title)
    if content:
        content=markdown2.markdown(content)
        return content

def check_pageExists(title):
    """Returns True if the page with the title exists, else False"""

    for entry in util.list_entries():
        if entry.casefold()== title.casefold():
            return True
    return False

def save_page(title,page):
    """Saves the page content to the system"""
    print(f"[SAVING] {title}.md")
    util.save_entry(title,page)

def substrTitle(title):
    """Finds the substring exists in the list of entries"""
    entries=[]
    if title is not(None):
        for entry in util.list_entries():
            if title.casefold() in entry.casefold():
                entries.append(entry)
    return entries

def searchBox(request):
    if request.GET.get('q'):
        print("Query in index exists")
        title=str(request.GET['q'])
        if check_pageExists(title):
            return HttpResponseRedirect(reverse("page",args=[title]))
        #else if page doesnt exist we check for the substring in the title
        entries=substrTitle(title)
        return render(request, "encyclopedia/index.html", {
        "entries":entries,
        "random_page":random_page(),
    })




def index(request):
    query=searchBox(request)
    if query:
        return query
        
    return render(request, "encyclopedia/index.html", {
        "entries":util.list_entries(),
        "random_page":random_page(),
    }
    )

def page(request,title):
    query=searchBox(request)
    if query:
        return query
    return render(request,"encyclopedia/page.html",{
        "title":title,
        "content":page_content(title),
        "random_page":random_page()
    })


def new_page(request):
    query=searchBox(request)
    if query:
        return query
    if request.method=="POST":
        form=NewPageForm(request.POST)
        if form.is_valid():
            content=form.cleaned_data["content"]
            title=form.cleaned_data["title"]
            if check_pageExists(title):
                print(f"[Error] Page exists, new page not created")
                return render(request,'encyclopedia/page.html',{"exists":True})
            #else if page doen't exist save the file 
            save_page(title,content)
            return HttpResponseRedirect(reverse("page",args=[title]))
        else:
            return render(request, "encyclopedia/new_page.html",{
                "form":form
            })
            

    return render(request,"encyclopedia/new_page.html",{
        "form":NewPageForm(),
        "random_page":random_page(),
    })

def edit_page(request):
    query=searchBox(request)
    if query:
        return query
    if request.method=="POST":
        form=NewPageForm(request.POST)
        if form.is_valid():
            content=form.cleaned_data["content"].encode()
            title=form.cleaned_data['title']
            save_page(title,content)
            return HttpResponseRedirect(reverse("page",args=[title]))


    #else if method is GET
    title=request.GET["page"]
    return render(request,"encyclopedia/edit_page.html",{
    "form":NewPageForm(initial={
        'title':title,
        'content':util.get_entry(title),
    }),
    "random_page":random_page()

    })
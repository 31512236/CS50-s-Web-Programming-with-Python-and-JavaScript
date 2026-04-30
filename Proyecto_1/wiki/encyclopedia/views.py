import markdown2
import random #Import the random function from Python
from django.shortcuts import render
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", { #When we want to show the home page of our wiki
        "entries": util.list_entries()
    })

def entry(request, title):

    content = util.get_entry(title) #The system goes to entries folder and looks for one that has the same name as what you saved in the title variable

    if content is None: #if no entry matches
        return render(request, "encyclopedia/error.html",{
            "message": "The website does not exist." #show an error message 
        })

    html = markdown2.markdown(content) #if an entry matches, call the content from markdown

    return render(request,"encyclopedia/entry.html",{ #And show the content in website
        "title": title, 
        "content": html
    })

def search(request): #The "request" object contains everything the user typed in the search field
    query = request.GET.get("q") #Gets what the user wrote

    entries = util.list_entries() #It calls the util.py file to check the "entries/"" folder and returns a list

    if query in entries:
        return entry(request, query)

    matching_entries = []

    for e in entries: #Search for coincidences
        if query.lower() in e.lower():  #Check if the query is within the name
            matching_entries.append(e) #Add the matching results to a "matching_entries" list

    return render(request, "encyclopedia/results.html",{ #Show the results
        "results": matching_entries, 
        "entry": query #Add the h1 to the search results
    })

def new(request): #requests the server

    if request.method == "POST": #Add new information using the POST method

        #The text that the user writes will be saved in the title and body variables
        title = request.POST.get("title")
        body = request.POST.get("content")

        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/new-error.html", { #In case the entry does not exist
                "message": "The website already exists." #If the entry already exists, to avoid duplicates
            })

        content = f"# {title}\n\n{body}"

        util.save_entry(title, content)

        return entry(request, title)

    else:
        return render(request, "encyclopedia/new.html")

def edit(request, title): #It's a function similar to new, but in this case, within the parameters we write title to indicate that an existing entry will be called
    
    if request.method == "POST":
        
        body = request.POST.get("content")#Call the content that already exists in the entry

        content = f"{body}"#Rebuilds the markdown 

        util.save_entry(title, content)#Overwrite using save_entry

        return entry(request, title) #Redirect to entry

    else:
        content = util.get_entry(title) #Get the form content

        return render(request, "encyclopedia/edit.html", { #Send it to HTML
        "title": title,
        "content": content
})

def random_page(request):
    entries = util.list_entries()  #List of all pages
    
    title = random.choice(entries)  #Choose one at random
    
    return entry(request, title)  #Reuse your entry function


        
        


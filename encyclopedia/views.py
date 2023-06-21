from django.shortcuts import render
import markdown2
import random
from . import util


# Display list of all entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Display entry page with content
def entry(request, title):

    # Get the list of all entries
    entries = util.list_entries()

    # Loop through each entry
    for entry in entries:

        # Check if entry is matched with requesting title with case-insensitive
        if entry.lower() == title.lower():

            # Render entry page if it's matched
            return render(request, "encyclopedia/entry.html", {
                "title": entry,
                "content": markdown2.markdown(util.get_entry(entry))
            })

    # Otherwise, render error page indicate that page did not exist
    return render(request, "encyclopedia/error.html", {
        "message": "Entry does not exist"
    })

# Search function for searching entry
def search(request):

    # Check the method if user request POST data to server
    if request.method == "POST":

        # Get the query that user search
        query = request.POST['q']

        # Get the list of entries
        entries = util.list_entries()

        # Create a recommendation list to store result that likely related to query
        recommendation = []

        # Loop through each entry
        for entry in entries:

            # Check if entry is matched with requesting title with case-insensitive
            if query.lower() == entry.lower():

                # Render the entry page if it's matched
                return render(request, "encyclopedia/entry.html", {
                    "title": entry,
                    "content": markdown2.markdown(util.get_entry(entry))
                })

            # Otherwise, check for the title that likely related to query
            elif query.lower() in entry.lower():

                # Append to the list of recommendation
                recommendation.append(entry)

        # Render search page with list of recommendation
        return render(request, "encyclopedia/search.html", {
        "recommendation": recommendation
    })

# Create a new page function
def new_page(request):

    # Check the method if user request POST data to server
    if request.method == "POST":

        # Get the list of entries
        entries = util.list_entries()

        # Get the title user request to POST to server
        title = request.POST['title']

        # Get the markdown content that user request to POST to server
        content = request.POST['markdown_content']

        # Loop through each entry
        for entry in entries:

            # Check if the title is in list of entries
            if title.lower() == entry.lower():

                # Render error page indicate that entry already exist
                return render(request, "encyclopedia/error.html", {
                "message": "Entry already exist"
            })

        # Save entry to the list of entries
        util.save_entry(title, content)

        # Render entry page that just saved
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(util.get_entry(title))
        })

    # If the method is GET then render newPage allow user to create a new page
    else:
        return render(request, "encyclopedia/newPage.html")

# Edit function allow user to edit content of the entry
def edit_page(request):

    # Check the method if user request POST data to server
    if request.method == "POST":

        # Get the title user request to POST to server
        title = request.POST['entry_title']

        # Render entry page that user request to edit
        return render(request, "encyclopedia/editPage.html", {
            "title": title,
            "content": util.get_entry(title)
        })

# Function allow user save the edit user make
def save_edit(request):

    # Check the method if user request POST data to server
    if request.method == "POST":

        # Get the title user request to POST to server
        title = request.POST['title']

        # Get the markdown content that user request to POST to server
        content = request.POST['markdown_content']

        # Get the list of entries
        entries = util.list_entries()

        # Loop through each entry
        for entry in entries:

            # Check if the entry is already exit
            if entry.lower() == title.lower():

                # Save the entry with new changes
                util.save_entry(entry, content)

                # Render the entry with new changes
                return render(request, "encyclopedia/entry.html", {
                    "title": entry,
                    "content": markdown2.markdown(util.get_entry(entry))
                })

        # Save the new changes
        util.save_entry(title, content)

        # Render entry with new changes
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(util.get_entry(title))
        })

# Random page function
def random_page(request):
    return entry(request, random.choice(util.list_entries()))
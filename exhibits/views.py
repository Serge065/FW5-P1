from django.shortcuts import render

from storage import load_authors, load_collections, load_conditions, load_exhibits


def exhibits(request):
    authors = load_authors()
    collections = load_collections()
    conditions = load_conditions()
    exhibits_dict = load_exhibits(authors, collections, conditions)

    context = {
        "exhibits": list(exhibits_dict.values()),
    }
    return render(request, "exhibits/exhibit_list.html", context)


def exhibit_detail(request, exhibit_id):
    authors = load_authors()
    collections = load_collections()
    conditions = load_conditions()
    exhibits_dict = load_exhibits(authors, collections, conditions)

    exhibit = exhibits_dict.get(exhibit_id)

    context = {"exhibit": exhibit}
    return render(
        request,
        "exhibits/exhibit_detail.html",
        context,
        status=404 if exhibit is None else 200,
    )
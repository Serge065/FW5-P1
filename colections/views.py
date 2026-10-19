from django.shortcuts import render

from storage import load_authors, load_collections, load_conditions, load_exhibits


def collections(request):
    colls = load_collections()
    context = {"collections": list(colls.values())}
    return render(request, "collections/collection_list.html", context)


def collection_detail(request, collection_id):
    colls = load_collections()
    collection = colls.get(collection_id)

    if collection is None:
        return render(
            request,
            "collections/collection_detail.html",
            {"collection": None},
            status=404,
        )

    authors_dict = load_authors()
    conditions = load_conditions()
    exhibits_dict = load_exhibits(authors_dict, colls, conditions)

    collection_exhibits = [
        ex for ex in exhibits_dict.values()
        if ex.collection and ex.collection.id == collection_id
    ]

    context = {"collection": collection, "exhibits": collection_exhibits}
    return render(request, "collections/collection_detail.html", context)
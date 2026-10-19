from django.shortcuts import render

from storage import load_authors, load_collections, load_conditions, load_exhibits


def authors(request):
    authors_dict = load_authors()
    context = {"authors": list(authors_dict.values())}
    return render(request, "authors/author_list.html", context)


def author_detail(request, author_id):
    authors_dict = load_authors()
    author = authors_dict.get(author_id)

    if author is None:
        return render(
            request,
            "authors/author_detail.html",
            {"author": None},
            status=404,
        )

    collections = load_collections()
    conditions = load_conditions()
    exhibits_dict = load_exhibits(authors_dict, collections, conditions)

    author_exhibits = [
        ex for ex in exhibits_dict.values()
        if ex.author and ex.author.id == author_id
    ]

    context = {"author": author, "exhibits": author_exhibits}
    return render(request, "authors/author_detail.html", context)
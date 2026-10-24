from django.shortcuts import render
from storage import load_authors, load_collections, load_conditions, load_exhibits
from db import execute

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
    
def exhibit_search(request):
    query = request.GET.get("q", "").strip()
    results = []
    
    if query:
        sql = """
            SELECT e.id, e.name, e.year, e.price, a.lastname AS author
            FROM exhibits e
            LEFT JOIN authors a ON e.author_id = a.id
            WHERE e.name ILIKE %s
            ORDER BY e.year DESC
        """
        results = execute(sql, (f"%{query}%",), fetch="all")
        
    return render(request, "exhibits/exhibit_search.html", {
        "query": query,
        "exhibits": results
    })

def exhibits_statistics(request):
    sql = """
        SELECT c.name AS collection_name, 
               COUNT(e.id) AS exhibits_count,
               COALESCE(SUM(e.price), 0) AS total_price
        FROM collections c
        LEFT JOIN exhibits e ON c.id = e.collection_id
        GROUP BY c.id, c.name
        ORDER BY exhibits_count DESC
    """
    stats = execute(sql, fetch="all")
    
    return render(request, "exhibits/exhibit_statistics.html", {
        "statistics": stats
    })
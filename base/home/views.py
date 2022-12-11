from django.shortcuts import render
from .utils import add_search_engine, get_search_engines, get_default_search_engine, get_bookmark_categories, get_shortcuts
from .models import SearchEngine

def home(request):
    search_engine = SearchEngine.objects.all()
    if not search_engine:
        add_search_engine()

    search_engines = get_search_engines()
    default_engine = get_default_search_engine(search_engines)
    bookmark_categories = get_bookmark_categories(request.user.id)
    shortcuts = get_shortcuts(bookmark_categories)

    context = {
        'default_engine': default_engine,
        'search_engines': search_engines,
        'bookmark_categories': bookmark_categories,
        'shortcuts': shortcuts
    }
    return render(request, 'home.html', context)

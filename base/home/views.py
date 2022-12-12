from django.shortcuts import render
from .models import SearchEngine
from .models import ApiKey
from .utils import add_search_engine
from .utils import get_search_engines
from .utils import get_default_search_engine
from .utils import get_bookmark_categories
from .utils import get_shortcuts
from .utils import add_api_service_names
from .utils import get_api_services

def home(request):
    search_engines = SearchEngine.objects.all()
    if not search_engines:
        add_search_engine()
        search_engines = get_search_engines()


    default_engine = get_default_search_engine(search_engines)
    user_id = request.user.id
    bookmark_categories = get_bookmark_categories(user_id)
    shortcuts = get_shortcuts(bookmark_categories)

    api_services = ApiKey.objects.filter(user=user_id)
    if not api_services:
        add_api_service_names(user_id)
        api_services = get_api_services(user_id)


    context = {
        'default_engine': default_engine,
        'search_engines': search_engines,
        'bookmark_categories': bookmark_categories,
        'shortcuts': shortcuts,
        'api_services': api_services
    }
    return render(request, 'home.html', context)

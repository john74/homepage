from django.shortcuts import render
from .models import SearchEngine
from .models import CustomUser
from .utils import add_search_engine
from .utils import get_search_engines
from .utils import get_default_search_engine
from .utils import get_bookmark_categories
from .utils import get_shortcuts
from .utils import add_api_service_names
from .utils import get_api_services
from .utils import  get_forecast_data
from .utils import  get_current_weather_data
from .utils import  get_week_forecast
from .utils import get_today_forecast
from .utils import get_current_weather


def home(request):
    search_engines = SearchEngine.objects.all()
    if not search_engines:
        add_search_engine()
        search_engines = get_search_engines()

    search_engines = get_search_engines()
    default_engine = get_default_search_engine(search_engines)
    user = CustomUser.objects.get(id=request.user.id)
    bookmark_categories = get_bookmark_categories(user.id)
    shortcuts = get_shortcuts(bookmark_categories)

    apis = get_api_services(user.id)
    if not apis:
        add_api_service_names(user)
        apis = get_api_services(user.id)

    forecast_weather_data = get_forecast_data(apis['open_weather'], user)
    week_forecast = get_week_forecast(forecast_weather_data)
    today_forecast = get_today_forecast(week_forecast)
    current_weather_data = get_current_weather_data(apis['open_weather'], user)
    current_weather = get_current_weather(current_weather_data)


    context = {
        'default_engine': default_engine,
        'search_engines': search_engines,
        'bookmark_categories': bookmark_categories,
        'shortcuts': shortcuts,
        'week_forecast': week_forecast,
        'today_forecast': today_forecast,
        'current_weather': current_weather,
        'apis': apis
    }
    return render(request, 'home.html', context)

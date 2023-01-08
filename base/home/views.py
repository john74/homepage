from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from settings.models import Profile
from bookmarks.models import Bookmark, BookmarkCategory
from .utils import get_default_search_engine
from .utils import get_shortcuts
from .utils import add_api_service_names
from .utils import get_api_services
from .utils import  get_forecast_data
from .utils import  get_current_weather_data
from .utils import  get_week_forecast
from .utils import get_today_forecast
from .utils import get_current_weather
from .utils import categorize_bookmarks
from .utils import get_bookmarks_with_subcategory
from .utils import get_bookmarks_with_no_subcategory
from .utils import get_bookmark_sub_categories


@login_required()
def home(request):
    user = request.user
    if user.first_login:
        return redirect('/setup/')

    # search_engines = SearchEngine.objects.all()
    # if not search_engines:
    #     add_search_engine()
    #     search_engines = get_search_engines()

    # search_engines = get_search_engines()
    # default_engine = get_default_search_engine(search_engines)
    # shortcuts = get_shortcuts(bookmark_categories)

    # apis = get_api_services(user.id)
    # if not apis:
    #     add_api_service_names(user)
    #     apis = get_api_services(user.id)

    # forecast_weather_data = get_forecast_data(apis['open_weather'], user)
    # week_forecast = get_week_forecast(forecast_weather_data)
    # today_forecast = get_today_forecast(week_forecast)
    # current_weather_data = get_current_weather_data(apis['open_weather'], user)
    # current_weather = get_current_weather(current_weather_data)

    from .utils import get_bookmark_main_categories
    bookmarks = Bookmark.objects.filter(category__user=user)
    bookmark_main_categories = get_bookmark_main_categories(bookmarks)
    bookmark_sub_categories = get_bookmark_sub_categories(bookmark_main_categories, bookmarks)

    categorized_bookmarks = categorize_bookmarks(bookmark_main_categories, bookmarks)

    bookmarks_with_subcategory = get_bookmarks_with_subcategory(bookmark_sub_categories, categorized_bookmarks)
    bookmarks_with_no_subcategory = get_bookmarks_with_no_subcategory(categorized_bookmarks)


    context = {
        'bookmark_categories': [category.name for category in bookmark_main_categories],
        'bookmarks_with_no_subcategory': bookmarks_with_no_subcategory,
        'bookmarks_with_subcategory': bookmarks_with_subcategory,
        # 'default_engine': default_engine,
        # 'search_engines': search_engines,
        # 'shortcuts': shortcuts,
        # 'week_forecast': week_forecast,
        # 'today_forecast': today_forecast,
        # 'current_weather': current_weather,
        # 'apis': apis
    }
    return render(request, 'home.html', context)

from datetime import datetime, date
import httpx
from .constants import API_KEY_SERVICE_NAMES
from bookmarks.models import Bookmark
from bookmarks.models import BookmarkCategory, BookmarkSubCategory, Bookmark
from settings.models import ApiKey, Profile


def get_default_search_engine(engines):
    for engine in engines:
        if engine['default']:
            return {
                "name": engine['name'],
                "action": engine['action'],
                "method": engine['method'],
                'name_attribute': engine['name_attribute'],
                'icon': engine['icon']
            }


def get_bookmark_main_categories(bookmarks):
    categories = set()
    for bookmark in bookmarks:
        categories.add(bookmark.category)
    return categories

def categorize_bookmarks(bookmark_categories, bookmarks):
    categorized_bookmarks = {}
    for category in bookmark_categories:
        category_bookmarks = []
        for bookmark in bookmarks:
            if bookmark.category == category:
                category_bookmarks.append(bookmark)
        if category_bookmarks:
            categorized_bookmarks[category] = category_bookmarks
    return categorized_bookmarks


def get_bookmark_sub_categories(bookmark_main_categories, bookmarks):
    sub_categories = {}
    for category in bookmark_main_categories:
        temp = []
        for bookmark in bookmarks:
            if bookmark.sub_category is None:
                continue
            if bookmark.sub_category in temp:
                continue
            if bookmark.sub_category.category == category:
                temp.append(bookmark.sub_category)
        sub_categories[category] = temp
    return sub_categories


def get_bookmarks_with_subcategory(bookmark_sub_categories, categorized_bookmarks):
    bookmarks_with_subcategory = {}
    for category, bookmarks in categorized_bookmarks.items():

        available_sub_categories = bookmark_sub_categories[category]
        if not available_sub_categories:
            continue

        temp = {}
        for sub_category in available_sub_categories:
            sub_temp = []
            for bookmark in bookmarks:
                if bookmark.sub_category == sub_category:
                    sub_temp.append(bookmark)
            temp[sub_category] = sub_temp
        bookmarks_with_subcategory[category.name] = temp
    return bookmarks_with_subcategory


def get_bookmarks_with_no_subcategory(categorized_bookmarks):
    bookmarks_with_no_subcategory = {}
    for category, bookmarks in categorized_bookmarks.items():
        temp = []
        for bookmark in bookmarks:
            if bookmark.sub_category is None:
                temp.append(bookmark)
        bookmarks_with_no_subcategory[category.name] = temp
    return bookmarks_with_no_subcategory


def get_shortcuts(bookmarks):
    shortcuts = []
    for bookmark in bookmarks:
        if bookmark.is_shortcut:
            shortcuts.append({
                'name': bookmark.name,
                'url': bookmark.url,
                'icon': bookmark.icon
            })
    return shortcuts


def get_api_services(user):
    apis = ApiKey.objects.filter(service__user=user)
    services = {}
    for api in apis:
        name = api.service.name.lower().replace(' ', '_')
        services[name] = api.key
    return services


# def add_api_service_names(user):
#     for name in API_KEY_SERVICE_NAMES:
#         Api.objects.create(
#             user = user,
#             name = name
#         )


def get_forecast_data(api_services, user):
    open_weather_api_key = api_services['open_weather']
    if not open_weather_api_key:
        return
    user_profile = Profile.objects.get(user=user)
    city = user_profile.city
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={open_weather_api_key}&units=metric'
    data = httpx.get(url)

    if data.status_code != 200:
        return
    return data.json()


def get_current_weather_data(api_services, user):
    open_weather_api_key = api_services['open_weather']
    if not open_weather_api_key:
        return
    user_profile = Profile.objects.get(user=user)
    city = user_profile.city
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_api_key}&units=metric'
    data = httpx.get(url)

    if data.status_code != 200:
        return
    weather_data = data.json()
    return {
        'temp': weather_data['main']['temp'],
        'temp_min': weather_data['main']['temp_min'],
        'temp_max': weather_data['main']['temp_max'],
        'feels_like': weather_data['main']['feels_like'],
        'weather_description': weather_data['weather'][0]['description']
    }


def get_week_forecast(data):
    if not data:
        return
    timezone = data['city']['timezone']
    days = data['list']
    forecast = {}
    for day in days:
        date_time = datetime.utcfromtimestamp(day['dt'] + timezone)
        forecast_time = date_time.strftime('%H:%M')
        if forecast_time in ['01:00', '02:00', '03:00', '04:00', '05:00', '06:00']:
            continue

        data = {
            'temp': day['main']['temp'],
            'temp_min': day['main']['temp_min'],
            'temp_max': day['main']['temp_max'],
            'feels_like': day['main']['feels_like'],
            'weather_description': day['weather'][0]['description']
        }

        forecast_date = date_time.strftime('%d-%m-%Y')
        if forecast_date in forecast:
            forecast[forecast_date].update({forecast_time:data})
        else:
            forecast[forecast_date] = {forecast_time:data}
    return forecast


def get_today_forecast(data):
    if not data:
        return
    today = date.today().strftime('%d-%m-%Y')
    today_forecast = None
    if today in data:
        today_forecast = data[today]
    return today_forecast


def get_current_weather(data):
    return {
        'temp': data['main']['temp'],
        'temp_min': data['main']['temp_min'],
        'temp_max': data['main']['temp_max'],
        'feels_like': data['main']['feels_like'],
        'weather_description': data['weather'][0]['description']
    }

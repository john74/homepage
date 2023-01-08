from datetime import datetime, date
import httpx
from .constants import API_KEY_SERVICE_NAMES
from bookmarks.models import Bookmark
from bookmarks.models import BookmarkCategory, BookmarkSubCategory, Bookmark

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


def categorize_bookmarks(bookmark_categories):
    categorized_bookmarks = {}
    for category in bookmark_categories:
        bookmarks = [bookmark for bookmark in Bookmark.objects.filter(category=category)]
        categorized_bookmarks[category] = Bookmark.objects.filter(category=category)
    return categorized_bookmarks


def get_bookmarks_with_subcategory(categorized_bookmarks):
    bookmarks_with_subcategory = {}
    for category, bookmarks in categorized_bookmarks.items():
        available_sub_categories = BookmarkSubCategory.objects.filter(category=category)
        if available_sub_categories:
            for sub_category in available_sub_categories:
                sub_category_bookmarks = bookmarks.filter(sub_category=sub_category)
                if sub_category_bookmarks:
                    sub_category_name = sub_category_bookmarks[0].sub_category.name
                    if category.name in bookmarks_with_subcategory:
                        bookmarks_with_subcategory[category.name].update(
                            {sub_category_name:sub_category_bookmarks}
                        )
                    else:
                        bookmarks_with_subcategory[category.name] = {sub_category_name:sub_category_bookmarks}
    return bookmarks_with_subcategory


def get_bookmarks_with_no_subcategory(categorized_bookmarks):
    bookmarks_with_no_subcategory = {}
    for category, bookmarks in categorized_bookmarks.items():
        no_sub_category_bookmarks = bookmarks.filter(sub_category=None)
        if no_sub_category_bookmarks:
            bookmarks_with_no_subcategory[category.name] = no_sub_category_bookmarks
    return bookmarks_with_no_subcategory


def get_shortcuts(bookmark_categories):
    shortcuts = []
    for bookmarks in bookmark_categories.values():
        for bookmark in bookmarks:
            shortcut = bookmark.shortcut
            if shortcut:
                shortcuts.append({
                    'name': bookmark.name,
                    'url': bookmark.url,
                    'icon': bookmark.icon
                })
    return shortcuts


def get_api_services(user_id):
    apis = Api.objects.filter(user=user_id)
    services = {}
    for api in apis:
        name = api.name.lower().replace(' ', '_')
        services[name] = api.key
    return services


def add_api_service_names(user):
    for name in API_KEY_SERVICE_NAMES:
        Api.objects.create(
            user = user,
            name = name
        )


def get_forecast_data(key, user):
    if not key:
        return
    city = user.city
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}&units=metric'
    data = httpx.get(url)

    if data.status_code != 200:
        return
    return data.json()


def get_current_weather_data(key, user):
    if not key:
        return
    city = user.city
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric'
    data = httpx.get(url)

    if data.status_code != 200:
        return
    return data.json()


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

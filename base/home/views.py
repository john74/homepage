from django.shortcuts import render
from .models import SearchEngine, BookmarkCategory, Bookmark

def home(request):
    search_engine = SearchEngine.objects.exists()
    if not search_engine:
        SearchEngine.objects.create(
            name = "Google",
            url = "https://www.google.com",
            form_action = "/search",
            form_method = "GET",
            name_attribute = 'q',
            default = True
        )

    search_engines = []
    for engine in SearchEngine.objects.all().order_by('-default', 'name'):
        name = engine.name
        url = engine.url[:-1] if engine.url[-1] == '/' else engine.url
        action = '/' + engine.form_action if engine.form_action[0] != '/' else engine.form_action
        method = engine.form_method
        name_attribute = engine.name_attribute
        icon = engine.icon
        search_engines.append({
            'name': name.strip(),
            'action': url.strip() + action.strip(),
            'method': method.strip(),
            'name_attribute': name_attribute.strip(),
            'default': engine.default,
            'icon': icon.strip()
        })

    default_search_engine = SearchEngine.objects.get(default=True)
    default_name = default_search_engine.name
    default_url = default_search_engine.url[:-1] if default_search_engine.url[-1] == '/' else default_search_engine.url
    default_action = '/' + default_search_engine.form_action if default_search_engine.form_action[0] != '/' else default_search_engine.form_action
    default_method = default_search_engine.form_method
    default_name_attribute = default_search_engine.name_attribute
    default_icon = default_search_engine.icon
    default_engine = {
        "name": default_name.strip(),
        "action": default_url.strip() + default_action.strip(),
        "method": default_method.strip(),
        'name_attribute': default_name_attribute.strip(),
        'icon': default_icon.strip()
    }

    user_bookmark_categories = BookmarkCategory.objects.filter(user=request.user.id)
    if user_bookmark_categories:
        bookmark_categories = {}
        for category in user_bookmark_categories:
            bookmarks = Bookmark.objects.filter(category=category)
            bookmark_categories[category] = bookmarks

    context = {
        'default_engine': default_engine,
        'search_engines': search_engines,
        'bookmark_categories': bookmark_categories
    }
    return render(request, 'home.html', context)

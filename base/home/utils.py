from .models import SearchEngine, BookmarkCategory, Bookmark


def add_search_engine():
    SearchEngine.objects.create(
        name = "Google",
        url = "https://www.google.com",
        form_action = "/search",
        form_method = "GET",
        name_attribute = 'q',
        default = True
    )


def get_search_engines():
    engines = SearchEngine.objects.all().order_by('-default', 'name')
    search_engines = []
    for engine in engines:
        name = engine.name
        url = engine.url[:-1] if engine.url[-1] == '/' \
              else engine.url
        action = '/' + engine.form_action if engine.form_action[0] != '/' \
                 else engine.form_action
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
    return search_engines


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


def get_bookmark_categories(user_id):
    categories = BookmarkCategory.objects.filter(user=user_id)
    bookmark_categories = {}
    if categories:
        for category in categories:
            bookmark_categories[category] = Bookmark.objects.filter(category=category)
    return bookmark_categories


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

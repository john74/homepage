SEARCH_ENGINES = {
    'Google': {
        'name': 'Google',
        'url': 'https://www.google.com',
        'form_action': '/search',
        'form_method': 'GET',
        'name_attribute': 'q',
        'default': True
    },
    'Duck Duck Go': {
        'name': 'Duck Duck Go',
        'url': 'https://duckduckgo.com',
        'form_action': '/',
        'form_method': 'GET',
        'name_attribute': 'q',
        'default': False
    },
    'Startpage': {
        'name': 'Startpage',
        'url': 'https://www.startpage.com',
        'form_action': '/sp/search',
        'form_method': 'POST',
        'name_attribute': 'query',
        'default': False
    },
    'Brave': {
        'name': 'Brave',
        'url': 'https://search.brave.com',
        'form_action': '/search',
        'form_method': 'GET',
        'name_attribute': 'q',
        'default': False
    },
    'Searx': {
        'name': 'Searx',
        'url': 'https://searx.garudalinux.org',
        'form_action': '/search',
        'form_method': 'POST',
        'name_attribute': 'q',
        'default': False
    },
    'Whoogle': {
        'name': 'Whoogle',
        'url': 'https://search.garudalinux.org',
        'form_action': '/search',
        'form_method': 'POST',
        'name_attribute': 'q',
        'default': False
    }
}

DEFAULT_THEMES = {
    'Dark': {
        'name': 'Dark',
        'primary_color': '#000',
        'secondary_color': '#000',
        'text_color': '#000'
    },
    'Light': {
        'name': 'Light',
        'primary_color': '#fff',
        'secondary_color': '#fff',
        'text_color': '#fff'
    }
}

EMAIL_SERVICES = ['Gmail', 'Proton Mail']

APIS = ['Open Weather']

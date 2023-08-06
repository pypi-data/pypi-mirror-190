from enum import Enum
from typing import Dict, List
from segmenthee.cart_api import *
from datetime import datetime as dt, timezone
import json
import re
from urllib.parse import urlparse, parse_qs, unquote


class CustomDimension(str, Enum):
    REFERRER = Config.CD_REFERRER
    REDIRECTS = Config.CD_REDIRECTS
    NAVIGATION = Config.CD_NAVIGATION
    TABTYPE = Config.CD_TABTYPE
    TABCOUNT = Config.CD_TABCOUNT
    SESSION_ID = Config.CD_SESSION_ID


CATEGORY_MAP: Dict[str, int] = {
    '/funko': -1,
    '/tarsasjatekok': 0,
    '/logikai-jatekok': 1,
    '/szabadidosport': 2,
    '/kreativ-kutyuk': 3,
    '/gyereksarok': 4
}

CATEGORY_FILTER: Dict[int, int] = {
    312: 0,
    633: 0,
    327: 0,
    332: 0,
    328: 0,
    542: 0,
    541: 0,
    392: 0,
    449: 0,

    657: -1,
    652: -1,
    655: -1,
    656: -1,

    154: 1,
    520: 1,
    160: 1,
    521: 1,
    331: 1,

    174: 2,
    213: 2,
    62: 2,
    77: 2,
    130: 2,
    121: 2,
    184: 2,
    170: 2,
    309: 2,
    320: 2,

    201: 3,
    496: 3,
    321: 3,
    322: 3,
    389: 3,
    202: 3
}

PREDEFINED_FILTER: Dict[str, int] = {
    'category|312/tarsasjatek_jatekido|8,9': 0,
    'category|312/tarsasjatek_jatekido|8': 0,
    'category|312/tarsasjatek_jatekido|8,10,9': 0,
    'category|312/tarsasjatek_jatekido|8,10,9,11': 0,
    'category|312/tarsasjatek_jatekosszam|19': 0,
    'category|312/tarsasjatek_jatekosszam|18': 0,
    'category|312/tarsasjatek_jatekosszam|20': 0,

    'category|174/aktiv_szabadido_hol_hasznalnad|5': 2,
    'category|174/aktiv_szabadido_hol_hasznalnad|2': 2,
    'category|174/aktiv_szabadido_hol_hasznalnad|1': 2,
    'category|174/aktiv_szabadido_hol_hasznalnad|4': 2,
}


INFO_PAGES: List[str] = [
    '/programok',
    '/blog',
    '/szakuzletunk',
    '/szallitasi-informaciok',
    '/fizetesi-modok',
    '/kapcsolat',
    '/reflexshop-tarsasjatekok',
    '/altalanos_szerzodesi_feltetelek',
    '/adatkezelesi_tajekoztato',
    '/index.php?route=information/personaldata'
]


def get_event(item: Dict) -> SessionBodyEvent:
    time = dt.fromtimestamp(item.get('_ts', int(dt.now().timestamp())), timezone.utc).isoformat()
    browsing_data = {"referrer": item.get(CustomDimension.REFERRER),
                     "tabcount": int(item[CustomDimension.TABCOUNT]),
                     "tabtype": item[CustomDimension.TABTYPE],
                     "navigation": item[CustomDimension.NAVIGATION],
                     "redirects": int(item[CustomDimension.REDIRECTS]),
                     'title': item.get('dt'),
                     'utm_source': get_utm_source(item),
                     'utm_medium': item.get('utm_medium', '')}

    if item.get('t') == 'pageview':
        parts = urlparse(get_fixed_url(item.get('dl')))
        query: Dict[str, str] = parse_query(parts.query)
        if parts.path == '/':
            event = MainPageBrowsingEvent(time, **browsing_data)
            return event
        if item.get('pa') == 'detail':
            browsing_data["product_id"] = item.get('pr1id')
            category: int = -1
            for path, cat in CATEGORY_MAP.items():
                if parts.path.startswith(path):
                    category = cat
                    break

            pr1pr = item.get('pr1pr', 0)
            price = int(pr1pr) if pr1pr != 'NaN' else 0
            event = ProductPageBrowsingEvent(time, category, price, **browsing_data)
            return event
        if parts.path == '/szakuzletunk':
            event = ShopListBrowsingEvent(time, **browsing_data)
            return event
        if parts.path == '/reflexshop-tarsasjatekok':
            event = BoardGamesUpdateEvent(time, **browsing_data)
            return event
        if parts.path == '/cart':
            event = CartBrowsingEvent(time, **browsing_data)
            return event
        if parts.path == '/checkout':
            if parts.fragment == '/customerdata/':
                event = CustomerDataEntryBrowsingEvent(time, **browsing_data)
                return event
            if parts.fragment == '/shippingmethod/':
                event = ShippingMethodBrowsingEvent(time, **browsing_data)
                return event
            if parts.fragment == '/paymentmethod/':
                event = PaymentMethodBrowsingEvent(time, **browsing_data)
                return event
            if parts.fragment == '/confirmation/':
                event = ConfirmationPageBrowsingEvent(time, **browsing_data)
                return event

            event = CheckoutPageBrowsingEvent(time, **browsing_data)
            return event

        if parts.path == '/index.php' and query.get('route') == 'checkout/success':
            event = CheckoutSuccessPageBrowsingEvent(time, **browsing_data)
            return event

        if parts.path == '/index.php' and query.get('route') == 'wishlist/wishlist':
            event = WishListBrowsingEvent(time, **browsing_data)
            return event

        if parts.path == '/index.php' and query.get('route', '').startswith('account/'):
            event = AccountPageBrowsingEvent(time, **browsing_data)
            return event

        # CategoryPage
        for path, category in CATEGORY_MAP.items():
            if parts.path == path or parts.path.find(path) > -1:
                kwargs = {"category_id": category, **get_pagination(query), **browsing_data}
                event = CategoryPageBrowsingEvent(time, **kwargs)
                return event

        # CategoryPage
        if parts.path == '/index.php' and query.get('route') == 'product/list':
            if query.get('keyword') is None and (cat_id := query.get('category_id')):
                category = CATEGORY_FILTER.get(int(cat_id), -1)
                kwargs = {"category_id": category, **get_pagination(query), **browsing_data}
                event = CategoryPageBrowsingEvent(time, **kwargs)
                return event

        # PredefinedFilter -> CategoryPage -> SearchResults
        if parts.path == '/index.php' and query.get('route') == 'filter':
            category = PREDEFINED_FILTER.get(query.get('filter'), -2)
            if category > -2:
                kwargs = {"category_id": category, **get_pagination(query), **browsing_data}
                event = PredefinedFilterBrowsingEvent(time, **kwargs)
                return event

            if query.get('filter', '').startswith('category|') and query.get('keyword') is None:
                numbers = re.findall(r'\d+', query.get('filter'))
                category = CATEGORY_FILTER.get(int(numbers[0]), -2) if numbers else -2
                if category > -2:
                    kwargs = {"category_id": category, **get_pagination(query), **browsing_data}
                    event = CategoryPageBrowsingEvent(time, **kwargs)
                    return event

            kwargs = {**get_pagination(query), **browsing_data}
            event = SearchResultsBrowsingEvent(time, **kwargs)
            return event

        # SearchResults
        if parts.path == '/kereses' or query.get('route') == 'product/list':
            kwargs = {**get_pagination(query), **browsing_data}
            event = SearchResultsBrowsingEvent(time, **kwargs)
            return event

        # InformationPage
        if parts.path in INFO_PAGES or query.get('route') in INFO_PAGES:
            event = InformationPageBrowsingEvent(time, **browsing_data)
            return event

        event = BrowsingEvent(time, **browsing_data)
        return event

    if item.get('t') == 'event':
        if item.get('ec') == 'Értesítés kérése' and item.get('ea') == 'Értesítés kérése sikeres':
            event = RegistrationEvent(time)
            return event
        if item.get('ec') == 'e-cart' and item.get('ea') == 'update':
            data = json.loads(item.get('el'))
            delta_count = data.get('itemCount')
            delta_total = round(data.get('total'), 2)
            event = CartModifyEvent(time, delta_count, delta_total)
            return event
        if item.get('ec') == 'OptiMonk':
            if item.get('ea') == 'shown':
                event = CouponOfferedEvent(time, item.get('el'))
                return event
            if item.get('ea') == 'filled':
                event = CouponAcceptedEvent(time, item.get('el'))
                return event

    event = SystemEvent(time)
    return event


def get_utm_source(item: Dict) -> str:
    keys = item.keys()
    if 'utm_source' in keys:
        return item.get('utm_source')
    if 'gclid' in keys:
        return 'google'
    if 'fbclid' in keys:
        return 'facebook'
    return ''


def get_fixed_url(url: str) -> str:
    p1 = url.find('?')
    p2 = url.find('&')
    if p1 == -1 and p2 > -1:
        return url[:p2] + '?' + url[p2+1:]
    return url[:p2] + url[p1:] + url[p2:p1] if -1 < p2 < p1 else url


def parse_query(query: str) -> Dict[str, str]:
    return {} if query.strip() == '' else {k: v[0] for k, v in parse_qs(unquote(query)).items()}


def get_pagination(query: Dict) -> Dict:
    pagination = {"page": query.get('page', '1')}
    if 'sort_order' in query.keys():
        pagination["sort"] = query.get('sort_order')
    elif 'sort' in query.keys():
        pagination["sort"] = query.get('sort') + '_' + query.get('order', 'asc').lower()
    else:
        pagination["sort"] = 'default'
    return pagination

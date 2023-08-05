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
    '/karacsonyi_ajandekotletek': -1,
    '/akciok_es_ujdonsagok': -1,

    '/vibrator': 3,

    '/erotikus_eszkozok_noknek': 1,
    '/elojatekszerek': 1,
    '/gesagolyok': 1,
    '/dildok': 1,
    '/analjatekok': 1,
    '/felcsatolhato_dildok': 1,
    '/szemerem_es_mellpumpak': 1,
    '/gumiferfi': 1,
    '/babydollok_neglizsek_kontosok': 1,
    '/szexi_bodyk': 1,
    '/fehernemu_es_mellemelo_szettek': 1,
    '/cicaruhak': 1,
    '/szexi_ruhak': 1,
    '/felsok_fuzok_overallok': 1,
    '/jelmezek_parokak': 1,
    '/tangak_noi_alsok': 1,
    '/harisnyatartok_harisnyakotok': 1,
    '/kiegeszitok_ekszerek': 1,
    '/plus_size_fehernemuk': 1,

    '/ferfiaknak': 0,
    '/fleshlight_maszturbatorok': 0,
    '/muvaginak': 0,
    '/tenga-es-svakom-kenyeztetok': 0,
    '/ajkak-es-egyeb-oromszerzok': 0,
    '/mupopsik': 0,
    '/prosztata_izgatok': 0,
    '/guminok': 0,
    '/ferfi_alsok_es_kiegeszitok': 0,
    '/peniszgyuruk': 0,
    '/peniszpumpak_es_penisznoveles': 0,
    '/peniszkopenyek_es_mandzsettak': 0,

    '/drogeria': 2,
    '/testapolas': 2,
    '/termektisztitas_karbantartas': 2,
    '/masszazsolajok_es_gelek': 2,
    '/potencianovelo_ferfiaknak': 2,
    '/kesleltetok_erekciotartok': 2,
    '/vagyfokozok_noknek': 2,
    '/drogeria/ovszerek': 2,
    '/drogeria/szines-izes-ovszer': 2,
    '/specialis-meretu-ovszerek': 2,
    '/vizbazisu_sikositok': 2,
    '/izes_illatos_es_izgato_hatasu_sikositok': 2,
    '/szilikonos_hibrid_anal_sikositok': 2,
    '/tartozekok-elem-tolto': 2,

    '/szorakozas': 4,
    '/elso-jatekszereim': 4,
    '/leanybucsu': 4,
    '/legenybucsu': 4,
    '/szextarsasjatekok': 4,
    '/egyeb_ajandekok': 4,

    '/bdsm': 5,
}

CATEGORY_FILTER: Dict[int, int] = {
    851: 3,
    836: 3,
    84: 3,
    70: 3,
    75: 3,
    833: 3,
    847: 3,
    64: 3,
    63: 3,
    846: 3,
    80: 3,
    843: 3,
    908: 3,
    870: 3,
    69: 3,
    868: 3,
    873: 3,
    81: 3,

    59: 1,
    62: 1,
    85: 1,
    867: 1,
    871: 1,
    78: 1,
    61: 1,
    99: 1,
    112: 1,
    102: 1,
    44: 1,
    101: 1,
    113: 1,
    49: 1,
    114: 1,
    105: 1,
    110: 1,
    821: 1,

    801: 0,
    88: 0,
    850: 0,
    874: 0,
    859: 0,
    805: 0,
    28: 0,
    117: 0,
    90: 0,
    95: 0,
    91: 0,

    131: 2,
    30: 2,
    803: 2,
    872: 2,
    133: 2,
    135: 2,
    96: 2,
    306: 2,
    134: 2,
    136: 2,
    123: 2,
    804: 2,
    856: 2,

    903: 4,
    137: 4,
    141: 4,
    143: 4,
    140: 4,

    884: 5,
    857: 5,
    777: 5,
    126: 5,
    65: 5,
    125: 5
}

PREDEFINED_FILTER: Dict[str, int] = {
}

INFO_PAGES: List[str] = [
    '/gyik',
    '/megoldasaink/#diszkrecio',
    '/megoldasaink/#ingyenesszallitas',
    '/hirek',
    '/kapcsolat',
    '/rolunk',
    '/ajandekutalvany',
    '/elallas',
    '/merettabla',
    '/husegpont',
    '/online-szextanfolyam',
    '/aszf',
    '/adatvedelmi_nyilatkozat',
    '/impresszum',
    '/fontos-informacio-termekeinkrol',
    '/partner-program'
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
            if category := PREDEFINED_FILTER.get(query.get('filter')):
                kwargs = {"category_id": category, **get_pagination(query), **browsing_data}
                event = PredefinedFilterBrowsingEvent(time, **kwargs)
                return event

            if query.get('filter', '').startswith('category|') and query.get('keyword') is None:
                numbers = re.findall(r'\d+', query.get('filter'))
                if len(numbers) > 0 and (category := CATEGORY_FILTER.get(int(numbers[0]), -1)):
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

import re
import json
import requests
import datetime

from bson import json_util
from bs4 import BeautifulSoup
from string import punctuation


# Enter the area you want to collect property data from, keep blank ("") to search whole of NI
SEARCH_AREA = ""

DIR_PATH = '/home/owen/Code/Sukasa/research/data'

BASIC_REQUEST = {
    "baseURL": "https://www.propertypal.com",
    "forSalePath": "/property-for-sale",
    "forRentPath": "/property-to-rent",
    "sortOptions": {
        "mostPopular": "/sort-hot",
        "recentlyAdded": "/sort-dateHigh",
        "recentlyUpdated": "/sort-updatedHigh",
        "priceLowHigh": "/sort-priceLow",
        "priceHighLow": "/sort-priceHigh"
    },
    "userAgent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0"
}

POSTCODE_AREAS = {
    'BT1': 'central belfast',
    'BT2': 'central belfast',
    'BT3': 'central belfast',
    'BT4': 'east belfast',
    'BT5': 'east belfast',
    'BT6': 'east belfast',
    'BT7': 'central belfast',
    'BT8': 'south belfast',
    'BT9': 'south belfast',
    'BT10': 'south belfast',
    'BT11': 'west belfast',
    'BT12': 'west belfast',
    'BT13': 'north belfast',
    'BT14': 'north belfast',
    'BT15': 'central belfast',
    'BT16': 'east belfast',
    'BT17': 'south belfast',
    'BT18': 'holywood',
    'BT19': 'bangor',
    'BT20': 'bangor',
    'BT21': 'donaghadee',
    'BT22': 'strangford',
    'BT23': 'newtownards',
    'BT24': 'ballynahinch',
    'BT25': 'dromore',
    'BT26': 'hillsborough',
    'BT27': 'east lisburn',
    'BT28': 'lisburn',
    'BT29': 'crumlin',
    'BT30': 'downpatrick',
    'BT31': 'castlewellan',
    'BT32': 'banbridge',
    'BT33': 'newcastle',
    'BT34': 'hilltown',
    'BT35': 'newry',
    'BT36': 'glengormley',
    'BT37': 'whiteabbey',
    'BT38': 'carrickfergus',
    'BT39': 'ballyclare',
    'BT40': 'larne',
    'BT41': 'antrim',
    'BT42': 'ballymena',
    'BT43': 'ballymena',
    'BT44': 'ballymena',
    'BT45': 'magherafelt',
    'BT46': 'maghera',
    'BT47': 'londonderry',
    'BT48': 'londonderry',
    'BT49': 'limavady',
    'BT50': 'limavady',
    'BT51': 'coleraine',
    'BT52': 'coleraine',
    'BT53': 'ballymoney',
    'BT54': 'ballycastle',
    'BT55': 'portstewart',
    'BT56': 'portrush',
    'BT57': 'bushmills',
    'BT58': 'newtownabbey',
    'BT60': 'armagh',
    'BT61': 'armagh',
    'BT62': 'craigavon',
    'BT63': 'craigavon',
    'BT64': 'craigavon',
    'BT65': 'craigavon',
    'BT66': 'craigavon',
    'BT67': 'craigavon',
    'BT68': 'caledon',
    'BT69': 'aughnacloy',
    'BT70': 'dungannon',
    'BT71': 'dungannon',
    'BT74': 'eniskillen',
    'BT75': 'fivemiletown',
    'BT76': 'clogher',
    'BT77': 'augher',
    'BT78': 'omagh',
    'BT79': 'omagh',
    'BT80': 'cookstown',
    'BT81': 'castlederg',
    'BT82': 'strabane',
    'BT92': 'eniskillen',
    'BT93': 'eniskillen',
    'BT94': 'eniskillen',
    'Belfast': 'central belfast'
}


POSTCODE_TO_PARLIAMENTARIES = {
  'bt1': 'east belfast',
  'bt2': 'south belfast',
  'bt3': 'east belfast',
  'bt4': 'east belfast',
  'bt5': 'east belfast',
  'bt6': 'east belfast',
  'bt7': 'south belfast',
  'bt8': 'south belfast',
  'bt9': 'south belfast',
  'bt10': 'south belfast',
  'bt11': 'west belfast',
  'bt12': 'west belfast',
  'bt13': 'west belfast',
  'bt14': 'north belfast',
  'bt15': 'north belfast',
  'bt16': 'east belfast',
  'bt17': 'west belfast',
  'bt18': 'north down',
  'bt19': 'north down',
  'bt20': 'north down',
  'bt21': 'north down',
  'bt22': 'strangford',
  'bt23': 'strangford',
  'bt24': 'strangford',
  'bt25': 'lagan valley',
  'bt26': 'lagan valley',
  'bt27': 'lagan valley',
  'bt28': 'lagan valley',
  'bt29': 'south antrim',
  'bt30': 'south down',
  'bt31': 'south down',
  'bt32': 'south down',
  'bt33': 'south down',
  'bt34': 'south down',
  'bt35': 'newry and armagh',
  'bt36': 'south antrim',
  'bt37': 'north belfast',
  'bt38': 'east antrim',
  'bt39': 'south antrim',
  'bt40': 'east antrim',
  'bt41': 'south antrim',
  'bt42': 'south antrim',
  'bt43': 'north antrim',
  'bt44': 'north antrim',
  'bt45': 'mid ulster',
  'bt46': 'mid ulster',
  'bt47': 'east londonderry',
  'bt48': 'foyle',
  'bt49': 'east londonderry',
  'bt51': 'east londonderry',
  'bt52': 'east londonderry',
  'bt53': 'north antrim',
  'bt54': 'north antrim',
  'bt55': 'east londonderry',
  'bt56': 'east londonderry',
  'bt57': 'north antrim',
  'bt58': 'newtownabbey',
  'bt60': 'newry and armagh',
  'bt61': 'newry and armagh',
  'bt62': 'upper bann',
  'bt63': 'upper bann',
  'bt64': 'upper bann',
  'bt65': 'upper bann',
  'bt66': 'upper bann',
  'bt67': 'upper bann',
  'bt68': 'newry and armagh',
  'bt69': 'fermanagh and south tyrone',
  'bt70': 'fermanagh and south tyrone',
  'bt71': 'fermanagh and south tyrone',
  'bt74': 'fermanagh and south tyrone',
  'bt75': 'fermanagh and south tyrone',
  'bt76': 'fermanagh and south tyrone',
  'bt77': 'fermanagh and south tyrone',
  'bt78': 'west tyrone',
  'bt79': 'west tyrone',
  'bt80': 'mid ulster',
  'bt81': 'west tyrone',
  'bt82': 'west tyrone',
  'bt92': 'fermanagh and south tyrone',
  'bt93': 'fermanagh and south tyrone',
  'bt94': 'fermanagh and south tyrone' 
}


COUNTY_POSTCODE = {
    'Antrim': [],
    'Armagh': [],
    'Down': [],
    'Fermanagh': [],
    'Londonderry': [],
    'Tyrone': []
}


AMENITIES_LIST = ['garden', 'garage', 'driveway', 'parking', 'bay window']


def get_property_page(area, page_number, property_type, sort_by):
    type_url = 'forSalePath' if property_type == 'sale' else 'forRentPath'
    url = '{}{}'.format(
        BASIC_REQUEST['baseURL'],
        BASIC_REQUEST[type_url])
    if area:
        url += '/{}'.format(area)
    if sort_by is not None:
        url += BASIC_REQUEST['sortOptions'][sort_by]
    if page_number > 1:
        url += '/page-{}'.format(page_number)
    request_page = requests.get(
        url=url,
        headers={'User-Agent': BASIC_REQUEST['userAgent']})
    if request_page.status_code == 200:
        return BeautifulSoup(request_page.content, "lxml")
    else:
        raise ValueError(
            'Page not found: The request received a {} status code'.format(
                request_page.status_code))


def get_final_page_number(first_page_soup):
    raw_page_number = first_page_soup.find("li", {"class", "paging-last"}).get_text()
    clean_page_number = raw_page_number.strip().replace(',', '')
    return int(clean_page_number)


def get_all_main_images(page_soup):
    property_images = []
    all_images = page_soup.findAll("div", {"class": "propbox-img"})
    for image in all_images:
        string_image = str(image)
        if 'is-no-photo' in string_image:
            property_images.append(None)
        elif 'propbox-time' in string_image or 'openviewing' in string_image:
            property_images.append(
                image.find("img").attrs['data-lazy-src'])
    return property_images


def strip_punctuation(string):
    prep_string = string.replace('-', ' ')
    return ''.join(char for char in prep_string if char not in punctuation)


def clean_price(price):
    if price is None:
        return price
    else:
        raw_price = price.get_text()
        cleaned_price = raw_price.strip().replace(',', '')
    return float(re.sub(r'[^0-9.]', '', str(cleaned_price)))


def get_currency(raw_price):
    currencies = {
        '£': 'pound',
        '€': 'euro',
        '$': 'dollar'
    }
    string_price = str(raw_price)
    for c, v in currencies.items():
        if c in string_price:
            return v
    return 'unknown'


def get_price(page_soup):
    offer = page_soup.find("span", {"class": "price-offers"})
    if offer is not None:
        offer = offer.get_text().strip()
    price = page_soup.find("span", {"class": "price-value"})
    min_price = page_soup.find("span", {"class": "price-min"})
    max_price = page_soup.find("span", {"class": "price-max"})
    currency = 'unknown'
    if price is not None:
        currency = get_currency(price)
    elif min_price is not None:
        currency = get_currency(price)
    return {
        'offer': offer,
        'price': clean_price(price),
        'minPrice': clean_price(min_price),
        'maxPrice': clean_price(max_price),
        'currency': currency
    }


def get_property_id(html_string, clean_address, id_length=10):
    property_id = ''
    start_string = html_string.find(clean_address)
    for i in range(id_length):
        new_char = html_string[start_string + len(clean_address) + i]
        if new_char is not '"':
            property_id += html_string[start_string + len(clean_address) + i]
        else:
            break
    return property_id


def get_clean_address(address, town):
    trans_address = strip_punctuation(address).lower().replace(' ', '-')
    return str('/{}-{}/'.format(
        trans_address,
        town.lower()))


def get_hyperlink(page_soup, address, town):
    if town is None or address is None:
        return None

    clean_address = get_clean_address(
        address=address,
        town=town)
    property_id = get_property_id(
        html_string=str(page_soup),
        clean_address=clean_address)
    return clean_address + property_id


def get_address(page_soup):
    raw_address = page_soup.find("span", {"class": "propbox-addr"})
    if raw_address is not None:
        raw_address = raw_address.get_text()
    else:
        return None
    clean_address = str(raw_address.rstrip(', '))
    return clean_address


def get_postcode(page_soup):
    raw_postcode = page_soup.find("span", {"class": "propbox-town"})
    clean_postcode = str(raw_postcode.get_text())
    return clean_postcode


def get_brief(page_soup):
    raw_brief = page_soup.find("p", {"class": "propbox-brief"})
    if raw_brief is None:
        return None
    else:
        clean_brief = str(raw_brief.get_text().strip())
        return clean_brief


def get_estate_agent(page_soup):
    agent = page_soup.find("p", {"class": "propbox-account"})
    agent_data = {'name': None, 'branch': None}
    if agent is not None:
        rep = {
            'Marketed by ': '',
            'Developed by ': ''
        }
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        agent = pattern.sub(
            lambda m: rep[re.escape(m.group(0))],
            agent.get_text().strip())
        if '(' in agent:
            agent_data['name'] = str(agent.split(' (')[0])
            agent_data['branch'] = str(agent[agent.find("(") + 1:agent.find(")")])
        else:
            agent_data['name'] = str(agent)
    return agent_data


def property_location(detail_soup):
    map_data = detail_soup.find('a', {'class': 'Mediabox-miniBoxMap'}).attrs
    if map_data is None:
        return {
            'lat': float(0),
            'lon': float(0)
        }
    map_data_options = json.loads(map_data['data-map-options'])
    return {
        'lat': float(map_data_options['lat']),
        'lon': float(map_data_options['lng'])
    }


def amenity_present(detail_page, amenity):
    return amenity in detail_page.decode().lower()


def parse_epc_rating(epc_rating_list):
    parsed_epc = {
        'actual': {
            'band': None,
            'score': None
        },
        'potential': {
            'band': None,
            'score': None
        }
    }
    if len(epc_rating_list) == 2:
        parsed_epc_values = []
        for epc in epc_rating_list:
            match = re.match(
                pattern=r"([a-z]+)([0-9]+)",
                string=epc,
                flags=re.I)
            if match:
                items = match.groups()
                for item in items:
                    parsed_epc_values.append(item)
        parsed_epc['actual']['band'] = parsed_epc_values[0]
        parsed_epc['actual']['score'] = int(parsed_epc_values[1])
        if len(parsed_epc_values) > 2:
            parsed_epc['potential']['band'] = parsed_epc_values[2]
            parsed_epc['potential']['score'] = int(parsed_epc_values[3])
    return parsed_epc


def get_property_details(hyperlink):
    if hyperlink is None:
        return None

    data = {}
    page_response = requests.get(
        url='{}{}'.format(
            BASIC_REQUEST['baseURL'],
            hyperlink),
        headers={'User-Agent': BASIC_REQUEST['userAgent']})
    if page_response.status_code == 200:
        detail_page = page_response.content
        detail_soup = BeautifulSoup(detail_page, "lxml")
        key_info_table = detail_soup.find("table", {"id": "key-info-table"})
        key_info_rows = key_info_table.find_all('tr')
        for row in key_info_rows:
            row_title = str(row.findAll('th')[0].get_text().lower())
            if row_title != 'stamp duty' and row_title != 'price':
                cols = row.findAll('td')
                cols = [ele.text.strip() for ele in cols]
                if cols[0] != "":
                    info = [ele for ele in cols if ele][0].encode('ascii', 'ignore').strip().decode()
                    if row_title == 'rates':
                        info = float(info.replace(' pa*', '').replace(',', ''))
                    elif 'epc' in row_title:
                        info = info.split('\n', 1)[0]
                        info = parse_epc_rating(
                            epc_rating_list=info.split('/'))
                    elif row_title in ['bathrooms', 'bedrooms', 'receptions']:
                        info = int(info)
                    else:
                        info = str(info)
                    data[to_camel_case(string=row_title)] = info
        data['amenities'] = {}
        for amenity in AMENITIES_LIST:
            data['amenities'][to_camel_case(string=amenity)] = amenity_present(
                detail_page=detail_page,
                amenity=amenity)
        data['location'] = property_location(
            detail_soup=detail_soup)
        data['keyInformation'] = key_information(
            detail_soup=detail_soup)
        data['phoneNumber'] = enquiry_phone_number(
            detail_soup=detail_soup)
        data['propertyImages'] = property_images(
            detail_soup=detail_soup)
        data['longPostcode'] = detail_soup.find(
            "span", {"class": "text-ib"}).get_text()
        # data['htmlPage'] = str(detail_soup)
        return data
    else:
        return None
    
    
def multiple_replace(pattern_dict, text):
    regex = re.compile("(%s)" % "|".join(map(re.escape, pattern_dict.keys())))
    return regex.sub(lambda mo: pattern_dict[mo.string[mo.start():mo.end()]], text) 


def key_information(detail_soup):
    key_info = detail_soup.find("div", {"class": "prop-descr-text"})
    if key_info is not None:
        key_info = key_info.get_text()
    else:
        return None
    encoded_key_info = key_info.encode('ascii', 'ignore').decode()
    patterns = { "\n": " ", "\t": " " }
    cleaned_key_info = multiple_replace(
        pattern_dict=patterns, 
        text=encoded_key_info)
    return re.sub(' +', ' ', str(cleaned_key_info))


def property_images(detail_soup):
    photos = []
    photo_list = detail_soup.find("div", {"class": "Slideshow"})
    if len(photo_list) > 0:
        photo_details = photo_list.findAll("a")
        for photo in photo_details:
            photos.append(photo.attrs['href'])
    return photos


def enquiry_phone_number(detail_soup):
    enquiry_object = detail_soup.find("a", {"class": "tel-reveal enquiry-tel btn btn-red"})
    if enquiry_object:
        phone_number = enquiry_object.attrs['data-office-phone']
    else:
        phone_number = None
    return phone_number


def to_camel_case(string):
    humped_camel = ''.join(x for x in string.title() if not x.isspace())
    return humped_camel[0].lower() + humped_camel[1:]


def generate_tags(taggables):
    tags = []
    for tag in taggables:
        if tag is not None:
            tags.append(tag.lower())
    return tags


def find_county(postcode):
    for k, v in COUNTY_POSTCODE.items():
        if postcode in v:
            return k
    return 'Unknown'


def property_dataset(page_soup):
    dataset = []
    property_details = page_soup.findAll("div", {"class": "propbox-details"})
    number_of_properties = len(property_details)
    for i in range(number_of_properties):
        try:
            address = get_address(property_details[i])
            postcode_split = get_postcode(property_details[i]).split()
            if len(postcode_split) > 1:
                town = postcode_split[0]
                postcode = postcode_split[1]
                if postcode in POSTCODE_AREAS.keys():
                    area = POSTCODE_AREAS[postcode]
                else:
                    area = None
                county = find_county(
                    postcode=postcode)
                hyperlink = get_hyperlink(
                    page_soup=page_soup,
                    address=address,
                    town=town)
                property_id = get_property_id(
                    html_string=str(page_soup),
                    clean_address=get_clean_address(
                        address=address,
                        town=town))
            else:
                area = county = town = postcode = hyperlink = property_id = None
            tags = generate_tags(
                taggables=[address, town, postcode, area])
            print('{}{}'.format(
                    BASIC_REQUEST['baseURL'],
                    hyperlink))
            details = {}
            try:
                details = get_property_details(hyperlink)
            except:
                print("Failed parsing {}".format(hyperlink))            
            dataset.append({
                'timeAdded': datetime.datetime.now(),
                'propertyId': property_id,
                'tags': tags,
                'address': address,
                'town': town,
                'area': area,
                'county': county,
                'postcode': postcode,
                'priceInfo': get_price(property_details[i]),
                'brief': get_brief(property_details[i]),
                'estateAgent': get_estate_agent(property_details[i]),
                'hyperlink': '{}{}'.format(
                    BASIC_REQUEST['baseURL'],
                    hyperlink),
                'details': details
            })
        except:
            print("Could not parse property!")
    return dataset


def scrape_ni_dataset(area, property_type, sort_by,
                      page_limit=False, first_only=False):
    first_page = get_property_page(
        area=area,
        page_number=0,
        property_type=property_type,
        sort_by=sort_by)
    if first_only:
        final_page_number = 2
    elif page_limit:
        final_page_number = 5
    else:
        final_page_number = get_final_page_number(
            first_page)
    print('Parsing page 1 of {}...'.format(final_page_number))
    property_data = property_dataset(first_page)
    for page_number in range(2, final_page_number):
        try:
            print('Parsing page {} of {}...'.format(
                page_number, final_page_number))
            property_page = get_property_page(
                    area=area,
                    page_number=page_number,
                    property_type=property_type,
                    sort_by=sort_by)
            property_data += property_dataset(property_page)
        except ValueError:
            print("Oops! Some parsing went wrong in search page {}".format(
                    page_number))
    return property_data


def save_to_file(property_data):
    properties_json = json.dumps(property_data, default=json_util.default)
    json_file = open('{}/property/all-ni-property-data-{}.json'.format(
            DIR_PATH, datetime.date.today()), 'w')
    json_file.write(properties_json)
    json_file.close()


properties = scrape_ni_dataset(
    area=SEARCH_AREA,
    property_type='sale',
    sort_by='recentlyAdded')

save_to_file(properties)


def merge_with_master(master_dataset, all_property_ids, property_dataset):
    for property in property_dataset:
        if property['propertyId'] in all_property_ids:
            return {
                'masterDataset': master_dataset,
                'shouldContinue': False
            }
        else:
            master_dataset.append(property)
    return {
        'masterDataset': master_dataset,
        'shouldContinue': True
    }



for property in properties:
    print(property['priceInfo']['price'])

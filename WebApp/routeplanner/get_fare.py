import requests
from bs4 import BeautifulSoup

def calc_fare(shape_id, board, alight):

    GTFSRoute.object.get(shape_id=shape_id).route_name
    direction = shape_id[-1]
    url = f"https://www.dublinbus.ie/Fare-Calculator/Fare-Calculator-Results/?routeNumber={route_name}&direction={direction}&board={board}&alight={alight}"
    fare_page = requests.get(url)
    soup = BeautifulSoup(fare_page.text, 'html.parser')
    fare_elem_id = "ctl00_FullRegion_MainRegion_ContentColumns_holder_FareListingControl_lblFare"
    fare_elem = soup.find_all(id=fare_elem_id)
    return fare_elem[0].contents[0]



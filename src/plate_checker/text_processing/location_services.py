import asyncio
import winsdk.windows.devices.geolocation as wdg
from geopy.geocoders import Nominatim

def find_location():
    async def getCoords():
        locator = wdg.Geolocator()
        pos = await locator.get_geoposition_async()
        geolocator = Nominatim(user_agent="toms_amazing_app")
        print (str(pos.coordinate.latitude), str(pos.coordinate.longitude))
        location = geolocator.reverse(f'{str(pos.coordinate.latitude)}, {str(pos.coordinate.longitude)}')
        list=location[0].split(',')
        
        return [pos.coordinate.latitude, pos.coordinate.longitude], list[4],list[0], list[1]


    def getLoc():
        try:
            return asyncio.run(getCoords())
        except PermissionError:
            print("ERROR: You need to allow applications to access you location in Windows settings")
    return getLoc()

find_location()

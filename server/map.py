import googlemaps
from key import maps_key
import numpy as np
from warnings import warn

from pprint import pprint

map_client = googlemaps.Client(maps_key)




def get_input_prompt_for_location(place_lat, place_lng):
    place_search = map_client.places_nearby(location=(place_lat, place_lng), radius=10)

    info = place_search["results"][0]
    lat = info["geometry"]["location"]["lat"]
    lng = info["geometry"]["location"]["lng"]
    dist = np.sqrt((lat - place_lat) ** 2 + (lng - place_lng) ** 2)
    for r in place_search["results"]:
        lat = r["geometry"]["location"]["lat"]
        lng = r["geometry"]["location"]["lng"]
        if np.sqrt((lat - place_lat) ** 2 + (lng - place_lng) ** 2) < dist:
            info = r

    pprint(info)

    try:
        name = f"L'utilisateur est interessé par l'endroit qui s'appelle \"{info['name']}\"."
        name_for_user = f"\"{info['name']}\""
    except KeyError:
        warn("couldn't read location name")
        name = "Le nom de l'endroit est inconnu."
        name_for_user = ""

    try:
        openness = "L'endroit est actuellement ouvert." if info["opening_hours"]["open_now"] else "L'endroit est actuellement fermé."
    except KeyError:
        openness = ''

    try:
        rating = f"L'endroit est noté {info['rating']} sur 5 sur google."
    except KeyError:
        rating = ''

    try:
        types = "L'endroit porte les codes de location " + '\"'+'", "'.join(info["types"])+'\".'
    except KeyError:
        warn("couldn't read location types")
        types = ''

    try:
        vicinity = f"L'endroit se trouve à proximité de {info['vicinity']}."
    except KeyError:
        warn("couldn't read location vicinity")
        vicinity = ''

    message_s = f"{name} {types} {openness} {rating} {vicinity}"
    message_u = f"Décrit l'endroit {name_for_user}"

    return message_s, message_u



def get_description(place_lat, place_lng):
    return get_input_prompt_for_location(place_lat, place_lng)

if __name__ == "__main__":
    # m = get_input_prompt_for_location(45.641010300357344, 5.869864225387573)
    # print(m)
    # m = get_input_prompt_for_location(45.64247299277823, 5.871087312698364)
    # print(m)
    # m = get_input_prompt_for_location(45.64574328486849, 5.866785049438477)
    # print(m)
    # m = get_input_prompt_for_location(45.638564893384796, 5.870883464813232)
    # print(m)
    m_u, m_a = get_input_prompt_for_location(45.6401026617584, 5.871065855026245)
    print(m_u, "\n", m_a)
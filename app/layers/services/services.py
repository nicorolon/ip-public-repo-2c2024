# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from ..transport.transport import getAllImages as transport_getAllImages
from ..utilities.card import Card

def getAllImages(input=None):
    # obtiene un listado de datos "crudos" desde la API, usando a transport.py.
    json_collection = transport_getAllImages(input)

    # recorre cada dato crudo de la colección anterior, lo convierte en una Card y lo agrega a images.
    images = []
    for imagenesCrudas in json_collection:
        card = Card(
            url=imagenesCrudas['image'], #IMAGEN DEL PERSONAJE
            nombrePersonaje=imagenesCrudas.get('title', 'Sin título'), #NOMBRE DEL PERSONAJE
            estado=imagenesCrudas.get('status', 'Desconocido'), #ESTADO DEL PERSONAJE
            ultimaLocalizacion=imagenesCrudas.get('last_location', 'Desconocido'), #ULT LOCALIZACIÓN DEL PERSONAJE
            episodio=imagenesCrudas.get('first_seen', 'Fecha no especificada') #EPISODIO DEL PERSONAJE
        )
        images.append(card)
    return images

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request del template en una Card.
    fav.user = '' # le asignamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # transformamos cada favorito en una Card, y lo almacenamos en card.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.
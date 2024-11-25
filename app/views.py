# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from .layers.persistence import repositories
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    images =services.getAllImages()

    favourite_list =  repositories.getAllFavourites(request.user)

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

def search(request):
    search_msg = request.POST.get('query', '').strip()  #Acá elimino los espacios que pueden dificultar la comparación

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):
        images =services.getAllImages(search_msg)
        
        favourite_list =  favourite_list = repositories.getAllFavourites(request.user)
        
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = repositories.getAllFavourites(request.user)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    services.saveFavourite(request)
    return redirect('favoritos')

@login_required
def deleteFavourite(request):
    services.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def exit(request):
    # Cerrar la sesión
    logout(request)

    # Redirigir al usuario a la página de inicio de sesión
    return redirect('login')
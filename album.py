from .models import PhotoAlbum

def show_albums():
    albums = PhotoAlbum.objects.filter(album=True)
    return {'albums': albums}

def show_photos(one_album):
    try:
        one_album = PhotoAlbum.objects.get(pk=one_album, album=True)
    except:
        return show_albums()
    return {'album': one_album}

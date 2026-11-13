from django.conf import settings
# MODIF : ajout de "messages" pour afficher le message d'erreur rouge dans l'admin
from django.contrib import admin, messages
# MODIF : HttpResponse sert à renvoyer le texte du robots.txt
from django.http import HttpResponse
# MODIF : "redirect" sert à renvoyer la personne vers la liste des envois
from django.shortcuts import redirect
from django.urls import include, path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap  # import de l'outil pour sitemap
# MODIF : on importe la vue de Wagtail qui gère la suppression des envois,
# pour pouvoir la copier et lui ajouter notre règle
from wagtail.contrib.forms.views import DeleteSubmissionsView

from search import views as search_views


# MODIF : toute cette classe est nouvelle.
# Elle reprend la vue de suppression de Wagtail et ajoute une vérification avant.
class RestrictedDeleteSubmissionsView(DeleteSubmissionsView):
    """Seuls les superusers et le groupe 'Superadmin'
    peuvent supprimer des envois de formulaire"""

    # dispatch() est appelée à chaque fois que quelqu'un ouvre cette page
    def dispatch(self, request, *args, **kwargs):
        # On regarde si la personne est superuser OU dans le groupe autorisé.
        # Le nom du groupe doit être identique à celui créé dans Wagtail.
        autorise = request.user.is_superuser or request.user.groups.filter(
            name="Superadmin"
        ).exists()

        # Si elle n'a pas le droit : message d'erreur + retour à la liste des envois,
        # et rien n'est supprimé
        if not autorise:
            messages.error(
                request,
                # Tu peux changer ce texte comme tu veux
                "Vous n'avez pas le droit de supprimer ces messages.",
            )
            return redirect("wagtailforms:list_submissions", page_id=kwargs["page_id"])

        # Si elle a le droit : on laisse Wagtail faire la suppression normalement
        return super().dispatch(request, *args, **kwargs)


# MODIF : nouvelle fonction pour le SEO.
# Les robots des moteurs de recherche lisent /robots.txt avant d'explorer le site :
# il leur dit ce qu'ils peuvent explorer et où trouver le sitemap.
def robots_txt(request):
    content = (
        "User-agent: *\n"  # s'adresse à tous les robots
        "Allow: /\n"  # ils peuvent explorer tout le site...
        "Disallow: /admin/\n"  # ...sauf l'admin de Wagtail, inutile dans Google
        "Disallow: /django-admin/\n"  # ...et l'admin de Django
        # adresse complète du sitemap (le domaine change seul une fois en ligne)
        "Sitemap: " + request.build_absolute_uri("/sitemap.xml") + "\n"
    )
    return HttpResponse(content, content_type="text/plain")


urlpatterns = [
    path("django-admin/", admin.site.urls),
    # MODIF : nouvelle ligne. Elle intercepte l'adresse de suppression des envois
    # et utilise notre vue à la place de celle de Wagtail.
    # Elle doit être AVANT "admin/", sinon Wagtail passe en premier
    # et notre règle ne s'applique jamais.
    path(
        "admin/forms/submissions/<int:page_id>/delete/",
        RestrictedDeleteSubmissionsView.as_view(),
    ),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("sitemap.xml", sitemap),  # déclaration du path sitemap
    path("robots.txt", robots_txt),  # MODIF : fichier pour les robots des moteurs de recherche
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
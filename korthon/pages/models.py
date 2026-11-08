from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

@register_setting  # ajoute une entrée "Réglages" dans l'admin, un seul formulaire par site
class ReglagesSite(BaseSiteSetting):
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Logo du site affiché dans le header et le footer",
    )
    lien_invitation = models.URLField(blank=True, help_text="Lien d'invitation du bot Discord")  # bouton <<Ajouter à mon serveur>>
    lien_support = models.URLField(blank=True, help_text="Lien d'invitation du serveur Discord de support")  # lien << Discord de support>>
    copyright = models.CharField(max_length=100, default="© 2026 Korthon. Tous droits réservés.", help_text="Texte de copyright affiché dans le footer du site")
    page_mentions_legales = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Page des mentions légales",
    )

    panels = [
        FieldPanel("logo"),
        FieldPanel("lien_invitation"),
        FieldPanel("lien_support"),
        FieldPanel("copyright"),
        FieldPanel("page_mentions_legales"),
    ]
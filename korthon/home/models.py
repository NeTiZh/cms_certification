from django.db import models
from modelcluster.fields import ParentalKey  # relie les blocs à la page, enregistrés ensemble
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable, Page


# Un bloc de l'accueil : un texte d'accroche et une capture du bot.
# Orderable : Dylan peut changer l'ordre des blocs dans l'admin.
class BlocAccroche(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="blocs_accroche")
    accroche = models.CharField(max_length=150, help_text="Phrase courte qui donne envie d'ajouter le bot")
    capture = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.PROTECT,
        related_name="+",
        help_text="Capture du bot sur Discord",
    )

    panels = [
        FieldPanel("accroche"),
        FieldPanel("capture"),
    ]


class HomePage(Page):
    page_decouvrir = models.ForeignKey(
        "wagtailcore.page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Page vers laquelle mène le bouton « Découvrir Korthon »",
    )
    
    content_panels = Page.content_panels + [
        InlinePanel("blocs_accroche", min_num=1, label="Blocs d'accroche"),
        FieldPanel("page_decouvrir"),
    ]
    
    max_count = 1  # une seule page Accueil
    
    class Meta:
        verbose_name = "Accueil"
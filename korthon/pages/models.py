from django.db import models
from modelcluster.fields import ParentalKey  # lien page -> champs, édités ensemble (formulaire de contact)
from wagtail.admin.panels import FieldPanel, InlinePanel  # InlinePanel : liste de champs avec un bouton "Ajouter"
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField  # page avec formulaire / un champ du formulaire
from wagtail.contrib.forms.panels import FormSubmissionsPanel  # lien vers les messages reçus, dans l'admin
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page

@register_setting  # ajoute une entrée "Réglages" dans l'admin, un seul formulaire par site
class SiteSettings(BaseSiteSetting):
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Logo du site affiché dans le header",
    )
    invite_link = models.URLField(blank=True, help_text="Lien d'invitation du bot Discord")  # bouton <<Ajouter à mon serveur>>
    support_link = models.URLField(blank=True, help_text="Lien d'invitation du serveur Discord de support")  # lien << Discord de support>>
    copyright = models.CharField(max_length=100, default="© 2026 Korthon", help_text="Texte de copyright affiché dans le footer du site")
    legal_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Page des mentions légales",
    )

    panels = [
        FieldPanel("logo"),
        FieldPanel("invite_link"),
        FieldPanel("support_link"),
        FieldPanel("copyright"),
        FieldPanel("legal_page"),
    ]
# Page mention légales
class LegalNoticePage(Page):
    content = RichTextField(help_text="Editeur, hébergement, données personnelles, cookies, etc.")

    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]

    max_count = 1  # limite le nombre de pages de ce type à 1
    parent_page_types = ["home.HomePage"]  # limite la page parente à HomePage
    subpage_types = []  # interdit la création de sous-pages

    class Meta:
        verbose_name = "Mentions légales"

# Page Contact
# Les champs du formulaire ne sont pas écrits dans le code : ils sont créés dans l'admin
# (nom, e-mail, sujet, message). Chaque envoi est enregistré dans l'admin, sans e-mail.


# Un champ du formulaire (ex. : "E-mail", obligatoire, de type e-mail).
# AbstractFormField fournit déjà le libellé, le type, "obligatoire", les choix et la valeur par défaut.
class FormField(AbstractFormField):
    # ParentalKey plutôt que ForeignKey : la page et ses champs sont enregistrés ensemble,
    # ce qui permet de les modifier en brouillon avant de publier.
    # related_name="form_fields" est imposé : Wagtail cherche les champs sous ce nom.
    page = ParentalKey("ContactPage", on_delete=models.CASCADE, related_name="form_fields")


# AbstractForm : page qui affiche un formulaire et enregistre les réponses.
# AbstractEmailForm enverrait aussi un e-mail, ce que le cahier des charges exclut.
class ContactPage(AbstractForm):
    intro = RichTextField(blank=True, help_text="Explication affichée au-dessus du formulaire de contact")
    privacy_notice = RichTextField(blank=True, help_text="Texte de confidentialité affiché au-dessus du bouton d'envoi du formulaire")
    submit_label = models.CharField(max_length=50, default="Envoyer", help_text="Texte du bouton d'envoi du formulaire")
    thank_you_text = RichTextField(blank=True, help_text="Texte affiché après l'envoi du formulaire")

    # Ordre des blocs dans l'admin, de haut en bas
    content_panels = AbstractForm.content_panels + [
        FormSubmissionsPanel(),  # nombre de messages reçus, avec un lien pour les lire
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Champs du formulaire"),  # liste des champs avec un bouton "Ajouter"
        FieldPanel("privacy_notice"),
        FieldPanel("submit_label"),
        FieldPanel("thank_you_text"),
    ]

    max_count = 1  # une seule page Contact
    parent_page_types = ["home.HomePage"]  # toujours sous l'accueil
    subpage_types = []  # pas de sous-page

    class Meta:
        verbose_name = "Contact"

class DiscoverPage(Page):
    intro = RichTextField(blank=True, help_text="Présentation du bot, en quelques phrases")
    documentation_page = models.ForeignKey(
        "wagtailcore.page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Page vers laquelle mène le bouton « Voir les commandes »",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("documentation_page"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Les catégories publiées dont la case « Afficher sur la page Découvrir » est cochée
        context["categories"] = CategoryPage.objects.live().filter(show_on_discover=True)
        return context

    max_count = 1  # une seule page Découvrir
    parent_page_types = ["home.HomePage"]  # toujours sous l'accueil
    subpage_types = []  # pas de sous-page

    class Meta:
        verbose_name = "Découvrir"


# Une commande du bot, rattachée à sa catégorie.
# Orderable : on choisit l'ordre d'affichage des commandes dans l'admin.
class Command(Orderable):
    page = ParentalKey("CategoryPage", on_delete=models.CASCADE, related_name="commands")
    name = models.CharField(max_length=50, help_text="Nom de la commande")
    description = models.TextField(help_text="description de la commande")
    usage = models.CharField(max_length=100, help_text="Usage de la commande ex: /ban <member> <reason>")
    permission = models.CharField(max_length=50, help_text="ex: Administrateur, etc..", blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("usage"),
        FieldPanel("permission"),
    ]

class DocumentationPage(Page):
    intro = RichTextField(blank=True, help_text="Présentation des commandes, en quelques phrases")
    parent_page_types = ["home.HomePage"]
    subpage_types = ["pages.CategoryPage"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    class Meta:
        verbose_name = "Documentation"

# Une catégorie de commandes (Général, Modération, etc..)
class CategoryPage(Page):
    intro = RichTextField(blank=True, help_text="Présentation de la catégorie, affichée aussi sur la page Découvrir")
    screenshot = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Capture affichée dans le bloc de la catégorie sur la page Découvrir",
    )
    show_on_discover = models.BooleanField(default=False, help_text="Afficher cette catégorie sur la page Découvrir")

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("screenshot"),
        FieldPanel("show_on_discover"),
        InlinePanel("commands", label="Commandes"),
    ]

    parent_page_types = ["pages.DocumentationPage"] # toujours sous la Documentation
    subpage_types = [] # pas de sous-page

    class Meta:
        verbose_name = "Catégorie"
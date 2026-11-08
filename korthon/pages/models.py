from django.db import models
from modelcluster.fields import ParentalKey  # lien page -> champs, édités ensemble (formulaire de contact)
from wagtail.admin.panels import FieldPanel, InlinePanel  # InlinePanel : liste de champs avec un bouton "Ajouter"
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField  # page avec formulaire / un champ du formulaire
from wagtail.contrib.forms.panels import FormSubmissionsPanel  # lien vers les messages reçus, dans l'admin
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.models import Page

@register_setting  # ajoute une entrée "Réglages" dans l'admin, un seul formulaire par site
class ReglagesSite(BaseSiteSetting):
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Logo du site affiché dans le header",
    )
    lien_invitation = models.URLField(blank=True, help_text="Lien d'invitation du bot Discord")  # bouton <<Ajouter à mon serveur>>
    lien_support = models.URLField(blank=True, help_text="Lien d'invitation du serveur Discord de support")  # lien << Discord de support>>
    copyright = models.CharField(max_length=100, default="© 2026 Korthon", help_text="Texte de copyright affiché dans le footer du site")
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
# Page mention légales
class MentionsLegalesPage(Page):
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
class ChampFormulaire(AbstractFormField):
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
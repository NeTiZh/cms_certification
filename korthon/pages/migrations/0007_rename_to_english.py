# Renommage des modèles et des champs en anglais.
# RenameModel et RenameField gardent les données : seuls les noms changent en base.
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0006_decouvrirpage"),
    ]

    operations = [
        migrations.RenameModel("ReglagesSite", "SiteSettings"),
        migrations.RenameField("SiteSettings", "lien_invitation", "invite_link"),
        migrations.RenameField("SiteSettings", "lien_support", "support_link"),
        migrations.RenameField("SiteSettings", "page_mentions_legales", "legal_page"),
        migrations.RenameModel("MentionsLegalesPage", "LegalNoticePage"),
        migrations.RenameModel("ChampFormulaire", "FormField"),
        migrations.RenameModel("DecouvrirPage", "DiscoverPage"),
        migrations.RenameField("DiscoverPage", "page_documentation", "documentation_page"),
    ]

# Renommage des modèles et des champs de l'accueil en anglais.
# RenameModel et RenameField gardent les données : seuls les noms changent en base.
import django.db.models.deletion
import modelcluster.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_alter_homepage_options_homepage_page_decouvrir_and_more"),
    ]

    operations = [
        migrations.RenameModel("BlocAccroche", "TaglineBlock"),
        migrations.RenameField("TaglineBlock", "accroche", "tagline"),
        migrations.RenameField("TaglineBlock", "capture", "screenshot"),
        migrations.AlterField(
            model_name="taglineblock",
            name="page",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tagline_blocks",
                to="home.homepage",
            ),
        ),
        migrations.RenameField("HomePage", "page_decouvrir", "discover_page"),
    ]

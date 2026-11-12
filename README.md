# Korthon — site de présentation et documentation du bot

Site vitrine du bot Discord **Korthon** : présentation du bot, documentation de ses 33 commandes, formulaire de contact et mentions légales. Réalisé avec **Wagtail** dans le cadre de la certification Simplon.

## Prérequis

- Python 3.13
- Git

## Installation

```bash
# 1. Récupérer le projet
git clone https://github.com/NeTiZh/cms_certification.git
cd cms_certification

# 2. Créer et activer l'environnement virtuel
python3 -m venv env
source env/bin/activate          # Windows : env\Scripts\activate

# 3. Installer les dépendances
pip install -r korthon/requirements.txt

# 4. Créer les tables de la base de données
cd korthon
python manage.py migrate

# 5. Créer le compte administrateur
python manage.py createsuperuser

# 6. Lancer le site
python manage.py runserver
```

Le site est alors visible sur http://127.0.0.1:8000 et l'administration sur http://127.0.0.1:8000/admin.

## Créer le contenu du site

La base de données n'est pas dans le dépôt : l'étape 4 (`migrate`) en crée une nouvelle, vide, dans `korthon/db.sqlite3`. Le contenu se crée ensuite dans l'administration (http://127.0.0.1:8000/admin), avec le compte de l'étape 5.

1. **Paramètres → Site settings** : logo, lien d'invitation du bot, lien du Discord de support, copyright.
2. **Pages** : sous la page d'accueil, créer les pages dans cet ordre :
   - **Découvrir**, **Documentation**, **Contact** et **Mentions légales**, de type du même nom ;
   - sous **Documentation**, les 5 pages **Catégorie** (Général, Modération, Communauté, Support, Fun), chacune avec ses commandes. Cocher « Afficher sur la page Découvrir » pour celles à montrer sur Découvrir.
3. **Page d'accueil** : modifier son titre, ajouter les 3 blocs d'accroche (texte et illustration) et choisir la page Découvrir pour le bouton.
4. **Page Contact** : ajouter les champs du formulaire (Nom ou pseudo, E-mail, Sujet en liste déroulante, Message).
5. **Paramètres → Site settings** : choisir la page Mentions légales pour le lien du pied de page.

Les images utilisées sur le site sont dans le dossier `korthon/media/`.

## Arborescence des pages

- Accueil
  - Découvrir
  - Documentation
    - Général, Modération, Communauté, Support, Fun (33 commandes)
  - Contact
  - Mentions légales et politique de confidentialité

## Extensions Wagtail utilisées

| Extension | Usage |
|---|---|
| `wagtail.contrib.forms` | Formulaire de contact administrable, messages lus dans l'admin |
| `wagtail.images` | Illustrations de l'accueil, captures de Découvrir et logo (SVG accepté) |
| `wagtail.contrib.settings` | Logo, liens Discord, copyright et lien des mentions légales, modifiables à un seul endroit |
| `wagtail.contrib.sitemaps` | Plan du site pour Google, sur `/sitemap.xml` |

## Utilisateurs et droits

| Rôle | Pour qui | Droits |
|---|---|---|
| Administrateur | Dylan, le client | Tous les droits (superutilisateur) : publier, régler le site, gérer les comptes |
| Support | Les personnes du support | Lire les messages du formulaire de contact, sans pouvoir publier ni modifier les réglages |

Pour recréer le groupe Support dans une base neuve : **Paramètres → Groupes → Ajouter un groupe**, cocher « Peut accéder à l'administration de Wagtail », puis dans les permissions de pages, donner « Modifier » sur la page Contact uniquement.

## Données personnelles (RGPD)

Le formulaire collecte le nom ou pseudo, l'e-mail, le sujet et le message, uniquement pour répondre au visiteur. Les messages sont conservés 1 an. Le détail est sur la page « Mentions légales et politique de confidentialité ».

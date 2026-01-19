from otree.api import *


doc = """
Étude sur la rareté (Sociale vs Quantitative) pour le concert de Joules.
"""

class Constants(BaseConstants):
    name_in_url = 'concert_joules'
    players_per_group = None
    num_rounds = 1
    prix_billet = 80

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # --- Variable Système ---
    condition = models.StringField()
    nombre_clics = models.IntegerField(initial=0) # Plus besoin de la sous-classe !

    # --- Données Socio-démographiques ---
    age = models.IntegerField(label="Quel est votre âge ?", min=18, max=99)
    genre = models.StringField(
        label="Quel est votre genre ?",
        choices=['Femme', 'Homme', 'Non-binaire', 'Préfère ne pas répondre'],
        widget=widgets.RadioSelect
    )

    # --- Consentement ---
    consentement = models.BooleanField(
        label="En cochant cette case, j'accepte de participer à cette étude.",
        widget=widgets.CheckboxInput
    )

    # --- Variables de l'expérience ---
    achat = models.BooleanField(
        label="Souhaitez-vous acheter un billet pour ce concert ?",
        choices=[
            [True, "Oui, j'achète ce billet"],
            [False, "Non, je n'achète pas de billet"]
        ],
        widget=widgets.RadioSelect
    )
    offre_enchere = models.CurrencyField(
        label="Quel est le prix maximum que vous seriez prêt à payer pour ce billet ?",
        min=0, max=200
    )

# --- FONCTIONS ---

def creating_session(subsession):
    import itertools
    # Crée un cycle infini des conditions pour les répartir équitablement
    conditions = itertools.cycle(['control', 'social', 'quantitatif'])
    for p in subsession.get_players():
        p.condition = next(conditions)

# 4. CLASSES DE PAGES (Définissez les classes ici !)
class Introduction(Page):
    form_model = 'player'
    form_fields = ['age', 'genre']

class Consentement(Page):
    form_model = 'player'
    form_fields = ['consentement']

# --- PAGES ---
class VenteBillet(Page):
    form_model = 'player'
    form_fields = ['achat']  # On utilise maintenant le champ binaire

    @staticmethod
    def vars_for_template(player: Player):
        # La logique des messages reste la même
        messages = {
            'control': "Billets disponibles pour le concert de Joules.",
            'social': "Succès massif : Déjà 1 250 personnes ont acheté leur billet ! De plus, 42 personnes consultent actuellement cette page.",
            'quantitatif': "Attention : Offre limitée ! Il ne reste plus que 8 billets disponibles en ligne.",
        }
        styles = {
            'control': 'secondary',
            'social': 'success',
            'quantitatif': 'danger'
        }

        return {
            'instruction': messages.get(player.condition),
            'alerte_style': styles.get(player.condition),
            'prix': Constants.prix_billet,
        }
class Enchere(Page):
    form_model = 'player'
    form_fields = ['offre_enchere', 'nombre_clics']



    @staticmethod
    def vars_for_template(player: Player):
        return {
            'prix_depart': Constants.prix_billet
        }

class Merci(Page):
    pass
#Page de conclusion pour remercier les participants et leur dire que s'ils ont des questions ils peuvent nous contacter.

page_sequence = [
    Introduction,
    Consentement,
    VenteBillet,
    Enchere,
    Merci
]

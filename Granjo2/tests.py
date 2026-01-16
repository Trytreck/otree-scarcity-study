from otree.api import Currency as c, currency_range, expect
from . import *
import random

class PlayerBot(Bot):
    def play_round(self):
        # 1. Page Introduction
        yield Introduction, {
            'age': random.randint(18, 70),
            'genre': random.choice(['Femme', 'Homme', 'Autre'])
        }

        # 2. Page Consentement
        yield Consentement, {
            'consentement': True
        }

        # 3. Page VenteBillet (Choix d'achat aléatoire)
        choix_achat = random.choice([True, False])
        yield VenteBillet, {
            'achat': choix_achat
        }

        # 4. Page Enchere (Uniquement si achat est True)
        if choix_achat:
            yield Enchere, {
                'offre_enchere': random.randint(40, 150)
            }

        # 5. Page Merci (Pas de champs à remplir)
        yield Submission(Merci, check_html=False)

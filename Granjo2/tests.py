from otree.api import Currency as c, currency_range, expect
from . import *
import random

class PlayerBot(Bot):
    def play_round(self):
        # 1. Page Introduction
        yield Introduction, {
            'age': random.randint(18, 50),
            'genre': random.choice(['Femme', 'Homme'])
        }

        # 2. Page Consentement
        yield Consentement, {'consentement': True}

        # 3. Préparation des données selon la condition
        if self.player.condition == 'quantitatif':
            p_achat, clics, o_min, o_max = 0.9, random.randint(20, 40), 100, 160
        elif self.player.condition == 'social':
            p_achat, clics, o_min, o_max = 0.7, random.randint(10, 25), 85, 130
        else: # control
            p_achat, clics, o_min, o_max = 0.4, random.randint(2, 10), 60, 95

        # 4. Page VenteBillet
        decision_achat = random.random() < p_achat
        yield VenteBillet, {'achat': decision_achat}

        # 5. Page Enchère (Tout le monde la joue)
        if decision_achat:
            offre = random.randint(o_min, o_max)
        else:
            offre = random.randint(10, 79) # Prix bas car refus d'achat à 80

        yield Enchere, {
            'offre_enchere': c(offre),
            'nombre_clics': clics
        }

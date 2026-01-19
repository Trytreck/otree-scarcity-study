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

        # 3. Définition des variables selon la condition
        # (on prépare les chiffres pour la suite)
        if self.player.condition == 'social':
            p_achat, clics, o_min, o_max = 0.9, random.randint(20, 40), 100, 160
        elif self.player.condition == 'quantitatif':
            p_achat, clics, o_min, o_max = 0.7, random.randint(10, 25), 85, 130
        else: # condition 'control'
            p_achat, clics, o_min, o_max = 0.4, random.randint(2, 10), 60, 95

        # 4. Page VenteBillet
        decision_achat = random.random() < p_achat
        yield VenteBillet, {'achat': decision_achat}

        # 5. Page Enchère (Jouée par TOUT LE MONDE)
        if decision_achat:
            # Si le bot a acheté (achat=True), il met un prix élevé
            offre = random.randint(o_min, o_max)
        else:
            # Si le bot a dit non (achat=False), il met un prix bas (< 80)
            offre = random.randint(10, 79)

        yield Enchere, {
            'offre_enchere': c(offre),
            'nombre_clics': clics
        }

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class WybierzKostke(FlaskForm):
    """wybor kostki """

    kostka = StringField("Kostka")
    potwierdz = SubmitField("Potwierdź wybór")


class ImionaGraczy(FlaskForm):
    """nadanie imion gracza"""
    gracz_1 = StringField("Kostka")
    gracz_2 = StringField("Kostka")
    potwierdz = SubmitField("Rozpocznij grę")
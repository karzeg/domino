from flask import Flask, render_template, redirect, url_for, flash
from game import *
from form import *

app = Flask(__name__)
app.secret_key = 'asdfasdfasdfaskjdlhflwgejnlhus'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/formularz', methods=['POST', 'GET'])
def wypelnij_formularz():
    global gra, gracz_1, gracz_2

    form_gracze = ImionaGraczy()

    if form_gracze.validate_on_submit() and form_gracze.potwierdz.data:
        gracz_1 = form_gracze.gracz_1.data
        gracz_2 = form_gracze.gracz_2.data

        gra = Game(gracz_1=gracz_1, gracz_2=gracz_2)

        return redirect(url_for('gra'))

    return render_template('formularz.html', form_gracze=form_gracze)


@app.route('/gra', methods=['POST', 'GET'])
def gra():
    global gra, gracz_1, gracz_2, na_stole

    form = WybierzKostke()

    if form.validate_on_submit():
        gra.start(form.kostka.data)

        if gra.koniec:
            return render_template("koniec.html", przegrany=gra.turn)
        return redirect(url_for('gra'))

    return render_template('game.html', gra=gra, ilosc_na_stosie=len(gra.domino),
                           ilosc_reka=len(gra.gracze[gra.turn].domino_gracza))


@app.route('/wyloz_kostke/<kostka>')
def wyloz_kostke(kostka):
    global gra

    if kostka not in gra.gracze[gra.turn].domino_gracza:
        flash('Brak pasujacej')

    try:
        gra.ruch_gracza(gra.gracze[gra.turn].domino_gracza[int(kostka)])
        gra.czy_zakonczyc_gre()

        if gra.koniec:
            return redirect(url_for('koniec'))

        gra.zmiana_gracza()

    except AssertionError as e:
        return redirect(url_for('dobierz_kostke'))

    return redirect(url_for('gra'))


@app.route('/dobierz_kostke')
def dobierz_kostke():
    global gra
    gra.ruch_gracza()
    gra.zmiana_gracza()

    return redirect(url_for('gra'))


@app.route('/koniec_gry')
def koniec():
    global gra

    # if len(gra.gracze[gra.turn].domino_gracza) < len(gra.gracze[(gra.turn + 1) % 2].domino_gracza):

    if len(gra.gracze[gra.turn].domino_gracza) < len(gra.gracze[(gra.turn + 1) % 2].domino_gracza):
        wygrany = gra.imiona[gra.turn]
        wygrany_pkt = len(gra.gracze[gra.turn].domino_gracza)
        przegrany = gra.imiona[(gra.turn + 1) % 2]
        przegrany_pkt = len(gra.gracze[(gra.turn + 1) % 2].domino_gracza)

    else:
        wygrany = gra.imiona[(gra.turn + 1) % 2]
        wygrany_pkt = len(gra.gracze[(gra.turn + 1) % 2].domino_gracza)
        przegrany = gra.imiona[gra.turn]
        przegrany_pkt = len(gra.gracze[gra.turn].domino_gracza)

    koniec_gry = gra.koniec

    return render_template('koniec.html', wygrany=wygrany[0], przegrany=przegrany[0], koniec_gry=koniec_gry,
                           wygrany_pkt=wygrany_pkt, przegrany_pkt=przegrany_pkt)


if __name__ == "__main__":
    app.run(debug=True)

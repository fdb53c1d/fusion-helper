from . import dbutil
from flask import Blueprint, render_template, aborts


bp = Blueprint('views', __name__)


@bp.route('/', methods=['GET'])
def index():
    db = dbutil.get_db()
    cursor = db.cursor()

    cursor.execute('SELECT Id, Name, Description, Attack, Defense, Type FROM cards')
    cards = cursor.fetchall()

    cursor.execute('SELECT Id, Type FROM types')
    card_types = cursor.fetchall()

    if not cards or not card_types:
        abort(404)

    return render_template('index.html', cards=cards, types=card_types)


@bp.route('/card/<int(min=1, max=722):card_id>/', methods=['GET'])
def card_page(card_id):
    db = dbutil.get_db()
    cursor = db.cursor()

    cursor.execute("""SELECT Id, Name, Description, GuardianStarA, GuardianStarB,
                      Type, Attack, Defense FROM cards WHERE Id = ?""", (card_id,))
    card = cursor.fetchone()

    cursor.execute('SELECT Id, Type FROM types')
    card_types = cursor.fetchall()

    cursor.execute('SELECT Id, Star FROM stars')
    star_names = cursor.fetchall()

    if not card or not card_types or not star_names:
        abort(404)

    return render_template('card.html', card=card, types=card_types, stars=star_names)


@bp.route('/calc/', methods=['GET'])
def fusion_calc():
    db = dbutil.get_db()
    cursor = db.cursor()

    cursor.execute('SELECT Id, Name, Attack, Defense, Type FROM cards')
    cards = cursor.fetchall()

    cursor.execute('SELECT ID, Type FROM Types')
    card_types = cursor.fetchall()

    if not cards or not card_types:
        abort(404)

    return render_template('calc.html', cards=cards, types=card_types, teste=True)

from . import dbutil
from flask import abort, Blueprint, jsonify
from werkzeug.wrappers import Response


bp = Blueprint('api', __name__)


@bp.route('/api/cardinfo/<int(min=1, max=722):card_id>/', methods=['GET'])
def get_card_info(card_id):
    db = dbutil.get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM cards WHERE Id = ?', (card_id,))
    data = cursor.fetchone()
    if data is not None:
        return jsonify(dict(data))

    return jsonify({})


@bp.route('/api/cardinfo/all/', methods=['GET'])
def get_all_cards():
    db = dbutil.get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM cards')
    data = cursor.fetchall()
    if len(data) > 0:
        return jsonify([dict(row) for row in data])

    return jsonify({})


@bp.route('/api/cardinfo/<int:id_from>-<int:id_to>/', methods=['GET'])
def get_card_range(id_from, id_to):
    db = dbutil.get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM cards WHERE Id BETWEEN ? AND ?', (id_from, id_to))
    data = cursor.fetchall()
    if len(data) > 0:
        return jsonify([dict(row) for row in data])

    return jsonify({})


@bp.route('/api/fusion/<int:card_id>/', methods=['GET'])
def get_card_fusions(card_id):
    db = dbutil.get_db()
    cursor = db.cursor()

    cursor.execute('SELECT Card1, Card2, Result FROM fusions WHERE Card1 = ? OR Card2 = ?', (card_id, card_id))
    fusion_to = [dict(row) for row in cursor.fetchall()]

    cursor.execute('SELECT Card1, Card2, Result FROM fusions WHERE Result = ?', (card_id,))
    fusion_from = [dict(row) for row in cursor.fetchall()]

    result = {'from': fusion_from, 'to': fusion_to}

    return jsonify(result)


@bp.route('/api/fusion/<int:card1>+<int:card2>/')
def get_fusion(card1, card2):
    db = dbutil.get_db()
    cursor = db.cursor()

    cursor.execute('SELECT Result FROM fusions WHERE Card1 = ? AND Card2 = ?', (min(card1, card2), max(card1, card2)))
    result = cursor.fetchone()

    if result is not None:
        return Response(str(result['Result']), mimetype='text/plain')

    return Response('', mimetype='text/plain')


@bp.route('/api/fusions/<int_list:id_list>/')
def get_hand_fusions(id_list):
    if len(id_list) < 2:
        abort(404)

    db = dbutil.get_db()
    cursor = db.cursor()

    fusion_list = []

    back(id_list, set(), fusion_list, cursor)

    return jsonify(fusion_list)


# Backtracking function to retrieve all possible fusions from a list of cards
def back(card_list, visited, fusion_list, cursor, depth=0, until=None, last=0):
    # keep it from persisting across calls
    if until is None:
        until = []

    # stop recursion at maximum depth
    if depth == len(card_list):
        return

    for i in range(len(card_list)):
        # prevent repeating cards more than necessary
        if until.count(card_list[i]) == card_list.count(card_list[i]):
            continue

        until.append(card_list[i])

        current = None
        if len(until) == 2:
            current = (frozenset(until[:2]), tuple())
        elif len(until) > 2:
            current = (frozenset(until[:2]), tuple(until[2:]))

        # check if current sequence was already visited
        # if not, add it to visited set
        if current is not None:
            if current in visited:
                until = until[:-1]
                continue
            visited.add(current)

        if len(until) == 1:
            next_card = until[0]
        else:
            cursor.execute('SELECT Result FROM fusions WHERE Card1 = ? AND Card2 = ?',
                           (min(last, until[-1]), max(last, until[-1])))
            result = cursor.fetchone()
            if result is not None:
                fusion = {}
                for idx, x in enumerate(until):
                    fusion['Card' + str(idx+1)] = x
                fusion['Result'] = result['Result']
                fusion_list.append(fusion)
                next_card = result['Result']
            else:
                until = until[:-1]
                continue

        back(card_list, visited, fusion_list, cursor, depth=depth+1, until=until[:], last=next_card)

        # discard last element after recursion
        until = until[:-1]

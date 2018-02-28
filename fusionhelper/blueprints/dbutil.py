from flask import Blueprint, current_app, g
import json
import sqlite3


bp = Blueprint('dbutil', __name__)


def initdb():
    print('Creating tables...')
    create_tables()
    print('Done.')
    print('Populating cards table...')
    init_cards()
    print('Done.')
    print('Populating equips table...')
    init_equips()
    print('Done.')
    print('Populating rituals table...')
    init_rituals()
    print('Done.')
    print('Populating fusions table...')
    init_fusions()
    print('Done.')
    print('Populating stars table...')
    init_stars()
    print('Done.')
    print('Populating types table...')
    init_types()
    print('Done.')


def get_db():
    if not (hasattr(g, 'sqlite_db')):
        db = sqlite3.connect(current_app.config['DATABASE'])
        db.row_factory = sqlite3.Row
        g.sqlite_db = db

    return g.sqlite_db


def create_tables():
    db = get_db()
    cursor = db.cursor()

    with current_app.open_resource('database/schema.sql', mode='r') as f:
        cursor.executescript(f.read())

    db.commit()


def init_cards():
    db = get_db()
    cursor = db.cursor()
    cards = json.loads(current_app.open_resource('database/Cards.json').read().decode('utf-8'))

    for card in cards:
        cursor.execute("""INSERT INTO cards (Id, Name, Description, GuardianStarA, GuardianStarB,
                                              Level, Type, Attack, Defense, Stars, CardCode, Attribute)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (card['Id'], card['Name'], card['Description'], card['GuardianStarA'], card['GuardianStarB'],
                        card['Level'], card['Type'], card['Attack'], card['Defense'], card['Stars'], card['CardCode'],
                        card['Attribute']))

    db.commit()


def init_equips():
    db = get_db()
    cursor = db.cursor()
    cards = json.loads(current_app.open_resource('database/Cards.json').read().decode('utf-8'))

    for card in cards:
        if card['Equip'] is not None:
            for equip in card['Equip']:
                cursor.execute('INSERT INTO equips (Equip_id, Equipped_id) VALUES (?, ?)', (card['Id'], equip))

    db.commit()


def init_rituals():
    db = get_db()
    cursor = db.cursor()
    cards = json.loads(current_app.open_resource('database/Cards.json').read().decode('utf-8'))

    for card in cards:
        if card['Ritual'] is not None:
            ritual = card['Ritual']
            cursor.execute('INSERT INTO rituals (Ritual_id, Card1, Card2, Card3, Result) VALUES (?, ?, ?, ?, ?)',
                           (ritual['RitualCard'], ritual['Card1'], ritual['Card2'], ritual['Card3'], ritual['Result']))

    db.commit()


def init_fusions():
    db = get_db()
    cursor = db.cursor()
    cards = json.loads(current_app.open_resource('database/Cards.json').read().decode('utf-8'))

    for card in cards:
        if card['Fusions'] is not None:
            for fusion in card['Fusions']:
                fusion_sorted = sorted([fusion['_card1'], fusion['_card2']])
                cursor.execute('SELECT ROWID FROM fusions WHERE Card1 = ? AND Card2 = ? AND Result = ?',
                               (fusion_sorted[0], fusion_sorted[1], fusion['_result']))
                if cursor.fetchone() is None:
                    cursor.execute('INSERT INTO fusions (Card1, Card2, Result) VALUES (?, ?, ?)',
                                   (fusion_sorted[0], fusion_sorted[1], fusion['_result']))

    db.commit()


def init_types():
    db = get_db()
    cursor = db.cursor()
    card_types = json.loads(current_app.open_resource('database/types.json').read().decode('utf-8'))

    for idx, card_type in enumerate(card_types):
        cursor.execute('INSERT INTO types (Id, Type) VALUES (?, ?)', (idx, card_type))

    db.commit()


def init_stars():
    db = get_db()
    cursor = db.cursor()
    star_names = json.loads(current_app.open_resource('database/stars.json').read().decode('utf-8'))

    for idx, star in enumerate(star_names):
        cursor.execute('INSERT INTO stars (Id, Star) VALUES (?, ?)', (idx, star))

    db.commit()

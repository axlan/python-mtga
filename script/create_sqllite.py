import sqlite3

from mtga.set_data import all_mtga_cards, all_mtga_abilities

db_file = 'mtga.db'
with open(db_file, 'w'):
    pass

conn = sqlite3.connect(db_file)
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE rarity(
             rarity_id    INTEGER PRIMARY KEY, 
             rarity_name  TEXT)''')
c.execute('''CREATE TABLE types(
             type_id    INTEGER PRIMARY KEY, 
             type_name  TEXT)''')
c.execute('''CREATE TABLE abilities(
             ability_id    INTEGER PRIMARY KEY, 
             ability_text  TEXT)''')       
c.execute('''CREATE TABLE cards(
             mtga_id     INTEGER PRIMARY KEY, 
             card_rarity INTEGER,
             name        TEXT,
             pretty_name TEXT,
             cost        TEXT,
             color_identity        TEXT,
             card_type        INTEGER,
             sub_types        TEXT,
             set_id TEXT,
             set_number INTEGER,
             FOREIGN KEY(card_rarity) REFERENCES rarity(rarity_id),
             FOREIGN KEY(card_type) REFERENCES types(type_id))''')
c.execute('''CREATE TABLE ability_card_junction(
             mtga_id    INTEGER,
             ability_id INTEGER,
             FOREIGN KEY(mtga_id) REFERENCES cards(mtga_id),
             FOREIGN KEY(ability_id) REFERENCES abilities(ability_id))''')   


rarities = [ 'Common',
             'Uncommon',
             'Rare',
             'Mythic Rare',
             'Token',
             'Basic']
rarity_map = {k:i for i,k in enumerate(rarities)}
for i, val in enumerate(rarities):
    c.execute('''INSERT INTO rarity VALUES(?, ?)''', (i, val))

types = []
type_map = {}

abilities = []


cards = all_mtga_cards.cards


for card in cards:
    if card.card_type not in types:
        types.append(card.card_type)
        i = len(types) - 1
        type_map[card.card_type] = i
        c.execute('''INSERT INTO types VALUES(?, ?)''', (i, card.card_type))

    c.execute('''INSERT INTO cards VALUES(?, ?, ?,?, ?, ?, ?, ?, ?, ?)''',
        (card.mtga_id,
         rarity_map[card.rarity],
         card.name,
         card.pretty_name,
         " ".join(card.cost),
         " ".join(card.color_identity),
         type_map[card.card_type],
         card.sub_types,
         card.set,
         card.set_number))
    for ability in card.abilities:
        if ability not in abilities:
            abilities.append(ability)
            c.execute('''INSERT INTO abilities VALUES(?, ?)''', (ability, all_mtga_abilities[ability]))
        c.execute('''INSERT INTO ability_card_junction VALUES(?, ?)''', (card.mtga_id, ability))
                                                        

conn.commit()
conn.close()

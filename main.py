import sqlite3


class Card:
    def __init__(self, id, name, type, text) -> None:
        self.id = id
        self.name = name
        self.type = type
        # self.picture = 0
        self.text = text
    
    def __str__(self) -> str:
        return f"Card('{self.name}')"

class Stack:
    def __init__(self) -> None:
        self.cards = []
    
    def add(self, card, count=1):
        self.cards += [card] * count
    
    def remove(self, card, count):
        pass
    
    def __str__(self) -> str:
        return 'Stack(' + ', \n'.join(map(str, self.cards)) + ')'
    
    def __len__(self) -> int:
        return len(self.cards)

class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.is_alive = True
        self.hand = Stack()

class CardSet:
    def __init__(self, name) -> None:
        self.name = name
        self.cards = Stack()
        
        connection = sqlite3.connect('expl_fruit.db')
        cursor = connection.cursor()

        cursor.execute(f'select card, count from card_set_link join sets on card_set_link.seet = sets.id;')
        ids = cursor.fetchall()

        for i in ids:
            cursor.execute(f'select * from cards where id = {i[0]};')
            card = cursor.fetchone()
            card = Card(card[0], card[3], card[2], card[1])
            self.cards.add(card, i[1])

        connection.commit()
        connection.close()
    
    def build_deck(players_count: int) -> list:
        pass
    
    def __str__(self) -> str:
        return f"CardSet('{self.name}, {str(self.cards)}')"
    
    def __len__(self) -> int:
        return len(self.cards)

class Game:
    def __init__(self, players: list, cardset: CardSet) -> None:
        self.players = players
        self.cardset = cardset

if __name__ == '__main__':
    x = CardSet('Классика')
    print(x)
    print(len(x))
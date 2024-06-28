import sqlite3
import random

class Card:
    def __init__(self, id, name, type, text) -> None:
        self.id = id
        self.name = name
        self.type = type
        # self.picture = 0
        self.text = text
    
    def __str__(self) -> str:
        return f"Card({self.id}, '{self.name}')"

class Stack:
    def __init__(self, cardset) -> None:
        self.cards = []
        self.cardset = cardset
    
    def add(self, card_id: int, count=1):
        self.cards.append(self.cardset.get_card_by_id(card_id))
    
    def remove(self, card_id: int, count=1):
        black_list = []
        for i, card in enumerate(self.cards):
            if card.id == card_id:
                black_list.append(i)
                count -= 1
            if not count:
                break
        for i in range(len(black_list)):
            self.cards.pop(black_list[i] - i)

    def load(self, card, count):
        self.cards.extend([card] * count)
    
    def __str__(self) -> str:
        return 'Stack(' + ', \n'.join(map(str, self.cards)) + ')'
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def copy(self):
        result = Stack(self.cardset)
        for card in self.cards:
            result.add(card.id)
        return result
    
    def count(self, card_id: int):
        return len(tuple((c for c in self.cards if c.id == card_id)))

    def get_card_by_id(self, card_id: int):
        return next(c for c in self.cards if c.id == card_id)
    
    # def __getitem__(self, item):
    #      return self.cards[item]
    
    # def __setitem__(self, key, value):
    #     self.cards[key] = value
    
    def pop(self):
        return self.cards.pop(0).id

    def shuffle(self):
        random.shuffle(self.cards)
        random.shuffle(self.cards)

class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.is_alive = True
        self.hand = None

class CardSet:
    def __init__(self, name) -> None:
        self.name = name
        self.cards = Stack(self)
        self.import_from_db()
        self.set_consts()
    
    def import_from_db(self):
        connection = sqlite3.connect('expl_fruit.db')
        cursor = connection.cursor()

        cursor.execute(f'select card, count from card_set_link join sets on card_set_link.seet = sets.id;')
        ids = cursor.fetchall()

        for i in ids:
            cursor.execute(f'select * from cards where id = {i[0]};')
            card = cursor.fetchone()
            card = Card(card[0], card[3], card[2], card[1])
            self.cards.load(card, i[1])

        connection.commit()
        connection.close()
    
    def __str__(self) -> str:
        return f"CardSet('{self.name}, {str(self.cards)}')"
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def get_card_by_id(self, card_id):
        return self.cards.get_card_by_id(card_id)
    
    def set_consts(self):
        self.BOMB_ID = 0
        self.DEFUSE_ID = 1

class Game:
    def __init__(self, players: list, cardset: CardSet) -> None:
        self.players = players
        self.cardset = cardset
        self.deck = Stack(self.cardset)
        self.trash = Stack(self.cardset)
        self.active_player_id = 0
    
    def start(self):
        self.wake_up_players()
        self.make_deck(len(self.players))
        self.deck.shuffle()
        print('deck', self.deck)
        self.fill_hands()
        self.main()
    
    def wake_up_players(self):
        for p in self.players:
            p.is_alive = True
    
    def make_deck(self, count_players: int):
        self.deck = self.cardset.cards.copy()
        count_bombs = self.deck.count(self.cardset.BOMB_ID)
        self.deck.remove(self.cardset.BOMB_ID, count_bombs - len(self.players) + 1)
    
    def fill_hands(self):
        count_bombs = self.deck.count(self.cardset.BOMB_ID)
        count_defuse = self.deck.count(self.cardset.DEFUSE_ID)

        self.deck.remove(self.cardset.BOMB_ID, count_bombs)
        self.deck.remove(self.cardset.DEFUSE_ID, count_defuse)
        
        for player in self.players:
            player.hand = Stack(self.cardset)
            player.hand.add(self.cardset.DEFUSE_ID)
            count_defuse -= 1
            for i in range(4):
                player.hand.add(self.deck.pop())
        
        self.deck.add(self.cardset.BOMB_ID, count_bombs)
        self.deck.add(self.cardset.DEFUSE_ID, count_defuse)
        self.deck.shuffle()
    
    def check_end(self):
        return 1 != len(list(filter(lambda p: p.is_alive, self.players)))

    def main(self):
        while not self.check_end():
            pass


if __name__ == '__main__':
    s = CardSet('Classic')
    p1 = Player('Daniel')
    p2 = Player('Nikita')
    p3 = Player('Ivan')
    p4 = Player('Denis')
    pl = [p1, p2, p3, p4]
    g = Game(pl, s)
    g.start()

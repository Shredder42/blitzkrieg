import random
import pygame
from tokens import Token

class TokenBag:
    def __init__(self):
        self.allied_token_bag = self.create_token_bag()
        self.axis_token_bag = None
        

    def create_token_bag(self):
        token_bag = []
        # need to deal with the initial rect values
        token_bag.append(Token('allied', 'blitz', 1, 0, 0, 'allied_blitz.png'))
        token_bag.append(Token('allied', 'army', 1, 0, 0, 'allied_army_1.png'))
        token_bag.append(Token('allied', 'army', 1, 0, 0, 'allied_army_1.png'))
        token_bag.append(Token('allied', 'army', 1, 0, 0, 'allied_army_1.png'))
        token_bag.append(Token('allied', 'army', 2, 0, 0, 'allied_army_2.png'))
        token_bag.append(Token('allied', 'army', 2, 0, 0, 'allied_army_2.png'))
        token_bag.append(Token('allied', 'army', 3, 0, 0, 'allied_army_3.png'))
        token_bag.append(Token('allied', 'army', 3, 0, 0, 'allied_army_3.png'))
        token_bag.append(Token('allied', 'airforce', 1, 0, 0, 'allied_airforce_1.png'))
        token_bag.append(Token('allied', 'airforce', 1, 0, 0, 'allied_airforce_1.png'))
        token_bag.append(Token('allied', 'airforce', 1, 0, 0, 'allied_airforce_1.png'))
        token_bag.append(Token('allied', 'airforce', 2, 0, 0, 'allied_airforce_1.png'))
        token_bag.append(Token('allied', 'airforce', 2, 0, 0, 'allied_airforce_1.png'))
        token_bag.append(Token('allied', 'navy', 1, 0, 0, 'allied_navy_1.png'))
        token_bag.append(Token('allied', 'navy', 1, 0, 0, 'allied_navy_1.png'))
        token_bag.append(Token('allied', 'navy', 1, 0, 0, 'allied_navy_1.png'))
        token_bag.append(Token('allied', 'navy', 2, 0, 0, 'allied_navy_2.png'))
        token_bag.append(Token('allied', 'navy', 2, 0, 0, 'allied_navy_2.png'))
        token_bag.append(Token('allied', 'navy', 3, 0, 0, 'allied_navy_3.png'))
        token_bag.append(Token('allied', 'navy', 3, 0, 0, 'allied_navy_3.png'))
        token_bag.append(Token('allied', 'army', 1, 0, 0, 'allied_general.png'))
        token_bag.append(Token('allied', 'navy', 1, 0, 0, 'allied_admiral.png'))
        random.shuffle(token_bag)
        return token_bag


class PlayerHand:
    def __init__(self, bag):
        self.bag = bag
        self.hand_list = self.draw_starting_hand()

    def draw_starting_hand(self):
        hand_list = []
        for i in range(5):
            hand_list.append(self.bag.pop())
        return hand_list



if __name__ == '__main__':
    bag = TokenBag()
    print(type(bag.allied_token_bag))
    print(len(bag.allied_token_bag))
    print(bag.allied_token_bag[0].unit)

    hand = PlayerHand(bag.allied_token_bag)
    for token in hand.hand_list:
        print(f'{token.unit} value {token.value}')


    


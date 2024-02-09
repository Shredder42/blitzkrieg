import random
import pygame
from tokens import Token

class TokenBags:
    ''' token bag that holds the tokens to draw from '''
    def __init__(self):
        self.allied_token_bag = self.create_allied_token_bag()
        self.axis_token_bag = self.create_axis_token_bag()
        

    def create_allied_token_bag(self):
        token_bag = []
        token_bag.append(Token('allied', 'blitz', 0, 'allied_blitz.png', True))
        token_bag.append(Token('allied', 'army', 1, 'allied_army_1.png'))
        token_bag.append(Token('allied', 'army', 1, 'allied_army_1.png'))
        token_bag.append(Token('allied', 'army', 1, 'allied_army_1.png'))
        token_bag.append(Token('allied', 'army', 2, 'allied_army_2.png'))
        token_bag.append(Token('allied', 'army', 2, 'allied_army_2.png'))
        token_bag.append(Token('allied', 'army', 3, 'allied_army_3.png'))
        token_bag.append(Token('allied', 'army', 3, 'allied_army_3.png'))
        token_bag.append(Token('allied', 'airforce', 1, 'allied_airforce_1.png'))
        token_bag.append(Token('allied', 'airforce', 1, 'allied_airforce_1.png'))
        token_bag.append(Token('allied', 'airforce', 1, 'allied_airforce_1.png'))
        token_bag.append(Token('allied', 'airforce', 2, 'allied_airforce_2.png'))
        token_bag.append(Token('allied', 'airforce', 2, 'allied_airforce_2.png'))
        token_bag.append(Token('allied', 'navy', 1,'allied_navy_1.png'))
        token_bag.append(Token('allied', 'navy', 1, 'allied_navy_1.png'))
        token_bag.append(Token('allied', 'navy', 1, 'allied_navy_1.png'))
        token_bag.append(Token('allied', 'navy', 2, 'allied_navy_2.png'))
        token_bag.append(Token('allied', 'navy', 2, 'allied_navy_2.png'))
        token_bag.append(Token('allied', 'navy', 3, 'allied_navy_3.png'))
        token_bag.append(Token('allied', 'navy', 3, 'allied_navy_3.png'))
        token_bag.append(Token('allied', 'army', 1, 'allied_general.png'))
        token_bag.append(Token('allied', 'navy', 1, 'allied_admiral.png'))
        random.shuffle(token_bag)
        return token_bag
    
    def create_axis_token_bag(self):
        token_bag = []
        token_bag.append(Token('axis', 'blitz', 0, 'axis_blitz.png', True))
        token_bag.append(Token('axis', 'army', 1, 'axis_army_1.png'))
        token_bag.append(Token('axis', 'army', 1, 'axis_army_1.png'))
        token_bag.append(Token('axis', 'army', 1, 'axis_army_1.png'))
        token_bag.append(Token('axis', 'army', 2, 'axis_army_2.png'))
        token_bag.append(Token('axis', 'army', 2, 'axis_army_2.png'))
        token_bag.append(Token('axis', 'army', 3, 'axis_army_3.png'))
        token_bag.append(Token('axis', 'army', 3, 'axis_army_3.png'))
        token_bag.append(Token('axis', 'airforce', 1, 'axis_airforce_1.png'))
        token_bag.append(Token('axis', 'airforce', 1, 'axis_airforce_1.png'))
        token_bag.append(Token('axis', 'airforce', 1, 'axis_airforce_1.png'))
        token_bag.append(Token('axis', 'airforce', 2, 'axis_airforce_2.png'))
        token_bag.append(Token('axis', 'airforce', 2, 'axis_airforce_2.png'))
        token_bag.append(Token('axis', 'navy', 1,'axis_navy_1.png'))
        token_bag.append(Token('axis', 'navy', 1, 'axis_navy_1.png'))
        token_bag.append(Token('axis', 'navy', 1, 'axis_navy_1.png'))
        token_bag.append(Token('axis', 'navy', 2, 'axis_navy_2.png'))
        token_bag.append(Token('axis', 'navy', 2, 'axis_navy_2.png'))
        token_bag.append(Token('axis', 'navy', 3, 'axis_navy_3.png'))
        token_bag.append(Token('axis', 'navy', 3, 'axis_navy_3.png'))
        token_bag.append(Token('axis', 'army', 1, 'axis_general.png'))
        token_bag.append(Token('axis', 'navy', 1, 'axis_admiral.png'))
        random.shuffle(token_bag)
        return token_bag


class PlayerHand:
    ''' players playing hand '''
    def __init__(self, bag):
        self.bag = bag
        self.hand_list = self.draw_starting_hand()

    def draw_starting_hand(self):
        hand_list = []
        for i in range(5):
            x = 50 + i * 60
            y = 870
            current_token = self.bag.pop()
            current_token.token_starting_location(x, y) 
            hand_list.append(current_token)
        return hand_list
    
    def draw_new_token(self):
        self.hand_list.append(self.bag.pop())
        for i, token in enumerate((self.hand_list)):
            x = 50 + i * 60
            y = 870
            token.token_starting_location(x, y) 





if __name__ == '__main__':
    bag = TokenBags()
    print(type(bag.allied_token_bag))
    print(len(bag.allied_token_bag))
    print(bag.allied_token_bag[0].unit)

    hand = PlayerHand(bag.allied_token_bag)
    for token in hand.hand_list:
        print(f'{token.unit} value {token.value}')


    


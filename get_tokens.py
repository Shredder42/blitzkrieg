import os
import pygame


def punch_out_pieces(punch_out, x, y, side, row_length, row):
    '''
    load punchout image and crop out specific game pieces
    '''
    pieces = pygame.image.load(os.path.join('images', punch_out))
    for i in range(row_length):
        piece_png = pieces.subsurface(x, y, 90, 90)
        pygame.image.save(piece_png, os.path.join('images',f'{side}_row_{row}_image_{i+1}.png'))
        x += 113

def symbols():
    board = pygame.image.load(os.path.join('images', 'blitzkrieg_game_board_italian.jpg'))
    symbol = board.subsurface(266, 207, 12, 12 )
    pygame.image.save(symbol, os.path.join('images', 'allied_symbol_3.jpg'))
    symbol = board.subsurface(438, 207, 12, 12 )
    pygame.image.save(symbol, os.path.join('images', 'axis_symbol_3.jpg'))

# Axis tiles
    # horizontal spacing is 113 - beginning at 39
    # vertical spacing is 113 - beginning at 27

# punch_out_pieces('axis_tokens.png', 39, 27, 'axis', 7, 1)
# punch_out_pieces('axis_tokens.png', 39, 140, 'axis', 7, 2)
# punch_out_pieces('axis_tokens.png', 39, 253, 'axis', 6, 3)
# punch_out_pieces('axis_tokens.png', 39, 366, 'axis', 7, 4)
# punch_out_pieces('axis_tokens.png', 39, 479, 'axis', 7, 5)


# Allied tiles
    # horizontal spacing is 113 - beginning at 36
    # vertical spacing is 113 - beginning at 27

# punch_out_pieces('allied_tokens.png', 36, 27, 'allied', 7, 1)
# punch_out_pieces('allied_tokens.png', 36, 140, 'allied', 7, 2)
# punch_out_pieces('allied_tokens.png', 36, 253, 'allied', 7, 3)
# punch_out_pieces('allied_tokens.png', 36, 366, 'allied', 7, 4)
# punch_out_pieces('allied_tokens.png', 36, 479, 'allied', 7, 5)

# Images renamed outside of python and duplicates removed
    
symbols()
        



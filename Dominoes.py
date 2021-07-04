import random


def shuffle_deal(doms):
    random.shuffle(doms)
    
    stock, comp, player = [], [], []
    i = 0
    for d in doms:
        if i < 14:
            stock.append(d)
        elif 15 <= i < 22:
            comp.append(d)
        else:
            player.append(d)
        i += 1

    return stock, comp, player


def start_piece(comp, play):
    doubles = []

    for d in comp:
        if d[0] == d[1]:
            doubles.append(d)
   
    if len(doubles) > 0:
        doubles.sort()
        comp_high = doubles.pop()
    else:
        comp_high = []

    doubles = []

    for d in play:
        if d[0] == d[1]:
            doubles.append(d)

    if len(doubles) > 0:
        doubles.sort()
        play_high = doubles.pop()
    else:
        play_high = []

    if comp_high > play_high:
        return comp_high, "player", True
    elif comp_high < play_high:
        return play_high, "computer", True
    else:
        return [], "", False


# displays the pieces in play, if there are more than 6 pieces, 
# only the first 3 and last 3 are displayed
def display_snake(in_play):
    print()
    if len(in_play) > 6:
        print("{0}{1}{2}...{3}{4}{5}".format
              (in_play[0], in_play[1], in_play[2], in_play[-3], in_play[-2], in_play[-1]))
    else:
        for p in in_play:
            print(p, end="")
    print()


# displays the player's pieces as a numbered list
def display_player(pieces):
    i = 1
    for p in pieces:
        print("{0}:{1}".format(i, p))
        i += 1


def player_moves(pieces, stock, snake):
    limit = len(pieces)
    l_or_r = 0 # a 1 for the left, a 0 for the right
    selection = input()
    good = [str(j) for j in range(0, limit+1)]
    is_good = False

    while not is_good:
        if selection == "0" or selection == "-0":
            return stock.pop(), 2
        if selection[0] == "-":
            l_or_r = 1
            selection = selection.lstrip("-")
        if selection in good:
            selection = int(selection)
            is_good, in_play = placement_checker(pieces[selection - 1], l_or_r, snake)
            if not is_good:
                print("Illegal move. Please try again.")
                selection = input()
                l_or_r = 0
        else:
            print("Invalid input. Please try again.")
            selection = input()
            l_or_r = 0

    return in_play, l_or_r



def comp_moves(pieces, stock, snake):
    # ranking the pieces based on their rarity
    count_dict = {}
    temp = 0
    for i in range(0,7):
        for x in snake:
            temp += x.count(i)
        for y in pieces:
            temp += y.count(i)
        count_dict[i] = temp
        temp = 0

    the_scores = []
    for dom in pieces:
        for num in dom:
            temp += count_dict[num]
        the_scores.append(temp)
        temp = 0

    # a 1 for the left, a 0 for the right
    l_or_r = 0
    good_piece = False
    play_pieces = []
    for d in pieces:
        play_pieces.append(d)
    i = the_scores.index(max(the_scores))
    the_scores.pop(i)
    play = play_pieces.pop(i)

    # going through all the pieces to see if there is a match
    # on either side. if not, draw from the stock
    while not good_piece and len(play_pieces) != 0:
        good_piece, the_piece = placement_checker(play, l_or_r, snake)
        if good_piece:
            return the_piece, l_or_r
        if l_or_r:
            l_or_r = 0
            i += 1
            i = the_scores.index(max(the_scores))
            the_scores.pop(i)
            play = play_pieces.pop(i)
        else:
            l_or_r = 1

    return stock.pop(), 3


def placement_checker(play_piece, position, snake):
    # position = 1 is left, 0 is right
    a_match = False
    #match_pos = 0
    if position == 1:
        if play_piece.count(snake[0][0]) > 0:
            a_match = True
            if play_piece.index(snake[0][0]) == 0:
                play_piece.reverse()
    elif position == 0:
        if play_piece.count(snake[-1][1]) > 0:
            a_match = True
            if play_piece.index(snake[-1][1]) == 1:
                play_piece.reverse()
    
    return a_match, play_piece


def end_of_game(player, comp, snake):
    # if a player uses all of their pieces, the game is over
    # so return True and 1
    if len(player) == 0:
        #print("The game is over. You won!")
        return True, 1
    elif len(comp) == 0: # return True and 2
        #print("The game is over. The computer won!")
        return True, 2

    # if the numbers on the ends of the snake are identical
    # and appear within the snake 8 times, the game is over
    # and it is a draw, so return True and 3
    list_snake = []
    #count = 0
    for i in snake:
        for j in i:
            list_snake.append(j)

    if list_snake[0] == list_snake[-1] and list_snake.count(list_snake[0]) >= 8:
        return True, 3

    return False, 0


# *******MAIN*******

# creating the dominos
dominos = []

for i in range(0, 7):
    for j in range(0, (i+1)):
        dominos.append([j, i])

# shuffling the pieces, dealing 7 to each player, figuring out
# the starting piece, and who will have the first turn
can_start = False

while not can_start:
    stock_pieces, computer_pieces, player_pieces = shuffle_deal(dominos)
    starting_piece, status, can_start = start_piece(computer_pieces, player_pieces)

if computer_pieces.count(starting_piece) != 0:
    computer_pieces.remove(starting_piece)
else:
    player_pieces.remove(starting_piece)

dom_snake = [starting_piece]
game_over = False
winner = 0

while not game_over:
    print("=" * 70)
    print("Stock size: {0}".format(len(stock_pieces)))
    print("Computer pieces: {0}".format(len(computer_pieces)))

    display_snake(dom_snake)

    print("\nYour pieces:")
    display_player(player_pieces)

    print("\nStatus: " ,end="")

    if status == "player":
        print("It's your turn to make a move. Enter your command.")
        next_move, location = player_moves(player_pieces, stock_pieces, dom_snake)
        if location == 0 or location == 1:
            if player_pieces.count(next_move) > 0:
                player_pieces.remove(next_move)
            else:
                next_move.reverse()
                player_pieces.remove(next_move)
        status = "computer"
    else:
        print("Computer is about to make a move. Press Enter to continue...")
        input()
        next_move, location = comp_moves(computer_pieces, stock_pieces, dom_snake)
        if location == 0 or location == 1:
            if computer_pieces.count(next_move) > 0:
                computer_pieces.remove(next_move)
            else:
                next_move.reverse()
                computer_pieces.remove(next_move)
        status = "player"

    if location == 0:
        dom_snake.append(next_move)
    elif location == 1:
        dom_snake.insert(0, next_move)
    elif location == 2:
        player_pieces.append(next_move)
    elif location == 3:
        computer_pieces.append(next_move)

    game_over, winner = end_of_game(player_pieces, computer_pieces, dom_snake)

    if len(stock_pieces) == 0 and not game_over:
        game_over = True
        winner = 3

print("=" * 70)
print("Stock size: {0}".format(len(stock_pieces)))
print("Computer pieces: {0}".format(len(computer_pieces)))

display_snake(dom_snake)

print("\nYour pieces:")
display_player(player_pieces)

print("\nStatus: " ,end="")

if winner == 1:
    print("The game is over, You won!")
elif winner == 2:
    print("The game is over. The computer won!")
else:
    print("The game is over. It's a draw!")


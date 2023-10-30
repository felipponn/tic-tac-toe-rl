import random as rd
# a(0,1,2,3,...,8) := estado do jogo
# a(i) está em {X,O,vazio}
# vazio := 0
# X := 1
# O := 2

# No total, 3^9 = 19683 estados possíveis
MAX_STATES = 19683

# Função que retorna o estado do jogo
def get_state(board):
    state = 0
    for i in range(9):
        if board[i] == 'X':
            state += 3**i
        elif board[i] == 'O':
            state += 2*(3**i)
    return state

# Função que mostra o tabuleiro
def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print()
        if i % 3 != 2:
            print(board[i], end = '|')
        else:
            print(board[i], end = ' ')
    print()

# Função que retorna o tabuleiro a partir do estado
def get_board(state):
    board = [' ' for i in range(9)]
    for i in range(9):
        if state % 3 == 1:
            board[i] = 'X'
        elif state % 3 == 2:
            board[i] = 'O'
        state = state // 3
    return board

# Função que checa se algum jogador ganhou
def check_win(board):
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != ' ':
            return board[i]
        if board[3*i] == board[3*i+1] == board[3*i+2] != ' ':
            return board[3*i]
    if board[0] == board[4] == board[8] != ' ':
        return board[0]
    if board[2] == board[4] == board[6] != ' ':
        return board[2]
    if ' ' not in board:
        return 'draw'
    return ' '

# Função que treina o computador jogando
def train_play(player_symbol, state, archetype):
    board = get_board(state)
    if archetype == 'random':
        while True:
            pos = rd.randint(0, 8)
            if board[pos] == ' ':
                break
    elif archetype == 'kinda_smart':
        opponent = 'X' if player_symbol == 'O' else 'O'
        while True:
            pos = rd.randint(0, 8)
            if board[pos] == ' ':
                break
        for i in range(9):
            if board[i] == ' ':
                board[i] = player_symbol
                if check_win(board) == player_symbol:
                    pos = i
                    break
                board[i] = ' '
        for i in range(9):
            if board[i] == ' ':
                board[i] = opponent
                if check_win(board) == opponent:
                    pos = i
                    break
                board[i] = ' '
    return pos

# Função que aprende a jogar
def learn(player_symbol, learning_rate, exploration_rate, epochs):
    values = [0.5 for i in range(MAX_STATES)]
    for i in range(MAX_STATES):
        board = get_board(i)
        if check_win(board) == player_symbol:
            values[i] = 1
        elif check_win(board) == 'draw':
            values[i] = 0.5
        elif check_win(board) != ' ':
            values[i] = 0

    archetypes = ['random', 'kinda_smart', 'kinda_smart']
    
    for epoch in range(epochs):
        idx = rd.randint(0, 2)
        board = [' ' for i in range(9)]
        state = get_state(board)
        opponent = 'X' if player_symbol == 'O' else 'O'
        for turn in range(9):
            if check_win(board) != ' ':
                break
            if (turn % 2 == 0 and player_symbol == 'X') or (turn % 2 == 1 and player_symbol == 'O'):
                if rd.random() < exploration_rate:
                    while True:
                        pos = rd.randint(0, 8)
                        if board[pos] == ' ':
                            break
                else:
                    max_value = -1
                    for i in range(9):
                        if board[i] == ' ':
                            board[i] = player_symbol
                            new_state = get_state(board)
                            board[i] = ' '
                            if values[new_state] > max_value:
                                max_value = values[new_state]
                                pos = i
                board[pos] = player_symbol
                new_state = get_state(board)
                values[state] += learning_rate * (values[new_state] - values[state])
                state = new_state
            else:
                pos = train_play(player_symbol, state, archetypes[idx])
                board[pos] = opponent
                new_state = get_state(board)
                values[state] += learning_rate * (values[new_state] - values[state])
                state = new_state
        if epoch % 1000 == 0:
            print('Epoch:', epoch)
    return values

def play(player_symbol, values):
    board = [' ' for i in range(9)]
    state = get_state(board)
    opponent = 'X' if player_symbol == 'O' else 'O'
    for turn in range(9):
        print_board(board)
        print("-----")
        if check_win(board) != ' ':
            break
        if (turn % 2 == 0 and player_symbol == 'X') or (turn % 2 == 1 and player_symbol == 'O'):
            max_value = -1
            for i in range(9):
                if board[i] == ' ':
                    board[i] = player_symbol
                    new_state = get_state(board)
                    board[i] = ' '
                    if values[new_state] > max_value:
                        max_value = values[new_state]
                        pos = i
            board[pos] = player_symbol
            new_state = get_state(board)
            state = new_state
        else:
            pos = -1
            while pos == -1 or board[pos] != ' ':
                pos = int(input('Posição: '))
            board[pos] = opponent
            new_state = get_state(board)
            state = new_state
    print_board(board)
    print("-----")
    print('Winner:', check_win(board))
    if check_win(board) == opponent:
        print("Congratulations, you beat the computer!")
    elif check_win(board) == 'draw':
        print("It's a draw!")
    else:
        print("You lost!")

def simulate(player_symbol, values, epochs):
    wins_for_the_computer = 0
    draws = 0
    for _ in range(epochs):
        board = [' ' for i in range(9)]
        state = get_state(board)
        opponent = 'X' if player_symbol == 'O' else 'O'
        for turn in range(9):
            if check_win(board) != ' ':
                break
            if (turn % 2 == 0 and player_symbol == 'X') or (turn % 2 == 1 and player_symbol == 'O'):
                max_value = -1
                for i in range(9):
                    if board[i] == ' ':
                        board[i] = player_symbol
                        new_state = get_state(board)
                        board[i] = ' '
                        if values[new_state] > max_value:
                            max_value = values[new_state]
                            pos = i
                board[pos] = player_symbol
                new_state = get_state(board)
                state = new_state
            else:
                pos = train_play(player_symbol, state, 'kinda_smart')
                board[pos] = opponent
                new_state = get_state(board)
                state = new_state
        if check_win(board) == player_symbol:
            wins_for_the_computer += 1
        elif check_win(board) == 'draw':
            draws += 1
    return (wins_for_the_computer+0.5*draws)/epochs

def main():
    max_X = {'learning_rate': 0, 'exploration_rate': 0, 'value': 0}
    max_O = {'learning_rate': 0, 'exploration_rate': 0, 'value': 0}
    possibilities = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    for learning_rate in possibilities:
        for exploration_rate in possibilities:
            epochs = 2000
            values = learn('X', learning_rate, exploration_rate, epochs)
            value = simulate('X', values, 1000)
            if value > max_X['value']:
                max_X['learning_rate'] = learning_rate
                max_X['exploration_rate'] = exploration_rate
                max_X['value'] = value
            values = learn('O', learning_rate, exploration_rate, epochs)
            value = simulate('O', values, 1000)
            if value > max_O['value']:
                max_O['learning_rate'] = learning_rate
                max_O['exploration_rate'] = exploration_rate
                max_O['value'] = value
    print('X:', max_X)
    print('O:', max_O)

if __name__ == '__main__':
    main()

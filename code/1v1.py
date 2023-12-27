from keras.models import Sequential
from tensorflow.keras.models import load_model
import chess
import numpy as np 
import ChessEngine as ce


model = load_model('/Users/viktorsjoberg/Desktop/Chess/fit/model1.h5')

def FENtoVEC (FEN):
    pieces = {"r":5,"n":3,"b":3.5,"q":9.5,"k":20,"p":1,"R":-5,"N":-3,"B":-3.5,"Q":-9.5,"K":-20,"P":-1}
    FEN = list(str(FEN.split()[0]))
    VEC = []
    for i in range(len(FEN)):
        if FEN[i] == "/":
            continue
        if FEN[i] in pieces:
            VEC.append(pieces[FEN[i]])
        else:
            em = [VEC.append(0) for i in range(int(FEN[i]))]

    return VEC

def evaluate_board():
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    else:
        FENp = board.epd()
        inVEC = np.asarray([FENtoVEC(FENp)])
        evalu = model.predict(inVEC)[0]*10
        return evalu
board = chess.Board()
print(evaluate_board())
def alphabeta( alpha, beta, depthleft ):
    bestscore = -9999
    if( depthleft == 0 ):
        return quiesce( alpha, beta )
    for move in board.legal_moves:
        board.push(move)   
        score = -alphabeta( -beta, -alpha, depthleft - 1 )
        board.pop()
        if( score >= beta ):
            return score
        if( score > bestscore ):
            bestscore = score
        if( score > alpha ):
            alpha = score   
    return bestscore
def quiesce( alpha, beta ):
    stand_pat = evaluate_board()
    if( stand_pat >= beta ):
        return beta
    if( alpha < stand_pat ):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)        
            score = -quiesce( -beta, -alpha )
            board.pop()

            if( score >= beta ):
                return beta
            if( score > alpha ):
                alpha = score  
    return alpha
def selectmove(depth):
    bestMove = chess.Move.null()
    bestValue = -99999
    alpha = -100000
    beta = 100000
    for move in board.legal_moves:
        board.push(move)
        boardValue = -alphabeta(-beta, -alpha, depth-1)
        if boardValue > bestValue:
            bestValue = boardValue;
            bestMove = move
        if( boardValue > alpha ):
            alpha = boardValue
        board.pop()
    return bestMove




board = chess.Board()

# Initialize your engines
# For the first engine (minimax-based)
maxDepth = 2  # or any other depth you want to use
engine1 = ce.Engine(board, maxDepth, chess.WHITE)

# For the second engine (neural network-based)
# Ensure that the neural network model and required functions are properly defined

def game_over(board):
    return board.is_checkmate() or board.is_stalemate() or board.can_claim_draw()

while not game_over(board):
    print(board)

    if board.turn == chess.WHITE:
        # Engine 1 (White) makes a move
        board.push(engine1.getBestMove())
    else:
        # Engine 2 (Black) makes a move
        move = selectmove(2)
        board.push(move)

    # Output the board after each move
    print(board)
# ChessEngine 
import chess as ch
import random as rd



class Engine:
    def __init__(self, board, maxDepth, color):
        self.board=board
        self.maxDepth=maxDepth
        self.color=color
        self.PIECE_VALUES = [
        100, 320, 330, 500, 900, 2000,
        -100, -320, -330, -500, -900, -2000
        ]
        self.PAWN_W_PST = [
            0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10,-20,-20, 10, 10,  5,
            5, -5,-10,  0,  0,-10, -5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5,  5, 10, 25, 25, 10,  5,  5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0,  0,  0,  0,  0,  0,  0,  0 
        ]
        self.KNIGHT_W_PST = [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50
        ]
        self.BISHOP_W_PST = [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -20,-10,-10,-10,-10,-10,-10,-20
        ]
        self.ROOK_W_PST = [
            0,  0,  5,  10, 10, 5,  0,  0,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            5,  10, 10, 10, 10, 10, 10, 5,
            0,  0,  0,  0,  0,  0,  0,  0,
        ] 
        self.QUEEN_W_PST = [
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -10,  5,  5,  5,  5,  5,  0,-10,
            0,  0,  5,  5,  5,  5,  0, -5,
            -5,  0,  5,  5,  5,  5,  0, -5,
            -10,  0,  5,  5,  5,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20,
        ]
        self.KING_W_PST = [
            20,  30,  10,  0,   0,   10,  30,  20,
            20,  20,  0,   0,   0,   0,   20,  20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
        ]




    def getBestMove(self):
        return self.engine(None, 1)

    def evalfunct(self):
        compt = 0
        for i in range(64):
            compt+=self.squareResPoints(ch.SQUARES[i])
        compt+=self.mateOpportunity()+self.openning()+0.001*rd.random()
        return compt


    def openning(self):
        if self.board.fullmove_number < 10:
            if self.board.turn == self.color:
                return -1 / 30 * self.board.legal_moves.count()
            else:
                return 0
        return 0

    def mateOpportunity(self):
        if (self.board.legal_moves.count()==0):
            if (self.board.turn == self.color):
                return -100000
            else:
                return 10000
        return 0    
    
    #Takes a square as input and 
    #return the corresponding han´s berliner´s
    #system value of it´s resident
    def squareResPoints(self, square):
        piece = self.board.piece_at(square)
        if piece is None:
            return 0
        if piece.color == ch.BLACK:
            square = 63 - square

        piece_type = piece.piece_type
        piece_value = self.PIECE_VALUES[piece_type - 1]  # Adjust the index according to your PIECE_VALUES list
        square_value = 0

        if(piece_type==ch.PAWN):
            square_value = self.PAWN_W_PST[square]
        elif(piece_type==ch.ROOK):
            square_value = self.ROOK_W_PST[square]
        elif(piece_type==ch.BISHOP):
            square_value = self.BISHOP_W_PST[square]
        elif(piece_type==ch.KNIGHT):
            square_value = self.KNIGHT_W_PST[square]
        elif(piece_type==ch.QUEEN):
            square_value = self.QUEEN_W_PST[square]
        elif(piece_type==ch.KING):
            square_value = self.KING_W_PST[square]
        if piece.color != self.color:
            return -(piece_value + square_value)
        else:
            return piece_value + square_value
        
    def engine(self, candidate, depth):
        if ( depth == self.maxDepth or self.board.legal_moves.count()==0):
                return self.evalfunct()
        else: 
            #get list of legal moves of the current position 
            moveList = list(self.board.legal_moves)

            # initialise newCandidate
            newCandidate=None

            if(depth % 2 != 0):
                newCandidate=float("-inf")
            else:
                newCandidate=float("inf")

            for i in moveList:
                #Play the move i 
                self.board.push(i)

                #Get the value of move i 
                value = self.engine(newCandidate, depth+1)

                #basic minmax algorithm:
                #if maximizing (engine´s turn)
                if(value > newCandidate and depth % 2 != 0):
                    newCandidate=value
                    if(depth==1):
                        move=i
                #if minimizing (human´s turn) 
                elif(value < newCandidate and depth % 2 == 0):
                    newCandidate=value
                
                #Alpha-beta pruning cuts:
                #(if previous move was made by the engine)
                if (candidate != None and value < candidate and depth % 2 == 0):
                    self.board.pop()
                    break

                #Alpha-beta pruning cuts:
                #(if previous move was made by the human)
                elif (candidate != None and value > candidate and depth % 2 != 0):
                    self.board.pop()
                    break
                self.board.pop()
        if (depth>1):
            #Return value of a th node in the tree 
            return newCandidate
        else:
            return move            





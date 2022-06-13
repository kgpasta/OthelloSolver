import struct, string, copy, random

class Kaustubh_Garimella:

    def __init__(self):
        self.board = [[' ']*8 for i in range(8)]
        self.size = 8
        self.board[4][4] = 'W'
        self.board[3][4] = 'B'
        self.board[3][3] = 'W'
        self.board[4][3] = 'B'
        # a list of unit vectors (row, col)
        self.directions = [ (-1,-1), (-1,0), (-1,1), (0,-1),(0,1),(1,-1),(1,0),(1,1)]
        
#prints the board
    def PrintBoard(self):

        # Print column numbers
        print("  ",end="")
        for i in range(self.size):
            print(i+1,end=" ")
        print()

        # Build horizontal separator
        linestr = " " + ("+-" * self.size) + "+"

        # Print board
        for i in range(self.size):
            print(linestr)                       # Separator
            print(i+1,end="|")                   # Row number
            for j in range(self.size):
                print(self.board[i][j],end="|")  # board[i][j] and pipe separator 
            print()                              # End line
        print(linestr)

    def board_full(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.get_square(i,j)==" ":
                    return False
        return True
    
#determines the score of the board by adding +1 for every tile owned by player, and -1 for every tile owned by opp
    def score(self, player, opp):
        score = 0
        for i in range(self.size):
            for j in range(self.size):
                if(self.get_square(i,j)==player):
                    score +=1
                elif(self.get_square(i,j)==opp):
                    score -= 1
        return score

#returns true if the square was played, false if the move is not allowed
    def place_piece(self, row, col, player, opp):
        if(self.get_square(row,col)!=" "):
            return False
        
        
        if(player == opp):
            print("player and opponent cannot be the same")
            return False
        legal = False
        #for each direction, check to see if the move is legal by seeing if the adjacent square
        #in that direction is occuipied by the opponent. If it isnt check the next direction.
        #if it is, check to see if one of the players pieces is on the board beyond the oppponents piece,
        #if the chain of opponents pieces is flanked on both ends by the players pieces, flip
        #the opponents pieces 
        for Dir in self.directions:
            #look across the length of the board to see if the neighboring squares are empty,
            #held by the player, or held by the opponent
            for i in range(self.size):
                if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
                    #does the adjacent square in direction dir belong to the opponent?
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= opp and i==1 : # no
                        #no pieces will be flipped in this direction, so skip it
                        break
                    #yes the adjacent piece belonged to the opponent, now lets see if there are a chain
                    #of opponent pieces
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
                        break

                    #with one of player's pieces at the other end
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==player and i!=0 and i!=1 :
                        #set a flag so we know that the move was legal
                        legal = True
                        self.flip_tiles(row, col, Dir, i, player)
                        break
                    
                        
        return legal

#sets all tiles along a given direction (Dir) from a given starting point (col and row) for a given distance
# (dist) to be a given value ( player )
    def flip_tiles(self, row, col, Dir, dist, player):
        for i in range(dist):
            self.board[row+ i*Dir[0]][col + i*Dir[1]] = player
        return True
    
#returns the value of a square on the board
    def get_square(self, row, col):
        return self.board[row][col]

#checks all board positions to see if there is a legal move
    def has_move(self, player, opp):
        for i in range(self.size):
            for j in range(self.size):
                if self.islegal(i,j,player,opp):
                    return True
        return False

#checks every direction fromt the position which is input via "col" and "row", to see if there is an opponent piece
#in one of the directions. If the input position is adjacent to an opponents piece, this function looks to see if there is a
#a chain of opponent pieces in that direction, which ends with one of the players pieces.    
    def islegal(self, row, col, player, opp):
        if(self.get_square(row,col)!=" "):
            return False
        for Dir in self.directions:
            for i in range(self.size):
                if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
                    #does the adjacent square in direction dir belong to the opponent?
                    if self.get_square(row+ i*Dir[0],col + i*Dir[1])!= opp and i==1 : # no
                        #no pieces will be flipped in this direction, so skip it
                        break
                    #yes the adjacent piece belonged to the opponent, now lets see if there are a chain
                    #of opponent pieces
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
                        break

                    #with one of player's pieces at the other end
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==player and i!=0 and i!=1 :
                        #set a flag so we know that the move was legal
                        return True
        return False

#returns true if no square in the board contains "_", false otherwise
    def full_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if(self.board[i][j]==' '):
                    return False

        return True

    #Get all legal spaces on board and return
    def get_open_spaces(self,player,opp):
        row = []
        col = []
        for i in range(self.size):
            for j in range(self.size):
                if(self.islegal(i,j,player,opp)):
                    row.append(i)
                    col.append(j)
        return row,col

    #Places piece of opponent's color at (row,col) and then returns 
    #the best move, determined by the make_move(...) function
    def play_square(self, row, col, playerColor, oppColor):
        # Place a piece of the opponent's color at (row,col)
        if (row,col) != (-1,-1):
            self.place_piece(row,col,oppColor,playerColor)

        b2 = copy.deepcopy(self.board)
        # Determine best move and and return value to Matchmaker
        i,j = make_intelligent_cpu_move(self,playerColor, oppColor)
        self.board = b2
        self.place_piece(i,j,playerColor,oppColor)
        return i,j
    
#Checks to see if the given player controls the entire board
    def all_pieces(self, player):
        for i in range(self.size):
            for j in range(self.size):
                if(self.get_square(i,j) != player and self.get_square(i,j) != ' '):
                    return False
        return True

    def corner(self,row,col):
        if(row == 0 and (col == 0 or col == 7)):
            return True
        elif(row == 7 and (col == 0 or col == 7)):
            return True
        else:
            return False

    def evaluate(self, player, opp):
        score = 0
        for i in range(self.size):
            for j in range(self.size):
                if(self.corner(i,j) and self.get_square(i,j) == player):
                    score -= 10
                elif(self.corner(i,j) and self.get_square(i,j) == opp):
                    score += 10
                elif(self.islegal(i,j,player,opp)):
                    score -= 1
                elif(self.islegal(i,j,opp,player)):
                    score += 1
        return score
                
                   
#The cpu will search the game board for a legal move, and play the first one it finds
def make_simple_cpu_move(board, cpuval, oppval):
    for i in range(board.size):
        for j in range(board.size):
            if(board.islegal(i,j,cpuval, oppval)):
                # board.place_piece(i,j,cpuval, oppval)
                # print("CPU has played row: " +str(i+1)+"  col: "+str(j+1))
                return i,j
    return (-1,-1)

def make_random_cpu_move(board,cpuval,oppval):
    r,c = board.get_open_spaces(cpuval,oppval)
    i,j = -1, -1
    if(r):
        index = random.randint(0,len(r) - 1)
        i,j = r[index],c[index]
    return i,j

#Alpha-Beta pruning with Minimax to make move
def make_intelligent_cpu_move(board,cpuval,oppval):
    row,col,score = maximize(board,-100,100,cpuval,oppval,3)
    if(row == None or col == None):
        row = -1
        col = -1
    return row,col

#Maximizing function
def maximize(board,a,b,cpuval,oppval,depth):
    maxscore = None
    maxrow = None
    maxcol = None
    alpha = a
    beta = b

    if(depth == 0):
        return maxrow,maxcol,board.evaluate(cpuval,oppval)
        
    r,c = board.get_open_spaces(cpuval,oppval)
    if(not r):
        return maxrow,maxcol,board.evaluate(cpuval,oppval)
    else:
        for i in range(0,len(r)):
            if(alpha > beta):
                break

            board2 = copy.deepcopy(board)
            board.place_piece(r[i],c[i],cpuval,oppval)

            if(board.full_board() or board.board_full()):
                score = board.evaluate(cpuval,oppval)
            else:
                row,col,score = minimize(board,alpha,beta,cpuval,oppval,depth - 1)
            
            if(score > alpha):
                alpha = score

            board = board2
            
            if maxscore == None or alpha > maxscore:
                maxscore = alpha
                maxrow = r[i]
                maxcol = c[i]
            
    return maxrow,maxcol,maxscore

#Minimizing function
def minimize(board,a,b,cpuval,oppval,depth):
    minscore = None
    minrow = None
    mincol = None
    alpha = a
    beta = b

    if(depth == 0):
        return minrow,mincol,board.evaluate(oppval,cpuval)
    
    r,c = board.get_open_spaces(oppval,cpuval)

    if(not r):
        return minrow,mincol,board.evaluate(oppval,cpuval)
    else:
        for i in range(0,len(r)):
            if(alpha > beta):
                break

            board2 = copy.deepcopy(board)
            board.place_piece(r[i],c[i],oppval,cpuval)
            
            if(board.full_board() or board.board_full()):
                score = board.evaluate(oppval,cpuval)
            else:
                row,col,score = maximize(board,alpha,beta,cpuval,oppval,depth - 1)

            if(score < beta):
                beta = score

            board = board2

            if minscore == None or beta < minscore:
                minscore = beta
                minrow = r[i]
                mincol = c[i]
    return minrow,mincol,minscore

##def main():
##    b1 = Kaustubh_Garimella()
##    b2 = Kaustubh_Garimella()
##    b = Kaustubh_Garimella()
##    b.PrintBoard()
##
##    Human = 'W'
##    CPU = 'B'
##    player = CPU
##    opp = Human
##    rowS = -1
##    colS = -1
##    rowC = -1
##    colC = -1
##    canPlayHuman = True
##    canPlayCPU = True
##   
##    #alternate between human's turn and CPU turn. if theres is no available move for one of the players, then
##    #it becomes their opponents turn again.
##    #if the board is full, the winner is announced
##    while( b.full_board()==False and (canPlayHuman or canPlayCPU)):
##        if player==CPU :
##            canPlayCPU = True
##            if b.all_pieces(player):
##                break
##            print("CPU")
##            rowC,colC = b1.play_square(rowS,colS,CPU,Human)
##            #print(b1.evaluate(CPU,Human))
##            if(rowC == -1 or colC == -1):
##                canPlayCPU = False
##                player = Human
##                opp = CPU
##                continue
##            else:
##                b.place_piece(rowC,colC,CPU,Human)
##                b.PrintBoard()
##                player = Human
##                opp = CPU
##
##        elif player==Human :
##            canPlayHuman = True
##            if b.all_pieces(player):
##                break
##            print("CPU")
##            rowS,colS = b2.play_square(rowC,colC,Human,CPU)
##            #print(b2.evaluate(Human,CPU))
##            if(rowS == -1 or colS == -1):
##                canPlayHuman = False
##                player = CPU
##                opp = Human
##                continue
##            else:
##                b.place_piece(rowS,colS,Human,CPU)
##                b.PrintBoard()
##                player = CPU
##                opp = Human
##            
##            
##    if( b.score(Human, CPU) > 0):
##        print("The winner is: "+ Human)
##    elif(b.score(Human, CPU) == 0):
##        print("The game is a draw")
##    else:
##        print("The winner is: " + CPU)
##main()
##            

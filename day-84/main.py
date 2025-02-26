import os
import platform


matrixGame = [ [-1 for j in range(3) ] for i in range(3)]
visualRep = ["O", "X"]
vertical = ["   ","   |"]

def clear_terminal():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def printMatrix(matrix):
    i = 0
    for row in matrix: 
        string = ""
        j = 0
        for elem in row: 
            j+=1
            if elem == -1: 
                string = string + "    " + vertical[j < 3]
                continue
            string = string + (f"   {visualRep[elem]}{vertical[j < 3]}")   
        print(string)
        i += 1
        if i !=3: 
            print("-----------------------")


def checkWin(playerMark, matrix): 
    win = [playerMark for i in range(3)]
    
    #First case
    temp = [matrix[i][0] for i in range (3)]
    if matrix[0] ==  win or temp == win: 
        return True
    
    #Second case
    temp = [matrix[i][2] for i in range (3)]
    if matrix[2] ==  win or temp == win: 
        return True
    
    #Third case
    matTemp = []
    matTemp.append([matrixGame[i][i]    for i in range(3)])
    matTemp.append([matrixGame[i][2-i]  for i in range(3)])
    matTemp.append([matrixGame[i][1]    for i in range(3)])
    matTemp.append(matrixGame[1])

    if win in matTemp:
        return True 
    
    return False

def selectPos(matrix): 
    while True: 
        try: 
            x = int(input("Enter a availabe row    (0-2): "))
            y = int(input("Enter a availabe column (0-2): "))

            if matrix[x][y] == -1: 
                return (x,y)
            else: 
                print("You must to select a available square")
        except: 
            print("You must to enter integer numbers in the range [0,2]")

def game(): 
    clear_terminal()
    i = 0
    print("Welcome to Tic Tac Toe!")
    playersMark = ['O', 'X']
    players = [0,1]
    moves = 0
    while True:
        print(f"It's {playersMark[i]}'s turn")
        printMatrix(matrixGame)
        pos = selectPos(matrixGame)
        matrixGame[pos[0]][pos[1]] = players[i]
        isWin = checkWin(players[i], matrixGame)
        if isWin: 
            clear_terminal()
            printMatrix(matrixGame)
            print(f"Yeiii! {playersMark[i]} won the game")
            break
        i+=1
        moves +=1

        if moves == 9: 
            clear_terminal()
            printMatrix(matrixGame)
            print("Tie :(")
            break
        if i == 2: 
            i = 0
        clear_terminal()

game()
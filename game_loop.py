#RANDOM SKAITLI

import random

def numGen (count = 5, min = 40000, max = 50000):
    
    validNum = [n for n in range(min, max + 1) if n % 60 == 0]
    return random.sample(validNum, count)

numbers = numGen()
print (numbers)



#GAME LOOP

def turnPlayer():

    move = input("move: ")
    return move

def turnAI():

    move = print("ai made a move") #placeholder
    return move

def gameLoop():
    gameOver = False

    while not gameOver:
        movePlayer = turnPlayer()
        

        if gameOver == True:
            break
        
        if movePlayer == "1234": #for testing
            break

        moveAI = turnAI()

gameLoop()        
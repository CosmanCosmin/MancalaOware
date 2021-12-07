import random

scores = [0, 0]
board = [4] * 12
playerTurn = random.randrange(0, 2)

while scores[0] < 25 and scores[1] < 25:
    print(board)
    print("Player 0 score: %d\nPlayer 1 score: %d" % (scores[0], scores[1]))
    print("Player %d. " % playerTurn, end="")
    if not playerTurn:
        print("Choose a spot between 0-5:")
    else:
        print("Choose a spot between 6-11:")
    spot = int(input())
    while not (6 * playerTurn <= spot <= 6 * playerTurn + 5):
        spot = int(input("Incorrect. Choose again:"))
    currentSpot = spot - 1
    while board[spot] > 0:
        if currentSpot < 0:
            currentSpot = 11
        if spot == currentSpot:
            currentSpot -= 1
        board[currentSpot] += 1
        if board[currentSpot] in [2, 3] and 6 * (1 - playerTurn) <= currentSpot <= 6 * (1 - playerTurn) + 5:
            scores[playerTurn] += board[currentSpot]
            board[currentSpot] = 0
        currentSpot -= 1
        board[spot] -= 1
    playerTurn = 1 - playerTurn
print(1 - playerTurn, " wins!")

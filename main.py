import random
import pygame


def play():
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


def drawBoard():
    pygame.init()
    pygame.display.set_caption("Mancala Oware Abapa")
    maxX, maxY = 612, 612
    pointsArray = [[maxX / 2, maxY / 6], [2 * maxX / 3, 3 * maxY / 14],
                   [7 * maxX / 9, maxY / 3], [5 * maxX / 6, maxY / 2],
                   [7 * maxX / 9, 2 * maxY / 3], [2 * maxX / 3, 11 * maxY / 14],
                   [maxX / 2, 5 * maxY / 6], [maxX / 3, 11 * maxY / 14],
                   [2 * maxX / 9, 2 * maxY / 3], [maxX / 6, maxY / 2],
                   [2 * maxX / 9, maxY / 3], [maxX / 3, 3 * maxY / 14]]
    screen = pygame.display.set_mode((maxX, maxY))
    backgroundImage = pygame.image.load("tree_trunk.jpg")
    screen.blit(backgroundImage, (0, 0))
    pointsDrawn = 0
    for x in pointsArray:
        pygame.draw.circle(screen, pygame.Color(220, 20, 60) if pointsDrawn < 6 else pygame.Color(0, 0, 139),
                           (x[0], x[1]), 33, width=5)
        pointsDrawn += 1
    pygame.display.flip()


def main():
    drawBoard()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == '__main__':
    main()

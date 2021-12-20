import random
import pygame
from pygame.examples.joystick import BLACK


def getPoints(maxX, maxY):
    return [[maxX // 2, maxY // 6], [2 * maxX // 3, 3 * maxY // 14],
            [7 * maxX // 9, maxY // 3], [5 * maxX // 6, maxY // 2],
            [7 * maxX // 9, 2 * maxY // 3], [2 * maxX // 3, 11 * maxY // 14],
            [maxX // 2, 5 * maxY // 6], [maxX // 3, 11 * maxY // 14],
            [2 * maxX // 9, 2 * maxY // 3], [maxX // 6, maxY // 2],
            [2 * maxX // 9, maxY // 3], [maxX // 3, 3 * maxY // 14]]


def drawBoard(maxX, maxY, pointsArray):
    pygame.init()
    pygame.display.set_caption("Mancala Oware Abapa")
    screen = pygame.display.set_mode((maxX, maxY))
    backgroundImage = pygame.image.load("tree_trunk.jpg")
    screen.blit(backgroundImage, (0, 0))
    pointsDrawn = 0
    circles = []
    for x in pointsArray:
        circles.append(
            pygame.draw.circle(screen, pygame.Color(220, 20, 60) if pointsDrawn < 6 else pygame.Color(0, 0, 139),
                               (x[0], x[1]), 33, width=5))
        pointsDrawn += 1
    pygame.display.flip()
    return circles, screen


def drawNumber(num, point, screen):
    font = pygame.font.SysFont('ComicSans', 16)
    image = font.render(str(num), True, BLACK).convert_alpha()
    screen.blit(image, (point[0], point[1]))


def updateBoard(points, board, screen):
    for point, value in zip(points, board):
        drawNumber(value, point, screen)
    pygame.display.flip()


def sow(board, index, playerTurn):
    score = 0
    currentSpot = index - 1
    while board[index] > 0:
        if currentSpot < 0:
            currentSpot = 11
        if index == currentSpot:
            currentSpot -= 1
        board[currentSpot] += 1
        if board[currentSpot] in [2, 3] and 6 * (1 - playerTurn) <= currentSpot <= 6 * (1 - playerTurn) + 5:
            score += board[currentSpot]
            board[currentSpot] = 0
        currentSpot -= 1
        board[index] -= 1
    return score


def main():
    maxX, maxY = 612, 612
    points = getPoints(maxX, maxY)
    board = [4] * 12
    circles, screen = drawBoard(maxX, maxY, points)
    updateBoard(points, board, screen)
    running = True

    playerTurn = random.randrange(0, 2)
    scores = [0, 0]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked = [circles.index(c) for c in circles if c.collidepoint(pos)]
                if clicked and (0 <= clicked[0] < 6 and playerTurn == 0) or (6 <= clicked[0] < 12 and playerTurn == 1):
                    scores[playerTurn] += sow(board, clicked[0], playerTurn)
                    circles, screen = drawBoard(maxX, maxY, points)
                    updateBoard(points, board, screen)
                    playerTurn = 1 - playerTurn
            if event.type == pygame.QUIT:
                running = False


if __name__ == '__main__':
    main()

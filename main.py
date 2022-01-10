import random
import sys

import pygame
from copy import deepcopy


def getPoints(maxX, maxY):
    return [[maxX // 2, maxY // 6], [2 * maxX // 3, 3 * maxY // 14],
            [7 * maxX // 9, maxY // 3], [5 * maxX // 6, maxY // 2],
            [7 * maxX // 9, 2 * maxY // 3], [2 * maxX // 3, 11 * maxY // 14],
            [maxX // 2, 5 * maxY // 6], [maxX // 3, 11 * maxY // 14],
            [2 * maxX // 9, 2 * maxY // 3], [maxX // 6, maxY // 2],
            [2 * maxX // 9, maxY // 3], [maxX // 3, 3 * maxY // 14]]


def drawBoard(maxX, maxY, pointsArray, playerTurn):
    pygame.init()
    pygame.display.set_caption("Mancala Oware Abapa")
    screen = pygame.display.set_mode((maxX, maxY))
    backgroundImage = pygame.image.load("tree_trunk.jpg")
    screen.blit(backgroundImage, (0, 0))
    pointsDrawn = 0
    circles = []
    pygame.draw.circle(screen, pygame.Color(220, 20, 60) if not playerTurn else pygame.Color(0, 0, 139),
                       (maxX / 2, maxY / 2), 33)
    for x in pointsArray:
        circles.append(
            pygame.draw.circle(screen, pygame.Color(220, 20, 60) if pointsDrawn < 6 else pygame.Color(0, 0, 139),
                               (x[0], x[1]), 33, width=5))
        pointsDrawn += 1
    pygame.display.flip()
    return circles


def drawNumber(num, point, color, fontSize):
    font = pygame.font.SysFont('ComicSans', fontSize)
    image = font.render(str(num), True, color).convert_alpha()
    pygame.display.get_surface().blit(image, (point[0], point[1]))


def updateBoard(points, board, scores):
    for point, value in zip(points, board):
        drawNumber(value, point, (0, 0, 0), 16)
    x, y = pygame.display.get_surface().get_size()
    drawNumber(scores[1], (x / 2 - 80, y / 2 - 32), (0, 0, 255), 32)
    drawNumber(scores[0], (x / 2 + 48, y / 2 - 32), (255, 0, 0), 32)
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
    return board, score


def initiateGame():
    return random.randrange(0, 2), [0, 0], [4] * 12


def lookAhead(board, index, playerTurn):
    board, _ = sow(board, index, playerTurn)
    return sum(board[0:6]) != 0 if playerTurn == 1 else sum(board[6:12]) != 0


def play():
    maxX, maxY = 612, 612
    points = getPoints(maxX, maxY)
    running = True
    playerTurn, scores, board = initiateGame()
    circles = drawBoard(maxX, maxY, points, playerTurn)
    updateBoard(points, board, scores)
    clickable = True
    click = False
    while running:
        for event in pygame.event.get():
            if click:
                pos = pygame.mouse.get_pos()
                clicked = [circles.index(c) for c in circles if c.collidepoint(pos)]
                if clicked:
                    if ((0 <= clicked[0] < 6 and playerTurn == 0) or (6 <= clicked[0] < 12 and playerTurn == 1)) \
                            and board[clicked[0]] and lookAhead(deepcopy(board), clicked[0], playerTurn):
                        board, score = sow(deepcopy(board), clicked[0], playerTurn)
                        scores[playerTurn] += score
                        playerTurn = 1 - playerTurn
                        circles = drawBoard(maxX, maxY, points, playerTurn)
                        updateBoard(points, board, scores)
                        if scores[0] >= 25 or scores[1] >= 25:
                            clickable = False
            click = False
            if event.type == pygame.MOUSEBUTTONDOWN and clickable:
                if event.button == 1:
                    click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


class Button:
    def __init__(self, image, position, callback):
        self.image = image
        self.rect = image.get_rect(topleft=position)
        self.callback = callback

    def onClick(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


def playWithAI():
    maxX, maxY = 612, 612
    points = getPoints(maxX, maxY)
    running = True
    playerTurn, scores, board = initiateGame()
    circles = drawBoard(maxX, maxY, points, playerTurn)
    updateBoard(points, board, scores)
    clickable = True
    click = False
    while running:
        for event in pygame.event.get():
            if click:
                pos = pygame.mouse.get_pos()
                clicked = [circles.index(c) for c in circles if c.collidepoint(pos)]
                if playerTurn == 1:
                    spot = random.randint(6, 11)
                    while not board[spot] or not lookAhead(deepcopy(board), spot, playerTurn):
                        spot = random.randint(6, 11)
                    board, score = sow(deepcopy(board), spot, playerTurn)
                    scores[playerTurn] += score
                    playerTurn = 0
                    circles = drawBoard(maxX, maxY, points, playerTurn)
                    updateBoard(points, board, scores)

                if clicked and playerTurn == 0:
                    if (0 <= clicked[0] < 6) and board[clicked[0]] and lookAhead(deepcopy(board), clicked[0],
                                                                                 playerTurn):
                        board, score = sow(deepcopy(board), clicked[0], playerTurn)
                        scores[playerTurn] += score
                        playerTurn = 1
                        circles = drawBoard(maxX, maxY, points, playerTurn)
                        updateBoard(points, board, scores)
                if scores[0] >= 25 or scores[1] >= 25:
                    clickable = False
            click = False
            if event.type == pygame.MOUSEBUTTONDOWN and clickable:
                if event.button == 1:
                    click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def main():
    running = True
    pygame.init()
    pygame.display.set_caption("Mancala Oware Abapa")
    backgroundImage = pygame.image.load("main_menu.jpg")
    buttonImage = pygame.image.load("main_button.jpg")

    while running:
        screen = pygame.display.set_mode((612, 612))
        screen.blit(backgroundImage, (0, 0))
        twoPlayerButton = Button(buttonImage, (260, 220), play)
        playWithAIButton = Button(buttonImage, (260, 320), playWithAI)
        screen.blit(twoPlayerButton.image, twoPlayerButton.rect)
        screen.blit(playWithAIButton.image, playWithAIButton.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                twoPlayerButton.onClick(event)
                playWithAIButton.onClick(event)
        pygame.display.update()


if __name__ == '__main__':
    main()

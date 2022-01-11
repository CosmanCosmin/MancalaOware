import random
import sys
from copy import deepcopy

import pygame

from button import Button


def getPoints(maxX, maxY):
    """
    Return the center points for the circles corresponding to the playing spots.

    Keyword arguments:
    maxX -- the screens width
    maxY -- the screens height
    """
    return [[maxX // 2, maxY // 6], [2 * maxX // 3, 3 * maxY // 14],
            [7 * maxX // 9, maxY // 3], [5 * maxX // 6, maxY // 2],
            [7 * maxX // 9, 2 * maxY // 3], [2 * maxX // 3, 11 * maxY // 14],
            [maxX // 2, 5 * maxY // 6], [maxX // 3, 11 * maxY // 14],
            [2 * maxX // 9, 2 * maxY // 3], [maxX // 6, maxY // 2],
            [2 * maxX // 9, maxY // 3], [maxX // 3, 3 * maxY // 14]]


def drawBoard(maxX, maxY, pointsArray, playerTurn):
    """
    Draw the background image and all the circles on the game board and return the circle objects.

    Keyword arguments:
    maxX -- the screens width
    maxY -- the screens height
    pointsArray -- the centers of the circles to be drawn
    playerTurn -- whose turn it is in the game
    """
    pygame.init()
    pygame.display.set_caption("Mancala Oware Abapa")
    screen = pygame.display.set_mode((maxX, maxY))
    backgroundImage = pygame.image.load("resources/tree_trunk.jpg")
    screen.blit(backgroundImage, (0, 0))
    pointsDrawn = 0
    circles = []
    RED = pygame.Color(220, 20, 60)
    BLUE = pygame.Color(0, 0, 139)
    pygame.draw.circle(screen, RED if not playerTurn else BLUE,
                       (maxX / 2, maxY / 2), 33)
    for x in pointsArray:
        circles.append(
            pygame.draw.circle(screen, RED if pointsDrawn < 6 else BLUE,
                               (x[0], x[1]), 33, width=5))
        pointsDrawn += 1
    pygame.display.flip()
    return circles


def drawText(text, point, color, fontSize):
    """
    Write text on the screen at certain coordinates.

    :param text: text to be written
    :param point: where the text should be written as (x, y) coordinates
    :param color: color of the text
    :param fontSize: size of the font
    """
    font = pygame.font.SysFont('ComicSans', fontSize)
    image = font.render(str(text), True, color).convert_alpha()
    pygame.display.get_surface().blit(image, (point[0], point[1]))


def updateBoard(points, board, scores):
    """
    Update the values of all spots on the board and the player's scores.

    :param points: the centers of the circles
    :param board: the array of values for each circle
    :param scores: the scores of each player
    """
    for point, value in zip(points, board):
        drawText(value, point, (0, 0, 0), 16)
    x, y = pygame.display.get_surface().get_size()
    drawText(scores[1], (x / 2 - 80, y / 2 - 32), (0, 0, 255), 32)
    drawText(scores[0], (x / 2 + 48, y / 2 - 32), (255, 0, 0), 32)
    pygame.display.flip()


def sow(board, index, playerTurn):
    """
    Move the values from the selected spot to n other counter-clockwise spots, remove them from those spots and add to
    the players score if there's 2 or 3 remaining.

    :param board: the array of values for each spot
    :param index: the spot chosen by the current player as their move
    :param playerTurn: whose turn it is in the game
    :return: the array of updated values and the scores of each player
    """
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
    """
    Return the needed pre-requisites to start a game.

    :return: the player who starts as in a number between 0 and 1, the scores of each player, the array of values for
    each circle
    """
    return random.randrange(0, 2), [0, 0], [4] * 12


def lookAhead(board, index, playerTurn):
    """
    Return a boolean that represents if the move makes it so the next player doesn't have a possible move.

    :param board: the array of values for each spot
    :param index: the spot chosen by the current player
    :param playerTurn: whose turn it is in the game
    :return: a boolean value that represents if there's a possible move or not for the next player
    """
    board, _ = sow(board, index, playerTurn)
    return sum(board[0:6]) != 0 if playerTurn == 1 else sum(board[6:12]) != 0


def victory(playerTurn):
    """
    Print the "victory screen".

    :param playerTurn: whose turn it is in the game
    """
    drawText("Game over", (230, 230), (0, 0, 0), 32)
    playerTurn = "Red" if playerTurn == 0 else "Blue"
    drawText(f"{playerTurn} wins!", (240, 330), (0, 0, 0), 32)


def play():
    """Infinitely loop and check for events such as mouse clicks so the game can be played by two players."""
    maxX, maxY = 612, 612
    points = getPoints(maxX, maxY)
    running = True
    playerTurn, scores, board = initiateGame()
    circles = drawBoard(maxX, maxY, points, playerTurn)
    updateBoard(points, board, scores)
    clickable = True
    click = False
    while running:
        if not clickable:
            pygame.display.flip()
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
                        if scores[0] >= 1 or scores[1] >= 1:
                            clickable = False
                            victory(1 - playerTurn)
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


def playWithAI():
    """Infinitely loop and check for events such as mouse clicks so the game can be played by a player vs an AI."""
    maxX, maxY = 612, 612
    points = getPoints(maxX, maxY)
    running = True
    playerTurn, scores, board = initiateGame()
    circles = drawBoard(maxX, maxY, points, playerTurn)
    updateBoard(points, board, scores)
    clickable = True
    click = False
    while running:
        if not clickable:
            pygame.display.flip()
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
                if scores[0] >= 1 or scores[1] >= 1:
                    clickable = False
                    victory(1 - playerTurn)
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
    """Print the main screen from where you can select either PvP or PvAI."""
    running = True
    pygame.init()
    pygame.display.set_caption("Mancala Oware Abapa")
    backgroundImage = pygame.image.load("resources/main_menu.jpg")
    buttonImage = pygame.image.load("resources/main_button.jpg")

    while running:
        screen = pygame.display.set_mode((612, 612))
        screen.blit(backgroundImage, (0, 0))
        twoPlayerButton = Button(buttonImage, (260, 220), play)
        playWithAIButton = Button(buttonImage, (260, 320), playWithAI)
        screen.blit(twoPlayerButton.image, twoPlayerButton.rect)
        screen.blit(playWithAIButton.image, playWithAIButton.rect)
        drawText("PvP", (310, 220), (0, 0, 0), 32)
        drawText("P vs AI", (280, 320), (0, 0, 0), 32)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                twoPlayerButton.onClick(event)
                playWithAIButton.onClick(event)
        pygame.display.update()


if __name__ == '__main__':
    main()

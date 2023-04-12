import pygame
import random
import sys

word = ''
buttons = []
guess = []
hacked = []
virus = 0
BLACK = (0,0,0)
WHITE = (255,255,255)

pygame.init()

screen=pygame.display.set_mode((700,500))
pygame.display.set_caption('Save The PC')

med = pygame.font.SysFont("source code pro", 30)
large = pygame.font.SysFont('source code pro', 40)
small = pygame.font.SysFont('source code pro', 20)


def start():
    screen.fill(WHITE)
    pic = pygame.image.load(f"intro.png")
    screen.blit(pic, (330 - pic.get_width()/2 + 20, 90))
    pygame.display.update()


def inGame():
    screen.fill(WHITE)
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(screen, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(screen, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2)
            label = med.render(chr(buttons[i][5]), 1, BLACK)
            screen.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = layout(word, guess)
    label1 = large.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    
    screen.blit(label1,(350 - length/2, 400))

    pic = hacked[virus]
    screen.blit(pic, (325 - pic.get_width()/2 + 20, 150))
    pygame.display.update()

def layout(word, guess=[]):
    spaces = ''
    letters = guess
    for x in range(len(word)):
        if word[x] != ' ':
            spaces += '_ '
            for i in range(len(letters)):
                if word[x].upper() == letters[i]:
                    spaces = spaces[:-2]
                    spaces += word[x].upper() + ' '
        elif word[x] == ' ':
            spaces += ' '
    return spaces

def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None

def getWord():
    file = open('words.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)
    return f[i][:-1]

def found(guess):
    if guess.lower() not in word.lower():
        return True
    else:
        return False

def end(winner=False):

    reset = True
    inGame()
    pygame.time.delay(1000)
    screen.fill(WHITE)

    if winner == True:
        result = large.render('You Saved the PC !! ', 1, BLACK)
    else:
        result = large.render('You Lost all the Files !!', 1, BLACK)

    screen.blit(med.render(word.upper(), 1, BLACK), (350 - med.render(word.upper(), 1, BLACK).get_width()/2, 295))
    screen.blit(med.render('The word was : ', 1, BLACK), (350 - med.render('The word was : ', 1, BLACK).get_width()/2, 245))
    screen.blit(result, (350- result.get_width() / 2, 90))
    screen.blit(small.render('[ Press any Key to Play Again ]', 1, BLACK), (350- small.render('[ Press any Key to Play Again ]', 1, BLACK).get_width() / 2, 160))
    screen.blit(pygame.image.load(f"funfact.png"), (330 - pygame.image.load(f"funfact.png").get_width()/2 + 20, 380))
    pygame.display.update()
    while reset:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                reset = False
    reset_game()

def reset_game():
    global virus
    global guess
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True
    virus = 0
    guess = []
    word = getWord()


def main():
    global virus
    global guess
    global word
    for i in range(7):
        image = pygame.image.load(f"V{i}.png")
        hacked.append(image)

    inc = round(700 / 13)
    for i in range(26):
        if i < 13:
            y = 40
            x = 25 + (inc * i)
        else:
            x = 25 + (inc * (i - 13))
            y = 85
        buttons.append([(0, 253, 200), x, y, 20, True, 65 + i])

    word = getWord() 
    run = True

    start()
    pygame.time.delay(6000)
    while run:
        inGame()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                letter = buttonHit(clickPos[0], clickPos[1])
                if letter != None:
                    guess.append(chr(letter))
                    buttons[letter - 65][4] = False
                    if found(chr(letter)):
                        if virus != 5:
                            virus += 1
                        else:
                            end()
                    else:
                        print(layout(word, guess))
                        if layout(word, guess).count('_') == 0:
                            end(True)

    pygame.quit()

if __name__ == "__main__":
    main()
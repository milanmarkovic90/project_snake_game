import pygame
from pygame.locals import *
import time
import random

# Konvertierung in OOP (Klassen und Objekten)

# Variabeln kreieren für Blockgrösse und Hintergrundfarbe
SIZE = 40
BACKGROUND_COLOR = 110, 110, 5

# Klasse "Apfel"
class Apple:

    # Apfel importieren
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.image = pygame.transform.scale(self.image, (40, 40)) #EVTL. OBSOLET
        self.x = SIZE*3
        self.y = SIZE*3
    
    # Apfel zeichnen
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()
    
    # Apfel bewegen bei Kollision
    def move(self):
        self.x = random.randint(0,24)*SIZE
        self.y = random.randint(0,19)*SIZE

# Klasse "Schlange"
class Snake:

    # Spielfenster bauen und Schlange importieren
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.block = pygame.transform.scale(self.block, (40, 40)) #EVTL. OBSOLET
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    # Schlange zeichnen
    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    # Schlange bewegen
    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'   

    # Schlange bei Kollision mit Apfel vergrössern
    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    # Bewegung implementieren
    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
         
        self.draw()

# Klasse "Spiel"
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    # Kollision Schlange mit Apfel implementieren
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    # Spielsound implementieren
    def play_background_music(self):
        pygame.mixer.music.load("resources/music.mp3")
        pygame.mixer.music.play()
    
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    # Hintergrundbild einfügen
    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))

    # Spielfunktion modularisieren
    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        
        # Schlange isst Apfel
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # Schlange kollidiert mit sich selbst
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game Over"

        # Schlange kollidiert mit Spielrand
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound("game over")
            raise "Game Over"

    # Punktezahl anzeigen
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800,10))

    # Game Over Text anzeigen
    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial',30)
        linel = font.render(f"Game Over! Your Score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(linel, (200,300))
        linel2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(linel2, (200,350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    # Neustart einrichten
    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    # Autostart einrichten
    def run(self):
        running = True
        pause = False

        # Main Event Loop initialisieren
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:

                    # Tastenbefehle programmieren
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)

# Spiel starten
if __name__ == "__main__":
    game = Game()
    game.run()

# Learnings:
# 1.    Wenn bei Programmieren etwas mehrfach benutzt wird, ist es besser, eine Variabel zu kreeiren
# 1a.   Oder auch eine Funktion.
# 2.    Objektorientiertes Programmieren: Macht Sinn, wenn der Code besonders lang ist (> 30 Zeilen).
#       Macht es einfacher für eine Drittperson zu verstehen, was gemacht wurde.
# 3.    Sämtliche UI Änderungen immer am Schluss mit pygame.display.flip() beenden. -> Für das Refreshing des Screens.
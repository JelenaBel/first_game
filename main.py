import pygame
import random
import math


class MyGame:
    def __init__(self):
        pygame.init()
        self.t = 0
        self.lives = 10
        self.window = pygame.display.set_mode((640, 510))
        self.window.fill((255, 255, 255))
        self.game_font = pygame.font.SysFont("Arial", 24)

        self.load_images()

        pygame.display.set_caption("Money, money, money...")
        self.robot_x = 0
        self.robot_y = 480 - self.images[4].get_height()
        self.coordinates = {}
        self.coordinates_hirvio = {}
        self.level = 1
        self.clock = pygame.time.Clock()
        self.gameover = False
        self.new_game()
        self.main_loop()

    def load_images(self):
        self.images = []
        robot_2 = pygame.image.load("robo.png").convert_alpha()
        robot_2 = pygame.transform.smoothscale(robot_2, (25, 40))
        kolikko = pygame.image.load("kolikko.png").convert_alpha()
        kolikko = pygame.transform.smoothscale(kolikko, (25, 40))
        hirvio = pygame.image.load("hirvio.png").convert_alpha()
        hirvio = pygame.transform.smoothscale(hirvio, (25, 40))
        robot = pygame.image.load("robo.png")
        kivi = pygame.image.load("kolikko.png")

        self.images.append(kolikko)
        self.images.append(robot_2)
        self.images.append(kolikko)
        self.images.append(hirvio)
        self.images.append(robot)
        self.images.append(kivi)

    def new_game(self):

        self.coin_rain()
        self.hirvio_rain()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                robot = self.images[4]
                target_x = event.pos[0] - robot.get_width()
                if target_x < 0:
                    target_x = 0
                elif target_x > 640 - robot.get_width():
                    target_x = 640 - robot.get_width()
                target_y = 480 - robot.get_height()
                self.robot_x = target_x
                self.robot_y = target_y
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    self.new_game()
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.QUIT:
                exit()

    def coin_rain(self):
        y_old = 0

        for i in range(0, 400):
            x_k = random.randint(0, (640 - self.images[5].get_width()))
            n = random.randint(-50, -1)
            if i > 30:
                m = i / 2
            else:
                m = i
            y_k = m * 10 * n
            print((y_k * (-1)) - (y_old * (-1)))
            if abs((y_k * (-1)) - (y_old * (-1))) < 1000:
                y_k = y_k - 1000

            coor: tuple
            coor = (x_k, y_k)
            name = 'kivi' + str(i)
            self.coordinates[name] = coor
            y_old = y_k

    def hirvio_rain(self):
        # creating hirvio rain
        y_old = 0
        for j in range(0, 200):
            x_k = random.randint(0, 640 - self.images[5].get_width())
            n = random.randint(-50, -1)
            if j > 30:
                m = j / 2
            else:
                m = j
                y_k = m * 10 * n * j

            if abs((y_k * (-1)) - (y_old * (-1))) < 500:
                y_k = y_k - 500

            coor: tuple
            coor = (x_k, y_k)
            name = 'hirvio' + str(j)
            self.coordinates_hirvio[name] = coor
            y_old = y_k

    def main_loop(self):
        while True:
            self.check_events()
            self.clock_is_ticking()
            pygame.display.flip()

    def clock_is_ticking(self):

        if self.level == 1:
            robot = self.images[4]
            robot_w = robot.get_width()
            robot_h = robot.get_height()
            kivi = self.images[5]
            kivi_w = kivi.get_width()
            kivi_h = kivi.get_height()

            hirvio = self.images[3]

            # moving the rain
            for name, value in self.coordinates.items():
                x = value[0]
                y = value[1] + 1
                coord: tuple
                coord = (x, y)
                self.coordinates[name] = coord

                # moving the hirvio
            for name1, value1 in self.coordinates_hirvio.items():
                x1 = value1[0]
                y1 = value1[1] + 1.5
                coord1: tuple
                coord1 = (x1, y1)
                self.coordinates_hirvio[name1] = coord1
        self.window.fill((255, 255, 255))
        self.text1 = self.game_font.render(f"Pisteet: {self.t}", True, (0, 0, 0))
        self.text2 = self.game_font.render(f"Lives: {self.lives}", True, (0, 0, 0))
        pygame.draw.rect(self.window, (211, 211, 211), (0, 480, 640, 30))
        game_text = self.game_font.render("Press g = new game", True, (255, 0, 0))
        number = game_text.get_width()
        self.window.blit(game_text, ((640 / 2) - number - 20, 480))

        game_text = self.game_font.render("Esc = exit game", True, (255, 0, 0))
        self.window.blit(game_text, ((640 / 2) + 20, 480))
        self.window.blit(self.text1, (480, 10))
        self.window.blit(self.text2, (480, 30))
        self.window.blit(robot, (self.robot_x, self.robot_y))
        if self.gameover == False:
            for kivet, place in self.coordinates.items():
                self.window.blit(kivi, (place[0], place[1]))
            for hirvi, paikka in self.coordinates_hirvio.items():
                self.window.blit(hirvio, (paikka[0], paikka[1]))
        self.checking()
        if self.t >= 150:

            game_text = self.game_font.render("Congratulations, you solved the game!", True, (255, 0, 0))
            game_text_x = 320 - game_text.get_width() / 2
            game_text_y = 240 - game_text.get_height() / 2

            self.window.blit(game_text, (game_text_x, game_text_y))
            self.gameover = True

        elif self.lives == 0:

            game_text = self.game_font.render("Sorry, you lose. G - new game", True, (255, 0, 0))
            game_text_x = 320 - game_text.get_width() / 2
            game_text_y = 240 - game_text.get_height() / 2
            pygame.draw.rect(self.window, (0, 0, 0),
                             (game_text_x, game_text_y, game_text.get_width(), game_text.get_height()))
            self.window.blit(game_text, (game_text_x, game_text_y))

            self.gameover = True

        else:
            pygame.display.flip()
            self.clock.tick(120)

    def checking(self):
        robot = self.images[4]
        kivi = self.images[5]
        hirvio = self.images[3]

        for kivet, place in self.coordinates.items():
            if self.gameover == True:
                break
            if self.robot_y == int(place[1]) + kivi.get_height() and self.robot_x + int(robot.get_width()) >= int(
                    place[0]) and int(place[0]) + kivi.get_width() >= self.robot_x \
                    and place[1] + kivi.get_height() != 480:
                self.t = self.t + 1
                new_coor = (1000, 1000)
                self.coordinates[kivet] = new_coor
            elif self.robot_y <= int(place[1]) + kivi.get_height() and self.robot_x + int(robot.get_width()) >= int(
                    place[0]) and int(place[0]) + kivi.get_width() >= self.robot_x and place[
                1] + kivi.get_height() != 480:
                self.t = self.t + 1
                new_coor = (1000, 1000)
                self.coordinates[kivet] = new_coor

        for hirvi, paikka in self.coordinates_hirvio.items():
            if self.gameover == True:
                break
            if self.robot_y == int(paikka[1] + hirvio.get_height()) and self.robot_x + int(robot.get_width()) >= int(
                    paikka[0]) and int(paikka[0]) + hirvio.get_width() >= self.robot_x and paikka[
                1] + hirvio.get_height() < 480:
                self.lives = self.lives - 1
                new_coor1 = (1000, 1000)
                self.coordinates_hirvio[hirvi] = new_coor1
            elif self.robot_y <= int(paikka[1]) + hirvio.get_height() and self.robot_x + int(robot.get_width()) >= int(
                    paikka[0]) and int(paikka[0]) + hirvio.get_width() >= self.robot_x and paikka[
                1] + hirvio.get_height() < 480:
                self.lives = self.lives - 1
                new_coor1 = (1000, 1000)
                self.coordinates_hirvio[hirvi] = new_coor1

        if self.lives == 0 or self.t >= 150:
            self.gameover = True


if __name__ == "__main__":
    MyGame()

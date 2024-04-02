import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración global
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
LIME = (191, 255, 0)
PINK = (255, 192, 203)
GREY = (128, 128, 128)
NAVY = (0, 0, 128)
TEAL = (0, 128, 128)

# Asegúrate de que el modo de video esté configurado antes de cargar la imagen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dispara y Esquiva")

# Carga y escala la imagen de fondo para que se ajuste exactamente a la pantalla
background_image = pygame.image.load('universe.jpg').convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dispara y Esquiva")
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.obstacles = []
        self.projectiles = []
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.obstacle_timer = 0
        self.obstacle_interval = 75  # Ajusta esto según quieras que los obstáculos aparezcan más o menos frecuentemente

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        if keys[pygame.K_UP]:
            self.player.move_up()
        if keys[pygame.K_DOWN]:
            self.player.move_down()
        if keys[pygame.K_SPACE]:
            self.player.shoot(self.projectiles)

    def update(self):

        # Obtener el estado actual del teclado
        keys = pygame.key.get_pressed()

        # Mover el jugador a la izquierda o a la derecha según la tecla presionada
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        # Actualizar la posición de los proyectiles y remover los que salen de la pantalla
        for projectile in self.projectiles[:]:
            projectile.move()
            if projectile.y < 0:  # Si el proyectil sale de la pantalla
                self.projectiles.remove(projectile)

        # Actualizar la posición de los obstáculos
        for obstacle in self.obstacles[:]:
            obstacle.move()
            if obstacle.off_screen(SCREEN_HEIGHT):  # Si el obstáculo sale de la pantalla
                self.obstacles.remove(obstacle)

        # En el método update de Game, después de mover los obstáculos
        for obstacle in self.obstacles[:]:
            obstacle.move()
            # Probabilidad aleatoria de que el obstáculo dispare
            if random.randint(0, 100) < 5:  # Ajusta este valor como veas necesario
                obstacle.shoot(self.projectiles)

        # Comprobar colisiones entre proyectiles y obstáculos
        for projectile in self.projectiles[:]:
            for obstacle in self.obstacles[:]:
                if projectile.x < obstacle.x + obstacle.width and \
                        projectile.x + projectile.width > obstacle.x and \
                        projectile.y < obstacle.y + obstacle.height and \
                        projectile.y + projectile.height > obstacle.y:
                    self.projectiles.remove(projectile)
                    self.obstacles.remove(obstacle)
                    self.score += 1  # Aumentar puntuación por cada obstáculo destruido
                    break  # Salir del bucle interno para evitar errores de modificación de la lista durante la iteración
        # En Game.update, después de actualizar la posición de los proyectiles
        for projectile in self.projectiles[:]:
            projectile.move()
            # Si el proyectil es enemigo y golpea al jugador
            if projectile.enemy and self.player.x < projectile.x + projectile.width and \
                    self.player.x + self.player.width > projectile.x and \
                    self.player.y < projectile.y + projectile.height and \
                    self.player.y + self.player.height > projectile.y:
                self.show_game_over_screen()  # Mostrar pantalla de Game Over

        # Comprobar colisiones entre el jugador y los obstáculos
        for obstacle in self.obstacles:
            if self.player.x < obstacle.x + obstacle.width and \
                    self.player.x + self.player.width > obstacle.x and \
                    self.player.y < obstacle.y + obstacle.height and \
                    self.player.y + self.player.height > obstacle.y:
                self.show_game_over_screen()

        # Generación periódica de obstáculos
        self.obstacle_timer += 1
        if self.obstacle_timer >= self.obstacle_interval:
            self.obstacles.append(Obstacle(random.randint(0, SCREEN_WIDTH - 40), -40))
            self.obstacle_timer = 0

    def draw(self):
        # Llenar el fondo de la pantalla con un color
        # self.screen.fill(BLACK)
        self.screen.blit(background_image, (0, 0))

        # Dibujar el jugador
        self.player.draw(self.screen)

        # Dibujar cada uno de los proyectiles
        for projectile in self.projectiles:
            projectile.draw(self.screen)

        # Dibujar cada uno de los obstáculos
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Preparar el fondo blanco para el score
        padding = 5  # Ajusta el padding según necesites
        score_text = self.font.render(f"Puntuación: {self.score}", True, GREEN)
        score_bg_size = score_text.get_size()
        score_bg_rect = pygame.Rect(5, 5, score_bg_size[0] + padding * 2, score_bg_size[1] + padding * 2)

        # Dibujar el fondo blanco para la puntuación
        self.screen.fill(BLACK, score_bg_rect)

        # Dibujar la puntuación en verde sobre el fondo blanco
        self.screen.blit(score_text, (10, 10))

        # Actualizar la pantalla
        pygame.display.flip()

    def show_game_over_screen(self):
        self.screen.fill(BLACK)  # Fondo de la pantalla de Game Over

        # Crea una fuente más grande para el mensaje de Game Over
        game_over_font = pygame.font.Font(None, 80)  # Aumenta el segundo parámetro para un tamaño de fuente más grande
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        self.screen.blit(game_over_text, game_over_rect)

        # Mostrar puntuación (puedes usar la fuente regular para esto o también hacerla más grande)
        score_text = self.font.render(f"Puntuación final: {self.score}", True, GREEN)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(score_text, score_rect)

        # Opciones de Jugar de Nuevo o Salir (ajusta el tamaño de la fuente según sea necesario)
        play_again_text = self.font.render("Jugar de Nuevo (J)", True, GREEN)
        play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        self.screen.blit(play_again_text, play_again_rect)

        exit_text = self.font.render("Salir (S)", True, GREEN)
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100))
        self.screen.blit(exit_text, exit_rect)

        pygame.display.flip()  # Actualizar la pantalla

        # Esperar a que el jugador elija una opción
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)  # Salir completamente del programa
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_j:  # Jugar de Nuevo
                        waiting = False
                        self.reset_game()  # Restablecer el juego para jugar de nuevo
                    elif event.key == pygame.K_s:  # Salir del juego
                        pygame.quit()
                        exit(0)

    def reset_game(self):
        self.obstacles = []
        self.projectiles = []
        self.score = 0
        self.player = Player()  # Recrear el jugador para restablecer su posición y estado
        self.obstacle_timer = 0
        self.running = True  # Asegurarse de que el bucle del juego continúe corriendo
        self.run()  # Iniciar el juego de nuevo


class Player:
    def __init__(self):
        self.width = 50  # Aumentar el tamaño de la nave
        self.height = 50  # Aumentar el tamaño de la nave
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.speed = 8
        self.color = BLUE
        self.shoot_delay = 250  # Tiempo en milisegundos entre disparos
        self.last_shot = pygame.time.get_ticks()

    def move_left(self):
        self.x = max(0, self.x - self.speed)

    def move_right(self):
        self.x = min(SCREEN_WIDTH - self.width, self.x + self.speed)

    def move_up(self):
        self.y = max(0, self.y - self.speed)  # Asegura que no salga por arriba de la pantalla

    def move_down(self):
        self.y = min(SCREEN_HEIGHT - self.height, self.y + self.speed)  # Asegura que no salga por abajo de la pantalla

    def shoot(self, projectiles):
        # Verifica si ha pasado suficiente tiempo desde el último disparo
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now  # Actualiza el tiempo del último disparo
            left_wing_tip_x = self.x + self.width * 0.1
            right_wing_tip_x = self.x + self.width - self.width * 0.1
            projectiles.append(Projectile(left_wing_tip_x, self.y + self.height * 0.5))
            projectiles.append(Projectile(right_wing_tip_x, self.y + self.height * 0.5))


    def draw(self, screen):
        # Cuerpo principal de la nave
        body_rect = pygame.Rect(self.x + self.width * 0.2, self.y, self.width * 0.6, self.height * 0.8)
        pygame.draw.rect(screen, self.color, body_rect)

        # Núcleo de energía
        core_rect = pygame.Rect(self.x + self.width * 0.4, self.y + self.height * 0.2, self.width * 0.2,
                                self.height * 0.4)
        pygame.draw.rect(screen, YELLOW, core_rect)

        # Punta superior
        pygame.draw.polygon(screen, self.color, [
            (self.x + self.width * 0.5, self.y - self.height * 0.2),
            (self.x + self.width * 0.3, self.y + self.height * 0.2),
            (self.x + self.width * 0.7, self.y + self.height * 0.2)
        ])

        # Alas superiores e inferiores más grandes
        pygame.draw.polygon(screen, self.color, [
            (self.x - self.width * 0.1, self.y + self.height * 0.6),
            (self.x + self.width * 0.2, self.y + self.height * 0.2),
            (self.x + self.width * 0.2, self.y + self.height)
        ])
        pygame.draw.polygon(screen, self.color, [
            (self.x + self.width * 1.1, self.y + self.height * 0.6),
            (self.x + self.width * 0.8, self.y + self.height * 0.2),
            (self.x + self.width * 0.8, self.y + self.height)
        ])


class Obstacle:
    def __init__(self, x, y, width=50, height=50, speed=3, color=(128, 0, 0)):  # Color rojo oscuro para los enemigos
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        # Cuerpo principal de la nave
        body_rect = pygame.Rect(self.x + self.width * 0.2, self.y + self.height * 0.2, self.width * 0.6,
                                self.height * 0.8)
        pygame.draw.rect(screen, self.color, body_rect)

        # Núcleo de energía
        core_rect = pygame.Rect(self.x + self.width * 0.4, self.y + self.height * 0.4, self.width * 0.2,
                                self.height * 0.4)
        pygame.draw.rect(screen, YELLOW, core_rect)

        # Punta inferior, invertida para mirar hacia abajo
        pygame.draw.polygon(screen, self.color, [
            (self.x + self.width * 0.5, self.y + self.height * 1.5),  # Punta dirigida hacia abajo
            (self.x + self.width * 0.3, self.y + self.height * 0.8),  # Esquina izquierda
            (self.x + self.width * 0.7, self.y + self.height * 0.8)  # Esquina derecha
        ])

        # Alas superiores, reorientadas para apuntar hacia abajo
        pygame.draw.polygon(screen, self.color, [
            (self.x, self.y + self.height * -0.2),
            (self.x - self.width * 0.1, self.y + self.height * 0.4),  # Extender ala izquierda hacia afuera
            (self.x + self.width * 0.2, self.y + self.height * 0.4)
        ])
        pygame.draw.polygon(screen, self.color, [
            (self.x + self.width, self.y + self.height * -0.2),
            (self.x + self.width * 1.1, self.y + self.height * 0.4),  # Extender ala derecha hacia afuera
            (self.x + self.width * 0.8, self.y + self.height * 0.4)
        ])

        # Alas inferiores, manteniendo la misma orientación
        pygame.draw.polygon(screen, self.color, [
            (self.x - self.width * 0.1, self.y + self.height * 0.6),
            (self.x + self.width * 0.2, self.y + self.height * 0.6),
            (self.x + self.width * 0.2, self.y + self.height * 1.3)  # Ajuste para mantener la ala dentro del cuerpo
        ])
        pygame.draw.polygon(screen, self.color, [
            (self.x + self.width * 1.1, self.y + self.height * 0.6),
            (self.x + self.width * 0.8, self.y + self.height * 0.6),
            (self.x + self.width * 0.8, self.y + self.height * 1.3)  # Ajuste para mantener la ala dentro del cuerpo
        ])

    def shoot(self, projectiles):
        # Disparar desde la posición central hacia abajo
        projectile_x = self.x + self.width / 2 - 2.5
        projectiles.append(Projectile(projectile_x, self.y + self.height, enemy=True))

    def off_screen(self, screen_height):
        return self.y > screen_height


class Projectile:
    def __init__(self, x, y, enemy=False):
        self.x = x
        self.y = y
        self.speed = 10 if not enemy else -10  # Los proyectiles enemigos se mueven hacia abajo
        self.width = 5
        self.height = 20
        self.color = RED if not enemy else GREEN  # Color distinto para proyectiles enemigos
        self.tip_color = YELLOW
        self.enemy = enemy  # Almacena si el proyectil es enemigo

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        # Dibuja el cuerpo principal del proyectil
        pygame.draw.rect(screen, self.color, (self.x, self.y + self.height * 0.2, self.width, self.height * 0.8))

        # Dibuja la punta del proyectil
        tip_points = [
            (self.x + self.width / 2, self.y),  # Punto superior central
            (self.x, self.y + self.height * 0.2),  # Inferior izquierdo
            (self.x + self.width, self.y + self.height * 0.2)  # Inferior derecho
        ]
        pygame.draw.polygon(screen, self.tip_color, tip_points)

        # Opcional: añadir un efecto de brillo o energía en el centro
        pygame.draw.line(screen, YELLOW, (self.x + self.width / 2, self.y + self.height * 0.2),
                         (self.x + self.width / 2, self.y + self.height), 2)


# Iniciar el juego
game = Game()
game.run()

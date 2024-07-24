import pygame
import random

# Inicializa a biblioteca
pygame.init()

# Definindo o tamanho da tela
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Definindo as cores
white = (255, 255, 255)
black = (0, 0, 0)

# Carregando as imagens
mario_animacao = [pygame.image.load(f'assets/mario_{i}.png') for i in range(3)]  # Listar quantidade de frames da animacao do mario
inimigo_animacao = [pygame.image.load(f'assets/inimigo_{i}.png') for i in range(3)]
fundo_img = pygame.image.load('assets/background.png')

# Definindo a dimensão dos sprites
mario_largura, mario_altura = 50, 50
inimigo_largura, inimigo_altura = 50, 50

# Transformando os sprites em escala do jogo
mario_animacao = [pygame.transform.scale(img, (mario_largura, mario_altura)) for img in mario_animacao]
inimigo_animacao = [pygame.transform.scale(imginimigo, (inimigo_largura, inimigo_altura)) for imginimigo in inimigo_animacao]

# Inicializando a fonte do placar
fonte = pygame.font.Font(None, 36)


def redimensionarFundo():
    global fundo_img
    fundo_img = pygame.transform.scale(pygame.image.load('assets/background.png'), (screen_width, 430))

class Mario:
    def __init__(self):
        self.x = 50
        self.y = screen_height - mario_altura - 10
        self.y_change = 0
        self.jump = False
        self.on_ground = True
        self.jump_speed = 15
        self.gravity = 1

        # Configurações da animação do sprite
        self.animacao_inicial = 0
        self.velocidade_animacao = 0.2
        self.contador_animacao = 0

    def draw(self):
        screen.blit(mario_animacao[self.animacao_inicial], (self.x, self.y))

    def update(self):
        if self.jump and self.on_ground:
            self.y_change = -self.jump_speed
            self.on_ground = False
        self.y += self.y_change
        if not self.on_ground:
            self.y_change += self.gravity  # Gravidade
        if self.y >= screen_height - mario_altura - 10:
            self.y = screen_height - mario_altura - 10
            self.y_change = 0
            self.on_ground = True
            self.jump = False

        # Atualizando animacao frame a frame
        self.contador_animacao += self.velocidade_animacao
        if self.contador_animacao >= 1:
            self.contador_animacao = 0
            self.animacao_inicial = (self.animacao_inicial + 1) % len(mario_animacao)


# Classe dos inimigos
class Inimigo:
    def __init__(self):
        self.x = screen_width
        self.y = screen_height - inimigo_altura - 10
        self.passou = False
        self.velocidade = 10

        self.inimigo_animacao_inicial = 0
        self.inimigo_velocidade_animacao = 0.2
        self.inimigo_contador_animacao = 0

    def draw(self):
        screen.blit(inimigo_animacao[self.inimigo_animacao_inicial], (self.x, self.y))

    def update(self):
        self.x -= self.velocidade
        if self.x < -inimigo_largura:
            self.x = screen_width + random.randint(100, 300)
            self.passou = False

        self.inimigo_contador_animacao += self.inimigo_velocidade_animacao
        if self.inimigo_contador_animacao >= 1:
            self.inimigo_contador_animacao = 0
            self.inimigo_animacao_inicial = (self.inimigo_animacao_inicial + 1) % len(inimigo_animacao)

    def aumentar_velocidade(self, incremento):
        self.velocidade += incremento

def lerRecorde():
    recordes = []
    try:
        with open('recordes.txt', 'r') as arquivo:
            for linha in arquivo:
                # Dividir a linha no formato nome : recorde
                nome_jogador, recorde = linha.strip().split(' : ')
                # pega os dados do txt e adiciona no array
                recordes.append((nome_jogador, int(recorde)))
    except (FileNotFoundError, ValueError):
        pass # Se o arquivo nao existe retorna vazio
    return recordes

def salvarRecorde(nome_jogador, recorde):
    with open('recordes.txt', 'a') as arquivo:
        arquivo.write(f"{nome_jogador} : {recorde}\n")

def mostrarPlacar(score):
    placar = fonte.render(f"Score: {score}", True, black)
    screen.blit(placar, (10, 10))


def mostrarNomeJogador(nome_jogador):
    nome_texto = fonte.render(nome_jogador, True, black)
    nome_correto = nome_texto.get_rect(topright=(screen_width - 10, 10))
    screen.blit(nome_texto, nome_correto)


def mostrarMenu():
    global screen_width, screen_height, screen
    menu = True
    nome_jogador = ""
    input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 30, 200, 50)
    cor_inativo = pygame.Color('lightskyblue3')
    cor_ativo = pygame.Color('dodgerblue2')
    cor = cor_inativo
    ativo = False

    recorde = lerRecorde()
    maior_recorde = max((rec[1] for rec in recorde), default=0)

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if ativo:
                    if event.key == pygame.K_RETURN:
                        menu = False
                    elif event.key == pygame.K_BACKSPACE:
                        nome_jogador = nome_jogador[:-1]
                    else:
                        nome_jogador += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    ativo = not ativo
                else:
                    ativo = False
                cor = cor_ativo if ativo else cor_inativo

                play_button_rect = pygame.Rect(screen_width // 2 - 50, screen_height // 2 + 40, 100, 50)
                if play_button_rect.collidepoint(event.pos):
                    menu = False

            if event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                redimensionarFundo()
                input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 30, 200, 50)

        screen.blit(fundo_img, (0, 0))
        txt_surface = fonte.render(nome_jogador, True, black)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, cor, input_box, 2)

        play_button = fonte.render('Jogar', True, black)
        play_button_rect = play_button.get_rect(center=(screen_width // 2, screen_height // 2 + 80))
        screen.blit(play_button, play_button_rect.topleft)

        recorde_text = fonte.render(f"Maior recorde: {maior_recorde}", True, black)
        recorde_rect = recorde_text.get_rect(center=(screen_width // 2, screen_height // 2 + 130))
        screen.blit(recorde_text, recorde_rect.topleft)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    return nome_jogador

# Mostra a tela e a mensagem de game over
def mostrarGameOver(nome_jogador, score):
    global screen_width, screen_height, screen
    game_over = True
    recorde = lerRecorde()
    maior_recorde = max((rec[1] for rec in recorde), default=0)

    salvarRecorde(nome_jogador, score)

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            screen.blit(fundo_img, (0, 0))  # Desenhar o fundo
            game_over_text = fonte.render("Game Over", True, black)
            game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
            screen.blit(game_over_text, game_over_rect.topleft)

            score_text = fonte.render(f"Score: {score}", True, black)
            score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(score_text, score_rect.topleft)

            recorde_text = fonte.render(f"Maior Recorde: {maior_recorde}", True, black)
            recorde_rect = recorde_text.get_rect(center=(screen_width // 2, screen_height // 2 + 30))
            screen.blit(recorde_text, recorde_rect.topleft)

            play_button = fonte.render('Voltar ao Menu', True, black)
            play_button_rect = play_button.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
            screen.blit(play_button, play_button_rect.topleft)

            if event.type == pygame.MOUSEBUTTONDOWN and play_button_rect.collidepoint(event.pos):
                game_over = False
                return

        pygame.display.flip()
        pygame.time.Clock().tick(30)


def loopInfinito(nome_jogador):
    global screen_width, screen_height, screen

    clock = pygame.time.Clock()
    mario = Mario()
    inimigo = [Inimigo()]
    score = 0
    game_over = False
    incremento_velocidade = 0.5

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and mario.on_ground:
                    mario.jump = True
            if event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                redimensionarFundo()
                mario.y = screen_height - mario_altura - 10
                for i in inimigo:
                    i.y = screen_height - inimigo_altura - 10

        screen.blit(fundo_img, (0, 0))  # Desenhar o bakcground na tela
        mario.update()
        mario.draw()

        for i in inimigo:
            i.update()
            i.draw()
            if i.x + inimigo_largura < mario.x and not i.passou:
                score += 1
                i.passou = True

                # Chama a função da classe inimigo que incrementa sobre a variável e aumenta a velocidade dos inimigos
                for recebe in inimigo:
                    recebe.aumentar_velocidade(incremento_velocidade)
            if mario.x < i.x < mario.x + mario_largura and mario.y + mario_altura > i.y:
                game_over = True

        # Chamar função de mostrar o placar
        mostrarPlacar(score)
        # Chamar a função de mostrar nome do jogador
        mostrarNomeJogador(nome_jogador)
        # Chamar função da biblioteca para atualizar a tela
        pygame.display.update()
        # relógio para atualização da tela (Quase como se fosse o FPS do jogo)
        clock.tick(30)
    mostrarGameOver(nome_jogador, score)
    nome_jogador = mostrarMenu()
    loopInfinito(nome_jogador)

# Redimensionar a imagem de fundo para o tamanho inicial
redimensionarFundo()

# Exibição do menu e nome do jogador
nome_jogador = mostrarMenu()

# Iniciar loop infinito do jogo
loopInfinito(nome_jogador)

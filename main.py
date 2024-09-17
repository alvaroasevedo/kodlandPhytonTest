import pygame
import random

# Inicializa o PyGame
pygame.init()

# Constantes
LARGURA_TELA = 800
ALTURA_TELA = 600
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

# Cria a tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Defensores Espaciais")

# Carregar recursos (imagens e sons podem ser adicionados aqui)
imagem_jogador = pygame.Surface((50, 50))
imagem_jogador.fill(VERDE)
imagem_inimigo = pygame.Surface((50, 50))
imagem_inimigo.fill(VERMELHO)

# Estado do jogo
jogando = True
pontuacao = 0

# Define o Jogador
class Jogador:
    def __init__(self):
        self.imagem = imagem_jogador
        self.rect = self.imagem.get_rect(midbottom=(LARGURA_TELA // 2, ALTURA_TELA - 10))
        self.velocidade = 5
    
    def mover(self, direcao):
        if direcao == "esquerda" and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if direcao == "direita" and self.rect.right < LARGURA_TELA:
            self.rect.x += self.velocidade
    
    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

# Define o Inimigo
class Inimigo:
    def __init__(self, x, y):
        self.imagem = imagem_inimigo
        self.rect = self.imagem.get_rect(topleft=(x, y))
        self.velocidade = 2
    
    def mover(self):
        self.rect.y += self.velocidade
    
    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

# Define o Tiro
class Tiro:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.velocidade = -5
    
    def mover(self):
        self.rect.y += self.velocidade
    
    def desenhar(self, tela):
        pygame.draw.rect(tela, BRANCO, self.rect)

# Funções Personalizadas
def criar_inimigos(num_inimigos):
    inimigos = []
    for _ in range(num_inimigos):
        x = random.randint(0, LARGURA_TELA - 50)
        y = random.randint(-100, -40)
        inimigos.append(Inimigo(x, y))
    return inimigos

def verificar_colisao(tiro, inimigo):
    return tiro.rect.colliderect(inimigo.rect)

# Loop do Jogo
def loop_jogo():
    global jogando, pontuacao
    
    jogador = Jogador()
    tiros = []
    inimigos = criar_inimigos(5)
    relogio = pygame.time.Clock()
    
    while jogando:
        tela.fill(PRETO)
        
        # Manipulação de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogando = False
        
        # Controles
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            jogador.mover("esquerda")
        if teclas[pygame.K_RIGHT]:
            jogador.mover("direita")
        if teclas[pygame.K_SPACE]:
            tiros.append(Tiro(jogador.rect.centerx, jogador.rect.top))
        
        # Atualizar tiros
        for tiro in tiros[:]:
            tiro.mover()
            if tiro.rect.bottom < 0:
                tiros.remove(tiro)
        
        # Atualizar inimigos
        for inimigo in inimigos[:]:
            inimigo.mover()
            if inimigo.rect.top > ALTURA_TELA:
                inimigos.remove(inimigo)
                inimigos.append(Inimigo(random.randint(0, LARGURA_TELA - 50), random.randint(-100, -40)))
            
            for tiro in tiros[:]:
                if verificar_colisao(tiro, inimigo):
                    tiros.remove(tiro)
                    inimigos.remove(inimigo)
                    pontuacao += 10
                    inimigos.append(Inimigo(random.randint(0, LARGURA_TELA - 50), random.randint(-100, -40)))
        
        # Desenho
        jogador.desenhar(tela)
        for tiro in tiros:
            tiro.desenhar(tela)
        for inimigo in inimigos:
            inimigo.desenhar(tela)
        
        # Mostrar pontuação
        fonte = pygame.font.SysFont(None, 36)
        texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, BRANCO)
        tela.blit(texto_pontuacao, (10, 10))
        
        # Atualizar a tela
        pygame.display.flip()
        relogio.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    loop_jogo()

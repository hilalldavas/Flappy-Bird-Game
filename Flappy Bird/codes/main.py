import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936
#oyun penceresi
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')
#başlık

#yazı tipini tanımla
font = pygame.font.SysFont('Bauhaus 93', 60)

#rengi tanımla
white = (255,255,255)

#oyun değişkenini tanımla
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 180
pipe_frequency = 1500 #milisaniye
last_pipe = pygame.time.get_ticks() - pipe_frequency #son boru oyunun ilk başlatıldığı zamandır
score = 0
pass_pipe = False


#resim yükleme
bg1 = pygame.image.load('img/bg.png')
bg2 = pygame.image.load('img/bg2.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')



#puanı ekrana yansıtmak için metin ,yazı tipi,rengi
def draw_text(text, font, text_col, x, y):
    img =font.render(text, True, text_col) #yazı tipim görsele dönüşcek(metin)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0  # hızı sınırlar veya kontrol eder,sayaç
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0  # kuşumun hızı
        self.clicked = False
        # basılı tuttuduğumda yükselmenin devam etmemesi için


    #resimm listesi oluşturdum ve sayaç ekledim
    def update(self):

        if flying == True:

            self.vel += 0.5
            if self.vel > 8:
               self.vel = 8  # konsolda görülür, hız sınırım, baskı, zemine çarptığı an hız sabit kalıcak

            if self.rect.bottom < 768:  #yer çekimi varmış gibi,düşme görüntüsü
                self.rect.y += int(self.vel)

        if game_over == False:
            # atlama
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked == True
                self.vel = -10  #tıkladıpımda yer çekimine ters yönde (negatif yön) gitmesini istediğim için - değeri verdim

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked == False

            # animasyon
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            # eklediğim resimlerden büyük veya eşit oldupunda başa sarmasını sağladım,animasyonun tamamlandığı haline gelmiş oluyor

            # kuşu döndür
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        #konum 1 üst ,-1 alt (boru için)
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
        #iki boru arası 180 piksellik boşluk sağladım


    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
        #boruların oyun hafızasında yer kaplamaması için ekrandan cıkınca silinmesini sağladım


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


    def draw(self):

        action = False

        #fare konumunu al
        pos = pygame.mouse.get_pos()

        #farenin düğmenin üzerinde olup olmadıpını kontrol et
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action =True

        #buton çizmek
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

#ekranı ikiye böldük, zemin ve arka plan için
bird_group.add(flappy)

#yeniden başlatma düğmesi oluştur
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

run = True

while run:

    clock.tick(fps)
    #her sayı için ekranın güncelleme sayısı oyun sürdükçe devam etcek

    #arka plan çiz
    screen.blit(bg1, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    #zemin çiz ve kaydır
    screen.blit(ground_img, (ground_scroll, 768))

    #puanı kontrol et
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and  bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False



    draw_text(str(score), font, white, int(screen_width / 2), 20)


    #çarpışma aramak
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # kuşun yere çarpıp çarpmadığını kontrol edin
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        #yeni borular oluştur
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now


        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()

    #oyunun bitip bitmediğini kontol et ve sıfırla
    if game_over == True:
       if button.draw() == True:
            game_over = False
            score = reset_game()

    if (score % 2 == 1):
        clock.tick(fps)
        # arka plan çiz
        screen.blit(bg2, (0, 0))

        bird_group.draw(screen)
        bird_group.update()
        pipe_group.draw(screen)
        screen.blit(ground_img, (ground_scroll, 768))

        # puanı kontrol et
        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                    and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                    and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False

        draw_text(str(score), font, white, int(screen_width / 2), 20)

        # çarpışma aramak
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            game_over = True

        # kuşun yere çarpıp çarpmadığını kontrol edin
        if flappy.rect.bottom >= 768:
            game_over = True
            flying = False

        if game_over == False and flying == True:

            # yeni borular oluştur
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
                top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now

            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0

            pipe_group.update()

        # oyunun bitip bitmediğini kontol et ve sıfırla
        if game_over == True:
            if button.draw() == True:
                game_over = False
                score = reset_game()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True


    #oyundan çık işlevi
    pygame.display.update()
pygame.quit()




import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys
import random
from enum import Enum

pygame.init()
pygame.font.init()

def resource_path(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path)
    return path

W = 600
icon_surf = pygame.Surface((64, 64))
icon_surf.fill((28, 170, 156))
pygame.draw.line(icon_surf, (66, 66, 66), (10, 50), (54, 6), 8)
pygame.draw.line(icon_surf, (66, 66, 66), (54, 50), (10, 6), 8)
pygame.draw.circle(icon_surf, (239, 231, 200), (55, 55), 8, 2)
icon = pygame.image.fromstring(pygame.image.tostring(icon_surf, "RGB"), (64, 64), "RGB")
pygame.display.set_icon(icon_surf)
G = 3
CS = W // G
LW = 15
CR = CS // 3
CW = 15
SP = CS // 4

BG = (28, 170, 156)
LN = (23, 145, 135)
CL = (239, 231, 200)
CR_C = (66, 66, 66)
TX = (255, 255, 255)

class Mode(Enum):
    MENU = 1
    BOT = 2
    PVP = 3
    END = 4

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((W, W))
        pygame.display.set_caption('Tic Tac Toe')
        icon = pygame.image.load(resource_path("tictactoe_icon.png"))
        pygame.display.set_icon(icon)
        self.screen.fill(BG)
        self.f_lg = pygame.font.Font(None, 60)
        self.f_md = pygame.font.Font(None, 40)
        self.f_sm = pygame.font.Font(None, 30)
        self.reset()
        self.mode = Mode.MENU
        self.ai_timer = 0
        
    def reset(self):
        self.board = [[' ' for _ in range(G)] for _ in range(G)]
        self.player = 'X'
        self.over = False
        self.winner = None
        self.ai_timer = 0
        
    def draw_lines(self):
        for i in range(1, G):
            pygame.draw.line(self.screen, LN, (0, i*CS), (W, i*CS), LW)
            pygame.draw.line(self.screen, LN, (i*CS, 0), (i*CS, W), LW)
        
    def draw_board(self):
        for r in range(G):
            for c in range(G):
                if self.board[r][c] == 'O':
                    pygame.draw.circle(self.screen, CL, (int(c*CS+CS//2), int(r*CS+CS//2)), CR, CW)
                elif self.board[r][c] == 'X':
                    pygame.draw.line(self.screen, CR_C, (c*CS+SP, r*CS+CS-SP), (c*CS+CS-SP, r*CS+SP), CW)
                    pygame.draw.line(self.screen, CR_C, (c*CS+SP, r*CS+SP), (c*CS+CS-SP, r*CS+CS-SP), CW)
                    
    def move(self, r, c, p):
        if self.board[r][c] == ' ':
            self.board[r][c] = p
            return True
        return False
        
    def full(self):
        return all(self.board[r][c] != ' ' for r in range(G) for c in range(G))
        
    def check(self, p):
        for i in range(G):
            if all(self.board[i][j] == p for j in range(G)) or all(self.board[j][i] == p for j in range(G)):
                return True
        return all(self.board[i][i] == p for i in range(G)) or all(self.board[i][G-1-i] == p for i in range(G))
        
    def empty(self):
        return [(r, c) for r in range(G) for c in range(G) if self.board[r][c] == ' ']
        
    def ai(self):
        cells = self.empty()
        for r, c in cells:
            self.board[r][c] = 'O'
            if self.check('O'):
                return
            self.board[r][c] = ' '
        for r, c in cells:
            self.board[r][c] = 'X'
            if self.check('X'):
                self.board[r][c] = 'O'
                return
            self.board[r][c] = ' '
        if (1, 1) in cells:
            self.board[1][1] = 'O'
        else:
            r, c = random.choice(cells)
            self.board[r][c] = 'O'
            
    def menu(self):
        self.screen.fill(BG)
        t = self.f_lg.render('TIC TAC TOE', True, TX)
        self.screen.blit(t, t.get_rect(center=(W//2, 100)))
        
        b1 = pygame.Rect(50, 250, 500, 80)
        pygame.draw.rect(self.screen, LN, b1, 3)
        t1 = self.f_md.render('Play with Bot', True, TX)
        self.screen.blit(t1, t1.get_rect(center=b1.center))
        
        b2 = pygame.Rect(50, 380, 500, 80)
        pygame.draw.rect(self.screen, LN, b2, 3)
        t2 = self.f_md.render('Play with Friend', True, TX)
        self.screen.blit(t2, t2.get_rect(center=b2.center))
        
        return b1, b2
        
    def end_screen(self):
        s = pygame.Surface((W, W))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        self.screen.blit(s, (0, 0))
        
        t = self.f_lg.render(f'Winner: {self.winner}' if self.winner else 'Draw!', True, TX)
        self.screen.blit(t, t.get_rect(center=(W//2, 200)))
        
        b = pygame.Rect(150, 380, 300, 80)
        pygame.draw.rect(self.screen, LN, b, 3)
        t = self.f_md.render('Menu', True, TX)
        self.screen.blit(t, t.get_rect(center=b.center))
        return b
        
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            if self.mode in [Mode.BOT, Mode.PVP] and self.player == 'O' and not self.over and self.ai_timer > 0:
                self.ai_timer -= 1
                if self.ai_timer == 0:
                    self.ai()
                    if self.check('O'):
                        self.winner = 'O'
                        self.over = True
                        self.mode = Mode.END
                    elif self.full():
                        self.over = True
                        self.mode = Mode.END
                    else:
                        self.player = 'X'
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    m = e.pos
                    if self.mode == Mode.MENU:
                        b1, b2 = self.menu()
                        if b1.collidepoint(m):
                            self.reset()
                            self.mode = Mode.BOT
                        elif b2.collidepoint(m):
                            self.reset()
                            self.mode = Mode.PVP
                    elif self.mode in [Mode.BOT, Mode.PVP] and not self.over:
                        c, r = m[0]//CS, m[1]//CS
                        if self.move(r, c, self.player):
                            if self.check(self.player):
                                self.winner = self.player
                                self.over = True
                                self.mode = Mode.END
                            elif self.full():
                                self.over = True
                                self.mode = Mode.END
                            else:
                                self.player = 'O' if self.player == 'X' else 'X'
                                if self.mode == Mode.BOT and self.player == 'O':
                                    self.ai_timer = 30
                    elif self.mode == Mode.END:
                        b = self.end_screen()
                        if b.collidepoint(m):
                            self.mode = Mode.MENU
            
            if self.mode == Mode.MENU:
                self.menu()
            elif self.mode in [Mode.BOT, Mode.PVP]:
                self.screen.fill(BG)
                self.draw_lines()
                self.draw_board()
            elif self.mode == Mode.END:
                self.end_screen()
            
            pygame.display.update()
            clock.tick(60)

def main():
    try:
        game = Game()
        game.run()
    except:
        pygame.quit()

if __name__ == '__main__':
    try:
        Game().run()
    except KeyboardInterrupt:
        pygame.quit()

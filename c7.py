import pygame
import sys

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Ukuran jendela
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 400

# Ukuran kantong
POCKET_RADIUS = 30

class Mancala:
    def __init__(self):
        self.player1_pockets = [7, 7, 7, 7, 7, 7, 7]
        self.player2_pockets = [7, 7, 7, 7, 7, 7, 7]
        self.player1_mancala = 0
        self.player2_mancala = 0
        self.player_turn = 0  # Player 1 starts

    def display_board(self, screen):
        screen.fill(WHITE)
        
        font = pygame.font.Font(None, 36)
        
        # Draw player 2 pockets
        for i, stones in enumerate(reversed(self.player2_pockets)):
            pygame.draw.circle(screen, BLUE, (100 + i * 100, 100), POCKET_RADIUS)
            text = font.render(str(stones), True, BLACK)
            screen.blit(text, (100 + i * 100 - 10, 100 - 10))
        
        # Draw player 1 pockets
        for i, stones in enumerate(self.player1_pockets):
            pygame.draw.circle(screen, BLUE, (100 + i * 100, 300), POCKET_RADIUS)
            text = font.render(str(stones), True, BLACK)
            screen.blit(text, (100 + i * 100 - 10, 300 - 10))
        
        # Draw Mancalas
        pygame.draw.rect(screen, BLUE, (50, 175, 50, 50))
        pygame.draw.rect(screen, BLUE, (850, 175, 50, 50))
        
        man1_text = font.render(str(self.player1_mancala), True, BLACK)
        screen.blit(man1_text, (865, 185))
        
        man2_text = font.render(str(self.player2_mancala), True, BLACK)
        screen.blit(man2_text, (65, 185))
        
        pygame.display.flip()

    def make_move(self, pocket):
        if self.player_turn == 0:
            stones = self.player1_pockets[pocket]
            self.player1_pockets[pocket] = 0
            pos = pocket
            while stones > 0:
                pos = (pos + 1) % 16
                if pos == 7:
                    self.player1_mancala += 1
                    stones -= 1
                    if stones == 0:  # Jika batu terakhir jatuh di Mancala pemain
                        return True
                elif pos < 7:
                    self.player1_pockets[pos] += 1
                    stones -= 1
                elif pos > 7 and pos < 15:
                    self.player2_pockets[pos - 8] += 1
                    stones -= 1

            if pos < 7 and self.player1_pockets[pos] == 1:
                self.player1_mancala += self.player2_pockets[6 - pos] + 1
                self.player2_pockets[6 - pos] = 0
                self.player1_pockets[pos] = 0
            return False
        else:
            stones = self.player2_pockets[pocket]
            self.player2_pockets[pocket] = 0
            pos = pocket + 8  # Menyesuaikan posisi awal untuk pemain 2
            while stones > 0:
                pos = (pos + 1) % 16
                if pos == 15:
                    self.player2_mancala += 1
                    stones -= 1
                    if stones == 0:  # Jika batu terakhir jatuh di Mancala pemain
                        return True
                elif pos > 7 and pos < 15:
                    self.player2_pockets[pos - 8] += 1
                    stones -= 1
                elif pos < 7:
                    self.player1_pockets[pos] += 1
                    stones -= 1

            if 8 <= pos < 15 and self.player2_pockets[pos - 8] == 1:
                self.player2_mancala += self.player1_pockets[6 - (pos - 8)] + 1
                self.player1_pockets[6 - (pos - 8)] = 0
                self.player2_pockets[pos - 8] = 0
            return False

    def check_end_game(self):
        return all(stone == 0 for stone in self.player1_pockets) or all(stone == 0 for stone in self.player2_pockets)

    def determine_winner(self):
        if self.player1_mancala > self.player2_mancala:
            return "Player 1"
        elif self.player1_mancala < self.player2_mancala:
            return "Player 2"
        else:
            return "Tie"

    def handle_player_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if self.player_turn == 0:
                    for i in range(7):
                        if 70 + i * 100 - POCKET_RADIUS < mouse_x < 70 + i * 100 + POCKET_RADIUS and 270 < mouse_y < 330:
                            return i
                else:
                    for i in range(7):
                        if 70 + i * 100 - POCKET_RADIUS < mouse_x < 70 + i * 100 + POCKET_RADIUS and 70 < mouse_y < 130:
                            return 6 - i
        return None

    def game_over_animation(self, screen):
        screen.fill(RED)
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over", True, WHITE)
        screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

    def winner_animation(self, screen, winner):
        screen.fill(GREEN)
        font = pygame.font.Font(None, 72)
        text = font.render(f"{winner} Wins!", True, WHITE)
        screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
        
        # Menampilkan skor total
        player1_score_text = font.render(f"Player 1 Score: {self.player1_mancala}", True, WHITE)
        player2_score_text = font.render(f"Player 2 Score: {self.player2_mancala}", True, WHITE)
        screen.blit(player1_score_text, (WINDOW_WIDTH // 2 - player1_score_text.get_width() // 2, WINDOW_HEIGHT // 2 + 50))
        screen.blit(player2_score_text, (WINDOW_WIDTH // 2 - player2_score_text.get_width() // 2, WINDOW_HEIGHT // 2 + 100))

        pygame.display.flip()
        pygame.time.wait(3000)

    def play_game(self):
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Permainan Congklak')
        while not self.check_end_game():
            self.display_board(screen)
            pocket = None
            while pocket is None:
                pocket = self.handle_player_input()
            if not self.make_move(pocket):
                self.player_turn = 1 - self.player_turn
        self.display_board(screen)
        winner = self.determine_winner()
        self.game_over_animation(screen)
        self.winner_animation(screen, winner)
        print("Game over!")
        print(f"The winner is {winner}!")
        pygame.quit()

if __name__ == "__main__":
    game = Mancala()
    game.play_game()

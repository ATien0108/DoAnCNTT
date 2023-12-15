import pygame
from pygame.locals import *
from database_manager import get_history

class GUI:
    def __init__(self):
        pygame.init()

        self.WINDOW_WIDTH = 500
        self.WINDOW_HEIGHT = 620
        self.main_screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris Game")

        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.Font(None, 40)
        self.input_font = pygame.font.Font(None, 32)

        self.input_rect = pygame.Rect(150, 220, 200, 30)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = ''
        self.text_surface = self.input_font.render(self.text, True, self.color)
        self.width = max(200, self.text_surface.get_width() + 10)

        self.start_button_rect = pygame.Rect(150, 300, 200, 50)
        self.history_button_rect = pygame.Rect(150, 370, 200, 50)
        self.start_button_surface = self.title_font.render("Start", True, (255, 255, 255))
        self.history_button_surface = self.title_font.render("History", True, (255, 255, 255))
        self.back_button_rect = pygame.Rect(150, 500, 200, 50)
        self.back_button_surface = self.title_font.render("Back", True, (255, 255, 255))


        self.input_active = False

    def show_start_screen(self):
        self.main_screen.fill((255, 255, 255))

        # Vẽ tiêu đề tên trò chơi
        title_surface = self.title_font.render("Tetris Game", True, (0, 0, 0))
        title_rect = title_surface.get_rect(centerx=self.input_rect.centerx, centery=self.input_rect.y - 60)
        self.main_screen.blit(title_surface, title_rect)

        # Vẽ ô nhập tên
        pygame.draw.rect(self.main_screen, self.color, self.input_rect, 2)
        self.input_rect.w = self.width
        self.text_surface = self.input_font.render(self.text, True, self.color)

        # Tính toán vị trí cho dòng chữ
        text_x = self.input_rect.x + (self.input_rect.width - self.text_surface.get_width()) // 2
        text_y = self.input_rect.y + (self.input_rect.height - self.text_surface.get_height()) // 2

        self.main_screen.blit(self.text_surface, (text_x, text_y))

        # Vẽ nút Start
        pygame.draw.rect(self.main_screen, (0, 0, 0), self.start_button_rect, 0, 10)
        self.main_screen.blit(self.start_button_surface, self.start_button_surface.get_rect(centerx=self.start_button_rect.centerx, centery=self.start_button_rect.centery))

        # Vẽ nút History
        pygame.draw.rect(self.main_screen, (0, 0, 0), self.history_button_rect, 0, 10)
        self.main_screen.blit(self.history_button_surface, self.history_button_surface.get_rect(centerx=self.history_button_rect.centerx, centery=self.history_button_rect.centery))

        pygame.display.update()

    def run_start_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.start_button_rect.collidepoint(mouse_pos) and self.input_active:
                        return self.text  # Trả về tên người chơi khi nhấn "Start"
                    elif self.history_button_rect.collidepoint(mouse_pos):
                        self.run_history_screen()  # Chuyển đến màn hình lịch sử khi nhấn "History"
                    elif self.input_rect.collidepoint(mouse_pos):
                        self.input_active = not self.input_active
                    else:
                        self.input_active = False
                    self.color = self.color_active if self.input_active else self.color_inactive

                if event.type == pygame.KEYDOWN:
                    if self.input_active:
                        if event.key == pygame.K_RETURN:
                            return self.text  # Trả về tên người chơi khi nhấn "Enter"
                        elif event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += event.unicode
                        self.width = max(200, self.text_surface.get_width() + 10)
                        self.input_rect.w = self.width

            self.show_start_screen()
            self.clock.tick(60)
    
    def show_history_screen(self):
        self.main_screen.fill((255, 255, 255))

        # Hiển thị tiêu đề "History"
        title_surface = self.title_font.render("History", True, (0, 0, 0))
        title_rect = title_surface.get_rect(centerx=self.WINDOW_WIDTH // 2, centery=50)
        self.main_screen.blit(title_surface, title_rect)

        # Hiển thị lịch sử từ cơ sở dữ liệu
        history = get_history()
        if history:
            y_position = 100
            for record in history:
                player_name, score = record
                history_text = f"Player: {player_name}, Score: {score}"
                text_surface = pygame.font.Font(None, 32).render(history_text, True, (0, 0, 0))
                self.main_screen.blit(text_surface, (50, y_position))
                y_position += 40

        # Vẽ nút "BACK"
        pygame.draw.rect(self.main_screen, (0, 0, 0), self.back_button_rect, 0, 10)
        self.main_screen.blit(self.back_button_surface, self.back_button_surface.get_rect(centerx=self.back_button_rect.centerx, centery=self.back_button_rect.centery))

        pygame.display.update()



    def run_history_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.back_button_rect.collidepoint(mouse_pos):
                        return  # Quay lại màn hình trước
            

            self.show_history_screen()
            self.clock.tick(60)

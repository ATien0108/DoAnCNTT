import pygame, sys
from game import Game
from colors import Colors
from database_manager import add_player_to_database, add_score_to_database
from gui import GUI
from game import Game

# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 620

title_font = pygame.font.Font(None, 40)
input_font = pygame.font.Font(None, 32)
score_surface = title_font.render("Score", True, Colors.navy)
player_name_surface = title_font.render("Name", True, Colors.navy)
next_surface = title_font.render("Next", True, Colors.navy)
game_over_surface = title_font.render("GAME OVER", True, Colors.navy)
reset_button_surface = title_font.render("RESET", True, Colors.green_milk)
back_button_surface = title_font.render("BACK", True, Colors.green_milk)
quit_button_surface = title_font.render("QUIT", True, Colors.green_milk)
# back_button_surface_start = title_font.render("BACK", True, Colors.green_milk)

# back_button_rect_start = pygame.Rect(20, 20, 100, 40)
quit_button_rect = pygame.Rect(320, 420, 170, 50)
back_button_rect = pygame.Rect(320, 480, 170, 50)
reset_button_rect = pygame.Rect(320, 550, 170, 50)
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 165, 170, 180)
player_name_rect = pygame.Rect(320, 350, 170, 60)

# Tạo bề mặt hiển thị (rộng 300px, cao 600px)
main_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
input_screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

# Tiêu đề
pygame.display.set_caption("Tetris Game")

# Tạo đồng hồ kiểm soát tốc độ khung hình 
clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200) #Khối rơi xuống 200ms, có thể tùy chỉnh

#Cờ để kiểm soát trạng thái màn hình
in_game = False

#Biến tên người chơi
player_name = ""
input_active = False
input_rect = pygame.Rect(400 // 2 - 100, 250, 200, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
text = ''
text_surface = input_font.render(text, True, color)
width = max(330, text_surface.get_width() + 10)
height = max(330, text_surface.get_height() + 10)

#Đánh dấu thêm vào csdl
added_to_database = False
gui = GUI()

player_name = gui.run_start_screen()
print(f"Player Name: {player_name}")
add_player_to_database(player_name)
game = Game()
# main.py
def get_player_name():
    return player_name

while True:
    for event in pygame.event.get():
        # Khi nhấn vào QUIT thì sẽ thoát ra và đóng trò chơi lại
        if event.type == pygame.QUIT:
            add_score_to_database("0")
            pygame.quit()
            sys.exit()
         # Xử lý sự kiện khi không ở trong game
        if not in_game:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if input_rect.collidepoint(event.pos):
                    input_active = True
                    in_game = True
                color = color_active if input_active else color_inactive

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        player_name = text
                        in_game = True
                        add_player_to_database(text)
                        added_to_database = True  # Đánh dấu là đã thêm vào cơ sở dữ liệu 
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                    width = max(200, text_surface.get_width() + 10)
                    input_rect.w = width
                    print(f"Current text: {text}")
        else:
            if event.type == pygame.KEYDOWN:
                if game.game_over == True:
                    game.game_over = False
                    game.reset()
                if event.key == pygame.K_LEFT and game.game_over == False:
                    game.move_left()
                if event.key == pygame.K_RIGHT and game.game_over == False:
                    game.move_right()
                if event.key == pygame.K_DOWN and game.game_over == False:
                    game.move_down()
                    game.update_score(0, 1)
                if event.key == pygame.K_UP and game.game_over == False:
                    game.rotate()
            if event.type == GAME_UPDATE and game.game_over == False:
                game.move_down()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if reset_button_rect.collidepoint(mouse_pos):
                    if game.game_over == False:
                        add_score_to_database("0")
                    if game.game_over == True:
                        add_player_to_database(player_name)
                    game.reset()
                if back_button_rect.collidepoint(mouse_pos):
                    input_active = False
                    in_game = False  # Đặt lại trạng thái về màn hình nhập tên
                    game.reset()
                if quit_button_rect.collidepoint(mouse_pos):
                    if game.game_over == False:
                       add_score_to_database("0")
                    pygame.quit()
                    sys.exit()       
    #Drawing
    main_screen.fill(Colors.nude)
    if not in_game:
    # Tạo bề mặt văn bản "PLAY"
        play_text_surface = input_font.render("PLAY", True, (255, 0, 0))

        # Cập nhật kích thước và vị trí của hộp chữ để vừa với văn bản "PLAY"
        input_rect.w = play_text_surface.get_width() + 1
        input_rect.h = play_text_surface.get_height() + 1

        # Đặt vị trí hiển thị của văn bản "PLAY" và hộp chữ ở giữa màn hình
        input_rect.x = (500 - input_rect.w) // 2
        input_rect.y = (1000 - input_rect.h) // 2

        # Hiển thị văn bản "PLAY" và vẽ hộp chữ
        main_screen.blit(play_text_surface, (input_rect.x, input_rect.y))
        pygame.draw.rect(main_screen, color, input_rect, 2)

        # Tạo bề mặt văn bản cho tiêu đề
        title_text_surface = input_font.render("TETRIS GAME", True, (0, 0, 0))
        # Đặt vị trí hiển thị của tiêu đề phía trên nút chữ "PLAY"
        title_x = input_rect.x + (input_rect.w - title_text_surface.get_width()) // 2
        title_y = input_rect.y - title_text_surface.get_height() - 400
        # Hiển thị tiêu đề
        main_screen.blit(title_text_surface, (title_x, title_y))

        # Danh sách các đoạn văn bản và khoảng cách giữa chúng
        text_contents = [
            "ARE YOU READY?",
            "NOTE:",
            "IF YOU EXIT THE GAME DURING PLAY",
            "YOUR SCORE WILL BE 0"
        ]
        # Tạo bề mặt văn bản và hiển thị cho mỗi đoạn văn bản
        for i, text_content in enumerate(text_contents):
            title_text_surface = input_font.render(text_content, True, (0, 0, 0))
            title_x = input_rect.x + (input_rect.w - title_text_surface.get_width()) // 2
            title_y = input_rect.y - title_text_surface.get_height() - 300 + (i * 50)
            main_screen.blit(title_text_surface, (title_x, title_y))

        # pygame.draw.rect(main_screen, (0, 0, 0), back_button_rect_start, 0, 10)
        # main_screen.blit(back_button_surface_start, back_button_surface_start.get_rect(centerx = back_button_rect_start.centerx, centery = back_button_rect_start.centery))
        # pygame.display.update()


      
    else:
        player_name_surface = title_font.render(player_name, True, Colors.green_milk)
        score_value_surface = title_font.render(str(game.score), True, Colors.green_milk)

        main_screen.blit(score_surface, (365, 20, 50, 50))
        main_screen.blit(next_surface, (365, 130, 50, 50))

        if game.game_over == True:
            main_screen.blit(game_over_surface, (320, 450, 50, 50))

        pygame.draw.rect(main_screen, Colors.black, score_rect, 0, 10)
        main_screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
        
        pygame.draw.rect(main_screen, Colors.black, next_rect, 0, 10)
        
        pygame.draw.rect(main_screen, Colors.black, player_name_rect, 0, 10)
        main_screen.blit(player_name_surface, player_name_surface.get_rect(centerx = player_name_rect.centerx, centery = player_name_rect.centery))

        pygame.draw.rect(main_screen, Colors.black, reset_button_rect, 0, 10)
        main_screen.blit(reset_button_surface, reset_button_surface.get_rect(centerx=reset_button_rect.centerx, centery=reset_button_rect.centery))

        pygame.draw.rect(main_screen, Colors.black, back_button_rect, 0, 10)
        main_screen.blit(back_button_surface, back_button_surface.get_rect(centerx=back_button_rect.centerx, centery=back_button_rect.centery))

        pygame.draw.rect(main_screen, Colors.black, quit_button_rect, 0, 10)
        main_screen.blit(quit_button_surface, quit_button_surface.get_rect(centerx=quit_button_rect.centerx, centery=quit_button_rect.centery))

        game.draw(main_screen)

    pygame.display.update()
    clock.tick(60)

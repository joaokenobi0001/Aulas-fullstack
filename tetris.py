import pygame  
import random

pygame.init()

screen_width = 300
screen_height = 600
block_size = 30

colors = [
    (0, 0, 0),       
    (255, 0, 0),     
    (0, 255, 0),     
    (0, 0, 255),     
    (255, 255, 0),  
    (255, 165, 0),   
    (128, 0, 128)   
]

cols = screen_width // block_size
rows = screen_height // block_size

shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 4, 4, 4]],

    [[5, 5],
     [5, 5]],

    [[0, 0, 6],
     [6, 6, 6]],

    [[6, 0, 0],  
     [6, 6, 6]]  
]

def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

class Tetris:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.gameover = False
        self.score = 0
        self.current_shape = self.new_shape()
        self.next_shape = self.new_shape()
        self.current_x = cols // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0

    def new_shape(self):
        return random.choice(shapes)

    def valid_move(self, shape, offset):
        off_x, off_y = offset
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = x + off_x
                    new_y = y + off_y
                    if new_x < 0 or new_x >= self.cols or new_y >= self.rows or self.board[new_y][new_x]:
                        return False
        return True

    def clear_lines(self):
        lines_to_clear = [index for index, row in enumerate(self.board) if all(row)]
        for index in lines_to_clear:
            self.board.pop(index)
            self.board.insert(0, [0 for _ in range(self.cols)])
        self.score += len(lines_to_clear)

    def freeze_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[y + self.current_y][x + self.current_x] = cell
        self.clear_lines()
        self.current_shape = self.next_shape
        self.next_shape = self.new_shape()
        self.current_x = self.cols // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        if not self.valid_move(self.current_shape, (self.current_x, self.current_y)):
            self.gameover = True

    def move(self, dx, dy):
        if self.valid_move(self.current_shape, (self.current_x + dx, self.current_y + dy)):
            self.current_x += dx
            self.current_y += dy
            return True
        return False

    def rotate(self):
        rotated_shape = rotate_shape(self.current_shape)
        if self.valid_move(rotated_shape, (self.current_x, self.current_y)):
            self.current_shape = rotated_shape

    def drop(self):
        while self.move(0, 1):
            pass
        self.freeze_shape()

def draw_board(screen, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell < len(colors):  # Ensure the cell value is within the range of colors list
                pygame.draw.rect(screen, colors[cell], (x * block_size, y * block_size, block_size, block_size), 0)

def draw_shape(screen, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if cell < len(colors):
                    pygame.draw.rect(screen, colors[cell], ((off_x + x) * block_size, (off_y + y) * block_size, block_size, block_size), 0)
                else:
                    print(f"Error: cell value {cell} is out of range for colors list")

def main():
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Tetris(cols, rows)
    fall_time = 0

    while not game.gameover:
        fall_speed = 0.5  # seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.gameover = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_SPACE:
                    game.drop()

        fall_time += clock.get_rawtime()
        clock.tick()
        
        if fall_time / 1000 > fall_speed:
            if not game.move(0, 1):
                game.freeze_shape()
            fall_time = 0

        screen.fill((0, 0, 0))
        draw_board(screen, game.board)
        draw_shape(screen, game.current_shape, (game.current_x, game.current_y))
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

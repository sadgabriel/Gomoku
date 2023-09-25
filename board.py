import pygame

class Board():
    def __init__(self) -> None:
        self._grid = [ [ 0 for _ in range(15) ] for _ in range(15) ]
        return
    
    # raw print _grid for test
    def print_grid(self) -> None:
        for i in range(15):
            for j in range(15):
                print(self._grid[i][j], end = ' ')
            print()
    
    def put_stone(self, x, y, turn):
        if self._is_valid(x, y, turn):
            if turn % 2 == 1:   # if it is black turn / Black is odd / White is even
                self._grid[x][y] = 1
            else:               # if it is white turn
                self._grid[x][y] = 2
            return True
        else:                   # if the point which player click is not valid
            return False        # return False to do something for caller

    def check_end(self, x, y, turn):
        """
        Check the endding condition.
        Find 5 or more than continuous stones
        """
        if turn % 2 == 1:
            color = 1
        else:
            color = 2

        for dir in [[1, 1], [1, -1], [1, 0], [0, 1]]:
            line = Line(1, 0, dir)
            cur_x = x + line.direction[0]
            cur_y = y + line.direction[1]
            while not self._is_out_of_range(cur_x, cur_y):
                cur = self._grid[cur_x][cur_y]
                if cur != color:
                    break
                else:
                    line.length += 1
                cur_x += line.direction[0]
                cur_y += line.direction[1]
            cur_x = x - line.direction[0]
            cur_y = y - line.direction[1]
            while not self._is_out_of_range(cur_x, cur_y):
                cur = self._grid[cur_x][cur_y]
                if cur != color:
                    break
                else:
                    line.length += 1
                cur_x -= line.direction[0]
                cur_y -= line.direction[1]
            if line.length > 4:
                print(line.length, line.direction, line.num_opened)
                return True
        return False
            
    def _is_valid(self, x, y, turn):
        # check out of range
        if self._is_out_of_range(x, y):
            return False
        
        # check duplicated stone
        if self._grid[x][y] != 0:
            return False
        
        # check restricted_zone
        if self._grid[x][y] == 3:
            return False
        
        return True

    def update_restricted_zone(self, turn):
        """
        Iterate every grid
        to check restricted condition
        """
        if turn % 2 == 0:               # if it is white turn
            for i in range(15):         # change all restricted zone
                for j in range(15):     # into empty
                    if self._grid[i][j] == 3:
                        self._grid[i][j] = 0
        else:                           # if it is black turn
            for i in range(15):         # check restricted condition every grid
                for j in range(15):
                    if self._is_restricted(i, j):
                        self._grid[i][j] = 3

    def render(self, screen, turn = 0):
        # board render setup
        term = 45
        left = 280
        margin = 45
        pygame.draw.rect(screen, "brown", pygame.Rect(280, 0, 720, 720))
        for i in range(15):
            pygame.draw.line(screen, "black", (left + margin + i * term, margin), (left + margin + i * term, 720 - margin))
            pygame.draw.line(screen, "black", (left + margin, i * term + margin), (720 + left - margin, i * term + margin))

        for i in range(15):
            for j in range(15):
                if self._grid[i][j] == 1:
                    pygame.draw.circle(screen, "black", pygame.Vector2(left + margin + i * term, j * term + margin), 18)
                elif self._grid[i][j] == 2:
                    pygame.draw.circle(screen, "white", pygame.Vector2(left + margin + i * term, j * term + margin), 18)
                elif self._grid[i][j] == 3:
                    pygame.draw.circle(screen, "red", pygame.Vector2(left + margin + i * term, j * term + margin), 18)

    def _is_restricted(self, x, y):
        # find 3x3, 4x4 and overline
        if self._grid[x][y] == 1:
            return False
        directions = [[1, 1], [1, -1], [1, 0], [0, 1]]
        lines = []
        for dir in directions:
            line = Line(0, 0, dir)
            i = 1
            cur_x = x + line.direction[0]
            cur_y = y + line.direction[1]
            while not self._is_out_of_range(cur_x, cur_y):
                cur = self._grid[cur_x][cur_y]
                if cur == 0 or cur == 3:
                    line.num_opened += 1
                    break
                elif cur == 2:
                    break
                i += 1
                cur_x += line.direction[0]
                cur_y += line.direction[1]
            line.length += i
            i = 0
            cur_x = x - line.direction[0]
            cur_y = y - line.direction[1]
            while not self._is_out_of_range(cur_x, cur_y):
                cur = self._grid[cur_x][cur_y]
                if cur == 0 or cur == 3:
                    line.num_opened += 1
                    break
                elif cur == 2:
                    break
                i += 1
                cur_x -= line.direction[0]
                cur_y -= line.direction[1]
            line.length += i
            lines.append(line)
        num_3_line = 0
        num_4_line = 0
        for lin in lines:
            if lin.length > 5:          # overline
                #print("overline")
                return True
            elif lin.length == 4 and lin.num_opened != 0:
                # find 4 continuous black stones except zero open-ended
                num_4_line += 1
            elif lin.length == 3 and lin.num_opened == 2:
                # find two open-ended lines of 3 continuous black stones
                num_3_line += 1
            if num_4_line > 1:      # 4x4
                #print("4x4")
                return True
            elif num_3_line > 1:    # 3x3
                #print("3x3")
                return True
        return False

    def _is_out_of_range(self, x, y):
        # check out of range
        if x < 0 or x > 14 or y < 0 or y > 14:
            return True
        else:
            return False

class Line:
    def __init__(self, len, num_o, dir) -> None:
        self.length = len
        self.num_opened = num_o
        self.direction = dir
"""
Test code below


test_board = Board()
turn = 1
import random as rd
def win(x, y):
    print("win")
    print(turn)
    print(a, b)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

a=1
b=1
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("blue")

    # RENDER YOUR GAME HERE
    test_board.render(screen)

    # TEST CODE
    a = rd.randrange(0, 15)
    b = rd.randrange(0, 15)
    print(a,b)
    if not test_board.put_stone(a, b, turn):
        continue
    if test_board.check_end(a, b, turn):
        test_board.render(screen)
        pygame.display.flip()
        win(a, b)
    test_board.update_restricted_zone(turn)
    turn += 1

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(100)  # limits FPS to 60

pygame.quit()
"""
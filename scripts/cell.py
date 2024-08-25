import pygame


class Cell:
    def __init__(self, x, y, size, board, i, j):  
        self.alive = False
        self.x = x
        self.y = y
        self.size = size
        self.neighbours = []
        self.alive_neighbours = 0
        self.board = board
        self.i = i
        self.j = j
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
    

    def get_neighbours(self):
        grid = self.board.grid
        self.neighbours = []
        neighbours_coordinates = [(self.i, self.j+1), (self.i, self.j-1), (self.i-1, self.j), (self.i-1, self.j+1), 
                                  (self.i-1, self.j-1), (self.i+1, self.j), (self.i+1, self.j-1), (self.i+1, self.j+1)]
        for coordinate in neighbours_coordinates:
            try:
                if grid[coordinate[0]][coordinate[1]]:
                    self.neighbours.append(grid[coordinate[0]][coordinate[1]])
            except:
                pass
    
    def count_alive_neighbours(self):
        self.alive_neighbours = 0
        for i in self.neighbours:
            if i.alive == True:
                self.alive_neighbours += 1

    def update(self, neighbours):
        if self.alive:
            if neighbours < 2:
                self.die()
            elif neighbours > 3:
                self.die()
            else:
                self.live()
        else:
            if neighbours == 3:
                self.live()
            else:
                self.die()
        
    
    def draw(self, surface, alive_color, dead_color):
        
        if self.alive:
            color = alive_color
        else:
            color = dead_color
        
        pygame.draw.rect(surface, color, self.rect)

    def live(self):
        self.alive = True
    
    def die(self):
        self.alive = False

    

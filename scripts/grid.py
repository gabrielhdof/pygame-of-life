
from scripts.cell import Cell


class Grid:
    def __init__(self,x, y, block_size):
        self.x = x 
        self.y = y
        self.block_size = block_size
        self.generate_grid()
        self.alive_cells = 0
        pass
    
    def generate_grid(self):
        self.grid = []
        x_blocks = self.x // self.block_size
        y_blocks = self.y // self.block_size
        for i in range(x_blocks):
            row = []
            for j in range(y_blocks):
                cell = Cell(i * self.block_size, j * self.block_size, self.block_size, self, i, j)
                row.append(cell)
            self.grid.append(row)

    def update_grid(self):
        self.alive_cells = 0
        for row in self.grid:
            for cell in row:
                cell.get_neighbours()
        
        for row in self.grid:
            for cell in row:
                cell.count_alive_neighbours()
        
        for row in self.grid:
            for cell in row:
                if cell.alive:
                    self.alive_cells += 1
                cell.update(cell.alive_neighbours)
        
    def draw_grid(self, surface, alive_color, dead_color):
        for row in self.grid:
            for cell in row:
                cell.draw(surface, alive_color, dead_color)
    
    def click(self, mouse_pos):
        for row in self.grid:
            for cell in row:
                if cell.rect.collidepoint(mouse_pos):
                    cell.alive = not cell.alive
            



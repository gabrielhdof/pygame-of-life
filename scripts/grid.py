
from scripts.cell import Cell


class Grid:
    def __init__(self, x, y, block_size):
        self.x = x
        self.y = y
        self.block_size = block_size
        self.generate_grid()
        self.alive_cells = 0
        self.last_held_cell = None
        pass

    def generate_grid(self):
        self.grid: list[list[Cell]] = []
        x_blocks = self.x // self.block_size
        y_blocks = self.y // self.block_size
        for i in range(x_blocks):
            row = []
            for j in range(y_blocks):
                cell = Cell(i * self.block_size, j *
                            self.block_size, self.block_size, self, i, j)
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
        cell = self.cell_from_mouse_pos(mouse_pos)
        cell.alive = not cell.alive

    def holding(self, mouse_pos):
        cell_in_pos = self.cell_from_mouse_pos(mouse_pos)

        if self.last_held_cell is None:
            cell_in_pos.alive = not cell_in_pos.alive
            self.last_held_cell = cell_in_pos
            return

        if self.last_held_cell.get_idx_in_grid() != cell_in_pos.get_idx_in_grid:
            cell_in_pos.alive = self.last_held_cell.alive
            self.last_held_cell = cell_in_pos

    def cell_from_mouse_pos(self, mouse_pos):
        for row in self.grid:
            for cell in row:
                if cell.rect.collidepoint(mouse_pos):
                    return cell
        return None

    def cancel_holding(self):
        self.last_held_cell = None

import tkinter as tk
import random

class VacuumWorld:
    def __init__(self, master):
        self.master = master
        self.master.title("Vacuum Cleaner Simulation")
        
        self.size = 10
        self.cell_size = 50
        
        self.canvas = tk.Canvas(master, width=self.size*self.cell_size, height=self.size*self.cell_size)
        self.canvas.pack()
        
        self.world = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.agent_pos = [0, 0]
        
        self.create_world()
        self.draw_world()
        
        self.master.after(500, self.update)
    
    def create_world(self):
        # Place some obstacles
        for _ in range(10):
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if [x, y] != self.agent_pos:
                self.world[y][x] = 2  # 2 represents an obstacle
        
        # Make some cells dirty
        for _ in range(20):
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if self.world[y][x] == 0:
                self.world[y][x] = 1  # 1 represents a dirty cell
    
    def draw_world(self):
        self.canvas.delete("all")
        for y in range(self.size):
            for x in range(self.size):
                if self.world[y][x] == 0:
                    color = "white"
                elif self.world[y][x] == 1:
                    color = "brown"
                else:
                    color = "gray"
                self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size, 
                                             (x+1)*self.cell_size, (y+1)*self.cell_size, 
                                             fill=color)
        
        # Draw agent
        self.canvas.create_oval(self.agent_pos[0]*self.cell_size, self.agent_pos[1]*self.cell_size,
                                (self.agent_pos[0]+1)*self.cell_size, (self.agent_pos[1]+1)*self.cell_size,
                                fill="red")
    
    def update(self):
        # Clean current cell if dirty
        if self.world[self.agent_pos[1]][self.agent_pos[0]] == 1:
            self.world[self.agent_pos[1]][self.agent_pos[0]] = 0
        
        # Move agent
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x, new_y = self.agent_pos[0] + dx, self.agent_pos[1] + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.size and self.world[new_y][new_x] != 2:
                self.agent_pos = [new_x, new_y]
                break
        
        self.draw_world()
        self.master.after(500, self.update)

root = tk.Tk()
app = VacuumWorld(root)
root.mainloop()

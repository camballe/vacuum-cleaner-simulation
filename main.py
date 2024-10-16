import tkinter as tk
from tkinter import filedialog, messagebox
import random
import time

class Environment:
    MAZE_SIZE = 10
    OBSTACLE = -1
    MAP_ROAD = '-'
    MAP_OBSTACLE = 'O'
    MAX_DIRT = 50

    def __init__(self, infile):
        self.bump_ = False
        self.maze_ = [[0 for _ in range(self.MAZE_SIZE)] for _ in range(self.MAZE_SIZE)]
        self.preAction_ = Agent.ActionType.IDLE
        self.map_file = infile.name

        comment = infile.readline()
        self.agentPosX_, self.agentPosY_, self.dirtyProb_, self.randomSeed_ = map(float, infile.readline().split())
        self.agentPosX_, self.agentPosY_, self.randomSeed_ = int(self.agentPosX_), int(self.agentPosY_), int(self.randomSeed_)
        self.dirtyProb_ = float(self.dirtyProb_)

        for row in range(self.MAZE_SIZE):
            line = infile.readline().split()
            for col in range(self.MAZE_SIZE):
                if line[col] == self.MAP_OBSTACLE:
                    self.maze_[row][col] = self.OBSTACLE

    def Change(self, rng):
        for row in range(self.MAZE_SIZE):
            for col in range(self.MAZE_SIZE):
                if self.maze_[row][col] != self.OBSTACLE and rng.random() < self.dirtyProb_:
                    self.maze_[row][col] = min(self.MAX_DIRT, self.maze_[row][col] + 1)

    def AcceptAction(self, action):
        self.bump_ = False
        if action == Agent.ActionType.SUCK:
            if self.maze_[self.agentPosX_][self.agentPosY_] > 0:
                self.maze_[self.agentPosX_][self.agentPosY_] -= 1
        elif action == Agent.ActionType.UP:
            if self.agentPosX_ > 0 and self.maze_[self.agentPosX_ - 1][self.agentPosY_] != self.OBSTACLE:
                self.agentPosX_ -= 1
            else:
                self.bump_ = True
        elif action == Agent.ActionType.DOWN:
            if self.agentPosX_ < self.MAZE_SIZE - 1 and self.maze_[self.agentPosX_ + 1][self.agentPosY_] != self.OBSTACLE:
                self.agentPosX_ += 1
            else:
                self.bump_ = True
        elif action == Agent.ActionType.LEFT:
            if self.agentPosY_ > 0 and self.maze_[self.agentPosX_][self.agentPosY_ - 1] != self.OBSTACLE:
                self.agentPosY_ -= 1
            else:
                self.bump_ = True
        elif action == Agent.ActionType.RIGHT:
            if self.agentPosY_ < self.MAZE_SIZE - 1 and self.maze_[self.agentPosX_][self.agentPosY_ + 1] != self.OBSTACLE:
                self.agentPosY_ += 1
            else:
                self.bump_ = True
        self.preAction_ = action

    def DirtAmount(self, x, y):
        return 0 if self.maze_[x][y] == self.OBSTACLE else self.maze_[x][y]

    def isCurrentPosDirty(self):
        return self.maze_[self.agentPosX_][self.agentPosY_] > 0

    def isJustBump(self):
        return self.bump_

class Agent:
    class ActionType:
        UP, DOWN, LEFT, RIGHT, SUCK, IDLE = range(6)

    def __init__(self):
        self.bump_ = False
        self.dirty_ = False

    def Perceive(self, env):
        self.bump_ = env.isJustBump()
        self.dirty_ = env.isCurrentPosDirty()

    def Think(self):
        if self.dirty_:
            return self.ActionType.SUCK
        return random.choice([self.ActionType.UP, self.ActionType.DOWN, self.ActionType.LEFT, self.ActionType.RIGHT])

class RandomNumberGenerator:
    def __init__(self, seed):
        random.seed(seed)

    def random(self):
        return random.random()

class Evaluator:
    def __init__(self):
        self.dirtyDegree_ = 0
        self.consumedEnergy_ = 0

    def Eval(self, action, env):
        if action == Agent.ActionType.SUCK:
            self.consumedEnergy_ += 2
        elif action != Agent.ActionType.IDLE:
            self.consumedEnergy_ += 1

        self.dirtyDegree_ = 0
        for row in range(Environment.MAZE_SIZE):
            for col in range(Environment.MAZE_SIZE):
                da = env.DirtAmount(row, col)
                self.dirtyDegree_ += (da * da)

    def DirtyDegree(self):
        return self.dirtyDegree_

    def ConsumedEnergy(self):
        return self.consumedEnergy_

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Vacuum Cleaner Agent Simulation")
        self.canvas = tk.Canvas(self.master, width=500, height=500)
        self.canvas.pack(side=tk.LEFT)

        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack(side=tk.LEFT, padx=10)

        self.stats_frame = tk.Frame(self.master)
        self.stats_frame.pack(side=tk.LEFT, padx=10)

        self.setup_controls()
        self.setup_stats()

        self.env = None
        self.agent = None
        self.evaluator = None
        self.rng = None
        self.current_time = 0
        self.current_run = 0
        self.total_runs = 10
        self.life_time = 2000
        self.total_dirty_degree = 0
        self.total_consumed_energy = 0

    def setup_controls(self):
        tk.Button(self.control_frame, text="New Map", command=self.new_map).pack(fill=tk.X)
        tk.Button(self.control_frame, text="Do One Step", command=self.do_one_step).pack(fill=tk.X)
        tk.Button(self.control_frame, text="Do One Run", command=self.do_one_run).pack(fill=tk.X)
        tk.Button(self.control_frame, text="Do All Run", command=self.do_all_run).pack(fill=tk.X)

    def setup_stats(self):
        self.time_step_label = tk.Label(self.stats_frame, text="Time Step: 0")
        self.time_step_label.pack()
        self.action_label = tk.Label(self.stats_frame, text="Action: IDLE")
        self.action_label.pack()
        self.dirty_degree_label = tk.Label(self.stats_frame, text="Dirty Degree: 0")
        self.dirty_degree_label.pack()
        self.consumed_energy_label = tk.Label(self.stats_frame, text="Consumed Energy: 0")
        self.consumed_energy_label.pack()
        self.completed_runs_label = tk.Label(self.stats_frame, text="Completed Runs: 0")
        self.completed_runs_label.pack()
        self.total_score_label = tk.Label(self.stats_frame, text="Total Score: Dirty Degree = 0, Consumed Energy = 0")
        self.total_score_label.pack()
        self.average_score_label = tk.Label(self.stats_frame, text="Average Score: Dirty Degree = 0, Consumed Energy = 0")
        self.average_score_label.pack()

    def new_map(self):
        file_path = filedialog.askopenfilename(filetypes=[("Map files", "*.map")])
        if file_path:
            self.load_map(file_path)

    def load_map(self, file_path):
        try:
            with open(file_path, "r") as infile:
                self.env = Environment(infile)
                self.rng = RandomNumberGenerator(self.env.randomSeed_)
            self.agent = Agent()
            self.evaluator = Evaluator()
            self.current_time = 0
            self.current_run = 1
            self.total_dirty_degree = 0
            self.total_consumed_energy = 0
            self.update_display()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading map: {str(e)}")

    def do_one_step(self):
        if self.env and self.current_time < self.life_time:
            self.env.Change(self.rng)
            self.agent.Perceive(self.env)
            action = self.agent.Think()
            self.env.AcceptAction(action)
            self.evaluator.Eval(action, self.env)
            self.current_time += 1
            self.update_display()
            self.master.update()

    def do_one_run(self):
        if not self.env:
            messagebox.showerror("Error", "Please load a map first.")
            return
        
        while self.current_time < self.life_time:
            self.do_one_step()
            time.sleep(0.01)

    def next_run(self):
        if self.current_run < self.total_runs:
            self.current_run += 1
            self.total_dirty_degree += self.evaluator.DirtyDegree()
            self.total_consumed_energy += self.evaluator.ConsumedEnergy()
            self.load_map(self.env.map_file)
            self.current_time = 0
            self.evaluator = Evaluator()

    def do_all_run(self):
        if not self.env:
            messagebox.showerror("Error", "Please load a map first.")
            return
        
        for _ in range(self.total_runs):
            self.do_one_run()
            self.next_run()
        
        avg_dirty_degree = self.total_dirty_degree / self.total_runs
        avg_consumed_energy = self.total_consumed_energy / self.total_runs
        
        messagebox.showinfo("All Runs Completed", 
                            f"Average Dirty Degree: {avg_dirty_degree:.2f}\n"
                            f"Average Consumed Energy: {avg_consumed_energy:.2f}")

    def update_display(self):
        self.canvas.delete("all")
        cell_size = 500 // Environment.MAZE_SIZE
        for x in range(Environment.MAZE_SIZE):
            for y in range(Environment.MAZE_SIZE):
                if self.env.maze_[x][y] == Environment.OBSTACLE:
                    color = "gray"
                else:
                    dirt_level = self.env.maze_[x][y]
                    green = max(0, 255 - dirt_level * 5)
                    color = f"#{green:02x}ff{green:02x}"  # Green to white
                self.canvas.create_rectangle(y*cell_size, x*cell_size, (y+1)*cell_size, (x+1)*cell_size, fill=color, outline="")
        
        # Draw agent
        self.canvas.create_oval(self.env.agentPosY_*cell_size + 2, self.env.agentPosX_*cell_size + 2, 
                                (self.env.agentPosY_+1)*cell_size - 2, (self.env.agentPosX_+1)*cell_size - 2, fill="red", outline="")

        # Update statistics
        self.time_step_label.config(text=f"Time Step: {self.current_time}")
        self.action_label.config(text=f"Action: {self.action_to_string(self.env.preAction_)}")
        self.dirty_degree_label.config(text=f"Dirty Degree: {self.evaluator.DirtyDegree()}")
        self.consumed_energy_label.config(text=f"Consumed Energy: {self.evaluator.ConsumedEnergy()}")
        
        completed_runs = self.current_run - (1 if self.current_time < self.life_time else 0)
        self.completed_runs_label.config(text=f"Completed Runs: {completed_runs}")
        self.total_score_label.config(text=f"Total Score: Dirty Degree = {self.total_dirty_degree}, Consumed Energy = {self.total_consumed_energy}")
        
        if completed_runs > 0:
            avg_dirty = self.total_dirty_degree / completed_runs
            avg_energy = self.total_consumed_energy / completed_runs
            self.average_score_label.config(text=f"Average Score: Dirty Degree = {avg_dirty:.2f}, Consumed Energy = {avg_energy:.2f}")

    def action_to_string(self, action):
        return ["UP", "DOWN", "LEFT", "RIGHT", "SUCK", "IDLE"][action]

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

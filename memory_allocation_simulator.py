import tkinter as tk
from tkinter import messagebox
import random

class MemoryAllocationSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Memory Allocation Simulator and Leak Detector")
        self.root.geometry("900x750")

        self.memory_size = 100  # Total memory size
        self.memory_blocks = ["Free"] * self.memory_size
        self.processes = []  # Store process details
        self.total_allocated = 0
        self.total_deallocated = 0
        self.last_allocated_position = 0  # For Next Fit algorithm

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Advanced Memory Allocation Simulator and Leak Detector", font=("Arial", 16), bg="lightblue", fg="black")
        title_label.pack(fill=tk.X)

        # Memory statistics
        self.stats_label = tk.Label(self.root, text=f"Total Allocated: {self.total_allocated} | Total Deallocated: {self.total_deallocated} | Free Space: {self.memory_size - self.total_allocated}", font=("Arial", 12), bg="lightgray")
        self.stats_label.pack(fill=tk.X, pady=5)

        # Input fields for memory allocation
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Process Name:").grid(row=0, column=0, padx=5)
        self.process_name_entry = tk.Entry(input_frame)
        self.process_name_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Process Size:").grid(row=0, column=2, padx=5)
        self.process_size_entry = tk.Entry(input_frame)
        self.process_size_entry.grid(row=0, column=3, padx=5)

        tk.Button(input_frame, text="Allocate Memory", command=self.allocate_memory, bg="green", fg="white").grid(row=0, column=4, padx=5)

        tk.Label(input_frame, text="Algorithm:").grid(row=1, column=0, padx=5)
        self.algorithm_var = tk.StringVar(value="First Fit")
        tk.OptionMenu(input_frame, self.algorithm_var, "First Fit", "Best Fit", "Worst Fit", "Next Fit").grid(row=1, column=1, padx=5)

        tk.Label(input_frame, text="Resize Memory:").grid(row=2, column=0, padx=5)
        self.resize_memory_entry = tk.Entry(input_frame)
        self.resize_memory_entry.grid(row=2, column=1, padx=5)
        tk.Button(input_frame, text="Resize", command=self.resize_memory, bg="teal", fg="white").grid(row=2, column=2, padx=5)

        # Display memory blocks
        self.memory_canvas = tk.Canvas(self.root, width=850, height=300, bg="white")
        self.memory_canvas.pack(pady=10)

        # Action Buttons
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=5)

        tk.Button(action_frame, text="Detect Memory Leaks", command=self.detect_leaks, bg="red", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(action_frame, text="Deallocate Memory", command=self.deallocate_memory, bg="orange", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(action_frame, text="Reset Memory", command=self.reset_memory, bg="blue", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(action_frame, text="Fragmentation Analysis", command=self.fragmentation_analysis, bg="purple", fg="white").grid(row=0, column=3, padx=5)

        # Process List
        self.process_list_box = tk.Listbox(self.root, height=10, width=60)
        self.process_list_box.pack(pady=10)

        # Additional Information
        tk.Label(self.root, text="Color Legend:", font=("Arial", 10)).pack(pady=5)
        legend_frame = tk.Frame(self.root)
        legend_frame.pack()

        tk.Label(legend_frame, text="Free", bg="green", fg="white", width=10).grid(row=0, column=0, padx=5)
        tk.Label(legend_frame, text="Allocated", bg="blue", fg="white", width=10).grid(row=0, column=1, padx=5)
        tk.Label(legend_frame, text="Leaked", bg="red", fg="white", width=10).grid(row=0, column=2, padx=5)

        self.update_memory_canvas()

    def allocate_memory(self):
        try:
            process_name = self.process_name_entry.get().strip()
            process_size = int(self.process_size_entry.get())
            algorithm = self.algorithm_var.get()

            if not process_name or process_size <= 0:
                raise ValueError("Invalid input")

            # Check available space
            free_space = sum(1 for block in self.memory_blocks if block == "Free")
            if process_size > free_space:
                messagebox.showerror("Error", "Not enough free memory to allocate the process.")
                return

            # Allocation based on algorithm
            allocated = False
            if algorithm == "First Fit":
                allocated = self.first_fit(process_name, process_size)
            elif algorithm == "Best Fit":
                allocated = self.best_fit(process_name, process_size)
            elif algorithm == "Worst Fit":
                allocated = self.worst_fit(process_name, process_size)
            elif algorithm == "Next Fit":
                allocated = self.next_fit(process_name, process_size)

            if allocated:
                self.total_allocated += process_size
                self.process_list_box.insert(tk.END, f"{process_name}: {process_size} units allocated using {algorithm}.")
                messagebox.showinfo("Success", "Memory Allocated Successfully!")
            else:
                messagebox.showwarning("Error", "Could not allocate memory. Try again.")

            self.update_memory_canvas()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid process details.")

    def first_fit(self, process_name, process_size):
        for i in range(len(self.memory_blocks) - process_size + 1):
            if all(block == "Free" for block in self.memory_blocks[i:i+process_size]):
                for j in range(i, i+process_size):
                    self.memory_blocks[j] = process_name
                self.processes.append((process_name, process_size))
                return True
        return False

    def best_fit(self, process_name, process_size):
        best_start = -1
        best_size = float("inf")

        i = 0
        while i < len(self.memory_blocks):
            if self.memory_blocks[i] == "Free":
                start = i
                while i < len(self.memory_blocks) and self.memory_blocks[i] == "Free":
                    i += 1
                size = i - start
                if process_size <= size < best_size:
                    best_start = start
                    best_size = size
            i += 1

        if best_start != -1:
            for i in range(best_start, best_start + process_size):
                self.memory_blocks[i] = process_name
            self.processes.append((process_name, process_size))
            return True
        return False

    def worst_fit(self, process_name, process_size):
        worst_start = -1
        worst_size = -1

        i = 0
        while i < len(self.memory_blocks):
            if self.memory_blocks[i] == "Free":
                start = i
                while i < len(self.memory_blocks) and self.memory_blocks[i] == "Free":
                    i += 1
                size = i - start
                if size >= process_size and size > worst_size:
                    worst_start = start
                    worst_size = size
            i += 1

        if worst_start != -1:
            for i in range(worst_start, worst_start + process_size):
                self.memory_blocks[i] = process_name
            self.processes.append((process_name, process_size))
            return True
        return False

    def next_fit(self, process_name, process_size):
        start_pos = self.last_allocated_position
        i = start_pos

        while True:
            if all(self.memory_blocks[j % self.memory_size] == "Free" for j in range(i, i + process_size)):
                for j in range(i, i + process_size):
                    self.memory_blocks[j % self.memory_size] = process_name
                self.last_allocated_position = (i + process_size) % self.memory_size
                self.processes.append((process_name, process_size))
                return True
            i = (i + 1) % self.memory_size
            if i == start_pos:  # We've looped back to the start position
                break
        return False

    def resize_memory(self):
        try:
            new_size = int(self.resize_memory_entry.get())
            if new_size <= 0:
                raise ValueError("Memory size must be positive.")

            if new_size > self.memory_size:
                self.memory_blocks.extend(["Free"] * (new_size - self.memory_size))
            elif new_size < self.memory_size:
                if any(block != "Free" for block in self.memory_blocks[new_size:]):
                    messagebox.showerror("Error", "Cannot shrink memory: Allocated blocks would be lost.")
                    return
                self.memory_blocks = self.memory_blocks[:new_size]

            self.memory_size = new_size
            self.update_memory_canvas()
            messagebox.showinfo("Success", f"Memory resized to {self.memory_size} units.")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid memory size.")

    def detect_leaks(self):
        leaks = []
        for i, block in enumerate(self.memory_blocks):
            if block != "Free" and random.choice([True, False]):  # Randomly simulate a leak
                leaks.append(i)
                self.memory_blocks[i] = "Leaked"

        self.update_memory_canvas()

        if leaks:
            messagebox.showinfo("Leaks Detected", f"Memory leaks detected at blocks: {', '.join(map(str, leaks))}")
        else:
            messagebox.showinfo("No Leaks", "No memory leaks detected.")

    def deallocate_memory(self):
        try:
            selected = self.process_list_box.curselection()
            if not selected:
                raise ValueError("No process selected")

            process_details = self.process_list_box.get(selected[0])
            process_name = process_details.split(":")[0]

            deallocated_size = 0
            for i in range(len(self.memory_blocks)):
                if self.memory_blocks[i] == process_name:
                    self.memory_blocks[i] = "Free"
                    deallocated_size += 1

            self.process_list_box.delete(selected[0])
            self.processes = [p for p in self.processes if p[0] != process_name]

            self.total_allocated -= deallocated_size
            self.total_deallocated += deallocated_size

            messagebox.showinfo("Success", "Memory Deallocated Successfully!")
            self.update_memory_canvas()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def reset_memory(self):
        self.memory_blocks = ["Free"] * self.memory_size
        self.processes.clear()
        self.process_list_box.delete(0, tk.END)
        self.total_allocated = 0
        self.total_deallocated = 0
        self.last_allocated_position = 0
        self.update_memory_canvas()
        messagebox.showinfo("Success", "Memory Reset Successfully!")

    def fragmentation_analysis(self):
        free_blocks = []
        i = 0

        while i < len(self.memory_blocks):
            if self.memory_blocks[i] == "Free":
                start = i
                while i < len(self.memory_blocks) and self.memory_blocks[i] == "Free":
                    i += 1
                free_blocks.append(i - start)
            else:
                i += 1

        internal_fragments = len([block for block in free_blocks if block < 5])
        external_fragmentation = sum(free_blocks)

        messagebox.showinfo(
            "Fragmentation Analysis",
            f"Total Free Blocks: {len(free_blocks)}\nInternal Fragments (<5 units): {internal_fragments}\nExternal Fragmentation (Total Free Space): {external_fragmentation}"
        )

    def update_memory_canvas(self):
        self.memory_canvas.delete("all")
        block_width = 850 / self.memory_size

        for i, block in enumerate(self.memory_blocks):
            color = "green" if block == "Free" else ("red" if block == "Leaked" else "blue")
            self.memory_canvas.create_rectangle(i * block_width, 0, (i+1) * block_width, 50, fill=color, outline="black")
            self.memory_canvas.create_text((i + 0.5) * block_width, 25, text=block, fill="white" if block != "Free" else "black")

        self.stats_label.config(text=f"Total Allocated: {self.total_allocated} | Total Deallocated: {self.total_deallocated} | Free Space: {self.memory_size - self.total_allocated}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryAllocationSimulator(root)
    root.mainloop()

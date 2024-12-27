import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math

class PERTTask:
    def __init__(self, name, optimistic_duration, most_likely_duration, pessimistic_duration):
        self.name = name
        self.optimistic_duration = optimistic_duration
        self.most_likely_duration = most_likely_duration
        self.pessimistic_duration = pessimistic_duration

        self.calculate_pert_values()

    def calculate_pert_values(self):
        self.expected = (self.optimistic_duration + 4 * self.most_likely_duration + self.pessimistic_duration) / 6.0
        self.variance = ((self.pessimistic_duration - self.optimistic_duration) / 6.0) ** 2
        self.standard_deviation = math.sqrt(self.variance)

class PERTCalculatorGUI:
    def __init__(self):
        self.tasks = []
        self.project_time = 0.0
        self.project_variance = 0.0
        self.project_standard_deviation = 0.0

        self.root = tk.Tk()
        self.root.title("PERT ")

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates to center the main window
        x = (screen_width - 400) / 2
        y = (screen_height - 400) / 2

        self.root.geometry(f"700x450+{int(x)}+{int(y)}")

        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.LabelFrame(self.root, text="Task Information", padding=(10, 5), relief="groove")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        output_frame = ttk.Frame(self.root)
        output_frame.grid(row=1, column=0, padx=10, pady=10)

        tk.Label(input_frame, text="Task Name", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(input_frame, text="Optimistic Duration", font=("Helvetica", 12)).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(input_frame, text="Most Likely Duration", font=("Helvetica", 12)).grid(row=0, column=2, padx=5, pady=5)
        tk.Label(input_frame, text="Pessimistic Duration", font=("Helvetica", 12)).grid(row=0, column=3, padx=5, pady=5)

        style = ttk.Style()

        style.configure("TEntry", padding=5, font=("Helvetica", 12), background="#EFEFEF")  # Light gray background

        self.name_entry = ttk.Entry(input_frame, style="TEntry")
        self.optimistic_entry = ttk.Entry(input_frame, style="TEntry")
        self.most_likely_entry = ttk.Entry(input_frame, style="TEntry")
        self.pessimistic_entry = ttk.Entry(input_frame, style="TEntry")

        self.name_entry.grid(row=1, column=0, padx=5, pady=5)
        self.optimistic_entry.grid(row=1, column=1, padx=5, pady=5)
        self.most_likely_entry.grid(row=1, column=2, padx=5, pady=5)
        self.pessimistic_entry.grid(row=1, column=3, padx=5, pady=5)

        style.configure("TButton", padding=5, font=("Helvetica", 12), background="#4CAF50", foreground="#000000")  # Green background, black text

        ttk.Button(input_frame, text="Calculate PERT", command=self.calculate_pert, style="TButton").grid(row=2, column=0, columnspan=4, pady=(10, 0))
        ttk.Button(input_frame, text="Clear Screen", command=self.clear_screen, style="TButton").grid(row=3, column=0, columnspan=4, pady=(10, 0))

        self.output_text = tk.Text(output_frame, height=10, width=30, font=("Helvetica", 12))
        self.output_text.config(state="disabled", wrap="word")
        self.output_text.grid(row=0, column=0)

    def calculate_pert(self):
        try:
            name = self.name_entry.get()
            optimistic = int(self.optimistic_entry.get())
            most_likely = int(self.most_likely_entry.get())
            pessimistic = int(self.pessimistic_entry.get())

            task = PERTTask(name, optimistic, most_likely, pessimistic)
            self.tasks.append(task)

            self.calculate_pert_values()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numerical values for time estimates.")

    def calculate_pert_values(self):
        total_expected = 0.0
        total_variance = 0.0

        for task in self.tasks:
            task_expected = task.expected
            task_variance = task.variance

            total_expected += task_expected
            total_variance += task_variance

        self.project_time = total_expected
        self.project_variance = total_variance
        self.project_standard_deviation = math.sqrt(total_variance)

        self.display_pert_results()

    def display_pert_results(self):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)

        self.output_text.insert(tk.END, f"PERT Project Time: {self.project_time:.2f}\n")
        self.output_text.insert(tk.END, f"Variance of Total Project: {self.project_variance:.2f}\n")
        self.output_text.insert(tk.END, f"Standard Deviation: {self.project_standard_deviation:.2f}\n")
        self.output_text.insert(tk.END, "Probability of Completion:\n")

        for task in self.tasks:
            probability = self.calculate_probability(task.expected, task.variance)
            self.output_text.insert(tk.END, f"{task.name}: {probability:.2f}\n")

        self.output_text.config(state="disabled")

    def calculate_probability(self, expected, variance):
        z = (self.project_time - expected) / self.project_standard_deviation
        return 1 - self.cumulative_distribution(z)

    def cumulative_distribution(self, z):
        t = 1 / (1 + 0.2316419 * abs(z))
        y = (((((1.330274429 * t - 1.821255978) * t + 1.781477937) * t - 0.356563782) * t + 0.319381530) * t) / (2 * math.pi) + 0.5

        if z > 0:
            return 1 - y
        else:
            return y

    def clear_screen(self):
        self.tasks.clear()
        self.project_time = 0.0
        self.project_variance = 0.0
        self.project_standard_deviation = 0.0
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")
        self.name_entry.delete(0, tk.END)
        self.optimistic_entry.delete(0, tk.END)
        self.most_likely_entry.delete(0, tk.END)
        self.pessimistic_entry.delete(0, tk.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    pert_calculator = PERTCalculatorGUI()
    pert_calculator.run()

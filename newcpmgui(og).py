import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk


class Task:
    name = None
    duration = 0
    early_start = 0
    early_finish = 0
    late_start = 0
    late_finish = 0
    slack = 0
    is_critical = None
    dependencies = []

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.dependencies = []
        self.is_critical = False

    def add_dependency(self, dependency):
        self.dependencies.append(dependency)


G = nx.Graph()
nodes = []
node_colors = {}


class Cpm:
    def get_input(self, tasks, num_task, entry_tasks):
        for i in range(num_task):
            name = str(entry_tasks[i][0])
            duration = int(entry_tasks[i][1])
            dependency_names = entry_tasks[i][2]

            list_of_dependency = dependency_names.split(',')

            nodes.append(name)
            add_task = Task(name.strip(), duration)
            tasks.append(add_task)

            if i == 0:
                continue

            dependency_found = False

            for name_dependency in list_of_dependency:
                if not name_dependency.strip():
                    return print("dep should not be empty")
                else:
                    for task in tasks:
                        if task.name == name_dependency.strip():
                            add_task.add_dependency(task)
                            G.add_edges_from([(task.name, name)])
                            dependency_found = True

                    if not dependency_found:
                        print("Task does not exist")

    def display_tasks(self, tasks):
        for task in tasks:
            print("\n\nname : ", task.name)
            print("duration : ", task.duration)
            print("Early_start : ", task.early_start)
            print("Early_finish : ", task.early_finish)
            print("Late_start :", task.late_start)
            print("Late_finish :", task.late_finish)
            print("SLACK TIME : ", task.slack)
            for name in task.dependencies:
                print(name.name, end="  ")

            for task in tasks:
                if task.slack == 0:
                    task.is_critical = True
                    node_colors[task.name] = "red"
                else:
                    node_colors[task.name] = "skyblue"

        pos = nx.spring_layout(G)
        print("\n\n Node colors :", node_colors)
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700,
                font_color='black', node_color=list(node_colors.values()), font_size=10)
        plt.show()

    def calculateCPM(self, tasks):
        tasks[0].early_start = 0
        tasks[0].early_finish = tasks[0].duration
        max_finish_time = 0

        for j in range(1, len(tasks)):
            current_task = tasks[j]

            for task_dependency in current_task.dependencies:
                max_finish_time = max(
                    max_finish_time, task_dependency.early_finish)

            current_task.early_start = max_finish_time
            current_task.early_finish = max_finish_time + current_task.duration

        last_task = tasks[len(tasks)-1]
        last_task.late_finish = last_task.early_finish
        last_task.late_start = last_task.late_finish - last_task.duration

        # Backward Pass
        for k in range(len(tasks)-2, -1, -1):
            current_task = tasks[k]
            check_late_finish = 0

            for search_task in tasks:
                if current_task in search_task.dependencies:
                    if current_task.late_finish == 0:
                        current_task.late_finish = search_task.late_start
                        current_task.late_start = current_task.late_finish - current_task.duration
                    else:
                        check_late_finish = search_task.late_start
                        current_task.late_finish = min(
                            current_task.late_finish, check_late_finish)
                        current_task.late_start = current_task.late_finish - current_task.duration

            current_task.slack = current_task.late_finish - current_task.early_finish


class GUI:

    def __init__(self):
        self.num_task = None
        self.task_data = []

    def display_gui(self, tasks):
        def newwindow():
            self.num_task = int(en1.get())

            base = tk.Tk()
            base.geometry("400x800")
            base.title("Inputs")
           
           

            tasks_gui = []
            for i in range(self.num_task):
                task_frame = ttk.Frame(base, padding="10")
                task_frame.grid(row=i, column=0, sticky="w")

                label = ttk.Label(task_frame, text=f"Name of Task {i + 1}:")
                label.grid(row=1, column=0, sticky="w")
                entry = ttk.Entry(task_frame)
                entry.grid(row=1, column=1, sticky="w")

                label2 = ttk.Label(task_frame, text=f"Duration of Task {i + 1}:")
                label2.grid(row=2, column=0, sticky="w")
                entry2 = ttk.Entry(task_frame)
                entry2.grid(row=2, column=1, sticky="w")

                label3 = ttk.Label(task_frame, text=f"Name of Dependencies:")
                label3.grid(row=3, column=0, sticky="w")
                entry3 = ttk.Entry(task_frame)
                entry3.grid(row=3, column=1, sticky="w")

                tasks_gui.append({
                    'name': entry,
                    'duration': entry2,
                    'dependencies': entry3
                })

            def submit():
                # Clear the existing tasks
                tasks.clear()
                
                for task in tasks_gui:
                    name = task['name'].get()
                    duration = task['duration'].get()
                    dependencies = task['dependencies'].get()
                    g.task_data.append([name, duration, dependencies])

                c = Cpm()
                c.get_input(num_task=g.num_task, tasks=tasks, entry_tasks=g.task_data)
                c.calculateCPM(tasks=tasks)
                submit_task(base, tasks)
                c.display_tasks(tasks)

            def submit_task(base, tasks):
                task_info = []
                for task in tasks:
                    name = task.name
                    duration = task.duration
                    early_start = task.early_start
                    early_finish = task.early_finish
                    late_start = task.late_start
                    late_finish = task.late_finish
                    slack = task.slack
                    dependencies = ', '.join(dep.name for dep in task.dependencies)

                    task_info.append((name, duration, early_start, early_finish, late_start, late_finish, slack, dependencies))

                new_window = tk.Toplevel(base)
                new_window.title("Task Information")

                table_frame = ttk.Frame(new_window)
                table_frame.pack(fill=tk.BOTH, expand=True)

                columns = ['Name', 'Duration', 'Early Start', 'Early Finish', 'Late Start', 'Late Finish', 'Slack', 'Dependencies']
                treeview = ttk.Treeview(table_frame, columns=columns, show='headings')
                for col in columns:
                    treeview.heading(col, text=col)

                for task in task_info:
                     treeview.insert('', 'end', values=task)

                treeview.pack(fill=tk.BOTH, expand=True)    
            
                    

                # base.destroy()  # Close the window after submitting

            submit_button = ttk.Button(base, text="Submit", command= lambda:[submit()])
            submit_button.grid(row= self.num_task + 1, column=0, pady=10)

            base.mainloop()  # Run the new window loop

            # print(self.task_data)  # Print the collected data after the window is closed

        root = tk.Tk()
        root.geometry("400x250")
        root.title("CPM")
        root.configure(bg="slategray2")

        lb1 = ttk.Label(root, text="Number of Tasks", width=15, background="slategray2", font=("arial", 12))
        lb1.place(x=120, y=100)
        en1 = ttk.Entry(root, width=10,text=5)
        en1.place(x=250, y=100)

        submit_button = ttk.Button(root, text="Submit", width=10, command=newwindow)
        submit_button.place(x=175, y=150)

        root.mainloop()

tasks = []
g = GUI()
task_data = g.display_gui(tasks)



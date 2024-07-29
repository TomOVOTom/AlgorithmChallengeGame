import tkinter as tk
import random
import time
import json

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("算法挑战游戏")
        self.score = 0
        self.total_time = 0
        self.start_time = None
        self.leaderboard = Leaderboard()
        self.create_widgets()
        self.generate_problem()

    def create_widgets(self):
        self.problem_label = tk.Label(self.root, text="", font=("Courier", 16))
        self.problem_label.pack(pady=20)

        self.answer_entry = tk.Entry(self.root, font=("Courier", 16))
        self.answer_entry.pack(pady=20)
        self.answer_entry.bind("<Return>", self.check_answer)

        self.submit_button = tk.Button(self.root, text="提交答案", command=self.check_answer, font=("Courier", 16))
        self.submit_button.pack(pady=20)

        self.result_label = tk.Label(self.root, text="", font=("Courier", 16))
        self.result_label.pack(pady=20)

        self.score_label = tk.Label(self.root, text="得分: 0", font=("Courier", 16))
        self.score_label.pack(pady=20)

        self.time_label = tk.Label(self.root, text="总用时: 0秒", font=("Courier", 16))
        self.time_label.pack(pady=20)

        self.leaderboard_button = tk.Button(self.root, text="查看排行榜", command=self.show_leaderboard, font=("Courier", 16))
        self.leaderboard_button.pack(pady=20)

    def generate_problem(self):
        self.num1 = random.randint(1, 100)
        self.num2 = random.randint(1, 100)
        self.problem_label.config(text=f"{self.num1} + {self.num2} = ?")
        self.answer_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.start_time = time.time()

    def check_answer(self, event=None):
        try:
            answer = int(self.answer_entry.get())
            end_time = time.time()
            time_taken = end_time - self.start_time
            self.total_time += time_taken
            if answer == self.num1 + self.num2:
                self.score += 1
                self.result_label.config(text="正确!", fg="green")
            else:
                self.result_label.config(text="错误!", fg="red")
            self.score_label.config(text=f"得分: {self.score}")
            self.time_label.config(text=f"总用时: {int(self.total_time)}秒")
            self.root.after(500, self.generate_problem)
        except ValueError:
            self.result_label.config(text="请输入一个有效的数字", fg="red")

    def show_leaderboard(self):
        self.leaderboard.update(self.score, self.total_time)
        self.leaderboard.show()

class Leaderboard:
    def __init__(self):
        self.records = self.load_records()

    def load_records(self):
        try:
            with open('leaderboard.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_records(self):
        with open('leaderboard.json', 'w') as file:
            json.dump(self.records, file)

    def update(self, score, total_time):
        self.records.append({'score': score, 'time': total_time})
        self.records = sorted(self.records, key=lambda x: (-x['score'], x['time']))
        self.save_records()

    def show(self):
        leaderboard_window = tk.Toplevel()
        leaderboard_window.title("排行榜")
        for idx, record in enumerate(self.records[:10], start=1):
            tk.Label(leaderboard_window, text=f"{idx}. 得分: {record['score']}, 用时: {int(record['time'])}秒", font=("Courier", 16)).pack(pady=5)

root = tk.Tk()
game = Game(root)
root.mainloop()
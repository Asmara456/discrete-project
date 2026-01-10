import tkinter as tk
from tkinter import messagebox
import math

try:
    import winsound
    WINDOWS = True
except:
    WINDOWS = False


import winsound

def play_alarm():
    # A repeating high-low siren pattern using built-in winsound.Beep()
    for i in range(5):  # Number of cycles
        winsound.Beep(1200, 300)  # High tone
        winsound.Beep(700, 300)   # Low tone

class Student:
    def __init__(self, sid, row, col):
        self.sid = sid
        self.row = row
        self.col = col


class ExamGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Anti-Cheating Monitor – Attractive GUI Edition")
        self.root.geometry("1150x720")
        self.root.configure(bg="#f3eaff")

        self.rows = 15
        self.cols = 15
        self.next_id = 1
        self.students = {}
        self.min_distance = 1.4

        self.grid_buttons = {}

        self.build_header()
        self.build_grid()
        self.build_controls()
        self.build_footer()
        self.build_legend()

    # ---------------- Header ----------------
    def build_header(self):
        header = tk.Label(
            self.root,
            text="ANTI-CHEATING SEATING MONITOR",
            font=("Comic Sans MS", 26, "bold"),
            fg="#ffffff",
            bg="#7b2cbf",
            padx=20,
            pady=12
        )
        header.pack(fill="x")

    # ---------------- Footer ----------------
    def build_footer(self):
        footer = tk.Label(
            self.root,
            text="Project by • Your Name",
            font=("Comic Sans MS", 14),
            fg="#ffffff",
            bg="#9d4edd",
            pady=8
        )
        footer.pack(fill="x", side="bottom")

    # ---------------- Legend ----------------
    def build_legend(self):
        legend_frame = tk.Frame(self.root, bg="#f3eaff")
        legend_frame.pack(pady=8)

        items = [
            ("⚪ White", "Student Seated"),
            ("🟧 Orange", "Warning (Row/Column Risk)"),
            ("🟥 Red", "High Risk (Too Close)"),
        ]

        for color, meaning in items:
            tk.Label(
                legend_frame,
                text=f"{color}  =  {meaning}",
                font=("Arial", 12),
                bg="#f3eaff"
            ).pack(anchor="w")

    # ---------------- Grid ----------------
    def build_grid(self):
        grid_frame = tk.Frame(self.root, bg="#f3eaff")
        grid_frame.pack(pady=20)

        # Column labels (BLACK)
        for c in range(self.cols):
            tk.Label(
                grid_frame,
                text=str(c + 1),
                font=("Arial", 10, "bold"),
                fg="black",
                bg="#f3eaff"
            ).grid(row=0, column=c + 1)

        # Grid buttons
        for r in range(self.rows):

            # Row labels (BLACK)
            tk.Label(
                grid_frame,
                text=chr(65 + r),
                font=("Arial", 10, "bold"),
                fg="black",
                bg="#f3eaff"
            ).grid(row=r + 1, column=0, padx=4)

            for c in range(self.cols):

                btn = tk.Button(
                    grid_frame,
                    text="",
                    width=3,
                    height=1,
                    bg="#e7d6ff",
                    activebackground="#d8c4ff",
                    relief="raised",
                    bd=2,
                    command=lambda x=r, y=c: self.toggle_seat(x, y)
                )

                # Hover effect
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#d8c4ff"))
                btn.bind("<Leave>", lambda e, b=btn, r=r, c=c: self.reset_hover(b, r, c))

                btn.grid(row=r + 1, column=c + 1, padx=2, pady=2)
                self.grid_buttons[(r, c)] = btn

    # Reset hover depending on seat status
    def reset_hover(self, btn, r, c):
        if (r, c) in self.students:
            btn.config(bg="white")
        else:
            btn.config(bg="#e7d6ff")

    # ---------------- Controls ----------------
    def build_controls(self):
        control_frame = tk.Frame(self.root, bg="#f3eaff")
        control_frame.pack(pady=10)

        analyze_btn = tk.Button(
            control_frame,
            text="Analyze Cheating Risk 🔍",
            font=("Comic Sans MS", 14, "bold"),
            bg="#5a189a",
            fg="white",
            padx=20,
            pady=5,
            activebackground="#7b2cbf",
            command=self.analyze_seats
        )
        analyze_btn.grid(row=0, column=0, padx=20)

        clear_btn = tk.Button(
            control_frame,
            text="Clear All ❌",
            font=("Comic Sans MS", 14, "bold"),
            bg="#c9184a",
            fg="white",
            padx=20,
            pady=5,
            activebackground="#ff758f",
            command=self.reset_all
        )
        clear_btn.grid(row=0, column=1, padx=20)

    # ---------------- Toggle Seat ----------------
    def toggle_seat(self, r, c):
        btn = self.grid_buttons[(r, c)]
        if (r, c) in self.students:
            del self.students[(r, c)]
            btn.config(bg="#e7d6ff", text="")
        else:
            self.students[(r, c)] = Student(self.next_id, r, c)
            self.next_id += 1
            btn.config(bg="white", text="●")

    # ---------------- Analysis ----------------
    def analyze_seats(self):
        for pos, btn in self.grid_buttons.items():
            if pos in self.students:
                btn.config(bg="white")
            else:
                btn.config(bg="#e7d6ff")

        warnings = []
        high_risk = False
        student_list = list(self.students.values())

        for i in range(len(student_list)):
            for j in range(i + 1, len(student_list)):
                s1 = student_list[i]
                s2 = student_list[j]

                # Same row
                if s1.row == s2.row:
                    self.mark_warning((s1.row, s1.col))
                    self.mark_warning((s2.row, s2.col))
                    warnings.append(f"Row conflict: Student {s1.sid} & {s2.sid}")

                # Same column
                if s1.col == s2.col:
                    self.mark_warning((s1.row, s1.col))
                    self.mark_warning((s2.row, s2.col))
                    warnings.append(f"Column conflict: Student {s1.sid} & {s2.sid}")

                # Distance check
                dist = math.dist((s1.row, s1.col), (s2.row, s2.col))
                if dist < self.min_distance:
                    self.mark_high_risk((s1.row, s1.col))
                    self.mark_high_risk((s2.row, s2.col))
                    warnings.append(f"TOO CLOSE: Student {s1.sid} & {s2.sid}")
                    high_risk = True

        if high_risk:
            play_alarm()

        if warnings:
            messagebox.showwarning("Cheating Risks Found", "\n".join(warnings))
        else:
            messagebox.showinfo("Success", "No cheating risks detected.")

    def mark_warning(self, pos):
        self.grid_buttons[pos].config(bg="orange")

    def mark_high_risk(self, pos):
        self.grid_buttons[pos].config(bg="red")

    def reset_all(self):
        self.students.clear()
        self.next_id = 1
        for btn in self.grid_buttons.values():
            btn.config(bg="#e7d6ff", text="")


# ---------------- Run ----------------
root = tk.Tk()
app = ExamGUI(root)
root.mainloop()
import tkinter as tk
from tkinter import ttk
import random

# ------------------------- Quiz Data -------------------------
QUESTIONS = [
    {
        "q": "Which protocol secures web traffic (the 'S' in HTTPS)?",
        "options": ["SSL/TLS", "FTP", "SMTP", "SSH"],
        "answer": 0,
    },
    {
        "q": "Which data structure uses First-In-First-Out (FIFO)?",
        "options": ["Stack", "Queue", "Tree", "Graph"],
        "answer": 1,
    },
    {
        "q": "Which is a supervised ML task?",
        "options": ["Clustering", "PCA", "Classification", "t-SNE"],
        "answer": 2,
    },
    {
        "q": "Which SQL clause filters rows before grouping?",
        "options": ["HAVING", "WHERE", "GROUP BY", "ORDER BY"],
        "answer": 1,
    },
    {
        "q": "In Python, which creates a list comprehension?",
        "options": ["{x for x in ...}", "(x for x in ...)", "[x for x in ...]", "list(x for x in ...)"],
        "answer": 2,
    },
]

# ------------------------- Config -------------------------
QUESTION_TIME = 15            # seconds per question
BASE_POINTS = 500             # base + (time_left * multiplier)
TIME_MULTIPLIER = 20
AUTO_NEXT_DELAY_MS = 1100     # auto-advance after showing feedback

# ------------------------- App -------------------------
class KahootQuiz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kahoot-style Quiz (Tkinter)")
        self.geometry("760x480")
        self.minsize(680, 420)
        self.configure(bg="#0f172a")  # dark slate

        # State
        self.score = 0
        self.q_index = -1
        self.time_left = QUESTION_TIME
        self.timer_job = None
        self.locked = False

        # Prepare question order with shuffled options per question
        self.questions = self._prepare_questions(QUESTIONS)

        # UI
        self._build_ui()
        self.next_question()

    # Shuffle options for each question while preserving correct index
    def _prepare_questions(self, raw):
        out = []
        for item in raw:
            opts_idx = list(enumerate(item["options"]))
            random.shuffle(opts_idx)
            options = [t[1] for t in opts_idx]
            # new answer index after shuffle:
            new_ans = next(i for i, (old_i, _) in enumerate(opts_idx) if old_i == item["answer"])
            out.append({"q": item["q"], "options": options, "answer": new_ans})
        random.shuffle(out)
        return out

    def _build_ui(self):
        # Top bar
        top = tk.Frame(self, bg="#0f172a")
        top.pack(fill="x", padx=16, pady=12)

        self.title_lbl = tk.Label(top, text="Kahoot-style Quiz", fg="#e2e8f0", bg="#0f172a",
                                  font=("Segoe UI", 18, "bold"))
        self.title_lbl.pack(side="left")

        self.score_lbl = tk.Label(top, text="Score: 0", fg="#a5b4fc", bg="#0f172a",
                                  font=("Segoe UI", 14, "bold"))
        self.score_lbl.pack(side="right", padx=(8, 0))

        # Timer + Progress
        mid = tk.Frame(self, bg="#0f172a")
        mid.pack(fill="x", padx=16)

        self.timer_lbl = tk.Label(mid, text=f"Time: {QUESTION_TIME}s", fg="#f8fafc", bg="#0f172a",
                                  font=("Segoe UI", 12, "bold"))
        self.timer_lbl.pack(anchor="w")

        self.progress = ttk.Progressbar(mid, maximum=QUESTION_TIME, length=300)
        self.progress.pack(anchor="w", pady=(4, 10))
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TProgressbar", troughcolor="#1e293b", background="#60a5fa", bordercolor="#1e293b")

        # Question
        self.question_lbl = tk.Label(self, text="", wraplength=700, justify="left",
                                     fg="#f1f5f9", bg="#0f172a", font=("Segoe UI", 16))
        self.question_lbl.pack(fill="x", padx=16, pady=(10, 6))

        # Options (Radiobuttons)
        self.selected = tk.IntVar(value=-1)
        self.option_frames = []
        self.radio_buttons = []

        options_frame = tk.Frame(self, bg="#0f172a")
        options_frame.pack(fill="both", expand=True, padx=16)

        for i in range(4):
            f = tk.Frame(options_frame, bg="#111827", highlightthickness=1, highlightbackground="#1f2937")
            f.pack(fill="x", pady=6)
            rb = tk.Radiobutton(
                f, text=f"Option {i+1}", variable=self.selected, value=i,
                command=self.on_select,
                font=("Segoe UI", 13), anchor="w", justify="left",
                bg="#111827", fg="#e5e7eb", selectcolor="#111827",
                activebackground="#111827", activeforeground="#e5e7eb", padx=12, pady=10
            )
            rb.pack(fill="x")
            self.option_frames.append(f)
            self.radio_buttons.append(rb)

        # Feedback
        self.feedback_lbl = tk.Label(self, text="", fg="#fecaca", bg="#0f172a",
                                     font=("Segoe UI", 13, "bold"))
        self.feedback_lbl.pack(padx=16, pady=(6, 0), anchor="w")

        # Bottom bar
        bottom = tk.Frame(self, bg="#0f172a")
        bottom.pack(fill="x", padx=16, pady=12)

        self.next_btn = tk.Button(bottom, text="Next ▶", command=self.next_question,
                                  font=("Segoe UI", 12, "bold"),
                                  bg="#22c55e", fg="#0b1320", activebackground="#16a34a",
                                  relief="flat", padx=16, pady=8)
        self.next_btn.pack(side="right")

        self.reset_btn = tk.Button(bottom, text="Restart ↻", command=self.restart,
                                   font=("Segoe UI", 11),
                                   bg="#334155", fg="#e2e8f0", activebackground="#1f2937",
                                   relief="flat", padx=12, pady=6)
        self.reset_btn.pack(side="left")

    def restart(self):
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        self.score = 0
        self.q_index = -1
        self.time_left = QUESTION_TIME
        self.score_lbl.config(text="Score: 0")
        self.feedback_lbl.config(text="")
        self.questions = self._prepare_questions(QUESTIONS)
        self.unlock_options()
        self.next_question()

    def on_select(self):
        if self.locked:
            return
        self.locked = True
        sel = self.selected.get()
        correct = self.questions[self.q_index]["answer"]

        # Stop timer
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None

        # Score: faster = more points
        if sel == correct:
            gained = BASE_POINTS + self.time_left * TIME_MULTIPLIER
            self.score += gained
            self.score_lbl.config(text=f"Score: {self.score}")
            self.feedback_lbl.config(text=f"✅ Correct! +{gained} pts")
        else:
            self.feedback_lbl.config(text=f"❌ Wrong! Correct answer highlighted.")

        # Highlight
        for i, f in enumerate(self.option_frames):
            if i == correct:
                f.configure(bg="#064e3b")  # green-ish
                self.radio_buttons[i].configure(bg="#064e3b")
            elif i == sel:
                f.configure(bg="#7f1d1d")  # red-ish
                self.radio_buttons[i].configure(bg="#7f1d1d")

        self.disable_options()
        # Auto-advance after short delay
        self.after(AUTO_NEXT_DELAY_MS, self.next_question)

    def disable_options(self):
        for rb in self.radio_buttons:
            rb.configure(state="disabled")

    def unlock_options(self):
        for f in self.option_frames:
            f.configure(bg="#111827")
        for rb in self.radio_buttons:
            rb.configure(state="normal", bg="#111827")
        self.selected.set(-1)
        self.locked = False

    def next_question(self):
        # End if finished
        self.q_index += 1
        if self.q_index >= len(self.questions):
            self.end_quiz()
            return

        # Reset per-question UI
        self.unlock_options()
        self.feedback_lbl.config(text="")
        self.time_left = QUESTION_TIME
        self.timer_lbl.config(text=f"Time: {self.time_left}s")
        self.progress["value"] = self.time_left

        q = self.questions[self.q_index]
        self.title_lbl.config(text=f"Question {self.q_index + 1} / {len(self.questions)}")
        self.question_lbl.config(text=q["q"])
        for i, text in enumerate(q["options"]):
            self.radio_buttons[i].config(text=text)

        # Start timer
        self._tick()

    def _tick(self):
        self.progress["value"] = self.time_left
        self.timer_lbl.config(text=f"Time: {self.time_left}s")
        if self.time_left <= 0:
            # Time up → mark as wrong, reveal correct, auto-next
            self.locked = True
            self.disable_options()
            correct = self.questions[self.q_index]["answer"]
            for i, f in enumerate(self.option_frames):
                if i == correct:
                    f.configure(bg="#064e3b")
                    self.radio_buttons[i].configure(bg="#064e3b")
            self.feedback_lbl.config(text="⏰ Time's up!")
            self.after(AUTO_NEXT_DELAY_MS, self.next_question)
            return
        self.time_left -= 1
        self.timer_job = self.after(1000, self._tick)

    def end_quiz(self):
        # Clear timer if any
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        self.title_lbl.config(text="Quiz Finished")
        self.question_lbl.config(text=f"Your final score: {self.score}")
        self.feedback_lbl.config(text="Click 'Restart ↻' to play again.")
        for rb in self.radio_buttons:
            rb.config(text="—", state="disabled")
        for f in self.option_frames:
            f.configure(bg="#111827")

# ------------------------- Run -------------------------
if __name__ == "__main__":
    app = KahootQuiz()
    app.mainloop()

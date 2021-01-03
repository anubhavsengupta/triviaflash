from tkinter import *
import requests
import random
import html

totalScore = 0


def main():
    isTrue = None

    class DataBase:
        def __init__(self):

            self.difficulty = 'easy'
            self.currentQuestion = 0
            self.encoding = 'utf-8'
            self.list = []
            self.pairs = {}
            self.question = None
            self.answer = []
            self.amount = 3
            if self.difficulty == "easy":
                self.amount = 3
            elif self.difficulty == "medium":
                self.amount = 5
            elif self.difficulty == "hard":
                self.amount = 10

            self.parameters = {
                "amount": 5,
                "type": "boolean"
            }

        def connect_to_API(self):
            URL = requests.get('https://opentdb.com/api.php', params=self.parameters)
            URL.encoding = self.encoding
            data = URL.json()
            for q in data["results"]:
                self.list.append(html.unescape(q["question"]))
                self.answer.append(q["correct_answer"])
                self.pairs[html.unescape(q["question"])] = q["correct_answer"]
            self.question = random.choice(html.unescape(self.list))

        def check_right_answer_true(self, item, user_answer):
            global totalScore
            self.currentQuestion += 1
            try:
                # if user_answer == self.pairs[item]:
                if self.currentQuestion != len(self.answer):
                    if user_answer == self.answer[self.currentQuestion - 1]:
                        totalScore += 1
                        print("You got it correct")
                        score.config(text=f"Score: {totalScore}")
                        # new
                        screen.configure(bg="green")
                    else:
                        screen.configure(bg="red")
                    screen.after(500, self.change_bg)
                else:
                    if user_answer == self.answer[self.currentQuestion - 1]:
                        totalScore += 1
                        screen.configure(bg="green")
                    else:
                        screen.configure(bg="red")
                    screen.after(500, self.change_bg)
                    score.config(text=f"Score: {totalScore}")
                    question.itemconfig(quote_text, text=f"Game Over, your score was {totalScore} / {len(self.list)}")

            except IndexError:
                question.itemconfig(quote_text, text=f"Game Over, your score was {totalScore} / {len(self.list)}")

        def change_question(self):
            try:
                randomChoice = html.unescape(self.list[self.currentQuestion + 1])
                # randomChoice = random.choice(html.unescape(self.list))

                question.itemconfig(quote_text, text=randomChoice)

                self.check_right_answer_true(randomChoice, "True")
            except IndexError:
                randomChoice = html.unescape(self.list[-1])
                # randomChoice = random.choice(html.unescape(self.list))

                question.itemconfig(quote_text, text=randomChoice)

                self.check_right_answer_true(randomChoice, "True")

        def change_question_false(self):
            try:
                random_choice = html.unescape(self.list[self.currentQuestion + 1])
                # random_choice = random.choice(html.unescape(self.list))

                question.itemconfig(quote_text, text=random_choice)

                self.check_right_answer_true(random_choice, "False")
            except IndexError:
                random_choice = html.unescape(self.list[-1])
                # random_choice = random.choice(html.unescape(self.list))

                question.itemconfig(quote_text, text=random_choice)

                self.check_right_answer_true(random_choice, "False")

        def start(self):
            question.itemconfig(quote_text, text=self.list[0])
            self.currentQuestion = 0

        def change_bg(self):
            screen.configure(bg="#505459")

    db = DataBase()
    db.connect_to_API()

    screen = Tk()

    # Configuration
    screen.title("Trivia")

    screen.configure(bg="#505459")
    screen.config(padx=20, pady=20)
    # User Interface
    start = Button(screen, text="Start", command=db.start)
    start.grid(row=0, column=0)
    score = Label(screen, text="Score: 0", font=("Arial", 30, "bold"), bg="#505459",
                  fg="White")
    score.grid(row=1, column=0)

    question = Canvas(width=280, height=284, bg="#505459", highlightthickness=0)

    question.grid(row=2, column=0)

    textbubble = PhotoImage(file="chat-black-rectangular-rounded-speech-balloon-interface-symbol.png")

    question_image = question.create_image(140, 160, image=textbubble)
    quote_text = question.create_text(150, 150, text=f"Press Start to start", font=("Arial", 15, "bold"),
                                      fill="white", width=200)

    checkboxes = Canvas(screen, bg="#505459", height=150, width=150)
    checkboxes.grid(row=3, column=0)

    img_checkmark = PhotoImage(file='check-mark.png')
    img_X = PhotoImage(file='close.png')

    checkmark = Button(checkboxes, image=img_checkmark, background='#505459', command=db.change_question,
                       highlightthickness=0)

    x_mark = Button(checkboxes, image=img_X, background='#505459', command=db.change_question_false)

    checkmark.pack(side=LEFT)
    x_mark.pack(side=RIGHT)

    screen.mainloop()


main()

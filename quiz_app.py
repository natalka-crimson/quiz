import tkinter as tk
from tkinter import ttk, messagebox
import json
from abc import ABC, abstractmethod


class WelcomeScreen(tk.Tk):
    def __init__(self, topics):
        super().__init__()
        self.topics = topics
        self.show_main_screen()
    
    def show_main_screen(self):
        self.title('Welcome to Quiz App')
        self.geometry('800x500')
        self.configure(bg='light blue')
        
        self.choice_label = tk.Label(self, bg='light blue', fg='black', text='Select a quiz to measure your comprehension:', wraplength=750, font=('Ebrima bold', 22))
        self.choice_label.pack(pady=60)  
        
        center_frame = tk.Frame(self, bg='light blue')
        center_frame.pack(expand=True, pady=(0, 20))
        
        self.choice_buttons = []
        for i in range(2):
            button = tk.Button(center_frame, text='', width=20, height=5, wraplength=190, font=('Ebrima bold', 16), bg='RoyalBlue4', fg='white', activebackground='RoyalBlue1', command=lambda choice=i: self.start_quiz(choice))
            button.pack(side='left', padx=5)
            self.choice_buttons.append(button)
        
        self.update_button_texts()
    
    def update_button_texts(self):
        for i, topic in enumerate(self.topics):
            self.choice_buttons[i].config(text=topic.name)
    
    def start_quiz(self, choice):
        app = QuizApp(self.topics[choice])
        self.destroy()
        app.mainloop()

class AbstractTopic(ABC):
    def __init__(self, link: str):
        self.json_link = link
        self.questions = self.get_questions()
    def get_questions(self):
        try:
            with open(self.json_link, 'r', encoding='UTF-8') as file:
                questions = json.load(file)
        except FileNotFoundError:
            print(f'The file "{self.json_link}" was not found.')
            return None
        except Exception as e:
            print(f'An unexpected error occurred: {e}')
            return None
        else:
            if not isinstance(questions, list):
                print('Invalid JSON format: Expected a list of questions.')
                return None
            return questions
    
    @abstractmethod
    def calc_points(self, points):
        pass

class EnglishTopic(AbstractTopic):
    def __init__(self, link: str):
        super().__init__(link)
        self.name = 'English test'

    def calc_points(self, points):
        que_num = len(self.questions)
        percentage = points / que_num * 100
        result = ''
        if percentage >= 98:
            result = f'Congratulations!\nYour level is: C2 - Proficiency\nYou got {points} out of {que_num}'
        elif percentage >= 90:
            result = f'Awesome result!\nYour level is: C1 - Advanced\nYou got {points} out of {que_num}'
        elif percentage >= 80:
            result = f'Excellent result!\nYour level is: B2 - Upper-Intermediate\nYou got {points} out of {que_num}'
        elif percentage >= 60:
            result = f'Well done!\nYour level is: B1 - Intermediate\nYou got {points} out of {que_num}'
        elif percentage >= 40:
            result = f'Keep studing, you\'re heading in the right direction!\nYour level is: A2 - Elementary\nYou got {points} out of {que_num}'
        elif percentage > 0:
            result = f'Not bad! You\'re on the right path!\nYour level is: A1 - Beginner\nYou got {points} out of {que_num}'
        else:
           result = f'Try hard, learn more!\nYou got {points} out of {que_num}'
        return result

class PythonTopic(AbstractTopic):
    def __init__(self, link: str):
        super().__init__(link)
        self.name = 'Python Basic test'

    def calc_points(self, points):
        que_num = len(self.questions)
        percentage = points / que_num * 100
        result = ''
        if percentage >= 98:
            result = f'Congratulations!\nYou got {points} out of {que_num}'
        elif percentage >= 90:
            result = f'Awesome result!\nYou got {points} out of {que_num}'
        elif percentage >= 80:
            result = f'Excellent result!\nYou got {points} out of {que_num}'
        elif percentage >= 60:
            result = f'Well done!\nYou got {points} out of {que_num}'
        elif percentage >= 40:
            result = f'Keep studing, you\'re heading in the right direction!\nYou got {points} out of {que_num}'
        elif percentage > 0:
            result = f'Not bad! You\'re on the right path!\nYou got {points} out of {que_num}'
        else:
           result = f'Try hard, learn more!\nYou got {points} out of {que_num}'
        return result


class QuizApp(tk.Tk):
    def __init__(self, topic: AbstractTopic):
        super().__init__()
        self.question_set = topic

        self.questions = self.question_set.questions
        self.points = 0
        
        self.current_question_index = 0
        self.show_window()

    def show_window(self):
        self.title('Quiz App')
        self.geometry('800x550')
        self.configure(bg='light blue')

        self.question_label = tk.Label(self, bg='light blue', fg='black', text='', wraplength=750, font=('Ebrima bold', 22))
        self.question_label.pack(pady=60)

        self.answer_buttons = []
        for i in range(0, 4, 2):
            frame = tk.Frame(self)
            frame.configure(bg='light blue')
            frame.pack(side='top', pady=5)
            for j in range(2):
                ans_index = i + j
                button = tk.Button(frame, text='', width=20, wraplength=190, font=('Ebrima', 12), command=lambda ans=ans_index: self.check_answer(ans))
                button.pack(side='left', padx=5)
                self.answer_buttons.append(button)

        self.progress_bar = ttk.Progressbar(self, length=400)
        self.progress_bar.pack(side='bottom', pady=20)

        self.load_question()

    def load_question(self):
        total_questions = len(self.questions)
        progress_value = int((self.current_question_index / total_questions) * 100)
        self.progress_bar['value'] = progress_value
        
        question_data = self.questions[self.current_question_index]
        self.question_label.config(text=question_data['question'])
        for i, answer in enumerate(question_data['answers']):
            self.answer_buttons[i].config(text=answer)


    def check_answer(self, selected_answer_index):
        question_data = self.questions[self.current_question_index]
        selected_answer = question_data['answers'][selected_answer_index]
        correct_answer = question_data['correct_answer']

        if selected_answer == correct_answer:
            self.points += 1
        self.next_question()

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.load_question()
        else:
            self.progress_bar['value'] = 100
            for button in self.answer_buttons:
                button.config(state='disabled')
            self.show_points()
    
    def show_points(self):
        self.points_number = self.question_set.calc_points(self.points)
        result_str = self.points_number
        self.add_buttons()
        messagebox.showinfo('Your result', result_str)
        
    def add_buttons(self):
        self.return_to_main_button = tk.Button(self, text='Select another test', width=15, font=('Ebrima', 12), bg='LightGoldenrod1', activebackground='LightGoldenrod2', command=self.return_to_main_screen)
        self.return_to_main_button.pack(side='bottom', pady=10)
        
        self.try_again_button = tk.Button(self, text='Try again', width=15, font=('Ebrima', 12), bg='RosyBrown2', activebackground='RosyBrown3', command=self.start_again)
        self.try_again_button.pack(side='bottom', pady=10)
        
        self.show_answers_button = tk.Button(self, text='Show answers', width=15, font=('Ebrima', 12), bg='DarkSeaGreen2', activebackground='DarkSeaGreen3', command=self.show_answers)
        self.show_answers_button.pack(side='bottom', pady=10)

    def show_answers(self):
        result_window = tk.Toplevel(self)
        result_window.title('Correct answers')
        result_window.geometry('850x700')
        result_window.config(bg='light blue')

        result_text = tk.Text(result_window, bg='light blue', wrap='word', font=('Ebrima', 12))

        scrollbar = tk.Scrollbar(result_window, command=result_text.yview)
        result_text.config(yscrollcommand=scrollbar.set)

        result_text.pack(side='left', padx=20, pady=20, expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')

        for i, question_data in enumerate(self.questions):
            result_text.insert('end', '{}. {}\n'.format(i+1, question_data['question']))
            result_text.insert('end', 'Correct Answer: {}\n\n'.format(question_data['correct_answer']))

        result_text.configure(state='disabled')
    
    def start_again(self):
        self.points = 0
        self.current_question_index = 0
        self.try_again_button.destroy()
        self.show_answers_button.destroy()
        self.return_to_main_button.destroy()
        for button in self.answer_buttons:
            button.config(state='active')
        self.load_question()
    
    def return_to_main_screen(self):
        self.destroy()
        start = WelcomeScreen([english_test, python_test])
        start.mainloop()


if __name__ == "__main__":
    english_test = EnglishTopic('english_questions.json')
    python_test = PythonTopic('python_questions.json')
    start = WelcomeScreen([english_test, python_test])
    start.mainloop()
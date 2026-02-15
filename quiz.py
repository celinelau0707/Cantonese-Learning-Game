from playsound import playsound
from hashTable import Player,hash_table,load_id_counter,save_id_counter
import keyboard
import random
import json
import time
import threading
import os
from section_base import GameSection


def import_question(question,choice,sound):    # original code
    choice = {
        "A": question["choices"][0]["text"],
        "B": question["choices"][1]["text"],
        "C": question["choices"][2]["text"]
    }
    sound = {
        "A": question["choices"][0].get("sound", ""),
        "B": question["choices"][1].get("sound", ""),
        "C": question["choices"][2].get("sound", "")
    }
    return choice, sound

def play_choice_sound(question):       # original code
    for choice in question["choices"]:
        if choice["sound"]:
            playsound(choice["sound"])
            time.sleep(0.5)

def play_question_sound(question):     # original code
    if question.get("sound"):
        playsound(question["sound"])
        time.sleep(0.5)

def repeat(event, current_question=None):                    # original code
    if event.name == "ctrl" and current_question:
        play_question_sound(current_question)
        play_choice_sound(current_question)

def checkvalid(user_answer,timer=None):      # original code
    while user_answer not in ('A', 'B', 'C'):
        if timer and timer.time_up():   # check the time when players are inputting 
            return None
        print("\033[A\033[K", end="")
        print("Invalid input. Please input again (A, B, or C):", end="")
        user_answer = input().upper()
    return user_answer


class QuizSection(GameSection):  # manage quiz section
    def __init__(self,questions,easy_questions,medium_questions,hard_questions,username, player_id ):
        self.questions = questions
        self.easy_questions = easy_questions
        self.medium_questions = medium_questions
        self.hard_questions = hard_questions
        self.current_question = None
        self.total_score = 0
        self.username = username
        self.player_id = player_id
        self.time = None
        self.ended = False  # to track if the quiz has ended
        self.player_hash = hash_table(10)
        self.player_hash.Read_data()
        
    def start(self):     # start the quiz 
        self.runQuiz()
        
    def runQuiz(self):
        self.time = CountdownTimer(600)
        self.time.time_start()

        for i, self.current_question in enumerate(self.questions):
            if self.time.time_up():
                print("\nTime is up! The quiz is over.")
                self.time.stop()
                self.end()
                return

            random.shuffle(self.current_question["choices"])
            choice, sound = import_question(self.current_question, {}, {})
            correct = self.current_question["correct"]
            
            print("Question",i+1,":",self.current_question["question"])
            play_question_sound(self.current_question)

            for key, value in choice.items():
                print(f"{key}: {value}")
                if sound[key]:
                    playsound(sound[key])
                    time.sleep(0.5)
            
            keyboard.unhook_all()
            keyboard.on_press(lambda event: repeat(event,self.current_question)) 
            print("press ctrl to repeat the audio")
            
            if self.time.time_up():
                print("\nTime is up! The quiz is over.")
                self.time.stop()
                self.end()
                return

            user_answer = input("Your answer (A, B, or C): ").upper()

            if self.time.time_up():
                print("\nTime is up! The quiz is over.")
                self.time.stop()
                self.end()
                return
            
            user_answer = checkvalid(user_answer, self.time)
            
            if user_answer is None:
                print("\nTime is up! The quiz is over.")
                self.time.stop()  #stop the timer
                self.end()
                return
            
            if choice[user_answer] == correct:
                print("Nice! +1 score")
                self.total_score += 1
            else:
                self.player_hash.wrong_word_append(correct,self.player_id)
                print("Incorrect. The correct answer is: ", correct)

        keyboard.unhook_all()
        self.time.stop()
        self.end()

    def end(self):           # display the results of quiz
        if not self.ended:
            self.ended = True
            time_spent = int(time.time()-self.time.start_time)
            minutes, seconds = divmod(time_spent, 60)
            print("\nYour total score is: ",self.total_score,"/",len(self.questions))
            print("You have spent: ",minutes,":",round(seconds,2))

            if self.questions is self.easy_questions:
                level = "easy"
            elif self.questions is self.medium_questions:
                level = "medium"
            else:
                level = "hard"
            result=f"score:{self.total_score}, spent time: {minutes}:{round(seconds,2)}"
            self.player_hash.score_insert(level,self.total_score,self.player_id,ranked=True)
            leaderboard = Leaderboard(level)
            leaderboard.update(self.username, self.player_id, self.total_score, time_spent)
            
    
class CountdownTimer:  # count time and remind player time_left(1 & 5 mins)
    def __init__(self,time_limit):
        self.time_limit = time_limit
        self.start_time = None
        self.start_display_time = 0
        self.running = True

    def time_start(self):
        self.start_time = time.time()
        print("The quiz starts.\nYou have 10 minutes to do the quiz.")
        self.thread = threading.Thread(target=self.time_remind)
        self.thread.start()  

    def time_remind(self):    
        while self.running:
            elapsed_time = time.time() - self.start_time
            time_left = self.time_limit - int(elapsed_time)
    
            if time_left <= 0:
                self.running = False

            if time_left == 300:
                print("You have 5 minutes left.")
            elif time_left == 60:
                print("You have 1 minute left.")
            
            time.sleep(1)
    
    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()

    def time_up(self):   # check if time is up
        elapsed_time = time.time() - self.start_time
        return elapsed_time > self.time_limit
            
class Leaderboard:  # create leaderboard for each quiz level
        def __init__(self,level):
            self.level = level
            self.leaderboard_file = f"leaderboard_{level}.json"
            self.leaderboard = self.load_leaderboard()

        def load_leaderboard(self):  # load leaderboard data from file
                if os.path.exists(self.leaderboard_file):
                    with open(self.leaderboard_file,"r", encoding="utf-8") as file:
                        return json.load(file)
                return []
        
        def save_leaderboard(self):   # save leaderboard data to file
            with open(self.leaderboard_file,"w", encoding="utf-8") as file:
                json.dump(self.leaderboard,file)
        
        def update(self,username,player_id,score,time_spent):  # update the new results
            self.leaderboard.append({"username": username, "player_id": player_id, "score": score, "time_spent": time_spent})
            self.leaderboard.sort(key=lambda x: (-x['score'],x['time_spent'])) #sort by score descending,time ascending
            self.save_leaderboard()   
            self.display()

        def display(self):    
            print("\t\t\t Leaderboard")
            print("============================================================")
            print("Rank\tUsername\tID\tScore\tTime Spent(min:sec)")
            for rank, record in enumerate(self.leaderboard,start=1):
                minutes,seconds = divmod(record['time_spent'],60)  #divmod(a//b,a%b)
                print(f"{rank}\t{record['username']}\t\t{record['player_id']}\t {record['score']}\t\t{minutes}:{seconds:2d}")
            print()
            
def importQ(file_path):
    with open(file_path,"r",encoding="utf-8") as file:
        return json.load(file)
    
if __name__ == "__main__":
    print("This module contains quiz classes and should be imported, but not run directly.")
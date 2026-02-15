# exercise.py
from stack import UndoManager
from quiz import import_question
from playsound import playsound
from pynput.keyboard import Listener
import random
import time
import os
from section_base import GameSection
from hashTable import Player,hash_table, load_id_counter , save_id_counter

class ExerciseSection(GameSection):
    def __init__(self, questions, difficulty,  username , player_id):
        self.questions = questions  #store all questions
        self.undo_stack = UndoManager()
        self.state = {"current_index": 0,"score": 0,"answered": {}}
        self.player_hash = hash_table(10)
        self.player_hash.Read_data()
        self.username = username
        self.player_id = player_id
        self.difficulty=difficulty

    def start(self):
        while self.state["current_index"] < len(self.questions):
            index = self.state["current_index"]
            self.current_question = self.questions[index]
            random.shuffle(self.current_question["choices"])
            choice, sound = import_question(self.current_question, {}, {})
            correct = self.current_question["correct"]

            print("\nQuestion", index + 1, ":", self.current_question["question"])
            self.play_question_sound()
            for key, value in choice.items():
                print(f"{key}: {value}")
                if sound[key]:
                    playsound(sound[key])
                    time.sleep(0.5)

            def on_press(key):
                try:
                    k = key.char
                except AttributeError:
                    k = key.name

                if k == "ctrl_l" or k =="ctrl_r":
                    self.repeat_sound()
                elif k == "h":
                    self.player_hash.highlight_exercise("h", correct, self.player_id)

            print("Press Ctrl to repeat the audio. Press h to highlight keyword")
            with Listener(on_press=on_press) as listener:
                # While listener is active, wait for user input
                while True:
                    user_input = input("Your answer (A, B, or C) or 'back': ").strip().upper()
                    valid_user_input = self.check_input_valid(user_input)
                    if valid_user_input == "BACK":
                        if self.conduct_undo():
                            break
                        continue
                    if valid_user_input in ('A', 'B', 'C'):
                        self.check_answer(user_input, correct, choice)
                        if choice[user_input] == correct:
                            print(f"{correct} is Correct!")
                        else:
                            self.player_hash.wrong_word_append(correct,self.player_id)
                            print(f"Incorrect! The correct answer was: {correct}")
                        self.undo_stack.push({"current_index": index, "score": self.state["score"], "answered": self.state["answered"].copy()})
                        self.state["current_index"] += 1
                        break
                    else:
                        print("Invalid! Must be A/B/C or 'back'")
        
            if self.state["current_index"] >= len(self.questions):
                self.end()  # End the exercise session
                return False  # Stop the listener

        return True

    def check_answer(self, user_input,correct, choice):
        index = self.state["current_index"]
        is_correct = choice[user_input] == correct
        already_answered = self.state["answered"].get(index, False)
        if is_correct and not already_answered:
            self.state["score"] += 1
            self.state["answered"][index] = True
        elif not is_correct and already_answered:
            self.state["score"] -= 1
            self.state["answered"][index] = False
    def conduct_undo(self):                      #restore previous state
        state = self.undo_stack.pop()
        if state:
            self.state.update({
                "current_index": state["current_index"],
                "score": state["score"],
                "answered": state["answered"].copy()
            })
            print(f"Restored to Question {state['current_index'] + 1}")
            return True
        print("No history to undo")
        return False

    def repeat_sound(self):  
        if self.current_question.get("sound"):
            playsound(self.current_question["sound"])
            time.sleep(0.5)
        for choice in self.current_question["choices"]:
            if choice.get("sound") :
                playsound(choice["sound"])
                time.sleep(0.5)

    def play_question_sound(self):                  #original code
        if self.current_question.get("sound"):
            playsound(self.current_question["sound"])
            time.sleep(0.5)

    def check_input_valid(self, user_input):        #original code
        cleaned = user_input.strip().upper()
        if cleaned in {'A', 'B', 'C', 'BACK'}:
            return cleaned
        else:
            return None
    
    def end(self):
        score = (f"{min(self.state['score'], len(self.questions))} / {len(self.questions)}")
        print("\nYour total score is: ", score )
        self.player_hash.score_insert(self.difficulty,score,self.player_id,ranked=False)
        print("Exercise session ended.")


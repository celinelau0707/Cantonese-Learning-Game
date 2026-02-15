from quiz import QuizSection, Leaderboard
from exercise import ExerciseSection
from playsound import playsound
import random
import time
from question_linked_list import Node , audio_player
import os
from pynput.keyboard import Listener
from hashTable import Player,hash_table,load_id_counter,save_id_counter
import json

def importQ(file_path):
    with open(file_path,"r",encoding="utf-8") as file:
        return json.load(file)

def menu(username,user_id):
    print("Welcome to cantonese learning!")
    print(f"Current Player: {username} id: {user_id}")
    print("================================================")
    print("Enter 1 if you want to learn                    ") # Bruce's part on showing learning materials by linked list
    print("Enter 2 if you want to do exercises (unranked)  ") # Andy's part for undo feature  where users can revert their last few mistakes in quizzes.)
    print("Enter 3 if you want to do quizs (ranked)        ") # Teresa's part for making time-quiz and score leaderboard
    print("Enter 4 for player profile setting              ") # Celine's part for customized player profile (Preferred difficulty)
    print("Enter 5 to show leaderboard                     ")
    print("Enter 6 to logout                               ")
    print("Enter exit if you give up                       ")
    print("================================================")

def show_leaderboard():
    level = input("Enter difficulty level to view leaderboard (easy, medium, hard): ").lower()
    if level not in ("easy", "medium", "hard"):
        print("Invalid level. Please try again.")
        return

    leaderboard = Leaderboard(level)
    leaderboard.display()

def setting(id_counter):
    print("")
    print("==============Player Profile Setting==============")
    print("Enter 1 to Register New Player")
    print("Enter 2 to Search Player")
    print("Enter 3 to display current Player profile")
    print("Enter 4 to display all profile")
    print("Enter 5 to delete player profile")
    action = input("Enter: ")
    if action=='1':
        id_counter+=1
        new_player = Player.Register(id_counter)
        player_hash.insert(new_player)
        player_hash.display_table()
        save_id_counter(id_counter)
        player_hash.Save_data()
    elif action=='2':
        find= input("Please enter player name/ player id for searching: ").lower()
        player_hash.search(find)
    elif action =='3':
        player_hash.search(user_id)
    elif action=='4':
        player_hash.display_table()
    elif action=='5':
        player_hash.DeleteData()
    else:
        print("Invalid input")
        return


if __name__ == "__main__":
    easy_question = importQ("easy_questions.txt")      #import the txt file to variable "question"
    medium_question = importQ("medium_questions.txt")
    hard_question = importQ("hard_questions.txt")
    material = importQ("learn_material.txt")
    #====================================define objects====================================
    """
    casual_version = [Node(f"node{i+1}") for i in range(len(easy_question))]        #creating node1 to node"x"
    medium_version = [Node(f"node{i+1}") for i in range(len(medium_question))]        #creating node1 to node"x"
    hard_version = [Node(f"node{i+1}") for i in range(len(hard_question))]        #creating node1 to node"x"    
    learn_material = [Node(f"vocab{i+1}") for i in range(len(material))]
    """
    #====================================load question.txt and material stuff ====================================
    id_counter = load_id_counter()
    player_hash = hash_table(10)
    player_hash.Read_data()
    #====================================initialize ====================================
    question_size = 8
    os.system("cls")
    #====================================real start====================================
    while True:
        username, user_id = player_hash.current_player()
        casual_version = [Node(f"node{i+1}",username , user_id) for i in range(len(easy_question))]        #creating node1 to node"x"
        medium_version = [Node(f"node{i+1}",username , user_id) for i in range(len(medium_question))]        #creating node1 to node"x"
        hard_version = [Node(f"node{i+1}",username , user_id) for i in range(len(hard_question))]        #creating node1 to node"x"    
        learn_material = [Node(f"vocab{i+1}",username , user_id) for i in range(len(material))]
        menu(username, user_id)
        choice=input("Enter: ")
        if choice == '1':
            os.system("cls")
            Node.load_material(learn_material, material)
            Node.show_vocab_one_by_one(learn_material,player_hash,user_id)
        elif choice =='2': # unranked exercises with linked list
            print("Please choose( 1: exercise 2: show answer)")
            action=input("Enter: ")
            if action=='1':
                print("Please choose level( 1: Easy, 2: Medium, 3: Hard )")
                level = input("Enter: ")
                if level == '1':
                    random.shuffle(easy_question)
                    exercise_section = ExerciseSection(easy_question , "Easy", username, user_id)
                    exercise_section.start()
                elif level == '2':
                    random.shuffle(medium_question)
                    exercise_section = ExerciseSection(medium_question , "Medium", username, user_id)
                    exercise_section.start()
                elif level == '3':
                    random.shuffle(hard_question)
                    exercise_section = ExerciseSection(hard_question ,"Hard" , username, user_id)
                    exercise_section.start()
                else:
                    print("Invalid input. Please try again.")
            elif action =='2':
                print("Please choose level( 1: Easy, 2: Medium, 3: Hard )")
                level=input("Enter: ")
                if level == '1': 
                    os.system("cls")
                    Node.load_question(casual_version, easy_question, question_size)
                    Node.show_question_one_by_one(casual_version,player_hash,user_id)
                elif level =='2':
                    os.system("cls")
                    Node.load_question(medium_version, medium_question, question_size)
                    Node.show_question_one_by_one(medium_version,player_hash,user_id)
                elif level =='3':
                    os.system("cls")
                    Node.load_question(hard_version, hard_question, question_size)
                    Node.show_question_one_by_one(hard_version,player_hash,user_id)
                else:
                    print("Invalid input. Please try again.")
            else:
                print("Invalid input. Please try again.")
        elif choice == '3':
            print("Please choose level( 1: Easy, 2: Medium, 3: Hard )")
            level=input("Enter: ")
            if level=='1':
                random.shuffle(easy_question)
                quiz_section = QuizSection(easy_question,easy_question,medium_question,hard_question,username, user_id)
                quiz_section.start()
            elif level=='2':
                random.shuffle(medium_question)
                quiz_section = QuizSection(medium_question,easy_question,medium_question,hard_question,username, user_id)
                quiz_section.start()
            elif level=='3':
                random.shuffle(hard_question)
                quiz_section = QuizSection(hard_question,easy_question,medium_question,hard_question,username, user_id)
                quiz_section.start()
        elif choice== '4':
            setting(id_counter)
        elif choice =='5':
            show_leaderboard()
        elif choice =='6':
            player_hash.logout()
        elif choice == "exit":
            for i in range(1,6):        #just a little exit animation
                print("exiting", "."*i)
                time.sleep(0.3)
                print("\033[F\033[K", end="")
            os.system("cls")
            break
        else:
            os.system("cls")
            print("\033[F\033[K", end="")
            print("wrong key, enter it again!!!")

#added line 105,107 , 135-137
import json
import random
import os
from pynput import keyboard
from pynput.keyboard import Listener
import time
from playsound import playsound
from hashTable import hash_table

def importQ(file_path):     #copy from comp1080sef project code
    with open(file_path, "r", encoding="utf-8") as file:  
        return json.load(file)

def audio_player(path):
    playsound(path)

def question_sound(currentNode):
    try:
        playsound(currentNode.data[5])
        time.sleep(0.3)
    except:
        pass

def choice_sound(currentNode):
    try:
        for i in range(1,4,1):
            playsound(currentNode.data[i]["sound"])
    except:
        pass

class Node:
    def __init__(self, data, username, player_id):
        self.data = data
        self.next = None
        self.previous = None
        self.username = username
        self.player_id = player_id

    def load_question(data, question, num_nodes):
        global index_list
        global choice_order     
        random.shuffle(index_list)
        random.shuffle(choice_order)
        
        for i, ques in enumerate(question):     
            data[i].data = []       #make an array to store the whole question data
            data[i].data.append(ques["question"])       #load the question
            for choice_num in choice_order:     #load the choices
                data[i].data.append(ques["choices"][choice_num])
            
            data[i].data.append(ques["correct"])        #load the correct answer
            data[i].data.append(ques["sound"])      #index 5
        for i in range(num_nodes-1):
            data[index_list[i]].next = data[index_list[i+1]]        #link the nodes together by the order of "index_list" in ascending order
        data[index_list[num_nodes-1]].next = data[index_list[0]]        #link the final node and the first node

        for i in range(num_nodes-1, 0, -1):
            data[index_list[i]].previous = data[index_list[i-1]]        #link the nodes together by the order of "index_list" in descending order
        data[index_list[0]].previous = data[index_list[num_nodes-1]]        #link the final node and the first node

    def show_question_one_by_one(data,player_hash,player_id):
        global index_list
        startNode = data[index_list[0]]
        currentNode = startNode
        current_index = index_list.index(data.index(currentNode)) + 1  # Add 1 for question number
        Node.single_question_print(data, currentNode, current_index)
        def on_press(key):
            nonlocal startNode, currentNode, current_index
            if key == keyboard.Key.esc:
                for i in range(1,6):        #just a little exit animation
                    print("exiting", "."*i)
                    time.sleep(0.3)
                    print("\033[F\033[K", end="")
                os.system('cls' if os.name == 'nt' else 'clear')
                return False
            try:
                k = key.name
            except:
                k = key.char
            if k in ["left", "right", "p", "h"]:
                if k == "left":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    currentNode = currentNode.previous
                    current_index = index_list.index(data.index(currentNode)) + 1  # Add 1 for question number
                    Node.single_question_print(data, currentNode, current_index)
                elif k == "right":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    currentNode = currentNode.next
                    current_index = index_list.index(data.index(currentNode)) + 1  # Add 1 for question number
                    Node.single_question_print(data, currentNode, current_index)
                elif k == "p":
                    question_sound(currentNode)
                    choice_sound(currentNode)
                elif k == "h":
                    player_hash.highlight_exercise(k, currentNode.data[4], player_id)

        with Listener(on_press=on_press) as listener:
            listener.join()

    def single_question_print(data, currentNode, current_index):
        print(f"Question {current_index}: {currentNode.data[0]}")
        print("Choices: ")
        for i, letter in enumerate(["A", "B", "C"], start = 1):
            print(f"{letter}.", currentNode.data[i]["text"], end = "  ")
        print("\nAnswer: ",  currentNode.data[4])
        print("=" * 120)
        print("Press arrow key (left /right ) to move") # newly added for display
        print(f"<previous(p)  {current_index}/8  next(n)>")       
        print("Press p to play sound")
        print("Press esc to exit the current session. Press h to highlight keyword")  # newly added for display     
        '''print("="*20, "for testing", "="*20)             #for testing the sound path correct or not
        print("question Sound: ", currentNode.data[5])
        for i in range(1,4,1):
            print(currentNode.data[i]["sound"], end = "   ")
        print("\n", "="*20, "testing end", "="*20)'''

    def load_material(data, material):
        for i in range(len(material)-1):
            data[i].next = data[i+1]
        data[len(material)-1].next = data[0]

        for i in range(len(material)-1, 0, -1):
            data[i].previous = data[i-1]
        data[0].previous = data[len(material)-1]

        for i, key in enumerate(material.values()):
            data[i].data = []
            data[i].data.append(key["word"])  # Add the "word"
            data[i].data.append(key["meaning"])  # Add the "meaning"
            data[i].data.append(key["pronunciation"])  # Add the "pronunciation"
            data[i].data.append(key["sound"])
    
    def show_material(data, index):
        print(f"{index+1}.  vocab: ", data[index].data[0])
        print("     meaning: ", data[index].data[1])
        print("     pronounciation: ", data[index].data[2])
        print("Press arrow key (left /right ) to move") # newly added for display
        print("<--previous/next-->") # newly added for display
        print("Press p to play sound")
        print("Press esc to exit the current session. Press h to highlight keyword")  # newly added for display
        print("="*120)

    def show_vocab_one_by_one(data,player_hash,user_id):
        startNode = data[0]
        currentNode = startNode
        index_list = list(range(len(data)))
        current_index = 0
        Node.show_material(data, current_index)
        def on_press(key):
            nonlocal startNode, currentNode, current_index
            if key == keyboard.Key.esc:
                for i in range(1,6):        #just a little exit animation
                    print("exiting", "."*i)
                    time.sleep(0.3)
                    print("\033[F\033[K", end="")
                os.system('cls' if os.name == 'nt' else 'clear')
                return False
            try:
                k = key.name
            except:
                k = key.char
            if k in ["left", "right", "p" , "h"]:
                if k == "left":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    currentNode = currentNode.previous
                    current_index = index_list.index(data.index(currentNode))  # Add 1 for question number
                    Node.show_material(data, current_index)

                elif k == "right":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    currentNode = currentNode.next
                    current_index = index_list.index(data.index(currentNode))  # Add 1 for question number
                    Node.show_material(data, current_index)
                elif k == "p":
                    playsound(data[current_index].data[3])
                elif k == "h":
                    player_hash.highlight_exercise(k, currentNode.data[0], user_id)

        with Listener(on_press=on_press) as listener:
            listener.join()
#===========================================================================================#
index_list = list(range(8))     #define list order for linked list
choice_order = list(range(3))       #define list order for answer suffle


if __name__ == "__main__":
    easy_question = importQ("easy_questions.txt")      #import the txt file to variable "question"
    normal_question = importQ("medium_questions.txt")
    hard_question = importQ("hard_questions.txt")
    material = importQ("learn_material.txt")
    #====================================define objects====================================
    casual_version = [Node(f"node{i+1}") for i in range(len(easy_question))]        #creating node1 to node"x"
    medium_version = [Node(f"node{i+1}") for i in range(len(normal_question))]        #creating node1 to node"x"
    hard_version = [Node(f"node{i+1}") for i in range(len(hard_question))]        #creating node1 to node"x"    
    learn_material = [Node(f"vocab{i+1}") for i in range(len(material))]
    #====================================load all stuff====================================
    question_size = 8
    os.system('cls' if os.name == 'nt' else 'clear')
    #====================================real start====================================
    while True:
        choice = input("choose from easy(1), medium(2), hard(3), learn(4):  ")
        if choice == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            Node.load_question(casual_version, easy_question, question_size)
            Node.show_question_one_by_one(casual_version)
        elif choice == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            Node.load_question(medium_version, normal_question, question_size)
            Node.show_question_one_by_one(medium_version)
        elif choice == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            Node.load_question(hard_version, hard_question, question_size)
            Node.show_question_one_by_one(hard_version)
        elif choice == "4":
            os.system('cls' if os.name == 'nt' else 'clear')
            Node.load_material(learn_material, material)
            Node.show_vocab_one_by_one(learn_material)
        elif choice == "esc":
            for i in range(1,6):        #just a little exit animation
                print("exiting", "."*i)
                time.sleep(0.3)
                print("\033[F\033[K", end="")
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\033[F\033[K", end="")
            print("wrong key, enter it again!!!")

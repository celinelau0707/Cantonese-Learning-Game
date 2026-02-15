import json
import os
from datetime import datetime


class Player:
    def __init__(self,name,player_id,most_wrong={},highlight=[],score=()):
        self.name = name.lower() # "John"
        self.id = player_id # 1
        self.most_wrong= most_wrong # ["ng goi, nei ho"]
        self.highlight = highlight # ["siu sam"]
        self.score= score # ["Time Quized mode": 55 , "Exercise": 20 , "Easy" : 80 ]
    
    def Register(player_id): #register player profile
        name = input("Please register your name: ")
        return Player(name,player_id)
        
    def to_dict(self):
        return {
            "name": self.name,  # Use the 'name' attribute as "player"
            "id": self.id          # Use the 'id' attribute for the player ID
        }

        
        
def load_id_counter(filename='id_counter.txt'): #load file for player id
        with open(filename, 'r') as f:
            return int(f.read().strip())

def save_id_counter(counter, filename='id_counter.txt'): #save file for player id
    with open(filename, 'w') as f:
        f.write(str(counter))

class hash_table: # hash table initialization
    def __init__(self,size):
        self.size=size
        self.table= [ [] for _ in range(size)]

    def _hash(self,key): # hash key function
        return key % self.size
    
    def insert(self, player): # insert player object to table bucket
        index = self._hash(player.id)
        self.table[index].append(player)

    """   
    def delete(self, item): # delete by id
        with open("current_player.txt", "r") as f:
            current_player_data = json.load(f)
            current_player_id = current_player_data["id"]

        for bucket in self.table:
            for i, player in enumerate(bucket):
                if player.id==int(item):
                    if player.id == current_player_id:
                        print("\nThe current player is being deleted. Logging out...")
                        self.logout()
                    del bucket[i]
                    self.Save_data()
                    print("Player has been successfully removed.")
                    return
        print("Player has not been found")
        """

    def delete_by_id(self,player_id,current_player_id):
        for bucket in self.table:
            for i, player in enumerate(bucket):
                if player.id==int(player_id):
                    if player.id == current_player_id:
                        print("\nThe current player is being deleted. Logging out...")
                        self.logout()
                    del bucket[i]
                    self.Save_data()
                    print("Player has been successfully removed.")
                    return

    def delete(self,player): # search by id or name
        player=str(player)
        table = self.to_list()
        with open("current_player.txt", "r") as f:
            current_player_data = json.load(f)
            current_player_id = current_player_data["id"]

        if not(player.isnumeric()):
            found=self.search_all_by_name(player)
            if len(found)>1:
                        print("Multiple profiles found with that name.")
                        for p in found:
                            print(f"Name: {p[0]} | ID: {p[1]}")
                        player_id = input("Enter the id of player you want to delete: ")
                        found= self.search_by_id(player_id)
                        if (found):
                            self.delete_by_id(player_id,current_player_id)
                        else:
                            print("name not found.")
            elif len(found)==1:
                player_id = found[0][1]
                self.delete_by_id(player_id, current_player_id)
            else:
                print("Player is not found.")
        elif player.isnumeric():
            found= self.search_by_id(player)
            if (found):
                self.delete_by_id(player_id,current_player_id)
            else:
                print("Id not found.")
        else:
                print("Player is not found.")

    def display_table(self): #display hash table
        for i, players in enumerate(self.table):
            print(f"{i}: ", [(p.name, p.id, p.most_wrong, p.highlight, p.score) for p in players])
        
    def display_player(self, items): #display 1 specific player by name or id
            name = items[0] 
            player_id = items[1]
            most_wrong = items[2]
            if (most_wrong):
                most_wrong=max(most_wrong) # fetch most wrong word from dict
            highlight = items[3]
            score = items[4]
            print("="*48)
            print("name: ",name)
            print("player id: ",player_id)
            print("most wrong word: ", most_wrong)
            print("score:\n" + ''.join([''.join(i) + '\n' for i in score]))
            # ''.join(i) + '\n' = list to string + nextline
            # outside : ''.join ('easy...\n, medium...\n')
            print("="*48)

    def DeleteData(self): #delete terminal
        action = int(input("Enter 1 to delete specific name/id, Enter 2 to delete all: "))
        if (action==1):
            delete_item= input("Please enter the required name/id: ")
            print("are you sure to delete this name/id: ",delete_item,"? (yes/no)")
            confirm = input().lower()
            if (confirm=="yes"):
                self.delete(delete_item)
        elif action == 2 :
            confirm = input("Are you sure you want to delete all data? (yes/no): ").lower()
            if confirm == "yes":
                self.__init__(10)
                self.Save_data()
                print("All data deleted.")
                self.logout()
            elif confirm=="no":
                pass

    def to_list(self): #turn hash table to list (due to player object)
        result = []
        for bucket in self.table:
            new_bucket = []
            for player in bucket:
                new_bucket.append(list(player.__dict__.values()))
            result.append(new_bucket)
        return result

    def Save_data(self): # save hash table to json to txt
        json_string= json.dumps(self.to_list())
        with open("player_hash.txt", "w") as f:
            f.write(json_string)

    def Read_data(self): # read hash table from json from txt
        if not os.path.exists("player_hash.txt") or os.stat("player_hash.txt").st_size == 0:
            return self
        else:
            with open("player_hash.txt", "r") as f:
                file_content = f.read()
                table = json.loads(file_content)

                self.table = []
                for bucket in table:
                    new_bucket = []
                    for player in bucket:
                        name = player[0]
                        player_id = player[1]
                        most_wrong = player[2] 
                        highlight = player[3] 
                        score = player[4]

                        player = Player(name, player_id, most_wrong, highlight, score)
                        new_bucket.append(player)
                    self.table.append(new_bucket)

    def search_by_id(self, player_id): #search by player id
        table=self.to_list()
        key = self._hash(int(player_id)) #search by player_id
        bucket = table[key]
        for player in bucket:
            if player[1]==int(player_id):
                return player
        return False
    
    def search(self,player): # search by id or name
        player=str(player)
        table = self.to_list()
        if not(player.isnumeric()):
            found=self.search_all_by_name(player)
            if len(found)>1:
                        print("Multiple profiles found with that name.")
                        for p in found:
                            print(f"Name: {p[0]} | ID: {p[1]}")
                        player_id = input("Enter your id: ")
                        found= self.search_by_id(player_id)
                        if (found):
                            print("Player is found!")
                            self.display_player(found)
                        else:
                            print("Id not found.")
            elif len(found)==1:
                        for bucket in table:
                            for player in bucket:
                                if player[0] == player:
                                    print("Player is found!")
                                    self.display_player(player)
            else:
                print("Player is not found.")
        elif player.isnumeric():
            found= self.search_by_id(player)
            if (found):
                self.display_player(found)
            else:
                print("Id not found.")
        else:
                print("Player is not found.")

    def search_all_by_name(self, name):
        table = self.to_list()
        results = []
        for bucket in table:
            for player in bucket:
                if player[0] == name:
                    results.append(player)
        return results
           
    def highlight_exercise(self, key_name , word , player_id):
        if key_name == "h":
            player_id = int(player_id)
            index = self._hash(player_id)
            for player in self.table[index]:
                if player.id == player_id:
                    if word not in player.highlight:
                        player.highlight.append(word)
                        print(f"Highlighted: '{word}' added to your profile.")
                        self.Save_data()
                    else:
                        print("Already highlighted.")
                    break

    def wrong_word_append(self,word,player_id):
        player_id = int(player_id)
        index = self._hash(player_id)
        for player in self.table[index]:
            if player.id == player_id:
                if word in player.most_wrong:
                    player.most_wrong[word] +=1
                else:
                    player.most_wrong[word] = 1

                self.Save_data()
                break

    def score_insert(self,difficulty, score, player_id,ranked):
            time= datetime.today().strftime('%Y-%m-%d %H:%M')
            if ranked==False:
                result= [f"{difficulty} exercise: score: {score}, time: {time}"]
            else:
                result= [f"{difficulty} quiz: score: {score}, time: {time}"]
            player_id = int(player_id)
            index = self._hash(player_id)
            for player in self.table[index]:
                if player.id == player_id:
                        player.score.append(result)
                        self.Save_data()
                        break

    def login(self, found):
        table = self.to_list()

        if not found.isnumeric():
            matches = self.search_all_by_name(found)

            if len(matches) > 1:
                print("Multiple profiles found with that name.")
                player_id = input("Enter your ID: ")
                player = self.search_by_id(player_id)
                if player:
                    return player[0], player[1]
                else:
                    print("ID not found.")
                    return None

            elif len(matches) == 1:
                player = matches[0]
                return player[0], player[1]
            else:
                print("Name not found.")
                return None

        else:  # If numeric, search by ID
            player = self.search_by_id(found)
            if player:
                return player[0], player[1]
            else:
                print("ID not found.")
                return None

    def current_player(self):
        while True:
            if not os.path.exists("current_player.txt") or os.stat("current_player.txt").st_size == 0:
                print("\n==== Player Login ====")
                print("1. Login with existing profile")
                print("2. Register new profile")
                choice = input("Select (1/2): ")

                if choice == '2':
                    id_counter = load_id_counter()
                    id_counter += 1
                    player = Player.Register(id_counter)
                    self.insert(player)
                    print(f"\nRegistered new player: {player.name} (ID: {player.id})")     
                    save_id_counter(id_counter)
                    self.Save_data()

                    with open("current_player.txt", "w") as f:
                        json.dump(player.to_dict(), f)

                    return player.name, player.id

                elif choice == '1':
                    name = input("\nEnter your name: ").lower()
                    player_data = self.login(name)

                    if player_data:
                        with open("current_player.txt", "w") as f:
                            json.dump({"name": player_data[0], "id": player_data[1]}, f)
                        return player_data
            else:
                with open("current_player.txt", "r") as f:
                    data = json.load(f)
                    return data["name"], data["id"]

    def logout(self):
        with open("current_player.txt", "w") as f:
            f.write("")                                


                
if __name__ == '__main__' :
        print("This module is meant for testing on hash table module and should be imported.")
        id_counter = load_id_counter()
        player_hash = hash_table(10)
        player_hash.Read_data()
        print("1: create new profile, 2: search, 3: display, 4: delete, 5: exit")
        action = int(input())
        if action==1:
            id_counter+=1
            new_player = Player.Register(id_counter)
            player_hash.insert(new_player)
            player_hash.display_table()
            save_id_counter(id_counter)
            player_hash.Save_data()
        elif action==2:
            find= input("Please enter player name/ player id for searching: ").lower()
            player_hash.search(find)
        elif action==3:
            player_hash.display_table()
        elif action==4:
            player_hash.DeleteData()
        else:
            exit()

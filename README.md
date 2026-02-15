# Hong Kong metropolitan University comp2090SEF group 41 project

# Cantonese Teaching game

	Previously, This project is from HKMU COMP1080SEF course group project, it targets user is for NCS students which is Non-Chinese Speaking Students, it aims is to teach NCS students some common Cantonese in order to help them to be able to listen to Cantonese and make simple conversation in campus. However, the previous project lacked interactive elements, which resulted in low engagement and could not attract students to the learning process.
	The current project is to solve the shortcomings of the previous project by adding a variety of features into the learning and quiz modes to increase the immersion and motivation. Improving module organization, enhancing simplicity in creating modules, and utilizing various data structures can engage and motivate NCS students to learn Cantonese more effectively, leading to better communication in Hong Kong.

# installation
1. install python 3.9 from python.org or from Microsoft store (for window user).
tutorial:
2. open window command prompt
3. direct to the python code file folder
4. type the following command one by one (without double quote):     
    * "python -m venv .venv"   
    * ".\\.venv.Scripts\\activate"   
    * "pip install -r requirements.txt"
5. type "python main.py"

# usage example
To use the Cantonese Learning App, run the following command:

```
python main.py
```

This will start the application and present you with the main menu. From there, you can choose to:

1. Learn Cantonese vocabulary
2. Practice exercises (unranked)
3. Take quizzes (ranked)
4. Manage your player profile
5. View the leaderboard
6. Logout

Follow the on-screen instructions to navigate through the different features of the app.

## API

The Cantonese Learning App uses the following APIs:

- `playsound`: To play audio files for questions and vocabulary.
- `pynput.keyboard`: To handle keyboard input for repeating audio and highlighting keywords.

# declaration
This project have used generative AI to assist the development of the project.    

openAI : Used for debugging general errors of compilation and syntax errors.
It is also used as generating ideas for using json files on data structured imported and  solving difficulty storing player objects as providing the ideas of to_dict() and to_list() for converting objects to dictionaries and list for saving and reading player_hash.

Copilot  :Used for debugging general errors of compliation and syntax errors.
It also generate idea in structure of the functions.

Poe: used for debugging general errors of compilation and syntax errors
It also generate idea of loading and saving player records using json files.

Deepseek :  used for debugging general errors of compilation and syntax errors

# credit
1. thank you <https://www.narakeet.com/languages/cantonese-text-to-speech-yue/> for providing using right for generating audio file for education purpose.

2. thanks for openAI for generating ideas in programme developmant and debugging.

3. thanks for microsoft copilot for generating ideas in programme development and debugging.

4. thanks for Poe for  generating idea of loading and saving player records using json files and debugging general errors of compliation and syntax errors.

5.  thanks for Deepseek for used for debugging general errors of compilation and syntax errors.

6. credit for the previous project from group  

7. credit for all contributors: Celine, Bruce, Andy, Teresa, Karry.

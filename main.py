import random
from typing import List, Tuple
from openai import OpenAI
import os

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Agent:
    def __init__(self, role: str):
        self.role = role
        self.context = []

    def generate_response(self, prompt: str) -> str:
        self.context.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.context
        )
        
        assistant_response = response.choices[0].message.content
        self.context.append({"role": "assistant", "content": assistant_response})
        
        return assistant_response

class Host(Agent):
    def __init__(self, topics: List[str]):
        super().__init__("host")
        self.topics = topics
        self.chosen_topic = ""

    def choose_topic(self):
        self.chosen_topic = random.choice(self.topics)
        self.context.append({"role": "system", "content": f"You are the host in a game of 20 Questions. The topic you've chosen is '{self.chosen_topic}'. Answer the guesser's yes/no questions truthfully based on this topic."})

    def answer_question(self, question: str) -> str:
        prompt = f"Question: {question}\nPlease answer with just 'Yes' or 'No'."
        return self.generate_response(prompt)

class Guesser(Agent):
    def __init__(self):
        super().__init__("guesser")
        self.context.append({"role": "system", "content": "You are the guesser in a game of 20 Questions. Your goal is to guess the topic by asking yes/no questions. Be strategic in your questioning."})

    def ask_question(self) -> str:
        prompt = "Based on the previous questions and answers, what yes/no question would you like to ask next? Respond with just the question."
        return self.generate_response(prompt)

    def make_guess(self) -> str:
        prompt = "Based on the information you've gathered, what do you think the topic is? Make your best guess. Respond with just the guess."
        return self.generate_response(prompt)

class Game:
    def __init__(self, host: Host, guesser: Guesser, max_turns: int = 20):
        self.host = host
        self.guesser = guesser
        self.max_turns = max_turns
        self.current_turn = 0
        self.game_over = False
        self.winner = None

    def play(self) -> Tuple[bool, int]:
        self.host.choose_topic()
        print(f"Host has chosen the topic: {self.host.chosen_topic}")
        
        while not self.game_over and self.current_turn < self.max_turns:
            self.current_turn += 1
            
            # Guesser's turn
            if self.current_turn % 2 == 1:
                action = self.guesser.ask_question()
                print(f"Turn {self.current_turn}: Guesser asks: {action}")
                answer = self.host.answer_question(action)
                print(f"Host answers: {answer}")
                self.guesser.context.append({"role": "user", "content": f"Question: {action}\nAnswer: {answer}"})
            else:
                action = self.guesser.make_guess()
                print(f"Turn {self.current_turn}: Guesser guesses: {action}")
                
                if action.lower() == self.host.chosen_topic.lower():
                    self.game_over = True
                    self.winner = "guesser"
                    print(f"Correct! The guesser wins in {self.current_turn} turns.")
                else:
                    print("Incorrect guess. The game continues.")
            
        if not self.game_over:
            self.winner = "host"
            print(f"Game over! The host wins. The topic was: {self.host.chosen_topic}")
        
        return self.winner == "guesser", self.current_turn

class GameRunner:
    def __init__(self, num_games: int, topics: List[str]):
        self.num_games = num_games
        self.topics = topics
        self.results = []

    def run(self):
        for game_num in range(self.num_games):
            print(f"\nGame {game_num + 1}:")
            host = Host(self.topics)
            guesser = Guesser()
            game = Game(host, guesser)
            result = game.play()
            self.results.append(result)

    def analyze_results(self):
        guesser_wins = sum(result[0] for result in self.results)
        total_turns = sum(result[1] for result in self.results)
        avg_turns = total_turns / self.num_games

        print("\nGame Analysis:")
        print(f"Total games: {self.num_games}")
        print(f"Guesser wins: {guesser_wins}")
        print(f"Host wins: {self.num_games - guesser_wins}")
        print(f"Guesser win rate: {guesser_wins / self.num_games:.2%}")
        print(f"Average turns per game: {avg_turns:.2f}")

# Run the game
topics = ["cat", "airplane", "basketball", "computer", "pizza", "elephant", "guitar", "sunflower", "smartphone", "ocean"]
runner = GameRunner(3, topics)
runner.run()
runner.analyze_results()
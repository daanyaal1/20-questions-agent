import random
from typing import List, Tuple
from openai import OpenAI
import os
import argparse


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Agent:
    def __init__(self, role: str):
        self.role = role
        self.context = []

    def generate_response(self, prompt: str) -> str:
        self.context.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-4o",
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
        self.qa_history = []
        
    def take_turn(self):
        prompt = """
        Based on the information you have, decide whether to ask a question or make a guess.
        If you're not confident enough to guess, ask a yes/no question that explores a different aspect of the topic.
        If you think you know the answer, make a guess.
                
        Respond in the following format:
        Action: [QUESTION or GUESS]
        Content: [Your question or guess here]
        
        Remember, questions should be yes/no questions. Guesses should be specific.
        """
        response = self.generate_response(prompt)
        action, content = self.parse_response(response)
        return action.lower(), content
    
    def parse_response(self, response: str) -> Tuple[str, str]:
        lines = response.strip().split("\n")
        action = lines[0].split(":")[1].strip().lower()
        content = lines[1].split(":")[1].strip()
        return action, content
    
    def add_qa_to_history(self, question: str, answer: str):
        self.qa_history.append((question, answer))
        
class Game:
    def __init__(self, host: Host, guesser: Guesser, max_turns: int = 20):
        self.host = host
        self.guesser = guesser
        self.max_turns = max_turns
        self.current_turn = 0
        self.game_over = False
        self.winner = None

    def is_correct_guess(self, guess: str, topic: str) -> bool:
        prompt = f"""
        Your job is to determine whether the guesser has correctly won a game of 20 questions.
        20 Questions is a guessing game where one player thinks of an object, person, or concept, 
        and the other player(s) try to identify it by asking up to 20 yes-or-no questions. The game
        ends when either the subject is correctly guessed or 20 questions have been asked without a
        correct guess, making it a test of deductive reasoning and strategic questioning.
        
        Respond with either 'Correct' or 'Incorrect' if the guess accurately matches the topic, followed by a brief explanation.
        The correct answer is "{topic}".
        The guesser has guessed "{guess}".
        
        The guesser should have nailed down the answer e.g. if the answer is 
        "cactus" you shouldn't accept the guess "plant", but do accept "a catcus".
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an impartial judge in a game of 20 Questions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )

        result = response.choices[0].message.content.strip().lower()
        print(f"LLM Judgment: {result}")
        return result.startswith("correct")

    def play(self) -> Tuple[bool, int]:
        self.host.choose_topic()
        print(f"Host has chosen the topic: {self.host.chosen_topic}")
        
        while not self.game_over and self.current_turn < self.max_turns:
            self.current_turn += 1
            
            action_type, action_content = self.guesser.take_turn()
            
            if action_type == "question":
                print(f"Turn {self.current_turn}: Guesser asks: {action_content}")
                answer = self.host.answer_question(action_content)
                print(f"Host answers: {answer}")
                self.guesser.add_qa_to_history(action_content, answer)
                self.guesser.context.append({"role": "user", "content": f"Question: {action_content}\nAnswer: {answer}"})
            elif action_type == "guess":
                print(f"Turn {self.current_turn}: Guesser guesses: {action_content}")
                
                if self.is_correct_guess(action_content, self.host.chosen_topic):
                    self.game_over = True
                    self.winner = "guesser"
                    print(f"Correct! The guesser wins in {self.current_turn} turns.")
                    print(f"The actual topic was: {self.host.chosen_topic}")
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

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run 20 Questions AI experiments")
    parser.add_argument('-n', '--num_games', type=int, default=10,
                        help="Number of experiments (games) to run (default: 100)")
    return parser.parse_args()

if __name__ == "__main__":
    with open("topics.txt", 'r') as file:
        topics = [line.strip() for line in file if line.strip()]
    args = parse_arguments()
    runner = GameRunner(args.num_games, topics)
    runner.run()
    runner.analyze_results()
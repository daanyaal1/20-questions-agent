# 20 Questions Agents

### Running a Simulation

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=<YOUR-API-KEY>
python main.py --num_games 10
```

At the end of your experiment you'll see some simple results of your simulation like e.g.:

```
Game Analysis:
Total games: 10
Guesser wins: 6
Host wins: 0
Guesser win rate: 60.00%
Average turns per game: 15.50
```

The game topic is chosen randomly for each game from the [topics.txt](topics.txt) file.

You can see example of of an experiment that's previously ran [here](sample_games.txt).

### Evaluation

I played 100 games with the agents, where the host randomly selects from the topics configuration file. Here is a summary of the results:

```
Game Analysis:
Total games: 100
Guesser wins: 55
Host wins: 45
Guesser win rate: 55.00%
Average turns per game: 15.22
```

Clearly there is some room for improvement if we want to take this further!

### Thoughts and Observations

The following are some musings after simulating some games with our agents. Problems are identified, and sometimes I proposition an avenue of exploration that I have tried or which we could try in the future.

1. How should we deal with ambiguity - the winning condition can be somewhat ambiguous e.g. should we accept 'a personal computer (PC)' when the topic is 'computer'

   - a strict string matching is approach is perhaps too strict as a 'no' response will throw off the agent and cause it to start guessing other topics
   - in the end I implemented an LLM-based judge. initally the judge was too lenient e.g. see the interaction below

   ```
   e.g. Turn 2: Guesser guesses: Is it an animal?
   LLM Judgment: correct. a cat is indeed an animal, so this guess fits the correct topic.
   Correct! The guesser wins in 2 turns.
   The actual topic was: cat
   ```

   - with some tuning of the prompt I got it to behave closer to the behaviour I expected

2. I get the feeling sometimes that the LLM question generator is too influenced by the previous line of questioning (i.e. the kinds of language/tokens in the context window)

   - e.g. see the following interaction where the answer was _guitar_ and the agent guesses chair because it was already thinking along the lines of 'furniture'.

   ```
   Turn 8: Guesser guesses: A piece of furniture.
   LLM Judgment: incorrect. the guess "a piece of furniture" does not accurately match the correct answer, "guitar." a guitar is a musical instrument, not a piece of furniture.
   Incorrect guess. The game continues.
   Turn 9: Guesser asks: Is it used for storage?
   Host answers: No.
   Turn 10: Guesser guesses: A chair.
   ```

3. There's a fine balance between exploration and exploitation

   - A too narrow line of questioning too early can be detrimental e.g. asking a question like 'is it a cactus' vs 'does it produce food' when the topic was 'sunflower'
   - Even worse over-specifity early on can lead to a spiral of bad questioning that we never recover from!
   - We could modify the prompt for the question generator to explicitly encourage more diverse questions.
   - We could consider an epsilon-greedy approach to break such 'bad' cycles. Most of the time, we use the LLM to generate a question based on context, but occasionally (with probability ε) ask a completely random question from a predefined list of general questions. This strategy borrows ideas from reinforcement learning.
   - We could use another LLM call to score the diversity of the generated question compared to previous questions, and reject questions that are too similar.

4. Often a narrow line of questioning/specific guesses are influenced by some recent piece of information e.g. consider the following game:

   ```
   Turn 18: Guesser asks: Is it commonly used for reading?
   Host answers: Yes.
   Turn 19: Guesser guesses: Is it an e-reader?
   LLM Judgment: incorrect. an e-reader is a specific type of device for reading digital books, while a computer is a more general device capable of performing a wide variety of tasks beyond just reading.
   Incorrect guess. The game continues.
   Turn 20: Guesser guesses: Is it a tablet?
   LLM Judgment: incorrect. a "tablet" is a specific type of device and not accurately synonymous with a "computer". although related, they are distinct categories of technology. the correct answer is "computer".
   Incorrect guess. The game continues.
   Game over! The host wins. The topic was: computer
   ```

   - The LLM guesser agent biases towards specific information and often the most recent information (i.e. that the object is used for reading)
   - We could consider a strategy that randomly drops information when making guesses to prevent this bias
   - Another apporach may be to prompt the guesser agent to ask only 'absolute' questions like "Is the device's primary purpose for reading". This could help ensure the guesser agents knowledge is not

5. Some games are going by with all questions and not a single guess! We could make guesses more likely later in the game and/or force a guess on the last go.

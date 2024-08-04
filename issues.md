### Issues

- the winning condition is ambiguous- LLM is too quick too easy to declare a win, heuristics are too strict
  e.g. Turn 2: Guesser guesses: Is it an animal?
  LLM Judgment: correct. a cat is indeed an animal, so this guess fits the correct topic.
  Correct! The guesser wins in 2 turns.
  The actual topic was: cat

e.g. answer here was guitar- why has it guessed chair after being told its not furniture??
Turn 8: Guesser guesses: A piece of furniture.
LLM Judgment: incorrect. the guess "a piece of furniture" does not accurately match the correct answer, "guitar." a guitar is a musical instrument, not a piece of furniture.
Incorrect guess. The game continues.
Turn 9: Guesser asks: Is it used for storage?
Host answers: No.
Turn 10: Guesser guesses: A chair.

e.g. another interaction that was too influenced by previous contexts
Turn 19: Guesser asks: Is it a physical activity or game?
Host answers: Yes.
Turn 20: Guesser guesses: A deck of cards.
LLM Judgment: incorrect. the topic is "basketball," not "a deck of cards."
Incorrect guess. The game continues.
Game over! The host wins. The topic was: basketball

- LLM's question generator is too influenced by previous contexts (tokens) - need a question generator to balance exploration and exploitation- but this trends it toward exploitation. Also asks too narrow questions e.g. 'is it a cactus' vs 'does it produce food'
- LLM's ques

How to deal with ambiguit e.g. answer here is airplane:

Turn 9: Guesser asks: Is it a commercial airplane?
Host answers: Yes.
Turn 10: Guesser guesses: Is it a passenger jet?
LLM Judgment: incorrect. a "passenger jet" is a type of airplane, but it is not specifically the answer "airplane" itself, which includes all kinds of airplanes beyond just passenger jets.
Incorrect guess. The game continues.

Thoughts:

- exploration vs exploitation
- until we have A yes the agent should explore the space 100% of the time
- the more yes'es we have the more we should favour exploitation

Observation - some games go by with all questions and not a single guess! make guesses more likely later in the game.

Observation- some times the question misleads as it becomes too specific e.g.

Turn 19: Guesser guesses: Is it an e-reader?
LLM Judgment: incorrect. an e-reader is a specific type of device for reading digital books, while a computer is a more general device capable of performing a wide variety of tasks beyond just reading.
Incorrect guess. The game continues.
Turn 20: Guesser guesses: Is it a tablet?
LLM Judgment: incorrect. a "tablet" is a specific type of device and not accurately synonymous with a "computer". although related, they are distinct categories of technology. the correct answer is "computer".
Incorrect guess. The game continues.
Game over! The host wins. The topic was: computer

Issue: After writing the summarising attributes prompt we get a shortened list of attributes e.g. for a smartphone we got:

- It is not a living thing.
- It is man-made.
- It is used for entertainment.
- It can be found indoors.
- It requires electricity to function.
- It is related to visual entertainment, like watching movies or TV.
- It is not primarily used to play video games.
- It is used to listen to music or audio.
- It is commonly found in a living room.

But prompting an LLM with this leads to outputs like smartphone.
We should also tell it what it is not.

e.g. Some attributesa are intentionally misleading e.g. 'commonly found in a living room' leads to answers like 'TV'. maybe some kind of bagging (e.g. like a decision tree)

winning condition does not always work e.g.:
Turn 16: Guesser guesses: Is it a personal computer (PC)?
LLM Judgment: incorrect.

the correct answer is "computer," whereas the guess "a personal computer (pc)" is more specific and refers to a particular type of computer. the guess should match the given answer exactly.
Incorrect guess. The game continues.

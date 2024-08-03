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

-

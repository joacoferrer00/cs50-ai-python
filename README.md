# CS50's Introduction to AI with Python

My project submissions for [CS50 AI](https://cs50.harvard.edu/ai/), Harvard's introduction to artificial intelligence concepts and algorithms using Python.

Each project explores a different area of AI — from classic search algorithms to machine learning — by implementing core ideas from scratch.

---

## Projects

### Project 0a — [Degrees](./degrees/)
**Topic:** Search algorithms  
Find the shortest connection between two actors through shared movies (Six Degrees of Kevin Bacon), using **BFS** to find the shortest path in a graph.

```
python degrees.py large
```

---

### Project 0b — [Tic-Tac-Toe](./tictactoe/)
**Topic:** Adversarial search  
An unbeatable Tic-Tac-Toe AI using the **Minimax** algorithm — the AI always plays optimally, so the best a human can do is draw.

```
python runner.py
```

---

### Project 1a — [Knights](./knights/)
**Topic:** Knowledge representation & logical inference  
Solve "Knights and Knaves" logic puzzles using **propositional logic** and a model-checking algorithm that determines what must be true given a set of statements.

```
python puzzle.py
```

---

### Project 1b — [Minesweeper](./minesweeper/)
**Topic:** Knowledge representation & inference under uncertainty  
An AI that plays Minesweeper by representing the board as logical sentences and inferring safe cells and mines from what it knows.

```
python runner.py
```

---

### Project 2a — [PageRank](./pagerank/)
**Topic:** Probability & Markov chains  
Implements Google's **PageRank** algorithm two ways: by sampling a random surfer's behavior, and by iteratively computing ranks until convergence.

```
python pagerank.py corpus0
```

---

### Project 2b — [Heredity](./heredity/)
**Topic:** Bayesian networks  
Uses a **Bayesian network** to compute the probability that people in a family inherited a gene and exhibit a genetic trait, given partial observations.

```
python heredity.py data/family0.csv
```

---

### Project 3 — [Crossword](./crossword/)
**Topic:** Constraint Satisfaction Problems (CSP)  
Generates a filled crossword puzzle by modeling it as a CSP and solving it with **backtracking search**, arc consistency (AC-3), and heuristics like MRV and degree.

```
python generate.py data/structure1.txt data/words1.txt output.png
```

---

### Project 4a — [Shopping](./shopping/)
**Topic:** Machine learning — supervised learning  
Predicts whether an online shopping user will complete a purchase, using a **k-nearest neighbors** classifier trained on browsing session data (pages visited, time spent, proximity to a holiday, etc.).

```
python shopping.py shopping.csv
```

---

### Project 4b — [Nim](./nim/)
**Topic:** Machine learning — reinforcement learning  
An AI that learns to play Nim through **Q-learning** — it trains by playing thousands of games against itself, building a strategy from experience rather than explicit rules.

```
python play.py
```

---

### Project 5 — [Traffic](./traffic/)
**Topic:** Neural networks / computer vision  
A **convolutional neural network** built with TensorFlow/Keras to classify German traffic signs (43 categories, GTSRB dataset). Compares three architectures (no-conv baseline, standard CNN, deeper CNN with BatchNorm) and reaches ~98% test accuracy.

```
python traffic.py gtsrb
```

---

### Project 6a — [Parser](./parser/)
**Topic:** Natural language processing

Parses English sentences using a context-free grammar (CFG) and NLTK's ChartParser. Defines grammar rules for noun phrases, verb phrases, prepositional phrases, adjective phrases, and coordination. Extracts noun phrase chunks — the smallest NPs that contain no nested NPs.

```bash
python parser.py sentences/1.txt
# Holmes sat.
#       S
#  _____|___
# NP        VP
# |         |
# N         V
# |         |
# holmes   sat
# 
# Noun Phrase Chunks
# holmes
```

---

### Project 6b — [Attention](./attention/)
**Topic:** Natural language processing / transformers

Uses BERT (via Hugging Face `transformers`) to predict masked words in a sentence. Generates 144 attention diagrams (12 layers × 12 heads) visualizing what each attention head attends to, and includes an analysis of learned linguistic relationships.

```bash
python mask.py
# Text: The doctor told the patient to take the [MASK].
# The doctor told the patient to take the medication.
# The doctor told the patient to take the pill.
# The doctor told the patient to take the drug.
```

---

## Topics covered

| Week | Area | Projects |
|---|---|---|
| 0 | Search | Degrees, Tic-Tac-Toe |
| 1 | Logic & Knowledge | Knights, Minesweeper |
| 2 | Probability | PageRank, Heredity |
| 3 | Optimization | Crossword |
| 4 | Machine Learning | Shopping, Nim |
| 5 | Neural Networks | Traffic |
| 6 | Natural Language Processing | Parser, Attention |

---

## Setup

Most projects only need Python 3. Some have extra dependencies:

```bash
# Minesweeper and Tic-Tac-Toe use pygame
pip install -r minesweeper/requirements.txt
pip install -r tictactoe/requirements.txt
```

---

## Course

[CS50's Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/) — Harvard / edX

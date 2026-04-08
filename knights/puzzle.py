from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."

phraseA0 = And(AKnight, AKnave)

knowledge0 = And(

    # Reglas del mundo (estructura)
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # Regla de verdad / mentira
    Implication(AKnight, phraseA0),
    Implication(AKnave, Not(phraseA0))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

phraseA1 = And(AKnave, BKnave)

knowledge1 = And(

    # Reglas del mundo (estructura)
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # Regla de verdad / mentira
    Implication(AKnight, phraseA1),
    Implication(AKnave, Not(phraseA1))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

phraseA2 = Or(And(AKnight, BKnight),And(AKnave, BKnave))
phraseB2 = Or(And(AKnight, BKnave),And(AKnave, BKnight))

knowledge2 = And(

    # Reglas del mundo (estructura)
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # Regla de verdad / mentira
    Implication(AKnight, phraseA2),
    Implication(AKnave, Not(phraseA2)),
    Implication(BKnight, phraseB2),
    Implication(BKnave, Not(phraseB2))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

ASaidKnight = Symbol("A said 'I am a knight'")
ASaidKnave  = Symbol("A said 'I am a knave'")

phraseB3_1 = ASaidKnave
phraseB3_2 = CKnave
phraseC3 = AKnight

knowledge3 = And(

    # Reglas del mundo (estructura)
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    Or(ASaidKnight, ASaidKnave),
    Not(And(ASaidKnight, ASaidKnave)),

    # Regla de verdad / mentira

    Implication(And(AKnight, ASaidKnave), AKnave),
    Implication(And(AKnave, ASaidKnave), Not(AKnave)),
    Implication(And(AKnight, ASaidKnight), AKnight),
    Implication(And(AKnave, ASaidKnight), Not(AKnight)),

    Implication(BKnight, phraseB3_1),
    Implication(BKnave, Not(phraseB3_1)),
    Implication(BKnight, phraseB3_2),
    Implication(BKnave, Not(phraseB3_2)),

    Implication(CKnight, phraseC3),
    Implication(CKnave, Not(phraseC3))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

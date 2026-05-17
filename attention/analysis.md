# Analysis

## Layer 3, Head 1

This attention head appears to have learned that each token should attend strongly to the token that immediately follows it. The pattern is visible as a near-perfect diagonal in the attention diagram, where every row has its brightest cell one step to the right. This suggests the head has learned a sequential dependency, where understanding a word is closely tied to knowing what comes next.

Example Sentences:
- The cat sat on the [MASK].
- The doctor told the patient to take the [MASK].

## Layer 8, Head 11

This attention head appears to have learned the relationship between determiners and the nouns they modify. Tokens like "the" and "a" attend strongly to the noun that immediately follows them. This makes intuitive sense: determiners are grammatically bound to their nouns, and a language model would benefit from linking them explicitly.

Example Sentences:
- The cat sat on the [MASK].
- The doctor told the patient to take the [MASK].

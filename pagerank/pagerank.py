import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = {}
    N = len(corpus)

    
    for p in corpus:
        distribution[p] = (1 - damping_factor) / N

    if corpus[page]:
        for linked_page in corpus[page]:
            distribution[linked_page] += damping_factor / len(corpus[page])

    else:
        for p in corpus:
            distribution[p] += damping_factor / N
            
    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    counts = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus))

    for i in range(n):

        counts[current_page] += 1
        distribution = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
             list(distribution.keys()),
            weights=list(distribution.values())
        )[0]

    for page in counts:
        counts[page] /= n

    return counts

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)

    # Inicializar todos con 1 / N
    ranks = {page: 1 / N for page in corpus}

    while True:

        new_ranks = {}

        # Calcular nuevo rank para cada página
        for p in corpus:

            # Parte base (teleport)
            rank = (1 - damping_factor) / N

            # Sumar contribuciones
            for possible_parent in corpus:

                links = corpus[possible_parent]

                # Caso sin links: apunta a todas
                if len(links) == 0:
                    rank += damping_factor * (ranks[possible_parent] / N)

                # Caso normal: si apunta a p
                elif p in links:
                    rank += damping_factor * (
                        ranks[possible_parent] / len(links)
                    )

            new_ranks[p] = rank

        # Chequear convergencia
        stable = True

        for page in ranks:
            if abs(new_ranks[page] - ranks[page]) > 0.001:
                stable = False
                break

        # Si ya no cambia, terminamos
        if stable:
            return new_ranks

        # Si no, seguimos iterando
        ranks = new_ranks


if __name__ == "__main__":
    main()

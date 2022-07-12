# Problem 60:
#     Prime Pair Sets
#
# Description:
#     The primes 3, 7, 109, and 673, are quite remarkable.
#     By taking any two primes and concatenating them in any order the result will always be prime.
#     For example, taking 7 and 109, both 7109 and 1097 are prime.
#     The sum of these four primes, 792, represents the lowest sum for a set of four primes with this property.
#
#     Find the lowest sum for a set of five primes for which any two primes concatenate to produce another prime.

from itertools import combinations
from math import floor, sqrt
from scipy.sparse import dok_matrix
from typing import List, Tuple


def is_prime(x: int) -> bool:
    """
    Returns True iff `x` is prime.

    Args:
        x (int): Natural number

    Returns:
        (bool): True iff `x` is prime

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(x) == int and x > 0

    mid = floor(sqrt(x)) + 1
    for d in range(2, mid):
        if x % d == 0:
            return False
    return True


def is_pairwise_concatable(x: int, y: int) -> bool:
    """
    Returns True iff `x` and `y` are pairwise-concatable.

    Args:
        x (int): Natural number
        y (int): Natural number

    Returns:
        (bool): True iff `x` and `y` are pairwise-concatable

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(x) == int and x > 0
    assert type(y) == int and y > 0

    sx = str(x)
    sy = str(y)
    return is_prime(int(sx+sy)) and is_prime(int(sy+sx))


def main(k: int) -> Tuple[List[int], int]:
    """
    Returns the set of primes of size `k` having the lowest sum,
      such that all pairwise concatenations of those primes are also primes.
    Also returns the sum of this set of primes.

    Args:
        k (int): Natural number greater than 1

    Returns:
        (Tuple[List[int], int]):
            Tuple of ...
              * Set of `k` pairwise-prime-concat-able primes having the lowest sum
              * Sum of those primes

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(k) == int and k > 1

    # Idea:
    #     Maintain an unweighted, undirected graph, represented as an adjacency matrix.
    #       * Nodes are candidate prime numbers
    #       * An edge between two nodes means that nodes `p` and `q` are pairwise-concatable
    #     A desirable set of `k` primes is thus a k-clique in this graph.
    #
    #     Algorithm:
    #       * Iterate upwards through integers, discovering prime numbers
    #       * After finding a new prime `p`:
    #           * Calculate adjacency between `p` and other candidate primes
    #           * Find any `k`-clique in the graph which includes `p`
    #
    #     Also, memoize the already discovered primes to speed up computation.

    # Candidate primes represented as an undirected graph
    prime_cands = [3]
    prime_to_index = {3: 0}
    prime_degrees = {3: 0}
    n = len(prime_to_index)
    adj = dok_matrix((n, n), dtype=bool)

    # Start prime-checking from 7, since 2 and 5 will be skipped
    x = 7
    while True:
        if is_prime(x):
            # Add `x` to the graph
            n += 1
            adj.resize(n, n)
            prime_degrees[x] = 0
            for q, j in prime_to_index.items():
                if is_pairwise_concatable(x, q):
                    adj[-1, j] = adj[j, -1] = True
                    prime_degrees[q] += 1
                    prime_degrees[x] += 1
                else:
                    continue
            prime_to_index[x] = n-1
            prime_cands.append(x)

            # IDEA FOR IMPROVEMENT:
            #     Cliques are currently found by considering all candidate k-sets and checking them.
            #     Could do this better with a recursive clique-finding algorithm.

            # Now see if there are any `k`-cliques including `x`
            if prime_degrees[x] >= k-1:
                # Collect set of other primes which could join `x`
                clique_cands = []
                i = prime_to_index[x]
                for q, j in prime_to_index.items():
                    if prime_degrees[q] >= k-1 and adj[j, i]:
                        clique_cands.append(q)

                # Try choosing `k-1` other primes to form a set along with `x`,
                #   and if any found, use one having the lowest sum
                p_sum_best = None
                for p_subset in combinations(clique_cands, k - 1):
                    p_set = list(p_subset) + [x]
                    if all(map(lambda pair: adj[prime_to_index[pair[0]], prime_to_index[pair[1]]],
                               combinations(p_subset, 2))) and (p_sum_best is None or sum(p_set) < p_sum_best):
                        p_set_best = p_set
                        p_sum_best = sum(p_set)
                    else:
                        continue

                    # Check if any set was found at all, and if so, return best
                    if p_sum_best is not None:
                        return p_set_best, p_sum_best

        x += 1


if __name__ == '__main__':
    prime_set_size = int(input('Enter a natural number (greater than 1): '))
    prime_set, prime_set_sum = main(prime_set_size)
    print('Prime set of size {} where all pairwise concatenations are also prime:'.format(prime_set_size))
    print('  {}'.format(', '.join(map(str, prime_set))))
    print('Sum of those primes:')
    print('  {}'.format(prime_set_sum))

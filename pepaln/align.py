from intervaltree import Interval, IntervalTree
from pprint import pprint
import sys

class Match(object):
    """
    Represents a match
    """
    def __init__(self, name, start, end, pep):
        self.name, self.start, self.end, self.pep = name, start, end, pep

    def __repr__(self):
        return str(f"M:{self.__dict__}")

def find_matches(peps, name, sequence):
    """
    Takes a list of peptides and matches them against each
    """
    matches = list()

    for step, tmp in enumerate(sequence):
        target = sequence[step:]
        for pep in peps:
            if target.startswith(pep.motif):
                start, end = step, step + len(pep.motif)
                match = Match(name=name, start=start, end=end, pep=pep)
                matches.append(match)

    return matches


def find_layout(matches, pad=1):
    """
    Finds the layout that can packs alignments into the fewest number of lines.
    """

    # The packing style depends on which intervals are added first.
    matches = sorted(matches, key=lambda m: (m.start, m.end))

    def find_tree(ival, trees, pad=pad):
        """
        Finds (or creates) an interval tree where the interval fits.
        """
        for tree in trees:
            if not tree.overlaps(ival.begin - pad, ival.end + pad):
                return tree

        tree = IntervalTree()
        trees.append(tree)
        return tree

    trees = []
    full = IntervalTree()
    for match in matches:
        ival = Interval(match.start, match.end, data=match)
        tree = find_tree(ival, trees=trees)
        tree.add(ival)
        full.add(ival)

    return full, trees


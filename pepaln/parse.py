import csv, sys


class Peptide(object):

    def __init__(self, motif, value, label):
        self.motif, self.value, self.label = motif, safe_float(value),  label

    def __repr__(self):
        return str(f"P:{self.__dict__}")


def safe_float(text):
    """
    Converts text to float. Returns 0 on invalid float.
    """
    try:
        return float(text)
    except ValueError as exc:
        return 0


def read_fasta(fname):
    """
    Parses a multi record fasta file.

    Returns a dictionary with sequence name as the key and sequence as value.
    """
    store = dict()

    header = None

    for line in open(fname):
        line = line.strip()

        if line.startswith(">"):
            # New fasta record
            header = line[1:].split()[0]
            store[header] = ""
        else:
            # Collect the fasta sequence
            store[header] += line

    return store

def read_peptides(fname, label=None):
    """
    Reads and parses an input file with measurements for each peptide.
    Returns a dictionary keyed by each individual pattern with the rest of the row as values for the key.
    """
    store = []

    stream = csv.reader(open(fname), delimiter="\t")

    # Skip header
    next(stream)

    # Apply label if needed
    if label:
        stream = filter(lambda x: x[2] == label, stream)

    # Iterate over the stream
    for row in stream:

        # Read the first three columns
        first, value, label = row[0:3]

        value = safe_float(value)

        peptides = first.split(";")

        for motif in peptides:
            motif = motif.strip()
            pep = Peptide(motif=motif, value=value, label=label)
            store.append(pep)

    return store

def print_locs(locs, stream=sys.stdout, sep=","):
    """
    Prints the locations as tabular file.
    """
    header = ["target", "peptide", "start", "end", "value", "label"]

    line = sep.join(header)

    print(line, file=stream)

    for row in locs:

        row = map(str, row)

        line = sep.join(row)

        print(line, file=stream)

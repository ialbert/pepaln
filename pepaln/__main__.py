import plac, sys
from pathlib import Path
from . import parse, align, render
from pprint import pprint

def error(msg, stop=True):
    """
    Print error message.
    """
    print(msg, file=sys.stderr)
    if stop:
        sys.exit(1)

def warn(msg):
    """
    Print a warning message.
    """
    error(msg, stop=False)

@plac.opt('mass', "Mass-spec result file containing peptide sequences.")
@plac.opt('ref', "Reference file to match the peptides against.")
@plac.opt('pdf', "Output file for pdf file")
@plac.opt('txt', "Output file for text alignments")
@plac.opt('gff', "Output file as GFF data")
def run(mass, ref, pdf="output.pdf", txt="output.txt", gff="output.gff"):

    if not (mass or ref):
        parser = plac.parser_from(run)
        parser.print_help()
        sys.exit(1)

    # Will reuse this variable name but it makes for better parameter.
    pname = pdf

    # The labels
    labels = [ "POS", "NEG" ]

    fasta = parse.read_fasta(ref)

    pdf = render.get_canvas()

    dstream = open(gff, 'wt')
    tstream = open(txt, 'wt')

    for label in labels:

        peps = parse.read_peptides(fname=mass, label=label)

        for name, sequence in fasta.items():

            matches = align.find_matches(peps=peps, name=name, sequence=sequence)

            render.save_data(matches, stream=dstream)

            full, trees = align.find_layout(matches=matches)

            render.text_layout(full=full, trees=trees, name=name, sequence=sequence, label=label, stream=tstream)

            render.pdf_layout(pdf=pdf, full=full, trees=trees, name=name, sequence=sequence, label=label)


    if pname:
        render.save_canvas(pdf=pdf, fname=pname)


if __name__ == '__main__':
    plac.call(run)

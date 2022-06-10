"""
A module to visualize matches.
"""
import sys, math

FONT_SIZE = 8
MAX_COLOR_VAL = 3
DARK = (20, 20, 20)

NOCOVER_SYMB = "*"


try:
    from fpdf import FPDF
except ImportError as exc:
    FPDF = None
    print(f"PDF generation disabled: {exc}", file=sys.stderr)


def floatRgb(mag, cmin, cmax):
    """
    Return a tuple of floats between 0 and 1 for the red, green and blue amplitudes.
    """

    try:
        # normalize to [0,1]
        x = float(mag - cmin) / float(cmax - cmin)
    except:
        # cmax = cmin
        x = 0.5
    blue = min((max((4 * (0.75 - x), 0.)), 1.))
    red = min((max((4 * (x - 0.25), 0.)), 1.))
    green = min((max((4 * math.fabs(x - 0.5) - 1., 0.)), 1.))
    return (red, green, blue)



def rgb(mag, cmin, cmax):
    """
    Return a tuple of integers to be used in AWT/Java plots.
    """
    mag = math.log(mag + 3)
    red, green, blue = floatRgb(mag, cmin, cmax)
    return (int(red * 255), int(green * 255), int(blue * 255))


def text_layout(full, trees, name, sequence, label, stream=sys.stdout):

    print(f">{name} (Mode={label})", file=stream)

    print(sequence, file=stream)

    line = [' '] * len(sequence)
    for index, tmp in enumerate(sequence):
        if not full.overlaps(index):
            line[index] = NOCOVER_SYMB

    print("".join(line), file=stream)

    for tree in trees:
        line = [' '] * len(sequence)
        for ival in tree:
            start, end, motif = ival.begin, ival.end, ival.data.pep.motif
            line[start:start + len(motif)] = motif

        print("".join(line), file=stream)


def save_data(matches, stream=sys.stdout):
    for m in matches:
        line = [ m.name, m.pep.motif, ".", m.start + 1, m.end, ".", m.pep.value, ".", f"Mode={m.pep.label}"]
        line = map(str, line)
        line = "\t".join(line)
        print(line, file=stream)


def get_canvas():
    """
    Returns the PDF canvas.
    """

    if not FPDF:
        return None

    pdf = FPDF(format="A4")
    pdf.add_page(orientation="L")
    pdf.set_font("Courier", size=FONT_SIZE)
    return pdf


def save_canvas(pdf, fname="output.pdf"):

    if pdf is None:
        return

    pdf.write(FONT_SIZE / 2, f"COLOR LEGEND:")
    pdf.ln()

    for value in range(1, 10):
        red, green, blue = rgb(value, 1, MAX_COLOR_VAL)
        pdf.set_text_color(red, green, blue)
        pdf.write(FONT_SIZE / 2, f"Value = {value}")
        pdf.ln()

    pdf.output(fname)


def pdf_layout(pdf, full, trees, name, sequence, label, file=sys.stdout):
    if pdf is None:
        return

    # Set dark color.
    pdf.set_text_color(*DARK)

    # Add the name of the sequence
    pdf.write(FONT_SIZE / 2, f">{name} (Mode={label})")
    pdf.ln()

    # Add the sequence
    pdf.write(FONT_SIZE / 2, sequence)
    pdf.ln()

    # Add the no coverage line
    line = [' '] * len(sequence)
    for index, tmp in enumerate(sequence):
        if not full.overlaps(index):
            line[index] = NOCOVER_SYMB
    line = "".join(line)

    pdf.write(FONT_SIZE / 2, line)
    pdf.ln()

    for tree in trees:
        last = 0
        for ival in sorted(tree):
            start, end, match = ival.begin, ival.end, ival.data
            skip = start - last
            if skip:
                empty = " " * skip
                pdf.write(FONT_SIZE / 2, empty)

            value = float(match.pep.value)
            red, green, blue = rgb(value, 1, MAX_COLOR_VAL)
            pdf.set_text_color(red, green, blue)
            pdf.write(FONT_SIZE / 2, match.pep.motif)
            pdf.set_text_color(*DARK)
            last = end

        pdf.ln()

    pdf.ln()

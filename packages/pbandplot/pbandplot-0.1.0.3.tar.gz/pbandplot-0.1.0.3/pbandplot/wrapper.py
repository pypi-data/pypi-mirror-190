import argparse, os, re
import matplotlib.pyplot as plt
from pbandplot import plots, readdata

def main():
    pltname = [os.path.split(os.getcwd())[-1]]
    parser = argparse.ArgumentParser(description='Plot the phonon band structure from phonopy results.',
                                     epilog='''
Example:
pbandplot -i band.dat -o pband.png -l g m k g -d projected_dos.dat -g "$\pi^2_4$" -e Si C O
''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', "--version",  action="version", version="pbandplot 0.1.0.3")
    parser.add_argument('-s', "--size",     type=float, nargs=2, help='figure size: width, height')
    parser.add_argument('-b', "--broken",   type=float, nargs=3, help='broken axis: start, end, height ratio')
    parser.add_argument('-y', "--vertical", type=float, nargs=2, help="vertical axis")
    parser.add_argument('-g', "--legend",   type=str,   nargs=1, default=pltname, help="legend labels")
    parser.add_argument('-c', "--color",    type=str,   default='blue', help="plot color")
    parser.add_argument('-i', "--input",    type=str,   default="BAND.dat", help="plot figure from .dat file")
    parser.add_argument('-o', "--output",   type=str,   default="BAND.png", help="plot figure filename")
    parser.add_argument('-l', "--labels",   type=str.upper, nargs='+', default=[], help='labels for high-symmetry points')
    parser.add_argument('-d', "--dos",      type=str,   help="plot Phonon DOS from .dat file")
    parser.add_argument('-x', "--horizontal", type=float, nargs=2, help="horizontal axis")
    parser.add_argument('-e', "--elements", type=str,   nargs='+', default=[], help="PDOS labels")
    parser.add_argument('-w', "--wratios",  type=float, default=0.5, help='width ratio for DOS subplot')
    parser.add_argument('-f', "--font",     type=str,   default='STIXGeneral', help="font to use")

    args = parser.parse_args()

    labels = [re.sub("'|‘|’", '′', re.sub('"|“|”', '″', re.sub('^GA[A-Z]+$|^G$', 'Γ', i))) for i in args.labels]
    elements = [re.sub("'|‘|’", '′', re.sub('"|“|”', '″', i)) for i in args.elements]
    legend = args.legend
    color  = args.color

    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['ytick.minor.visible'] = True
    plt.rcParams['font.family'] = '%s'%args.font
    plt.rcParams["mathtext.fontset"] = 'cm'

    if os.path.exists(args.input):
        arr, fre, ticks = readdata.bands(args.input)
        if args.dos is None:
            if args.broken is None:
                plots.Nobroken(arr, fre, ticks, args.output, labels, args.size, args.vertical, legend, color)
            else:
                broken = args.broken
                if broken[2] >= 1 or broken[2] <= 0:
                    broken[2] = 0.2

                plots.Broken(arr, fre, ticks, args.output, labels, args.size, args.vertical, broken, legend, color)
        elif os.path.exists(args.dos):
            darr, dele = readdata.dos(args.dos)
            width_ratios = args.wratios
            if width_ratios >= 1 or width_ratios <= 0:
                width_ratios = 0.5

            if args.broken is None:
                plots.NobrokenWd(arr, fre, ticks, args.output, labels, args.size, args.vertical, darr, dele, elements, args.horizontal, width_ratios, legend, color)
            else:
                broken = args.broken
                if broken[2] >= 1 or broken[2] <= 0:
                    broken[2] = 0.2

                plots.BrokenWd(arr, fre, ticks, args.output, labels, args.size, args.vertical, broken, darr, dele, elements, args.horizontal, width_ratios, legend, color)


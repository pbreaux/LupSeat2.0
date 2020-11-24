import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib import colors
from models.room import *
from models.parser import *

def save_file(rm, filepath, stdts, str_form, seed):
    """Saves seats with student info to a file

    Args:
        stdst (dict{Student}): map of students, identified by sid
        filepath (str): filepath for output
        str_form (str): output format for each student, specified by user
        seed (int): seed for randomizer
    """
    fmt = SliceFormatter()

    with open(filepath, 'w') as outfile:
        for row in range(rm.max_row):
            for col in range(rm.max_col):
                if rm.seats[row][col] == None:
                    continue

                if rm.seats[row][col].sid == -1:
                    continue

                row_chr = int_to_chr(row)
                col_chr = str(col + 1)

                sid = rm.seats[row][col].sid
                fname = stdts[sid].first
                lname = stdts[sid].last

                stdt_str = fmt.format(str_form, sid=str(sid), fname=fname, lname=lname)

                outfile.write("{}{}: {}\n".format(row_chr, col_chr, stdt_str))

        outfile.write("\nSeed:{}\n".format(seed))

    print("Finished saving to file: {}".format(filepath))

def save_gfile(rm, filepath):
    """Saves seats with student info to an image file

    Args:
        filepath (str): filepath for output
    """
    data = np.zeros((rm.max_row, rm.max_col))

    cmap = colors.ListedColormap(['white', 'red', 'lightsteelblue', 'royalblue'])
    for row in range(rm.max_row):
        for col in range(rm.max_col):
            if rm.seats[row][col] == None:
                data[row][col] = 0
            elif rm.seats[row][col].broken:
                data[row][col] = 1 
            elif rm.seats[row][col].sid == -1:
                data[row][col] = 2
            else:
                data[row][col] = 3

    fig, ax = plt.subplots()
    im = ax.imshow(data, cmap=cmap, vmin=0, vmax=3)
    cbar = plt.colorbar(im, ticks=[0, 1, 2, 3], orientation='horizontal')
    cbar.ax.set_xticklabels(['no seat', 'broken', 'empty', 'taken'])

    col_ticks = list(range(1,rm.max_col+1))
    row_ticks = [int_to_chr(row) for row in range(rm.max_row)]
    
    # Draw row separators
    for row, cols in enumerate(rm.row_breaks):
        for col in cols:
            l = mlines.Line2D([col+0.5, col+0.5], [row+0.5, row-0.5], color='black', linewidth=2)
            ax.add_line(l)

    ax.set_xticks(np.arange(len(col_ticks)))
    ax.set_yticks(np.arange(len(row_ticks)))

    ax.set_xticklabels(col_ticks)
    ax.set_yticklabels(row_ticks)

    # Loop over data dimensions and create text annotations.
    for i in range(len(col_ticks)):
        for j in range(len(row_ticks)):
            label = row_ticks[j] + str(col_ticks[i])
            text = ax.text(i, j, label,ha="center", va="center", color="w")

    ax.set_title("Seating Chart")
    fig.tight_layout()
    plt.savefig(filepath)

    print("Finished saving to image file: {}".format(filepath))

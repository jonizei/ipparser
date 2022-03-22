from filters import *
import os

def init_files(tmp_dir, tmp_files):
    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)

    for f in tmp_files:
        if not os.path.isfile(f):
            f = open(f, 'w')
            f.close()

def read_lines(file, count):
    lines = []
    for i in range(0, count):
        line = file.readline()
        if line:
            lines.append(line)

    return lines

def write_tmp_file(fileFrom, fileTo, filter):
    with open(fileFrom, 'r') as input:
        with open(fileTo, 'w') as output:
            lines = read_lines(input, 100)
            while len(lines) > 0:
                for line in lines:
                    line = line.replace(' ', '')
                    if line != '' and line != '\n':
                        new_line = filter.filter_single(line)
                        if new_line != None and new_line != '':
                            output.write(new_line + '\n')

                lines = read_lines(input, 100)
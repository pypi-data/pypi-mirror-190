import sys
import getopt
import subprocess
import time

def r_search(grid, word, index, x, y, dir):
    # Word found
    if (index == len(word)):
        return 1
    # Searching beyond grid boundary
    elif ((x < 0) or (y < 0) or (x == len(grid[0])) or (y == len(grid))):
        return 0
    # Continue searching in current direction
    else:
        # If current character is found
        if grid[y][x] == word[index]:
            index += 1
            # Search N direction
            if dir == "N" and r_search(grid, word, index, x, y - 1, "N") == 1:
                return 1
            # Search NE direction
            elif dir == "NE" and r_search(grid, word, index, x + 1, y - 1, "NE") == 1:
                return 1
            # Search E direction
            elif dir == "E" and r_search(grid, word, index, x + 1, y, "E") == 1:
                return 1
            # Search SE direction
            elif dir == "SE" and r_search(grid, word, index, x + 1, y + 1, "SE") == 1:
                return 1
            # Search S direction
            elif dir == "S" and r_search(grid, word, index, x, y + 1, "S") == 1:
                return 1
            # Search SW direction
            elif dir == "SW" and r_search(grid, word, index, x - 1, y + 1, "SW") == 1:
                return 1
            # Search W direction
            elif dir == "W" and r_search(grid, word, index, x - 1, y, "W") == 1:
                return 1
            # Search NW direction
            elif dir == "NW" and r_search(grid, word, index, x - 1, y - 1, "NW") == 1:
                return 1
            else:
                return 0
        # If current character is not found
        else:
            return 0

def base_search(grid, word):
    # Iterate through each row of word search grid
    for y in range(len(grid)):
        # Iterate through each column of word search grid
        for x in range(len(grid[y])):
            # Locate first letter of words
            if grid[y][x] == word[0]:
                # Begin search and display (x,y) coordinate and direction of word found
                if r_search(grid, word, 0, x, y, "N") == 1:
                    print("%s found at (%d, %d) N" % (word, x + 1, y + 1))
                elif r_search(grid, word, 0, x, y, "NE") == 1:
                    print("%s found at (%d, %d) NE" % (word, x + 1, y + 1))
                elif r_search(grid, word, 0, x, y, "E") == 1:
                    print("%s found at (%d, %d) E" % (word, x + 1, y + 1))
                elif r_search(grid, word, 0, x, y, "SE") == 1:
                    print("%s found at (%d, %d) SE" % (word, x + 1, y + 1))
                elif r_search(grid, word, 0, x, y, "S") == 1:
                    print("%s found at (%d, %d) S" % (word, x + 1, y + 1))
                elif r_search(grid, word, 0, x, y, "SW") == 1:
                    print("%s found at (%d, %d) SW" % (word, x + 1, y + 1))
                elif r_search(grid, word, 0, x, y, "W") == 1:
                    print("%s found at (%d, %d) W" % (word, x + 1, y + 1))
                elif r_search(grid, word, 0, x, y, "NW") == 1:
                    print("%s found at (%d, %d) NW" % (word, x + 1, y + 1))

def word_search_solver():
    # verbose = False
    # words = ""
    # puzzle_grid = []

    # # Process/parse arguments
    # arg_list = []
    # if len(sys.argv) > 1:
    #     arg_list = sys.argv[1:]
    # options = "vi:l:"
    # long_options = ["verbose", "input_file=", "wordlist="]
    # try:
    #     args, vals = getopt.getopt(arg_list, options, long_options)
    #     for currentArg, currentVal in args:
    #         if currentArg in ("-v", "--verbose"):
    #             verbose = True
    #         elif currentArg in ("-i", "--input_file"):
    #             f = open(str(currentVal), "r")
    #             for line in f:
    #                 if line[-1] == "\n":
    #                     puzzle_grid.append(line.split(" ")[:-1])
    #                 else:
    #                     puzzle_grid.append(line.split(" "))
    #             f.close()
    #         elif currentArg in ("-l", "--wordlist"):
    #             f = open(str(currentVal), "r")
    #             for line in f:
    #                 if words == "":
    #                     words += line
    #                 else:
    #                     words += " " + line
    #             f.close()
    # # Error msgs for command line arguments
    # except getopt.error as err:
    #     if err.opt in ("-i", "--input_file"):
    #         print("ERROR: Must provide an input file containing word search grid", file=sys.stderr)
    #     elif err.opt in ("-l", "--wordlist"):
    #         print("ERROR: Must provide wordlist for corresponding word search grid", file=sys.stderr)
    #     else:
    #         print("ERROR: Invalid argument", file=sys.stderr)
    #     return -1

    # # Enforcing command line args
    # if puzzle_grid == [] or words == "":
    #     print("ERROR: Must provide word search grid and/or word list", file=sys.stderr)
    #     return -1

    # # Display word search grid
    # if verbose:
    #     print("Displaying Word Search Grid")
    #     for y in puzzle_grid:
    #         for x in y:
    #             print(x + " ", end="")
    #         print("")
    #     print("")
    
    # Solve word search and display answers and solve time
    print("Location of words are in (col, row) format")
    start = time.perf_counter()
    for word in words.split():
        base_search(puzzle_grid, word.upper())
    end = time.perf_counter()
    print(f"Solve time: {1000 * (end - start)} ms")

    return 0

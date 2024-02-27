import argparse

# Construct the argument parser
ap = argparse.ArgumentParser(
    prog = '',
    description = "Setup network of IBFT nodes",
    conflict_handler = 'error',
    add_help = True)

# Add the arguments to the parser
ap.add_argument("-r", "--enablerpi", required=False, default="no", help="Setup for Raspberry PI: yes or no")
ap.add_argument("-b", "--soperand", required=False, help="second operand")
args = vars(ap.parse_args())

# Calculate the sum
# print("Sum is {}".format(int(args['foperand']) + int(args['soperand'])))
print(args['forRPI'])

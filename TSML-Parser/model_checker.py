import copy
from parser import parse
from compute_fixpoint import compute_fixpoint
from deadlock import print_deadlock_states

input_path = './elevator.tsml'
output_path = './output.tsml'

# Read the input file, parse it and return the corresponding model
parsed_model = parse(input_path)

# We make a deepcopy of the parsed model because compute_fixpoint() will modify it
model_to_synchronize = copy.deepcopy(parsed_model)

# Compute_fixpoint() returns a unique Class based on the input model
synchronized_class = compute_fixpoint(model_to_synchronize)

# Check if there are deadlocks in the model
print_deadlock_states(synchronized_class)

# Dump the model to output to a file so that we can read it
# You can choose a parsed model or a synchronized class
model_to_output = synchronized_class

output_file = open(output_path, 'w+')
output_file.write(str(model_to_output))
output_file.close

#Este código es de Gemini
import itertools

# Number of coins
N = 7

# 1. Generate all possible microstates
# itertools.product creates all combinations of 'H' and 'T' of length 7
# It returns tuples like ('H', 'T', 'H', 'H', 'T', 'T', 'T')
all_combinations = list(itertools.product(['H', 'T'], repeat=N))

# 2. Prepare a dictionary to store macrostates
# Keys: number of heads (0 through 7)
# Values: a list of microstates (strings) that have that many heads
macrostates = {k: [] for k in range(N + 1)}

# 3. Categorize each microstate by its macrostate (number of heads)
for microstate_tuple in all_combinations:
    # Convert tuple to a clean string, e.g., "HTHHTTT"
    microstate_str = "".join(microstate_tuple)
    
    # Count how many 'H's are in this microstate
    num_heads = microstate_str.count('H')
    
    # Append to the corresponding macrostate group
    macrostates[num_heads].append(microstate_str)

# 4. Print the results analogous to a table
print(f"System: N = {N} coins")
print(f"Total Microstates (2^N): {len(all_combinations)}\n")

# Table header
print(f"{'Macrostate (Heads)':<18} | {'Multiplicity (Count)':<20} | {'Microstates'}")
print("-" * 100)

for heads in range(N + 1):
    list_of_microstates = macrostates[heads]
    multiplicity = len(list_of_microstates)
    
    # To keep the output readable in the terminal, we'll only print the first 5 
    # microstates for each macrostate, followed by "..." if there are more.
    display_microstates = ", ".join(list_of_microstates[:5])
    if multiplicity > 5:
        display_microstates += ", ..."
        
    print(f"{heads:<18} | {multiplicity:<20} | {display_microstates}")

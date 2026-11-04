1. Scope of AI statement
Artificial intelligence assistance in this project was limited to an auxiliary code helper for code syntax and
graph formatting. The platform google Gemini was used for the purposes that will be detailed in what follows:

2. Prompt examples
Below are some examples of the actual prompts submitted to the AI assistant during the project.
### Prompt Example 1: Integrating Memory Tracking
> *"Modify as little as possible this code so that it includes the memory usage using tracemalloc and returns `(count, elapsed_time, peak_ram_mb)` instead of printing directly:"*  

### Prompt Example 2: Runner Script Formatting
> *"Modify this runner script accordingly so that it handles the new returned tuple `(count, elapsed, peak_ram)` from `measure_microstates(N)` and prints a clean ASCII table with formatted columns for N, Total States, Time (s), and RAM (MB)."*

### Prompt Example 3: Theoretical Verification
> *"Why is the memory complexity O(1) for Method 2 and Method 3 even though the loop runs 2^N times? Explain the difference between time complexity and space complexity in lazy evaluation."*
>
### Prompt Example 4: Checking mistakes
> * Pasted our thermodynamics.py and asked "Point possible errors".
> * Identified entropy_change(N, k) used undefined variables k_1, k_2, and docstrings placed above the def line, so Python did not treat them as docstrings.

### Prompt Example 5: Thermodynamic tests
>* "What do the tests in the  have to check?"
>*  Output: A pytest file comparing every function with math.comb values (probabilities, normalisation, symmetry P_k = P_{N−k}, maximum at N/2, out-of-range states, ΔS, likelihood ratio, waiting time).
Team action: Added to tests/test_thermodynamics.py, matched function names to our module, executed with python -m pytest -v.

## 3. Human Verification & Auditing Steps

To ensure scientific integrity, code correctness, and data accuracy, all AI-suggested modifications underwent rigorous human oversight prior to execution and reporting.
 
 Independent mathematical verifications were done at every step, particularly regarding theroetical number of microstates, and theoretical time-complexities.

 Furthermore, every line od suggested code was inspected minuciously to prevent incorrect executions or conceptual errors.

 Finally, all tables and graphs were verified according to theoretical results and code generated in order to find any possible bug or inaccuracy. 

 ## 4. Declaration of Responsibility

The authors retains full accountability for the accuracy, validity, and integrity of all code, performance benchmark figures, analysis, and conclusions presented in this work.

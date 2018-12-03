# Constraint Satisfaction - Seating Students in Buses

Algorithm that intends to seat students in a bus while minimizing the amount of rowdy groups seated together.

## Contributors

<ul>
<li>Taj Shaik (@tajshaik24)</li>
<li>Saurav Chhatrapati (@saurav-c)</li>
<li>Osama Ahmed (@osamaahmed20)</li>
</ul>

## Input Generation

Run the following command with respective flags to generate small, medium, and large inputs:\
`python3 inputGen.py [-s] [-m] [-l]`

## Solver

In order to use the solver, you must install the following packages:
<ul>
<li>networkx</li>
<li>metis</li>
</ul> 
These packages can be installed with `pip` using the following commands: 
<ul>
<li>pip install networkx</li>
<li>pip install metis</li>
</ul> 
If you don't have pip installed on your machine: please visit the following website: https://pip.pypa.io/en/stable/installing/

Before running the code, make sure you have the following folder inside the current directory: `all_inputs` which contains all of the provided inputs.

Run the following command with respective flags to generate the outputs:\
`python3 solver.py`


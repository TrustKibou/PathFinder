# PATH FINDER IN A WORLD OF GRIDS
### Included Packages:
- matplotlib
- shapely
- heapq



### Steps to Run:
1. Ensure Python 3.11+ and listed packages are installed on your system
2. In terminal, move to project directory and run "search.py"\
``python search.py``
3. Program will execute and present you with a list of options. After choosing an option, the grid world will appear in a new window.
   4. In order to select another option from the menu, you must CLOSE the opened grid window. Once you do so, the menu will repopulate.

_Note: virtual environment and explicit dependency install not required_

#### Package Install:
1. Run the following command in terminal:\
``pip install matplotlib shapely``

### About
Path Finder is a basic implementation of artificial intelligence that utilizes different systematic algorithms to calculate the best path from a source point to a destination point.

There are four algorithms total that the user can choose from to calculate this best path. Two are uninformed (breadth first search and depth first search) and two are informed (greedy best first search and A* search).

User can visualize each algorithm's path decision in one execution; there is no need to rerun to view a different search result.


### Future Features
- Ability to change start/endpoints
- Ability to add terrain conditions
- Ability to define grid size
- Additional obstacles
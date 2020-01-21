from mazelib import Maze
from mazelib.generate.Prims import Prims

m = Maze()
m.generator = Prims(27, 34)
m.generate()

print(m.grid)
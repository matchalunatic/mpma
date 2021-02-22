from . import *
from IPython import embed
import sys

t = sys.argv[1]

r = RelationshipGraph()

r.load_file(t)
g = r.render_relationships_from_center()

print("""
g -> graphviz object
r = relational graph
""")
embed()
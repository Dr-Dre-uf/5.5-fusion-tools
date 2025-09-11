import inspect
from fusion_tools.visualization import Visualization

print(inspect.signature(Visualization))
print(inspect.getsource(Visualization.__init__))

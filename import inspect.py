import inspect
import fusion_tools.visualization.components as comp

print([name for name, obj in inspect.getmembers(comp, inspect.isclass)])

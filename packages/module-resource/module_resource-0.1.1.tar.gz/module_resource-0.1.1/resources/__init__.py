import os as __os
import inspect as __inspect

def get_resource_path(object, path, resource_path="resources"):
    """
    ```python
    import resources
    import you_module

    path = resources.get_resource_path(you_module, 'icon.png')
    print(path) # ...\you_module_path\\resources\icon.png
    
    o = object()
    path = resources.get_resource_path(o, 'icon.png')
    print(path) # ...\current_path\\resources\icon.png
    ```
    """
    return __os.path.join(__os.path.join(__os.path.dirname(__inspect.getfile(object)), resource_path), path)
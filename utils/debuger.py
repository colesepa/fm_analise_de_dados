import inspect

def debug_print(*args, **kwargs):
    
    frame = inspect.currentframe().f_back
    
    filename = inspect.getfile(frame)
    
    lineno = frame.f_lineno
    
    print(f"[{filename}:{lineno}]", *args, **kwargs)
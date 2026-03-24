import os, subprocess, platform

def find_path(filename: str):
    if filename.endswith(".exe"):
        filename = filename[:-4]
        
    system = platform.system()

    if system == 'Windows':
        command = f"where {filename}.exe"
    else:
        command = f"which {filename}"
    
    result = subprocess.run(
        command, 
        capture_output= True, 
        text= True
    )
    print(result.stdout.split('\n'))
        

find_path(filename= "python")
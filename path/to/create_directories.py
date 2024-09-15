import os

def create_directories():
    directories = [
        "humanitarian_dashboard/data",
        "humanitarian_dashboard/templates",
        "humanitarian_dashboard/static"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

if __name__ == "__main__":
    create_directories()

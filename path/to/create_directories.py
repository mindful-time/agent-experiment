import os

def create_project_structure():
    os.makedirs('mozambique_dashboard/data', exist_ok=True)

if __name__ == '__main__':
    create_project_structure()

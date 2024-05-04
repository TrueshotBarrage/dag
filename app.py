from src.topsort import Graph
from src.node_manager import TaskManager

def main():
    g = Graph("A>B,B>C,B>D,D>E,C>E", debug=False)
    manager = TaskManager(g)
    
    manager.execute()

if __name__ == "__main__":
    main()
import math

class DecisionTree:
    def __init__(self):
        self.root = self.__Node()

    def fit(self, X, y):
        tree = DecisionTree()
        tree.root.set(X, y)
        return tree

    class __Node:
        def __init__(self, parent=None):
            self.classes = {}
            self.X = None
            self.y = None
            self.info = 0
            self.parent = parent
            self.children = []
            
        def set(self, X, y):
            self.X = X
            self.y = y.column(0)
            self.info = self.__cal_info(self.y)

        def __entropy(self, event, space):
            prob = event/space
            return prob*math.log(prob,2)
        
        def __cal_info(self, y):
            classes = set(y)
            info = 0

            for c in classes:
                space = len(y)
                event = y.count(c)
                info += self.__entropy(event, space)
            
            return -1*info

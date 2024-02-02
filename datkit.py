import math
from collections import deque

class DecisionTree:
    def __init__(self):
        self.root = Node()

    def fit(self, X, y):
        tree = DecisionTree()
        tree.root.fit(X, y)
        return tree
    
    def print_tree(self):
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if(node.children != []):
                print(node)
            for child in node.children:
                queue.append(child["node"])

class Node:
    def __init__(self):
        self.X = None
        self.y = None
        self.info = 0
        self.children = []
        self.data = {}
        self.parent = ""
        self.select_attr = ""
        self.answer = ""
    
    def __str__(self):
        string = []
        string.append("--------------------------------\n")
        if(self.parent != ""):
            string.append("From - [" + self.parent + "]\n")
            string.append("--------------------------------\n")
        else:
            string.append("Start\n")
            string.append("--------------------------------\n")
        if(self.children != []): string.append(self.select_attr + "?\n")
        for child in self.children:
            string.append(child["value"] + ": ")
            if(child["node"].children != []):
                string.append(child["node"].select_attr)
            else: string.append(child["node"].answer)
            string.append("\n")
        string.append("--------------------------------\n")
        return ''.join(string)
        
    def fit(self, X, y):
        self.X = X
        self.y = y
        self.info = self.__cal_info(self.y.column(0))
        self.__prepare_data()
        self.__count_data()
        self.__info_data()

        max_gain = 0
        for attr in self.data:
            if self.data[attr]["gain"] > max_gain:
                self.select_attr = attr
                max_gain = self.data[attr]["gain"]
        
        for value in self.data[self.select_attr]["values"]:
            child = Node()
            child.parent = self.select_attr + ": " + value
            if(self.data[self.select_attr]["values"][value]["info"] == 0):
                values = self.data[self.select_attr]["values"][value]["classes"]
                child.answer = max(values, key=values.get)
            else:
                new_X = X.select(X.equal(self.select_attr, value)).drop_column([self.select_attr])
                new_y = y.select(X.equal(self.select_attr, value))
                child.fit(new_X, new_y)
            self.children.append({"value": value, "node": child})
    
    def __prepare_data(self):
        self.data = {}
        for i in range(len(self.X.attributes)):
            attr_name = self.X.attributes[i]
            self.data[attr_name] = {}
            self.data[attr_name]["values"] = {}
            values = list(set(self.X.column(i)))

            for j in range(len(values)):
                value_name = values[j]
                self.data[attr_name]["values"][value_name] = {}
                self.data[attr_name]["values"][value_name]["count"] = 0
                self.data[attr_name]["values"][value_name]["classes"] = {}
                for label in set(self.y.column(0)):
                    self.data[attr_name]["values"][value_name]["classes"][label] = 0

    def __count_data(self):
        attributes = self.X.attributes
        rows = self.X.rows
        for n in range(len(rows)):
            attributes
            for i in range(len(attributes)):
                label = self.y.column(0)[n]
                self.data[attributes[i]]["values"][rows[n][i]]["classes"][label] += 1
                self.data[attributes[i]]["values"][rows[n][i]]["count"] += 1

    def __info_data(self):
        attributes = self.X.attributes
        for i in range(len(attributes)):
            attr_name = attributes[i]
            values = list(set(self.X.column(i)))
            attr_info = 0
            for value_name in values:
                info = 0
                space = self.data[attr_name]["values"][value_name]["count"]
                for label in self.data[attr_name]["values"][value_name]["classes"]:
                    event = self.data[attr_name]["values"][value_name]["classes"][label]
                    info += self.__entropy(event, space)
                self.data[attr_name]["values"][value_name]["info"] = info = -1*info
                attr_info += space/len(self.X.rows)*info
            space = self.data[attr_name]["info"] = attr_info
            space = self.data[attr_name]["gain"] = self.info - attr_info
    
    def __cal_info(self, y):
        classes = set(y)
        info = 0

        for c in classes:
            space = len(y)
            event = y.count(c)
            info += self.__entropy(event, space)
        
        return -1*info
    
    def __entropy(self, event, space):
        if (event == 0): return 0
        prob = event/space
        return prob*math.log(prob,2)

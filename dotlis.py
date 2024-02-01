class DataTable:
  def __init__(self, attributes, rows):
    self.attributes = attributes
    self.rows = rows
    self.num = len(rows) - 1

  def column(self, number):
    return [row[number] for row in self.rows]

  def split(self, cut_point):
    first = DataTable(self.attributes[:cut_point], [[item for item in row[:cut_point]] for row in self.rows])
    second = DataTable(self.attributes[cut_point:], [[item for item in row[cut_point:]] for row in self.rows])
    return first, second
  
  def exclass(self, attr_name):
    index = self.attributes.index(attr_name)
    y = DataTable(self.attributes[index], [[row[index]] for row in self.rows])
    X = DataTable(self.__excludes(self.attributes, [index]), self.__drop_column(self.rows, [index]))
    return X, y
  
  def __excludes(self, original_list, indices_to_exclude):
    return [original_list[i] for i in range(len(original_list)) if i not in indices_to_exclude]
  
  def __drop_column(self, rows, list_of_column):
    return [[item for item in self.__excludes(row, list_of_column)] for row in rows]
  
def read_tsv(filename):
    f = open(filename, "r")
    source = f.read()
    # source = source.replace(" ", "\t")
    rows = list(filter(lambda item: item != "", source.split("\n")))

    rows = [row.split("\t") for row in rows]
    # rows = [list(filter(lambda item: item != "", row.split("\t"))) for row in rows]
    attributes = rows[0]
    
    return DataTable(attributes, rows[1:])

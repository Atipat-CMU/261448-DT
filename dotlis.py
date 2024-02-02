import tylib

class DataTable:
  def __init__(self, attributes, rows):
    self.attributes = attributes
    self.rows = rows
    self.num = len(rows) - 1

  def column(self, number):
    return [row[number] for row in self.rows]
  
  def equal(self, attr_name, value_name):
    index = self.attributes.index(attr_name)
    values = self.column(index)
    return [i for i in range(len(values)) if values[i] == value_name]
  
  def drop(self, indices):
    return DataTable(self.attributes, self.__excludes(self.rows, indices))
  
  def drop_column(self, list_of_column):
    tabel = DataTable(self.attributes, self.rows)
    if(tylib.is_type(list_of_column, str)):
      list_of_column = [tabel.attributes.index(column) for column in list_of_column]
    tabel.attributes = [self.attributes[i] for i in range(len(self.attributes)) if i not in list_of_column]
    tabel.rows = [[item for item in tabel.__excludes(row, list_of_column)] for row in tabel.rows]
    return tabel
  
  def select(self, indices):
    return DataTable(self.attributes, self.__includes(self.rows, indices))
  
  def exclass(self, attr_name):
    index = self.attributes.index(attr_name)
    y = DataTable(self.attributes[index], [[row[index]] for row in self.rows])
    X = DataTable(self.__excludes(self.attributes, [index]), self.drop_column([index]).rows)
    return X, y
  
  def __excludes(self, list, indices):
    return [list[i] for i in range(len(list)) if i not in indices]
  
  def __includes(self, list, indices):
    return [list[i] for i in range(len(list)) if i in indices]
  
def read_tsv(filename):
    f = open(filename, "r")
    source = f.read()
    rows = list(filter(lambda item: item != "", source.split("\n")))

    rows = [row.split("\t") for row in rows]
    attributes = rows[0]
    
    return DataTable(attributes, rows[1:])

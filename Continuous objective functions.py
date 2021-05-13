# An assortment of selected continuous objective functions

def sphere(x):
  """
  The sphere function
  """
    x = np.array(x)
    return np.sum(np.square(x))
  
def schwefel_222(x):
  """
  Schwefel 2.22 function
  """
    x = np.array(x)
    return np.sum(np.abs(x)) + np.prod(np.abs(x))
  
def schwefel_12(x):
  """
  Schwefel 1.2 function
  """
    x = np.array(x)
    return np.sum([np.sum(x[:i]) ** 2
                   for i in range(len(x))])  
  
def schwefel_221(x):
  """
  Schwefel 2.21 function
  """
    x = np.array(x)
    return np.max(np.abs(x))
  

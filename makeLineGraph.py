from matplotlib import pyplot as plt
import svmCrossValidation as s
import cPickle

#y is an array of two tuples (series, label) since there can be more than one series
def genLineGraph(x, y, xlabel, ylabel, title, legend = True, labels = True, logScale = False, legendLoc = "upper left"):
  plt.figure()
  if labels:
    for series, label in y:
      plt.plot(x, series, label = label)
  else:
    for series in y:
      plt.plot(x, series)
  if legend:
    plt.legend(loc = legendLoc)
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  if logScale:
    plt.yscale('log')
  plt.show()

def initialSVMGraph():
  x = []
  y1 = []
  y2 = []
  y3 = []
  y4 = []
  for count in range(2, 21):
    x.append(count)
    y1.append(s.crossValidate(s.vects, count, classifier = 'svm', Kparam = 'rbf'))
    y2.append(s.crossValidate(s.vects, count, classifier = 'svm', Kparam = 'linear'))
    y3.append(s.crossValidate(s.vects, count, classifier = 'svm', Kparam = 'poly'))
    y4.append(s.crossValidate(s.vects, count, classifier = 'svm', Kparam = 'sigmoid'))
   # y5.append(s.crossValidate(s.vects, count, classifier = 'svm', Kparam = 'precomputed'))
  return x, y1, y2, y3, y4

def genInitAutoencoderGraph():
  with open('500hidden.p', 'rb') as fp:
    five = cPickle.load(fp)
  with open('/home/ryan/Programming/Footballer/graphs/400hidden.p', 'rb') as fp:
    four = cPickle.load(fp)
  with open('/home/ryan/Programming/Footballer/graphs/300hidden.py', 'rb') as fp:
    three = cPickle.load(fp)
  with open('/home/ryan/Programming/Footballer/graphs/200hidden.p', 'rb') as fp:
    two = cPickle.load(fp)
  x = []
  count = 1
  while count < 101:
    x.append(count)
    count += 1
  y = [(two, "200 Hidden Nodes"), (three, "300 Hidden Nodes"), (four, "400 Hidden Nodes"), (five, "Five Hundred Hidden Nodes")]
  genLineGraph(x, y, "Epoch", "Error", "Autoencoder Error Rates", logScale = True)

def genInitSVMgraph():
  with open('initsvmrbf.p') as fp:
    rbf = cPickle.load(fp)
  with open('linear.p') as fp:
    linear = cPickle.load(fp)
  with open('poly.p') as fp:
    poly = cPickle.load(fp)
  with open('sigmoid.p') as fp:
    sig = cPickle.load(fp)
  x = []
  count = 1
  while count < 20:
    x.append(count)
    count += 1
  y = [(rbf, "Radial Basis Kernel Function"), (linear, "Linear Kernel Function"), (poly, "Polynmolial Kernel Function"), (sig, "Sigmoidal Kernel Function")]
  genLineGraph(x, y, "Slices", "Proportion Correct", "SVM Classification Initial Prediction Results", legendLoc = "lower right")

def gen50Corrupted():
  with open('50050denoise.p') as fp:
    five = cPickle.load(fp)
  with open('40050denoise.p') as fp:
    four = cPickle.load(fp)
  with open('30050denoise.p') as fp:
    three = cPickle.load(fp)
  x = []
  count = 1
  while count < 101:
    x.append(count)
    count += 1
  y = [(three, "300 Hidden Nodes"), (four, "400 Hidden Nodes"), (five, "500 Hidden Nodes")]
  genLineGraph(x, y, "Epoch", "Error", "Denoising Autoencoder Error Rates with 50 Corrupted Inputs", logScale = True)
 
def gen150Corrupted():
  with open('500150denoise.p') as fp:
    five = cPickle.load(fp)
  with open('400150denoise.p') as fp:
    four = cPickle.load(fp)
  with open('300150denoise.p') as fp:
    three = cPickle.load(fp)
  x = []
  count = 1
  while count < 101:
    x.append(count)
    count += 1
  y = [(three, "300 Hidden Nodes"), (four, "400 Hidden Nodes"), (five, "500 Hidden Nodes")]
  genLineGraph(x, y, "Epoch", "Error", "Denoising Autoencoder Error Rates with 150 Corrupted Inputs", logScale = True)   

def gen300Corrupted():
  with open('500300denoise.p') as fp:
    five = cPickle.load(fp)
  with open('400300denoise.p') as fp:
    four = cPickle.load(fp)
  with open('300300denoise.p') as fp:
    three = cPickle.load(fp)
  x = []
  count = 1
  while count < 101:
    x.append(count)
    count += 1
  y = [(three, "300 Hidden Nodes"), (four, "400 Hidden Nodes"), (five, "500 Hidden Nodes")]
  genLineGraph(x, y, "Epoch", "Error", "Denoising Autoencoder Error Rates with 300 Corrupted Inputs", logScale = True)


import buildVector as bv
from sklearn import svm, linear_model
import cPickle

vects = cPickle.load(open('serialized_vectors.p', 'rb'))

def chunks(l, n):
  return [l[i:i+n] for i in range(0, len(l), n)]

def flatten(lst):
  return [val for subl in lst for val in subl]

#Input is the number of different validation and training sets
#Divides the vects into n slices and trains on all slices except 1 each time
#Outputs the proportion correct
def crossValidate(vects, n, classifier = 'linear',Cparam = 1.0, Kparam = 'rbf', Gparam = 0.0):
  trainingSets = []
  validationSets = []
  cks = chunks(vects, len(vects)/n)
  count = 0
  while count < len(cks):
    trainingSet = []
    validationSet = cks[count]
    count2 = 0
    while count2 < len(cks):
      if count2 != count:
        trainingSet.append(cks[count2])
      count2 += 1
    trainingSets.append(flatten(trainingSet))
    validationSets.append(validationSet)
    count += 1
  count = 0
  correct = 0
  incorrect = 0
  while count < len(trainingSets):
    trainingSet = trainingSets[count]
    validationSet = validationSets[count]
    tsData = []
    tsClass = []
    vData = []
    vClass = []
    for element, classification in trainingSet:
      tsData.append(element)
      tsClass.append(classification)
    for element, classification in validationSet:
      vData.append(element)
      vClass.append(classification)
    if classifier == 'svm':
      clf = svm.SVC(C = Cparam, gamma = Gparam, kernel = Kparam)
    elif classifier == 'linear':
      clf = linear_model.SGDClassifier()    
    clf.fit(tsData, tsClass)
    count2 = 0
    while count2 < len(vData):
      prediction = clf.predict(vData[count2])
      assert(len(prediction) == 1)
      if prediction[0] == vClass[count2]:
        correct += 1
      else:
        incorrect += 1
      count2 += 1
    print count
    count += 1
  print str(correct) + " correct guesses and " + str(incorrect) + " incorrect guesses"
  return float(correct) / float(correct + incorrect)

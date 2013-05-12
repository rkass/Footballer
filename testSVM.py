#deprecated. refer to svmcrossvalidation
import buildVector as bv
from sklearn import svm
import cPickle

with open('serialized_vectors.p', 'rb') as fp:
  vects = cPickle.load(fp)
X = []
y = []
for e, c in vects:
  X.append(e)
  y.append(c)


training = X[0:399] + X[500:]
yt = y[0:399] + y[500:]
validation = X[400:499]
vt = y[400:499]
 
clf = svm.SVC()
clf.fit(training, yt)
print "Support vectors built...validating..."
correct = 0
incorrect = 0

count = 0
while count < len(validation):
  prediction = clf.predict(validation[count])
  assert(len(prediction) == 1)
  if prediction[0] == vt[count]:
    correct += 1
  else:
    incorrect += 1
  count += 1

pct = float(correct) / (incorrect + correct)
print str(correct) + " Correct guesses and " + str(incorrect) + " incorrect guesses"
print str(pct)

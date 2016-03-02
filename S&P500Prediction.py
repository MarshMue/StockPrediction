import Quandl
import random
import config
spindex = Quandl.get("YAHOO/INDEX_GSPC", authtoken=config.key)

diff = (abs(spindex.Open - spindex.Close))
resetdiff = []
resetval = []
i = 0
while i < diff.values.size:
        resetdiff.append(diff[i])
        resetval.append(spindex.Close[i])
        i += 1
samplesize = 10000
finalval = 0
y = 0
while y < samplesize:
    n = 0
    iterations = 365
    diffarr = resetdiff
    valuearr = resetval

    while n < iterations:
        # get random value in array of differences and add it back to the diff array
        x = int(abs(random.random() * (len(diffarr) - 1)))
        diffarr.append(diffarr[x])
        # add the difference to the value array to try to predict what it will be
        valuearr.append(valuearr[len(valuearr) - 1] + diffarr[x])
        n += 1
    print str(valuearr[len(valuearr) - 1])
    finalval += valuearr[len(valuearr) - 1]
    y += 1
    print y
print finalval / samplesize

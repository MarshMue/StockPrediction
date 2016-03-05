import Quandl
import random
import config
import matplotlib.pyplot as plt

# get historical data of S&P
spindex = Quandl.get("YAHOO/INDEX_GSPC", authtoken=config.key)

# calculate daily difference in stock value
diff = spindex.Close - spindex.Open
# num of stock days in a year
year = 252
# years to simulate
years = 10
# days of simulation
days = year * years
# actual current value
realval = spindex.Close[spindex.Close.values.size - 1]

# set up static arrays of known data
resetdiff = []
resetval = []

# set up arrays for ceiling and floor
ceiling = [0] * (diff.values.size - 1)        # add days to size when not backtesting
floor = [10000] * (diff.values.size - 1)      # add days to size when not backtesting

# real values of market at close
ii = 0
realvals = []
while ii < spindex.Close.values.size:
    realvals.append(spindex.Close[ii])
    ii += 1

i = 0                 # set this if you want to backtest, otherwise 0

# set reset arrays to known values as well as floor and ceiling
while i < diff.values.size - days:
        resetdiff.append(diff[i])
        resetval.append(spindex.Close[i])
        ceiling[i] = spindex.Close[i]
        floor[i] = spindex.Close[i]
        i += 1

samplesize = 10000
finalval = 0
y = 0
# run simulation sample size
while y < samplesize:
    n = 0
    # reset arrays for simulation
    diffarr = resetdiff[:]
    valuearr = resetval[:]

    # simulate defined # of days of market action
    while n < days:
        # get random value in array of differences and add it back to the diff array
        x = int(abs(random.random() * (len(diffarr) - 1)))
        diffarr.append(diffarr[x])
        # add the difference to the value array to try to predict what it will be
        valuearr.append(valuearr[len(valuearr) - 1] + diffarr[x])
        index = len(valuearr) - 2
        if valuearr[index] > ceiling[index]:
            ceiling[index] = valuearr[index]
        if valuearr[index] < floor[index]:
            floor[index] = valuearr[index]
        n += 1

    finalval += valuearr[len(valuearr) - 1]
    y += 1
ind = 0

# debugging
# while ind < ceiling.__len__():
#     if ceiling[ind] == 0:
#         print str(ind)
#     ind += 1
# ind = 0
# while ind < floor.__len__():
#     if floor[ind] == 10000:
#         print str(ind)
#     ind += 1
# end debugging

# calculate average estimate based on simulations
avgest = finalval / samplesize
print "estimate value: " + str(avgest)
# uncomment for backtesting
print "percent error: " + str(abs(avgest-realval) * 100 / realval) + "\nBacktesting " + str(years) + " years"
plt.plot(range(0, len(floor)), floor, 'b-', range(0, len(ceiling)), ceiling, 'r-', range(0, len(realvals)), realvals, 'g-')
plt.title('S&P 500 Index')
plt.xlabel('Days since fund inception')
plt.ylabel('Value')
plt.show()

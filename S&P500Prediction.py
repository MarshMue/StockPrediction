import Quandl
import random
import config
# get historical data of S&P
spindex = Quandl.get("YAHOO/INDEX_GSPC", authtoken=config.key)

# calculate daily difference in stock value
diff = spindex.Close - spindex.Open
# num of stock days in a year
year = 252
# years to simulate
years = 2
# days of simulation
days = year * years
# actual current value
realval = spindex.Close[spindex.Close.values.size - 1]

# set up static arrays of known data
resetdiff = []
resetval = []
i = diff.values.size - days    # set this if you want to backtest, otherwise 0
while i < diff.values.size:
        resetdiff.append(diff[i])
        resetval.append(spindex.Close[i])
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
        n += 1

    finalval += valuearr[len(valuearr) - 1]
    y += 1

# calculate average estimate based on simulations
avgest = finalval / samplesize
print "estimate value: " + str(avgest)
# uncomment for backtesting
print "percent error: " + str(abs(avgest-realval) * 100 / realval) + "\nBacktesting " + str(years) + " years"

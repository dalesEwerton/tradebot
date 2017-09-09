import time
import sys, getopt
import datetime
from poloniex import poloniex
import matplotlib.pyplot as plt

def main(argv):
	period = 0.5
	pair = "BTC_XMR"
	prices = []
	currentMovingAverage = 0;
	lengthOfMA = 0
	startTime = False
	endTime = False
	historicalData = False
	tradePlaced = False
	typeOfTrade = False
	dataDate = ""
	orderNumber = ""
	initialPrice = 0;
	orderBuyed = 0;
	profit = []
	
	try:
		opts, args = getopt.getopt(argv,"hp:c:n:s:e:",["period=","currency=","points="])
	except getopt.GetoptError:
		print 'trading-bot.py -p <period length> -c <currency pair> -n <period of moving average>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'trading-bot.py -p <period length> -c <currency pair> -n <period of moving average>'
			sys.exit()
		elif opt in ("-p", "--period"):
			if (int(arg) in [300,900,1800,7200,14400,86400]):
				period = arg
			else:
				print 'Poloniex requires periods in 300,900,1800,7200,14400, or 86400 second increments'
				sys.exit(2)
		elif opt in ("-c", "--currency"):
			pair = arg
		elif opt in ("-n", "--points"):
			lengthOfMA = int(arg)
		elif opt in ("-s"):
			startTime = arg
		elif opt in ("-e"):
			endTime = arg




	conn = poloniex('key goes here','key goes here')

	if (startTime):
		historicalData = conn.api_query("returnChartData",{"currencyPair":pair,"start":startTime,"end":endTime,"period":period})

	while True:
		if (startTime and historicalData):
			nextDataPoint = historicalData.pop(0)
			lastPairPrice = nextDataPoint['weightedAverage']
			dataDate = datetime.datetime.fromtimestamp(int(nextDataPoint['date'])).strftime('%Y-%m-%d %H:%M:%S')
		elif(startTime and not historicalData):
			exit()
		else:
			currentValues = conn.api_query("returnTicker")
			lastPairPrice = currentValues[pair]["last"]
			dataDate = datetime.datetime.now()
			

		if (len(prices) > 0):
			currentMovingAverage = sum(prices) / float(len(prices))
			
		#Trading -- 3% Strategy
		if(initialPrice == 0):
			initialPrice =  float(lastPairPrice) - (float(lastPairPrice) * 0.03);
			print "Initial order price: " + str(initialPrice);
		elif(initialPrice >= lastPairPrice):
			print "BUY ORDER"
			initialPrice = -1
			orderBuyed = lastPairPrice + (lastPairPrice * 0.03);
		elif(initialPrice == -1):
			if(lastPairPrice >= orderBuyed):
				print "SELL_ORDER"
				profitAtual = (orderBuyed * 0.03) + (lastPairPrice - orderBuyed)
				profit.append(sum(profit) + profitAtual)
				plt.plot(profit)

		print "%s Period: %ss %s: %s Moving Average: %s" % (dataDate,period,pair,lastPairPrice,currentMovingAverage)

		prices.append(float(lastPairPrice))
		prices = prices[-lengthOfMA:]
		if (not startTime):
			time.sleep(int(period))


if __name__ == "__main__":
	main(sys.argv[1:])

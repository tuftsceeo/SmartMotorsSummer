def nearestNeighbor(data, point):
    try:
        point = point[0]
    except TypeError:
        pass
    if len(data) == 0:
        return 0
    diff = 1000
    test = None
    for i in data:
		if abs(i[0] - point) <= diff:
			diff = abs(i[0] - point)
			test = i
    return test[1]


def extremeLine(data, point): # Not currently functional
    try:
        point = point[0]
    except TypeError:
        pass
	dataSorted = list(data)
	dataSorted.sort(key = lambda x:x[0])
	low = dataSorted[0]
	high = dataSorted[-1]
    return int((high[1] - low[1])/(high[0] - low[0])*(point - low[0]) + low[1])
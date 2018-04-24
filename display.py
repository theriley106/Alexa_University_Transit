#https://api.mapbox.com/styles/v1/mapbox/streets-v10/static/pin-s-a+9ed4bd(-122.46589,37.77343),pin-s-b+000(-122.42816,37.75965),path-5+f44-0.5(%7DrpeFxbnjVsFwdAvr@cHgFor@jEmAlFmEMwM_FuItCkOi@wc@bg@wBSgM)/auto/500x300?access_token=pk.eyJ1IjoidGhlcmlsZXkxMDYiLCJhIjoiY2o4cm1xZzdnMTgzMDMzbnR1d3Q2Y2p6byJ9.C-Kuwbt67fBaEg0V5rGXzg
#https://api.mapbox.com/styles/v1/mapbox/streets-v10/static/pin-s-a+9ed4bd(-122.46589,37.77343),pin-s-b+000(-122.42816,37.75965)/auto/500x300?access_token=pk.eyJ1IjoidGhlcmlsZXkxMDYiLCJhIjoiY2o4cm1xZzdnMTgzMDMzbnR1d3Q2Y2p6byJ9.C-Kuwbt67fBaEg0V5rGXzg


def genMap(point1, point2=None, segment=None):
	url = "https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v9/static/pin-s-bus+9ed4bd{}".format(str(tuple(point1)).replace(" ", ""))
	if point2 != None:
		url = url + ",pin-s-b+000{}".format(str(tuple(point2)).replace(" ", ""))
	if segment != None:
		url = url + ",path-5+f44-0.5({})".format(str(segment))
	url = url + "/auto/1024x600?access_token=pk.eyJ1IjoidGhlcmlsZXkxMDYiLCJhIjoiY2o4cm1xZzdnMTgzMDMzbnR1d3Q2Y2p6byJ9.C-Kuwbt67fBaEg0V5rGXzg"
	return url


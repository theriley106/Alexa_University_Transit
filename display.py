#https://api.mapbox.com/styles/v1/mapbox/streets-v10/static/pin-s-a+9ed4bd(-122.46589,37.77343),pin-s-b+000(-122.42816,37.75965),path-5+f44-0.5(%7DrpeFxbnjVsFwdAvr@cHgFor@jEmAlFmEMwM_FuItCkOi@wc@bg@wBSgM)/auto/500x300?access_token=pk.eyJ1IjoidGhlcmlsZXkxMDYiLCJhIjoiY2o4cm1xZzdnMTgzMDMzbnR1d3Q2Y2p6byJ9.C-Kuwbt67fBaEg0V5rGXzg
#https://api.mapbox.com/styles/v1/mapbox/streets-v10/static/pin-s-a+9ed4bd(-122.46589,37.77343),pin-s-b+000(-122.42816,37.75965)/auto/500x300?access_token=pk.eyJ1IjoidGhlcmlsZXkxMDYiLCJhIjoiY2o4cm1xZzdnMTgzMDMzbnR1d3Q2Y2p6byJ9.C-Kuwbt67fBaEg0V5rGXzg


def genMap(point1, point2=(-82.791442, 34.641643)):
	url = "https://api.mapbox.com/styles/v1/mapbox/streets-v10/static/pin-s-a+9ed4bd{},pin-s-b+000{}/auto/1024x600?access_token=pk.eyJ1IjoidGhlcmlsZXkxMDYiLCJhIjoiY2o4cm1xZzdnMTgzMDMzbnR1d3Q2Y2p6byJ9.C-Kuwbt67fBaEg0V5rGXzg".format(str(point1).replace(" ", ""), str(point2).replace(" ", ""))
	return url


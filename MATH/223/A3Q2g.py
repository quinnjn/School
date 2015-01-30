for x in xrange(0,24):
	s = str(x)+" & $"
	xsquared = x*x
	s += str(xsquared)
	if(xsquared >= 24):
		while xsquared >=24:
			xsquared -=24
		s += " \equiv "+str(xsquared)

	s +="$\\\\"
	print s
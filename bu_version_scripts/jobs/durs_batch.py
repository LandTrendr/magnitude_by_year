import glob, os, subprocess, sys

#scenes = ['045026', '045027', '045028', '045029'] - done! - 6
#scenes = ['044026', '044027', '044028', '044029', '044030', '044031', '044032'] - 7
#scenes = ['043027', '043028', '043029', '043030', '043031', '043032']- done! -7
#scenes = ['043031', '043032']
scenes = ['045030', '045031']
#scenes = ['042028', '042029', '042030', '042031'] - done! -4
 
indeces = ['nbr', 'wetness', 'band5']
#indeces = ['band5']
#043031 - band 5 does not have durs file
for scene in scenes:

	print scene

	for index in indeces:
	
		print index
	
		yrssearch = glob.glob("/vol/v1/scenes/" + scene + "/outputs/" + index + "/*vertyrs.bsq")
		try:
			yrsfile = yrssearch[-1]
		except IndexError:
			print "indexerr"
			print yrssearch
			sys.exit()
# 		if len(yrssearch) > 1:
# 			print "More than 1 file found: ", yrssearch
# 			toto = raw_input("pause")
# 			if toto == '1':
# 				yrsfile = yrssearch[-1]
# 				print yrsfile
# 		else:
# 			yrsfile = yrssearch[0]
# 			
		
		durssearch = glob.glob("/vol/v1/scenes/" + scene + "/outputs/" + index + "/*durs.bsq")
		try:
			dursfile = durssearch[-1]
		except IndexError:
			print "indexerr"
			print durssearch
			sys.exit()
# 		if len(durssearch) > 1:
# 			print "More than 1 file found: ", durssearch
# 			toto = raw_input("pause")
# 			if toto == '1':
# 				dursfile = durssearch[-1]
# 				print dursfile
# 		else:
# 			dursfile = durssearch[0]
			
		outputfile = "/vol/v1/proj/cmonster/eastside/fitted_imagery/scenes/" + scene + "_" + index + "_yearly_duration.bsq"
		
		cmd = "python segment_split.py {0} {1} {2}".format(yrsfile, dursfile, outputfile)
		
		subprocess.call(cmd, shell=True)
		
		del yrsfile, dursfile
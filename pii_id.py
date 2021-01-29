import re, unidecode, os, importlib, json
from operator import itemgetter


def findall(p, s):
	'''Yields all the positions of
	the pattern p in the string s.'''
	i = s.find(p)
	while i != -1:
		yield i
		i = s.find(p, i+1)

def calculate_distance(data,data_decoded,x,keywords,threshold) :
	'''Calculate distance between two words on a string,
	prioritizes nearest find, ignores unicode.'''
	results = []

	i_x = data.find(x)
	relevant_data = data_decoded[:i_x]

	for k in keywords :
		try :
			i_k = min([ i for i in findall(k,relevant_data)], key=lambda x:abs(x-i_x))
		except :
			continue

		i_k += len(k)
		percent_distance = 100-(abs(i_x-i_k)*100 / len(data))
		if threshold > percent_distance :
			continue
		results.append( [ x, k , percent_distance ] )

	return sorted(results, key=itemgetter(2))	


def load_sensors() :
	sensors_folder = "./sensors"
	sensors = {}
	psensors = os.listdir(sensors_folder)
	
	for f in psensors :
		location = os.path.join(sensors_folder,f)

		if f[-5:] != ".json": continue

		s = json.loads(open(location,'r').read())
		
		sensors[s["name"].lower()] = s

		if "function_file" in s.keys() :
			info = importlib.util.spec_from_file_location( s["name"], os.path.join(sensors_folder,s["function_file"]) )
			p = importlib.util.module_from_spec(info)
			info.loader.exec_module(p)
			sensors[s["name"].lower()]["function"] = p.check	

	return sensors	

def run_sensors(options,data,threshold=0.0) :
	sensors = load_sensors()
	pii = {}

	options = [x.lower() for x in options]

	if "all" in options : 
		options = sensors.keys()

	data_u = unidecode.unidecode(data.lower())
	for o in options :
		if o in sensors.keys() :
			sensor_regex = re.compile(sensors[o]["regex"])
			data_regexed = re.findall(sensor_regex,data)

			probable = []
			for d in data_regexed :
				if type(d) == tuple :
					d = ''.join(d)
				if "function" in sensors[o].keys() :
					f_probable = sensors[o]["function"](d)
					probable.extend( f_probable )
				else :
					probable_distance = calculate_distance(data,data_u,d,sensors[o]["keywords"],threshold)
					if len(probable_distance) > 0 :
						probable.append( probable_distance )
			if len(probable) > 0 :	
				pii[o] = probable

	return pii

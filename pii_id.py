import re, unidecode, os, importlib, json
from operator import itemgetter

def calculate_distance(data,x,keywords) :
	results = []

	for k in keywords :
		i_x = data.find(x)
		relevant_data = unidecode.unidecode(data[:i_x].lower())
		i_k = relevant_data.find(k)

		if i_k < 0 : continue

		i_k += len(k)
		percent_distance = 100-((i_x-i_k)*100 / len(data))
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

def run_sensors(options,data) :
	sensors = load_sensors()
	pii = {}

	options = [x.lower() for x in options]

	if "all" in options : 
		options = sensors.keys()

	for o in options :
		if o in sensors.keys() :
			sensor_regex = re.compile(sensors[o]["regex"])
			data_regexed = re.findall(sensor_regex,data)

			probable = []

			for d in data_regexed :
				print(d)
				if "function" in sensors[o].keys() :
					f_probable = sensors[o]["function"](d)
					probable.extend( f_probable )
				else :
					probable.append( calculate_distance(data,d[0],sensors[o]["keywords"] ) )
			
			pii[o] = probable

	return pii

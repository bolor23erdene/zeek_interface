import pandas as pd
import os 
import sys

def extract_protocol_names(input_filename):
	""" Returns all protocol types of of conn.log and network protocol.logs from the text file retrieved from the original website 
	Attributes
	----------
	input_filename: the file that includes all the protocol types
	all_protocol_types: all protocol types of logs
	"""
	f = open(filename, "r")
	all_protocol_types = [row.split()[0] for row in f]
	return all_protocol_types 




def specs_logs(all_protocol_types):
	""" Converts all existing log.csv files into pandas dataframe
	Attributes
	----------
	all_protocol_types: names of all protocol logs
	dic_protocol: returns panda dataframe of the log files
	count: returns the number of different protocol log files 
	"""
	count = 0
	dic_protocol = {}
	all_protocol_types = [protocol_name+'.csv' for protocol_name in all_protocol_types]
	for protocol_name_csv in all_protocol_types:
		#print(protocol_name_csv)
		if os.path.exists(protocol_name_csv):
			field_names = pd.read_csv(protocol_name_csv, nrows=1)
			pd_file = pd.read_csv(protocol_name_csv,error_bad_lines=False)
			#print(protocol_name_csv, pd_file, pd_file.columns)
			#print(protocol_name_csv, pd_file.shape)
			#print(pd_file.columns)
			dic_protocol[protocol_name_csv.split('.')[0]] = pd_file
			count = count + 1
	#print(count)
	return dic_protocol, count

def free_text_func(dic_protocol, free_text):
	""" Returns all log files with entries that only include specified free_text 
	Attributes
	----------
	dic_protocol: protocol log files in pandas dataframe
	free_text_dic: returns the log files with specified free_text
	"""
	free_text_dic = {}
	for key in dic_protocol.keys():
		df = dic_protocol[key]
		free_text_df = pd.DataFrame()
		string_fields = list(df.select_dtypes(include='object').columns)
		for field in string_fields:
			sub_df = df[df[field].str.contains(free_text, na=False)]
			if free_text_df.empty:
				free_text_df = sub_df
			else:
				pd.concat([free_text_df, sub_df], axis=0)

		free_text_df = free_text_df.drop_duplicates()

		#print("TEMP_DF",key)
		#print(free_text_df)
		free_text_dic[key] = free_text_df

	return free_text_dic


def log_and_correlation(free_text_dic, uid, isUid, field_name, compare_val, protocol_type):
	""" Find all entries within a single log matching the provided query, find logs that has the matching uid field (if isUid = True), and export the results 
	Attributes
	----------
	free_text_dic: all entries with specified the free_text
	log_query_df: logs matching the provided query
	correl_df: entries with matching uid field if given 
	isUid: if user id or uid is provided
	uid: if provided, what the uid is
	"""
	for protocol_name in free_text_dic.keys():
		if protocol_name == protocol_type:
			df = free_text_dic[protocol_type]
			#print("COMPARES", compare_val, field_name)
			#print(df[field_name])
			log_query_df = df[df[field_name]==compare_val]
			#print(log_query_df, "log_query_df")
		else:
			log_query_df = pd.DataFrame()
			df = pd.DataFrame()

		if isUid == True:
			if 'uid' in list(df.columns):
				correl_df = df[df['uid']==uid]
				correl_df.to_csv(protocol_type+'_matches.csv')
				#print(correl_df,"CORREL_DF")
		else:
			log_query_df.to_csv(protocol_type+'_matches.csv')
			#print(log_query_df)

if __name__ == "__main__":

	free_text =  input("Input free-text query (example is google.com): \n")

	log_column = input("Input log.column query (example is ssl.id_resp_h = \"216.58.207.174\"): \n") 

	match_uid =  input("Input the matching uid query, (examples CXgnmuLSngpDdUlZ7 or no): \n") 

	# for log column
	first_part = log_column.split('=')[0]
	second_part = log_column.split('=')[1]
	protocol_type = first_part.split('.')[0].replace(" ","")
	field_name = first_part.split('.')[1].replace(" ","")
	compare_val = second_part.replace(" ","")

	if "\"" in compare_val:
		compare_val = compare_val.replace("\"", "")
	else:
		compare_val = float(compare_val)

	#print(protocol_type, field_name, compare_val)

	uid = match_uid
	isUid = True

	# for match_uid
	if match_uid == "no":
		uid = None
		isUid = False

		
	
	filename = "networkProtocols"

	all_protocol_types = extract_protocol_names(filename)

	#print("First Step\n\n\n", all_protocol_types)

	dic_protocol, count = specs_logs(all_protocol_types)

	#print("Second Step\n\n\n", count, dic_protocol)

	free_text_dic = free_text_func(dic_protocol, free_text)

	#print("Third Step\n\n\n", free_text_dic)

	#print("CALLING THE FUNCTION \n\n\n")

	log_and_correlation(free_text_dic, uid, isUid, field_name, compare_val, protocol_type)
	




from flask import Flask, render_template, request, json, url_for
from SPARQLWrapper import SPARQLWrapper, JSON
#from ColProperty import ColProperty
from flask_cors import CORS, cross_origin
import json, ast


app = Flask(__name__)
sparql = SPARQLWrapper("http://localhost:8890/sparql")

#----------------------------- for loading the home page --------------------------------
table_data = {}
header_data = []
header_map = {}
pca_map = {}
@app.route("/")
def main():
	return render_template('main.html')

@app.route("/gohome") 
def gohome():
	return render_template('main.html')

@app.route("/goindex", methods=['POST'])
def goindex():
	theme = request.form['inputTheme']
	print theme
	return render_template('index.html', theme=theme)

@app.route("/goindexafterclick/<string:themeval>", methods=['POST'])
def goindexafterclick():
	theme = themeval#theme = request.get_data()#request.args.get('theme')
	print theme
	return render_template('index.html', theme=theme)
#---------------------------- this is of no importance -------------------------------------

@app.route("/showSignUp")
def showSignUp():
	return render_template('signup.html')


#------------------- function for getting tables related to a given theme --------------------------------------

@app.route("/findByTheme",methods=['POST'])
def findByTheme():


	#_theme = "<"+request.form['inputTheme']+">"
	_theme = "<"+request.get_data()+">"

	

	sparql.setQuery("""
	SELECT ?g ?pa ?ca
where { graph ?g {

{ ?g <http://itlvocab.org/property/parentTheme>  """+_theme +""".
  ?g <http://itlvocab.org/property/row> 0}.
{?g <http://itlvocab.org/property/parentAnchor> ?pa . 
OPTIONAL{?g <http://itlvocab.org/property/childAnchor> ?ca }}

}
}
	""")
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	tables = []

	for result in results["results"]["bindings"]:
		#tableName = (result["g"]["value"]).encode('utf-8').split("/")[-1].split("#")[0]
		#print tableName
		tables.append((result["g"]["value"]).encode('utf-8'))
	# json_string = json.dumps([ob.__dict__ for ob in tables])
	return json.dumps(tables)



#------------------------------- function for getting table header based on the theme ----------------------------------------

@app.route('/getHeaderByTableName', methods=['GET','POST'])
def getdataa():
	#clicked=None
        if request.method == "POST":
        #clicked=request.json['data']
		namedgraph = request.get_data()

		sparql.setQuery("""
	SELECT ?AncColInd ?AncCol ?AncColType ?ConnectedCol ?ColIndex ?ConnectedColType ?Prop from <"""+namedgraph +""">where 
	{
		{
			{<"""+namedgraph+"""> <http://itlvocab.org/property/parentAnchor> ?AncCol}
			UNION 
			{<"""+namedgraph+"""> <http://itlvocab.org/property/childAnchor> ?AncCol}
		}.
	?AncCol <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>?AncColType.?AncCol<http://itlvocab.org/property/columnIndex>?AncColInd.
	?AncCol ?Prop ?ConnectedCol .
	?ConnectedCol <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?ConnectedColType.
	?ConnectedCol <http://itlvocab.org/property/columnIndex> ?ColIndex

	}	
	ORDER BY ?ColIndex """)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert() 
	colProperties = {}
	output = []
	header_property_map = {}
	for result in results["results"]["bindings"]:
		ancColIndex=(result["AncColInd"]["value"]).encode('utf-8')
		conColIndex=(result["ColIndex"]["value"]).encode('utf-8')
		ancCol = (result["AncCol"]["value"]).encode('utf-8').split("/")[-1].split(".")[-1]
		conCol = (result["ConnectedCol"]["value"]).encode('utf-8').split("/")[-1].split(".")[-1]
		header_property_map[result["AncColInd"]["value"]] = result["AncColType"]["value"]+"|"+result["AncColType"]["value"]+"|"+result["AncCol"]["value"]
		header_property_map[result["ColIndex"]["value"]] = result["ConnectedColType"]["value"]+"|"+result["Prop"]["value"]+"|"+result["AncCol"]["value"]
		

		print "check header Property"
		print header_property_map
		print "-------------------------------"
		#colproperty = ColProperty(ancCol,conCol,prop)
		if ancColIndex in colProperties:
			print "NO"
		else:
						colProperties[ancColIndex]=ancCol
		colProperties[conColIndex]=conCol
	#my_set = set(colProperties)
	#my_new_list = list(my_set)
	#print "----------------------- start test --------------------"
	#print header_property_map
	#print "------------------------ end test ----------------------"	
	keylist = colProperties.keys()
	keylist.sort()
	header_data=[]
	print "----------------------- start test --------------------"
	print keylist#header_property_map
	print "------------------------ end test ----------------------"	
	for key in keylist:
	    header_data.append(colProperties[key]+"|"+header_property_map[key])
	
	###print header_data
	table_data = {}
	for x in header_data:
		table_data[x.split("|")[0]] = ""
	
	
	#header_map={}
	i = 0
	#header_data= ast.literal_eval(json.dumps(header_data))

	for x in header_data:
		header_map[x.split("|")[0]] = i
		i+=1
	
	#for x in results["results"]["bindings"]:
	return json.dumps(header_data)
	#return "OK"



#----------------------------- function for getting table data based on the theme ------------------------------------------------


@app.route('/gettablerows', methods=['GET','POST'])
def getTabledata():
	temp_table_data = {}
	final_table_data = {}
	temp_link_data = {}
	final_link_data = {}
	if request.method == "POST":
		namedgraphtable = request.get_data()
		namedgraphtable= namedgraphtable.split(";");
		tablename = "\""+namedgraphtable[0].split("/")[-1].split("#")[0]+"\""
		sparql.setQuery("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?g ?row ?AncCol ?SrcData ?SrcDataURI ?ConnectedCol ?ConnectedColData ?ConnectedColDataURI ?propmined  
where { graph ?g {

{?g <http://itlvocab.org/property/parentTheme> <"""+namedgraphtable[1]+""">}. {?g <http://itlvocab.org/property/row> ?row}.
{{?g <http://itlvocab.org/property/parentAnchor> ?AncCol } UNION {?g <http://itlvocab.org/property/childAnchor> ?AncCol }}.
{?AncCol <http://itlvocab.org/property/relatedTo> ?ConnectedCol}.
?AncCol <http://itlvocab.org/property/data> ?SrcData . ?ConnectedCol  <http://itlvocab.org/property/data> ?ConnectedColData .
?SrcDataURI rdfs:label ?SrcData.
OPTIONAL {?ConnectedColDataURI rdfs:label ?ConnectedColData}.
OPTIONAL {?SrcDataURI ?propmined ?ConnectedColDataURI}


} . FILTER regex(?g,"""+ tablename + """ ,"i")
}
ORDER BY ?row""")
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		#for x in results["results"]["bindings"]:
		#	y = ast.literal_eval(json.dumps(x))
		#	temp_table_data[x['SrcData']['value']] = table_data
		#	temp_link_data[y['SrcData']['value']] = table_data



		for i  in results["results"]["bindings"]:
			final_table_data[int(i['row']['value'])] = {}
			final_link_data[int(i['row']['value'])] = {}			

		
		#temp_table_data = ast.literal_eval(json.dumps(temp_table_data))
		#temp_link_data = ast.literal_eval(json.dumps(temp_link_data))
		for temp in results["results"]["bindings"]:
			temp_variable = 'ConnectedColDataURI'	
			x = ast.literal_eval(json.dumps(temp)) #-----Converting the unicode charecters returned from the query is converted into strings --------#
			y = ast.literal_eval(json.dumps(temp)) #-----Converting the unicode charecters returned from the query is converted into strings --------#
			#temp_table_data[x['SrcData']['value']][header_map[x['ConnectedCol']['value'].split(".")[-1]]] = x['ConnectedColData']['value']
			#temp_link_data[y['SrcData']['value']][header_map[y['ConnectedCol']['value'].split(".")[-1]]] = y['ConnectedColDataURI']['value']
			#temp_table_data[x['SrcData']['value']][header_map[x['AncCol']['value'].split(".")[-1]]] = x['SrcData']['value']
			#temp_link_data[x['SrcData']['value']][header_map[x['AncCol']['value'].split(".")[-1]]] = x['SrcDataURI']['value'] 
			final_table_data[int(x['row']['value'])][header_map[x['AncCol']['value'].split(".")[-1]]] = x['SrcData']['value']
			final_link_data[int(x['row']['value'])][header_map[x['AncCol']['value'].split(".")[-1]]] = x['SrcDataURI']['value']
			final_table_data[int(x['row']['value'])][header_map[x['ConnectedCol']['value'].split(".")[-1]]] = x['ConnectedColData']['value']#temp_table_data[x['SrcData']['value']]
			if temp_variable in y:
				final_link_data[int(x['row']['value'])][header_map[x['ConnectedCol']['value'].split(".")[-1]]] = y['ConnectedColDataURI']['value']#temp_link_data[x['SrcData']['value']]			
			else:
				final_link_data[int(x['row']['value'])][header_map[x['ConnectedCol']['value'].split(".")[-1]]] = ""

		transfer_data = []
		print "---------------------test1---------------------"
		print final_table_data
		print "----------------------end test ----------------------"
		
		for x in final_table_data.keys():
			transfer_data.append(final_table_data[x])
		
		#print transfer_data
 		#return json.dumps(transfer_data)
 		data_link_map = {}#new
 		data_link_map[0] = final_table_data#new
 		data_link_map[1] = final_link_data#new

 		return json.dumps(data_link_map)#new
 		#return json.dumps(final_table_data)#old
		#return render_template("index.html", val = transfer_data)
	

#--------------------------------------------------------------------------------------------
#
@app.route('/getpaca', methods=['POST'])
def getpaca():
	pa_ca_map = {}
	if request.method == "POST":
        #clicked=request.json['data']
		namedgraph = request.get_data()
		#namedgraph= namedgraph.split(";");
		#tablename = "\""+namedgraph[0].split("/")[-1].split("#")[0]+"\""
		print namedgraph
		print "nnnnnnnnnnnnnnnn"
		sparql.setQuery("""
	SELECT ?AncColInd ?AncCol ?AncColType ?ConnectedCol ?ColIndex ?ConnectedColType ?Prop from <"""+namedgraph +""">where 
	{
		{
			{<"""+namedgraph+"""> <http://itlvocab.org/property/parentAnchor> ?AncCol}
			UNION 
			{<"""+namedgraph+"""> <http://itlvocab.org/property/childAnchor> ?AncCol}
		}.
	?AncCol <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>?AncColType.?AncCol<http://itlvocab.org/property/columnIndex>?AncColInd.
	?AncCol ?Prop ?ConnectedCol .
	?ConnectedCol <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?ConnectedColType.
	?ConnectedCol <http://itlvocab.org/property/columnIndex> ?ColIndex

	}	
	ORDER BY ?ColIndex """)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert() 
	print results
	print "rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr"
	for result in results["results"]["bindings"]:
		pa_ca_map[(result["AncColInd"]["value"]).encode('utf-8')] = []

	print pa_ca_map
	for x in results["results"]["bindings"]:
		bol_val = int(x["ColIndex"]["value"]) not in pa_ca_map.keys()
		print bol_val, int(x["ColIndex"]["value"]), pa_ca_map.keys()
#		(x["ColIndex"]["value"]).encode('utf-8') > (x["AncColInd"]["value"]).encode('utf-8') and 
		if(bol_val ):
			pa_ca_map[(x["AncColInd"]["value"]).encode('utf-8')].append((x["ColIndex"]["value"]).encode('utf-8'))	
	
	#pa_ca_map.remove(
	print " ------------------ pa cs -------------------"
	print pa_ca_map
	return json.dumps(pa_ca_map)

#--------------------------------------- Not necessary --------------------------------------
@app.route('/signUp',methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    print "Hello"+ _name
    # validate the received values
    if _name and _email and _password:
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

if __name__ == '__main__':
	app.run()

function colorchange(connecting_column, anchoring_column, property_name,anchoringcolumn_uri, connectedcol_uri)
{
	var links=document.getElementsByTagName("th") ;
	//var tupletext=
	document.getElementById("tuplename").value=anchoringcolumn_uri+"-----"+property_name+"-----"+connectedcol_uri;
	
	if(connecting_column==anchoring_column)
	{
		for (var i = 0 ; i < links.length ; i ++)  
		{links.item(i).style.backgroundColor = 'RoyalBlue' ;  } 
	}
	else
	{
	  
	for (var i = 0 ; i < links.length ; i ++)  
	{links.item(i).style.backgroundColor = 'white' ;  } 
	var cc=document.getElementById(connecting_column);
	var ac=document.getElementById(anchoring_column);
	cc.style.backgroundColor="RoyalBlue ";
	ac.style.backgroundColor="RoyalBlue ";
	}
}
function showSchema() {
   	document.getElementById('mySVG').style.display = "block";
	document.getElementById('schemabuttonclose').style.display = "block";
	document.getElementById('schemabutton').style.display = "none";
	document.getElementById('tuplename').style.display = "block";
	document.getElementById("tuplename").value=" ";
}

function closeSchema() {
   	document.getElementById('mySVG').style.display = "none";
	document.getElementById('schemabutton').style.display = "block";
	document.getElementById('schemabuttonclose').style.display = "none";
	document.getElementById('tuplename').style.display = "none";
	var links=document.getElementsByTagName("th") ;
	for (var i = 0 ; i < links.length ; i ++)  
	{links.item(i).style.backgroundColor = 'white' ;  } 
}
$(function() {
    $('#btnFindByTheme').click(function() {
        
	document.getElementById("header_names").innerHTML = "" ;
	var searchedname=document.getElementById("inputTheme").value;
	document.getElementById("searchedname").innerHTML = searchedname.split('/').pop() ;
	document.getElementById("vocabulary").innerHTML = searchedname;
	document.getElementById('schemabutton').style.display = "block";
	document.getElementById("table_names").setAttribute("value", "none");
	 $.ajax({
            url: '/findByTheme',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
	       console.log(response);
			console.log("Hi..ANMOL");
                var tableThemes = response.split("[")[1].split("]")[0].split(",");
                console.log(tableThemes)
		var set_id = " id = \" "
                var value_tag = "value = \""
                var on_click = "onclick = \"getdata(value)\"" 
                var html = "";
                for (var i = 0; i < tableThemes.length; i++) 
		{
		    table_name=tableThemes[i].split("/")[tableThemes[i].split("/").length-1].split("#")[0];
                    value_tag += tableThemes[i]
                    value_tag += "\""
		    set_id = set_id + table_name + "\"";
                    html+="<tr "+ "class = \"clickable-row\" >";
		    var checkbox=" <input type='checkbox' id = '"+table_name+"' onchange='func("+tableThemes[i]+", this)' value='Select' />";
		    console.log("Checkbox..Check?");
		    console.log(checkbox);
		    
                    html+="<td"+" "+on_click+"  "+value_tag  +">"+checkbox+"<a>"+table_name+"</a>"+"</td>";

                    html+="</tr>";

                }
                ///html+="</tbody>";
		console.log("Table Name Html..Check");
		console.log(html);
                document.getElementById("table_names").innerHTML = html;
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});


function func(tablethemename, obj) 
{

		
	if($(obj).is(":checked")){
		var new_obj = document.getElementById("table_names").getAttribute("value");
		if(new_obj == "none"){
			
			document.getElementById("table_names").setAttribute("value",obj.getAttribute("id"));

		}
		else{
		
			document.getElementById(new_obj).checked = false;			
			document.getElementById("table_names").setAttribute("value",obj.getAttribute("id"));
		
		
		}
		$.ajax({
            		url: '/getHeaderByTableName',
            		data: tablethemename,
              		type: 'POST',
           		success: function(response) 
			{
			console.log("checking header data ---------" + response);	
			document.getElementById("mySVG").innerHTML="";
			document.getElementById("header_names").innerHTML = "" ;
			var html="";
			
			var themename = response.split("[")[1].split("]")[0].split(",");
			

			console.log("ThemeNAme....check")
			console.log(themename);
			var data_html = "<tr id = \"data_rows\" >";
			//New
			var table = document.createElement('table');
			var thead= document.createElement('thead');
			table.className="table table-striped table-bordered";
			table.setAttribute("id", "themedata");
			table.setAttribute("cellspacing", "0");
			table.setAttribute("width", "100%");
			var tr = document.createElement('tr');   
			tr.setAttribute("id","header_id");
			var size=themename.length;
			//ANMOL
			var svg=document.createElement("svg");
			svg.setAttribute("height","1000px");
			svg.setAttribute("width","1000px");
			var svgNS = "http://www.w3.org/2000/svg";

			var length=0;
			for (var i = 0; i < themename.length; i++)
				{

					var temp=themename[i]//.split("\"");
					var col_name=temp.split("|")[0].split("\"")[1];
					var header_uri= temp.split("|")[1];
					var prop_name= temp.split("|")[2];
					//console.log(temp+" "+col_name+" "+header_uri+" "+prop_name);
					//html+=col_name;
					var th1 = document.createElement('th');
					th1.setAttribute("id",col_name);
					th1.setAttribute("class","headers");
						var a=document.createElement('a');
						a.setAttribute("data-toggle","tooltip");
						var textvalue = document.createTextNode(col_name);
							
						a.setAttribute("title",header_uri);
						//a.setAttribute("href","");
    						a.appendChild(textvalue)
						//td.appendChild(a);
					
					//var text1 = document.createTextNode(col_name);
					th1.appendChild(a);
					tr.appendChild(th1);
					
				}
			thead.appendChild(tr);
			table.appendChild(thead);
			var theme = document.getElementById('inputTheme').value;
			var new_data = tablethemename+";"+theme;
			$.ajax({
            			url: '/gettablerows',
            			data: new_data,
		      		type: 'POST',
		   		success: function(response) 
				{
				var temp=1;
				var tr2=document.createElement('tr'); 
				var tbody=document.createElement('tbody');
				var new_val = {};
				var new_val = JSON.parse(response);
				var obj1 = JSON.stringify(new_val[0]);
				console.log("hello-->"+obj1);
				var obj2 = JSON.stringify(new_val[1]);
				console.log("hello2-->"+obj2);
				var value = {};
				for(var key in new_val[0]){
					value = new_val[0][key];
					value1 = new_val[1][key];
					var value2 = []//{} //new array(); // [];
					var val2 = []//		{} //	new array(); //[];
					for(var key2 in value){
						
						var td=document.createElement('td');
						var a=document.createElement('a');
						a.setAttribute("data-toggle","tooltip");
						var textvalue = document.createTextNode(value[key2]);
							
						a.setAttribute("title",value1[key2]);
						a.setAttribute("href","");
    						a.appendChild(textvalue)
						td.appendChild(a);
						tr2.appendChild(td);
						if(temp%size == 0){
							tbody.appendChild(tr2);
							var tr3=document.createElement('tr');
							tr2=tr3;	
						}
						temp++;
					
					}
					
				}
				table.appendChild(tbody);
				document.getElementById("header_names").appendChild(table); 
				
				 $("#themedata").dataTable({
        "sDom": '<"row view-filter"<"col-sm-12"<"pull-left"f><"pull-right"l><"clearfix">>>t<"row view-pager"<"col-sm-12"<"text-enter"ip>>>'
		});
				//Anmol	
				
				var anchoringcolumn_temp=themename[0].split("|")[0].split("\"")[1];
				var anchoringcolumn_uri=themename[0].split("|")[1];
				//alert(anchoringcolumn_temp);
				//var anchoringcolumn=anchoringcolumn_temp[1];
				for (var i = 0; i < themename.length; i++)
				{
					var temp=themename[i]//.split("\"");
					var col_name=temp.split("|")[0].split("\"")[1];
					var header_uri= temp.split("|")[1];
					var prop_name= temp.split("|")[2].split("\"")[0];
					html+=col_name;
					var x=$('#'+col_name).position();
					var x2=$('#table_data').position();
					console.log(x+"   ");
					var myCircle = document.createElementNS(svgNS,"circle");
					myCircle.setAttributeNS(null,"id",col_name+"_circle");
					myCircle.setAttributeNS(null,"cx",x.left-30);
					myCircle.setAttributeNS(null,"cy",x.top-x2.top-840);
					myCircle.setAttributeNS(null,"r",12);
					myCircle.setAttributeNS(null,"fill","black");
					myCircle.setAttributeNS(null,"stroke","blue");
					myCircle.setAttributeNS(null,"stroke-width","3");
//myCircle.setAttribute("onclick","colorchange(\""+col_name+"\",\""+anchoringcolumn_temp+"\",\""+prop_name+"\",\""+anchoringcolumn_uri+"\",\""+header_uri+"\")");			
					//alert(col_name+" "+anchoringcolumn_temp+"  "+prop_name);
			myCircle.setAttribute("onclick","colorchange(\""+col_name+"\",\""+anchoringcolumn_temp+"\",\""+prop_name+"\",\""+anchoringcolumn_uri+"\",\""+header_uri+"\")");
					document.getElementById("mySVG").appendChild(myCircle);

				}
				var svg=document.getElementById("mySVG");
				svg.setAttribute("style","display:none");


				}
	 		});
			

			}



	 	});
}
	else{
		document.getElementById("mySVG").innerHTML="";
		document.getElementById("header_names").innerHTML = "" ;
		document.getElementById("table_names").setAttribute("value", "none");
	}


	
}





console.log("script linked.")
function swap(){
        if (document.getElementById("nid").innerHTML == "No"){
        document.getElementById("yid").innerHTML = "No";
        document.getElementById("nid").innerHTML = "Yes";
        }
        else{
                document.getElementById("yid").innerHTML = "Yes";
                document.getElementById("nid").innerHTML = "No";  
        }
}


function alert1(){
   alert("HAHAHA You are mad");   
}

function changeBackground(){
        possibity = "0123456789ABCDEF";
        colour = "";
        for (var i =0; i<6 ; ++i){
                colour += possibity[Math.floor(Math.random() * 16)];
        }
        colour = "#" + colour;
        debugger;
        document.body.style.backgroundColor = colour;
}


function tableObject(sr_no1, name1, prize1, quantity1)
{
        this.sr_no = sr_no1;
        this.name = name1;
        this.prize = prize1;
        this.quantity = quantity1;
}

var T1 = new tableObject(1,"salman", 500, 5);
var T2 = new tableObject(2,"shahrukh", 700, 10);
var T3 = new tableObject(3,"Uday", 5, 5000);
var T4 = new tableObject(4,"chunky", 7, 4500);
var row_array = [T1, T2, T3,T4];

function populate_table(row_array)
{
        var html = ""
        if (row_array.length > 0)
        {
                html+= "<table border = 1>"
                html +=     "<tr> <th>sr_no</th> <th>name</th> <th>email_id</th> <th>password</th><th>phone_number</th> </tr>"
                for (var i = 0; i<row_array.length; ++i)
                {
                        var j = i+1; 
                        html +=     "<tr><td>"+ j +"</td> <td>"+row_array[i].name+ "</td> <td>"+row_array[i].email_id+"</td> <td>"+row_array[i].password+"</td><td>"+row_array[i].phone_no+"</td></tr>"
                }
                html += "</table>"
        }
        

        return html
}


function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}




var incoming_json = '';
incoming_json += httpGet("http://127.0.0.1:5000/users");
var record_object = JSON.parse(incoming_json);
var records = record_object.records;
document.getElementById("table_id").innerHTML = populate_table(records);

document.getElementById("yid").addEventListener("mouseover", swap);
document.getElementById("nid").addEventListener("mouseover", swap);
document.getElementById("nid").addEventListener("click", alert1);
document.getElementById("yid").addEventListener("click", alert1);
document.getElementById("yid").addEventListener("mouseover", changeBackground);
document.getElementById("nid").addEventListener("mouseover", changeBackground);

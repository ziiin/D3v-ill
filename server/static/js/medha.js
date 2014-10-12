var tosend="a5";

function sendRequest(){  
console.log("starting a separate ajax");
 $.ajax({
      url:"/re_handler",  
      type: "get",
      data: {
        tuser:tosend,
        phone:"T"
      },
      success:function(data) {
 console.log("Working! blanck");
 $("#btn-1").text("Request sent");
 $("#btn-1").prop("disabled",true);
      },
 error: function(data) {
 console.log("Error");
 $("#btn-1").text("Error occured");
 }
   });
}

function populate_free()
{
  console.log("populating free");
   $.ajax({
      url:"/search",  
      type: "get",
      success:function(data) {
 console.log("Working! blanckooo");
 console.log(data);
 var myarr = data.split(",");
 
 for(x=0; x<myarr.length;x++){
  console.log("h "+myarr[x]);
  var str="#list-"+(x+1);
  var btn="btn-"+(x+1);
  tosend=myarr[x];
  if(tosend!=""){
  console.log(str);
  $(str).text(myarr[x]);
 $(str).append("<br><div class=\"button-set\"><button class=\"active\" onClick=\"sendRequest()\"  id="+btn+">Send Request</button></div>");
    }
 }

      },
 error: function(data) {
 console.log("Error");
 }
   });
}

function update(){  
console.log("starting a separte ajax");
 
 var email= $('#memail').val();
  var phone = $('#mphone').val();
 var msg = $('#mmsg').val();
 console.log("four values");
//console.log(uname,email,phone,msg);
 
 $.ajax({
      url:"/doreg",  
      type: "get",
        data: {
          
		  email: email,
		  phone: phone,
		  msg: msg
        },
      success:function(data) {
 console.log("Workingggg!");
 window.open("/gdl_home","_self");
      },
 error: function(data) {
 console.log("Error");
 }
   });
   
}

function grantRequest2(x){  
console.log("starting a separate ajax");
var ap = "F";
var rj = "F";
var bl = "F";
console.log("x value",x);
if(x==1)  ap="T";
if(x==2)  rj="T";
if(x==3) bl="T";
 $.ajax({
      url:"/re_handler",  
      type: "get",
        data: {
      accept_p: ap,
      reject_p:rj,
      block:bl,
          fuser: "u1",
      tuser: "u11"
        },
      success:function(data) {
 console.log("Working!");
 if(x==1)
 {
   $("#gabtn-2").text("Accepted");
 $("#gabtn-2").prop("disabled",true);
 $("#grbtn-2").hide();
 $("#gbbtn-2").hide();
 }
 if(x==2)
 {
   $("#gabtn-2").hide();
 $("#gbbtn-2").hide();
   $("#grbtn-2").text("Rejected");
 $("#grbtn-2").prop("disabled",true);
 }
 if(x==3)
 {
   $("#grbtn-2").hide();
 $("#gabtn-2").hide();
   $("#gbbtn-2").text("Blocked");
 $("#gbbtn-2").prop("disabled",true);
 }
 },
 error: function(data) {
 console.log("Error");
 $("#btn-2").text("Error occured");
 }
   });
}
function grantRequest(x){  
console.log("starting a separate ajax");
var ap = "F";
var rj = "F";
var bl = "F";

if(x==1)  ap="T";
if(x==2)  rj="T";
if(x==3) bl="T";
 $.ajax({
      url:"/re_handler",  
      type: "get",
        data: {
			accept_p: ap,
			reject_p:rj,
			block:bl,
          fuser: "u1",
		  tuser: "u11"
        },
      success:function(data) {
 console.log("Working!");
 if(x==1)
 {
	 $("#gabtn-1").text("Accepted");
 $("#gabtn-1").prop("disabled",true);
 $("#grbtn-1").hide();
 $("#gbbtn-1").hide();
 }
 if(x==2)
 {
	 $("#gabtn-1").hide();
 $("#gbbtn-1").hide();
	 $("#grbtn-1").text("Rejected");
 $("#grbtn-1").prop("disabled",true);
 }
 if(x==3)
 {
	 $("#grbtn-1").hide();
 $("#gabtn-1").hide();
	 $("#gbbtn-1").text("Blocked");
 $("#gbbtn-1").prop("disabled",true);
 }
 },
 error: function(data) {
 console.log("Error");
 $("#btn-1").text("Error occured");
 }
   });
}
function send_reg_ajax(){		
console.log("starting an serparte ajax");
	var username1 = $('#email').val(); // get username
    var password1 = $('#password').val(); // get password
var repassword1 = $('#re_password').val(); // get password
console.log(username1,password1,repassword1);
 $.ajax({
      url:"/register",  
	type: "post",
        data: {
          username: username1,
	password: password1,
	re_password: repassword1
        },
      success:function(data) {
	console.log("hey this is working");
	$("#reg_button").text("SuccessFully Registered");
      },
	error: function(data) {
	console.log("error");
	}
   });
}

function sendhomemap(x,y){
	console.log("function map",x,y);
	$.ajax({
      url:"/synch",  
	type: "get",
	data:{
		hla:x,
		hlo:y
	},
      success:function(data) {
	console.log("success map home");
	window.open("/gdl_office","_self");
      },
	error: function(data) {
	console.log("error");
	}
   });

}

function sendofficemap(x,y){
	console.log("function  officemap",x,y);
	$.ajax({
      url:"/synco",  
	type: "get",
	data:{
		ola:x,
		olo:y
	},
      success:function(data) {
	console.log("success map office");
	window.open("/re_form","_self");
      },
	error: function(data) {
	console.log("error");
	}
   });

}

function logout(){
console.log("logging out");
	$.ajax({
      url:"/logout",  
	type: "post",
      success:function(data) {
	console.log("hey this is working logout");
      },
	error: function(data) {
	console.log("error");
	}
   });
}

function login_function(){		
console.log("starting login ajax");
	var usernamee = $('#login_email').val(); // get username
    var passworde = $('#login_password').val(); // get password
console.log(usernamee,passworde);
 $.ajax({
      url:"/do_login",  
	type: "post",
        data: {
          username: usernamee,
	password: passworde
        },
      success:function(data) {
	console.log("success ajax login");
	if(data == "false_user"){
		$('#login_button').text("Not registered?");
	}
	else
	{
		window.open("/register_form","_self");
	}
	console.log(data);
      },
	error: function(data) {
	console.log("error");
	}
   });

}
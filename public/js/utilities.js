var get = function(url, callback) {
	var request = new XMLHttpRequest();	

	request.open("GET", url, true);

	request.onreadystatechange = function(){
		if(request.readyState === XMLHttpRequest.DONE && request.status == 200){
			//all is well
			var obj = JSON.parse(request.responseText)
			callback(obj);
		} else {
			//shit's gone down
		}
	}

	request.send();
}
var post = function(url, data, callback) {
	var request = new XMLHttpRequest();	

	request.open("POST", url, true);

	request.onreadystatechange = function(){
		if(request.readyState === XMLHttpRequest.DONE && request.status == 200){
			//all is well
			var obj = JSON.parse(request.responseText)
			callback(obj);
		} else {
			//shit's gone down
		}
	}

	request.send(data);
}

var getQueryString = function() {
	var qs = {};
	var query = window.location.search.substring(1);
	var vars = query.split('&');
	
	for (var i = 0; i < vars.length; i++) {
		var pair = vars[i].split('=');
		if(pair.length>1){
			qs[pair[0]] = pair[1].replace("/","");

		}	
	}	
	return qs;
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return false;
}
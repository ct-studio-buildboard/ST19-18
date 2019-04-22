// var i = 0;

function update_speed() {
  // i = i + 1;
  postMessage(get_speed());
  setTimeout("update_speed()",500);
}

function get_speed() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      return this.responseText;
    }
  };
  xhttp.open("GET", "http://10.148.131.75:8000/get_speed/", true);
  xhttp.send();
}

update_speed();
function submitGif(){
    var results = document.getElementsByClassName("results");
    results[0].style.display = 'none';
    results[1].style.display = 'none';
    var d = document.getElementById("content");
    d.className += " shake";
    var XHR = new XMLHttpRequest();
    var urlEncodedData = "";
    var form = new FormData(document.querySelector('#upload'));

    urlEncodedData = ('url=' + encodeURIComponent(form.get('url'))).replace(/%20/g, '+');

    // Define what happens on successful data submission
    XHR.addEventListener('load', function(event) {
        var data = JSON.parse(this.response);
        document.getElementById("guid").value = data.guid;
        results[0].style.display = 'inline';
        results[1].style.display = 'block';
        document.getElementById("savings").innerHTML = data.savings;
        d.classList.remove("shake");
    });

    // Define what happens in case of error
    XHR.addEventListener('error', function(event) {
        alert('Oops! Something goes wrong.');
    });

    // Set up our request
    XHR.open('POST', '/compress');

    // Add the required HTTP header for form data POST requests
    XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    // Finally, send our data.
    XHR.send(urlEncodedData);
}

function getGif(){
    var XHR = new XMLHttpRequest();
    var urlEncodedData = "";
    var form = new FormData(document.querySelector('#id_form'));

    urlEncodedData = ('guid=' + encodeURIComponent(form.get('guid'))).replace(/%20/g, '+');

    // Define what happens on successful data submission
    XHR.addEventListener('load', function(event) {
        var urlCreator = window.URL || window.webkitURL;
        var imageUrl = urlCreator.createObjectURL(this.response);
        document.querySelector("#image").src = imageUrl;
    });

    // Define what happens in case of error
    XHR.addEventListener('error', function(event) {
        alert('Oops! Something goes wrong.');
    });

    XHR.responseType = "blob";
    // Set up our request
    XHR.open('POST', '/get_gif');

    // Add the required HTTP header for form data POST requests
    XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    // Finally, send our data.
    XHR.send(urlEncodedData);
}

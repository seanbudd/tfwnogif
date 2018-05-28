function submitGif(){
    var XHR = new XMLHttpRequest();
    var urlEncodedData = "";
    var form = new FormData(document.querySelector('#upload'));

    urlEncodedData = ('url=' + encodeURIComponent(form.get('url'))).replace(/%20/g, '+');

    // Define what happens on successful data submission
    XHR.addEventListener('load', function(event) {
        var data = JSON.parse(this.response)
        document.getElementById("guid").value = this.guid;
        document.getElementById("guid").value = this.guid;
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
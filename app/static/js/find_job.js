document.addEventListener('DOMContentLoaded', function(){ // Аналог $(document).ready(function(){
    document.getElementById('elem').addEventListener('click', function(event) {
        event.preventDefault()
        var radios = document.getElementsByName('specialization');
        var specialization = ""

        var skills_str = document.getElementById('skills_str').value

        radios.forEach(e => {
            if (e.checked) {
                specialization = e.value;
            }})

        /*var block_to_insert ;
        var container_block ;

        block_to_insert = document.createElement( 'div' ) ;
        block_to_insert.innerHTML = 'This demo DIV block was inserted into the page using JavaScript.' ;

        container_block = document.getElementById( 'democontainer' );
        container_block.appendChild( block_to_insert );*/

        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
               // Typical action to be performed when the document is ready:
               document.getElementById("democontainer").innerHTML = xhr.responseText;
            }
        };
        xhr.open("GET", "results?specialization=" + specialization + "&skills_str=" + skills_str, true);
        //xhr.open("GET", "hello?text=" + specialization, true);
        //xhr.responseType = "JSON";
        //xhr.onload = function(e) {
        //  var arrOfStrings = JSON.parse(xhr.response);
        //  console.log(arrOfStrings)
        //}
        xhr.send();
        // todo: go on input extraction
        // todo: implement ajax request to flask view
        // todo: render response from flask
    });
});


document.addEventListener('DOMContentLoaded', function(){
    document.getElementById('elem').addEventListener('click', function(event) {
        event.preventDefault()
        var radios = document.getElementsByName('specialization');
        var specialization = ""

        var skills_str = document.getElementById('skills_str').value

        radios.forEach(e => {
            if (e.checked) {
                specialization = e.value;
            }})

        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
               document.getElementById("democontainer").innerHTML = xhr.responseText;
            }
        };
        xhr.open("GET", "results?specialization=" + encodeURIComponent(specialization) + "&skills_str=" + skills_str, true);
        xhr.send();

    });
});


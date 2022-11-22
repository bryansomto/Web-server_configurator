document.getElementById('id_file').addEventListener('change', function(event) {
    event.preventDefault();

    let fr = new FileReader();
    fr.onload = function() {
        document.getElementById('output').textContent = fr.result;
    }

    fr.readAsText(this.files[0])
});
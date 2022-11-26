document.querySelector('input[type="file"]').addEventListener('change', function (event) {
    return (this.files[0].name);
});
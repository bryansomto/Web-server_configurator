document.getElementById('id_file').addEventListener('change', function(event) {
    event.preventDefault();

    let fr = new FileReader();
    fr.onload = function() {
        document.getElementById('output').textContent = fr.result;
    }

    fr.readAsText(this.files[0])
});

// function onFileLoad(elementId, event) {
//     document.getElementById('id_file').innerText = event.target.result;
// }

// function onChooseFile(event, onLoadFileHandler) {
//     if (typeof window.FileReader !== 'function')
//         throw ("The file API isn't supported on this browser.");
//     let input = event.target;
//     if (!input)
//         throw ("The browser does not properly implement the event object");
//     if (!input.files)
//         throw ("This browser does not support the `files` property of the file input");
//     if (!input.files[0])
//         return undefined;
//     let file = input.files[0]
//     let fr = new FileReader();
//     fr.onload = onLoadFileHandler;
//     console.log(fr.readAsText(file));
// }
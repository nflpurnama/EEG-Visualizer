$(document).ready(function(){
    $('#view-eeg').on('click', function(){
        var fileInput = document.getElementById('file');
        var file = fileInput.files[0];
        if (file) {
            let formData = new FormData()
            formData.append('file', file)
            
            fetch('/view', {
                method: 'POST',
                body: formData
            })
            .then(response => response.blob())
            .then(data => {
                const imageUrl = URL.createObjectURL(data);
                const imgElement = document.createElement('img');
                imgElement.src = imageUrl;
                document.getElementById('eeg-container').appendChild(imgElement);
            })
            .catch(error => {
                console.error('Error:', error);
            });

            document.getElementById('file-response').innerText = 'file selected.';
        } else {
            document.getElementById('file-response').innerText = 'No file selected.';
        }
    });

    $('#view-eeg').on('mousedown', function(){
        $("#view-eeg").addClass("pressed-color")
    });

    $('#view-eeg').on('mouseup', function(){
        $("#view-eeg").removeClass("pressed-color")
    });
});
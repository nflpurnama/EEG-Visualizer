$(document).ready(function(){
    $('#view-eeg').on('click', function(){
        var fileInput = document.getElementById('file');
        var file = fileInput.files[0];
        if (file) {
            $('#eeg-container').empty();
            document.getElementById('file-response').innerText = 'file selected.';
            
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

        } else {
            document.getElementById('file-response').innerText = 'No file selected.';
        }
    });

    $('#go-to').on('click', function(){
        let fileInput = document.getElementById('file');
        let file = fileInput.files[0];
        if (file === undefined){
            document.getElementById('file-response').innerText = 'No file selected.';
        }

        else{
            $('#eeg-container').empty();
            document.getElementById('file-response').innerText = 'file selected.';
            
            let timestampInput = document.getElementById('timestamp');
            let timestampValue = timestampInput.value;
            
            let formData = new FormData()
            formData.append('file', file)
            formData.append('timestamp', timestampValue)

            fetch('/navigate', {
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
        }
    });

    $('#view-eeg').on('mousedown', function(){
        $("#view-eeg").addClass("pressed-color")
    });

    $('#view-eeg').on('mouseup', function(){
        $("#view-eeg").removeClass("pressed-color")
    });
});
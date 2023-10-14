$(document).ready(function(){
    $('#view-eeg').on('click', function(){
        $('#view-eeg').prop('disabled', true);
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
                $('#view-eeg').prop('disabled', false);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        } else {
            document.getElementById('file-response').innerText = 'No file selected.';
            $('#view-eeg').prop('disabled', false);
        }
    });

    $('#go-to').on('click', function(){
        $('#go-to').prop('disabled', true);
        let fileInput = document.getElementById('file');
        let file = fileInput.files[0];
        if (file === undefined){
            document.getElementById('file-response').innerText = 'No file selected.';
            $('#go-to').prop('disabled', false);
        }

        else{
            $('#eeg-container').empty();
            document.getElementById('file-response').innerText = 'file selected.';
            
            let timestampInput = document.getElementById('timestamp');
            let timestampValue = timestampInput.value;
            const [hours, minutes, seconds] = timestampValue.split(':').map(Number);
            let timestampInSeconds = hours * 3600 + minutes * 60 + seconds;
            
            console.log(timestampValue)
            console.log(timestampInSeconds)

            let formData = new FormData()
            formData.append('file', file)
            formData.append('timestamp', timestampInSeconds)

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
                $('#go-to').prop('disabled', false);
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

    $('a').on('click', function(event){
        event.preventDefault();
    })
});
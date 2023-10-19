$(document).ready(function(){
    const navs = ['#predict-tab-nav', '#upload-tab-nav', '#view-tab-nav', '#dataframe-tab-nav']

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

    $('#file').on('change', function(event){
        const uploadedFile = event.target.files[0];
        if (uploadedFile) {
            $('#view-tab-nav').removeClass('disabled')
            $('#predict-tab-nav').removeClass('disabled')

            $('#eeg-container').empty();
            
            let formData = new FormData()
            formData.append('file', uploadedFile)
        
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
            .then($('#view-tab-nav').click())
            .catch(error => {
                console.error('Error:', error);
            });
        }
    })

    $('#upload-tab-nav').on('click', navigateTab)

    $('#view-tab-nav').on('click', navigateTab)

    $('#dataframe-tab-nav').on('click', function(){
        let fileInput = document.getElementById('file');
        let file = fileInput.files[0];
        
        if (file !== undefined){
            navigateTab()

            let formData = new FormData()
            formData.append('file', file)

            fetch('/getdf', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => {
                console.error('Error:', error);
            });
        }
    })

    function navigateTab() {
        const navId = '#' + $(this).attr('id')
        const tabId = navId.replace('-nav', '')

        navs.filter(nav => nav != navId)
        .map(nav => {
            $(nav).removeClass('disabled')
            $(nav).removeClass('active')
        })
        
        const tabs = ['#predict-tab', '#upload-tab', '#view-tab']
        tabs.filter(tab => tab != tabId)
        .map(tab => {
            $(tab).addClass('d-none')
        })

        $(navId).addClass('disabled')
        $(navId).addClass('active')
        $(tabId).removeClass('d-none')
    }
});
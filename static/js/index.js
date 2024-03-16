$(document).ready(function(){
    const navs = ['#predict-tab-nav', '#upload-tab-nav', '#view-tab-nav', '#dataframe-tab-nav']
    const tabs = ['#predict-tab', '#upload-tab', '#view-tab', '#dataframe-tab']
    let EEG_DATA = {}

    $('#go-to').on('click', function(){
        $('#go-to').prop('disabled', true);
        $('#eeg-container').empty();
        
        let timestampInput = document.getElementById('timestamp');
        let timestampValue = timestampInput.value;
        const [hours, minutes, seconds] = timestampValue.split(':').map(Number);
        let timestampInSeconds = hours * 3600 + minutes * 60 + seconds;
        
        let formData = new FormData()
        formData.append('timestamp', timestampInSeconds)
        console.log(timestampInSeconds)
        
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
    });

    $('#file').on('change', function(event){
        const uploadedFile = event.target.files[0];
        if (uploadedFile) {
            $("#upload").prop('disabled', false)
        }else{
            $("#upload").prop('disabled', true)
        }
    })
    
    $('#upload').on('click', function(){
        $('#upload').prop('disabled', true);
        navs.filter(nav => nav != '#upload-tab-nav')
        .map(nav => {
            $(nav).addClass('disabled')
        })
        $("#upload-response").html('')
        $('#eeg-container').html('');

        let fileInput = document.getElementById('file');
        let file = fileInput.files[0];

        let formData = new FormData()
        formData.append('file', file)

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            $("#upload-response").html(data)
            navs.filter(nav => nav != '#upload-tab-nav')
            .map(nav => {
                $(nav).removeClass('disabled')
            })
            $('#upload').prop('disabled', false);
            $('#get-df').prop('disabled', false)
        })
        .catch(error => {
            console.error('Error:', error);
        });

    });

    $('#upload-tab-nav').on('click', function(event){navigateTab($(this))})
    
    $('#view-tab-nav').on('click', function(event){navigateTab($('#view-tab-nav'))})

    $('#dataframe-tab-nav').on('click', function(event){
        let fileInput = document.getElementById('file');
        let file = fileInput.files[0];
        
        if (file !== undefined){
            navigateTab($(this))
        }
    })

    $('#get-df').click(() => {
        fetch('/view', {
            method: 'GET',
        })
        .then(response => response.json())
        .then(data => {
            if(data != undefined){
                EEG_DATA = data
                console.log(EEG_DATA)
                plotEEGData(EEG_DATA)
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    })

// Function to plot EEG data for each channel
function plotEEGData(eegData) {
    Object.keys(eegData).forEach(channel => {
        const ctx = document.createElement('canvas').getContext('2d');
        ctx.canvas.width = 400;
        ctx.canvas.height = 200;
        document.body.appendChild(ctx.canvas);

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: [...Array(eegData[channel].length).keys()],
                datasets: [{
                    label: channel,
                    data: eegData[channel],
                    borderColor: 'blue',
                    fill: false
                }]
            },
            options: {
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'EEG Value'
                        }
                    }
                }
            }
        });
    });
}
    

    function navigateTab(element) {
        console.log(element)
        const navId = "#" + element.attr('id')
        const tabId = navId.replace('-nav', '')

        navs.filter(nav => nav != navId)
        .map(nav => {
            $(nav).removeClass('disabled')
            $(nav).removeClass('active')
        })
        
        tabs.filter(tab => tab != tabId)
        .map(tab => {
            $(tab).addClass('d-none')
        })

        $(navId).addClass('disabled')
        $(navId).addClass('active')
        $(tabId).removeClass('d-none')
    }
});
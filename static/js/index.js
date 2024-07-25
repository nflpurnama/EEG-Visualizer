$(document).ready(function(){
    const navs = ['#predict-tab-nav', '#upload-tab-nav', '#view-tab-nav', '#dataframe-tab-nav']
    const tabs = ['#predict-tab', '#upload-tab', '#view-tab', '#dataframe-tab']
    const slider = document.getElementById('image-slider')
    const eegImage = document.getElementById('eeg-image')
    const psdImage = document.getElementById('psd-image')
    const uploadResponsePlaceholder = document.getElementById('upload-response')  
    var arrImageEEG = []

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
        $("#predict-response").html('')
        $('#predict-response').removeClass('bg-success-subtle text-success')
        $('#predict-response').removeClass('bg-danger-subtle text-danger')
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
        .then(message => {
            navs.filter(nav => nav != '#upload-tab-nav')
            .map(nav => {
                $(nav).removeClass('disabled')
            });
            $('#upload').prop('disabled', false);
            $('#predict').prop('disabled', false);
            $('#get-df').prop('disabled', false);
            const wrapper = document.createElement('div')
            wrapper.innerHTML = [
                `<div class="alert alert-success alert-dismissible" role="alert">`,
                `   <div>${message}</div>`,
                '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
                '</div>'
            ].join('')

            uploadResponsePlaceholder.append(wrapper)
        })
        .catch(error => {
            console.error('Error:', error);
        });

    });

    $('#predict').on('click', function(){
        $('#predict').prop('disabled', true);
        $('#predict-btn-label').addClass('d-none')
        $('#predict-btn-load').removeClass('d-none')
        navs.filter(nav => nav != '#upload-tab-nav')
        .map(nav => {
            $(nav).addClass('disabled')
        })
        $("#predict-response").html('')
        $('#eeg-container').html('');

        fetch('/predict', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            if(data.prediction === 'Non-Epileptic'){
                $('#predict-response').addClass('bg-success-subtle text-success')
            }
            else{
                $('#predict-response').addClass('bg-danger-subtle text-danger')                
            }
                
            $("#predict-response").html(data.prediction);
            $('#predict-btn-label').removeClass('d-none')
            $('#predict-btn-load').addClass('d-none')
            $('#predict').prop('disabled', false);
            $('#get-df').prop('disabled', false);
            
            navs.filter(nav => nav != '#upload-tab-nav')
            .map(nav => {
                $(nav).removeClass('disabled')
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    $('#upload-tab-nav').on('click', async function(event){ await navigateTab($(this))})
    
    $('#image-slider').on('input', function(){
        eegImage.src = 'data:image/png;base64,' + arrImageEEG[this.value];
    })

    $('#view-tab-nav').on('click', async function(event){
        navigateTab($('#view-tab-nav'))
        $('#view-content').addClass('d-none')
        $('#view-load').removeClass('d-none')
        fetch('/view', {
            method: 'GET',
        })
        .then(response => response.json())
        .then(data => {
            arrImageEEG = data.eeg
            imagePSD = data.psd
            console.log(arrImageEEG)
            $('#view-load').addClass('d-none')
            $('#view-content').removeClass('d-none')
            slider.max = arrImageEEG.length - 1
            eegImage.src = 'data:image/png;base64,' + arrImageEEG[slider.value];
            psdImage.src = 'data:image/png;base64,' + imagePSD
        })
        .catch(error => {
            console.error('Error:', error);
        });
    })

    $('#dataframe-tab-nav').on('click', async function(event){
        let fileInput = document.getElementById('file');
        let file = fileInput.files[0];
        if (file !== undefined){
            await navigateTab($(this))
        }
    })
    
    function navigateTab(element) {
        return new Promise((resolve) => {
            // console.log(element)
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
        })
    }
});
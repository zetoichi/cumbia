Dropzone.options.imgDropzone = {
    method: 'post',
    paramName: 'pic',
    autoProcessQueue: false,
    uploadMultiple: true,
    dictDefaultMessage: 'Arrastre aquí las imágenes...',
    acceptedFiles: '.jpg,.png',
    addRemoveLinks: true,
    maxFiles: 12,
    parallelUploads: 12,
    init: function() {
        const uploadBtn = document.querySelector('#upload-imgs-btn')

        uploadBtn.addEventListener('click', e => {
            e.stopPropagation()
            e.preventDefault()
            this.processQueue()
        })

        this.on('successmultiple', (files, response) => {
            window.location.reload()
        })
        this.on('errormultiple', (files, response) => {
            console.log(response)
        })
    }
}
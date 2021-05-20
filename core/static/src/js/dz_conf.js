const pk = location.pathname.split('/').reverse()[0]

Dropzone.options.imgDropzone = {
    method: 'post',
    autoProcessQueue: false,
    uploadMultiple: true,
    dictDefaultMessage: 'Arrastre aquí las imágenes...',
}
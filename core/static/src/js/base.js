import { toggleImages } from './handleImages';

if (document.readyState == 'loading') {document.addEventListener(
    'DOMContentLoaded', ready)
} else {
    ready()
}

function ready() {
    // const phLinks = document.querySelectorAll('.ph-link')
    // const big = document.querySelector('.big')
    // const fullScreenLogo = document.querySelector('#full-screen-logo')
    // const fullScreenIso = document.querySelector('#full-screen-iso')
    
    // setTimeout(() => {
    //     fullScreenIso.style.display = 'none'
    //     fullScreenLogo.style.display = 'inline'
    // }, 3000);
    // setTimeout(() => {
    //     big.style.opacity = 0
    // }, 4500);
    // setTimeout(() => {
    //     big.remove()
    // }, 5100);
    // phLinks.forEach(link => {
    //     link.addEventListener('mouseenter', (e) => {
    //         toggleImages(e)
    //     })
    // })
    // phLinks.forEach(link => {
    //     link.addEventListener('mouseleave', (e) => {
    //         toggleImages(e)
    //     })
    // })
    // const dz = new Dropzone('#img-dropzone', {url: '/'})
}

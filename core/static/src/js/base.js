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
}

function toggleImages(e) {
    const phId = 'ph-' + e.target.value
    const phElement = document.querySelector(`#${phId}`)
    const phInfoId = 'ph-info-' + e.target.value
    const phInfoElement = document.querySelector(`#${phInfoId}`)
    const brandCenterHeader = document.querySelector('#brand-center-header')
    brandCenterHeader.classList.toggle('faded-out')
    phElement.classList.toggle('faded-out')
    phInfoElement.classList.toggle('faded-out')
}
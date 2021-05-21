import Splide from '@splidejs/splide';

document.addEventListener('DOMContentLoaded', () => {
    new Splide('.splide', {
        type: 'fade',
        perPage: 1,
        width: '60vw',
        height: '85vh',
        speed: 800,
        lazyLoad: 'nearby',
    }).mount();
} )
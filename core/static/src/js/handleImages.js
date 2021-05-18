export function toggleImages(e) {
    const phId = 'ph-' + e.target.value
    const phElement = document.querySelector(`#${phId}`)
    const phInfoId = 'ph-info-' + e.target.value
    const phInfoElement = document.querySelector(`#${phInfoId}`)
    const brandCenterHeader = document.querySelector('#brand-center-header')
    brandCenterHeader.classList.toggle('faded-out')
    phElement.classList.toggle('faded-out')
    phInfoElement.classList.toggle('faded-out')
}


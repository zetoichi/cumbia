import { handleMainToggle, handlePicActions } from './handlePics';

if (document.readyState == 'loading') {document.addEventListener(
    'DOMContentLoaded', ready)
} else {
    ready()
}



function ready() {
    handleEditMode()
    handleMainToggle()
    handlePicActions()
    handleCheckboxes()
}

function handleEditMode() {
    const editMode = document.querySelector('#edit-mode')
    if (editMode) {
        document.querySelectorAll('.edit-element').forEach(
            element => {
                element.classList.add('enabled')
            }
        )
    } else if (!editMode) {
        animateOpening()
    }
}

function handleCheckboxes() {
    const switches = document.querySelectorAll('.tgl-btn')
    switches?.forEach(sw => {
        sw.addEventListener('click', e => {
            const checkbox = e.target.previousElementSibling
            toggleCheckbox(checkbox)
        })
    })
}

function toggleCheckbox(checkbox) {
    if (checkbox.checked) {
        checkbox.checked = false
    } else if (!checkbox.checked) {
        checkbox.checked = true
    }
}

function animateOpening() {
    const big = document.querySelector('.big')
    const fullScreenLogo = document.querySelector('#full-screen-logo')
    
    if (big && fullScreenLogo) {
        setTimeout(() => {
            fullScreenLogo.style.display = 'none'
        }, 1500);
        setTimeout(() => {
            fullScreenLogo.style.display = 'inline'
        }, 1600);
        setTimeout(() => {
            fullScreenLogo.style.display = 'none'
        }, 2000);
        setTimeout(() => {
            fullScreenLogo.style.display = 'inline'
        }, 2100);
        setTimeout(() => {
            fullScreenLogo.style.display = 'none'
        }, 3000);
        setTimeout(() => {
            big.style.opacity = 0
        }, 3800);
        setTimeout(() => {
            big.remove()
        }, 5100);
    }
}
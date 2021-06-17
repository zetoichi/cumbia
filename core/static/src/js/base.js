import { handleMainPicToggle, handlePicActions } from './handlePics';
import { handleSwitches } from './switches';
import { handleEditMode } from './editMode';
import { handleBurger } from './burger';

if (document.readyState == 'loading') {document.addEventListener(
    'DOMContentLoaded', ready)
} else {
    ready()
}

function ready() {
    handleEditMode()
    handleMainPicToggle()
    handlePicActions()
    handleSwitches()
    handleBurger()
}
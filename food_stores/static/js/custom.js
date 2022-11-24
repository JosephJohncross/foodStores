const menuSelect = document.getElementById('menu-select')
const selectionBtn = document.querySelectorAll('.selection-btn')

menuSelect.addEventListener('click', toggleSelectionMenu)

function toggleSelectionMenu(e){
    if (e.target.classList.contains('selection-btn')) {
        selectionBtn.forEach(selectBtn => {
            selectBtn.dataset.pressed = "false"
        })
        e.target.dataset.pressed = "true"
    }
}
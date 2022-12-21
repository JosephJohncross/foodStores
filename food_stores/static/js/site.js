const axios = require('axios');
const menuSelect = document.getElementById('menu-select')
const selectionBtn = document.querySelectorAll('.selection-btn')
const closeOrder = document.getElementById('close-order');
const sideDrawer = document.getElementById('sideDrawer');
const orders = document.getElementById('orders')

menuSelect.addEventListener('click', toggleSelectionMenu)
closeOrder.addEventListener('click', slideDrawer)
orders.addEventListener('click', slideDrawer)

function toggleSelectionMenu(e){
    if (e.target.classList.contains('selection-btn')) {
        selectionBtn.forEach(selectBtn => {
            selectBtn.dataset.pressed = "false"
        })
        e.target.dataset.pressed = "true"
    }
}

function slideDrawer(){
    if (sideDrawer.classList.contains('translate-x-full')){
        sideDrawer.classList.remove('translate-x-full')
        sideDrawer.classList.add('translate-x-0')
    }
    else{
        sideDrawer.classList.remove('translate-x-0')
        sideDrawer.classList.add('translate-x-full')
    }
}

let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),{
            types: ['geocode', 'establishment'],
            componentRestrictions: {'country': ['in', 'us']}
        }
    )
    //Product to specify what should happen when the product is clicked
    autocomplete.addEventListener('place_changed', onPlaceChanged)
}

function onPlaceChanged(){
    var place = autocomplete.getPlace();

    //user did not select the prediction, reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "start typing..."
    }else{
        console.log('place name => ', place.name)
    }
    //get the address omponent and assign them to the fields
}
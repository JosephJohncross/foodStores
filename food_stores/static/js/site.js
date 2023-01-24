const menuSelect = document.getElementById('menu-select') || null
const selectionBtn = document.querySelectorAll('.selection-btn') || null
const closeOrder = document.getElementById('close-order') || null;
const sideDrawer = document.getElementById('sideDrawer') || null;
const orders = document.getElementById('orders')
const cartCount = document.getElementById('cart_count') || null
const homeSearch = document.getElementById('home-search') || null
const searchDropDown = document.getElementById('search-dropdown') || null
const longitudeField = document.getElementById('long') || null
const latitudeField = document.getElementById('lat') || null
const vendorCity = document.getElementById('lat') || null
const vendorCountry = document.getElementById('lat') || null
// const searchForm = document.getElementById('search-form') || null


homeSearch != null ? homeSearch.addEventListener('keyup', (e)=>{autoComplete(e)}) : ""
menuSelect !== null ? menuSelect.addEventListener('click', toggleSelectionMenu) : ""
closeOrder != null ? closeOrder.addEventListener('click', slideDrawer) : ""
orders != null ? orders.addEventListener('click', slideDrawer) : ""

document.onreadystatechange = () => {
    if ( document.readyState === 'complete'){
        document.onclick = (e)=>{
            if (e.target.classList.contains('add_cart')){
                e.preventDefault()
                addToCart(e.target)
            }
            else if (e.target.classList.contains('cart-increase')){
                e.preventDefault()
                incrementCartItem(e.target)
            }
            else if (e.target.classList.contains('cart-decrease')){
                e.preventDefault()
                decrementCartItem(e.target)
            }
            else if (e.target.classList.contains('delete-item')){
                e.preventDefault()
                decrementCartItem(e.target)
            }
            else if (e.target.closest('.address-item') !== null || e.target.classList.contains('address-item')){
                e.preventDefault()
                homeSearch.value = e.target.children[1]?.innerHTML || e.target.innerHTML
                longitudeField.value = e.target.children[2]?.value || e.target.nextElementSibling?.value 
                latitudeField.value = e.target.lastElementChild?.value || e.target.nextElementSibling?.nextElementSibling?.value
                searchDropDown.classList.add('hidden')
                searchDropDown.classList.remove('flex')
            }
        }
    }
}
function autoComplete(e){
    searchDropDown.innerHTML =''
    if (e.target.value.length < 3 || e.target.value == "") {
        searchDropDown.classList.add('hidden')
        searchDropDown.classList.remove('flex')
        return
    }
    else{
        searchDropDown.classList.add('flex')
        searchDropDown.classList.remove('hidden')
        const options = {
            method: 'GET',
            headers: {
                'X-RapidAPI-Key': '93464f8037msh725108e7458de10p12cd2cjsn038b91e1081a',
                'X-RapidAPI-Host': 'spott.p.rapidapi.com'
            }
        }
    
        fetch(`https://spott.p.rapidapi.com/places?type=CITY&limit=10&q=${encodeURI(e.target.value)}}`, options)
        .then(response => response.json())
        .then(response => {
            console.log(response)
            response.forEach(address => {
                var places = document.createElement('div')
                places.classList.add('place-flex', 'address-item')
                places.innerHTML = `
                <div class="">
                    <img src="https://img.icons8.com/color/96/null/google-maps.png" class="place-image"/>
                </div>
                <div class="place-text">${address.name}, ${address.country.name}</div>
                <input type="hidden" id="long-data" value="${address.coordinates.longitude}"/>
                <input type="hidden" id="lat-data" value="${address.coordinates.latitude}"/>
            `
                searchDropDown.append(places)
            })
        })
        .catch(err => console.error(err));
    }

    
}

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

// let autocomplete;

// function initAutoComplete() {
//     autocomplete = new google.maps.places.Autocomplete(
//         document.getElementById('id_address'),{
//             types: ['geocode', 'establishment'],
//             componentRestrictions: {'country': ['in', 'us']}
//         }
//     )
//     //Product to specify what should happen when the product is clicked
//     autocomplete.addEventListener('place_changed', onPlaceChanged)
// }

// function onPlaceChanged(){
//     var place = autocomplete.getPlace();

//     //user did not select the prediction, reset the input field or alert()
//     if (!place.geometry){
//         document.getElementById('id_address').placeholder = "start typing..."
//     }else{
//         console.log('place name => ', place.name)
//     }
//     //get the address omponent and assign them to the fields
// }

// Requests

async function addToCart(target){
    url = target.dataset.url

    var response = await fetch(url, {
        headers: {
            'X-Request-With': 'XMLHttpRequest'
        }
    })
    result = await response.json()
    console.log(result)
    if (result.status == "Success"){
        cartCount.textContent = result.cartcounter["cart_count"]
    }

    toastNotification(result)
    console.log(result)

    const nextURL = url
    const nextTitle = 'customerDashboard';
    const nextState = { additionalInformation: 'Updated the URL with JS' }; 

    // This will create a new entry in the browser's history, without reloading
    window.history.pushState(nextState, nextTitle, nextURL);

    // This will replace the current entry in the browser's history, without reloading
    window.history.replaceState(nextState, nextTitle, nextURL);
}

async function decrementCartItem(target){
    url = target.dataset.url
    id = target.dataset.url

    var response = await fetch(url, {
        headers: {
            'X-Request-With': 'XMLHttpRequest'
        }
    })
    result = await response.json()
    toastNotification(result)

    const nextURL = `${location.protocol}//${location.host}/customerDashboard/`;
    const nextTitle = 'customerDashboard';
    const nextState = { additionalInformation: 'Updated the URL with JS' };

    // This will create a new entry in the browser's history, without reloading
    window.history.pushState(nextState, nextTitle, nextURL);

    // This will replace the current entry in the browser's history, without reloading
    window.history.replaceState(nextState, nextTitle, nextURL);
    history.go()
}

async function incrementCartItem(target){
    url = target.dataset.url
    id = target.dataset.url

    var response = await fetch(url, {
        headers: {
            'X-Request-With': 'XMLHttpRequest'
        }
    })
    result = await response.json()
    toastNotification(result)

    const nextURL = `${location.protocol}//${location.host}/customerDashboard/`;
    const nextTitle = 'customerDashboard';
    const nextState = { additionalInformation: 'Updated the URL with JS' };

    // This will create a new entry in the browser's history, without reloading
    window.history.pushState(nextState, nextTitle, nextURL);

    // This will replace the current entry in the browser's history, without reloading
    window.history.replaceState(nextState, nextTitle, nextURL);
    history.go()
}

async function deleteCartItem(){
    url = target.dataset.url
    id = target.dataset.url

    var response = await fetch(url, {
        headers: {
            'X-Request-With': 'XMLHttpRequest'
        }
    })
    result = await response.json()
    toastNotification(result)

    const nextURL = url;
    const nextTitle = 'customerDashboard';
    const nextState = { additionalInformation: 'Updated the URL with JS' };

    // This will create a new entry in the browser's history, without reloading
    window.history.pushState(nextState, nextTitle, nextURL);

    // This will replace the current entry in the browser's history, without reloading
    window.history.replaceState(nextState, nextTitle, nextURL);
}

function toastNotification(result){
    //notification modal
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
        })
        
        Toast.fire({
        icon: result.status == "Success" ? "success": "error",
        title: result.message
    })
}

// async function placeAutoSuggestion(){
//     const options = {
//         method: 'GET',
//         headers: {
//             'X-RapidAPI-Key': '93464f8037msh725108e7458de10p12cd2cjsn038b91e1081a',
//             'X-RapidAPI-Host': 'spott.p.rapidapi.com'
//         }
//     };
    
//     response = await fetch('https://spott.p.rapidapi.com/places/autocomplete?limit=10&skip=0&country=US%2CCA&q=Sea&type=CITY', options)
//         .then(response => response.json())
//         .then(response => console.log(response))
//         .catch(err => console.log(err))
// }

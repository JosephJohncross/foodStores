const menuSelect = document.getElementById('menu-select') || null
const selectionBtn = document.querySelectorAll('.selection-btn') || null
const closeOrder = document.getElementById('close-order') || null;
const sideDrawer = document.getElementById('sideDrawer') || null;
const orders = document.getElementById('orders')
const cartCount = document.getElementById('cart_count') || null

menuSelect !== null ? menuSelect.addEventListener('click', toggleSelectionMenu) : ""
closeOrder != null ? closeOrder.addEventListener('click', slideDrawer) : ""
orders != null ? orders.addEventListener('click', slideDrawer) : ""

document.onreadystatechange = () => {
    if ( document.readyState === 'complete'){
        document.onclick = (e)=>{
            console.log(e.target);
            if (e.target.classList.contains('add_cart')){
                e.preventDefault()
                addToCart(e.target)
            }
            else if (e.target.classList.contains('cart-increase')){
                console.log("increm")   
                e.preventDefault()
                incrementCartItem(e.target)
            }
            else if (e.target.classList.contains('cart-decrease')){
                console.log("decrem")
                e.preventDefault()
                decrementCartItem(e.target)
            }
        }
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
    if (result.status == "Success"){
        cartCount.textContent = result.cartcounter["cart_count"]
    }
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

    //notification modal
    const Toast = Swal.mixin({
        toast: true,
        icon: "error",
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

    const nextURL = `${location.protocol}//${location.host}/customerDashboard/`;
    const nextTitle = 'customerDashboard';
    const nextState = { additionalInformation: 'Updated the URL with JS' };

    // This will create a new entry in the browser's history, without reloading
    window.history.pushState(nextState, nextTitle, nextURL);

    // This will replace the current entry in the browser's history, without reloading
    window.history.replaceState(nextState, nextTitle, nextURL);
    history.go()
}
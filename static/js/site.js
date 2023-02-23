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
const geoCode = document.getElementById('geocode') || null
const locationFinder = document.getElementById('location-finder') || null
const addHour = document.getElementById('add-hour') || null
const openingUrl = document.getElementById('opening_url') || null


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
            else if (e.target.id === "location-finder"){
                getCurrentUserLocation()
            }
            else if (e.target.id === "add-hour"){
                e.preventDefault()
                const day = document.getElementById('id_day').value
                const fromHour = document.getElementById('id_from_hour').value
                const toHour = document.getElementById('id_to_hour').value
                var isClosed = document.getElementById('id_is_closed').checked
                const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value
                const hourCont = document.getElementById('hour-cont')
                const addHours = document.getElementById('add-hours')
                const hourModalCloseBtn = document.getElementById('hour-modal-close')
                
                var condition
                
                if (isClosed){
                    isClosed = "True"
                    condition = "day !='' "
                }
                else{
                    isClosed = "False"
                    condition = 'day != "" && fromHour != "" && toHour != ""'
                }    

                if (eval(condition)){
                    fetch(`${openingUrl.value}`, {
                        method: "POST",
                        body: JSON.stringify({
                            "day": day,
                            "from_hour": fromHour,
                            "to_hour": toHour,
                            "is_closed": isClosed,
                        }),
                        headers: {
                            'X-CSRFToken': csrfToken,
                            'X-Request-With': 'XMLHttpRequest',
                            'Content-Type': 'application/json'
                        }
                    })
                    .then(response => response.json())
                    .then(result => {
                        console.log(result.status)
                        if (result.status == "Success"){
                            console.log(result);
                            //Adds new opening hour to vendor dashboard without page reload
                            var html = document.createElement('div')
                            html.classList = 'flex items-center'
                            html.id = `hour-${result.id}`
                            if (result.is_closed){
                                html.innerHTML = `<p class="font-semibold w-1/2">${result.day}</p>
                                        <span class="flex space-x-2 text-sm w-1/2">
                                            <p class="min-w-max">${ result.is_closed }</p>
                                        </span>
                                        <button id="remove_hour" class="w-1/3 text-red-500" data-hour_url="/vendor/opening_hours/delete/${result.id}">Delete</button>`
                            }
                            else{
                                html.innerHTML = `<p class="font-semibold w-1/2">${result.day}</p>
                                        <span class="flex space-x-2 text-sm w-1/2">
                                            <p class="min-w-max">${ result.from_hour }</p>
                                            <p class=""> - </p>
                                            <p class="min-w-max">${result.to_hour}</p>
                                        </span>
                                        <button id="remove_hour" class="w-1/2 text-red-500" data-hour_url="/vendor/opening_hours/delete/${result.id}">Delete</button>`

                            }
                            hourCont.append(html)
                            hourModalCloseBtn.click()
                            addHours.reset()
                            toastNotification(result)
                        }
                        else{
                            hourModalCloseBtn.click()
                            addHours.reset()
                            toastNotification(result)
                        }
                        
                    })
                    .catch(error => console.log(error))
                }
                else{
                    console.log("Please fil in required fields")
                }
            }
            else if (e.target.id === "remove_hour"){
                var url = e.target.dataset.hour_url
                const hourCont = document.getElementById('hour-cont')

                fetch(url, {
                    headers: {
                        'X-Request-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result.id)
                    if (result.status === "Success"){
                        var hourElem = document.getElementById(`hour-${result.id}`)
                        console.log(hourElem)
                        hourCont.removeChild(hourElem)
                        toastNotification(result)
                    }
                })
                .catch(error => console.log(error))
            }
            else if (e.target.id === "confirm-payment"){
                // e.preventDefault()
                var paymentType = document.querySelectorAll("input[name='payment_method']")
                if (paymentType[0].checked == false && paymentType[1].checked == false){
                    toastNotification({'status': 'error', 'message': 'Please select a payment method'})
                    return false
                }
                return true
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

const getCurrentUserLocation = () => {
    navigator.geolocation.getCurrentPosition((location)=> {
        geoCodeUserLocation(location.coords.latitude, location.coords.longitude)
        window.location = `?lat=${location.coords.latitude}+&lng=${location.coords.longitude}`
    })
}


const geoCodeUserLocation = (lat, lng) => {
    const url = `https://forward-reverse-geocoding.p.rapidapi.com/v1/reverse?lat=${lat}&lon=${lng}&accept-language=en&polygon_threshold=0.0`;

    const options = {
      method: 'GET',
      headers: {
        'X-RapidAPI-Key': `${geoCode.textContent}`,
        'X-RapidAPI-Host': 'forward-reverse-geocoding.p.rapidapi.com'
      }
    };

    fetch(url, options)
    	.then(res => res.json())
    	.then(json => console.log(json.display_name))
    	.catch(err => console.error('error:' + err));
}


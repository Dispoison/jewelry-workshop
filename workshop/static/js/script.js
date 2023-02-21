function getCookie(name) {
  if (!document.cookie) {
    return null;
  }

  const xsrfCookies = document.cookie.split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith(name + '='));

  if (xsrfCookies.length === 0) {
    return null;
  }
  return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}
const csrfToken = getCookie('csrftoken');

//In viewport animation
function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

const animateElements = document.querySelectorAll('.animate');

function checkViewport() {
  animateElements.forEach((el) => {
    if (isElementInViewport(el)) {
      el.classList.add('animate-visible');
    }
  });
}

window.addEventListener('scroll', checkViewport);

//Item page spoiler
const details = document.querySelector('.item-details__details');
const wrapper = document.querySelector('.item-details__wrapper');

details && details.addEventListener('click', () => {
  
  let containsUnactive = wrapper.classList.contains('item-details__wrapper_unactive');
  let containsActive = wrapper.classList.contains('item-details__wrapper_active');

  if(containsUnactive || (!containsUnactive && !containsActive)){
    wrapper.classList.remove('item-details__wrapper_unactive');
    wrapper.classList.add('item-details__wrapper_active');
  }
  else if(containsActive){
    wrapper.classList.remove('item-details__wrapper_active');
    wrapper.classList.add('item-details__wrapper_unactive');
  }
  else(
    alert('Помилка')
  );
  details.classList.toggle('item-details__details_active');
});


//Order review buttons
const editBtn = document.querySelector('.right-item__edit');
const saveBtn = document.querySelector('.right-item__save');
const orderBtn = document.querySelector('.right-item__btn');
let items = document.querySelectorAll('.left-item');
const order = document.querySelector('.right-item__order');
const orderPrice = document.querySelector('.right-item__right span');
const itemPrice = document.querySelector('.left-item__price');

let plusminusContainers = document.querySelectorAll('.left-item__btns');

const orderTotal = document.querySelector('.right-item__subtotal div span');

let htmlOrderItem = `<div class="right-item__order">
<div class="right-item__info">
     <div class="right-item__left">
         <span></span>
         <span></span>
     </div>
     <div class="right-item__right">
         <span></span>
         <span>грн.</span>
     </div>
</div>
 <div class="right-item__divider"></div>
</div>`


let htmlRedDot = `<g>
    <circle cx="15" cy="15" r="5" fill="red"></circle>
    <text x="15" y="17" font-size="8" font-weight="bold" text-anchor="middle" fill="white"></text>
</g>`

let htmlEmptyCart = `<section class="goods">
    <div class="container"><h2 class="goods__title">Кошик порожній...</h2></div>
</section>`

function generateOrderItem(itemName, itemPrice, itemQuantity){
  var div = document.createElement('div');
  div.innerHTML = htmlOrderItem.trim();
  let rightItemLeftSpans = div.querySelectorAll('.right-item__left span');
  rightItemLeftSpans[0].innerText = itemQuantity + ' ';
  rightItemLeftSpans[1].innerText = itemName;
  let rightItemRightFirstSpan = div.firstChild.querySelector('.right-item__right span');
  rightItemRightFirstSpan.innerText = `${parseInt(itemPrice) * parseInt(itemQuantity)} `;
  return div.innerHTML;
}

function updateOrder(){
  items = document.querySelectorAll('.left-item');
  let sum = 0;
  let itemName;
  let itemPrice;
  let itemQuantity;
  let orderItemContainer = document.querySelector('.right-item__order-container');
  orderItemContainer.innerHTML = '';
  let orderItem;
  items.forEach(item => {
    itemName = item.querySelector('.left-item__name').innerText;
    itemPrice = item.querySelector('.left-item__price').innerText;
    itemQuantity = item.querySelector('.left-item__quantity span').innerText;
    orderItem = generateOrderItem(itemName, itemPrice, itemQuantity);
    orderItemContainer.innerHTML += orderItem;
    sum += parseInt(itemPrice) * parseInt(itemQuantity);
  });
  orderTotal.innerText = sum;
}

items.forEach(item => {
  const plusBtn = item.querySelector('.left-item__plus');
  const minusBtn = item.querySelector('.left-item__minus');
  const itemQuantity = item.querySelector('.left-item__quantity span');
  const trash = item.querySelector('.left-item__trash')

  plusBtn && plusBtn.addEventListener('click', () => {
    itemQuantity.innerHTML ++;
    updateOrder();
  });
  
  minusBtn && minusBtn.addEventListener('click', () => {
    if(itemQuantity.innerHTML > 1){
      itemQuantity.innerHTML --;
      updateOrder();
    }
  });

  trash && trash.addEventListener('click', () => {
    item.parentElement.removeChild(item);
    updateOrder();
  });
});

editBtn && editBtn.addEventListener('click', () => {
  plusminusContainers = document.querySelectorAll('.left-item__btns');
  plusminusContainers.forEach(i => {
    i.classList.add('left-item__btns_active');
  });
  editBtn.classList.add('right-item__edit_unactive');
  saveBtn.classList.add('right-item__save_active');
  orderBtn.classList.add('right-item__btn_disabled')
  const trashes = document.querySelectorAll('.left-item__trash')
  trashes.forEach(trash => {
    trash.classList.add('left-item__trash_active');
  });
});

saveBtn && saveBtn.addEventListener('click', () => {
  plusminusContainers = document.querySelectorAll('.left-item__btns');
  editBtn.classList.remove('right-item__edit_unactive');
  plusminusContainers.forEach(i => {
    i.classList.remove('left-item__btns_active');
  });
  saveBtn.classList.remove('right-item__save_active');
  orderBtn.classList.remove('right-item__btn_disabled');
  const trashes = document.querySelectorAll('.left-item__trash')
  trashes.forEach(trash => {
    trash.classList.remove('left-item__trash_active');
  });

  items = document.querySelectorAll('.left-item');
  let orderData = [];
  let orderItem;
  let orderItemId;
  let orderItemQuantity;

  items.forEach(item => {
    orderItem = {};
    orderItemId = item.getAttribute('data-id');
    orderItemQuantity = item.querySelector('.left-item__quantity span').innerText;
    orderItem['id'] = orderItemId;
    orderItem['quantity'] = orderItemQuantity;
    orderData.push(orderItem);
  });

  const url = document.querySelector('.right-item__save').getAttribute('data-url');
  const csrf = document.querySelector('.right-item__save').getAttribute('data-csrftoken');
  sendPostRequestSave(orderData, url, csrf);
});

function sendPostRequestSave(data, url, csrf){
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (response.ok) {
      return response.json()
    }
      return Promise.reject(response);
  })
  .then(data => {
    if ("cart_items_quantity" in data){
      let cartItemsQuantity = data["cart_items_quantity"]
      setCartIconItemsQuantity(cartItemsQuantity);
      if (cartItemsQuantity <= 0){
        let divMain = document.querySelector('div.main')
        divMain.innerHTML = htmlEmptyCart;
      }
    }
  })
  .catch(error => console.error(error));
}

function sendPostRequestAdd(data, url, csrf){
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (response.ok) {
      return response.json()
    }
      return Promise.reject(response);
  })
  .then(data => {
    if ("cart_items_quantity" in data){
      let cartItemsQuantity = data["cart_items_quantity"]
      setCartIconItemsQuantity(cartItemsQuantity);
    }

    if ("added_item" in data){
      addBtn.classList.remove('item-details__btn__add')
      addBtn.classList.add('item-details__btn__remove')
      addBtn.innerHTML = 'Видалити з кошика'
    }
    else if ("removed_item" in data){
      addBtn.classList.remove('item-details__btn__remove')
      addBtn.classList.add('item-details__btn__add')
      addBtn.innerHTML = 'Додати до кошика'
    }
  })
  .catch(error => console.error(error));
}

function sendPostRequestOrderSubmit(data, url, csrf){
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (response.ok) {
      if (response.redirected) {
          window.alert('Замовлення успішно створене');
          window.location.replace(response.url)
      }
      return response.json()
    }
      return Promise.reject(response);
  })
  .then(data => {
    if ("cart_items_quantity" in data){
      let cartItemsQuantity = data["cart_items_quantity"]
      setCartIconItemsQuantity(cartItemsQuantity);
    }
  })
  .catch(error => console.error(error));
}

//Animation when cart updated
const addBtn = document.querySelector('.item-details__btn');
const bagIcon = document.querySelector('.header__bag');
addBtn && addBtn.addEventListener('click', () => {
  bagIcon.classList.add('header__bag_animate');
  setTimeout(() => {bagIcon.classList.remove('header__bag_animate')}, 500);

  // Swap 'add to cart' button to 'remove from cart'
  let csrf = addBtn.getAttribute('data-csrftoken');
  let itemId = addBtn.getAttribute('data-id');
  let cartItemAddUrl = addBtn.getAttribute('data-cart-add-url');
  let cartItemRemoveUrl = addBtn.getAttribute('data-cart-remove-url');
  let data = {"id": itemId}
  let requestUrl;
  if (addBtn.classList.contains('item-details__btn__add')){
    requestUrl = cartItemAddUrl
  }
  else if (addBtn.classList.contains('item-details__btn__remove')){
    requestUrl = cartItemRemoveUrl
  }
  sendPostRequestAdd(data, requestUrl, csrf)
});


// Set quantity value in header bag circle
function setCartIconItemsQuantity(quantity) {
  let headerBagSVG = document.querySelector('.header__bag a svg')
  let redDotG = headerBagSVG.querySelector('g')
  if (redDotG){
    if (quantity <= 0){
      headerBagSVG.removeChild(redDotG)
    }
    let redDotText = redDotG.querySelector('text');
    redDotText.innerHTML = quantity;
  }
  else {
    let div = document.createElement('div');
    div.innerHTML = htmlRedDot.trim();
    let redDotText = div.firstChild.querySelector('text');
    redDotText.innerHTML = quantity;
    headerBagSVG.innerHTML += div.innerHTML;
  }
}


//Send order information to server
function orderButtonSubmitted() {
  let data = {'client': {}};
  let cart = [];
  let itemId, itemQuantity;
  let clientForm = document.querySelector('.order__form')
  items = document.querySelectorAll('.left-item');
  let clientName = clientForm.querySelector('input[name=name]');
  let clientEmail = clientForm.querySelector('input[name=email]');
  let clientPhoneNumber = clientForm.querySelector('input[name=phone]');

  items.forEach(item => {
    itemId = item.getAttribute('data-id')
    itemQuantity = item.querySelector('.left-item__quantity span').innerText;
    cart.push({'id': itemId, 'quantity': itemQuantity})
  });
  data['cart'] = cart
  data['client']['name'] = clientName.value
  data['client']['phone_number'] = clientPhoneNumber.value
  data['client']['email'] = clientEmail.value

  let url = orderBtn.getAttribute('data-url')
  let csrf = orderBtn.getAttribute('data-csrftoken')
  sendPostRequestOrderSubmit(data, url, csrf)
}

function scrollToCategories() {
  document.querySelector('section.categories').scrollIntoView();
}

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

const details = document.querySelector('.item-details__details');
const wrapper = document.querySelector('.item-details__wrapper');

details.addEventListener('click', () => {
  
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
  else{
    alert(1);
  }
  details.classList.toggle('item-details__details_active');
});
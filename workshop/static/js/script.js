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
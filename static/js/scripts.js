// main slider
const myCarouselElement = document.querySelector("#mainSlider");

const carousel = new bootstrap.Carousel(myCarouselElement, {
  interval: 3000,
  touch: false,
  pause: false,
});

// best sellers owl carousel
$(document).ready(function () {
  $("#bestSellers").owlCarousel({
    loop: true,
    margin: 20,
    nav: true,
    navText: [
      "<span class='bi bi-chevron-left'></span>",
      "<span class='bi bi-chevron-right'></span>",
    ],
    dots: false,
    autoplay: true,
    autoplayTimeout: 3000,
    responsive: {
      0: {
        items: 1,
      },
      576: {
        items: 2,
      },
      991: {
        items: 4,
      },
    },
  });
});

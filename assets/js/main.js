/**
* Template Name: MyPortfolio
* Updated: May 30 2023 with Bootstrap v5.3.0
* Template URL: https://bootstrapmade.com/myportfolio-bootstrap-portfolio-website-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }
 

  /*
   * Easy event listener function
   */


  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * burgerMenu
   */
  const burgerMenu = select('.burger')
  on('click', '.burger', function(e) {
    burgerMenu.classList.toggle('active');
  })

  /**
   * Porfolio isotope and filter
   */
  window.addEventListener('load', () => {
    let portfolioContainer = select('#portfolio-grid');
    if (portfolioContainer) {
      let portfolioIsotope = new Isotope(portfolioContainer, {
        itemSelector: '.item',
      });

      let portfolioFilters = select('#filters a', true);

      on('click', '#filters a', function(e) {
        e.preventDefault();
        portfolioFilters.forEach(function(el) {
          el.classList.remove('active');
        });
        this.classList.add('active');


        const filterValue = this.getAttribute('data-filter');

  if (filterValue === '*') {
    // Mostra tutti gli elementi
    portfolioIsotope.arrange({
      filter: ''
    });
  } else if (filterValue === '.web') {
    // Mostra solo gli elementi con la classe 'web'
    portfolioIsotope.arrange({
      filter: '.web'
    });
  } else if (filterValue === '.design') {
    // Mostra solo gli elementi con la classe 'design'
    portfolioIsotope.arrange({
      filter: '.design'
    });
  } else if (filterValue === '.branding') {
    // Mostra solo gli elementi con la classe 'branding'
    portfolioIsotope.arrange({
      filter: '.branding'
    });
  } else if (filterValue === '.photography') {
    // Mostra solo gli elementi con la classe 'photography'
    portfolioIsotope.arrange({
      filter: '.photography'
    });
  }

  portfolioIsotope.on('arrangeComplete', function() {
    AOS.refresh();
  });
}, true);
    }

  });

  /**
   * Testimonials slider
   */
  new Swiper('.testimonials-slider', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    }
  });
/**
 * Animation on scroll
 */
window.addEventListener('load', () => {
  AOS.init({
    duration: 1000,
    easing: 'ease-in-out',
    once: true,
    mirror: false
  });

  new PureCounter();
});
})();
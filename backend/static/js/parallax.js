gsap.registerPlugin(ScrollTrigger);

const sections = gsap.utils.toArray(".container .panel"),
  container = document.querySelector(".container");

gsap.to(sections, {
  xPercent: -100 * (sections.length - 1),
  ease: "none",
  scrollTrigger: {
    trigger: ".container",
    pin: true,
    scrub: 1,
    snap: 1 / (sections.length - 1),
    end: () => "+=" + container.offsetWidth,
  },
});

$(".container .panel").mouseenter(function() {
  $(this).addClass("hover");
}).mouseleave(function() {
  $(this).removeClass("hover");
});

 //Smooth Scroll (gets break due to parallax scrolling)
 document.querySelectorAll('a[href^="#"]').forEach(anchor => {
   anchor.addEventListener('click', function(e) {
     e.preventDefault();
     document.querySelector(this.getAttribute('href')).scrollIntoView({
       behavior: 'smooth'
     });
   });
 });
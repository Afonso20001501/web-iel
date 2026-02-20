  $(document).ready(function(){
      var welcomeslide = $('#hero-slider')

            //HERO SLIDER
            welcomeslide.owlCarousel({
                 loop: true,
                 margin: 0,
                 nav: false,
                 items: 1,
                 dots: false,
                 autoplay: true,
                 autoplayTimeout: 7000,
                 smartSpeed: 1000,
                 navText:['ANTE', 'PROX'],
                 responsive:{
                      0:{
                         nav: false,    
                      },
                      768:{
                         nav: true,
                      }
                 }
            });

            welcomeslide.on('translate.owl.carousel', function () {
               var slideLayer = $("[data-animation]");
               slideLayer.each(function () {
                   var anim_name = $(this).data('animation');
                   $(this).removeClass('animated ' + anim_name).css('opacity', '0');
               });
            });

           welcomeslide.on('translated.owl.carousel', function () {
            var slideLayer = welcomeslide.find('.owl-item.active').find("[data-animation]");
            slideLayer.each(function () {
                var anim_name = $(this).data('animation');
                $(this).addClass('animated ' + anim_name).css('opacity', '1');
              });
           });
   });
   
    $('#project-slider').owlCarousel({
         loop: true,
         margin: 0,
         nav: true,
         dots: false,
         autoplayTimeout: 7000,
         smartSpeed: 1000,
         navText:['ANTE', 'PROX'],
         margin:15,
         responsive:{
              0:{
                   items: 1,
                   nav: false,
                   margin:0,
              },
              768:{
                 items: 2,
              },
              1140: {
                 items: 2,
                 center: true,
                 dots: true,
              }
       }
   })
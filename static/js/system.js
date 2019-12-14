function subMenu() {
     if($(window).width()>767 ){
     var sidebarWidth = $(".header").width();
        var mainWidth = $(window).width() - sidebarWidth;

        $(".main").width(mainWidth);
        $(".topBar").css('width', mainWidth);
        $(".footer").css('width', mainWidth);
        $(".main").css("margin-left", sidebarWidth);
        // {#toggle sidebar#}

        $(".menuBtn").click(function() {
            // {#$(".header").width(70);#}
            $(".header").toggleClass("menuToggle");
            $(".logoImg").toggleClass("logoImgE");
            if ($(".logo img").hasClass('logoImgE')) {
                $('.logoImgE.logoImg').attr('src', '/static/images/white.png');
            } else {
                $('.logoImg').attr('src', '/static/images/white.png');
            }


            var sidebarWidth = $(".header").width();
            var mainWidth = $(window).width() - sidebarWidth;
            console.log(mainWidth);
            $(".main").width(mainWidth);
            $(".topBar").css('width', mainWidth);
            $(".footer").css('width', mainWidth);
            $(".main").css("margin-left", sidebarWidth);
        });
}
 if($(window).width()<=767 ){
      $(".menuBtn").click(function() {
              if (jQuery(".header .main-menu-nav").hasClass('mainMenu-opened')) {
                jQuery(".header .main-menu-nav").slideUp(500, function() {
                    jQuery(this).removeClass("mainMenu-opened");
                });
               
            } else {
              jQuery(".header .main-menu-nav").slideDown(500, function() {
                      
                   jQuery(this).addClass("mainMenu-opened");
                });;
          }
      });

 }

        var topBarHeight = $(".topBar").outerHeight();
        // $(".mainContent").css("padding-top", topBarHeight + 15);




    

     var menuID = jQuery(".main-menu-nav");
    var downArrows = "<span class='down-arrow'></span>";
    var catchSubs = menuID.find('li ul');
    //$(".main-menu-nav li").has("ul").addClass('has-sub');
    catchSubs.parent().addClass('has-sub');
    catchSubs.parent().append(downArrows);

     /* submenu accordian */
    menuID.find('.down-arrow').siblings('a').on('click', function() {
        if (jQuery(this).siblings('ul').hasClass('open')) {
            jQuery(this).siblings('ul').slideUp(500, function() {
                jQuery(this).removeClass("open");
            });
            // jQuery(this).removeClass('submenu-opened');
        } else {
           jQuery('.down-arrow').siblings('ul').slideUp(500, function() {
               jQuery(this).removeClass("open");
           });
            jQuery(this).siblings('ul').slideDown(500, function() {

                jQuery(this).addClass("open");
            });
            // jQuery(this).addClass('submenu-opened');
        }
    });
    jQuery(".main-menu-nav ul").unbind('mouseenter mouseleave');

    resizeFix = function() {
        var mediasize = 1910;
        if (jQuery(window).width() > mediasize) { 
            menuID.on("mouseenter", ".has-sub", function() {
              
                jQuery(this).addClass("hovered");
            }).on("mouseleave", ".has-sub", function() {
                jQuery(this).removeClass("hovered");
            })
        }
        if (jQuery(window).width() <= mediasize) {
            jQuery(".main-menu-nav").on("mouseenter", ".has-sub", function() {
                jQuery(".has-sub").removeClass("hovered");

            }).on("mouseleave", ".has-sub", function() {
                jQuery(this).removeClass("hovered");
            })
        }
    };
    resizeFix();
    return jQuery(window).on('resize', resizeFix);
}

 jQuery(document).ready(function() {
     subMenu();
   
   });
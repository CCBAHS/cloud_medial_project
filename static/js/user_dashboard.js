$(function() {

  'use strict';

  $('.js-menu-toggle').click(function(e) {

  	var $this = $(this);

  	

  	if ( $('body').hasClass('show-sidebar') ) {
  		$('body').removeClass('show-sidebar');
  		$this.removeClass('active');
  	} else {
  		$('body').addClass('show-sidebar');	
  		$this.addClass('active');
  	}

  	e.preventDefault();

  });

  // click outisde offcanvas
	$(document).mouseup(function(e) {
    var container = $(".sidebar");
    if (!container.is(e.target) && container.has(e.target).length === 0) {
      if ( $('body').hasClass('show-sidebar') ) {
				$('body').removeClass('show-sidebar');
				$('body').find('.js-menu-toggle').removeClass('active');
			}
    }
	}); 

    $('.home').click(function(e) {
		var $this = $(this);		  
		if (! $('.home').hasClass('active') ) {
			$this.addClass('active');
		}   
		$('.explore').removeClass('active');
		$('.notifications').removeClass('active');
		$('.stats').removeClass('active');
		$('.signout').removeClass('active');
	});

    $('.explore').click(function(e) {
		var $this = $(this);		  
		if (! $('.explore').hasClass('active') ) {
			$this.addClass('active');
		}   
		$('.home').removeClass('active');
		$('.notifications').removeClass('active');
		$('.stats').removeClass('active');
		$('.signout').removeClass('active');   
	});

    $('.notifications').click(function(e) {
		var $this = $(this);		  
		if (! $('.notifications').hasClass('active') ) {
			$this.addClass('active');
		}   
		$('.explore').removeClass('active');
		$('.home').removeClass('active');
		$('.stats').removeClass('active');
		$('.signout').removeClass('active');   
	});

    $('.stats').click(function(e) {
		var $this = $(this);		  
		if (! $('.stats').hasClass('active') ) {
			$this.addClass('active');
		}   
		$('.explore').removeClass('active');
		$('.notifications').removeClass('active');
		$('.home').removeClass('active');
		$('.signout').removeClass('active');    
	});

    $('.signout').click(function(e) {
		var $this = $(this);		  
		if (! $('.home').hasClass('active') ) {
			$this.addClass('active');
		}   
		$('.explore').removeClass('active');
		$('.notifications').removeClass('active');
		$('.stats').removeClass('active');
		$('.home').removeClass('active');   
	});

});
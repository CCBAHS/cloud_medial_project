$(function () {

	'use strict';

	$('.js-menu-toggle').click(function (e) {

		var $this = $(this);



		if ($('body').hasClass('show-sidebar')) {
			$('body').removeClass('show-sidebar');
			$this.removeClass('active');
		} else {
			$('body').addClass('show-sidebar');
			$this.addClass('active');
		}

		e.preventDefault();

	});

	// click outisde offcanvas
	$(document).mouseup(function (e) {
		var container = $(".sidebar");
		if (!container.is(e.target) && container.has(e.target).length === 0) {
			if ($('body').hasClass('show-sidebar')) {
				$('body').removeClass('show-sidebar');
				$('body').find('.js-menu-toggle').removeClass('active');
			}
		}
	});

	// click on the sidebar
	$('.home').click(function (e) {
		var $this = $(this);
		if (!$('.home').hasClass('active')) {
			$this.addClass('active');
		}
		$('.explore').removeClass('active');
		$('.notifications').removeClass('active');
		$('.stats').removeClass('active');
		$('.signout').removeClass('active');
		$('.records').removeClass('active');
	});

	$('.explore').click(function (e) {
		var $this = $(this);
		if (!$('.explore').hasClass('active')) {
			$this.addClass('active');
		}
		$('.home').removeClass('active');
		$('.notifications').removeClass('active');
		$('.stats').removeClass('active');
		$('.signout').removeClass('active');
		$('.records').removeClass('active');
	});

	$('.notifications').click(function (e) {
		var $this = $(this);
		if (!$('.notifications').hasClass('active')) {
			$this.addClass('active');
		}
		$('.explore').removeClass('active');
		$('.home').removeClass('active');
		$('.stats').removeClass('active');
		$('.signout').removeClass('active');
		$('.records').removeClass('active');
	});

	$('.stats').click(function (e) {
		var $this = $(this);
		if (!$('.stats').hasClass('active')) {
			$this.addClass('active');
		}
		$('.explore').removeClass('active');
		$('.notifications').removeClass('active');
		$('.home').removeClass('active');
		$('.records').removeClass('active');
		$('.signout').removeClass('active');
	});

	$('.records').click(function (e) {
		var $this = $(this);
		if (!$('.records').hasClass('active')) {
			$this.addClass('active');
		}
		$('.explore').removeClass('active');
		$('.notifications').removeClass('active');
		$('.home').removeClass('active');
		$('.status').removeClass('active');
		$('.signout').removeClass('active');
	});

	$('.signout').click(function (e) {
		var $this = $(this);
		if (!$('.home').hasClass('active')) {
			$this.addClass('active');
		}
		$('.explore').removeClass('active');
		$('.notifications').removeClass('active');
		$('.stats').removeClass('active');
		$('.home').removeClass('active');
		$('.records').removeClass('active');
	});



});

// checkbox = document.getElementById('check-test');

// checkbox.addEventListener('change', e => {

//     if(e.target.checked){
// 		console.log('Bye');
// 		document.getElementById('tests').required = true;
//     }
//     else{
// 		console.log('Hello');
//         document.getElementById('tests').required = false;
//     }

// });


const btn = document.querySelector('#btn-submit');
btn.onclick = function () {
	const rbs = document.querySelectorAll('input[name="lab-type"]');
	let selectedValue;
	for (const rb of rbs) {
		if (rb.checked) {
			selectedValue = rb.value;
			break;
		}
	}
	if(selectedValue.match('pathology')){
		document.getElementById('pathology-section').style.display = 'block';
		document.getElementById('radiology-section').style.display = 'none';
		document.getElementById('pharmacy-section').style.display = 'none';
		document.getElementById('select-section').style.display = 'none';
	}
	else if(selectedValue.match('radiology')){
		document.getElementById('radiology-section').style.display = 'block';
		document.getElementById('pathology-section').style.display = 'none';
		document.getElementById('pharmacy-section').style.display = 'none';
		document.getElementById('select-section').style.display = 'none';
	}
	else if(selectedValue.match('pharmacy')){
		document.getElementById('pharmacy-section').style.display = 'block';
		document.getElementById('pathology-section').style.display = 'none';
		document.getElementById('radiology-section').style.display = 'none';
		document.getElementById('select-section').style.display = 'none';
	}
	else{
		document.getElementById('select-section').style.display = 'block';
		document.getElementById('radiology-section').style.display = 'none';
		document.getElementById('pharmacy-section').style.display = 'none';
		document.getElementById('pathology-section').style.display = 'none';
	}
};
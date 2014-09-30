$(document).ready(function() {

	// CUFON REPLACEMENT
	Cufon.replace('#navbar li a, h1.name, #main h2', { fontFamily: 'PT Sans Narrow' });

	Cufon.replace('#navbar li a span, a.read_more, #sidebar h3, #main h3.cufon, #main h4.cufon, #pagination a',  { fontFamily: 'PT Sans' });

	Cufon.replace('a.button', {
		fontFamily: 'PT Sans',
		textShadow: '1px 1px #434343'
	});


	//DROPDOWN SCRIPT
	$('#navbar ul').css({display: "none"});
	$('#navbar li').hover(function(){
		$(this).find('ul:first').css({visibility: "visible", display: "none"}).fadeIn('fast');
	},function(){
		$(this).find('ul:first').css({visibility: "hidden"});
	});

	// IE navbar last child fix
	$('#navbar li ul li:last-child').css('border-bottom', 'none');



    //IF BODY HAS CLASS VIDEO_BACKGROUND, MAKE HTML HEIGHT 100% AND ABILITY TO HIDE AND SHOW NAVIGATION ON HOME PAGE
	if($('body').hasClass('video_background') || $('body').hasClass('slider') )
	{
		$('html').css('height', '100%');
		$('#hide_menu a').css('display', 'block');

		//SHOWING MENU TOOLTIP ------ delete if you don't want it!
		$('#hide_menu a').hover( function(){
			$('.menu_tooltip').stop().fadeTo('fast', 1);
		},
		function () {
			$('.menu_tooltip').stop().fadeTo('fast', 0);
		});


		//HIDING MENU

		//click on hide menu button (arrow points up)
		$('#hide_menu a.menu_visible').live('click',function(){

			//add class hidden
			$('#hide_menu a.menu_visible')
				.removeClass('menu_visible')
				.addClass('menu_hidden')
				.attr('title', 'Show the navigation');

			// hide the tooltip
			$('.menu_tooltip').css('opacity', '0');

			//move navigation up, after replace the text
			$('#menu_wrap').animate({top: "-=480px"}, "normal", function() {
				$('.menu_tooltip p').text('Show the navigation');	//tooltip text in when menu is 'hidden'
			});

			return false;
		});


		//SHOWING MENU
		//click on show menu button (arrow points down)
		$('#hide_menu a.menu_hidden').live('click', function(){

			//add class visible
			$('#hide_menu a.menu_hidden')
			.removeClass('menu_hidden')
			.addClass('menu_visible');

			// hide the tooltip
			$('.menu_tooltip').css('opacity', '0');
			$('#menu_wrap').animate({ top: "+=480px"}, 'normal');
			$('.menu_tooltip p').text('Hide the navigation'); //tooltip text in when menu is 'visible'

			return false;
		});
	};



	//FORM (CONTACT & COMMENTS) SCRIPTS

	//set variables
	var nameVal = $("#form_name").val();
	var emailVal = $("#form_email").val();
	var websiteVal = $("#form_website").val();
	var messageVal = $("#form_message").val();


	//if name field is empty, show label in it
	if(nameVal == '') {
	$("#form_name").parent().find('label').css('display', 'block');
	}

	//if email field is empty, show label in it
	if(emailVal == '') {
	$("#form_email").parent().find('label').css('display', 'block');
	}

	//if website field is empty, show label in it
	if(websiteVal == '') {
	$("#form_website").parent().find('label').css('display', 'block');
	}


	//if message field is empty, show label in it
	if(messageVal == '') {
	$("#form_message").parent().find('label').css('display', 'block');
	}


	//hide labels on focus
	$('form input, form textarea').focus(function(){
		if($(this).attr('type') != "checkbox") {
			$(this).parent().find('label').fadeOut('fast');
		}
	});

	//show labels when field is not focused - only if there are no text
	$('form input, form textarea').blur(function(){
		var currentInput = 	$(this);
		if (currentInput.val() == ""){
		$(this).parent().find('label').fadeIn('fast');
		}
	});
	$('input, textarea').each(function(){
		if ($(this).val() == "" || $(this).attr('type') == 'checkbox')
			$(this).parent().find('label').css('display', 'block');
	});


	//SHORTCODES & ELEMENTS

	//tabs

	$(".tab_content").hide();
	$("ul.tabs").each(function() {
		$(this).find('li:first').addClass("active");
		$(this).next('.tab_container').find('.tab_content:first').show();
	});

	$("ul.tabs li a").click(function() {
		var cTab = $(this).closest('li');
		cTab.siblings('li').removeClass("active");
		cTab.addClass("active");
		cTab.closest('ul.tabs').nextAll('.tab_container:first').find('.tab_content').hide();

		var activeTab = $(this).attr("href"); //Find the href attribute value to identify the active tab + content
		$(activeTab).fadeIn(); //Fade in the active ID content
		return false;
	});


  	//toggles

  	$(".hide").hide();

  	$(".toggle").click(function(){
		$(this).closest(".toggle_box").find(".hide").toggle("fast");
		$(this).toggleClass('active');

		return false;
  	});

}); //document.ready function ends here




$(window).load(function (){
	if(!$('body').hasClass('slider')) {
		$('body').append('<div class="grid"></div>')
	}
});






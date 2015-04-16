/* ---------------------------------------------------------------- *
 * Post-page load functionality
 * ---------------------------------------------------------------- */

(function($) {
	$(function() {
		
		// Bootstrap Multi-Level Menus
		$('.submenu').hover(function() {
			
			// Display the submenu on hover
			$(this).children('ul')
				.removeClass('submenu-hide')
				.addClass('submenu-show');
				
		}, function() {
		
			// Hide the submenu when not on hover
			$(this).children('ul')
				.removeClass('.submenu-show')
				.addClass('submenu-hide');
			
		}).click(function() {
		
			// If the submenu item is clicked, navigate to its anchor
			window.location = $(this).children('a').attr('href');
			
		});
		
		// Center Header Logo only if the background image is present
		processLogoAndBackground($);
		$(window).load(function() {
			processLogoAndBackground($);
		}).resize(function() {
			processLogoAndBackground($);
		});

		// If the Activity Widget is present, activate the first tab
		if($('.tabbed-widget').length > 0) { 
			
			$('.nav-tabs').children('li:first')
				.addClass('active');
				
			$('.tab-content').children('.tab-pane:first')
				.addClass('active');
			
		} // end if
		
		// Navigate to the menu item's anchor
		$('.dropdown a').click(function() {
			window.location = $(this).attr('href');
		});
		
		// Introduce responsive functionality but only if the CSS is loaded
		if($('link[id*="bootstrap-responsive-css"]').length > 0) {
		
			// Force menus to collapse if resizing from mobile to full
			$(window).resize(function() {
				if($(this).width() >= 979) {
					$('.btn-navbar').trigger('click');
				} // end if
			});
			
			// Move sidebar below content on left sidebar layout
			if($('#sidebar').length > 0 && $('#wrapper > .container > .row').children(':first').attr('id') == 'sidebar') {
			
				moveSidebarInLeftSidebarLayout($);
				$(window).resize(function() {
					moveSidebarInLeftSidebarLayout($);
				});
			
			} // end if
			
			// FitVid
			$('.entry-content').fitVids();
			
		} // end if

	});
})(jQuery);

/**
 * In mobile view with the left-sidebar layout, repositions the sidebar below the content.
 */
function moveSidebarInLeftSidebarLayout($) {

	if($('#wrapper').width() < 768) {
		$('#sidebar').insertAfter('#main');
	} else {
		$('#sidebar').insertBefore('#main');
	} // end if

} // end moveSidebarInLeftSidebarLayout

/**
 * This positions the logo against the background so that it's centered and properly positioned for
 * responsive behavior.
 *
 * @params	$	A reference to the jQuery function.
 */
function processLogoAndBackground($) {
	
	// If we're viewing the mobile version of the site, we need to position the header elements
	if( $('.btn-navbar').is(':visible') ) {
	
		if( $('#header-image').length > 0 ) { 

			// If the header image is larger than the logo container, we subtract half the height of the header from the background image...
			if( $('#header-image').height() > $('#hgroup').height() ) {
			
				$('#hgroup').css({
					marginTop: Math.round( $('#header-image').height() / 2 ) - Math.round( $('#hgroup').height() / 2 )
				});
			
			// ...otherwise, we'll subtract the height of the hgroup from the header image	
			} else {
			
				$('#hgroup').css({
					marginTop: Math.round( $('#header-image').height() / 2 ) - Math.round( $('#hgroup').height() )
				});
				
			} // end if
		
		} else {
		
			if( $('#header-widget').length > 0 ) {
			
				// Only set the margin of the header widget to 20 if there's no logo
				if( $('#logo').length > 0 ) {
				
					$('#header-widget').css({
						marginTop: '20px'
					});
					
				} // end if
				
			} // end if
		
		} // end if/else
		
	} else {
	
		// If there's no logo and header image, we don't care about adjusting margins
		if( $('#header-image').length > 0 || $('#site-title > a').children('img').length > 0 ) { 
	
			var $background = null;
			if( ( $background = $('#header-image').children(':first').children('img')).length > 0 ) {
			
				$('#hgroup').css({
					padding: 0,
					marginTop: Math.round( $background.height() / 2 ) - Math.round( $('#hgroup').height() / 2 )
				});
				
			} // end if
			
			// If the widget is present...
			if($('#header-widget').length > 0) {
	
				// ...and there is a logo or header text
				if( $('#logo').length > 0 ) {
	
					$('#header-widget').css({
						marginTop: Math.round( $('#hgroup').height() / 2 ) - Math.round( $('#header-widget').height() / 2 )
					});	
				
				// ...or there is no logo or no header text
				} else {
	
					$('#header-widget').css({
						marginTop: Math.round( $('#header-image').height() / 2 ) - Math.round( $('#header-widget').height() )
					});
					
					// If there's a header widget but no logo or text, then we need to make the hgroup and the logo an anchor
					$('#hgroup')
						.css('cursor', 'pointer')
						.click(function(evt) {
							window.location = $('#site-title').children('a').attr('href');
						});
					
					
				} // end if
				
			} // end if
				
		} // end if 
	
	} // end if
	
} // end processLogoAndBackground
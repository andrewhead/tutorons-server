(function($) {
	$(function() {
		
		// Grab a reference to the gravatar container and its default image
		$gravatar = $('#comment-form-avatar').children('img');
		var sDefaultImageUrl = $gravatar.attr('src');
		
		// When the focus blurs from the field, update the gravatar
		$('#email').blur(function() {
			
			if($(this).val() === '') {
			
				$gravatar.attr('src', sDefaultImageUrl);
				
			} else {

				var sUrl = 'http://www.gravatar.com/avatar/' + md5($(this).val()) + '?d=' + sDefaultImageUrl;		
				$gravatar.attr('src', sUrl);
			
			} // end if/else
			
		});
		
		// Toggles acceptable HTML tags
		if($('.form-allowed-tags').length > 0) {

			$('.form-allowed-tags').children('a')
				.click(function(evt) {
					evt.preventDefault();
					$(this).siblings('code')
						.fadeToggle('fast');
				});
				
		} // end if
		
	});
})(jQuery);
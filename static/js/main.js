$(document).ready(function() {
	$(".char").mouseover(function() {
		charnum = $(this).attr("char");
		$(".char[char=" + charnum + "]").addClass("highlight");
	}).mouseout(function() {
		charnum = $(this).attr("char");
		$(".char[char=" + charnum + "]").removeClass("highlight");
	});
});
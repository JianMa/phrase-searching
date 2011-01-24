$(document).ready(function() {
	$("td.char").mouseover(function() {
		charnum = $(this).attr("charnum");
		$("td.char[charnum=" + charnum + "]").addClass("highlight");
	}).mouseout(function() {
		charnum = $(this).attr("charnum");
		$("td.char[charnum=" + charnum + "]").removeClass("highlight");
	});
	
	$("td.wordindex").mouseover(function() {
		wordnum = $(this).attr("wordnum");
		$("td.char[wordnum=" + wordnum + "]").addClass("highlight");
	}).mouseout(function() {
		wordnum = $(this).attr("wordnum");
		$("td.char[wordnum=" + wordnum + "]").removeClass("highlight");
	});
});
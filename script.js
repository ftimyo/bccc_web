function beautifultable() {
	$("tr.event-table-content:even").css("background-color", "cornsilk");
	$("tr.event-table-content:odd").css("background-color", "seashell");
	$("tr.sermon-table-content:odd").css("background-color", "seashell");
	$("tr.sermon-table-content:even").css("background-color", "gainsboro");
	$("tr.sermon-table-content").mouseenter(function(){$(this).css("background-color", "peachpuff");});
	$("tr.sermon-table-content:odd").mouseleave(function(){$(this).css("background-color", "seashell");});
	$("tr.sermon-table-content:even").mouseleave(function(){$(this).css("background-color", "gainsboro");});
	$("tr.event-table-content").mouseenter(function(){$(this).css("background-color", "peachpuff");});
	$("tr.event-table-content:odd").mouseleave(function(){$(this).css("background-color", "seashell");});
	$("tr.event-table-content:even").mouseleave(function(){$(this).css("background-color", "cornsilk");});
}
function morestyles(){
	beautifultable();
	$(function() {
		$( ".DateField" ).datepicker({
			changeDay: true,
			changeMonth: true,
			changeYear: true,
			yearRange: "2014:c+0",
		});
	});
	$(function() {
    $( "#sort" ).selectmenu();
  });
}

$("document").ready(morestyles);

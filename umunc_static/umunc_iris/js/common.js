/*
* @Author: eastpiger
* @Date:   2016-03-14 01:14:08
* @Last Modified by:   eastpiger
* @Last Modified time: 2016-03-14 22:29:29
*/
$(".process_panel_item.success .process_panel_icon").html("<span class=\"fui-check\"></span>");
$(".process_panel_item.next .process_panel_icon").html("<span class=\"fui-arrow-right\"></span>");
$(".process_panel_item.next,.process_panel_item.next,.process_panel_item.active").click(function(event) {
	window.location.href=this.attr("href");
});;



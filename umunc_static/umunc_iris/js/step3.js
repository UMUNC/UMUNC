$(function() {
	$("form  input,select,textarea").jqBootstrapValidation({submitError: function ($form, event, errors) {alert("提交失败！请检查是否存在非法输入！");}});
	$("#submitbutton").click(function(){
		$("#submit").val("1");
		$('#askModal').modal('hide');
		$("#savebutton").click();
	});
	$(".process_panel_item:nth-child(4)").removeClass("success");
	$(".process_panel_item:nth-child(4)").removeClass("next");
	$(".process_panel_item:nth-child(4)").addClass("active");
});

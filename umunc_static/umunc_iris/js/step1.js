$(function() {
	$("form  input,select,textarea").jqBootstrapValidation({submitError: function ($form, event, errors) {alert("提交失败！请检查是否存在非法输入！");}});
	$("#submitbutton").click(function(){
		$('#askModal').modal('hide');
		$("#submit").val("1");
		$("#savebutton").click();
	});
	$(".process_panel_item:nth-child(2)").addClass("active");
});

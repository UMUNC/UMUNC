function changeclass(){
	$("#name").val("无");
	$("#school").val("无");
	$("#password").val("无");
	$("#group").val("无");
	$("#name").parent().parent().css("display","none");
	$("#school").parent().parent().css("display","none");
	$("#password").parent().parent().css("display","none");
	$("#group").parent().parent().css("display","none");
	if ($("#class").val()=="1"){
		$("#name").val("");
		$("#school").val("");
		$("#password").val("");
		$("#name").parent().parent().css("display","block");
		$("#school").parent().parent().css("display","block");
		$("#password").parent().parent().css("display","block");
	}else if ($("#class").val()=="2"){
		$("#group").val("");
		$("#password").val("");
		$("#group").parent().parent().css("display","block");
		$("#password").parent().parent().css("display","block");
	}else if ($("#class").val()=="3"){
	};
};
$(function() {
	$("form  input,select,textarea").jqBootstrapValidation({submitError: function ($form, event, errors) {alert("提交失败！请检查是否存在非法输入！");}});
	$("#class").change(changeclass);
	changeclass();
	$("#submitbutton").click(function(){
		$('#askModal').modal('hide');
		$("#savebutton").click();
	});
});
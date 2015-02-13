function havejoinedcheck(){
	if ($("#munjoined").val()=="0"){
		$("#munjoinedc").val("无");
		$("#munjoinedc").parent().css("display","none");
	}else{
		$("#munjoinedc").parent().css("display","table");
	};
};
function transcommitee(){
	if ($("#conference").val()=="1"){
		$("#commitee").html('<option value="1">联动体系 - 国家内阁</option><option value="2">联动体系 - 联合国安全理事会</option><option value="3">联动体系 - 主新闻中心</option><option value="4">联动体系 - 联合国秘书处</option><option value="5">欧洲体系 - 欧盟委员会</option><option value="6">欧洲体系 - 欧盟理事会</option><option value="7">GAUS - United Security Council</option><option value="8">GAUS - United Nations General Assembly 1st Committee - Disarmament and International Security Committee</option><option value="9">独立会场 - 世界旅游旅行大会</option>');
	}else if ($("#conference").val()=="2"){
		$("#commitee").html('<option value="10">联动体系 - 国家内阁</option><option value="11">联动体系 - 东盟10+3峰会</option><option value="12">联动体系 - 主新闻中心</option><option value="13">联动体系 - 联合国秘书处</option><option value="14">独立会场 - 欧洲安全与合作组织部长级会议</option><option value="15">Independent Committee - United Nations General Assembly 1st Committee - Disarmament and International Security Committee</option>');
	}else if ($("#conference").val()=="3"){
		$("#commitee").html('<option value="16">联动体系 - 国家内阁</option><option value="17">联动体系 - 联合国安全理事会</option><option value="18">联动体系 - 主新闻中心</option><option value="19">联动体系 - 联合国秘书处</option><option value="20">独立会场 - 联合国开发计划署</option><option value="21">Independent Committee - United Nations General Assembly 3rd Committee - Social, Humanitarian and Culture Committee</option>');
	};
};
$(function() {
	$("form  input,select,textarea").jqBootstrapValidation({submitError: function ($form, event, errors) {alert("提交失败！请检查是否存在非法输入！");}});
	$("#submitbutton").click(function(){
		$("#submit").val("1");
		$("#savebutton").click();
	});
	havejoinedcheck();
	$("#munjoined").change(havejoinedcheck);
	$("#conference").change(transcommitee);
});
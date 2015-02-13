var communication_number;
var heartbeat,heartbeat2,heartbeat3,heartbeat4;
var meeting_count;
var communication_count_simple = new Array();
var vtime_base = 0,vtime_check = 0,vtime_step = 1;
var screen_lock=false;
function meeting_refresh(){
	clearTimeout(heartbeat2);
	$.ajax({
		url: "/cheetah/datacontrol/meeting/",
		data: {
			command:"GetHeartBeat"
		},
		success: function(data,status){
			if (data.result=="success"){
				if (data.count>meeting_count){
					meeting_count=data.count
					$("#main_panel #top_panel #Meetings #meeting_list tbody").html(data.meeting);
					Messenger().post( "Meeting has been updated.");
				}
			};
			heartbeat2=setTimeout("meeting_refresh()",60000);
		},
		error: function(){
			clearTimeout(heartbeat2);
			Messenger().post( "System error. Page will be upgraded.");
			Messenger().post( "Receive refresh command. Page will be upgraded in 10 seconds.");
			heartbeat=setTimeout("location.reload(true)",10000);
		},
		dataType: 'json'
	});
};
function startTime()
{
	function checkTime(i)
	{
		if (i<10) 
			{i="0" + i}
			return i
	}
	function formatTime(someday)
	{
		var Y=someday.getFullYear()
		var M=someday.getMonth()+1
		var D=someday.getDate()
		var h=someday.getHours()
		var m=someday.getMinutes()
		var s=someday.getSeconds()
		M=checkTime(M)
		D=checkTime(D)
		m=checkTime(m)
		s=checkTime(s)
		return Y+"-"+M+"-"+D+" "+h+":"+m+":"+s
	}
	clearTimeout(heartbeat4);
	var today=new Date();
	var vtoday=new Date();
	vtoday.setTime((today.getTime()-vtime_base)*vtime_step+vtime_check);
	$("#main_panel #top_panel #Communications #time_panel p").html(
		"Real: "+formatTime(today)+"<br/>Vitual: "+formatTime(vtoday));
	$("#main_panel #top_panel #Settings #setting_time_status").html(
		"Real: "+formatTime(today)+"<br/>Vitual: "+formatTime(vtoday)+
		"<br/>BaseTime: "+vtime_base+"<br/>VitualBaseTime: "+vtime_check+
		"<br/>TimeStep: "+vtime_step);
	heartbeat4=setTimeout('startTime()',100)
}
function time_refresh(){
	clearTimeout(heartbeat3);
	$.ajax({
		url: "/cheetah/datacontrol/time/",
		success: function(data,status){
			if (!((vtime_base==data.vtime_base) && (vtime_check==data.vtime_check) && (vtime_step==data.vtime_step))){
				vtime_base=data.vtime_base;
				vtime_check=data.vtime_check;
				vtime_step=data.vtime_step;
				startTime();
			};
		},
		dataType: 'json'
	});
	heartbeat3=setTimeout("time_refresh()",30000);
};
function communication_refresh_simple(){
  	var refresh_simple = arguments[0] ? arguments[0] : false;
	clearTimeout(heartbeat);
	$.ajax({
		url: "/cheetah/datacontrol/communication/",
		data: {
			command:"GetHeartBeatSimple"
		},
		success: function(data,status){
			if (data.messages=="REFRESH"){
				Messenger().post( "Receive refresh command. Page will be upgraded in 10 seconds.");
				heartbeat=setTimeout("location.reload(true)",10000);
				return
			};
			if (refresh_simple){
				$("#main_panel #top_panel #Communications #communication_list a #new_message").html("");
				$(data).each(function(index,element){
					communication_count_simple[element.id]=element.count;
				});
				return
			};
			$(data).each(function(index,element){
				if (element.id==communication_number){
					$("#main_panel #top_panel #Communications #communication_list a#"+element.name+" #new_message").html("");
					if (element.count!=communication_count_simple[element.id]){communication_refresh()};
					communication_count_simple[element.id]=element.count;
				}
				if ((element.id!=communication_number)&&(element.count!=communication_count_simple[element.id])){
					$("#main_panel #top_panel #Communications #communication_list a#"+element.name+" #new_message").html(element.count-communication_count_simple[element.id]);
				}else{
					$("#main_panel #top_panel #Communications #communication_list a#"+element.name+" #new_message").html("");
				};
			});
			heartbeat=setTimeout("communication_refresh_simple()",2000);
		},
		error: function(){
			Messenger().post( "System error. Page will be upgraded.");
			Messenger().post( "Receive refresh command. Page will be upgraded in 10 seconds.");
			heartbeat=setTimeout("location.reload(true)",10000);
		},
		dataType: 'json'
	});
};
function communication_refresh(){
  	var disable_screenlock = arguments[0] ? arguments[0] : false;
	$.ajax({
		url: "/cheetah/datacontrol/communication/",
		data: {
			command:"GetHeartBeat",
			number:communication_number
		},
		success: function(data,status){
			if (data.result=="success"){
				if (screen_lock&&!disable_screenlock){return};
				screen_lock=false;
				if ((data.room.Block==true)&&(data.staff==false)){
					$("#main_panel #top_panel #Communications .panel-footer input#content").attr("disabled","disabled");
					$("#main_panel #top_panel #Communications .panel-footer button").attr("disabled","disabled");
				}else{
					$("#main_panel #top_panel #Communications .panel-footer input#content").removeAttr("disabled");
					$("#main_panel #top_panel #Communications .panel-footer button").removeAttr("disabled");						
				};
				var height_delta=$("#main_panel #top_panel #Communications .panel-body div").height()-$("#main_panel #top_panel #Communications .panel-body").scrollTop();
				$("#main_panel #top_panel #Communications .panel-heading h3").html(data.room.Name);
				$("#main_panel #top_panel #Communications .panel-body").html(data.messages);
				$('[data-toggle="tooltip"]').tooltip();
				$("#main_panel #top_panel #Communications .panel-body").scrollTop($("#main_panel #top_panel #Communications .panel-body div").height()-height_delta);
			}else{
				$("#main_panel #top_panel #Communications .panel-footer input#content").attr("disabled","disabled");
				$("#main_panel #top_panel #Communications .panel-footer button").attr("disabled","disabled");
				$("#main_panel #top_panel #Communications .panel-body").html(data.result);
			};
			$('#loaddialog').modal('hide');
		},
		error: function(){
			Messenger().post( "System error. Page will be upgraded.");
			Messenger().post( "Receive refresh command. Page will be upgraded in 10 seconds.");
			heartbeat=setTimeout("location.reload(true)",10000);
		},
		dataType: 'json'
	});
};
function communication_fresh(number){
	screen_lock=true;
	$('#loaddialog').modal('show');
	clearTimeout(heartbeat);
	$("#main_panel #top_panel #Communications .list-group a").removeClass("active");
	$("#main_panel #top_panel #Communications .list-group a#communication_btn_"+number).addClass("active");
	communication_number=number;
	$("#main_panel #top_panel #Communications .panel-heading h3").html('Loading');
	$("#main_panel #top_panel #Communications .panel-body").html("Loading");
	communication_refresh(true);
	communication_refresh_simple();
};
function meeting_change(user_number,number,accept){
	$.ajax({
		url: "/cheetah/datacontrol/meeting/",
		data: {
			command:"PostChange",
			user_number:user_number,
			number:number,
			accept:accept,
			csrfmiddlewaretoken:$("#main_panel #top_panel #Communications #form_communication_send [name='csrfmiddlewaretoken']").val()
		},
		success: function(data,status){
			if (data.result=="success"){
				meeting_count=0;
				meeting_refresh();
			}else{
				alert("失败："+data.result);
			};
		},
		dataType: 'json',
		type: 'POST'
	});
};
$(function(){
	$.backstretch([
		"/static/umunc_cheetah/image/bg_1.jpg",
		"/static/umunc_cheetah/image/bg_2.jpg",
		"/static/umunc_cheetah/image/bg_3.jpg",
	], {
		fade: 1000,
		duration: 7000
	});	
	$('#loaddialog').modal({
		keyboard: false,
		backdrop: 'static',
		show: false,
	});
	Messenger.options = {
		extraClasses: 'messenger-fixed messenger-on-top',
		theme: 'air'
	};
	var date=new Date();
	$(".form_datetime").val(date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+' '+date.getHours()+':'+date.getMinutes());
	$(".form_datetime").datetimepicker({format: 'yyyy-mm-dd hh:ii',todayHighlight:true,todayBtn:true});
	$("#myModal,#setting_time_modal").on("show.bs.modal",function(){$('body').scrollTop(0)});
	$("#main_panel #top_panel #Communications #form_communication_send").submit(function(){
		$.ajax({
			url: "/cheetah/datacontrol/communication/",
			data: {
				command:"PostSend",
				number:communication_number,
				system:$("#main_panel #top_panel #Communications #form_communication_send input#system").prop("checked"),
				content:$("#main_panel #top_panel #Communications #form_communication_send input#content").val(),
				csrfmiddlewaretoken:$("#main_panel #top_panel #Communications #form_communication_send [name='csrfmiddlewaretoken']").val()
			},
			success: function(data,status){
				if (data.result=="success"){
					$("#main_panel #top_panel #Communications #form_communication_send input#content").val("FROM:… TO:…");
					communication_refresh();
				}else{
					alert("发送失败："+data.result);
				};
			},
			dataType: 'json',
			type: 'POST'
		});
		return false;
	});
	$("#form_communication_send_all").submit(function(){
		$.ajax({
			url: "/cheetah/datacontrol/communication/",
			data: {
				command:"PostSendAll",
				content:$("#form_communication_send_all #content").val(),
				csrfmiddlewaretoken:$("#main_panel #top_panel #Communications #form_communication_send [name='csrfmiddlewaretoken']").val()
			},
			success: function(data,status){
				if (data.result=="success"){
					$("#form_communication_send_all #content").val("");
					$('#communication_send_all_modal').modal('hide');
				}else{
					alert("发送失败："+data.result);
				};
			},
			dataType: 'json',
			type: 'POST'
		});
		return false;
	});
	$("#form_setting_time").submit(function(){
		function getDate(strDate) {  
			var date = eval('new Date(' + strDate.replace(/\d+(?=-[^-]+$)/,  
			function (a) { return parseInt(a, 10) - 1; }).match(/\d+/g) + ')');  
			return date;  
		};
		if (isNaN($("#form_setting_time #timestep").val())){
			alert("请输入数字！");
			return false;
		};
		$.ajax({
			url: "/cheetah/datacontrol/setting/",
			data: {
				command:"Time",
				BaseTime:getDate($("#form_setting_time #basetime").val()).getTime(),
				VirtualBaseTime:getDate($("#form_setting_time #virtualbasetime").val()).getTime(),
				TimeStep:$("#form_setting_time #timestep").val(),
				csrfmiddlewaretoken:$("#main_panel #top_panel #Communications #form_communication_send [name='csrfmiddlewaretoken']").val()
			},
			success: function(data,status){
				if (data.result=="success"){
					alert("成功执行");
					location.reload(true);
				}else{
					alert("发送失败："+data.result);
				};
			},
			dataType: 'json',
			type: 'POST'
		});
		return false;
	});
	$("#form_meeting_send").submit(function(){
		$.ajax({
			url: "/cheetah/datacontrol/meeting/",
			data: {
				command:"PostSend",
				host:$("#form_meeting_send #host").val(),
				to:$("#form_meeting_send #to").val(),
				location:$("#form_meeting_send #location").val(),
				description:$("#form_meeting_send #description").val(),
				time:$("#form_meeting_send #time").val(),
				csrfmiddlewaretoken:$("#main_panel #top_panel #Communications #form_communication_send [name='csrfmiddlewaretoken']").val()
			},
			success: function(data,status){
				if (data.result=="success"){
					$("#form_meeting_send #location").val("");
					$("#form_meeting_send #description").val("");
					$('#myModal').modal('hide');
					meeting_refresh();
				}else{
					alert("发送失败："+data.result);
				};
			},
			dataType: 'json',
			type: 'POST'
		});
		return false;
	});
	$("#main_panel #top_panel #Communications #block").click(function(){
		$.ajax({
			url: "/cheetah/datacontrol/communication/",
			data: {
				command:"PostBlock",
				number:communication_number,
				csrfmiddlewaretoken:$("#main_panel #top_panel #Communications #form_communication_send [name='csrfmiddlewaretoken']").val()
			},
			success: function(data,status){
				if (data.result=="success"){
					communication_refresh();
				}else{
					alert("失败："+data.result);
				};
			},
			dataType: 'json',
			type: 'POST'
		});
		return false;
	});
	$("#main_panel #top_panel #Settings #cache_clear_submit").click(function(){
		$.ajax({
			url: "/cheetah/datacontrol/setting/",
			data: {
				command:"ClearRefresh",
				csrfmiddlewaretoken:$("#main_panel #top_panel #Communications #form_communication_send [name='csrfmiddlewaretoken']").val()
			},
			success: function(data,status){
				if (data=="success"){
					alert("成功执行");
					location.reload(true);
				}else{
					alert("失败："+data.result);
				};
			},
			type: 'POST'
		});
		return false;
	});
	$("#main_panel #top_panel #Settings #frontend_refresh_submit").click(function(){
		$.ajax({
			url: "/cheetah/datacontrol/setting/",
			data: {
				command:"FrontendRefresh",
				csrfmiddlewaretoken:$("#main_panel #top_panel #Communications #form_communication_send [name='csrfmiddlewaretoken']").val()
			},
			success: function(data,status){
				if (data=="success"){
					alert("成功执行");
					location.reload(true);
				}else{
					alert("失败："+data.result);
				};
			},
			type: 'POST'
		});
		return false;
	});
	$('#form_file_send').submit(function(handle){
		$(this).ajaxSubmit({
			beforeSubmit : function() {
				var filepath=$("#form_file_send #file").val();
				var extStart=filepath.lastIndexOf(".");
				var ext=filepath.substring(extStart,filepath.length).toLowerCase();
				if(ext!=".pdf"&&ext!=".doc"&&ext!=".docx"){
					alert("Only PDF/DOC/DOCX file will be accepted.");
					return false;
				}
				$("#form_file_send #upload_submit").addClass("disabled");
				$("#form_file_send #upload_submit").html("Uploading……");
			},
			success : function(data) {
				if (data.result=="success"){
					alert("上传成功。");
					$("#form_file_send #url").html("Success! Click here to download.");
					$("#form_file_send #url").attr('href',data.url);
				}else{
					alert("失败："+data.result);
				};
				$("#form_file_send #upload_submit").removeClass("disabled");
				$("#form_file_send #upload_submit").html("Send");
			},
			error : function(data) {
				alert("上传发生错误！请刷新页面或联系我们。");
				$("#form_file_send #upload_submit").removeClass("disabled");
				$("#form_file_send #upload_submit").html("Send");
			},
			dataType :"json"
		});
		return false;
	});
	meeting_count=0;
	meeting_refresh();
	time_refresh();
	communication_refresh_simple(true);
	$("#main_panel #top_panel #Communications .list-group a:first").click();
    if ($("#communication_list").parent().height()>$("#Communications .panel").height()){$("#Communications .panel .panel-body").css("height",$("#communication_list").parent().height()-121)};
}) 
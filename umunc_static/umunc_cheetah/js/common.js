var identifier_communication,identifier_meeting;
var identifier_communication_static,identifier_meeting_static;
var status_communication_count = new Array();
var status_communication;
var heartbeat_handle,heartbeat_handle_time;
var heartbeat_command = 1;
var vtime_base = 0,vtime_check = 0,vtime_step = 1;
var control_sound = true;

function refresh(){
	clearTimeout(heartbeat_handle);
	Messenger().post("接收到刷新指令，页面将在20秒内刷新。");
	heartbeat_handle=setTimeout("location.reload(true)",20000);
};

function communication_refresh(){
  	var disable_screenlock = arguments[0] ? arguments[0] : false;
	var today=new Date();
	identifier_communication=today.getTime();
	identifier_communication_static=today.getTime();
	$.ajax({
		url: "/cheetah/datacontrol/heartbeat/",
		data: {
			command:"GetCommunication",
			number:status_communication
		},
		success: function(data,status){
			if (identifier_communication_static!=identifier_communication){
				return;
			};
			if (data.result=="success"){
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
            	$("#main_panel #top_panel #Communications .panel-body").animate({"scrollTop": $("#main_panel #top_panel #Communications .panel-body div").height()-height_delta}, "slow");
			}else{
				$("#main_panel #top_panel #Communications .panel-footer input#content").attr("disabled","disabled");
				$("#main_panel #top_panel #Communications .panel-footer button").attr("disabled","disabled");
				$("#main_panel #top_panel #Communications .panel-body").html(data.result);
			};
			$('#loaddialog').modal('hide');
		},
		error: function(){
			Messenger().post("System error. Page will be upgraded.");
			refresh();
		},
		dataType: 'json'
	});
};

function meeting_refresh(){
	identifier_meeting_static=identifier_meeting;
	$.ajax({
		url: "/cheetah/datacontrol/heartbeat/",
		data: {
			command:"GetMeeting"
		},
		success: function(data,status){
			if (identifier_meeting_static!=identifier_meeting){
				return;
			};
			if (data.result=="success"){
				$("#main_panel #top_panel #Meetings #meeting_list tbody").html(data.meeting);
			};
			$('#loaddialog').modal('hide');
		},
		error: function(){
			Messenger().post("System error. Page will be upgraded.");
			refresh();
		},
		dataType: 'json'
	});
};

function heartbeat(){
	clearTimeout(heartbeat_handle);
	$.ajax({
		url: "/cheetah/datacontrol/heartbeat/",
		data: {
			command:"GetHeartBeat"
		},
		success: function(data,status){
			if (data.messages=="REFRESH"){
				refresh();
				return
			};
			var communication_has_new=false,meeting_has_new=false;
			if (heartbeat_command==0){
				$(data.communication).each(function(index,element){
					if (element.id==status_communication){
						$("#main_panel #top_panel #Communications #communication_list a#"+element.name+" #new_message").html("");
						if (element.count!=status_communication_count[element.id]){
							communication_refresh()
							communication_has_new=true;
						};
						status_communication_count[element.id]=element.count;
					};
					if ((element.id!=status_communication)&&(element.count!=status_communication_count[element.id])){
						communication_has_new=($("#main_panel #top_panel #Communications #communication_list a#"+element.name+" #new_message").length >0)&&($("#main_panel #top_panel #Communications #communication_list a#"+element.name+" #new_message").html()!=element.count-status_communication_count[element.id]);
						$("#main_panel #top_panel #Communications #communication_list a#"+element.name+" #new_message").html(element.count-status_communication_count[element.id]);
					}else{
						$("#main_panel #top_panel #Communications #communication_list a#"+element.name+" #new_message").html("");
					};
				});
				if (identifier_meeting!=data.meeting){
					identifier_meeting=data.meeting;
					meeting_refresh();
					meeting_has_new=true;
				};
				if (!((vtime_base==data.virtualtime.vtime_base) && (vtime_check==data.virtualtime.vtime_check) && (vtime_step==data.virtualtime.vtime_step))){
					vtime_base=data.virtualtime.vtime_base;
					vtime_check=data.virtualtime.vtime_check;
					vtime_step=data.virtualtime.vtime_step;
				};
			};
			if (heartbeat_command==1){
				$("#main_panel #top_panel #Communications #communication_list a #new_message").html("");
				$(data.communication).each(function(index,element){
					status_communication_count[element.id]=element.count;
					if (element.id==status_communication){
						communication_refresh();
					};
				});
				heartbeat_handle=setTimeout("heartbeat()",3000);
				if (identifier_meeting!=data.meeting){
					identifier_meeting=data.meeting;
					meeting_refresh();
				};
				if (!((vtime_base==data.virtualtime.vtime_base) && (vtime_check==data.virtualtime.vtime_check) && (vtime_step==data.virtualtime.vtime_step))){
					vtime_base=data.virtualtime.vtime_base;
					vtime_check=data.virtualtime.vtime_check;
					vtime_step=data.virtualtime.vtime_step;
				};
			};
			if (heartbeat_command==2){
				$(data.communication).each(function(index,element){
					if (element.id==status_communication){
						$("#main_panel #top_panel #Communications #communication_list a#"+element.name+" #new_message").html("");
						if (element.count!=status_communication_count[element.id]){
							communication_refresh()
						};
						status_communication_count[element.id]=element.count;
					};
				});
			};
			if (communication_has_new){
				Messenger().post("收到新消息。");
			};
			if (meeting_has_new){
				Messenger().post("收到meeting更新。");
			};
			if (communication_has_new | meeting_has_new){
				if (control_sound){$('#chatAudio')[0].play();};
			};
			heartbeat_command=0;
			heartbeat_handle=setTimeout("heartbeat()",3000);
		},
		error: function(){
			Messenger().post("System error. Page will be upgraded.");
			refresh();
		},
		dataType: 'json'
	});
};

function communication_fresh(number){
	$('#loaddialog').modal('show');
	clearTimeout(heartbeat_handle);
	$("#main_panel #top_panel #Communications .list-group a").removeClass("active");
	$("#main_panel #top_panel #Communications .list-group a#communication_btn_"+number).addClass("active");
	$("#main_panel #top_panel #Communications .panel-heading h3").html('Loading');
	$("#main_panel #top_panel #Communications .panel-body").html("Loading");
	status_communication=number;
	status_communication_count[status_communication]=-1;
	if (heartbeat_command==0){heartbeat_command=2};
	heartbeat();
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
				$('#loaddialog').modal('show');
				heartbeat();
			}else{
				alert("失败："+data.result);
			};
		},
		dataType: 'json',
		type: 'POST'
	});
};

function meeting_global(number){
	$.ajax({
		url: "/cheetah/datacontrol/meeting/",
		data: {
			command:"PostGlobal",
			number:number,
			csrfmiddlewaretoken:$("#main_panel #top_panel #Communications #form_communication_send [name='csrfmiddlewaretoken']").val()
		},
		success: function(data,status){
			if (data.result=="success"){
				$('#loaddialog').modal('show');
				heartbeat();
			}else{
				alert("失败："+data.result);
			};
		},
		dataType: 'json',
		type: 'POST'
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
	clearTimeout(heartbeat_handle_time);
	var today=new Date();
	var vtoday=new Date();
	vtoday.setTime((today.getTime()-vtime_base)*vtime_step+vtime_check);
	$("#main_panel #top_panel #Communications #time_panel p").html(
		"Real: "+formatTime(today)+"<br/>Virtual: "+formatTime(vtoday));
	$("#main_panel #top_panel #Settings #setting_time_status").html(
		"Real: "+formatTime(today)+"<br/>Virtual: "+formatTime(vtoday)+
		"<br/>BaseTime: "+vtime_base+"<br/>VitualBaseTime: "+vtime_check+
		"<br/>TimeStep: "+vtime_step);
	heartbeat_handle_time=setTimeout('startTime()',100)
}

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
		extraClasses: 'messenger-fixed messenger-on-top messenger-on-right',
		theme: 'air'
	};
	var date=new Date();
	$(".form_datetime").val(date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+' '+date.getHours()+':'+date.getMinutes());
	$(".form_datetime").datetimepicker({format: 'yyyy-mm-dd hh:ii',todayHighlight:true,todayBtn:true,autoclose:true});
	$("#myModal,#setting_time_modal").on("show.bs.modal",function(){$('body').scrollTop(0)});
	$("#main_panel #top_panel #Communications #form_communication_send").submit(function(){
		if($("#main_panel #top_panel #Communications #form_communication_send input#content").val()=="FROM:… TO:…"){
			alert("Please type something.");
			return false;
		}
		$("#main_panel #top_panel #Communications .panel-footer input#content").attr("disabled","disabled");
		$("#main_panel #top_panel #Communications .panel-footer button").attr("disabled","disabled");
		$.ajax({
			url: "/cheetah/datacontrol/communication/",
			data: {
				command:"PostSend",
				number:status_communication,
				system:$("#main_panel #top_panel #Communications #form_communication_send input#system").prop("checked"),
				content:$("#main_panel #top_panel #Communications #form_communication_send input#content").val(),
				csrfmiddlewaretoken:$("#main_panel #top_panel #Communications #form_communication_send [name='csrfmiddlewaretoken']").val()
			},
			success: function(data,status){
				if (data.result=="success"){
					$("#main_panel #top_panel #Communications #form_communication_send input#content").val("FROM:… TO:…");
					heartbeat_command=2;
					heartbeat();
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
					alert("成功执行");
					$("#form_communication_send_all *").removeAttr("disabled");
					$("#form_communication_send_all #content").val("");
					$('#communication_send_all_modal').modal('hide');
					heartbeat();
				}else{
					alert("发送失败："+data.result);
					$("#form_communication_send_all *").removeAttr("disabled");
				};
			},
			dataType: 'json',
			type: 'POST'
		});
		$("#form_communication_send_all *").attr("disabled","disabled");
		return false;
	});
	$("#main_panel #top_panel #Communications #block").click(function(){
		$.ajax({
			url: "/cheetah/datacontrol/communication/",
			data: {
				command:"PostBlock",
				number:status_communication,
				csrfmiddlewaretoken:$("#main_panel #top_panel #Communications #form_communication_send [name='csrfmiddlewaretoken']").val()
			},
			success: function(data,status){
				if (data.result=="success"){
					heartbeat_command=2;
					heartbeat();
				}else{
					alert("失败："+data.result);
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
					$("#form_meeting_send *").removeAttr("disabled");
					$("#form_meeting_send #location").val("");
					$("#form_meeting_send #description").val("");
					$('#myModal').modal('hide');
					$('#loaddialog').modal('show');
					heartbeat();
				}else{
					alert("发送失败："+data.result);
					$("#form_meeting_send *").removeAttr("disabled");
				};
			},
			dataType: 'json',
			type: 'POST'
		});
		$("#form_meeting_send *").attr("disabled","disabled");
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
					$("#form_setting_time *").removeAttr("disabled");
				};
			},
			dataType: 'json',
			type: 'POST'
		});
		$("#form_setting_time *").attr("disabled","disabled");
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
				$("#form_file_send *").attr("disabled","disabled");
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
				$("#form_meeting_send *").removeAttr("disabled");
				$("#form_file_send #upload_submit").html("Send");
			},
			error : function(data) {
				alert("上传发生错误！请刷新页面或联系我们。");
				$("#form_meeting_send *").removeAttr("disabled");
				$("#form_file_send #upload_submit").html("Send");
			},
			dataType :"json"
		});
		return false;
	});
	$("#control_sound").click(function(){
		control_sound=!control_sound;
		if (control_sound){
			$("#control_sound").html("关闭声音");
		}else{
			$("#control_sound").html("开启声音");
		};
	});
	startTime();
	$("#main_panel #top_panel #Communications .list-group a:first").click();
	if ($("#communication_list").parent().height()>$("#Communications .panel").height()){$("#Communications .panel .panel-body").css("height",$("#communication_list").parent().height()-121)};
	$("body").append('<audio id="chatAudio"><source src="/static/umunc_cheetah/sound/notify.mp3" type="audio/mpeg"><source src="/static/umunc_cheetah/sound/notify.wav" type="audio/wav"></audio>');
})

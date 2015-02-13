
$(function() {
	$("form  input,select,textarea").jqBootstrapValidation({submitError: function ($form, event, errors) {alert("提交失败！请检查是否存在非法输入！");}});
	tinymce.init({
		selector: "textarea#review_text",
		theme : 'modern',
		content_css: "http://libs.baidu.com/bootstrap/2.3.2/css/bootstrap.min.css",
		skin : 'xenmce',
		language : 'zh_CN',
		media_poster: false,
		media_alt_source: false,
		relative_urls : false,
		remove_script_host : false,
		document_base_url : "http://www.wmcyb.com/",
		plugins: [
			"advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker",
			"searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking",
			"save table directionality emoticons template paste textcolor",
			"autoresize"
		],
		menubar : false,
		toolbar:
			["fullscreen | undo redo cut copy paste | searchreplace |",
			"formatselect fontselect fontsizeselect bold italic underline strikethrough forecolor backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent visualblocks visualchars | subscript superscript removeformat table blockquote | hr charmap"],
		font_formats: 
			"宋体=宋体,SimSun;"+
			"微软雅黑=微软雅黑,Microsoft YaHei;"+
			"楷体=楷体,楷体_GB2312, SimKai;"+
			"黑体=黑体, SimHei;"+
			"隶书=隶书, SimLi;"+
			"andale mono=andale mono;"+
			"arial=arial, helvetica,sans-serif;"+
			"arial black=arial black,avant garde;"+
			"comic sans ms=comic sans ms;"+
			"impact=impact,chicago;"+
			"times new roman=times new roman;",
		style_formats: [
			{title: 'Bold text', inline: 'b'},
			{title: 'Red text', inline: 'span', styles: {color: '#ff0000'}},
			{title: 'Red header', block: 'h1', styles: {color: '#ff0000'}},
			{title: 'Example 1', inline: 'span', classes: 'example1'},
			{title: 'Example 2', inline: 'span', classes: 'example2'},
			{title: 'Table styles'},
			{title: 'Table row 1', selector: 'tr', classes: 'tablerow1'}
		]
	});
	$("form").submit(function(e){
		tinyMCE.activeEditor.save();
	});
	$("#submitbutton").click(function(){
		$("#submit").val("1");
		$("#savebutton").click();
	});
});
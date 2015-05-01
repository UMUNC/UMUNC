var editor
Array.prototype.S=String.fromCharCode(2);
Array.prototype.in_array=function(e){
	var r=new RegExp(this.S+e+this.S);
	return (r.test(this.S+this.join(this.S)+this.S));
};
function TagRename(id,name){
	$('#TagRenameModal #id').val(id)
	$('#TagRenameModal #name').val(name)
	$('#TagRenameModal').modal('show')
};
function TagDelete(id){
	$("#form_tag_delete #id").val(id);
	$('#TagDeleteModal').modal('show');
};
function PostEdit(id){
	$.getJSON("/dashboard?command=GetPost&id="+id,function(result){
		$("#form_post_editor #command").val("PostEdit");
		$("#form_post_editor #title").val(result.title);
		$("#form_post_editor #id").val(id);
		editor.setValue(result.content);
		$('input[type=checkbox]').each(function(){
			$(this).iCheck('uncheck');
			if (result.tags.in_array($(this).attr("name"))){
				$(this).iCheck('check');
			};
		});
	});
};
function PostCheck(id,handle){
	if (handle==0){
		$("#form_post_list #command").val("PostCheck_R");
	}else{
		$("#form_post_list #command").val("PostCheck_A");
	};
	$("#form_post_list #id").val(id);
	$("#form_post_list").submit();
};
function PostDelete(id){
	$("#form_post_delete #id").val(id);
	$('#PostDeleteModal').modal('show');
};


$(function(){
	// $.backstretch([
	// 	"/static/image/bg.jpg"
	// ], {
	// 	fade: 1000,
	// 	duration: 7000
	// });	
	$('[data-toggle="popover"]').popover()
	editor = new Simditor({
		textarea: $('#editor'),
		toolbar:[
					'title',
					'bold',
					'italic',
					'underline',
					'strikethrough',
					'color',
					'ol',
					'ul',
					'blockquote',
					'code',
					'table',
					'link',
					'image',
					'hr',
					'indent',
					'outdent',
					'source',
				],
		upload:{
			url: './',
			params: {
				command: "ImageUpdate",
				csrfmiddlewaretoken: $("#new_post [name='csrfmiddlewaretoken']").val()
			},
			fileKey: 'upload_file',
			connectionCount: 3,
			leaveConfirm: '正在上传文件，如果离开上传会自动取消'}
	});
	$('input[type=checkbox]').each(function(){
		var self = $(this),
			label = self.next(),
			label_text = label.text();

		label.remove();
		self.iCheck({
			checkboxClass: 'icheckbox_line-blue',
			radioClass: 'iradio_line-blue',
			insert: '<div class="icheck_line-icon"></div>' + label_text
		});
	});
	$("#form_post_editor").submit(function(){
		editor.sync();
	});
	$("#new_post_btn").click(function(){
		$("#form_post_editor #command").val("PostNew");
		$("#form_post_editor #title").val("");
		$("#form_post_editor #id").val(0);
		editor.setValue("");
		$('input[type=checkbox]').each(function(){
			$(this).iCheck('uncheck');
		});
	});
	$('#MSGModal').modal('show')
}) 

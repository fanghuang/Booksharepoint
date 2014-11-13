var rh = rh || {};
rh.book = rh.book || {};

rh.book.editing = false;

rh.book.addEventHandlers = function(){
	$("#insert-book-modal").on("shown.bs.modal", function(){
		$("input[name=isbn]").focus();
	});
};

rh.book.enableButtons = function() {	
	$("#toggle-edit").click(function() {
		if (rh.book.editing) {
			rh.book.editing = false;
			$(".edit-actions").addClass("hidden");
			$(this).html("Edit");
		} else {
			rh.book.editing = true;
			$(".edit-actions").removeClass("hidden");
			$(this).html("Done");
		}

	});

	$("#add-book").click(function() {
		$("#insert-book-modal .modal-title").html("Add a Book");
		$("#insert-book-modal button[type=submit]").html("Add Book");
		
		$("#insert-book-modal input[name=image-url]").val("");
		$("#insert-book-modal input[name=price]").val("");
		$("#insert-book-modal input[name=entity_key]").val("").prop("disabled", true);
	});

	
	$(".ownbooks").click(function() {
		var entityKey = $(this).find(".entity-key").html();
		var imageurl = $(this).find(".image-url").html().replace(/&amp;/g, '&');
		var isbn = $(this).find(".isbn").html();
		var title = $(this).find(".title").html();
		var author = $(this).find(".author").html();
		var price = $(this).find(".price").html();
		var condition = $(this).find(".condition").html();
		var dept = $(this).find(".dept-abbrev").html().toUpperCase();

		$("#edit-book-modal .btn.delete-book .entity-key").html(entityKey);
		$("#edit-book-modal #auto--img").attr("src", imageurl);
		$("#edit-book-modal input[name=image-url]").val(imageurl);
		$("#edit-book-modal input[name=isbn]").val(isbn);
		$("#edit-book-modal input[name=title]").val(title);
		$("#edit-book-modal input[name=author]").val(author);
		$("#edit-book-modal input[name=price]").val(price);
		$("#edit-book-modal select[name=dept-abbrev]").val(dept);
		$("#edit-book-modal input[name=entity_key]").val(entityKey);
		$("#edit-book-modal select[name=condition]").val(parseInt(condition));

	});

	$(".delete-book").click(function() {
		var entityKey = $(this).find(".entity-key").html();
		$("#delete-book-modal input[name=entity_key]").val(entityKey);
	});

	$("#send-email").click(function() {
		var email = $(this).find(".contact-email").html();
		var imageurl = $(this).find(".image-url").html().replace(/&amp;/g, '&');
		var isbn = $(this).find(".isbn").html();
		var title = $(this).find(".title").html();
		var author = $(this).find(".author").html();
		var price = $(this).find(".price").html();
		var condition = $(this).find(".condition").html();
		var dept = $(this).find(".dept-abbrev").html().toUpperCase();
		var data = {email_address : email, imageurl : imageurl,
		 isbn : isbn, title : title, author : author, price : price,
		 condition : condition, dept : dept};
		console.log(data);
		$.post("/api/v1/email", data).done(function(resp){
			console.log("success");
		}).fail(function(jqxhr, textStatus, error){
			console.log("PPPP failed withh status: " + textStatus + ", " + error);
		});

	});
};

$(document).ready(function() {
	rh.book.enableButtons();
	rh.book.addEventHandlers();
});

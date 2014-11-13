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

	$(".edit-book").click(function() {
		$("#insert-book-modal .modal-title").html("Edit this Book");
		$("#insert-book-modal button[type=submit]").html("Edit Book");
		
		image_url = $(this).find(".image-url").html();
		price = $(this).find(".price").html();
		entityKey = $(this).find(".entity-key").html();
		
		$("#insert-book-modal input[name=image-url]").val(image_url);
		$("#insert-book-modal input[name=price]").val(price);
		$("#insert-book-modal input[name=entity_key]").val(entityKey).prop("disabled", false);
	});
	
	$(".ownbooks").click(function(){
		entityKey = $(this).find(".entity-key").html();
		imageurl = $(this).find(".image-url").html();
		isbn = $(this).find(".isbn").html();
		title = $(this).find(".title").html();
		author = $(this).find(".author").html();
		price = $(this).find(".price").html();
		condition = $(this).find(".condition").html();
		dept = $(this).find(".dept-abbrev").html();

		$("#edit-book-modal .btn.delete-book .entity-key").html(entityKey);
		$("#edit-book-modal .entity-key").val(entityKey);
		$("#edit-book-modal #auto-img").attr('src', ''+imageurl);
		$("#edit-book-modal input[name=image-url]").val(imageurl);
		$("#edit-book-modal input[name=isbn]").val(isbn);
		$("#edit-book-modal input[name=title]").val(title);
		$("#edit-book-modal input[name=author]").val(author);
		$("#edit-book-modal input[name=price]").val(price);
		$("#edit-book-modal input[name=condition]").val(condition);
		$("#edit-book-modal input[name=dept-abbrev]").val(dept);

	});

	$(".delete-book").click(function() {
		entityKey = $(this).find(".entity-key").html();
		$("#delete-book-modal input[name=entity_key]").val(entityKey);
	});
};

$(document).ready(function() {
	rh.book.enableButtons();
	rh.book.addEventHandlers();
});

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
	
	$(".delete-book").click(function() {
		entityKey = $(this).find(".entity-key").html();
		$("#delete-book-modal input[name=entity_key]").val(entityKey);
	});
};

$(document).ready(function() {
	rh.book.enableButtons();
	rh.book.addEventHandlers();
});

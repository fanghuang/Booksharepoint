var rh = rh || {};
rh.book = rh.book || {};

rh.book.editing = false;

rh.book.getBookByISBN = function(isbn, success_func, fail_func) {
	var url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn;
	$.getJSON(url).done(function(data) {
		success_func(data);
	}).fail(fail_func);
};


rh.book.enableSideNavBar = function() {
	$("#sidebar .list-group a").on("click", function() {
		$("#sidebar .list-group a").removeClass("active");
		$(this).addClass("active");

		$("#columns .pin").addClass("hidden");

		var dept = $(this).html().toLowerCase();
		rh.book.showBooksByDept(dept);

	});

	$($("#sidebar .list-group a").get(0)).on("click", function() {
		rh.book.showBooksByDept("*");
	});
};

rh.book.limitTextInput = function() {
	$(".isbn-input").keypress(function(e) {
		var chr = String.fromCharCode(e.which);
		return "1234567890".indexOf(chr) >= 0;
	});

	$(".price-input").keypress(function(e) {
		var chr = String.fromCharCode(e.which);
		return "1234567890.".indexOf(chr) >= 0;
	});

};


rh.book.addEventHandlers = function(){
	$("#insert-book-modal").on("shown.bs.modal", function(){
		$("input[name=isbn]").focus();
	});
	
	$('input[name="isbn"]').on(
			'input',
			function() {
				var isbn = $(this).val();
				if (isbn.length == 10 || isbn.length == 13) {
					rh.book.getBookByISBN(isbn, function(volumes) {
						console.log("book_info_request");
						if (volumes.totalItems > 0) {
							var books = volumes.items;

							var book = books[0];

							var book_info = book.volumeInfo;
							var book_title = book_info.title;
							$('#auto-title').val(book_title);

							var book_authors = book_info.authors;
							$('#auto-author').val(
									book_authors.toString().replace(/\s*,\s*/g,
											', '));

							var book_images = book_info.imageLinks;
							var book_thumbnail = book_images.thumbnail;
							book_thumbnail = book_thumbnail.replace(
									/&edge=curl/g, '');

							$('#auto-img').attr('src', book_thumbnail);
							$('#auto-img-src').val(book_thumbnail);
							// var book_obj = {title: book_title, author:
							// book_authors, img_url: book_thumbnail};

						}

					}, function() {
						console.log("failure");
					});
				} else {
					$('#auto-img').attr('src', '');
					$('#auto-img-src').val('');
					$('#auto-title').val('');
					$('#auto-author').val('');
				}
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
		$("#edit-book-modal #auto-img").attr("src", imageurl);
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
	
	
	$(".cart-btn").click(function() {
		var btnIndex = $(".cart-btn").index(this);
		$($('.cart-btn').get(btnIndex)).toggleClass('in-cart');
	});
};


rh.book.showBooksByDept = function(dept) {
	if (dept == "*") {
		$("#columns .pin").removeClass("hidden");
	} else if (dept) {
		$("#columns .pin." + dept).removeClass("hidden");
	}
};


/** main **/
$(document).ready(function() {
	rh.book.enableSideNavBar();
	rh.book.addEventHandlers();
	rh.book.limitTextInput();
	rh.book.enableButtons();
	
	rh.book.showBooksByDept("*");
});

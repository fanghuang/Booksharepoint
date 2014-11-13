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

	
	$(".ownbooks").click(function(){
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
	
	
	$(".cart-btn").click(function() {
		// Get the correct button
		var btnIndex = $(".cart-btn").index(this);
		var $btn = $($('.cart-btn').get(btnIndex));
		$btn.toggleClass('in-cart');
		
		// Get the key for the current book
		var book_key = $btn.find(".entity-key").html();
		
		// AJAX to add to cart
		var data = {entity_key : book_key};
		if ($btn.hasClass("in-cart")) {
			rh.book.addToCart(data);
		} else {
			rh.book.removeFromCart(data);
		}
		
	});
};

rh.book.addToCart = function(data) {
	$.post('/addtocart', data).done(function(resp) {
		// Update the label in the user drop form
		var $cart_counter = $("#cart-counter");
		var amt_in_cart = parseInt($cart_counter.html());
		$cart_counter.html(amt_in_cart + 1);
	}).fail(function(jqxhr, textStatus, error) {
		console.log("POST action Add to Cart failed");
		console.log(textStatus + " ");
	});
};

rh.book.removeFromCart = function(data) {
	$.post('/removefromcart', data).done(function(resp) {
		// Update the label in the user drop form
		var $cart_counter = $("#cart-counter");
		var amt_in_cart = parseInt($cart_counter.html());
		$cart_counter.html(amt_in_cart - 1);
	}).fail(function(jqxhr, textStatus, error) {
		console.log("POST action Remove from Cart failed");
		console.log(textStatus + " ");
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
	
	// Show all the books
	rh.book.showBooksByDept("*");
});

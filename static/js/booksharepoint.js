var rh = rh || {};
rh.book = rh.book || {};

rh.book.getBookByISBN = function(isbn, success_func, fail_func) {
	var url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn;
	$.getJSON(url).done(function(data) {
		success_func(data);
	}).fail(fail_func);
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

rh.book.showBooksByDept = function(dept) {
	if (dept == "*") {
		$("#columns .pin").removeClass("hidden");
	} else if (dept) {
		$("#columns .pin." + dept).removeClass("hidden");
	}
};

rh.book.hookBookAutoComplete = function() {
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
}

/** main * */
$(document).ready(function() {
	rh.book.enableSideNavBar();
	rh.book.limitTextInput();
	rh.book.hookBookAutoComplete();
	rh.book.showBooksByDept("*");
});

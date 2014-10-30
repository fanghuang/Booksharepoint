var rh = rh || {};
rh.book = rh.book || {};

rh.book.getBookByISBN = function(isbn, success_func, fail_func) {
  var url='https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn;
  $.getJSON(url)
    .done(function(data){
       success_func(data);
    }).fail(fail_func);
};
    
rh.book.limitTextInput = function() {
	$(".isbn-input").keypress( function(e) {
	      var chr = String.fromCharCode(e.which);
	      return "1234567890".indexOf(chr) >= 0;
	    });
	    
	    $(".price-input").keypress( function(e) {
	      var chr = String.fromCharCode(e.which);
	      return "1234567890.".indexOf(chr) >= 0;
	    });
};

rh.book.enableSideNavBar = function() {
	$("#sidebar .list-group a").on("click",function() {
		$("#sidebar .list-group a").removeClass("active");
		$(this).addClass("active");
	});
};

/** main **/
$(document).ready(function() {
	rh.book.enableSideNavBar();
	rh.book.limitTextInput();
});

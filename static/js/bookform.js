var rh = rh || {};
rh.book = rh.book || {};

rh.book.get_book_by_isbn = function(isbn, success_func, fail_func) {
  var url='https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn;
  $.getJSON(url)
    .done(function(data){
       success_func(data);
    }).fail(fail_func);
};
    
$(document).ready(function() {

    $(".isbn-input").keypress( function(e) {
      var chr = String.fromCharCode(e.which);
      return "1234567890".indexOf(chr) >= 0;
    });
    
    $(".price-input").keypress( function(e) {
      var chr = String.fromCharCode(e.which);
      return "1234567890.".indexOf(chr) >= 0;
    });
    
    $('input[name="input_isbn"]').on('input', function() {
        var isbn = $(this).val();
        if (isbn.length == 10 || isbn.length == 13) {
           rh.book.get_book_by_isbn(isbn,  
              function(volumes) {
                console.log("book_info_request");
                if (volumes.totalItems > 0) {
                  var books = volumes.items;
                  
                  var book = books[0];
                  
                  var book_info = book.volumeInfo;
                  var book_title = book_info.title;
                  $('#auto-title').text(book_title);
                  
                  var book_authors = book_info.authors;
                  $('#auto-author').text(book_authors);
                  
                  var book_images = book_info.imageLinks;
                  var book_thumbnail = book_images.thumbnail;
                  book_thumbnail = book_thumbnail.replace(/&edge=curl/g, '');
                  
                  $('#auto-img').attr('src', book_thumbnail);
                  // var book_obj = {title: book_title, author: book_authors, img_url: book_thumbnail};
                  
                }
                
              }, function() {
                console.log("failure");
              });
        } else {
           $('#auto-img').attr('src', '#');
           $('#auto-title').text('(none)');
           $('#auto-author').text('(none)');
        }
    });
});

import urllib2
import json, logging

def get_book_details(isbn):
    """ Wrapper for getting book information """
    
    def get_details_by_isbn(isbn):
        """ Calls Google Books API to get JSON for the given ISBN """
        
#         base_url = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
        data = None
        try:
            resp = urllib2.urlopen('https://www.googleapis.com/books/v1/volumes?q=isbn:'+ isbn)
            data = json.load(resp)
            logging.info(data)
        except urllib2.URLError, e:
            logging.error(e)
        return data
        
    info_dict = {}
    book_json = get_details_by_isbn(isbn)
    print book_json
    
    if book_json and book_json["totalItems"] > 0:
        books = book_json["items"]
        
        book = books[0]
        
        book_info =  book["volumeInfo"]
        book_title = book_info["title"]
        
        book_authors = book_info["authors"]
        authors = []
        for a in book_authors:
            authors.append(str(a))
        
        book_description = book_info["description"].encode("utf-8")
        
        book_images = book_info["imageLinks"]
        book_thumbnail = book_images["thumbnail"]
        book_thumbnail = book_thumbnail.replace("&edge=curl", "")
        
        info_dict["title"] = str(book_title)
        info_dict["authors"] = authors
        info_dict["description"] = str(book_description)
        info_dict["image_url"] = str(book_thumbnail) 
        return json.dumps(info_dict)
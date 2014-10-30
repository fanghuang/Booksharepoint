import requests

def get_book_details(isbn):
    """ Wrapper for getting book information """
    
    def get_details_by_isbn(isbn):
        """ Calls Google Books API to get JSON for the given ISBN """
        
        base_url = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
        r = requests.get(base_url + isbn)
        if (r.status_code == 200):
            return r.json()
        else:
            return None
        
    info_dict = {}
    book_json = get_details_by_isbn('978144930')
    print book_json
    
    if book_json["totalItems"] > 0:
        books = book_json["items"]
        
        book = books[0]
        
        book_info =  book["volumeInfo"]
        book_title = book_info["title"]
        
        book_authors = book_info["authors"]
        authors = []
        for a in book_authors:
            authors.append(str(a))
        
        book_description = book_info["description"]
        
        book_images = book_info["imageLinks"]
        book_thumbnail = book_images["thumbnail"]
        book_thumbnail = book_thumbnail.replace("&edge=curl", "")
        
        info_dict["title"] = str(book_title)
        info_dict["authors"] = authors
        info_dict["description"] = str(book_description)
        info_dict["image_url"] = str(book_thumbnail) 
        return info_dict
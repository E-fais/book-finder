import ttkbootstrap as ttk
from ttkbootstrap.constants import*
import requests
import json

root=ttk.Window(themename='morph')
root.title('Library')
root.iconbitmap('./assets/logo.ico')


query=input('book name').replace(' ','+')
query='inferno' #change to user input
BASE_URL=f"https://openlibrary.org/search.json?q={query}"
try:
    res=requests.get(BASE_URL).content
    res_data=json.loads(res)['docs']
    cover_key=res_data[0]["cover_edition_key"]
 
 #fetch new url for additional details
    work_response=requests.get(f"https://openlibrary.org/works/{cover_key}.json").content
    work_data=json.loads(work_response)

#infos to show user
    first_published_year=res_data[0]['first_publish_year']
    author_name=res_data[0]['author_name'][0]
    author_key=res_data[1]['author_key'][0]
    author_img_url=f"https://covers.openlibrary.org/a/olid/{author_key}.jpg"
    cover_img_url=f"https://covers.openlibrary.org/b/olid/{cover_key}-L.jpg"
    no_of_pages=work_data['number_of_pages']
    publish_date=work_data["publish_date"]



    
   
except Exception as err:
    print(err)   


# root.mainloop()

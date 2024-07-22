import ttkbootstrap as ttk
from ttkbootstrap.constants import*
import requests
import json

root=ttk.Window(themename='darkly')
root.title('Book Finder')
root.iconbitmap('./assets/logo.ico')
from PIL import Image,ImageTk

def get_book():
    query=entry.get()
    print(query)
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


frame=ttk.LabelFrame(root,padding=(10,10))
frame.pack(padx=100,pady=70)

logo_img=ImageTk.PhotoImage(Image.open('./assets/book.ico'))
logo_img_label=ttk.Label(frame,image=logo_img)
header=ttk.Label(frame,bootstyle='info',text="Book Finder",font=('helvetica',16))
sub_header=ttk.Label(frame,bootstyle='success',text='Search Your Favourite Books!',font=('helvetica',10,'bold'))
entry=ttk.Entry(frame,bootstyle="info",width=30,font=(12))
search_btn=ttk.Button(frame,bootstyle='info',text='Find Book',width=44,command=get_book)

header.grid(row=0,column=0,padx=10)
sub_header.grid(row=1,column=0,padx=10)
logo_img_label.grid(row=2,column=0,padx=10)
entry.grid(row=3,column=0,padx=10)
search_btn.grid(row=4,column=0,pady=20)


root.mainloop()

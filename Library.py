import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.constants import*
import requests
import json
from io import BytesIO

root=ttk.Window(themename='darkly')
root.title('Book Finder')
root.iconbitmap('./assets/logo.ico')
from PIL import Image,ImageTk

def get_book():
    query=entry.get()
    info_label.config(text=f'Searching for {query}...')
    if query=='':
       messagebox.showwarning('No input','Please type a book name')
    BASE_URL=f"https://openlibrary.org/search.json?q={query}"
    try:
        res=requests.get(BASE_URL).content
        res_data=json.loads(res)['docs']
        if res_data[0]["cover_edition_key"]:
          #fetch new url for additional details
          cover_key=res_data[0]["cover_edition_key"]
          work_response=requests.get(f"https://openlibrary.org/works/{cover_key}.json").content
 

        if requests.get(BASE_URL).status_code!=200:
           messagebox.showerror('Conection Error','Cannot connect to server')
        else:
          work_data=json.loads(work_response)
#infos to show user
        if work_data:
            first_published_year=res_data[0]['first_publish_year']
            author_name=res_data[0]['author_name'][0]

            author_key=res_data[0]['author_key'][0]

            author_img_url=f"https://covers.openlibrary.org/a/olid/{author_key}.jpg"
            cover_img_url=f"https://covers.openlibrary.org/b/olid/{cover_key}-M.jpg"
            no_of_pages=work_data['number_of_pages']
            publish_date=work_data["publish_date"]

            info_label.config(text='')
            
            #display result in new window
            result_window=ttk.Toplevel()
            result_window.title(query)
            result_frame = ttk.Frame(result_window, padding=(10, 10))
            result_frame.grid(row=0, column=0, sticky='nsew')
            book_name_label=ttk.Label(result_frame,text=query.upper(),font=('helvetica',13))
            book_name_label.grid(row=0,column=0)

            if cover_img_url:
                cover_img_data = requests.get(cover_img_url).content
                book_cover = ImageTk.PhotoImage(Image.open(BytesIO(cover_img_data)))
                book_cover_label = ttk.Label(result_frame, image=book_cover,padding=(25,25))
                book_cover_label.image = book_cover  # Keep a reference to avoid garbage collection
                book_cover_label.grid(row=3, column=0)

            # if author_img_url:
            #     author_img_data = requests.get(author_img_url).content
            #     author_image = ImageTk.PhotoImage(Image.open(BytesIO(author_img_data)))
            #     author_img_label = ttk.Label(result_frame, image=author_image,padding=(5,5))
            #     author_img_label.image = author_image  # Keep a reference to avoid garbage collection
            #     author_img_label.grid(row=4, column=0)

            if author_name:
                author_name_lable=ttk.Label(result_frame,text=f'Author : {author_name}',font=('helvetica',13),padding=(5,5))
                author_name_lable.grid(row=1,column=0)
           
            if no_of_pages:
                   no_of_pages_label=ttk.Label(result_frame,text=f'No of pages : {no_of_pages}',font=('helvetica',13))
                   no_of_pages_label.grid(row=5,column=0)
            if publish_date:
                      publish_date_label=ttk.Label(result_frame,text=f'Current Publish : {publish_date}',font=('helvetica',13))
                      publish_date_label.grid(row=2,column=0)
            if publish_date:
                    first_published_label=ttk.Label(result_frame,text=f'First published : {first_published_year}',font=('helvetica',13),padding=(10,5))
                    first_published_label.grid(row=6,column=0)
            ttk.Button(result_frame,text="Back",bootstyle='secondary',width=30,command=result_window.destroy).grid(row=7,column=0)


            
        else:
           messagebox.showinfo('Book Not Found','Book not found in Open Library!')
    except Exception as err:
       print(f'Error: {err}')
       info_label.config(text="Cannot fetch data")
     
frame=ttk.LabelFrame(root,padding=(10,10))
frame.pack(padx=100,pady=70)

logo_img=ImageTk.PhotoImage(Image.open('./assets/book.ico'))
logo_img_label=ttk.Label(frame,image=logo_img)
header=ttk.Label(frame,bootstyle='info',text="Book Finder",font=('helvetica',13))
sub_header=ttk.Label(frame,bootstyle='success',text='Search Your Favourite Books!',font=('helvetica',10,'bold'))
entry=ttk.Entry(frame,bootstyle="info",width=30,font=(12))
search_btn=ttk.Button(frame,bootstyle='info',text='Find Book',width=44,command=get_book)
info_label=ttk.Label(frame,text='')

header.grid(row=0,column=0,padx=10)
sub_header.grid(row=1,column=0,padx=10)
logo_img_label.grid(row=2,column=0,padx=10)
entry.grid(row=3,column=0,padx=10)
search_btn.grid(row=4,column=0,pady=20)
info_label.grid(row=5,column=0)


root.mainloop()

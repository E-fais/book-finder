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
    query = entry.get()
    info_label.config(text=f'Searching for {query}...')
    if query == '':
        messagebox.showwarning('No input', 'Please type a book name')
        return

    BASE_URL = f"https://openlibrary.org/search.json?q={query}"
    try:
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            messagebox.showerror('Connection Error', 'Cannot connect to server')
            return

        res_data = json.loads(response.content)['docs']
        if not res_data:
            messagebox.showinfo('Book Not Found', 'Book not found in Open Library!')
            info_label.config(text='')
            entry.delete(0,END)
            return

        if "cover_edition_key" not in res_data[0]:
            messagebox.showinfo('Book Not Found', 'Book cover not found in Open Library!')
            return

        cover_key = res_data[0]["cover_edition_key"]
        work_response = requests.get(f"https://openlibrary.org/works/{cover_key}.json").content
        work_data = json.loads(work_response)

        # Infos to show user
        if work_data:
            first_published_year = res_data[0].get('first_publish_year', 'Unknown')
            author_name = res_data[0].get('author_name', ['Unknown'])[0]
            author_key = res_data[0].get('author_key', ['Unknown'])[0]
            author_img_url = f"https://covers.openlibrary.org/a/olid/{author_key}.jpg"
            cover_img_url = f"https://covers.openlibrary.org/b/olid/{cover_key}-M.jpg"
            no_of_pages = work_data.get('number_of_pages', 'Unknown')
            publish_date = work_data.get("publish_date", 'Unknown')

            info_label.config(text='')

            # Display result in new window
            result_window = ttk.Toplevel()
            result_window.title(query)
            result_frame = ttk.Frame(result_window, padding=(10, 10))
            result_frame.grid(row=0, column=0, sticky='nsew')
            book_name_label = ttk.Label(result_frame, text=query.upper(), font=('helvetica', 13))
            book_name_label.grid(row=0, column=0)

            if cover_img_url:
                cover_img_data = requests.get(cover_img_url).content
                book_cover = ImageTk.PhotoImage(Image.open(BytesIO(cover_img_data)))
                book_cover_label = ttk.Label(result_frame, image=book_cover, padding=(25, 25))
                book_cover_label.image = book_cover  # Keep a reference to avoid garbage collection
                book_cover_label.grid(row=3, column=0)

            if author_name:
                author_name_label = ttk.Label(result_frame, text=f'Author: {author_name}', font=('helvetica', 13), padding=(5, 5))
                author_name_label.grid(row=1, column=0)

            if no_of_pages:
                no_of_pages_label = ttk.Label(result_frame, text=f'No of pages: {no_of_pages}', font=('helvetica', 13))
                no_of_pages_label.grid(row=5, column=0)

            if publish_date:
                publish_date_label = ttk.Label(result_frame, text=f'Current Publish: {publish_date}', font=('helvetica', 13))
                publish_date_label.grid(row=2, column=0)

            if first_published_year:
                first_published_label = ttk.Label(result_frame, text=f'First published: {first_published_year}', font=('helvetica', 13), padding=(10, 5))
                first_published_label.grid(row=6, column=0)

            ttk.Button(result_frame, text="Back", bootstyle='secondary', width=30, command=result_window.destroy).grid(row=7, column=0)

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

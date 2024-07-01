from tkinter import Tk
from pathlib import Path
from tkinter import Canvas,Button, PhotoImage,Label
from tkinter import filedialog
import cv2
import torch
from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, scale_coords
from utils.plots import plot_one_box
from utils.torch_utils import select_device, time_synchronized
import sqlite3
import os
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Frame, Label,messagebox
import sqlite3
import os
from PIL import Image, ImageTk, ImageDraw

def detect(weights=r'.\best.pt', source='', img_size=640, conf_thres=0.8, iou_thres=0.45, device='', classes=None, agnostic_nms=False):
    source, weights, imgsz = source, weights, img_size
    save_img = False  
    device = select_device(device)
    model = attempt_load(weights, map_location=device)
    stride = int(model.stride.max())  
    imgsz = check_img_size(imgsz, s=stride)  
    dataset = LoadImages(source, img_size=imgsz, stride=stride)
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.float()  
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        t1 = time_synchronized()
        with torch.no_grad():
            pred = model(img)[0]
        t2 = time_synchronized()
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=classes, agnostic=agnostic_nms)
        for i, det in enumerate(pred):
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  
                    print(f'{n} Brain{"s" * (n > 1)}')
                for *xyxy, conf, cls in det:
                    if conf >= 0.6:  
                        label = f'Brain {conf:.2f}'
                        plot_one_box(xyxy, im0s, label=label, color=(255,5,5), line_thickness=1)
        return Image.fromarray(cv2.cvtColor(im0s, cv2.COLOR_BGR2RGB))
def upload_file():
    global result_image
    file_path = filedialog.askopenfilename()
    result_image = detect(weights='./best.pt', source=file_path, img_size=640, conf_thres=0.1, iou_thres=0.45, device='', classes=None, agnostic_nms=False)
    image = result_image
    image.thumbnail((350, 350))
    image = image.resize((350,350))
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo
    c.execute("INSERT INTO images (path) VALUES (?)", (file_path,))
    conn.commit()
def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    if file_path:
        result_image.save(file_path) 
def Home(window):
    def relative_to_assets(path: str) -> Path:
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\frame0")
        return ASSETS_PATH / Path(path)
    global conn,c,image_image_1, image_image_2, button_image_1, button_image_2, button_image_3, button_image_4, button_image_5,button_image_6,button_image_7,image_label
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, path TEXT)''')
    conn.commit()
    def Change(Text):
        global current_window
        if Text == "home":
            home_button()
            current_window=window
        elif Text == "about":
            about_button()
            current_window=About(window)
        elif Text == "project":
            project_button()
            current_window=Project(window)
    def home_button():
        print("home_button button clicked")
        canvas.itemconfig(page_navigator, text="")
    def project_button():
        print("project_button button clicked")
        canvas.itemconfig(page_navigator, text="project")
    def about_button():
        print("About button clicked")
        canvas.itemconfig(page_navigator, text="About")
    def on_click(event, txt):
        if(txt == "exit"):
            window.destroy()
        elif(txt == "open"):
            upload_file()
        elif(txt == "save"):
            save_image()
        elif(txt == "delete"):
            image_label.config(image=None)
            image_label.image = None

        Change(txt)
        return "break"
    def on_enter(event, txt):
        window.config(cursor="hand2")
    def on_leave(event):
        window.config(cursor="arrow")
    canvas = Canvas(
        window,
        bg = "#F7F7F7",
        height = 467,
        width = 743,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)
    page_navigator = canvas.create_text(
        251.0,
        37.0,
        anchor="nw",
        text="",
        fill="#171435",
        font=("Montserrat Bold", 26 * -1)
    )
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        109.0,
        233.0,
        image=image_image_1
    )
    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        96.41600036621094,
        68.05867004394531,
        image=image_image_2
    )
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    button_1.place(
        x=11.0,
        y=172.0,
        width=156.0,
        height=37.0
    )
    button_1.bind("<Enter>", lambda event: on_enter(event, "Mouse over Home button"))
    button_1.bind("<Leave>", on_leave)
    button_1.bind("<ButtonPress>", lambda event: on_click(event, "home"))
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    button_2.bind("<Enter>", lambda event: on_enter(event, ""))
    button_2.bind("<Leave>", on_leave)
    button_2.bind("<ButtonPress>", lambda event: on_click(event, "open"))
    button_2.place(
        x=389.0,
        y=386.0,
        width=87.0,
        height=32.378665924072266
    )
    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    button_3.place(
        x=487.0,
        y=386.0,
        width=87.0,
        height=32.378665924072266
    )
    button_3.bind("<Enter>", lambda event: on_enter(event, "Mouse over Home button"))
    button_3.bind("<Leave>", on_leave)
    button_3.bind("<ButtonPress>", lambda event: on_click(event, "save"))
    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    button_4.place(
        x=389.0,
        y=424.0,
        width=185.0,
        height=32.378665924072266
    )
    button_4.bind("<Enter>", lambda event: on_enter(event, "Mouse over Home button"))
    button_4.bind("<Leave>", on_leave)
    button_4.bind("<ButtonPress>", lambda event: on_click(event, "delete"))
    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    button_5.place(
        x=20.0,
        y=221.0,
        width=124.0,
        height=25.0
    )
    button_5.bind("<Enter>", lambda event: on_enter(event, "Mouse over Project button"))
    button_5.bind("<Leave>", on_leave)
    button_5.bind("<ButtonPress>", lambda event: on_click(event, "project"))
    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    button_6.bind("<Enter>", lambda event: on_enter(event, "Mouse over About button"))
    button_6.bind("<Leave>", on_leave)
    button_6.bind("<ButtonPress>", lambda event: on_click(event, "about"))
    button_6.place(
        x=20.0,
        y=264.0,
        width=124.0,
        height=26.0
    )
    button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    button_7 = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    button_7.bind("<Enter>", lambda event: on_enter(event, "Mouse over Button 4"))
    button_7.bind("<Leave>", on_leave)
    button_7.bind("<ButtonPress>", lambda event: on_click(event, "exit"))
    button_7.place(
        x=17.0,
        y=436.0,
        width=130.0,
        height=26.0
    )
    image_label = Label(window)
    image_label.place(x = 307 , y = 20)
def About(window):
    global image_image_1,image_image_2,image_image_3,image_image_4,image_image_5,button_image_1,button_image_2,button_image_3,button_image_4,button_image_5
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\frame2")
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    def Change(Text):
        global current_window
        if Text == "home":
            home_button()
            current_window=Home(window)
        elif Text == "project":
            project_button()
            current_window=Project(window)
    def home_button():
        print("home_button button clicked")
        canvas.itemconfig(page_navigator, text="")

    def project_button():
        print("project_button button clicked")
        canvas.itemconfig(page_navigator, text="project")

    def on_click(event, txt):
        if(txt == "exit"):
            window.destroy()
        elif(txt == "open"):
            upload_file()
        elif(txt == "save"):
            save_image()
        elif(txt == "delete"):
            image_label.config(image=None)
            image_label.image = None
        Change(txt)
        return "break"
    def on_enter(event, txt):
        window.config(cursor="hand2")
    def on_leave(event):
        window.config(cursor="arrow")

    
    canvas = Canvas(
        window,
        bg = "#F7F7F7",
        height = 467,
        width = 742,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    page_navigator = canvas.create_text(
        251.0,
        37.0,
        anchor="nw",
        text="",
        fill="#171435",
        font=("Montserrat Bold", 26 * -1)
    )
    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        109.0,
        233.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        96.416015625,
        68.05865478515625,
        image=image_image_2
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=10.0,
        y=172.0,
        width=158.0,
        height=37.0
    )

    button_1.bind("<Enter>", lambda event: on_enter(event, "Mouse over Home button"))
    button_1.bind("<Leave>", on_leave)
    button_1.bind("<ButtonPress>", lambda event: on_click(event, "home"))

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_2 clicked"),
        relief="flat"
    )
    button_2.place(
        x=12.0,
        y=216.0,
        width=154.0,
        height=36.0
    )
    button_2.bind("<Enter>", lambda event: on_enter(event, "Mouse over Project button"))
    button_2.bind("<Leave>", on_leave)
    button_2.bind("<ButtonPress>", lambda event: on_click(event, "project"))

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_3 clicked"),
        relief="flat"
    )
    button_3.place(
        x=11.0,
        y=260.0,
        width=156.0,
        height=36.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4 clicked"),
        relief="flat"
    )
    button_4.place(
        x=27.0,
        y=436.0,
        width=110.0,
        height=26.0
    )
    button_4.bind("<Enter>", lambda event: on_enter(event, "Mouse over Button 4"))
    button_4.bind("<Leave>", on_leave)
    button_4.bind("<ButtonPress>", lambda event: on_click(event, "exit"))
    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        481.0,
        39.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        480.0,
        234.0,
        image=image_image_4
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_5 clicked"),
        relief="flat"
    )
    button_5.place(
        x=428.0,
        y=436.0,
        width=107.0,
        height=23.0
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        481.0,
        422.0,
        image=image_image_5
    )
def round_corners(pil_img, radius):
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
    alpha = Image.new('L', pil_img.size, 255)
    w, h = pil_img.size
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
    pil_img.putalpha(alpha)
    return pil_img
def delete_all_images(window):
    response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete all images?")
    if response:
        c.execute("DELETE FROM images")
        conn.commit()
        messagebox.showinfo("Success", "All images have been deleted.")
        Project(window)
def Project(window):
    global image_image_1,conn,c, image_image_2, button_image_1, button_image_2, button_image_3, button_image_4, button_image_5
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, path TEXT)''')
    conn.commit()
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\frame1")
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    def Change(Text):
        global current_window
        if Text == "home":
            home_button()
            current_window=Home(window)
        elif Text == "about":
            about_button()
            current_window=About(window)
        elif Text == "project":
            project_button()
            current_window=Project(window)
    def home_button():
        canvas.itemconfig(page_navigator, text="")
    def project_button():
        canvas.itemconfig(page_navigator, text="project")
    def about_button():
        canvas.itemconfig(page_navigator, text="About")
    def on_click(event, txt):
        if(txt == "exit"):
            window.destroy()
        Change(txt)
        return "break"
    def on_enter(event, txt):
        window.config(cursor="hand2")
    def on_leave(event):
        window.config(cursor="arrow")
    for widget in window.winfo_children():
        widget.destroy()
    c.execute("SELECT path FROM images")
    image_paths = c.fetchall()
    canvas = Canvas(window, bg="#F7F7F7", height=467, width=743, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    page_navigator = canvas.create_text(
            251.0,
            37.0,
            anchor="nw",
            text="",
            fill="#171435",
            font=("Montserrat Bold", 26 * -1)
        )
    frame = Frame(canvas,bg="#F7F7F7")
    canvas.create_window((210, 38), window=frame, anchor="nw")
    row = 0
    col = 0
    for image_path in image_paths:
        if os.path.exists(image_path[0]):
            img = Image.open(image_path[0])
            img = img.resize((113, 113))
            img = img.convert("RGBA")
            img_with_rounded_corners = round_corners(img, radius=20)
            img = ImageTk.PhotoImage(img_with_rounded_corners)
            panel = Label(frame, image=img)
            panel.image = img
            panel.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col == 4:
                row += 1
                col = 0
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(109.0, 233.0, image=image_image_1)
    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(96.416, 68.059, image=image_image_2)
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: print("button_1 clicked"), relief="flat")
    button_1.place(x=14.0, y=174.0, width=150.0, height=35.0)
    button_1.bind("<Enter>", lambda event: on_enter(event, "Mouse over Home button"))
    button_1.bind("<Leave>", on_leave)
    button_1.bind("<ButtonPress>", lambda event: on_click(event, "home"))
    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: print("button_2 clicked"), relief="flat")
    button_2.place(x=6.0, y=216.0, width=166.0, height=36.0)
    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: print("button_3 clicked"), relief="flat")
    button_3.place(x=13.699, y=261.52, width=150.685, height=32.379)
    button_3.bind("<Enter>", lambda event: on_enter(event, "Mouse over about button"))
    button_3.bind("<Leave>", on_leave)
    button_3.bind("<ButtonPress>", lambda event: on_click(event, "about"))
    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: print("button_4 clicked"), relief="flat")
    button_4.place(x=21.0, y=436.0, width=122.0, height=27.0)
    button_4.bind("<Enter>", lambda event: on_enter(event, "Mouse over Button 4"))
    button_4.bind("<Leave>", on_leave)
    button_4.bind("<ButtonPress>", lambda event: on_click(event, "exit"))
    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(image=button_image_5, borderwidth=0, highlightthickness=0, command=lambda: delete_all_images(window), relief="flat")
    button_5.place(x=389.0, y=424.0, width=185.0, height=32.379)
window = Tk()
window.geometry("743x467")
window.configure(bg = "#F7F7F7")
Home(window)
window.resizable(False, False)
window.mainloop()
import tkinter as tk

def toggle_card_visibility():
    global show_card
    show_card = 1
    show_card = not show_card
    if show_card:
        card_number_var.set("1233 3143 3343 3434")
        eye_btn.config(text="👁️")
    else:
        card_number_var.set("**** **** **** ****")
        eye_btn.config(text="🙈")

root = tk.Tk()
root.title("Account Overview")
root.geometry("960x600")
root.minsize(800, 500)
root.configure(bg="#ecf0f3")

main_frame = tk.Frame(root, bg="#ecf0f3")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)

content_frame = tk.Frame(main_frame, bg="#ecf0f3")
content_frame.grid(row=1, column=0, sticky="nsew")
content_frame.columnconfigure((0, 1), weight=1)
content_frame.rowconfigure(0, weight=1)

card_container = tk.Frame(content_frame, bg="#ecf0f3")
card_container.grid(row=0, column=0, sticky="n", padx=(0, 20), pady=10)

card_frame = tk.Frame(card_container, bg="#1e1e1e", width=420, height=220, bd=2, relief="solid")
card_frame.pack()
card_frame.pack_propagate(0)

tk.Label(card_frame, text="VISA", bg="#1e1e1e", fg="white",
         font=("Courier New", 20, "bold")).pack(anchor="ne", padx=20, pady=(15, 5))

card_number_var = tk.StringVar(value="1233 3143 3343 3434")
show_card = True

card_number_container = tk.Frame(card_frame, bg="#1e1e1e")
card_number_container.pack(fill="x", padx=20)

card_number_container.columnconfigure(0, weight=1)
card_number_container.columnconfigure(1, minsize=40)

card_number_label = tk.Label(card_number_container, textvariable=card_number_var,
                             bg="#1e1e1e", fg="white", font=("Courier New", 20, 'bold'), anchor="w")
card_number_label.grid(row=0, column=0, sticky="w")

eye_btn = tk.Button(card_number_container, text="👁️", bg="#1e1e1e", fg="white", bd=0,
                    font=("Arial", 14), command=toggle_card_visibility,
                    activebackground="#1e1e1e", cursor="hand2")
eye_btn.grid(row=0, column=1, sticky="e", padx=(10, 0))

info_bottom_frame = tk.Frame(card_frame, bg="#1e1e1e")
info_bottom_frame.pack(fill="x", padx=20, pady=(20, 10))

tk.Label(info_bottom_frame, text="Card Holder", bg="#1e1e1e", fg="#cccccc",
         font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w")

tk.Label(info_bottom_frame, text="Valid Thru", bg="#1e1e1e", fg="#cccccc",
         font=("Segoe UI", 9)).grid(row=0, column=1, sticky="e", padx=(40, 0))

tk.Label(info_bottom_frame, text="Kurt Rojo", bg="#1e1e1e", fg="white",
         font=("Segoe UI", 11, "bold")).grid(row=1, column=0, sticky="w", pady=5)

tk.Label(info_bottom_frame, text="12/25", bg="#1e1e1e", fg="white",
         font=("Segoe UI", 11)).grid(row=1, column=1, sticky="e", padx=(40, 0))

detail_frame = tk.Frame(content_frame, bg="#ffffff", bd=2, relief="ridge")
detail_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
detail_frame.columnconfigure(0, weight=1)

tk.Label(detail_frame, text="ACCOUNT INFORMATION", bg="#ffffff", fg="#2c3e50",
         font=("Segoe UI", 12, 'bold')).pack(anchor="nw", padx=20, pady=(20, 5))

info_frame = tk.Frame(detail_frame, bg="#ffffff")
info_frame.pack(fill="both", expand=True, padx=20, pady=10)
info_frame.columnconfigure(0, weight=1)

labels = ["Name", "Phone Number", "E-mail", "Address"]
values = ["Kurt Rojo", "+63 945 234 4568", "mail@email.com", "25th St., Masterson’s Avenue, Uptown"]

for label_text, value in zip(labels, values):
    item_frame = tk.Frame(info_frame, bg="#f7f9fa", bd=1, relief="solid")
    item_frame.pack(fill="x", pady=5)

    tk.Label(item_frame, text=label_text, bg="#f7f9fa", fg="#34495e",
             font=("Segoe UI", 10, 'bold')).pack(anchor="w", padx=10, pady=(5, 0))
    
    tk.Label(item_frame, text=value, bg="#f7f9fa", fg="#2c3e50",
             font=("Segoe UI", 10), wraplength=400, justify="left").pack(anchor="w", padx=10, pady=(0, 5))

controls_frame = tk.Frame(main_frame, bg="#ecf0f3")
controls_frame.grid(row=2, column=0, sticky="ew", pady=10)
controls_frame.columnconfigure(0, weight=1)

back_button = tk.Button(controls_frame, text="⟵ Back", font=("Segoe UI", 11), bg="#dfe6e9", fg="#2d3436",
                        activebackground="#b2bec3", padx=20, pady=5, relief="flat", cursor="hand2")
back_button.pack(side="left", padx=5)

footer_label = tk.Label(main_frame, text="© 2025 Kurt Bayot | Design by Kurt Bayot", bg="#ecf0f3", fg="#95a5a6",
                        font=("Segoe UI", 9))
footer_label.grid(row=3, column=0, sticky="s", pady=(10, 0))

root.mainloop()

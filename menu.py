from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from model import Manager,Table,Basemodel,Cook,Product,Drink,Pro,Order,Orderedtables,Baseorder,Maosh


def donothing():
    print("ishladi")


def oncloseTopWindow(window, toplevel):
    window.deiconify()
    window.state('zoomed')
    toplevel.destroy()

def oncloseTopWindow2(window, toplevel):
    # window.deiconify()
    window.state('zoomed')
    toplevel.destroy()


def openfinishdaywindow(window):
    window.withdraw()
    productwindow = Toplevel()
    productwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, productwindow))
    productwindow.title("Moliyaviy holat")
    productwindow.geometry('600x450')
    productwindow.resizable(0, 0)
    productwindow.config(bg="#706c3d")


    def closetables():
        for sel_table in Table.objects():
            if sel_table.isbusy ==1:
                salary = 0
                summamain = 0
                summasale = 0
                for obj in sel_table.order_objects():
                    summamain = summamain +  obj.price * obj.count
                    summasale = summasale + obj.sale_price * obj.count

                manager = Manager.objects()
                salary = summasale * obj.waiter_prot/100
                manager.waiter_salary = manager.waiter_salary + salary
                summasale = summasale + salary
                manager.expense = manager.expense + summamain
                manager.profit = manager.profit + summasale
                manager.money = manager.money + summasale
                manager.save()

                sel_table.isbusy = 0
                sel_table.save()
                #TABLELARNI YARATISH VA TARIXGA YOZISH
                ordered_table = Orderedtables(sel_table.table_id)
                ordered_table.save()            #table tarixtablega qo`shilyapti
                sel_table.create_table()         #tablega yangi table yaratildi
                # opencheckwindow(window, ordered_table.name)



    def finishday():
        # closetables()
        busy = False
        for sel_table in Table.objects():
            if sel_table.isbusy ==1:
                busy = True
        if busy == False:
            if messagebox.askokcancel(title="Diqqat!", message=f"Kunni hisob kitobini yopasizmi?"):
                manager =Manager.objects()
                maosh = Maosh.objects()

                sum1 = 0
                sum1 += manager.cooker_salary_prot
                maosh.cooker += manager.cooker_salary_prot
                sum1 += manager.waiter_salary
                maosh.waiter += manager.waiter_salary
                manager.waiter_salary = 0
                maosh.save()
                manager.save()

                summa = 0
                for cook in Cook.objects():
                    if cook.count > 0:
                        summa = summa + cook.price * cook.count
                        cook.count = 0
                        cook.price = 0
                        cook.sale_price = 0
                        cook.save()
                manager.expense += summa
                messagebox.showinfo(title = "Ma`lumot!",message = f"{sum1} so`m ish haqi uchun hisoblandi.  {summa} so`m sotilmagan taom uchun zararga qo`shildi")
        else:
            messagebox.showwarning(title = "Diqqat",message = "Bazi stollar buyurtmasi yopilmagan!")


    # label1 = Label(productwindow, text="Quyidagi band stollar hisob kitob qilinadi", height=1, bg="blue", fg="white")
    # label1.config(font=("Arial", 12))
    # label1.grid(row=0, column=0, columnspan=7)
    #
    # columns = ('table_number', 'bron')
    # table = ttk.Treeview(productwindow, columns=columns, show='headings')
    # table.heading('table_number', text='Table number')
    # table.heading('bron', text='Bron')
    # table.grid(row=1, column=0, columnspan=7)
    #
    # for table1 in Table.objects():
    #     if table1.isbusy==1:
    #         table.insert('', END, iid=table1.id, values=table1)


    label1 = Label(productwindow, text="Quyidagi taomlar bugun sotilmaganligi uchun tannarxlari zararga hisoblanadi", height=1, bg="red", fg="white")
    label1.config(font=("Arial", 12))
    label1.grid(row=2, column=0, columnspan=7)

    columns = ('product_name', 'product_count')
    table = ttk.Treeview(productwindow, columns=columns, show='headings')
    table.heading('product_name', text='Taom nomi')
    table.heading('product_count', text='Soni')
    table.grid(row=3, column=0, columnspan=7)

    for cook in Cook.objects():
        if cook.count>0:
            table.insert('', END, iid=cook.id, values=cook)

    manager = Manager.objects()

    label1 = Label(productwindow, text="__", height=1, bg="#706c3d", fg="#706c3d")
    label1.config(font=("Arial", 12))
    label1.grid(row=4, column=0, columnspan=7)

    result = f"Oshpaz uchun hisoblanadigan ish haqi:         {manager.cooker_salary_prot} so`m"
    label = Label(productwindow, text=result, height=2, bg="green", fg="black")
    label.config(font=("Arial", 12))
    label.grid(row=5, column=0, columnspan=7)

    label1 = Label(productwindow, text="__", height=1, bg="#706c3d", fg="#706c3d")
    label1.config(font=("Arial", 12))
    label1.grid(row=6, column=0, columnspan=7)

    result1 = f"Ofitsant uchun hisoblanadigan ish haqi:         {manager.waiter_salary} so`m"
    label = Label(productwindow, text=result1, height=2,  bg="green", fg="black")
    label.config(font=("Arial", 12))
    label.grid(row=7, column=0, columnspan=7)

    button = Button(productwindow, text='Finish day',bg="blue",font = ("Arial",12), fg="white", command=finishday)
    button.grid(row=8, column=5)



def openfinancialwindow(window):   #!!!!!!!!ISH HAQILARINI TO`LANAYOTGANDA HARAJATGA QO`SHAMAN YOKI BOSHQA JOYGA KO`CHIRILAYOTGANDA KUNNI YOPISH VAQTIDA
    window.withdraw()
    productwindow = Toplevel()
    productwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, productwindow))
    productwindow.title("Moliyaviy holat")
    productwindow.geometry('600x500')
    productwindow.resizable(0, 0)
    productwindow.config(bg="#706c3d")

    str_name = StringVar()
    str_name1 = StringVar()
    str_name2 = StringVar()
    result = StringVar()

    def addmoney():
        manager = Manager.objects()
        flot2 = True
        name = str(entry_table_name.get())
        for i in name:
            if not (i.isdigit() or i == '.'):
                flot2 = False
                break
        if flot2:
            count = float(name)
            if count >0:
                manager.money +=count
                manager.save()
                result = f"Korxona hisobidagi mablag`:         {manager.money} so`m"
                label.config(text=result)
                messagebox.showinfo(title="Updating", message=f"Korxona hisobiga {count} so`m qo`shildi")
                str_name.set('')

            else:
                messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi")
        else:
            messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi")


    def submoney():
        manager = Manager.objects()
        flot2 = True
        name = str(entry_table_name.get())
        for i in name:
            if not (i.isdigit() or i == '.'):
                flot2 = False
                break
        if flot2:
            count = float(name)
            if count >0 and count<=manager.money:
                manager.money -=count
                manager.save()
                result = f"Korxona hisobidagi mablag`:         {manager.money} so`m"
                label.config(text=result)
                messagebox.showinfo(title="Updating", message=f"Korxona hisobidan {count} so`m kamaytirildi")
                str_name.set('')

            else:
                messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi")
        else:
            messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi")


    def pay_cooker():
        manager = Manager.objects()
        maosh = Maosh.objects()
        flot2 = True
        name = str(entry_table_name2.get())
        for i in name:
            if not (i.isdigit() or i == '.'):
                flot2 = False
                break
        if flot2:
            count = float(name)
            if count > 0 and count <= maosh.cooker:
                manager.money -= count
                manager.save()
                maosh.cooker -= count
                maosh.save()
                result = f"Oshpazga hisoblangan ish haqi:            {maosh.cooker} so`m"
                label2.config(text=result)
                messagebox.showinfo(title="Updating", message=f"Oshpazga {count} so`m ish haqi berildi")
                str_name2.set('')
            else:
                messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi")
        else:
            messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi")


    def pay_waiter():
        manager = Manager.objects()
        maosh = Maosh.objects()
        flot2 = True
        name = str(entry_table_name1.get())
        for i in name:
            if not (i.isdigit() or i == '.'):
                flot2 = False
                break
        if flot2:
            count = float(name)
            if count > 0 and count <= maosh.waiter:
                manager.money -= count
                manager.save()
                maosh.waiter -= count
                maosh.save()
                result = f"Ofitsantga hisoblangan ish haqi:                         {maosh.waiter} so`m"
                label1.config(text=result)
                messagebox.showinfo(title="Updating", message=f"Ofitsantga {count} so`m ish haqi berildi")
                str_name1.set('')
            else:
                messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi")
        else:
            messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi")




    def setentry():
        pass

    manager = Manager.objects()
    maosh = Maosh.objects()
    result = f"Korxona hisobidagi mablag`:         {manager.money} so`m"
    label = Label(productwindow, text=result, height=2,width = 40, bg="green", fg="white")
    label.config(font=("Arial", 12))
    label.grid(row=1, column=0, columnspan=7)

    entry_table_name = Entry(productwindow, text=str_name, bg='white')
    entry_table_name.grid(row=2, column=2)

    button = Button(productwindow, text='___Add___', command=addmoney)
    button.grid(row=3, column=0)

    buttonn = Button(productwindow, text='___Sub___', command=submoney)
    buttonn.grid(row=3, column=1)

#---------------
    label1 = Label(productwindow, text="__", height=1, bg="#706c3d", fg="#706c3d")
    label1.config(font=("Arial", 12))
    label1.grid(row=4, column=0, columnspan=7)
    # ---------------
    result = f"Ofitsantga hisoblangan ish haqi:                         {maosh.waiter} so`m"
    label1 = Label(productwindow, text=result, height=2,bg="green", fg="white")
    label1.config(font=("Arial", 12))
    label1.grid(row=5, column=0, columnspan=7)

    entry_table_name1 = Entry(productwindow, text=str_name1, width=25, bg='white')
    entry_table_name1.grid(row=6, column=2)

    button1 = Button(productwindow, text='Paying', command=pay_waiter)
    button1.grid(row=7, column=0)

#---------------
    label1 = Label(productwindow, text="__", height=1, bg="#706c3d", fg="#706c3d")
    label1.config(font=("Arial", 12))
    label1.grid(row=8, column=0, columnspan=7)
    # ---------------
    result = f"Oshpazga hisoblangan ish haqi:        {maosh.cooker} so`m"
    label2 = Label(productwindow, text=result, height=2, bg="green", fg="white")
    label2.config(font=("Arial", 12))
    label2.grid(row=8, column=0, columnspan=7)

    entry_table_name2 = Entry(productwindow, text=str_name2, width=25, bg='white')
    entry_table_name2.grid(row=9, column=2)

    button2 = Button(productwindow, text='Paying', command=pay_cooker)
    button2.grid(row=10, column=0)

# ---------------
    label1 = Label(productwindow, text="__", height=1, bg="#706c3d", fg="#706c3d")
    label1.config(font=("Arial", 12))
    label1.grid(row=11, column=0, columnspan=7)
    # ---------------
    result = f"Korxonaga yig`ilgan tushumlar:                   {manager.profit} so`m"
    label1 = Label(productwindow, text=result, height=2, bg="green", fg="white")
    label1.config(font=("Arial", 12))
    label1.grid(row=12, column=0, columnspan=7)

# ---------------
    label1 = Label(productwindow, text="__", height=1, bg="#706c3d", fg="#706c3d")
    label1.config(font=("Arial", 12))
    label1.grid(row=13, column=0, columnspan=7)
    # ---------------
    result = f"Hisoblangan sof xarajatlar:                            {manager.expense} so`m"
    label1 = Label(productwindow, text=result, height=2, bg="green", fg="white")
    label1.config(font=("Arial", 12))
    label1.grid(row=14, column=0, columnspan=7)

# ---------------
    label1 = Label(productwindow, text="__", height=1, bg="#706c3d", fg="#706c3d")
    label1.config(font=("Arial", 12))
    label1.grid(row=15, column=0, columnspan=7)
    # ---------------
    result = f"Sof   foyda:                                                              {manager.realprofit} so`m"
    label1 = Label(productwindow, text=result, height=2, bg="green", fg="white")
    label1.config(font=("Arial", 12))
    label1.grid(row=16, column=0, columnspan=7)



def opensaryraisewindow(window):
    window.withdraw()
    productwindow = Toplevel()
    productwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, productwindow))
    productwindow.title("Tahrirlash")
    productwindow.geometry('450x250')
    productwindow.resizable(0, 0)
    productwindow.config(bg="#706c3d")

    sel_order = None
    str_name = StringVar()
    result = StringVar()

    def set_drink_raise():
        manager = Manager.objects()
        flot2 = True
        name = str(entry_table_name.get())
        for i in name:
            if not (i.isdigit() or i == '.'):
                flot2 = False
                break
        if flot2:
            count = float(name)
            if count > 0 and count <= 200:
                manager.drink_raise = count
                manager.save()
                result = f"Ichimliklarning ustama foizini belgilash!   Amaldagisi: {manager.drink_raise} %"
                label.config(text=result)
                str_name.set("")
                messagebox.showinfo(title="Updating", message=f"Ichimliklarning ustama foizi {count} % ga o`zgartirildi")
            else:
                messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi 0 dan 200 % gacha kiriting")
        else:
            messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi 0 dan 200 % gacha kiriting")


    def set_cook_raise():
        manager = Manager.objects()
        flot2 = True
        name = str(entry_table_name.get())
        for i in name:
            if not (i.isdigit() or i == '.'):
                flot2 = False
                break
        if flot2:
            count = float(name)
            if count > 0 and count <= 200:
                manager.cook_raise = count
                manager.save()
                result = f"Taomlarning ustama foizini belgilash!   Amaldagisi: {manager.cook_raise} %"
                label.config(text=result)
                str_name.set("")
                messagebox.showinfo(title="Updating", message=f"Taom ustama foizi {count} % ga o`zgartirildi")
            else:
                messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi 0 dan 200 % gacha kiriting")
        else:
            messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi 0 dan 200 % gacha kiriting")


    def set_waiter_salary():
        manager = Manager.objects()
        flot2 = True
        name = str(entry_table_name.get())
        for i in name:
            if not (i.isdigit() or i == '.'):
                flot2 = False
                break
        if flot2:
            count = float(name)
            if count >0 and count <=25:
                manager.waiter_salary_prot = count
                manager.save()
                result = f"Ofitsantning   ximat  foizini  belgilash!     Amaldagisi:   {manager.waiter_salary_prot} %"
                label.config(text=result)
                str_name.set("")
                messagebox.showinfo(title="Updating", message=f"Ofitsant xizmat foizi {count} % ga o`zgartirildi")
            else:
                messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi 0 dan 25 % gacha kiriting")
        else:
            messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi 0 dan 25 % gacha kiriting")


    def set_cooker_salary():
        manager = Manager.objects()
        flot2 = True
        name = str(entry_table_name.get())
        for i in name:
            if not (i.isdigit() or i == '.'):
                flot2 = False
                break
        if flot2:
            count = float(name)
            if count >0 and count<=1000000:
                manager.cooker_salary_prot = count
                manager.save()
                result = f"Oshpazning ish haqini belgilash! Amaldagisi: {manager.cooker_salary_prot} so`m"
                label.config(text=result)
                str_name.set("")
                messagebox.showinfo(title="Updating",message = f"Oshpaz maoshi {count} so`mga o`zgartirildi")
            else:
                messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi 0 dan 1mlngacha kiriting")
        else:
            messagebox.showerror(title="Xatolik", message=f"Miqdor noto`g`ri kiritildi 0 dan 1mlngacha kiriting")


    def clickEvent(event):
        global result
        manager = Manager.objects()
        print(listbox.curselection())
        # result = ""
        # button = ""
        if listbox.curselection()[0] == 0:
            result = f"Oshpazning ish haqini belgilash! Amaldagisi: {manager.cooker_salary_prot} so`m"
            label.config(text=result)
            button.configure(text="Oshpaz maoshini yangilash", command=set_cooker_salary)


        elif listbox.curselection()[0] == 1:
            result = f"Ofitsantning   ximat  foizini  belgilash!    Amaldagisi:   {manager.waiter_salary_prot} %"
            label.config(text=result)
            button.configure(text="Ofitsant xizmat foizni yangilash", command=set_waiter_salary)

        elif listbox.curselection()[0] == 2:
            result = f"Taomlarning ustama foizini belgilash!    Amaldagisi: {manager.cook_raise} %"
            label.config(text=result)
            button.configure(text="Taom ustama foizini yangilash", command=set_cook_raise)


        elif listbox.curselection()[0] == 3:
            result = f"Ichimliklarning ustama foizini belgilash!   Amaldagisi: {manager.drink_raise} %"
            label.config(text=result)
            button.configure(text="Ichinliklar ustama foizini yangilash", command=set_drink_raise)


    def setentry():
        pass

    listbox = Listbox(productwindow,  font=("Constantia", 18), width=22)
    listbox.grid(row=0, column=0)
    listbox.insert(25, "Oshpaz ish haqi")
    listbox.insert(2, "Ofitsant xizmati foizi")
    listbox.insert(33, "Taomlarga ustama foiz")
    listbox.insert(105, "Ichimliklarga ustama foiz")
    listbox.config(height=listbox.size())
    listbox.bind('<<ListboxSelect>>', clickEvent)

    label = Label(productwindow, text=result, height=2, bg="green", fg="black")
    label.config(font=("Arial", 12))
    label.grid(row=1, column=0, columnspan=7)
    result = "________________________________"
    label.config(text=result)

    entry_table_name = Entry(productwindow, text=str_name, width=10, bg='yellow')
    entry_table_name.grid(row=2, column=0)


    button = Button(productwindow, text='set', command=setentry)
    button.grid(row=3, column=0)





def openhistorieswindow(window):
    window.withdraw()
    productwindow = Toplevel()
    productwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, productwindow))
    productwindow.title("Tables")
    productwindow.geometry('980x320')
    productwindow.resizable(0, 0)
    productwindow.config(bg="#706c3d")

    sel_order = None
    str_order_name = StringVar()
    result = StringVar()
    result1 = StringVar()

    def deleteOrder():
        global sel_order
        if sel_order:
            if str_order_name.get() == "delete1":
                print(table.selection())
                selected_item = table1.selection()[0]
                table1.delete(selected_item)
                sel_order.delete()
                for item in table.get_children():
                    table.delete(item)
                result="____________________________________________________________"
                lb_name.config(text=result)
                result1="_________________________________"
                lb_name2.config(text=result1)

            else:
                messagebox.showerror(title="Xatolik", message="Parol xato! O`chirish uchun maxfiy parol kiritilishi kerak!")
        else:
            messagebox.showerror(title = "Xatolik", message = "Buyurtma tanlanmadi!")





    def onClick1(event):
        try:
            global sel_order
            id = int(table1.focus())
            sel_order = Orderedtables.get_by_id(id)
            name = sel_order.name

            for item in table.get_children():
                table.delete(item)

            summa = 0
            for order in Order.get_by_order_name(name):
                summa = summa + order.sale_price * order.count
                table.insert('', END, iid=order.id, values=order)

            all = summa * (order.waiter_prot / 100 + 1)
            salary = summa * order.waiter_prot / 100

            result = f"Jami: {summa} | Ofitsant xizmati {order.waiter_prot} % = {salary} | To`lov: {all} so`m"
            lb_name.config(text=result)
            result1 = "Sana: __.__.__                   vaqt: __.__"
            lb_name2.config(text=result1)


        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("Xatolik", str(err))

    columns = ('table_number')
    table1 = ttk.Treeview(productwindow, columns=columns, show='headings')
    table1.heading('table_number', text='Buyurtma nomi')
    table1.grid(row=1, column=0, columnspan=2)

    for order in Orderedtables.objects():
        table1.insert('', END, iid=order.id, values=order)

    table1.bind('<<TreeviewSelect>>', onClick1)

    lb_name = Label(productwindow, text="Password for deleting: ")
    lb_name.grid(row=2, column=1)

    entry_table_name = Entry(productwindow, text=str_order_name, width=23,show = '*',bg = 'yellow')
    # entry_table_name.config(state="disabled")
    entry_table_name.grid(row=3, column=1)

    btn_add = Button(productwindow, text='Delete', command=deleteOrder)
    btn_add.grid(row=4, column=1)

    columns = ('table_number', 'count', 'price', 'all')
    table = ttk.Treeview(productwindow, columns=columns, show='headings')
    table.heading('table_number', text='Nomi')
    table.heading('count', text='Soni')
    table.heading('price', text='Narxi')
    table.heading('all', text='Jami')
    table.grid(row=1, column=2, columnspan=3)

    lb_name = Label(productwindow, text="______  ______  _____")
    lb_name.config(font=("Arial", 12))
    lb_name.grid(row=2, column=3)

    lb_name2 = Label(productwindow, text="_____ _____")
    lb_name2.config(font=("Arial", 8))
    lb_name2.grid(row=3, column=3)

    # result = ""
    # if sel_order:
    #     summa = 0
    #     for order in Order.get_by_order_name(name):
    #         summa = summa + order.sale_price * order.count
    #         table.insert('', END, iid=order.id, values=order)
    #
    #     all = summa * (order.waiter_prot / 100 + 1)
    #     salary = summa * order.waiter_prot / 100
    #
    #     result = f"Jami: {summa} | Ofitsant xizmati {order.waiter_prot} % = {salary} | To`lov: {all} so`m"
    #
    #     lb_name = Label(productwindow, text=result)
    #     lb_name.config(font=("Arial", 8))
    #     lb_name.grid(row=2, column=2)
    #
    #     lb_name2 = Label(productwindow, text="Sana: __.__.__                   vaqt: __.__")
    #     lb_name2.config(font=("Arial", 8))
    #     lb_name2.grid(row=3, column=2)




def opencheckwindow(window,name):
    window.withdraw()
    productwindow = Toplevel()
    productwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow2(window, productwindow))
    productwindow.title("Buyurtma ro`yhati")
    productwindow.geometry('750x350')
    productwindow.resizable(0, 0)
    productwindow.config(bg="#706c3d")

    columns = ('table_number','count','price','all')
    table = ttk.Treeview(productwindow, columns=columns, show='headings')
    table.heading('table_number', text='Nomi')
    table.heading('count', text='Soni')
    table.heading('price', text='Narxi')
    table.heading('all', text='Jami')
    table.grid(row=1, column=0, columnspan=1)

    summa = 0
    for order in Order.get_by_order_name(name):
        summa = summa + order.sale_price * order.count
        table.insert('', END, iid=order.id, values=order)

    all = summa * (order.waiter_prot/100 + 1)
    salary = summa * order.waiter_prot/100

    result = f"Jami: {summa} | Ofitsant xizmati {order.waiter_prot} % = {salary} | To`lov: {all} so`m"
    lb_name = Label(productwindow, text=result)
    lb_name.config(font = ("Arial",13))
    lb_name.grid(row=2, column=0)

    lb_name2 = Label(productwindow, text="Sana: __.__.__                   vaqt: __.__")
    lb_name2.config(font=("Arial", 8))
    lb_name2.grid(row=3, column=0)

    lb_name1 = Label(productwindow, text="Tashrifingiz uchun tashakkur!")
    lb_name1.config(font=("Arial", 20))
    lb_name1.grid(row=4, column=0)



def finishorderwindow(window):
    window.withdraw()
    productwindow = Toplevel()
    productwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, productwindow))
    productwindow.title("Tables")
    productwindow.geometry('380x300')
    productwindow.resizable(0, 0)
    productwindow.config(bg="#706c3d")

    sel_table = None
    str_table_name = StringVar()

    def finishOrder():
        global sel_table
        if sel_table:
            if messagebox.askokcancel(title="Best!", message=f"{sel_table.number}-stol buyurtmasini yopasizmi?"):
                summamain = 0
                summasale = 0
                salary = 0
                for obj in sel_table.order_objects():
                    summamain = summamain +  obj.price * obj.count
                    summasale = summasale + obj.sale_price * obj.count

                manager = Manager.objects()
                salary = summasale * obj.waiter_prot/100
                manager.waiter_salary = manager.waiter_salary + salary
                summasale = summasale + salary
                manager.expense = manager.expense + summamain
                manager.profit = manager.profit + summasale
                manager.money = manager.money + summasale
                manager.save()

                sel_table.isbusy = 0
                sel_table.save()
                selected_item = table.selection()[0]
                table.delete(selected_item)

                #TABLELARNI YARATISH VA TARIXGA YOZISH
                ordered_table = Orderedtables(sel_table.table_id)
                ordered_table.save()            #table tarixtablega qo`shilyapti
                sel_table.create_table()         #tablega yangi table yaratildi

                opencheckwindow(window,ordered_table.name)
            else:
                messagebox.showinfo(title="Eslatma!", message="Buyurtma ro`yhatini ko`rish uchun == Buyurtma olish == menusiga kiring!")

        else:
            messagebox.showerror(title = "Xatolik", message = "Stol tanlanmadi!")



    def onClick1(event):
        # opencheckwindow(window, "order_num_8")
        try:
            global sel_table
            id = int(table.focus())
            sel_table = Table.get_by_id(id)
            str_table_name.set(str(sel_table.number)+" - stol")

        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("Xatolik", str(err))

    columns = ('table_number', 'bron')
    table = ttk.Treeview(productwindow, columns=columns, show='headings')
    table.heading('table_number', text='Table number')
    table.heading('bron', text='Bron')
    table.grid(row=1, column=0, columnspan=2)

    for table1 in Table.objects():
        if table1.isbusy == 1:
            table.insert('', END, iid=table1.id, values=table1)

    table.bind('<<TreeviewSelect>>', onClick1)

    lb_name = Label(productwindow, text="Stol nomi: ")
    lb_name.grid(row=2, column=0)

    entry_table_name = Entry(productwindow, text=str_table_name, width=23)
    entry_table_name.config(state="disabled")
    entry_table_name.grid(row=3, column=0)

    btn_add = Button(productwindow, text='Finish', command=finishOrder)
    btn_add.grid(row=3, column=1)



def get_orderwindow(window):
    window.withdraw()
    productwindow = Toplevel()
    productwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, productwindow))
    productwindow.title("Tables")
    productwindow.geometry('810x620')
    productwindow.resizable(0, 0)
    productwindow.config(bg="#706c3d")


    sel_cook = None
    sel_drink = None
    sel_table = None
    sel_order = None

    str_cook_name = StringVar()
    str_cook_count = StringVar()

    str_drink_name = StringVar()
    str_drink_count = StringVar()

    str_order_name = StringVar()
    str_order_count = StringVar()


    def onAddCook():
        global sel_cook,sel_table
        if sel_cook and sel_table and str_cook_count.get() != "":
            flot2 = True
            for i in str(str_cook_count.get()):
                if not (i.isdigit() or i == '.'):
                    flot2 = False
                    break
            if flot2:
                cook_id = int(table_cook.focus())
                count = float(str_cook_count.get())
                if count > 0 and count <= sel_cook.count:
                    if cook_id not in sel_table.order_cook_id_to_check():
                        manager = Manager.objects()
                        # prot = manager.cook_raise
                        order = Order(cook_id=cook_id,drink_id=0,name = sel_cook.name, count=count,price=sel_cook.price,sale_price=sel_cook.sale_price,table_id=sel_table.id,type1="cook",waiter_prot=manager.waiter_salary_prot)
                        sel_table.set_order_table(order)
                        sel_table.isbusy = 1
                        sel_table.save()
                        sel_cook.count -= count
                        if sel_cook.count == 0:
                            sel_cook.sale_price = 0
                            sel_cook.price = 0
                        sel_cook.save()
                        focused = table_cook.focus()
                        table_cook.item(focused, values=sel_cook)
                        focused1 = table.focus()
                        table.item(focused1, values=sel_table)
                        str_cook_name.set('')
                        str_cook_count.set('')
                        table_order.insert('', END, iid=order.id, values=order)
                        sel_cook = None
                    else:
                        if messagebox.askokcancel(title="Best!", message=f"{sel_cook.name}dan yana {count} miqdor qo`shasizmi?"):
                            order = sel_table.order_get_by_cook_id(cook_id)
                            order.count += count
                            sel_table.set_order_table(order)
                            sel_table.isbusy = 1
                            sel_table.save()
                            sel_cook.count -= count
                            if sel_cook.count == 0:
                                sel_cook.sale_price = 0
                                sel_cook.price = 0
                            sel_cook.save()
                            focused = table_cook.focus()
                            table_cook.item(focused, values=sel_cook)
                            focused1 = table.focus()
                            table.item(focused1, values=sel_table)
                            str_cook_name.set('')
                            str_cook_count.set('')
                            table_order.item(order.id, values=order)
                            # table_order.insert('', END, iid=order.id, values=order)
                            sel_cook = None
                        else:
                            str_cook_name.set('')
                            str_cook_count.set('')
                            sel_cook = None

                else:
                    messagebox.showinfo(title="Xatolik", message=f"Miqdor xato yoki {sel_cook.name}dan bu miqdor yuq!")
            else:
                messagebox.showerror(title="Xatolik", message="Noto`g`ri miqdor")
        else:
            messagebox.showerror(title="Xatolik", message="Stol va taomni tanlang!")


    def onAddDrink():
        global sel_drink, sel_table
        if sel_drink and sel_table and str_drink_count.get() != "":
            flot2 = True
            for i in str(str_drink_count.get()):
                if not (i.isdigit() or i == '.'):
                    flot2 = False
                    break
            if flot2:
                drink_id = int(table_drink.focus())
                count = float(str_drink_count.get())
                if count > 0 and count <= sel_drink.count:
                    if drink_id not in sel_table.order_drink_id_to_check():
                        manager = Manager.objects()
                        prot = manager.drink_raise
                        order = Order(cook_id=0, drink_id=drink_id, name=sel_drink.name, count=count, price=sel_drink.price,sale_price=sel_drink.sale_price, table_id=sel_table.id, type1="drink",waiter_prot=manager.waiter_salary_prot)
                        sel_table.set_order_table(order)
                        sel_table.isbusy = 1
                        sel_table.save()
                        sel_drink.count -= count
                        if sel_drink.count == 0:
                            sel_drink.sale_price = 0
                            sel_drink.price = 0
                        sel_drink.save()
                        focused = table_drink.focus()
                        table_drink.item(focused, values=sel_drink)
                        focused1 = table.focus()
                        table.item(focused1, values=sel_table)
                        str_drink_name.set('')
                        str_drink_count.set('')
                        table_order.insert('', END, iid=order.id, values=order)
                        sel_drink = None
                    else:
                        if messagebox.askokcancel(title="Best!",message=f"{sel_drink.name}dan yana {count} miqdor qo`shasizmi?"):
                            order = sel_table.order_get_by_drink_id(drink_id)
                            order.count += count
                            sel_table.set_order_table(order)
                            sel_table.isbusy = 1
                            sel_table.save()
                            sel_drink.count -= count
                            if sel_drink.count == 0:
                                sel_drink.sale_price = 0
                                sel_drink.price = 0
                            sel_drink.save()
                            focused = table_drink.focus()
                            table_drink.item(focused, values=sel_drink)
                            focused1 = table.focus()
                            table.item(focused1, values=sel_table)
                            str_drink_name.set('')
                            str_drink_count.set('')
                            table_order.item(order.id, values=order)
                            # table_order.insert('', END, iid=order.id, values=order)
                            sel_drink = None
                        else:
                            str_drink_name.set('')
                            str_drink_count.set('')
                            sel_drink = None

                else:
                    messagebox.showinfo(title="Xatolik", message=f"Miqdor xato yoki {sel_drink.name}dan bu miqdor yuq!")
            else:
                messagebox.showerror(title="Xatolik", message="Noto`g`ri miqdor")
        else:
            messagebox.showerror(title="Xatolik", message="Stol va ichimlikni tanlang!")


    def onUpdateOrder():
        global sel_cook, sel_order
        flot2 = True
        for i in str(str_order_count.get()):
            if not (i.isdigit() or i == '.'):
                flot2 = False
                break
        if entry_pro_count.get() != "" and flot2:
            count = float(str_order_count.get())
            if count > 0:
                focused = table_pro.focus()  # id sini oladi
                sel_order.counts = count
                sel_cook.set_product_table(sel_order)
                str_order_name.set('')
                str_order_count.set('')
                table_pro.item(focused, values=sel_order)  # focused idli elementni qiymatini o`zgartir
                sel_order = None
            else:
                messagebox.showinfo(title="Xatolik", message="Miqdor xato kiritildi!")
        else:
            messagebox.showinfo(title="Xatolik", message="Miqdor xato kiritildi!")

    def onDeleteOrder():
        global sel_table, sel_order
        if sel_table and str_order_count.get() != "":
            flot2 = True
            for i in str(str_order_count.get()):
                if not (i.isdigit() or i == '.'):
                    flot2 = False
                    break
            if sel_order and flot2:
                count = float(str_order_count.get())
                if count<=sel_order.count:
                    id = int(table_order.focus ())
                    order = sel_table.order_get_by_id(id)
                    if order.type1 == "cook":
                        messagebox.showinfo(title="Uzur!", message="Taom qaytarib olinmaydi!")
                    elif order.type1 == "drink":
                        if messagebox.askokcancel(title="Diqqat!", message=f"{order.name}dan {count} miqdorni qaytarmoqchimisiz?"):
                            order.count -= count
                            if order.count == 0:
                                selected_item = table_order.selection()[0]
                                table_order.delete(selected_item)         #tabledan o`chirish
                                sel_table.order_delete(order)              #bazadan o`chirish

                                if len(sel_table.check_isorderyes()) == 0:
                                    sel_table.isbusy = 0
                                    sel_table.save()
                                    table.item(sel_table.id, values=sel_table)
                            else:
                                sel_table.set_order_table(order)
                                table_order.item(order.id, values=order)

                            drink = Drink.get_by_id(order.drink_id)
                            drink.count += count
                            drink.save()
                            table_drink.item(drink.id, values=drink)   #drink oynasida shu drinkni o`zgartirib qo`yish

                    str_order_name.set('')
                    str_order_count.set('')
                    sel_order = None
                else:
                    messagebox.showerror(title="Xatolik", message="Buncha miqdor buyurtma qilinmagan!")
            else:
                messagebox.showerror(title="Xatolik", message="Kamaytiriladigan buyurtma tanlanmadi yoki not`o`gri qiymat")
        else:
            messagebox.showerror(title="Xatolik", message="Buyurtma tanlanmadi yoki miqdor xato!")

            for item in table_order.get_children():
                table_order.delete(item)

    def onClick1(event):
        try:
            global sel_table
            id = int(table.focus())
            sel_table = Table.get_by_id(id)

            for order in sel_table.order_objects():
                table_order.insert('', END, iid=order.id, values=order)
        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("Xatolik", str(err))

    def onClick2(event):
        try:
            global sel_order,sel_table
            id = int(table_order.focus())
            sel_order = sel_table.order_get_by_id(id)
            str_order_name.set(sel_order.name)
            # str_order_count.set(sel_order.count)
        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("Xatolik", str(err))

    def onClick3(event):
        try:
            global sel_cook
            id = int(table_cook.focus())
            sel_cook = Cook.get_by_id(id)
            str_cook_name.set(sel_cook.name)
            # str_cook_count.set(sel_cook.count)

        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("Xatolik", str(err))

    def onClick4(event):
        try:
            global sel_drink
            id = int(table_drink.focus())
            sel_drink = Drink.get_by_id(id)
            str_drink_name.set(sel_drink.name)
            # str_drink_count.set(sel_drink.count)

        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("Xatolik", str(err))


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # 1-TABLE COOK_PRODUCT
    columns = ('table_number', 'bron')
    table = ttk.Treeview(productwindow, columns=columns, show='headings')
    table.heading('table_number', text='Table number')
    table.heading('bron', text='Bron')
    table.grid(row=1, column=0, columnspan=2)

    for table1 in Table.objects():
        table.insert('', END, iid=table1.id, values=table1)

    table.bind('<<TreeviewSelect>>', onClick1)

    # 2-TABLE COOK_PRODUCT
    columns = ('pro_name', 'pro_count')
    table_order = ttk.Treeview(productwindow, columns=columns, show='headings')
    table_order.heading('pro_name', text='Mahsulot nomi')
    table_order.heading('pro_count', text='Miqdori')
    table_order.grid(row=1, column=2, columnspan=3)

    if sel_table:
        for order in sel_table.order_objects():
            table_order.insert('', END, iid=order.id, values=order)

    table_order.bind('<<TreeviewSelect>>', onClick2)

    lb_name3 = Label(productwindow, text="Buyurtma nomi: ")
    lb_name3.grid(row=2, column=2)

    entry_pro_name = Entry(productwindow, text=str_order_name, width=20)
    entry_pro_name.config(state="disabled")
    entry_pro_name.grid(row=3, column=2)

    lb_name4 = Label(productwindow, text="Buyurtma miqdori: ")
    lb_name4.grid(row=2, column=3)

    entry_pro_count = Entry(productwindow, text=str_order_count, width=20)
    entry_pro_count.grid(row=3, column=3)

    # btn_upd = Button(productwindow, text='Update', command=onUpdateOrder)
    # btn_upd.grid(row=4, column=2)

    btn_del = Button(productwindow, text='Buyurtmani kamaytirish', command=onDeleteOrder)
    btn_del.grid(row=4, column=3)

    # 3-TABLE COOK
    columns = ('cook_name', 'cook_count')
    table_cook = ttk.Treeview(productwindow, columns=columns, show='headings')
    table_cook.heading('cook_name', text='Taom nomi')
    table_cook.heading('cook_count', text='Miqdori')
    table_cook.grid(row=5, column=0, columnspan=2)

    for cook in Cook.objects():
        table_cook.insert('', END, iid=cook.id, values=cook)

    table_cook.bind('<<TreeviewSelect>>', onClick3)

    lb_name = Label(productwindow, text="Taom nomi: ")
    lb_name.grid(row=6, column=0)

    entry_product_name1 = Entry(productwindow, text=str_cook_name, width=18)
    entry_product_name1.config(state="disabled")
    entry_product_name1.grid(row=7, column=0)

    lb_name1 = Label(productwindow, text="Taom miqdori: ")
    lb_name1.grid(row=6, column=1)

    entry_product_count1 = Entry(productwindow, text=str_cook_count, width=18)
    entry_product_count1.grid(row=7, column=1)

    btn_add = Button(productwindow, text='Adding', command=onAddCook)
    btn_add.grid(row=8, column=1, columnspan=1)

    # 4-TABLE PRODUCT
    columns = ('drink_name', 'drink_count')
    table_drink = ttk.Treeview(productwindow, columns=columns, show='headings')
    table_drink.heading('drink_name', text='Ichimlik nomi')
    table_drink.heading('drink_count', text='Miqdori')
    table_drink.grid(row=5, column=2, columnspan=2)

    for drink in Drink.objects():
        table_drink.insert('', END, iid=drink.id, values=drink)

    table_drink.bind('<<TreeviewSelect>>', onClick4)

    lb_name = Label(productwindow, text="Ichimlik nomi: ")
    lb_name.grid(row=6, column=2)

    entry_product_name = Entry(productwindow, text=str_drink_name, width=18)
    entry_product_name.config(state="disabled")
    entry_product_name.grid(row=7, column=2)

    lb_name1 = Label(productwindow, text="Ichimlik miqdori: ")
    lb_name1.grid(row=6, column=3)

    entry_product_count = Entry(productwindow, text=str_drink_count, width=18)
    entry_product_count.grid(row=7, column=3)

    btn_add = Button(productwindow, text='Adding', command=onAddDrink)
    btn_add.grid(row=8, column=3, columnspan=1)




def ontablewindow(window):
    window.withdraw()
    tablewindow = Toplevel()
    tablewindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, tablewindow))
    tablewindow.title("Tables")
    tablewindow.geometry('400x270')
    tablewindow.resizable(0, 0)
    tablewindow.config(bg="#706c3d")



    # lb_name = Label(tablewindow, text="Brand Name: ")
    # lb_name.grid(row=0, column=0)


    columns = ('table_number','bron')
    table = ttk.Treeview(tablewindow, columns=columns, show='headings')
    table.heading('table_number', text='Table number')
    table.heading('bron', text='Bron')
    table.pack()

    for table1 in Table.objects():
        table.insert('', END, iid=table1.id, values=table1)


def onaddcookwindow(window):
    window.withdraw()
    cookwindow = Toplevel()
    cookwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, cookwindow))
    cookwindow.title("Tables")
    cookwindow.geometry('600x400')
    cookwindow.resizable(0, 0)
    cookwindow.config(bg="#706c3d")

    str_cook_name = StringVar()
    str_cook_count = StringVar()
    sel_cook = None



    def onAddProduct():
        if entry_name.get() != '' and  str_cook_count.get() != '':
            global sel_cook
            flot2 = True
            for i in str(str_cook_count.get()):
                if not (i.isdigit() or i == '.'):
                    flot2 = False
                    break
            if sel_cook and flot2:
                if len(sel_cook.check_isorderyes()) == 0:
                    messagebox.showerror(title="Xatolik", message="Bu ovqat tayyorlash uchun kerakli masalliqlar kiritilmagan!")
                else:
                    manager = Manager.objects()
                    count = float(str_cook_count.get())
                    summa=0
                    enough = True
                    for pro in sel_cook.pro_objects():
                        product = Product.get_by_id((pro.product_id))
                        if product.count<pro.counts * count:
                            enough = False
                            break
                        summa = summa + product.price * pro.counts
                        product.count = product.count - pro.counts * count
                        if product.count == 0:
                            product.price = 0
                        product.save()

                    if enough:
                        sel_cook.price = (sel_cook.price*sel_cook.count + summa * count)/(sel_cook.count + count)
                        sel_cook.sale_price = sel_cook.price * (manager.cook_raise/100 + 1)
                        sel_cook.count += count
                        manager.save()
                        sel_cook.save()

                        str_cook_name.set('')
                        str_cook_count.set('')
                        focused = table.focus()
                        table.item(focused, values=sel_cook)
                        messagebox.showinfo(title="Diqqat", message=f"{sel_cook.name} taomidan {count} miqdor qo`shildi, tannarxi={summa} sum 1 porsiya uchun")
                    else:
                        messagebox.showerror(title="Xatolik", message=f"{count} miqdor {sel_cook.name} tayyorlash uchun masalliqlar yetarli emas")
            else:
                messagebox.showerror(title="Xatolik", message="Qatorlar noto`g`ri to`ldirilgan!")
        else:
            messagebox.showerror(title="Xatolik", message="Qatorlar noto`g`ri to`ldirilgan!")





    def onClick(event):
        try:
            global sel_cook
            id = int(table.focus())
            sel_cook = Cook.get_by_id(id)
            str_cook_name.set(sel_cook.name)
        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("Xatolik", str(err))

    def onDeleteBrand():
        if entry_name.get() != '' and str_cook_count.get() != '':
            global sel_cook
            flot2 = True
            for i in str(str_cook_count.get()):
                if not (i.isdigit() or i == '.'):
                    flot2 = False
                    break

            if sel_cook and flot2:
                focused = table.focus()
                count = float(str_cook_count.get())
                if count <= sel_cook.count and count > 0:
                    sel_cook.count -= count
                    manager = Manager.objects()
                    summa = count * sel_cook.price
                    manager.expense += summa
                    manager.save()
                    str_cook_name.set('')
                    str_cook_count.set('')
                    if sel_cook.count == 0:     #tannarxni 0 ga tenglash
                        sel_cook.price = 0
                        sel_cook.sale_price = 0
                    sel_cook.save()
                    table.item(focused, values=sel_cook)
                    sel_cook = None
                    messagebox.showinfo(title="Diqqat", message=f"{summa} sum zarar hisobiga o`tkazildi")
                else:
                    messagebox.showinfo(title="Diqqat", message=f"{sel_cook.name} dan {count} miqdor yuq! yoki noto`g`ri miqdor")
            else:
                messagebox.showinfo(title="Xatolik", message="Qatorlar noto`g`ri to`ldirilgan!")



    columns = ('product_name', 'product_count', 'product_price')
    table = ttk.Treeview(cookwindow, columns=columns, show='headings')
    table.heading('product_name', text='Taom nomi')
    table.heading('product_count', text='Soni')
    table.heading('product_price', text='Tannarxi')
    table.pack()

    lb_name = Label(cookwindow, text="Taom nomi: ")
    lb_name.pack()

    entry_name = Entry(cookwindow, text=str_cook_name, width=40)
    entry_name.config(state="disabled")
    entry_name.pack()

    lb_name1 = Label(cookwindow, text="Taom soni: ")
    lb_name1.pack()

    entry_name1 = Entry(cookwindow, text=str_cook_count, width=40)
    entry_name1.pack()

    btn_add = Button(cookwindow, text='Add', command=onAddProduct)
    btn_add.pack()

    btn_del = Button(cookwindow, text='Delete', command=onDeleteBrand)
    btn_del.pack()

    table.bind('<<TreeviewSelect>>', onClick)

    for cook in Cook.objects():
        table.insert('', END, iid=cook.id, values=cook)


def onproductcookwindow(window):
    window.withdraw()
    productwindow = Toplevel()
    productwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, productwindow))
    productwindow.title("Tables")
    productwindow.geometry('480x620')
    productwindow.resizable(0, 0)
    productwindow.config(bg="#706c3d")

    sel_cook = None

    str_product_name = StringVar()
    str_product_count = StringVar()
    sel_product = None

    str_pro_name = StringVar()
    str_pro_count = StringVar()
    sel_pro = None



    def onAddProduct():
        global sel_product, sel_cook
        if sel_product and str_product_name.get() != '' and str_product_count.get() != '' and sel_product.name==str_product_name.get():
            flot2 = True
            for i in str(str_product_count.get()):
                if not (i.isdigit() or i == '.'):
                    flot2 = False
                    break
            if  flot2:
                product_id = int(table_product.focus())
                count = float(str_product_count.get())
                if count>0:
                    if product_id not in sel_cook.pro_objects_to_check():
                        pro = Pro(product_id,count)
                        sel_cook.set_product_table(pro)
                        str_product_name.set('')
                        str_product_count.set('')
                        table_pro.insert('', END, iid=pro.id, values=pro)
                        sel_product = None
                    else:
                        messagebox.showinfo(title="Xatolik", message="Bu mahsulot qo`shilgan!")
                else:
                    messagebox.showinfo(title="Xatolik", message="Qatorlar noto`g`ri to`ldirilgan!")
            else:
                messagebox.showinfo(title="Xatolik", message="Qatorlar noto`g`ri to`ldirilgan!")
        else:
            messagebox.showinfo(title="Xatolik", message="Qatorlar noto`g`ri to`ldirilgan!")

    def onClick1(event):
        try:
            global sel_cook
            id = int(table_cook.focus())
            sel_cook = Cook.get_by_id(id)

            for item in table_pro.get_children():
                table_pro.delete(item)

            for pro in sel_cook.pro_objects():
                table_pro.insert('', END, iid=pro.id, values=pro)
        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("Xatolik", str(err))

    def onClick2(event):
        try:
            global sel_product
            id = int(table_product.focus())
            sel_product = Product.get_by_id(id)
            str_product_name.set(sel_product.name)
        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("Xatolik", str(err))

    def onClick3(event):
        try:
            global sel_cook,sel_product,sel_pro
            id = int(table_pro.focus())
            sel_pro = sel_cook.pro_get_by_id(id)
            str_pro_name.set(sel_pro.product_name)
            str_pro_count.set(sel_pro.counts)

        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("Xatolik", str(err))

    def onUpdateBrand():
        global sel_cook,sel_pro
        flot2 = True
        for i in str(str_pro_count.get()):
            if not (i.isdigit() or i == '.'):
                flot2 = False
                break
        if entry_pro_count.get() !="" and flot2 :
            count = float(str_pro_count.get())
            if count>0:
                focused = table_pro.focus()   #id sini oladi
                sel_pro.counts = count
                sel_cook.set_product_table(sel_pro)
                str_pro_name.set('')
                str_pro_count.set('')
                table_pro.item(focused, values=sel_pro)   #focused idli elementni qiymatini o`zgartir
                sel_pro = None
            else:
                messagebox.showinfo(title="Xatolik", message="Miqdor xato kiritildi!")
        else:
            messagebox.showinfo(title="Xatolik", message="Miqdor xato kiritildi!")


    def onDeleteBrand():
        global sel_cook,sel_product,sel_pro
        if sel_pro:
            id = int(table_pro.focus())
            sel_cook.pro_delete(id)
            selected_item = table_pro.selection()[0]
            table_pro.delete(selected_item)
            str_pro_name.set('')
            str_pro_count.set('')
            sel_pro = None
        else:
            messagebox.showinfo(title="Xatolik", message="Mahsulot tanlanmadi!")


    # 1-TABLE COOK
    columns = ('cook_name')
    table_cook = ttk.Treeview(productwindow, columns=columns, show='headings')
    table_cook.heading('cook_name', text='Taom nomi')
    table_cook.grid(row=1, column=0, columnspan=2)

    for cook in Cook.objects():
        table_cook.insert('', END, iid=cook.id, values=cook)

    table_cook.bind('<<TreeviewSelect>>', onClick1)


    #2-TABLE PRODUCT
    columns = ('product_name')
    table_product = ttk.Treeview(productwindow, columns=columns, show='headings')
    table_product.heading('product_name', text='Mahsulot nomi')
    table_product.grid(row=1, column=2, columnspan=2)

    for product in Product.objects():
        table_product.insert('', END, iid=product.id, values=product)

    table_product.bind('<<TreeviewSelect>>', onClick2)

    # 3-TABLE COOK_PRODUCT
    columns = ('pro_name', 'pro_count')
    table_pro = ttk.Treeview(productwindow, columns=columns, show='headings')
    table_pro.heading('pro_name', text='Mahsulot nomi')
    table_pro.heading('pro_count', text='Miqdori')
    table_pro.grid(row=5, column=1, columnspan=3)

    if sel_cook:
        for cook in sel_cook.pro_objects():
            table_pro.insert('', END, iid=cook.id, values=cook)

    table_pro.bind('<<TreeviewSelect>>', onClick3)

    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #2-tablega
    lb_name = Label(productwindow, text="Mahsulot nomi: ")
    lb_name.grid(row = 2,column =2)

    entry_product_name = Entry(productwindow, text=str_product_name, width=18)
    entry_product_name.config(state="disabled")
    entry_product_name.grid(row = 3,column =2)

    lb_name1 = Label(productwindow, text="Mahsulot miqdori: ")
    lb_name1.grid(row = 2,column =3)

    entry_product_count = Entry(productwindow, text=str_product_count, width=18)
    entry_product_count.grid(row = 3,column =3)

    btn_add = Button(productwindow, text='Adding', command=onAddProduct)
    btn_add.grid(row = 4,column =3,columnspan = 1)

    #3-tablega
    lb_name3 = Label(productwindow, text="Mahsulot nomi: ")
    lb_name3.grid(row = 6,column =1)

    entry_pro_name = Entry(productwindow, text=str_pro_name, width=20)
    entry_pro_name.config(state="disabled")
    entry_pro_name.grid(row = 7,column =1)

    lb_name4 = Label(productwindow, text="Mahsulot miqdori: ")
    lb_name4.grid(row = 6,column =2)

    entry_pro_count = Entry(productwindow, text=str_pro_count, width=20)
    entry_pro_count.grid(row = 7,column =2)

    btn_upd = Button(productwindow, text='Update', command=onUpdateBrand)
    btn_upd.grid(row = 9,column =1)

    btn_del = Button(productwindow, text='Delete', command=onDeleteBrand)
    btn_del.grid(row = 9,column =2)


def oncookwindow(window):
    window.withdraw()
    productwindow = Toplevel()
    productwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, productwindow))
    productwindow.title("Tables")
    productwindow.geometry('800x420')
    productwindow.resizable(0, 0)
    productwindow.config(bg="#706c3d")

    str_product_name = StringVar()
    sel_product = None

    def onAddProduct():
        if entry_name.get() == '':
            messagebox.showerror(title="Xatolik", message="Taom nomini kiriting!")
        elif entry_name.get() in Cook.objects_to_check():
            messagebox.showerror(title="Xatolik", message="Bu nomli taom mavjud!")
        else:
            productnew = Cook(entry_name.get())
            productnew.save()
            # TABLE YARATISH KERAK MAHSULOTLAR RO`YHATINI SAQLASHGA

            table.insert('', END, iid=productnew.id, values=productnew)
            str_product_name.set('')

    def onClick(event):
        try:
            global sel_product
            id = int(table.focus())
            sel_product = Cook.get_by_id(id)
            str_product_name.set(sel_product.name)
        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("Xatolik", str(err))

    def onUpdateBrand():
        if entry_name.get() !="":
            global sel_product
            if sel_product and entry_name.get() != '':
                focused = table.focus()
                sel_product.name = str_product_name.get()
                sel_product.save()
                str_product_name.set('')
                table.item(focused, values=sel_product)
                sel_product = None
            else:
                messagebox.showerror(title="Xatolik", message="Taom tanlanmadi!")
        else:
            messagebox.showerror(title="Xatolik", message="Taom tanlanmadi!")

    def onDeleteBrand():
        if entry_name.get() in Cook.objects_to_check():
            global sel_product
            if sel_product and entry_name.get() != '':
                if sel_product.count > 0:
                    messagebox.showerror(title="Xatolik", message="Miqdor 0 dan katta bo`lgan taomni o`chirib bo`lmaydi!")
                else:
                    if messagebox.askokcancel(title="Diqqat!",message =f"{sel_product.name}ni o`chirmoqchimisiz?" ):
                        sel_product.delete()
                        sel_product = None
                        selected_item = table.selection()[0]
                        table.delete(selected_item)
                        str_product_name.set('')
                    else:
                        sel_product = None
                        str_product_name.set('')
            else:
                messagebox.showerror(title="Xatolik", message="Taom tanlanmadi!")
        else:
            messagebox.showerror(title="Xatolik", message="Taom tanlanmadi!")


    columns = ('product_name', 'product_count', 'product_price', 'product_sale_price')
    table = ttk.Treeview(productwindow, columns=columns, show='headings')
    table.heading('product_name', text='Taom nomi')
    table.heading('product_count', text='Soni')
    table.heading('product_price', text='Tannarxi')
    table.heading('product_sale_price', text='Sotish narxi')
    table.pack()

    entry_name = Entry(productwindow, text=str_product_name, width=40)
    entry_name.pack()

    table.bind('<<TreeviewSelect>>', onClick)  # tableni ustiuga tekkanda onClick ishlasin degani

    btn_add = Button(productwindow, text='Add', command=onAddProduct)
    btn_add.pack()

    btn_update = Button(productwindow, text='Update', command=onUpdateBrand)
    btn_update.pack()

    btn_del = Button(productwindow, text='Delete', command=onDeleteBrand)
    btn_del.pack()

    for drink in Cook.objects():
        table.insert('', END, iid=drink.id, values=drink)


def onadddrinkwindow(window):
    window.withdraw()
    productwindow = Toplevel()
    productwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, productwindow))
    productwindow.title("Tables")
    productwindow.geometry('600x400')
    productwindow.resizable(0, 0)
    productwindow.config(bg="#706c3d")

    str_product_name = StringVar()
    str_product_price = StringVar()
    str_product_count = StringVar()
    sel_product = None

    def onAddProduct():
        if entry_name.get() != '' and str_product_price.get() != '' and str_product_count.get() != '':
            global sel_product
            flot1 = True
            for i in str(str_product_price.get()):
                if not (i.isdigit() or i == '.'):
                    flot1 = False
                    break
            flot2 = True
            for i in str(str_product_count.get()):
                if not (i.isdigit() or i == '.'):
                    flot2 = False
                    break

            if sel_product and flot1 and flot2:
                focused = table.focus()
                count = float(str_product_count.get())
                price = float(str_product_price.get())
                manager = Manager.objects()
                summa = count * price
                if manager.money>=summa:
                    sel_product.price = (sel_product.price * sel_product.count + count * price) / (
                                sel_product.count + count)
                    sel_product.count += count
                    sel_product.sale_price = sel_product.price * (manager.drink_raise/100+1)   #sotish narxi qo`yilyapti
                    sel_product.save()
                    manager.money -= summa
                    manager.save()
                    str_product_name.set('')
                    str_product_price.set('')
                    str_product_count.set('')
                    table.item(focused, values=sel_product)
                    sel_product = None
                    messagebox.showinfo(title="Diqqat", message=f"{summa} sum korxona hisobidan yechildi")
                else:
                    messagebox.showerror(title="Diqqat", message=f"Korxona hisobida {summa} sum yuq")
            else:
                messagebox.showinfo(title="Xatolik", message="Qatorlar noto`g`ri to`ldirilgan!")

    def onClick(event):
        try:
            global sel_product
            id = int(table.focus())
            sel_product = Drink.get_by_id(id)
            str_product_name.set(sel_product.name)
            str_product_price.set(sel_product.price)
        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("Xatolik", str(err))

    def onDeleteBrand():
        if entry_name.get() != '' and str_product_price.get() != '' and str_product_count.get() != '':
            global sel_product
            flot2 = True
            for i in str(str_product_count.get()):
                if not (i.isdigit() or i == '.'):
                    flot2 = False
                    break

            if sel_product and flot2:
                focused = table.focus()
                count = float(str_product_count.get())
                if count <= sel_product.count:
                    sel_product.count -= count

                    manager = Manager.objects()
                    summa = count * sel_product.price
                    manager.expense += summa
                    manager.save()
                    str_product_name.set('')
                    str_product_price.set('')
                    str_product_count.set('')
                    if sel_product.count ==0:
                        sel_product.price =0
                        sel_product.sel_price =0
                    sel_product.save()
                    table.item(focused, values=sel_product)
                    sel_product = None
                    messagebox.showinfo(title="Diqqat", message=f"{summa} sum zarar hisobiga o`tkazildi")
                else:
                    messagebox.showinfo(title="Diqqat", message=f"{sel_product.name} dan {count} miqdor yuq!")
            else:
                messagebox.showinfo(title="Xatolik", message="Qatorlar noto`g`ri to`ldirilgan!")

    columns = ('product_name', 'product_count', 'product_price')
    table = ttk.Treeview(productwindow, columns=columns, show='headings')
    table.heading('product_name', text='Ichimlik nomi')
    table.heading('product_count', text='Soni')
    table.heading('product_price', text='Tannarxi')
    table.pack()

    lb_name = Label(productwindow, text="Ichimlik nomi: ")
    lb_name.pack()

    entry_name = Entry(productwindow, text=str_product_name, width=40)
    entry_name.config(state="disabled")
    entry_name.pack()

    lb_name1 = Label(productwindow, text="Ichimlik soni: ")
    lb_name1.pack()

    entry_name1 = Entry(productwindow, text=str_product_count, width=40)
    entry_name1.pack()

    lb_name2 = Label(productwindow, text="Ichimlik tannarxi: ")
    lb_name2.pack()

    entry_name2 = Entry(productwindow, text=str_product_price, width=40)
    entry_name2.pack()

    table.bind('<<TreeviewSelect>>', onClick)  # tableni ustiuga tekkanda onClick ishlasin degani

    btn_add = Button(productwindow, text='Add', command=onAddProduct)
    btn_add.pack()

    btn_del = Button(productwindow, text='Delete', command=onDeleteBrand)
    btn_del.pack()

    for drink in Drink.objects():
        table.insert('', END, iid=drink.id, values=drink)

def ondrinkwindow(window):
    window.withdraw()
    productwindow = Toplevel()
    productwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, productwindow))
    productwindow.title("Tables")
    productwindow.geometry('800x420')
    productwindow.resizable(0, 0)
    productwindow.config(bg="#706c3d")

    str_product_name = StringVar()
    sel_product = None

    def onAddProduct():
        if entry_name.get() == '':
            messagebox.showinfo(title="Xatolik", message="Ichimlik nomini kiriting!")
        elif entry_name.get() in Drink.objects_to_check():
            messagebox.showinfo(title="Xatolik", message="Bu nomli ichimlik mavjud!")
        else:
            productnew = Drink(entry_name.get())
            productnew.save()
            table.insert('', END, iid=productnew.id, values=productnew)
            str_product_name.set('')

    def onClick(event):
        try:
            global sel_product
            id = int(table.focus())
            sel_product = Drink.get_by_id(id)
            str_product_name.set(sel_product.name)
        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("Xatolik", str(err))

    def onUpdateBrand():
        global sel_product
        if sel_product and entry_name.get() != '':
            focused = table.focus()
            sel_product.name = str_product_name.get()
            sel_product.save()
            str_product_name.set('')
            table.item(focused, values=sel_product)
            sel_product = None
        else:
            messagebox.showinfo(title="Xatolik", message="Ichimlik tanlanmadi!")

    def onDeleteBrand():
        global sel_product
        if sel_product and entry_name.get() != '':
            if sel_product.count > 0:
                messagebox.showerror(title="Diqqat!", message="Miqdori 0 dan katta bo`lgan ichimlikni o`chirib bo`lmaydi!")
            else:
                if messagebox.askokcancel(title="Diqqat!", message=f"{sel_product.name}ni o`chirmoqchimisiz?"):
                    sel_product.delete()
                    sel_product = None
                    selected_item = table.selection()[0]
                    table.delete(selected_item)
                    str_product_name.set('')
                else:
                    str_product_name.set('')
                    sel_product = None
        else:
            messagebox.showerror(title="Xatolik", message="Ichimlik tanlanmadi!")

    columns = ('product_name', 'product_count', 'product_price','product_sale_price')

    table = ttk.Treeview(productwindow, columns=columns, show='headings')
    table.heading('product_name', text='Ichimlik nomi')
    table.heading('product_count', text='Soni')
    table.heading('product_price', text='Tannarxi')
    table.heading('product_sale_price', text='Sotish narxi')
    table.pack()

    entry_name = Entry(productwindow, text=str_product_name, width=40)
    entry_name.pack()

    table.bind('<<TreeviewSelect>>', onClick)  # tableni ustiuga tekkanda onClick ishlasin degani

    btn_add = Button(productwindow, text='Add', command=onAddProduct)
    btn_add.pack()

    btn_update = Button(productwindow, text='Update', command=onUpdateBrand)
    btn_update.pack()

    btn_del = Button(productwindow, text='Delete', command=onDeleteBrand)
    btn_del.pack()

    for drink in Drink.objects():
        table.insert('', END, iid=drink.id, values=drink)

def onaddproductwindow(window):
    window.withdraw()
    productwindow = Toplevel()
    productwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, productwindow))
    productwindow.title("Tables")
    productwindow.geometry('600x400')
    productwindow.resizable(0, 0)
    productwindow.config(bg="#706c3d")

    str_product_name = StringVar()
    str_product_price = StringVar()
    str_product_count = StringVar()
    sel_product = None

    def onAddProduct():
        if entry_name.get() != '' and str_product_price.get()!='' and str_product_count.get()!='':
            global sel_product
            flot1 = True
            for i in str(str_product_price.get()):
                if not (i.isdigit() or i=='.'):
                    flot1 = False
                    break
            flot2 = True
            for i in str(str_product_count.get()):
                if not (i.isdigit() or i=='.'):
                    flot2 = False
                    break

            if sel_product and flot1 and flot2:
                focused = table.focus()
                count = float(str_product_count.get())
                price = float(str_product_price.get())
                manager = Manager.objects()
                summa = count * price
                if manager.money>=summa:
                    sel_product.price = (sel_product.price * sel_product.count + count * price) / (sel_product.count + count)
                    sel_product.count += count
                    sel_product.save()
                    manager.money -= summa
                    manager.save()
                    str_product_name.set('')
                    str_product_price.set('')
                    str_product_count.set('')
                    table.item(focused, values=sel_product)
                    sel_product = None
                    messagebox.showinfo(title="Diqqat", message=f"{summa} sum korxona hisobidan yechildi")
                else:
                    messagebox.showerror(title="Diqqat", message=f"Korxona hisobida {summa} sum yuq")
            else:
                messagebox.showinfo(title="Xatolik", message="Qatorlar noto`g`ri to`ldirilgan!")



    def onClick(event):
        try:
            global sel_product
            id = int(table.focus())
            print(id)
            sel_product = Product.get_by_id(id)
            str_product_name.set(sel_product.name)
            str_product_price.set(sel_product.price)
        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("Xatolik", str(err))


    def onDeleteBrand():
        if entry_name.get() != '' and str_product_price.get() != '' and str_product_count.get() != '':
            global sel_product
            flot2 = True
            for i in str(str_product_count.get()):
                if not (i.isdigit() or i == '.'):
                    flot2 = False
                    break

            if sel_product and flot2:
                focused = table.focus()
                count = float(str_product_count.get())
                if count<= sel_product.count:
                    sel_product.count -= count

                    manager = Manager.objects()
                    summa = count * sel_product.price
                    manager.expense += summa
                    manager.save()
                    str_product_name.set('')
                    str_product_price.set('')
                    str_product_count.set('')
                    if sel_product.count == 0:
                        sel_product.price = 0
                    sel_product.save()
                    table.item(focused, values=sel_product)
                    sel_product = None
                    messagebox.showinfo(title="Diqqat", message=f"{summa} sum zarar hisobiga o`tkazildi")
                else:
                    messagebox.showinfo(title="Diqqat", message=f"{sel_product.name} dan {count} miqdor yuq!")
            else:
                messagebox.showinfo(title="Xatolik", message="Qatorlar noto`g`ri to`ldirilgan!")

    columns = ('product_name', 'product_count', 'product_price')
    table = ttk.Treeview(productwindow, columns=columns, show='headings')
    table.heading('product_name', text='Mahsulot nomi')
    table.heading('product_count', text='Soni')
    table.heading('product_price', text='Narxi')
    table.pack()

    lb_name = Label(productwindow, text="Mahsulot nomi: ")
    lb_name.pack()

    entry_name = Entry(productwindow, text=str_product_name, width=40)
    entry_name.config(state="disabled")
    entry_name.pack()

    lb_name1 = Label(productwindow, text="Mahsulot soni: ")
    lb_name1.pack()

    entry_name1 = Entry(productwindow, text = str_product_count, width=40)
    entry_name1.pack()

    lb_name2 = Label(productwindow, text="Mahsulot narxi: ")
    lb_name2.pack()

    entry_name2 = Entry(productwindow, text = str_product_price, width=40)
    entry_name2.pack()

    table.bind('<<TreeviewSelect>>', onClick)  # tableni ustiuga tekkanda onClick ishlasin degani

    btn_add = Button(productwindow, text='Add', command=onAddProduct)
    btn_add.pack()

    btn_del = Button(productwindow, text='Delete', command=onDeleteBrand)
    btn_del.pack()

    for product in Product.objects():
        table.insert('', END, iid=product.id, values=product)


def onproductswindow(window):
    window.withdraw()
    productwindow = Toplevel()
    productwindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, productwindow))
    productwindow.title("Tables")
    productwindow.geometry('600x420')
    productwindow.resizable(0, 0)
    productwindow.config(bg="#706c3d")

    str_product_name = StringVar()
    sel_product = None

    def onAddProduct():
        if entry_name.get() =='':
            messagebox.showinfo(title="Xatolik", message="Mahsulot nomini kiriting!")
        elif entry_name.get() in Product.objects_to_check():
            messagebox.showinfo(title="Xatolik", message="Bu nomli mahsulot mavjud!")
        else:
            productnew = Product(entry_name.get())
            productnew.save()
            table.insert('', END, iid=productnew.id, values=productnew)
            str_product_name.set('')


    def onClick(event):
        try:
            global sel_product
            id = int(table.focus())
            print(id)
            sel_product = Product.get_by_id(id)
            str_product_name.set(sel_product.name)
        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("Xatolik", str(err))

    def onUpdateBrand():
        global sel_product
        if sel_product:
            focused = table.focus()
            sel_product.name = str_product_name.get()
            sel_product.save()
            str_product_name.set('')
            table.item(focused, values=sel_product)
            sel_product = None
        else:
            messagebox.showinfo(title="Xatolik", message="Mahsulot tanlanmadi!")

    def onDeleteBrand():
        global sel_product
        if sel_product:
            if sel_product.id in Cook.pro_object() or sel_product.count > 0:
                messagebox.showerror(title="Xatolik",message=f"{sel_product.name} ba`zi taomlar masalliq ro`yhatida bor yoki miqdori 0 emas")
            else:
                if messagebox.askokcancel(title="Diqqat!", message=f"{sel_product.name}ni o`chirmoqchimisiz?"):
                    sel_product.delete()
                    sel_product = None
                    selected_item = table.selection()[0]
                    table.delete(selected_item)
                    str_product_name.set('')
                else:
                    sel_product = None
                    str_product_name.set('')
        else:
            messagebox.showinfo(title="Xatolik", message="Mahsulot tanlanmadi!")


    columns = ('product_name','product_count','product_price')
    table = ttk.Treeview(productwindow, columns=columns, show='headings')
    table.heading('product_name', text='Mahsulot nomi')
    table.heading('product_count', text='Soni')
    table.heading('product_price', text='Narxi')
    table.pack()

    entry_name = Entry(productwindow, text=str_product_name,width=40)
    entry_name.pack()


    table.bind('<<TreeviewSelect>>', onClick)  # tableni ustiuga tekkanda onClick ishlasin degani

    btn_add = Button(productwindow, text='Add', command=onAddProduct)
    btn_add.pack()

    btn_update = Button(productwindow, text='Update', command=onUpdateBrand)
    btn_update.pack()

    btn_del = Button(productwindow, text='Delete', command=onDeleteBrand)
    btn_del.pack()

    for product in Product.objects():
        table.insert('', END, iid=product.id, values=product)


def ontableswindow(window):
    window.withdraw()
    tablewindow = Toplevel()
    tablewindow.protocol('WM_DELETE_WINDOW', lambda: oncloseTopWindow(window, tablewindow))
    tablewindow.title("Tables")
    tablewindow.geometry('500x320')
    tablewindow.resizable(0, 0)
    tablewindow.config(bg="#706c3d")



    # lb_name = Label(tablewindow, text="Brand Name: ")
    # lb_name.grid(row=0, column=0)

    str_table_name = StringVar()
    sel_table = None

    def onAddBrand():
        if entry_name.get().isdigit():
            if int(entry_name.get()) in Table.objects_to_check():
                messagebox.showinfo(title="Xatolik", message="Bunday raqamli stol mavjud!")
            else:
                tablenew = Table(entry_name.get())
                tablenew.save()

                table.insert('', END, iid=tablenew.id, values=tablenew)
                str_table_name.set('')
        else:
            messagebox.showinfo(title = "Xatolik",message = "Stol nomerini raqamlarda kiriting!")

    def onClick(event):
        try:
            global sel_table
            id = int(table.focus())
            sel_table = Table.get_by_id(id)
            str_table_name.set(sel_table.number)
        except ValueError as err:
            pass
            # messagebox.showerror("O'chirishda xatolik", str(err))
        except Exception as err:
            messagebox.showerror("O'chirishda xatolik", str(err))

    def onUpdateBrand():
        global sel_table
        if sel_table and sel_table.isbusy==0:
            focused = table.focus()
            sel_table.number = str_table_name.get()
            sel_table.save()
            str_table_name.set('')
            table.item(focused, values=sel_table)
            sel_table = None
        else:
            messagebox.showinfo(title="Xatolik", message="Bu stol band yoki stol tanlanmadi!")

    def onDeleteBrand():
        global sel_table
        if sel_table and sel_table.isbusy==0:
            if messagebox.askokcancel(title="Diqqat!", message=f"{sel_table.number}-stolni o`chirmoqchimisiz?"):
                sel_table.delete()
                sel_table = None
                selected_item = table.selection()[0]
                table.delete(selected_item)
                str_table_name.set('')
            else:
                sel_table = None
                str_table_name.set('')
        else:
            messagebox.showinfo(title="Xatolik", message="Bu stol band yoki stol tanlanmadi!")


    columns = ('table_number','bron')
    table = ttk.Treeview(tablewindow, columns=columns, show='headings')
    table.heading('table_number', text='Table number')
    table.heading('bron', text='Bron')
    table.pack()

    entry_name = Entry(tablewindow, text=str_table_name,width=40)
    entry_name.pack()


    table.bind('<<TreeviewSelect>>', onClick)  # tableni ustiuga tekkanda onClick ishlasin degani

    btn_add = Button(tablewindow, text='Add', command=onAddBrand)
    btn_add.pack()

    btn_update = Button(tablewindow, text='Update', command=onUpdateBrand)
    btn_update.pack()

    btn_del = Button(tablewindow, text='Delete', command=onDeleteBrand)
    btn_del.pack()

    for table1 in Table.objects():
        table.insert('', END, iid=table1.id, values=table1)  # tablega ma`lumot to`ldiryapti


def makeMenu(window):
    menubar = Menu(window,font = ('Arial',15),bg = 'green')

    filemenu = Menu(menubar, tearoff=0,font = ("Arial",15))
    menubar.add_cascade(label="Manager", menu=filemenu)
    filemenu.add_command(label="Stollar ro`yhati", command=lambda: ontableswindow(window))
    # filemenu.add_command(label="Taomlar  ro`yhati", command=donothing)
    filemenu.add_command(label="Ichimliklar  ro`yhati", command=lambda: ondrinkwindow(window))
    filemenu.add_command(label="Mahsulotlar ro`yhati", command=lambda: onproductswindow(window))
    filemenu.add_separator()
    filemenu.add_command(label="Ichimlik qo`shish/kamaytirish", command=lambda: onadddrinkwindow(window))
    filemenu.add_command(label="Mahsulot qo`shish/kamaytirish", command=lambda: onaddproductwindow(window))
    filemenu.add_separator()
    filemenu.add_command(label="Ustama va ish haqlarini belgilash", command=lambda: opensaryraisewindow(window))
    filemenu.add_separator()
    filemenu.add_command(label="Kunni yopish", command=lambda: openfinishdaywindow(window))
    filemenu.add_command(label="Moliyaviy holatni ko`rsatish", command=lambda: openfinancialwindow(window))
    filemenu.add_separator()
    filemenu.add_command(label="Chiqish", command=window.quit)

    editmenu = Menu(menubar, tearoff=0,font = ("Arial",15))
    menubar.add_cascade(label="Waiter", menu=editmenu)
    editmenu.add_command(label="Stollar holati", command=lambda: ontablewindow(window))
    editmenu.add_separator()
    editmenu.add_command(label="Buyurtma olish", command=lambda: get_orderwindow(window))
    editmenu.add_command(label="Buyurtmani yopish", command=lambda: finishorderwindow(window))
    editmenu.add_separator()
    editmenu.add_command(label="Buyurtmalar tarixi", command=lambda: openhistorieswindow(window))


    servicemenu = Menu(menubar, tearoff=0,font = ("Arial",15))
    menubar.add_cascade(label="Cooker", menu=servicemenu)
    servicemenu.add_command(label="Taomlar ro`yhati", command=lambda: oncookwindow(window))
    servicemenu.add_command(label="Taom qo`shish/kamaytirish", command=lambda: onaddcookwindow(window))
    servicemenu.add_separator()
    servicemenu.add_command(label="Taom masalliqlarini belgilash", command=lambda: onproductcookwindow(window))

    return menubar

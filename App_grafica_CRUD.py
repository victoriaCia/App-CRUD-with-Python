from cgitb import text
from tkinter import *
from tkinter import messagebox
import sqlite3



root=Tk()
root.title("Aplicación CRUD")
root.config(background='gray50')
root.geometry("280x385")
root.iconbitmap("C:/Users/victo/Documents/Curso Python/App grafica CRUD-practica guiada/datebase_icono.ico")

barraMenu=Menu(root)
root.config(menu=barraMenu)

miFrame=Frame(root,width=280,height=370)
miFrame.config(background='gray50')
miFrame.pack()

id=StringVar()
nombre=StringVar()
apellido=StringVar()
direccion=StringVar()
password=StringVar()
coment=StringVar()


#-----------------------DESHABILITAR EL ENTRY SI NO ESTA CONECTADA LA BBDD-------

def normal_entry():
    cuadroId.config(state="normal")    
    cuadroNombre.config(state="normal")
    cuadroApellido.config(state="normal")
    cuadroDireccion.config(state="normal")
    cuadroPassword.config(state="normal")
    textComent.config(state="normal")   #ver para Text


#-------------------------------ENVIAR DATOS DESDE EL TEXT--------------------

def datos_text():    #funcion que devuelve el contenido de el Text: textComent
    com=textComent.get(1.0,"end-1c")
    return com

#--------------------------------CONECTAR Y DESCONECTAR----------------------------

def conectar():
    global miConexion,miCursor
    try:
        miConexion=sqlite3.connect("Usuarios")
        miCursor=miConexion.cursor()
        miCursor.execute('''
            CREATE TABLE datos_usuarios(
                id integer PRIMARY KEY AUTOINCREMENT,
                nombre varchar(20),
                apellido varchar(20),
                direccion varchar(20),
                password varchar(30),
                comentario varchar(140))
            ''')
        messagebox.showinfo("Base de datos creada","Base de datos Usuarios creada con éxito")
        normal_entry()
    except:
            miConexion=sqlite3.connect("Usuarios")
            miCursor=miConexion.cursor()
            messagebox.showinfo("Base de datos conectada","Se ha conectado a la base de datos con éxito")
            normal_entry()

def desconectar():
    try:
        miConexion.close()
        cuadroId.config(state="disable")
        cuadroNombre.config(state="disable")
        cuadroApellido.config(state="disable")
        cuadroDireccion.config(state="disable")
        cuadroPassword.config(state="disable")
        textComent.config(state="disable") 
    except:
        messagebox.showerror("Desconexion no realizada","No se ha conectado previamente a una base de datos")

#------------------------------------CREATE--------------------------

def insertar():
    global coment
    try:
        coment=datos_text()
        datosUsuario=[nombre.get(),apellido.get(),direccion.get(),password.get(),coment]
        miCursor.execute("INSERT INTO datos_usuarios VALUES(NULL,?,?,?,?,?)",datosUsuario)
        miConexion.commit()
        messagebox.showinfo("Registro insertado","Se ha insertado un registro con éxito")
    except NameError:
        messagebox.showerror("Base de datos no conectada","Debe conectarse previamente a la base de datos")


def busqueda():
    global coment
    try:
        try:
            id_busc=id.get()
            miCursor.execute("SELECT * FROM datos_usuarios WHERE id="+id_busc+"")

            vistaDatos=miCursor.fetchall()    #devuleve una tupla multidimensional

            nombre.set(vistaDatos[0][1])
            apellido.set(vistaDatos[0][2])
            direccion.set(vistaDatos[0][3])
            password.set(vistaDatos[0][4])
            textComent.delete("1.0","end")
            textComent.insert("1.0",vistaDatos[0][5])   
            
            miConexion.commit()
        except IndexError:
            messagebox.showerror("Error en la busqueda ","No hay un usuario con el id ingresado")
        except sqlite3.OperationalError:
            messagebox.showerror("Error en la busqueda ","El id ingresado no es válido")
    except NameError:
        messagebox.showerror("Base de datos no conectada","Debe conectarse previamente a la base de datos")


#-----------------------------UPDATE-----------------------------------

def actualizar():     #como hacer para ingrese un id correcto y salte mensaje??
    global coment
    try:
        try:
            coment=datos_text()
            miCursor.execute("UPDATE datos_usuarios SET nombre=? ,apellido=? ,direccion=? ,password=?,comentario=? WHERE id=?",(nombre.get(),apellido.get(),direccion.get(),password.get(),coment,id.get()))      
            miConexion.commit()
            messagebox.showinfo("Registro actualizado","El registro se ha actualizado con éxito")
        except IndexError:
            messagebox.showerror("Error en la busqueda ","No hay un usuario con el id ingresado")
        except sqlite3.OperationalError:
            messagebox.showerror("Error en la busqueda ","El id ingresado no es válido")
    except NameError:
        messagebox.showerror("Base de datos no conectada","Debe conectarse previamente a la base de datos")

#---------------------------------DELETE-----------------------------------

def eliminar():
    try:
        try:
            id_busc=id.get()
            miCursor.execute("DELETE from datos_usuarios where id="+id_busc+"")
            valor=messagebox.askokcancel("Eliminar registro","¿Seguro que desea eliminar el registro de la tabla?")
            if valor:
                miConexion.commit()
                messagebox.showinfo("Registro eliminado","El registro se ha eliminado con éxito")
        except IndexError:
            messagebox.showerror("Error en la busqueda ","No hay un usuario con el id ingresado")
        except sqlite3.OperationalError:
            messagebox.showerror("Error en la busqueda ","El id ingresado no es válido")
    except NameError:
        messagebox.showerror("Base de datos no conectada","Debe conectarse previamente a la base de datos")



#--------------------------BORRAR XCAMPOS------------------------------

def borrar_campos():     #como hacer para q, luego de borrar, no se inserten en un registro vacio????
    id.set("")
    nombre.set("")
    apellido.set("")
    direccion.set("")
    password.set("")
    textComent.delete("1.0","end")



#-------------------------VENTANAS EMERGENTES Y MENU---------------------

def infoAdicional():
    messagebox.showinfo("Herramientas CRUD","Se utiliza la base de datos SQLite")

def avisoLicencia():
    messagebox.showwarning("Licencia","Producto bajo licencia de Victoria Cia")

def salirAplicacion():    #no funciona bien: sale siempre
    valor=messagebox.askquestion("Salir","¿Desea salir de la aplicacion?")
    if valor=='yes':
        miConexion.close()
        root.destroy()


#---------------------------------MENUS----------------------------

menuBd=Menu(barraMenu,tearoff=0)
menuBd.add_command(label="Conectar",command=conectar)  
menuBd.add_command(label="Desconectar",command=desconectar)
menuBd.add_separator()
menuBd.add_command(label="Salir",command=salirAplicacion)


menuCRUD=Menu(barraMenu,tearoff=0)
menuCRUD.add_command(label="Crear",command=insertar)  
menuCRUD.add_command(label="Leer",command=busqueda)  
menuCRUD.add_command(label="Actualizar",command=actualizar)  
menuCRUD.add_command(label="Eliminar",command=eliminar)  


menuAyuda=Menu(barraMenu,tearoff=0)
menuAyuda.add_command(label="Licencia",command=avisoLicencia)  
menuAyuda.add_command(label="Acerca de...",command=infoAdicional) 

barraMenu.add_cascade(label="BBDD",menu=menuBd)
barraMenu.add_command(label="Borrar campos",command=borrar_campos) 
barraMenu.add_cascade(label="CRUD",menu=menuCRUD)
barraMenu.add_cascade(label="Ayuda",menu=menuAyuda)


#---------------------------------ENTRY-----------------------------

cuadroId=Entry(miFrame,textvariable=id)
cuadroId.grid(row=0,column=1,padx=10,pady=5)
cuadroId.config(justify="center",state="disable",fg="black",disabledbackground='gray50',background='gray80')
cuadroNombre=Entry(miFrame,textvariable=nombre)
cuadroNombre.grid(row=1,column=1,padx=10,pady=5)
cuadroNombre.config(justify="center",state="disable",disabledbackground='gray50',background='gray80')

cuadroApellido=Entry(miFrame,textvariable=apellido)
cuadroApellido.grid(row=2,column=1,padx=10,pady=5)
cuadroApellido.config(justify="center",state="disable",disabledbackground='gray50',background='gray80')

cuadroDireccion=Entry(miFrame,textvariable=direccion)
cuadroDireccion.grid(row=3,column=1,padx=10,pady=5)
cuadroDireccion.config(justify="center",state="disable",disabledbackground='gray50',background='gray80')

cuadroPassword=Entry(miFrame,textvariable=password)
cuadroPassword.grid(row=4,column=1,padx=10,pady=5)
cuadroPassword.config(show="*",justify="center",state="disable",disabledbackground='gray50',background='gray80')

textComent=Text(miFrame,width=16,height=5)    #ver variable tipo texto largo
textComent.grid(row=5,column=1,padx=10,pady=5)
textComent.config(state="disable",background='gray80')

scrollVert=Scrollbar(miFrame,command=textComent.yview)
scrollVert.grid(row=5,column=2,sticky="nsew")
scrollVert.config(bg='black',activebackground='black',cursor='hand2')
textComent.config(yscrollcommand=scrollVert.set)


#----------------------------LABEL----------------------------------

idLabel=Label(miFrame,text="ID:")
idLabel.grid(row=0,column=0,sticky='e',pady=5)
idLabel.config(fg="white",background="gray50",underline=True)

nombreLabel=Label(miFrame,text="NOMBRE:")
nombreLabel.grid(row=1,column=0,sticky='e',pady=5)
nombreLabel.config(background="gray50")

apellidoLabel=Label(miFrame,text="APELLIDO:")
apellidoLabel.grid(row=2,column=0,sticky='e',pady=5)
apellidoLabel.config(background="gray50")

direccionLabel=Label(miFrame,text="DIRECCION:")
direccionLabel.grid(row=3,column=0,sticky='e',pady=5)
direccionLabel.config(background="gray50")

passwordLabel=Label(miFrame,text="PASSWORD:")
passwordLabel.grid(row=4,column=0,sticky='e',pady=5)
passwordLabel.config(background="gray50")

comentarioLabel=Label(miFrame,text="COMENTARIOS:")
comentarioLabel.grid(row=5,column=0,sticky='e',pady=5)
comentarioLabel.config(background="gray50")

#-----------------------------------BUTTON--------------------------
#se puede crear otro frame y q los botones queden alineados en una sola fila

botonCreate=Button(miFrame,text="Create",command=insertar)
botonCreate.grid(row=6,column=0,columnspan=2,sticky=S+N+E+W)
botonCreate.config(background='gray20',activebackground='gray30',fg='white',cursor='hand2')

botonRead=Button(miFrame,text="Read",command=busqueda)
botonRead.grid(row=7,column=0,columnspan=2,sticky=S+N+E+W)
botonRead.config(background='gray20',activebackground='gray30',fg='white',cursor='hand2')

botonUpdate=Button(miFrame,text="Update",command=actualizar)
botonUpdate.grid(row=8,column=0,columnspan=2,sticky=S+N+E+W)
botonUpdate.config(background='gray20',activebackground='gray30',fg='white',cursor='hand2')

botonDelete=Button(miFrame,text="Delete",command=eliminar)
botonDelete.grid(row=9,column=0,columnspan=2,sticky=S+N+E+W)
botonDelete.config(background='gray20',activebackground='gray30',fg='white',cursor='hand2')



root.mainloop()
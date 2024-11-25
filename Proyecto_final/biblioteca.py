import mysql.connector
from datetime import datetime, timedelta, date
import tkinter as tk
from tkinter import messagebox

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="biblioteca"
)

cursor = conexion.cursor()



def agregar_usuario(nombre, direccion, telefono, email, monto_cuota, fecha_pago):
    try:
        fecha_registro = datetime.now().strftime('%Y-%m-%d')
        sql_usuario = """
            INSERT INTO Usuarios (nombre, direccion, telefono, email, fecha_registro) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql_usuario, (nombre, direccion, telefono, email, fecha_registro))
        conexion.commit()

        id_usuario = cursor.lastrowid
        sql_pago = """
            INSERT INTO Pagos (id_usuario, monto, fecha_pago) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql_pago, (id_usuario, monto_cuota, fecha_pago))
        conexion.commit()

        messagebox.showinfo("Éxito", "Usuario y pago inicial agregados con éxito.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


def agregar_libro(titulo, autor, genero):
    try:
        sql = "INSERT INTO Libros (titulo, autor, genero) VALUES (%s, %s, %s)"
        cursor.execute(sql, (titulo, autor, genero))
        conexion.commit()

        mensaje = f"Libro agregado con exito!\n\nTitulo: {titulo}\nAutor: {autor}\nGenero: {genero}"
        messagebox.showinfo("Confirmacion", mensaje)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrio un error al agregar el libro: {e}")



def calcular_multa(id_prestamo, fecha_devolucion_real):
    try:
        if isinstance(fecha_devolucion_real, str):  
            fecha_devolucion_real = datetime.strptime(fecha_devolucion_real, '%Y-%m-%d').date()
        sql = "SELECT fecha_devolucion FROM Prestamos WHERE id=%s"
        cursor.execute(sql, (id_prestamo,))
        resultado = cursor.fetchone()

        if resultado and resultado[0]:
            fecha_devolucion_pactada = resultado[0]  
            if fecha_devolucion_real > fecha_devolucion_pactada:
                dias_retraso = (fecha_devolucion_real - fecha_devolucion_pactada).days

                # Consultar la cuota mensual de la persona
                sql = "SELECT monto FROM Pagos WHERE id_usuario = (SELECT id_usuario FROM Prestamos WHERE id = %s)"
                cursor.execute(sql, (id_prestamo,))
                cuota_resultado = cursor.fetchone()

                if cuota_resultado and cuota_resultado[0]:
                    cuota_mensual = cuota_resultado[0]
                    cuota_mensual = float(cuota_mensual)  
                    multa = cuota_mensual * 0.03 * dias_retraso

                    messagebox.showinfo("Multa", f"La multa por retraso es: {multa:.2f} pesos.")
                    return multa
                else:
                    messagebox.showerror("Error", "No se encontro la cuota del prestamo o es invalida.")
                    return 0
            else:
                messagebox.showinfo("Sin Multa", "No hay retraso en la devolucion.")
                return 0
        else:
            messagebox.showerror("Error", "No se encontro la fecha de devolucion pactada o es invalida.")
            return 0
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrio un error al calcular la multa: {e}")
        return 0



def registrar_prestamo(id_usuario, id_libro, fecha_prestamo, fecha_devolucion_pactada):
    try:
        cursor.execute("SELECT estado FROM Libros WHERE id = %s", (id_libro,))
        libro = cursor.fetchone()
        if libro and libro[0] == 'Disponible':
            fecha_prestamo_dt = datetime.strptime(fecha_prestamo, '%Y-%m-%d').date()
            fecha_devolucion_pactada_dt = datetime.strptime(fecha_devolucion_pactada, '%Y-%m-%d').date()
            sql = """
                INSERT INTO Prestamos (id_usuario, id_libro, fecha_prestamo, fecha_devolucion)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (id_usuario, id_libro, fecha_prestamo_dt, fecha_devolucion_pactada_dt))
            conexion.commit()
            id_prestamo_registrado = cursor.lastrowid
            cursor.execute("UPDATE Libros SET estado = 'Prestado' WHERE id = %s", (id_libro,))
            conexion.commit()
            messagebox.showinfo("Éxito", f"Prestamo registrado con exito. El ID del prestamo es: {id_prestamo_registrado}")
        else:
            messagebox.showwarning("Error", "El libro no está disponible para prestamo.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrio un error al registrar el prestamo: {e}")



def devolver_libro(id_libro):
    cursor.execute("SELECT estado FROM Libros WHERE id = %s", (id_libro,))
    libro = cursor.fetchone()

    if libro and libro[0] == 'Prestado':
        cursor.execute("UPDATE Libros SET estado = 'Disponible' WHERE id = %s", (id_libro,))
        conexion.commit()

        cursor.execute("UPDATE Prestamos SET fecha_devolucion = %s WHERE id_libro = %s AND fecha_devolucion IS NULL",
                       (datetime.now().strftime('%Y-%m-%d'), id_libro))
        conexion.commit()

        messagebox.showinfo("Éxito", "Libro devuelto correctamente.")
    else:
        messagebox.showwarning("Error", "Este libro no está prestado.")

def mostrar_libros_disponibles():
    cursor.execute("SELECT id, titulo, autor FROM Libros WHERE estado = 'Disponible'")
    libros = cursor.fetchall()

    ventana = tk.Toplevel()
    ventana.title("Libros Disponibles")
    ventana.geometry("500x300")

    if libros:
        for libro in libros:
            tk.Label(ventana, text=f"ID: {libro[0]}, Título: {libro[1]}, Autor: {libro[2]}").pack()
    else:
        tk.Label(ventana, text="No hay libros disponibles en este momento.").pack()

def mostrar_todos_los_libros():
    cursor.execute("SELECT id, titulo, autor, genero FROM Libros")
    libros = cursor.fetchall()

    ventana = tk.Toplevel()
    ventana.title("Todos los Libros")
    ventana.geometry("500x300")

    if libros:
        for libro in libros:
            tk.Label(ventana, text=f"ID: {libro[0]}, Título: {libro[1]}, Autor: {libro[2]}, Género: {libro[3]}").pack()
    else:
        tk.Label(ventana, text="No hay libros registrados en este momento.").pack()

def mostrar_todos_los_usuarios():
    cursor.execute("SELECT id, nombre, email FROM Usuarios")
    usuarios = cursor.fetchall()

    ventana = tk.Toplevel()
    ventana.title("Todos los Usuarios")
    ventana.geometry("500x300")

    if usuarios:
        for usuario in usuarios:
            tk.Label(ventana, text=f"ID: {usuario[0]}, Nombre: {usuario[1]}, Email: {usuario[2]}").pack()
    else:
        tk.Label(ventana, text="No hay usuarios registrados en este momento.").pack()

def buscar_libro(titulo=None, autor=None, id_libro=None):
    query = "SELECT * FROM Libros WHERE 1=1"
    params = []

    if titulo:
        query += " AND titulo LIKE %s"
        params.append('%' + titulo + '%')
    if autor:
        query += " AND autor LIKE %s"
        params.append('%' + autor + '%')
    if id_libro:
        query += " AND id = %s"
        params.append(id_libro)

    cursor.execute(query, tuple(params))
    libros = cursor.fetchall()

    ventana = tk.Toplevel()
    ventana.title("Buscar Libro")
    ventana.geometry("500x300")

    if libros:
        for libro in libros:
            tk.Label(ventana, text=f"ID: {libro[0]}, Título: {libro[1]}, Autor: {libro[2]}, Género: {libro[3]}").pack()
    else:
        tk.Label(ventana, text="No se encontraron libros con los criterios proporcionados.").pack()


def buscar_usuario(nombre=None, id_usuario=None):
    query = "SELECT * FROM Usuarios WHERE 1=1"
    params = []

    if nombre:
        query += " AND nombre LIKE %s"
        params.append('%' + nombre + '%')
    if id_usuario:
        query += " AND id = %s"
        params.append(id_usuario)

    cursor.execute(query, tuple(params))
    usuarios = cursor.fetchall()

    ventana = tk.Toplevel()
    ventana.title("Buscar Usuario")
    ventana.geometry("500x300")

    if usuarios:
        for usuario in usuarios:
            tk.Label(ventana, text=f"ID: {usuario[0]}, Nombre: {usuario[1]}, Dirección: {usuario[2]}, Teléfono: {usuario[3]}, Email: {usuario[4]}").pack()
    else:
        tk.Label(ventana, text="No se encontraron usuarios con los criterios proporcionados.").pack()



def usuario_existe(id_usuario):
    cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE id = %s", (id_usuario,))
    resultado = cursor.fetchone()
    return resultado[0] > 0


def modificar_cuota(id_usuario, nuevo_monto):
    sql = "UPDATE Pagos SET monto = %s WHERE id_usuario = %s"
    cursor.execute(sql, (nuevo_monto, id_usuario))
    conexion.commit()


def actualizar_cuota(entry_id_usuario, entry_nueva_cuota, resultado_label):
    id_usuario = entry_id_usuario.get()
    nuevo_monto = entry_nueva_cuota.get()

    if id_usuario and nuevo_monto:
        if usuario_existe(id_usuario):
            modificar_cuota(id_usuario, nuevo_monto)
            resultado_label.config(text=f"Cuota de Usuario {id_usuario} actualizada a {nuevo_monto} exitosamente.")
        else:
            resultado_label.config(text=f"Error: El usuario {id_usuario} no existe.")
    else:
        resultado_label.config(text="Por favor, complete ambos campos.")
    
    entry_id_usuario.delete(0, tk.END)
    entry_nueva_cuota.delete(0, tk.END)



def eliminar_libro(id_libro):
    cursor.execute("SELECT * FROM Libros WHERE id = %s", (id_libro,))
    libro = cursor.fetchone()

    if libro:
        cursor.execute("DELETE FROM Libros WHERE id = %s", (id_libro,))
        conexion.commit()
        messagebox.showinfo("Éxito", "Libro eliminado con éxito.")
    else:
        messagebox.showwarning("Error", "El libro con ese ID no existe.")


def eliminar_usuario(id_usuario):
    cursor.execute("SELECT * FROM Usuarios WHERE id = %s", (id_usuario,))
    usuario = cursor.fetchone()

    if usuario:
        cursor.execute("DELETE FROM Usuarios WHERE id = %s", (id_usuario,))
        conexion.commit()
        messagebox.showinfo("Éxito", "Usuario eliminado con éxito.")
    else:
        messagebox.showwarning("Error", "El usuario con ese ID no existe.")




def reporte_morosos():
    try:
        cursor.execute("""
            SELECT Pagos.id_usuario, 
                   Usuarios.nombre, 
                   Pagos.fecha_pago
            FROM Pagos
            JOIN Usuarios ON Pagos.id_usuario = Usuarios.id
            WHERE Pagos.estado = 'pendiente' 
              AND Pagos.fecha_pago < CURDATE()
        """)
        morosos = cursor.fetchall()

        ventana = tk.Toplevel()
        ventana.title("Reporte de Morosos")
        ventana.geometry("500x300")

        if morosos:
            total_meses_retraso = 0
            cantidad_morosidad = 0

            for moroso in morosos:
                id_usuario, nombre_usuario, fecha_pago = moroso
                fecha_pago = datetime.strptime(str(fecha_pago), '%Y-%m-%d')
                today = datetime.today()
                meses_retraso = (today.year - fecha_pago.year) * 12 + today.month - fecha_pago.month

                if meses_retraso > 0:
                    total_meses_retraso += meses_retraso
                    cantidad_morosidad += 1

            if cantidad_morosidad > 0:
                promedio_meses_retraso = total_meses_retraso / cantidad_morosidad
                tk.Label(ventana, text=f"El promedio de meses de retraso de los socios morosos es: {promedio_meses_retraso:.2f} meses.").pack()
            else:
                tk.Label(ventana, text="No hay morosos con retraso en los meses.").pack()
        else:
            tk.Label(ventana, text="No hay morosos en este momento.").pack()

    except Exception as e:
        ventana = tk.Toplevel()
        ventana.title("Error")
        ventana.geometry("500x300")
        tk.Label(ventana, text=f"Error al generar el reporte: {e}").pack()



def ventana_eliminar_usuario():
    def eliminar():
        id_usuario = entry_id_usuario.get()
        if not id_usuario.isdigit():
            messagebox.showwarning("Error", "Por favor, ingrese un ID de usuario válido.")
            return
        eliminar_usuario(int(id_usuario))
    
    ventana = tk.Toplevel()
    ventana.title("Eliminar Usuario")
    ventana.geometry("400x300")
    
    tk.Label(ventana, text="ID Usuario:").pack()
    entry_id_usuario = tk.Entry(ventana)
    entry_id_usuario.pack()
    
    tk.Button(ventana, text="Eliminar", command=eliminar).pack(pady=10)


def ventana_eliminar_libro():
    def eliminar():
        id_libro = entry_id_libro.get()
        if not id_libro.isdigit():
            messagebox.showwarning("Error", "Por favor, ingrese un ID de libro válido.")
            return
        eliminar_libro(int(id_libro))
    
    ventana = tk.Toplevel()
    ventana.title("Eliminar Libro")
    ventana.geometry("400x300")
    
    tk.Label(ventana, text="ID Libro:").pack()
    entry_id_libro = tk.Entry(ventana)
    entry_id_libro.pack()

    tk.Button(ventana, text="Eliminar", command=eliminar).pack(pady=10)


def ventana_modificar():
    ventana_modificar = tk.Toplevel()
    ventana_modificar.title("Modificar Cuota")
    ventana_modificar.geometry("400x300")

    tk.Label(ventana_modificar, text="ID Usuario:").pack(pady=10)
    entry_id_usuario = tk.Entry(ventana_modificar)
    entry_id_usuario.pack()

    tk.Label(ventana_modificar, text="Nueva Cuota:").pack(pady=10)
    entry_nueva_cuota = tk.Entry(ventana_modificar)
    entry_nueva_cuota.pack()

    resultado_label = tk.Label(ventana_modificar, text="", font=("Arial", 10), fg="black")
    resultado_label.pack(pady=10)

    tk.Button(ventana_modificar, text="Actualizar Cuota", 
              command=lambda: actualizar_cuota(entry_id_usuario, entry_nueva_cuota, resultado_label)).pack(pady=20)

def ventana_principal():
    ventana_principal = tk.Tk()
    ventana_principal.title("Ventana Principal")
    ventana_principal.geometry("300x200")

    tk.Button(ventana_principal, text="Modificar Cuota", command=ventana_modificar).pack(pady=50)



def ventana_agregar_usuario():
    def agregar():
        nombre = entry_nombre.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()
        email = entry_email.get()
        monto_cuota = float(entry_monto_cuota.get())  
        fecha_pago = entry_fecha_pago.get()  
        
        agregar_usuario(nombre, direccion, telefono, email, monto_cuota, fecha_pago)
    
    ventana = tk.Toplevel()
    ventana.title("Agregar Usuario")
    ventana.geometry("400x350")
    
    tk.Label(ventana, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack()

    tk.Label(ventana, text="Dirección:").pack()
    entry_direccion = tk.Entry(ventana)
    entry_direccion.pack()
    
    tk.Label(ventana, text="Teléfono:").pack()
    entry_telefono = tk.Entry(ventana)
    entry_telefono.pack()
    
    tk.Label(ventana, text="Email:").pack()
    entry_email = tk.Entry(ventana)
    entry_email.pack()
    
    tk.Label(ventana, text="Monto Cuota:").pack()
    entry_monto_cuota = tk.Entry(ventana)
    entry_monto_cuota.pack()

    tk.Label(ventana, text="Fecha Pago (YYYY-MM-DD):").pack()
    entry_fecha_pago = tk.Entry(ventana)
    entry_fecha_pago.pack()

    tk.Button(ventana, text="Agregar", command=agregar).pack(pady=10)
    
    ventana.mainloop()


def ventana_agregar_libro():
    def agregar():
        titulo = entry_titulo.get()
        autor = entry_autor.get()
        genero = entry_genero.get()
        agregar_libro(titulo, autor, genero)
    
    ventana = tk.Toplevel()
    ventana.title("Agregar Libro")
    ventana.geometry("400x350")
    
    tk.Label(ventana, text="Titulo:").pack()
    entry_titulo = tk.Entry(ventana)
    entry_titulo.pack()

    tk.Label(ventana, text="Autor:").pack()
    entry_autor = tk.Entry(ventana)
    entry_autor.pack()

    tk.Label(ventana, text="Genero:").pack()
    entry_genero = tk.Entry(ventana)
    entry_genero.pack()

    tk.Button(ventana, text="Agregar", command=agregar).pack(pady=10)

def ventana_registrar_prestamo():
    def registrar():
        id_usuario = entry_id_usuario.get()
        id_libro = entry_id_libro.get()
        fecha_prestamo = entry_fecha_prestamo.get()
        fecha_devolucion_pactada = entry_fecha_devolucion.get()

        if not id_usuario.isdigit() or not id_libro.isdigit() or not fecha_prestamo or not fecha_devolucion_pactada:
            messagebox.showwarning("Error", "Por favor, ingrese datos validos.")
            return
        
        registrar_prestamo(int(id_usuario), int(id_libro), fecha_prestamo, fecha_devolucion_pactada)
    
    ventana = tk.Toplevel()
    ventana.title("Registrar Préstamo")
    ventana.geometry("400x300")
    
    tk.Label(ventana, text="ID Usuario:").pack()
    entry_id_usuario = tk.Entry(ventana)
    entry_id_usuario.pack()

    tk.Label(ventana, text="ID Libro:").pack()
    entry_id_libro = tk.Entry(ventana)
    entry_id_libro.pack()

    tk.Label(ventana, text="Fecha de Préstamo (YYYY-MM-DD):").pack()
    entry_fecha_prestamo = tk.Entry(ventana)
    entry_fecha_prestamo.pack()

    tk.Label(ventana, text="Fecha de Devolución Pactada (YYYY-MM-DD):").pack()
    entry_fecha_devolucion = tk.Entry(ventana)
    entry_fecha_devolucion.pack()

    tk.Button(ventana, text="Registrar", command=registrar).pack(pady=10)


def ventana_calcular_multa():
    def calcular():
        id_prestamo = entry_id_prestamo.get()
        fecha_devolucion_real_str = entry_fecha_devolucion_real.get()
        
        if not id_prestamo.isdigit():
            messagebox.showwarning("Error", "Por favor, ingrese un ID de prestamo valido.")
            return
        
        try:
            fecha_devolucion_real = datetime.strptime(fecha_devolucion_real_str, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showwarning("Error", "Por favor, ingrese una fecha valida (formato: YYYY-MM-DD).")
            return
        
        calcular_multa(int(id_prestamo), fecha_devolucion_real)
    
    ventana = tk.Toplevel()
    ventana.title("Calcular Multa")
    ventana.geometry("400x300")
    
    tk.Label(ventana, text="ID Préstamo:").pack()
    entry_id_prestamo = tk.Entry(ventana)
    entry_id_prestamo.pack()
    
    tk.Label(ventana, text="Fecha en la que el cliente devolvio el libro (YYYY-MM-DD):").pack()
    entry_fecha_devolucion_real = tk.Entry(ventana)
    entry_fecha_devolucion_real.pack()
    
    tk.Button(ventana, text="Calcular Multa", command=calcular).pack(pady=10)


def ventana_devolver_libro():
    def devolver():
        id_libro = entry_id_libro.get()
        if not id_libro.isdigit():
            messagebox.showwarning("Error", "Por favor, ingrese un ID de libro valido.")
            return
        devolver_libro(int(id_libro))
    
    ventana = tk.Toplevel()
    ventana.title("Devolver Libro")
    ventana.geometry("400x300")
    
    tk.Label(ventana, text="ID Libro:").pack()
    entry_id_libro = tk.Entry(ventana)
    entry_id_libro.pack()
    
    tk.Button(ventana, text="Devolver", command=devolver).pack(pady=10)

def ventana_buscar_libro():
    def buscar():
        titulo = entry_titulo.get()
        autor = entry_autor.get()
        id_libro = entry_id.get()
        
        buscar_libro(titulo=titulo, autor=autor, id_libro=id_libro)
    
    ventana = tk.Toplevel()
    ventana.title("Buscar Libro")
    ventana.geometry("400x300")
    

    tk.Label(ventana, text="Título:").pack(pady=5)
    entry_titulo = tk.Entry(ventana)
    entry_titulo.pack(pady=5)

    tk.Label(ventana, text="Autor:").pack(pady=5)
    entry_autor = tk.Entry(ventana)
    entry_autor.pack(pady=5)
    
   
    tk.Label(ventana, text="ID de Libro:").pack(pady=5)
    entry_id = tk.Entry(ventana)
    entry_id.pack(pady=5)

    tk.Button(ventana, text="Buscar", command=buscar).pack(pady=10)


def ventana_principal():
    ventana = tk.Tk()
    ventana.title("Biblioteca")
    ventana.geometry("400x400")
    
    tk.Button(ventana, text="1. Agregar Usuario", command=ventana_agregar_usuario).pack(pady=5)
    tk.Button(ventana, text="2. Agregar Libro", command=ventana_agregar_libro).pack(pady=5)
    tk.Button(ventana, text="3. Registrar Préstamo", command=ventana_registrar_prestamo).pack(pady=5)
    tk.Button(ventana, text="4. Ver Multa por Retraso", command=ventana_calcular_multa).pack(pady=5)
    tk.Button(ventana, text="5. Buscar Libro", command=ventana_buscar_libro).pack(pady=5)
    tk.Button(ventana, text="6. Modificar Cuota", command=ventana_modificar).pack(pady=5)
    tk.Button(ventana, text="7. Mostrar Todos los Usuarios", command=mostrar_todos_los_usuarios).pack(pady=5)
    tk.Button(ventana, text="8. Mostrar Todos los Libros", command=mostrar_todos_los_libros).pack(pady=5)
    tk.Button(ventana, text="9. Reporte de Morosos", command=reporte_morosos).pack(pady=5)
    tk.Button(ventana, text="10. Consultar Libros Disponibles", command=mostrar_libros_disponibles).pack(pady=5)
    tk.Button(ventana, text="11. Devolver Libro", command=ventana_devolver_libro).pack(pady=5)
    tk.Button(ventana, text="12. Eliminar Usuario", command=ventana_eliminar_usuario).pack(pady=5)  
    tk.Button(ventana, text="13. Eliminar Libro", command=ventana_eliminar_libro).pack(pady=5)  
    tk.Button(ventana, text="14. Salir", command=ventana.quit).pack(pady=5)

    ventana.mainloop()


ventana_principal()

import sys
import tkinter as tk

def validarUsuario(usuario, codigo):
	archivo = open("usuarios.txt", "r")

	texto = archivo.read()
	palabras = texto.split(";")
	print("ESTO ES",palabras)

	archivo.close()




def recibirC():
	recibirCantidad = tk.Tk()
	recibirCantidad.title("Recibir cantidad")
	recibirCantidad.resizable(False, False)
	recibirCantidad.iconbitmap("cripto.ico")
	recibirCantidad.geometry("600x400+200+100")
	recibirCantidad.config(cursor="hand2")

	LabelMoneda=tk.Label(recibirCantidad, text="Ingrese la moneda",  font=("Arial Bold", 12))
	LabelMoneda.grid(column=0, row=0, sticky="w", padx=20, pady=10)
	textoMoneda=tk.Entry(recibirCantidad)
	textoMoneda.grid(column=1, row=0, sticky="w", padx=20, pady=10)

	LabelCantidad=tk.Label(recibirCantidad, text="Ingrese la cantidad",  font=("Arial Bold", 12))
	LabelCantidad.grid(column=0, row=1, sticky="w", padx=20, pady=10)
	textoCantidad=tk.Entry(recibirCantidad)
	textoCantidad.grid(column=1, row=1, sticky="w", padx=20, pady=10)

	LabelCodigo=tk.Label(recibirCantidad, text="Ingrese el codigo",  font=("Arial Bold", 12))
	LabelCodigo.grid(column=0, row=2, sticky="w", padx=20, pady=10)
	textoCodigo=tk.Entry(recibirCantidad)
	textoCodigo.grid(column=1, row=2, sticky="w", padx=20, pady=10)

	botonEnviardatos = tk.Button(recibirCantidad, text="Enviar datos", font=("Arial Bold", 12))
	botonEnviardatos.grid(column=1, row=3, sticky="w", padx=20, pady=10, columnspan=2)


def Interfaz():
	Sesion.state(newstate="withdraw")
	Interfaz = tk.Tk()
	Interfaz.title("Mi billetera digital")
	Interfaz.resizable(False, False)
	Interfaz.iconbitmap("cripto.ico")
	Interfaz.geometry("600x400+200+100")
	Interfaz.config(cursor="hand2")

	titulo = tk.Label(Interfaz, text="Bienvenido a tu billetera digital", font=("Arial Bold", 18))
	titulo.grid(column=1, row=0, sticky="w", padx=130, pady=20, columnspan=4)

	botonRecibircantidad = tk.Button(Interfaz, text="Recibir cantidad", command=lambda:recibirC(), font=("Arial Bold", 12))
	botonRecibircantidad.grid(column=1, row=3, sticky="w", padx=20, pady=10)

	botonTransferirmonto = tk.Button(Interfaz, text="Transferir monto", font=("Arial Bold", 12))
	botonTransferirmonto.grid(column=1, row=4, sticky="w", padx=20, pady=10)

	botonMostrarbalance_m = tk.Button(Interfaz, text="Mostrar balance una moneda", font=("Arial Bold", 12))
	botonMostrarbalance_m.grid(column=1, row=5, sticky="w", padx=20, pady=10)

	botonMostrarbalance_g = tk.Button(Interfaz, text="Mostrar balance general", font=("Arial Bold", 12))
	botonMostrarbalance_g.grid(column=1, row=6, sticky="w", padx=20, pady=10)

	botonMostrarhistorial = tk.Button(Interfaz, text="Mostrar historico de transacciones", font=("Arial Bold", 12))
	botonMostrarhistorial.grid(column=1, row=7, sticky="w", padx=20, pady=10)

	botonSalir = tk.Button(Interfaz, text="Salir", command=lambda:sys.exit(), font=("Arial Bold", 12))
	botonSalir.grid(column=1, row=9, sticky="e", padx=20, pady=10)


""" Ventana de inicio de sesion del proyecto """
if __name__ == '__main__':
	Sesion= tk.Tk()
	Sesion.title("Mi billetera digital")
	Sesion.resizable(False, False)
	Sesion.iconbitmap("cripto.ico")
	Sesion.geometry("400x250+200+100")
	Sesion.config(cursor="hand2")

	titulo1 = tk.Label(Sesion, text="Bienvenido inicia sesion", font=("Arial Bold", 18))
	titulo1.grid(column=0, row=0, sticky="w", padx=70, pady=20, columnspan=2)

	LabelUsiario=tk.Label(Sesion, text="Usuario",  font=("Arial Bold", 12))
	LabelUsiario.grid(column=0, row=1, sticky="w", padx=20, pady=10)
	textoUsuario=tk.Entry(Sesion)
	textoUsuario.grid(column=1, row=1, sticky="w", padx=20, pady=10)

	LabelCodigo=tk.Label(Sesion, text="Codigo",  font=("Arial Bold", 12))
	LabelCodigo.grid(column=0, row=2, sticky="w", padx=20, pady=10)
	textoCodigo=tk.Entry(Sesion)
	textoCodigo.grid(column=1, row=2, sticky="w", padx=20, pady=10)

	botonIniciar = tk.Button(Sesion, text="Iniciar Sesion", command=lambda:validarUsuario(textoUsuario.get(), textoCodigo.get()), font=("Arial Bold", 12))
	botonIniciar.grid(column=0, row=3, sticky="w", padx=140, pady=30, columnspan=2)

	

	Sesion.mainloop()
 






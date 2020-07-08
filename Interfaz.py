
import sys
import requests
import tkinter as tk
from tkinter import messagebox

_ENDPOINT = "https://api.binance.com"

def validarUsuario(usuario, codigo):
	linea = config_linea(usuario, codigo)
	with open("usuarios.txt", "r") as fichero:
		for f_linea in fichero:
			if linea == f_linea:
				Interfaz(usuario, codigo)
				break


def config_linea(usuario, codigo):
	linea = "Usuario:{} Codigo:{}\n".format(usuario, codigo)
	return linea


def recibirC(codigo):
	recibirCantidad = tk.Toplevel()
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

	botonEnviardatos = tk.Button(recibirCantidad, text="Enviar datos", command=lambda:recibirDatos(str(textoMoneda.get()), textoCantidad.get(), textoCodigo.get(), codigo), font=("Arial Bold", 12))
	botonEnviardatos.grid(column=1, row=3, sticky="w", padx=20, pady=10, columnspan=2)

	botonRegresar = tk.Button(recibirCantidad, text="Regresar", command=recibirCantidad.destroy, font=("Arial Bold", 12))
	botonRegresar.grid(column=2, row=3, sticky="e", padx=20, pady=10)

def _url(api):
    return _ENDPOINT+api

def get_price(cripto):
    return requests.get(_url("/api/v3/ticker/price?symbol="+cripto))


def recibirDatos(monedaR, cantidad, codigoR, codigo):
	monedas=()
	monedas_dict={}	

	COINMARKET_API_KEY = "57c1101b-e4a3-4450-8290-8fd500f00a5a"
	headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': COINMARKET_API_KEY}

	data=requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",headers=headers).json()

	for cripto in data["data"]:
		monedas_dict[cripto["symbol"]]=cripto["name"]

	monedas = monedas_dict.keys()

	if monedaR in monedas:
		print("La moneda existe "+monedaR)
	else:
		messagebox.showwarning("Eror", "Moneda invalida no registrada en coimnmarketcap.com")

	if codigo == codigoR:
		messagebox.showwarning("Eror", "Este codigo pertenece a tu usuario")

	data = get_price(monedaR+"USDT").json()
	print("El precio de",monedaR,"en USD es:",data["price"])

	


def Interfaz(usuario, codigo):
	Sesion.withdraw()
	Interfaz = tk.Toplevel()
	Interfaz.title("Mi billetera digital")
	Interfaz.resizable(False, False)
	Interfaz.iconbitmap("cripto.ico")
	Interfaz.geometry("600x400+200+100")
	Interfaz.config(cursor="hand2")

	titulo = tk.Label(Interfaz, text="Bienvenido a tu billetera digital "+usuario, font=("Arial Bold", 18))
	titulo.grid(column=1, row=0, sticky="w", padx=80, pady=20, columnspan=4)

	botonRecibircantidad = tk.Button(Interfaz, text="Recibir cantidad", command=lambda:recibirC(codigo), font=("Arial Bold", 12))
	botonRecibircantidad.grid(column=1, row=3, sticky="w", padx=20, pady=10)

	botonTransferirmonto = tk.Button(Interfaz, text="Transferir monto", font=("Arial Bold", 12))
	botonTransferirmonto.grid(column=1, row=4, sticky="w", padx=20, pady=10)

	botonMostrarbalance_m = tk.Button(Interfaz, text="Mostrar balance una moneda", font=("Arial Bold", 12))
	botonMostrarbalance_m.grid(column=1, row=5, sticky="w", padx=20, pady=10)

	botonMostrarbalance_g = tk.Button(Interfaz, text="Mostrar balance general", font=("Arial Bold", 12))
	botonMostrarbalance_g.grid(column=1, row=6, sticky="w", padx=20, pady=10)

	botonMostrarhistorial = tk.Button(Interfaz, text="Mostrar historico de transacciones", font=("Arial Bold", 12))
	botonMostrarhistorial.grid(column=1, row=7, sticky="w", padx=20, pady=10)

	botonSalir = tk.Button(Interfaz, text="Cerrar sesion", command=Interfaz.destroy, font=("Arial Bold", 12))
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
	botonIniciar.grid(column=0, row=3, sticky="w", padx=140, pady=20, columnspan=2)

	Sesion.mainloop()
 

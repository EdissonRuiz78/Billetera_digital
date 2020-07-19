import sys
import requests 
import tkinter as tk
import numpy as np
from tkinter import messagebox
from datetime import datetime

#Ruta para uso de API y consulta de criptomonedas
_ENDPOINT = "https://api.binance.com"

#Diccionario de usuarios predeterminado para cada usuario con saldos
diccionario_usuarios = {"100":50000, "200":50000, "300":50000}

""" Clase para manejo de criptomoneda esto codigo no es propio se toma de un ejercicio
	realizado en el curso de Pyhton y programacion orientada a objetos (modificado)"""
class Criptomoneda(object):
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self.cantidad = cantidad

    def cantidad(self, cantidad):  
        self.cantidad=cantidad

    def mostrarNombre(self):
        return self.nombre
    
    def mostrarCantidad(self):  
        return  self.cantidad

""" Funcion para validar usarios predeterminados en un diccionario """
def validarUsuario(codigo):
	if codigo in diccionario_usuarios:
		Interfaz(codigo)
	else:
		messagebox.showwarning("Error", "Usuario no registrado")

""" Funcion para guardar registro de transacciones realizadas por cada usuario """
def guardarTransaccion(operacion, unidades, monedaR, codigoE, moneda_dolares, saldo_nuevo, codigo):
    archivo = open("transacciones_usuario{}.txt".format(codigo),"a")
    date = datetime.now()
    archivo.write("\n" + "Fecha" + ":" + date.strftime("%A %d/%m/%Y %I:%M:%S%p") + " -Transacción" + ": "+ operacion
        + " "+unidades+" unidades de la criptomoneda "+ monedaR + " del usuario "+ "con codigo "+ codigoE 
        + "\n" + "Total en USDT " + ": " + str(moneda_dolares) + " Nuevo saldo en USDT" + ": "+ str(saldo_nuevo))
    archivo.close()

""" Funcion que valida si la persona que envia dinero tiene saldo suficiente ademas actualiza 
	el saldo de la persona que recibe dinero en un diccionario temporal de saldos """ 
def validarSaldo(codigo, codigoE, moneda_dolares, monedaR, cantidad):
	saldo_actual = float(diccionario_usuarios[codigoE])
	if moneda_dolares > saldo_actual:
		messagebox.showwarning("Error", "Transaccion rechazada! valida si el usuario tiene suficiente saldo")
	else:
		saldo_nuevo = diccionario_usuarios[codigo] + moneda_dolares
		messagebox.showwarning("Felicidades", "Transaccion exitosa! Tu nuevo saldo es {} dolares".format(saldo_nuevo))
		diccionario_usuarios[codigo] = saldo_nuevo
		diccionario_usuarios[codigoE] = saldo_actual - moneda_dolares
		guardarTransaccion("recibiste", cantidad, monedaR, codigoE, moneda_dolares, saldo_nuevo, codigo)
		print(diccionario_usuarios)

""" Funcion que valida si el usuario que envia dinero tiene saldo suficiente ademas actualiza 
	el saldo de la persona que recibe y envia dinero en un diccionario temporal de saldos """ 
def enviarDinero(codigo, codigoR, moneda_dolares, monedaE, cantidad):
	saldo_actual = float(diccionario_usuarios[codigo])
	if moneda_dolares > saldo_actual:
		messagebox.showwarning("Error", "Transaccion rechazada! tu saldo no es suficiente")
	else:
		saldo_nuevo = diccionario_usuarios[codigoR] + moneda_dolares
		diccionario_usuarios[codigoR] = saldo_nuevo
		diccionario_usuarios[codigo] = saldo_actual - moneda_dolares
		messagebox.showwarning("Felicidades", "Transaccion exitosa! Haz enviado {:5.2f} dolares, tu nuevo saldo es {:5.2f} dolares"
		.format(moneda_dolares, (saldo_actual - moneda_dolares)))
		guardarTransaccion("enviaste", cantidad, monedaE, codigoR, moneda_dolares, saldo_nuevo, codigo)
		print(diccionario_usuarios)

""" Funcion para crear la URL de consulta para las criptomonedas """
def _url(api):
	return _ENDPOINT+api

""" Funcion para obtener el precio de la criptomoneda usando API requests """
def get_price(cripto):
    return requests.get(_url("/api/v3/ticker/price?symbol="+cripto))

""" Funcion para validar la criptomoneda, cantidad y codigo de quien se recibe dinero """
def recibirDatos(monedaR, cantidad, codigoE, codigo):
	monedas=()
	monedas_dict={}	
	bandera1 = False
	bandera2 = False
	bandera3 = False

	COINMARKET_API_KEY = "57c1101b-e4a3-4450-8290-8fd500f00a5a"
	headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': COINMARKET_API_KEY}

	data = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
		,headers=headers).json()

	for cripto in data["data"]:
		monedas_dict[cripto["symbol"]]=cripto["name"]

	monedas = monedas_dict.keys()

	if monedaR in monedas:
		bandera1 = True
	else:
		messagebox.showwarning("Error", monedaR+" Moneda invalida no registrada en coimnmarketcap.com")

	if codigo != codigoE:
		bandera2 = True
	else:
		messagebox.showwarning("Error", "Este codigo pertenece a tu usuario")

	if codigoE in diccionario_usuarios:
		bandera3 = True
	else:
		messagebox.showwarning("Error", "Codigo de usuario no valido")

	precioMoneda = get_price(monedaR+"USDT").json()
	moneda_dolares = float(precioMoneda["price"])*float(cantidad)

	if bandera1 and bandera2 and bandera3:
		validarSaldo(codigo, codigoE, moneda_dolares, monedaR, cantidad)
	else:
		print("Valida los datos ingresados")

""" Funcion para validar la criptomoneda, cantidad y codigo a quien se envia dinero """
def transferirDinero(monedaE, cantidad, codigoR, codigo):
	monedas=()
	monedas_dict={}	
	bandera1 = False
	bandera2 = False
	bandera3 = False

	COINMARKET_API_KEY = "57c1101b-e4a3-4450-8290-8fd500f00a5a"
	headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': COINMARKET_API_KEY}

	data = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
		,headers=headers).json()

	for cripto in data["data"]:
		monedas_dict[cripto["symbol"]]=cripto["name"]

	monedas = monedas_dict.keys()

	if monedaE in monedas:
		bandera1 = True
	else:
		messagebox.showwarning("Error", monedaE+" Moneda invalida no registrada en coimnmarketcap.com")

	if codigo != codigoR:
		bandera2 = True
	else:
		messagebox.showwarning("Error", "Este codigo pertenece a tu usuario")

	if codigoR in diccionario_usuarios:
		bandera3 = True
	else:
		messagebox.showwarning("Error", "Codigo de usuario no valido")

	precioMoneda = get_price(monedaE+"USDT").json()
	moneda_dolares = float(precioMoneda["price"])*float(cantidad)

	if bandera1 and bandera2:
		enviarDinero(codigo, codigoR, moneda_dolares, monedaE, cantidad)
	else:
		print("Valida los datos ingresados")

""" Interfaz para recibir determinada criptomoneda de determinado codigo de usuario """
def recibirC(codigo):
	recibirCantidad = tk.Toplevel()
	recibirCantidad.title("Recibir cantidad")
	recibirCantidad.resizable(False, False)
	recibirCantidad.iconbitmap("cripto.ico")
	recibirCantidad.geometry("600x400+430+100")
	recibirCantidad.config(cursor="hand2")

	LabelMoneda=tk.Label(recibirCantidad, text="Ingrese la moneda",  font=("Arial Bold", 12))
	LabelMoneda.grid(column=0, row=0, sticky="w", padx=20, pady=10)
	textoMoneda=tk.Entry(recibirCantidad)
	textoMoneda.grid(column=1, row=0, sticky="w", padx=20, pady=10)

	LabelCantidad=tk.Label(recibirCantidad, text="Ingrese la cantidad",  font=("Arial Bold", 12))
	LabelCantidad.grid(column=0, row=1, sticky="w", padx=20, pady=10)
	textoCantidad=tk.Entry(recibirCantidad)
	textoCantidad.grid(column=1, row=1, sticky="w", padx=20, pady=10)

	LabelCodigo=tk.Label(recibirCantidad, text="Ingrese codigo de quien recibe",  font=("Arial Bold", 12))
	LabelCodigo.grid(column=0, row=2, sticky="w", padx=20, pady=10)
	textoCodigo=tk.Entry(recibirCantidad)
	textoCodigo.grid(column=1, row=2, sticky="w", padx=20, pady=10)

	botonEnviardatos = tk.Button(recibirCantidad, text="Enviar datos", command=lambda:recibirDatos(str(textoMoneda.get()), textoCantidad.get(), textoCodigo.get(), codigo), font=("Arial Bold", 12))
	botonEnviardatos.grid(column=1, row=3, sticky="w", padx=20, pady=10, columnspan=2)

	botonRegresar = tk.Button(recibirCantidad, text="Regresar", command=recibirCantidad.destroy, font=("Arial Bold", 12))
	botonRegresar.grid(column=2, row=3, sticky="e", padx=20, pady=10)

""" Interfaz para enviar determinada criptomoneda a determinado codigo de usuario """
def transferirM(codigo):
	transferirMonto = tk.Toplevel()
	transferirMonto.title("Transferir Monto")
	transferirMonto.resizable(False, False)
	transferirMonto.iconbitmap("cripto.ico")
	transferirMonto.geometry("600x400+430+100")
	transferirMonto.config(cursor="hand2")

	LabelMoneda=tk.Label(transferirMonto, text="Ingrese la moneda",  font=("Arial Bold", 12))
	LabelMoneda.grid(column=0, row=0, sticky="w", padx=20, pady=10)
	textoMoneda=tk.Entry(transferirMonto)
	textoMoneda.grid(column=1, row=0, sticky="w", padx=20, pady=10)

	LabelCantidad=tk.Label(transferirMonto, text="Ingrese la cantidad",  font=("Arial Bold", 12))
	LabelCantidad.grid(column=0, row=1, sticky="w", padx=20, pady=10)
	textoCantidad=tk.Entry(transferirMonto)
	textoCantidad.grid(column=1, row=1, sticky="w", padx=20, pady=10)

	LabelCodigo=tk.Label(transferirMonto, text="Ingrese codigo a quien envia",  font=("Arial Bold", 12))
	LabelCodigo.grid(column=0, row=2, sticky="w", padx=20, pady=10)
	textoCodigo=tk.Entry(transferirMonto)
	textoCodigo.grid(column=1, row=2, sticky="w", padx=20, pady=10)

	botonEnviardatos = tk.Button(transferirMonto, text="Transferir dinero", command=lambda:transferirDinero(str(textoMoneda.get()), textoCantidad.get(), textoCodigo.get(), codigo), font=("Arial Bold", 12))
	botonEnviardatos.grid(column=1, row=3, sticky="w", padx=20, pady=10, columnspan=2)

	botonRegresar = tk.Button(transferirMonto, text="Regresar", command=transferirMonto.destroy, font=("Arial Bold", 12))
	botonRegresar.grid(column=2, row=3, sticky="e", padx=20, pady=10)

""" Interfaz principal donde aparecen todas las opciones del programa """
def Interfaz(codigo):
	Interfaz = tk.Toplevel()
	Interfaz.title("Mi billetera digital")
	Interfaz.resizable(False, False)
	Interfaz.iconbitmap("cripto.ico")
	Interfaz.geometry("600x400+430+100")
	Interfaz.config(cursor="hand2")

	titulo = tk.Label(Interfaz, text="Bienvenido a tu billetera digital usuario "+codigo, font=("Arial Bold", 18))
	titulo.grid(column=1, row=0, sticky="w", padx=60, pady=20, columnspan=4)

	botonRecibircantidad = tk.Button(Interfaz, text="Recibir cantidad", command=lambda:recibirC(codigo), font=("Arial Bold", 12))
	botonRecibircantidad.grid(column=1, row=3, sticky="w", padx=20, pady=10)

	botonTransferirmonto = tk.Button(Interfaz, text="Transferir monto", command=lambda:transferirM(codigo), font=("Arial Bold", 12))
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
	Sesion.geometry("400x250+20+100")
	Sesion.config(cursor="hand2")

	titulo1 = tk.Label(Sesion, text="Bienvenido inicia sesion", font=("Arial Bold", 18))
	titulo1.grid(column=0, row=0, sticky="w", padx=70, pady=20, columnspan=2)

	LabelUsiario=tk.Label(Sesion, text="Codigos de usuario",  font=("Arial Bold", 12))
	LabelUsiario.grid(column=0, row=1, sticky="w", padx=20, pady=10)
	LabelUsiarios=tk.Label(Sesion, text="100 - 200 - 300",  font=("Arial Bold", 12))
	LabelUsiarios.grid(column=1, row=1, sticky="w", padx=20, pady=10)

	LabelCodigo=tk.Label(Sesion, text="Ingresa un codigo",  font=("Arial Bold", 12))
	LabelCodigo.grid(column=0, row=2, sticky="w", padx=20, pady=10)
	textoCodigo=tk.Entry(Sesion)
	textoCodigo.grid(column=1, row=2, sticky="w", padx=20, pady=10)

	botonIniciar = tk.Button(Sesion, text="Iniciar Sesion", command=lambda:validarUsuario(textoCodigo.get()), font=("Arial Bold", 12))
	botonIniciar.grid(column=0, row=3, sticky="w", padx=140, pady=20, columnspan=2)

	Sesion.mainloop()
 

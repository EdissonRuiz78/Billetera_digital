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
#Diccionarios para almacenar las monedas recibidas y enviadas de cada usuario
diccionario_monedas1 =  {}
diccionario_monedas2 =  {}
diccionario_monedas3 =  {}

""" Funcion para validar usarios predeterminados en un diccionario """
def validarUsuario(codigo):
	if codigo in diccionario_usuarios:
		return True
	else:
		messagebox.showwarning("Error", "Este codigo de usuario no esta registrado")

""" Funcion para iniciar sesion en el programa """
def iniciarSesion(codigo):
	if validarUsuario(codigo):
		Interfaz(codigo)

""" Funcion para validar si la moneda ingresada esta registrada en coinmarketcap.com usando API"""
def validarMoneda(moneda):
	monedas=()
	monedas_dict={}

	COINMARKET_API_KEY = "57c1101b-e4a3-4450-8290-8fd500f00a5a"
	headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': COINMARKET_API_KEY}

	data = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
		,headers=headers).json()

	for cripto in data["data"]:
		monedas_dict[cripto["symbol"]]=cripto["name"]

	monedas = monedas_dict.keys()

	if moneda in monedas:
		return monedas_dict
	else:
		messagebox.showwarning("Error", moneda+" Moneda invalida no registrada en coinmarketcap.com")

""" Funcion para validar que los codigos de quien recibe y envia no sean iguales """	
def validarCodigo(codigo_envia, codigo_recibe):
	if codigo_envia != codigo_recibe:
		return True
	else:
		messagebox.showwarning("Error", "Este codigo pertenece a tu usuario")

""" Funcion para guardar registro de transacciones realizadas por cada usuario """
def guardarTransaccion(operacion, unidades, moneda_recibida, codigo_envia, moneda_dolares, saldo_nuevo, codigo_recibe):
    archivo = open("transacciones_usuario{}.txt".format(codigo_recibe),"a")
    date = datetime.now()
    archivo.write("Fecha" + ":" + date.strftime("%A %d/%m/%Y %I:%M:%S%p") + " -Transacción" + ": "+ operacion
        + " "+unidades+" unidades "+ moneda_recibida + " usuario "+ "con codigo "+ codigo_envia 
        + "\n" + "Total en USDT " + ": " + str(moneda_dolares) + " Nuevo saldo en USDT" + ": "+ str(saldo_nuevo) + "\n")
    archivo.close()

""" Funcion para actualizar las monedas que reciben los usuario en un diccinario """
def actualizaMoneda(codigo, moneda, cantidad):
	if codigo == "100":
		if moneda in diccionario_monedas1:
			temporal = int(diccionario_monedas1[moneda])
			diccionario_monedas1[moneda] = temporal + int(cantidad)
		else:
			diccionario_monedas1[moneda] = int(cantidad)
		print("Diccionario monedas usuario 100", diccionario_monedas1)

	if codigo == "200":
		if moneda in diccionario_monedas2:
			temporal = int(diccionario_monedas2[moneda])
			diccionario_monedas2[moneda] = temporal + int(cantidad)
		else:
			diccionario_monedas2[moneda] = int(cantidad)
		print("Diccionario monedas usuario 200", diccionario_monedas2)

	if codigo == "300":
		if moneda in diccionario_monedas3:
			temporal = int(diccionario_monedas3[moneda])
			diccionario_monedas3[moneda] = temporal + int(cantidad)
		else:
			diccionario_monedas3[moneda] = int(cantidad)
		print("Diccionario monedas usuario 300", diccionario_monedas3)

""" Funcion que valida si la persona que envia dinero tiene saldo suficiente ademas actualiza 
	el saldo de la persona que recibe dinero en un diccionario temporal de saldos """ 
def validarSaldo(codigo_recibe, codigo_envia, moneda_dolares, moneda_recibida, cantidad):
	saldo_actual = float(diccionario_usuarios[codigo_envia]) #Tomamos el saldo actual del usuario
	if moneda_dolares > saldo_actual: #Validamos que el valor a enviar no sea mayor al saldo que tiene el cliente
		messagebox.showwarning("Error", "Transaccion rechazada! valida si el usuario tiene suficiente saldo")
	else:
		saldo_nuevo = diccionario_usuarios[codigo_recibe] + moneda_dolares # Actualizamos el nuevo saldo del usuario que recibe
		messagebox.showinfo("Felicidades", "Transaccion exitosa! Tu nuevo saldo es {:5.2f} dolares".format(saldo_nuevo))
		diccionario_usuarios[codigo_recibe] = saldo_nuevo
		diccionario_usuarios[codigo_envia] = saldo_actual - moneda_dolares # Al usuario que envia dinero se lo descontamos del saldo
		actualizaMoneda(codigo_recibe, moneda_recibida, cantidad)
		guardarTransaccion("recibiste", cantidad, moneda_recibida, codigo_envia, moneda_dolares, saldo_nuevo, codigo_recibe)
		guardarTransaccion("enviaste", cantidad, moneda_recibida, codigo_recibe, moneda_dolares, saldo_nuevo, codigo_envia)
		print("Saldos de los usuarios", diccionario_usuarios)

""" Funcion que valida si el usuario que envia dinero tiene saldo suficiente ademas actualiza 
	el saldo de la persona que recibe y envia dinero en un diccionario temporal de saldos """ 
def enviarDinero(codigo_envia, codigo_recibe, moneda_dolares, moneda_enviada, cantidad):
	saldo_actual = float(diccionario_usuarios[codigo_envia]) #Tomamos el saldo actual del usuario 
	if moneda_dolares > saldo_actual: #Validamos que el valor a enviar no sea mayor al saldo que tiene el cliente
		messagebox.showwarning("Error", "Transaccion rechazada! tu saldo no es suficiente")
	else:
		saldo_nuevo = diccionario_usuarios[codigo_recibe] + moneda_dolares # Actualizamos el nuevo saldo del usuario que recibe
		diccionario_usuarios[codigo_recibe] = saldo_nuevo				   # el dinero para guardar el nuevo saldo
		diccionario_usuarios[codigo_envia] = saldo_actual - moneda_dolares # Al usuario que envia dinero se lo descontamos del saldo
		messagebox.showinfo("Felicidades", "Transaccion exitosa! Haz enviado {:5.2f} dolares, tu nuevo saldo es {:5.2f} dolares"
																		.format(moneda_dolares, (saldo_actual - moneda_dolares)))
		actualizaMoneda(codigo_recibe, moneda_enviada, cantidad) #Con esta funcion actualizamos las monedas que recibe el usuario
		guardarTransaccion("enviaste", cantidad, moneda_enviada, codigo_recibe, moneda_dolares, saldo_nuevo, codigo_envia)
		guardarTransaccion("recibiste", cantidad, moneda_enviada, codigo_envia, moneda_dolares, saldo_nuevo, codigo_recibe)
		print("Saldos de los usuarios", diccionario_usuarios)

""" Funcion para crear la URL de consulta para las criptomonedas """
def _url(api):
	return _ENDPOINT+api

""" Funcion para obtener el precio de la criptomoneda usando API requests """
def get_price(cripto):
    return requests.get(_url("/api/v3/ticker/price?symbol="+cripto))

""" Funcion para validar la criptomoneda, cantidad y codigo de quien se recibe dinero """
def recibirDatos(moneda_recibida, cantidad, codigo_envia, codigo_recibe):
	bandera1 = False
	diccionario_monedas = validarMoneda(moneda_recibida) #Tomanos un diccionario temporal para almacenar la monedas

	if moneda_recibida in diccionario_monedas:
		bandera1 = True

	if  bandera1 and validarCodigo(codigo_envia, codigo_recibe) and validarUsuario(codigo_envia):
		precioMoneda = get_price(moneda_recibida+"USDT").json() #Se obtiene el valor de la criptomoneda en dolares
		moneda_dolares = float(precioMoneda["price"])*float(cantidad) #Se multiplica el valor de la moneda en dolares por la cantidad
		validarSaldo(codigo_recibe, codigo_envia, moneda_dolares, moneda_recibida, cantidad)
	else:
		print("Valida los datos ingresados")

""" Funcion para validar la criptomoneda, cantidad y codigo a quien se envia dinero """
def transferirDinero(moneda_enviada, cantidad, codigo_recibe, codigo_envia):
	bandera1 = False
	diccionario_monedas = validarMoneda(moneda_enviada) #Tomanos un diccionario temporal para almacenar la monedas

	if moneda_enviada in diccionario_monedas:
		bandera1 = True

	if  bandera1 and validarCodigo(codigo_recibe, codigo_envia) and validarUsuario(codigo_recibe):
		precioMoneda = get_price(moneda_enviada+"USDT").json() #Se obtiene el valor de la criptomoneda en dolares
		moneda_dolares = float(precioMoneda["price"])*float(cantidad) #Se multiplica el valor de la moneda en dolares por la cantidad
		enviarDinero(codigo_envia, codigo_recibe, moneda_dolares, moneda_enviada, cantidad)
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

	botonEnviardatos = tk.Button(recibirCantidad, text="Enviar datos", command=lambda:recibirDatos(str(textoMoneda.get()),
												textoCantidad.get(), textoCodigo.get(), codigo), font=("Arial Bold", 12))
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

	botonEnviardatos = tk.Button(transferirMonto, text="Transferir dinero", command=lambda:transferirDinero(str(textoMoneda.get()),
															textoCantidad.get(), textoCodigo.get(), codigo), font=("Arial Bold", 12))
	botonEnviardatos.grid(column=1, row=3, sticky="w", padx=20, pady=10, columnspan=2)

	botonRegresar = tk.Button(transferirMonto, text="Regresar", command=transferirMonto.destroy, font=("Arial Bold", 12))
	botonRegresar.grid(column=2, row=3, sticky="e", padx=20, pady=10)

""" Interfaz para mostrar el balance de una moneda """
def mostrarBalanceM(codigo):
	mostrarBalancemoneda = tk.Toplevel()
	mostrarBalancemoneda.title("Mostrar balance de una moneda")
	mostrarBalancemoneda.resizable(False, False)
	mostrarBalancemoneda.iconbitmap("cripto.ico")
	mostrarBalancemoneda.geometry("600x400+430+100")
	mostrarBalancemoneda.config(cursor="hand2")
	nombreMoneda = tk.StringVar()
	nombreMoneda.set("")
	cantidadMoneda = tk.StringVar()
	cantidadMoneda.set("")
	totalDolares = tk.StringVar()
	totalDolares.set("")

	def consultaMoneda(moneda):
		diccionario_monedas = validarMoneda(moneda)
		nombreMoneda.set(diccionario_monedas.get(moneda))
		precioMoneda = get_price(moneda+"USDT").json()
		moneda_dolares = float(precioMoneda["price"]) #Se obtiene el valor de la moneda en dolares
		# Se identifica el usuario para consultar el diccionario temporal de monedas a usar segun usuario
		if codigo == "100":
			lista_moneda = diccionario_monedas1
		if codigo == "200":
			lista_moneda = diccionario_monedas2
		if codigo == "300":
			lista_moneda = diccionario_monedas3

		if moneda in lista_moneda: #Recorremos el diccionario para validar si la moneda esta en el diccionario
			cantidadMoneda.set(lista_moneda[moneda]) #Si la encuentra tomamos del diccionario la cantidad de moneda
			totalDolares.set(lista_moneda[moneda] * moneda_dolares) # Finalmente multiplicamos la cantidad de unidades por el total 
		else:
			#En caso tal de que no encuentre la moneda se muestra mensaje indicando que no se ha recibido unidades de esa moneda
			messagebox.showinfo("Informacion", "No has recibido unidades de la moneda {}".format(moneda))
			cantidadMoneda.set(0)
			totalDolares.set(0)

	LabelMoneda=tk.Label(mostrarBalancemoneda, text="Ingrese moneda a consultar",  font=("Arial Bold", 12))
	LabelMoneda.grid(column=0, row=0, sticky="w", padx=20, pady=10)
	textoMoneda=tk.Entry(mostrarBalancemoneda)
	textoMoneda.grid(column=1, row=0, sticky="w", padx=20, pady=10)

	botonEnviardatos = tk.Button(mostrarBalancemoneda, text="Consultar moneda", command=lambda:consultaMoneda(textoMoneda.get()), font=("Arial Bold", 12))
	botonEnviardatos.grid(column=1, row=3, sticky="w", padx=20, pady=10, columnspan=2)

	Labelnombremoneda=tk.Label(mostrarBalancemoneda, text="Nombre moneda",  font=("Arial Bold", 12))
	Labelnombremoneda.grid(column=0, row=4, sticky="w", padx=20, pady=10)
	textonombremoneda=tk.Entry(mostrarBalancemoneda, textvariable=nombreMoneda,  font=("Arial Bold", 12), state="readonly")
	textonombremoneda.grid(column=1, row=4, sticky="w", padx=20, pady=10)

	Labelnombremoneda=tk.Label(mostrarBalancemoneda, text="Cantidad",  font=("Arial Bold", 12))
	Labelnombremoneda.grid(column=0, row=5, sticky="w", padx=20, pady=10)
	textonombremoneda=tk.Entry(mostrarBalancemoneda, textvariable=cantidadMoneda,  font=("Arial Bold", 12), state="readonly")
	textonombremoneda.grid(column=1, row=5, sticky="w", padx=20, pady=10)

	Labelnombremoneda=tk.Label(mostrarBalancemoneda, text="Total en dolares",  font=("Arial Bold", 12))
	Labelnombremoneda.grid(column=0, row=6, sticky="w", padx=20, pady=10)
	textonombremoneda=tk.Entry(mostrarBalancemoneda, textvariable=totalDolares,  font=("Arial Bold", 12), state="readonly")
	textonombremoneda.grid(column=1, row=6, sticky="w", padx=20, pady=10)

	botonRegresar = tk.Button(mostrarBalancemoneda, text="Regresar", command=mostrarBalancemoneda.destroy, font=("Arial Bold", 12))
	botonRegresar.grid(column=2, row=7, sticky="e", padx=20, pady=10)

""" Interfaz para mostrar el balance de cada una de las monedas """
def mostrarBalanceG(codigo):
	mostrarBalancegeneral = tk.Toplevel()
	mostrarBalancegeneral.title("Mostrar balance general")
	mostrarBalancegeneral.resizable(False, False)
	mostrarBalancegeneral.iconbitmap("cripto.ico")
	mostrarBalancegeneral.geometry("600x400+430+100")
	mostrarBalancegeneral.config(cursor="hand2")
	total = tk.StringVar()
	total.set(0)

	LabelGeneral=tk.Label(mostrarBalancegeneral, text="Balance general", font=("Arial Bold", 12))
	LabelGeneral.grid(column=0, row=0, sticky="w", padx=20, pady=10)
	# Se identifica el usuario para consultar el diccionario temporal de monedas a usar segun usuario
	if codigo == "100":
		lista_moneda = diccionario_monedas1
	if codigo == "200":
		lista_moneda = diccionario_monedas2
	if codigo == "300":
		lista_moneda = diccionario_monedas3

	temporal1 = 0
	temporal2 = 0
	temporal3 = 0
	texto = ""
	j = 2
	for key in lista_moneda: #Se recorre el diccionario
		precioMoneda = get_price(key+"USDT").json() #Por cada criptomoneda se usa API para conocer el valor
		moneda_dolares = float(precioMoneda["price"]) #Se toma unicamente el valor de la moneda del archivo json
		diccionario_monedas = validarMoneda(key) #Esta funcion devuelve el diccionario de monedas con nombre y simbolo
		nombreMoneda = diccionario_monedas.get(key) # Para mostrar en ventana se toma unicamente el nombre de moneda
		temporal1 = lista_moneda[key]
		temporal3 = temporal1*moneda_dolares
		temporal2 += temporal1*moneda_dolares
		#En esta linea se genera un texto con nombre moneda, cantidad y total en dolares para mostrarla luego 
		#En un label que se va a generar por cada tipo de moneda guardada en el diccionario
		texto = "Moneda: " + nombreMoneda + "  Cantidad: " + str(temporal1) + "  Total dolares: " + str(temporal3)
		mylabel = tk.Label(mostrarBalancegeneral, text=texto, font=("Arial Bold", 12))
		mylabel.grid(column=0, row=j, sticky="w", padx=20, pady=10)
		j += 1 #La variable j nos sirve como item de aumento para que por cada moneda se genere en un espacio diferente en la malla
		round(temporal2, 2)
		total.set(temporal2)

	labelDolares = tk.Label(mostrarBalancegeneral, text="Total en dolares", font=("Arial Bold", 12))
	labelDolares.grid(column=0, row=6, sticky="e", padx=20, pady=10)
	textoDolares = tk.Entry(mostrarBalancegeneral, textvariable=total, font=("Arial Bold", 12), state="readonly", justify=tk.RIGHT)
	textoDolares.grid(column=0, row=7, sticky="e", padx=20, pady=10)

	botonRegresar = tk.Button(mostrarBalancegeneral, text="Regresar", command=mostrarBalancegeneral.destroy, font=("Arial Bold", 12))
	botonRegresar.grid(column=0, row=8, sticky="e", padx=20, pady=10)

""" Interfaz para mostrar el balance de cada una de las monedas """
def historico(codigo):
	historicoTransacciones = tk.Toplevel()
	historicoTransacciones.title("Historico de transacciones")
	historicoTransacciones.resizable(True, True)
	historicoTransacciones.iconbitmap("cripto.ico")
	historicoTransacciones.geometry("800x680+430+10")
	historicoTransacciones.config(cursor="hand2")
	totalHistorico = tk.StringVar()
	totalHistorico.set("")

	labelHistorico=tk.Label(historicoTransacciones, text="Historico de transacciones", font=("Arial Bold", 12))
	labelHistorico.grid(column=0, row=0, sticky="w", padx=20, pady=10)

	archivo = open("transacciones_usuario{}.txt".format(codigo), "r") #Se lee el archivo de transacciones de cada usuario
	j = 1
	for linea in archivo.readlines():
		mylabel = tk.Label(historicoTransacciones, text=linea, font=("Arial Bold", 12)) #Por cada linea se crea un label con el texto
		mylabel.grid(column=0, row=j, sticky="w", padx=20, pady=10) # Se muestra en la malla de la ventana
		j += 1
	archivo.close()	

	botonRegresar = tk.Button(historicoTransacciones, text="Regresar", command=historicoTransacciones.destroy, font=("Arial Bold", 12))
	botonRegresar.grid(column=0, row=10, sticky="e", padx=20, pady=10)


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

	botonMostrarbalance_m = tk.Button(Interfaz, text="Mostrar balance una moneda", command=lambda:mostrarBalanceM(codigo), font=("Arial Bold", 12))
	botonMostrarbalance_m.grid(column=1, row=5, sticky="w", padx=20, pady=10)

	botonMostrarbalance_g = tk.Button(Interfaz, text="Mostrar balance general", command=lambda:mostrarBalanceG(codigo), font=("Arial Bold", 12))
	botonMostrarbalance_g.grid(column=1, row=6, sticky="w", padx=20, pady=10)

	botonMostrarhistorial = tk.Button(Interfaz, text="Mostrar historico de transacciones", command=lambda:historico(codigo), font=("Arial Bold", 12))
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

	botonIniciar = tk.Button(Sesion, text="Iniciar Sesion", command=lambda:iniciarSesion(textoCodigo.get()), font=("Arial Bold", 12))
	botonIniciar.grid(column=0, row=3, sticky="w", padx=140, pady=20, columnspan=2)

	Sesion.mainloop()
 

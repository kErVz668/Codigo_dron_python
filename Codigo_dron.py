from djitellopy import Tello
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad


# Cálculo de la longitud de la curva
def curve_length(polynomial, a, b):
    derivative = np.polyder(polynomial)
    integrand = lambda x: np.sqrt(1 + (derivative(x))**2)
    length, _ = quad(integrand, a, b)
    return length

# Cálculo del área bajo la curva
def area_under_curve(polynomial, a, b):
    area, _ = quad(polynomial, a, b)
    return area



# Conectar el dron
dron = Tello()
dron.connect()

# Obtener nivel de batería
print(f'Nivel de batería: {dron.get_battery()}%')

# Listas de altura y posición
h_list = [50]
list_z = [40, -80, 60, -50, 35, -30, 30, -35, 50, -60, 80, -40]
x_list = [0]

# Valor constante
x = 40
y = 0

# Despegue del dron
dron.takeoff()


# Recorrer las posiciones y recolectar alturas
for i in list_z:
    dron.go_xyz_speed(x, y, i, 11)
    alt = dron.get_height()
    h_list.append(alt)
    x_list.append(x_list[-1] + x)  # Sumar el valor constante x al último valor de x_list

# Aterrizaje del dron
dron.land()

# Verifica que ambos tengan la misma longitud
if len(x_list) != len(h_list):
    raise ValueError("x_list y h_list deben tener la misma longitud.")

# Ajuste de curva polinómica (por ejemplo, de grado 13)
coefficients = np.polyfit(x_list, h_list, 12)
polynomial = np.poly1d(coefficients)

# Generar valores para la curva ajustada
x_values = np.linspace(min(x_list), max(x_list), 100)
fitted_h_values = polynomial(x_values)

# Plotear los datos originales y la curva ajustada
plt.scatter(x_list, h_list, color='red', label='Datos originales')
plt.plot(x_values, fitted_h_values, color='blue', label='Curva ajustada')
plt.xlabel('Posición X')
plt.ylabel('Altura')
plt.legend()
plt.show()

# Imprimir la ecuación del polinomio
print(f'La ecuación de la curva es: {polynomial}')

# Intervalo de integración
a = x_list[1]
b = x_list[11]

# Calcular la longitud de la curva y el área bajo la curva
length = curve_length(polynomial, a, b)
area = area_under_curve(polynomial, a, b)

print(f'Longitud de la curva: {length:.2f}')
print(f'Área bajo la curva: {area:.2f}')

import streamlit as st
import pandas as pd
import jwt
import csv
from jwt import DecodeError, ExpiredSignatureError

# Clave secreta para firmar el token JWT
SECRET_KEY = "tu_clave_secreta"

# Función para verificar el login y generar un token JWT
def login(username, password):
    try:
        df = pd.read_csv('usuarios.csv')
        if username in df['Usuario'].values and password in df[df['Usuario'] == username]['Contraseña'].values:
            # Generar el token JWT
            payload = {'username': username}
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return token
    except FileNotFoundError:
        st.error("El archivo de usuarios no ha sido encontrado.")
    except Exception as e:
        st.error(f"Error al leer el archivo de usuarios: {e}")
    
    return None

# Función para verificar un token JWT y obtener el username
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except (DecodeError, ExpiredSignatureError):
        return None

# Función para registrar un nuevo usuario
def register(username, password):
    with open('usuarios.csv', mode='a', newline='') as csvfile:
        fieldnames = ['Usuario', 'Contraseña']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Usuario': username, 'Contraseña': password})

def main():
    st.title("Aplicación de Login")

    page = st.sidebar.radio("Seleccione una opción:", ("Login", "Registro", "Recursos Protegidos"))

    if page == "Login":
        st.subheader("Iniciar sesión")
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Iniciar sesión"):
            token = login(username, password)
            if token:
                st.success("Inicio de sesión exitoso!")
                st.text("Tu token JWT:")
                st.text(token)
            else:
                st.error("Usuario o contraseña incorrectos")

    elif page == "Registro":
        st.subheader("Registro")
        new_username = st.text_input("Nuevo usuario")
        new_password = st.text_input("Nueva contraseña", type="password")

        if st.button("Registrarse"):
            register(new_username, new_password)
            st.success("¡Registro exitoso! Por favor inicie sesión.")

    elif page == "Recursos Protegidos":
        st.subheader("Acceso a Recursos Protegidos")
        token = st.text_input("Ingrese su token JWT")

        if st.button("Acceder"):
            username = verify_token(token)
            if username:
                st.success(f"Bienvenido, {username}! Has accedido a recursos protegidos.")
            else:
                st.error("Token inválido o expirado. Acceso denegado.")

if __name__ == "__main__":
    main()

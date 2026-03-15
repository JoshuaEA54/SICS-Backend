# Aquí va la lógica de autenticación

# Aquí va todo lo relacionado con verificar quién es el usuario. 
# En tu caso con Google OAuth, aquí validarías el token que Google te 
# devuelve y extraerías el email y nombre del usuario.

# from google.oauth2 import id_token
# from google.auth.transport import requests

# def verify_google_token(token: str):
#     try:
#         user_info = id_token.verify_oauth2_token(
#             token, requests.Request(), settings.GOOGLE_CLIENT_ID
#         )
#         return user_info  # contiene email, name, etc.
#     except ValueError:
#         return None
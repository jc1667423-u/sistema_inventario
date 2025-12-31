"""
Script para arreglar la contraseña del usuario admin
"""
import bcrypt
from base_datos.config_db import ejecutar_query

print("="*70)
print("ARREGLANDO CONTRASEÑA DEL USUARIO ADMIN")
print("="*70)

# Contraseña que queremos usar
password = "admin123"

# Generar hash correcto
print(f"\n1. Generando hash para la contraseña: {password}")
password_bytes = password.encode('utf-8')
salt = bcrypt.gensalt()
nuevo_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

print(f"   ✅ Hash generado: {nuevo_hash}")

# Verificar que el hash funciona
print(f"\n2. Verificando que el hash es correcto...")
verificacion = bcrypt.checkpw(password.encode('utf-8'), nuevo_hash.encode('utf-8'))
if verificacion:
    print("   ✅ Hash verificado correctamente")
else:
    print("   ❌ Error en la generación del hash")
    exit(1)

# Actualizar en la base de datos
print(f"\n3. Actualizando en la base de datos...")
try:
    query = "UPDATE usuarios SET password_hash = %s WHERE username = 'admin'"
    ejecutar_query(query, (nuevo_hash,), fetch=False)
    print("   ✅ Hash actualizado en la base de datos")
    
    # Verificar
    resultado = ejecutar_query("SELECT password_hash FROM usuarios WHERE username = 'admin'")
    hash_actualizado = resultado[0]['password_hash']
    
    print(f"\n4. Verificando actualización...")
    print(f"   Hash en BD: {hash_actualizado}")
    
    # Probar autenticación
    print(f"\n5. Probando autenticación...")
    es_correcto = bcrypt.checkpw(password.encode('utf-8'), hash_actualizado.encode('utf-8'))
    
    if es_correcto:
        print("   ✅ ¡AUTENTICACIÓN EXITOSA!")
        print("\n" + "="*70)
        print("✅ PROBLEMA SOLUCIONADO")
        print("="*70)
        print(f"Ahora puedes iniciar sesión con:")
        print(f"  Usuario: admin")
        print(f"  Contraseña: {password}")
        print("="*70)
    else:
        print("   ❌ La autenticación aún falla")
        
except Exception as e:
    print(f"   ❌ Error al actualizar: {e}")
    import traceback
    traceback.print_exc()
"""
Diagnóstico completo del problema de login
"""
import sys

print("="*70)
print("DIAGNÓSTICO COMPLETO DEL SISTEMA")
print("="*70)

# 1. Verificar bcrypt
print("\n1. Verificando bcrypt...")
try:
    import bcrypt
    print("   ✅ bcrypt instalado correctamente")
    print(f"   Versión: {bcrypt.__version__ if hasattr(bcrypt, '__version__') else 'N/A'}")
except ImportError:
    print("   ❌ bcrypt NO está instalado")
    print("   Solución: pip install bcrypt")
    sys.exit(1)

# 2. Verificar pymysql
print("\n2. Verificando pymysql...")
try:
    import pymysql
    print("   ✅ pymysql instalado correctamente")
except ImportError:
    print("   ❌ pymysql NO está instalado")
    print("   Solución: pip install pymysql")
    sys.exit(1)

# 3. Verificar conexión a BD
print("\n3. Verificando conexión a base de datos...")
try:
    from base_datos.config_db import ejecutar_query
    resultado = ejecutar_query("SELECT VERSION() as version")
    print(f"   ✅ Conexión exitosa")
    print(f"   Base de datos: {resultado[0]['version']}")
except Exception as e:
    print(f"   ❌ Error de conexión: {e}")
    sys.exit(1)

# 4. Verificar tabla usuarios
print("\n4. Verificando tabla usuarios...")
try:
    resultado = ejecutar_query("SELECT COUNT(*) as total FROM usuarios")
    total = resultado[0]['total']
    print(f"   ✅ Tabla usuarios existe")
    print(f"   Total de usuarios: {total}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# 5. Verificar usuario admin
print("\n5. Buscando usuario 'admin'...")
try:
    resultado = ejecutar_query("SELECT * FROM usuarios WHERE username = 'admin'")
    if resultado:
        user = resultado[0]
        print("   ✅ Usuario 'admin' encontrado")
        print(f"   - ID: {user['id']}")
        print(f"   - Username: {user['username']}")
        print(f"   - Nombre completo: {user['nombre_completo']}")
        print(f"   - Rol: {user['rol']}")
        print(f"   - Activo: {user['activo']}")
        print(f"   - Hash completo: {user['password_hash']}")
        
        # 6. Probar autenticación manualmente
        print("\n6. Probando autenticación con 'admin123'...")
        password_test = "admin123"
        hash_bd = user['password_hash']
        
        # Método 1: usando bcrypt directamente
        print("\n   Método 1: bcrypt directo")
        try:
            es_correcto = bcrypt.checkpw(
                password_test.encode('utf-8'),
                hash_bd.encode('utf-8')
            )
            if es_correcto:
                print("   ✅ Contraseña CORRECTA con bcrypt directo")
            else:
                print("   ❌ Contraseña INCORRECTA con bcrypt directo")
        except Exception as e:
            print(f"   ❌ Error con bcrypt: {e}")
        
        # Método 2: usando la función de utils
        print("\n   Método 2: usando verificar_password de utils")
        try:
            from utilis import verificar_password
            es_correcto = verificar_password(password_test, hash_bd)
            if es_correcto:
                print("   ✅ Contraseña CORRECTA con verificar_password")
            else:
                print("   ❌ Contraseña INCORRECTA con verificar_password")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Método 3: usando la clase Usuario
        print("\n   Método 3: usando Usuario.autenticar")
        try:
            from clases.usuarios import Usuario
            usuario_obj = Usuario.autenticar('admin', password_test)
            if usuario_obj:
                print("   ✅ Autenticación EXITOSA con Usuario.autenticar")
                print(f"   Usuario autenticado: {usuario_obj.nombre_completo}")
            else:
                print("   ❌ Autenticación FALLIDA con Usuario.autenticar")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
    else:
        print("   ❌ Usuario 'admin' NO EXISTE")
        print("\n   Creando usuario admin...")
        
        # Crear usuario admin
        from utilis import hashear_password
        password = "admin123"
        password_hash = hashear_password(password)
        
        query = """
            INSERT INTO usuarios 
            (username, password_hash, nombre_completo, rol, activo, debe_cambiar_password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        ejecutar_query(query, ('admin', password_hash, 'Administrador', 'super_admin', 1, 0), fetch=False)
        print(f"   ✅ Usuario creado con contraseña: {password}")

except Exception as e:
    print(f"   ❌ Error crítico: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("FIN DEL DIAGNÓSTICO")
print("="*70)
print("\nSi todos los checks son ✅ pero sigue fallando el login,")
print("el problema está en la ventana de login.")
print("="*70)
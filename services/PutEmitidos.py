import pandas as pd
from sqlalchemy import text
from services.Querys import salessystem, Session

def load_emitidos(archivo):
    """
    Procesa el archivo de 'Cuadro para Emitir' completado con Guías y Facturas.
    Actualiza la base de datos con los números asignados.
    """
    try:
        # Leer el Excel. Asumimos que la estructura es similar a la generada por get_emitir
        # Puede tener múltiples hojas (una por proveedor), así que leemos todas.
        xls = pd.read_excel(archivo, sheet_name=None, dtype=str)
        
        registros_actualizados = 0
        errores = []

        session = Session()
        
        for sheet_name, df in xls.items():
            # Normalizar nombres de columnas (quitar espacios, mayúsculas)
            df.columns = df.columns.str.strip().str.upper()
            
            # Verificar columnas mínimas necesarias
            if not {'CUI', 'GUIA', 'FACTURA'}.issubset(df.columns):
                continue # Saltar hojas que no tengan la estructura esperada
            
            # Filtrar filas que tengan CUI y (GUIA o FACTURA)
            df_validos = df.dropna(subset=['CUI'])
            df_validos = df_validos[
                (df_validos['GUIA'].notna() & (df_validos['GUIA'] != '')) | 
                (df_validos['FACTURA'].notna() & (df_validos['FACTURA'] != ''))
            ]

            for index, row in df_validos.iterrows():
                cui = row['CUI']
                guia = row['GUIA'] if pd.notna(row['GUIA']) else None
                factura = row['FACTURA'] if pd.notna(row['FACTURA']) else None
                
                # Intentar separar cod_pedido y cuo del CUI si es necesario, 
                # pero si la tabla tiene CUI o clave compuesta, usamos eso.
                # Asumiendo que la tabla 'facturas' tiene cod_pedido y cuo como PK,
                # y que CUI = cod_pedido + cuo (como string).
                # Esto puede ser delicado si el largo del cod_pedido varía.
                # Estrategia segura: Buscar por concatenación en la BD o asumir estructura fija.
                
                # Opción A: Update directo usando SQL crudo para flexibilidad
                # Actualizamos tabla FACTURAS
                query_facturas = text("""
                    UPDATE facturas 
                    SET guia = :guia, numero = :factura, estado = 'TERMINADO'
                    WHERE CONCAT(cod_pedido, cuo) = :cui
                """)
                
                # Actualizamos tabla REMISION_REMITENTE (si aplica)
                query_remision = text("""
                    UPDATE remision_remitente
                    SET factura = :factura, numero = :guia, estado = 'TERMINADO'
                    WHERE CONCAT(cod_pedido, cuo) = :cui
                """)

                try:
                    session.execute(query_facturas, {'guia': guia, 'factura': factura, 'cui': cui})
                    session.execute(query_remision, {'guia': guia, 'factura': factura, 'cui': cui})
                    registros_actualizados += 1
                except Exception as e:
                    errores.append(f"Error en CUI {cui}: {str(e)}")

        session.commit()
        session.close()

        if errores:
            return f"Proceso completado con {registros_actualizados} actualizaciones. Errores: {len(errores)}"
        return f"Éxito: Se actualizaron {registros_actualizados} registros correctamente."

    except Exception as e:
        return f"Error crítico al procesar el archivo: {str(e)}"

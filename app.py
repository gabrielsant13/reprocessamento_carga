import cx_Oracle
from tkinter import messagebox
import customtkinter as ctk

def valid_insert():
    numero = numero_entry.get()
    
    try:
        #conecta ao banco de dados
        connection = cx_Oracle.connect("user", "password", "host:port/service_name")
        cursor = connection.cursor()

        # Consulta no banco de dados Oracle para visualizar
        query = "select  ID_PK, VALOR_NEW, to_char(DATA_ALT, 'dd/mm/yy hh:mi:ss') AS DATA_ALT,  CAMPO_ALT from multisoftware_int_erp where id_pk = :numero and SN_INT_REG in ('S','E')"
        cursor.execute(query, {'numero': numero})
        resultado = cursor.fetchall()
        
        #retorno para a funcao reprocessar_numero(), verifica se o id existe
        if not resultado:
           return 1
       
        #se encontrar o id    
        else:                
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                
            return 0
        
    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        
        
#funcao para consultar informacoes do ID
def consultar_numero():
    numero = numero_entry.get()
    
    try:
        #conecta ao banco de dados
        connection = cx_Oracle.connect("user", "password", "host:port/service_name")
        cursor = connection.cursor()

        # Consulta no banco de dados Oracle para visualizar
        query = "select  ID_PK, VALOR_NEW, to_char(DATA_ALT, 'dd/mm/yy hh:mi:ss') AS DATA_ALT,  CAMPO_ALT from multisoftware_int_erp where id_pk = :numero and SN_INT_REG in ('S','E')"
        cursor.execute(query, {'numero': numero})
        resultado = cursor.fetchall()

        #se nao encontrar o id
        if not resultado:
            messagebox.showinfo("Consulta", "Nenhum resultado encontrado.")
            
            return 1
        
        #se encontrar o id    
        else:
            for linha in resultado:                
                messagebox.showwarning("Resultado da Consulta", "ID: " + str(linha[0]) + "\nCARGA: " + str(linha[1]) + "\nDATA: " + str(linha[2]) + "\nCAMPO DE PROCESSAMENTO: " + str(linha[3]))
                
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
                
            return 0

    except cx_Oracle.DatabaseError as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
 
#funcao para reprocessar o id            
def reprocessar_numero():
    #ler a informacao do campo
    id_pk = numero_entry.get()
    valid = valid_insert()
    
    if valid == 0:
    
        try:
            connection = cx_Oracle.connect("user", "password", "host:port/service_name")
            cursor = connection.cursor()
            
            #insert para novo processamento
            insert_query = "INSERT INTO MULTISOFTWARE_INT_ERP (EMPRESA_FAT, EMPRESA_LOG,DATA_ALT,VALOR_OLD,VALOR_NEW,CAMPO_ALT)(SELECT EMPRESA_FAT,EMPRESA_LOG,DATA_ALT,'REENVIO',VALOR_NEW,CAMPO_ALT FROM MULTISOFTWARE_INT_ERP WHERE ID_PK = " + id_pk + ")"
            cursor.execute(insert_query)
            
            connection.commit()

            messagebox.showwarning("Reprocessamento","REPROCESSAMENTO DO ID " + id_pk + " CONCLUIDO, VERIFIQUE A ROTINA DE LOG DE INTEGRAÇÃO 8078 UTILIZANDO O NUMERO DE CARGA")
            
        except Exception as e:
            messagebox.showwarning("Reprocessamento","Erro no processamento do ID " + id_pk + " VERIFIQUE A ROTINA DE LOG DE INTEGRAÇÃO 8078 UTILIZANDO O NUMERO DE CARGA")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                
            #comando para limpar o campo de digitar id
            numero_entry.delete(0, 'end')
            return
                
    else:
        messagebox.showwarning("Erro de reprocessamento","ID " + id_pk + " NAO ENCONTRADO. VERIFIQUE A ROTINA DE LOG DE INTEGRAÇÃO.")
        return    
        
        
# Criação da janela
window = ctk.CTk()
window.title("DCL Envio Manual HML v1.0")
window.geometry("350x300")
window.resizable(False, False)
ctk.set_appearance_mode("light") 

# Campo de entrada para o número
numero_label = ctk.CTkLabel(window, text="ID_PK para processamento:")
numero_label.pack()
numero_entry = ctk.CTkEntry(master=window,
                               placeholder_text="ID_PK",
                               width=150,
                               height=30,
                               border_width=2,
                               corner_radius=10)
numero_entry.pack()

# Botão de consulta
consultar_button = ctk.CTkButton(window, text="Consultar", command=consultar_numero)
consultar_button.pack(pady=10)

# Botão de reprocesso
id_pk = numero_entry.get()
consultar_button = ctk.CTkButton(window, text="Reprocessar", command=reprocessar_numero)
consultar_button.pack(pady=5)

window.mainloop()

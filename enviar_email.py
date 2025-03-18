import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email_recuperacao(destinatario, link_recuperacao):
    remetente = "seu_email@gmail.com"
    senha = "sua_senha_do_email"

    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = "Recuperação de Senha"
    
    corpo = f"""
    Olá,
    
    Para recuperar sua senha, clique no seguinte link:
    {link_recuperacao}
    
    Se você não solicitou a recuperação de senha, por favor, ignore este e-mail.
    
    Atenciosamente,
    Estaciona Fácil
    """
    
    mensagem.attach(MIMEText(corpo, 'plain'))
    
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls() 
        servidor.login(remetente, senha)  
        texto = mensagem.as_string()  
        servidor.sendmail(remetente, destinatario, texto)  
        servidor.quit()  
        print(f"E-mail enviado com sucesso para {destinatario}")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

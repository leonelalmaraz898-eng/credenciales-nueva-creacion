import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

st.set_page_config(page_title="Nueva Creación - Recolección", layout="centered")
st.title("🎒 Jardín Nueva Creación")
st.subheader("Formulario para Credencial 2025-2026")

with st.form("form_credencial"):
    st.markdown("### Datos del Alumno")
    nombre = st.text_input("Nombre completo del alumno*")
    categoria = st.selectbox("Categoría", ["1ro", "2do", "3ro", "Maternal"])
    ciclo = st.text_input("Ciclo", "2025-2026")
    curp = st.text_input("CURP")
    maestro = st.text_input("Maestro/a")
    sangre = st.text_input("Tipo de sangre")
    alergias = st.text_input("Alergias")

    st.markdown("### Datos del Tutor")
    tutor = st.text_input("Nombre del tutor*")
    whatsapp = st.text_input("WhatsApp (10 dígitos)*")

    st.markdown("### Fotos en JPG/PNG*")
    foto_alumno = st.file_uploader("1. FOTO ALUMNO", type=["jpg","jpeg","png"])
    foto_tutor = st.file_uploader("2. FOTO TUTOR", type=["jpg","jpeg","png"])
    foto_qr = st.file_uploader("3. CAPTURA QR WHATSAPP TUTOR", type=["jpg","jpeg","png"])

    enviar = st.form_submit_button("📨 ENVIAR TODO", type="primary")

if enviar:
    if not nombre or not tutor or not foto_alumno or not foto_tutor or not foto_qr:
        st.error("❌ Faltan datos obligatorios")
    else:
        try:
            msg = MIMEMultipart()
            msg['From'] = st.secrets["EMAIL_USER"]
            msg['To'] = st.secrets["TO_EMAIL"]
            msg['Subject'] = f"CREDENCIAL - {nombre} - {categoria}"

            cuerpo = f"""
            NUEVA CREDENCIAL
            Fecha: {datetime.now()}
            Alumno: {nombre}
            Categoria: {categoria}
            Ciclo: {ciclo}
            CURP: {curp}
            Maestro: {maestro}
            Sangre: {sangre}
            Alergias: {alergias}
            Tutor: {tutor}
            WhatsApp: {whatsapp}
            """
            msg.attach(MIMEText(cuerpo, 'plain'))

            for archivo, nombre_archivo in [(foto_alumno, f"1_ALUMNO_{nombre}.jpg"), (foto_tutor, f"2_TUTOR_{nombre}.jpg"), (foto_qr, f"3_QR_{nombre}.jpg")]:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(archivo.getvalue())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{nombre_archivo}"')
                msg.attach(part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(st.secrets["EMAIL_USER"], st.secrets["EMAIL_PASSWORD"])
            server.send_message(msg)
            server.quit()

            st.success(f"✅ ¡Gracias {tutor}! Datos de {nombre} enviados correctamente.")
            st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")

st.caption("Datos llegan a leonelalmaraz898@gmail.com")

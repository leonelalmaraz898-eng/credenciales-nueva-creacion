import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

st.set_page_config(page_title="Nueva Creación - Recolección", layout="centered")
st.title("🎒 Jardín Nueva Creación")
st.subheader("Formulario para Credencial 2026-2027")

with st.form("form_credencial"):
    st.markdown("### Datos del Alumno")
    nombre = st.text_input("Nombre completo del alumno*")
    categoria = st.selectbox("Categoría", ["1ro", "2do", "3ro"])
    ciclo = st.text_input("Ciclo Escolar", value="2026-2027")
    curp = st.text_input("CURP")
    maestro = st.text_input("Nombre del Maestro/a")
    director = st.text_input("Nombre del Director/a")
    sangre = st.text_input("Tipo de sangre")
    alergias = st.text_input("Alergias")

    st.markdown("### Datos del Tutor")
    nombre_tutor = st.text_input("Nombre del tutor*")
    dirección_tutor = st.text_input("Dirección del Tutor")
    whatsapp_tutor = st.text_input("WhatsApp Tutor (10 dígitos)*")

    st.markdown("### Datos de la persona autorizada")
    nombre_autorizada = st.text_input("Nombre completo de la persona autorizada")
    whatsapp_autorizada = st.text_input("Whatsapp persona autorizada (10 dígitos)*")

    st.markdown("### Fotos en JPG/PNG*")
    foto_alumno = st.file_uploader("1. FOTO ALUMNO", type=["jpg","jpeg","png"])
    foto_tutor = st.file_uploader("2. FOTO TUTOR", type=["jpg","jpeg","png"])
    foto_persona_autorizada = st.file_uploader("3. FOTO PERSONA AUTORIZADA", type=["jpg","jpeg","png"])
    foto_qr = st.file_uploader("4. CAPTURA QR WHATSAPP TUTOR", type=["jpg","jpeg","png"])

    enviar = st.form_submit_button("📨 ENVIAR TODO", type="primary")

if enviar:
    if not nombre or not nombre_tutor or not foto_alumno or not foto_tutor or not foto_persona_autorizada or not foto_qr:
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
            Director: {director}
            Sangre: {sangre}
            Alergias: {alergias}
            Tutor: {nombre_tutor}
            Dirección: {dirección_tutor}
            WhatsApp Tutor: {whatsapp_tutor}
            Persona Autorizada: {nombre_autorizada}
            WhatsApp Autorizada: {whatsapp_autorizada}
            """
            msg.attach(MIMEText(cuerpo, 'plain'))

            for archivo, nombre_archivo in [(foto_alumno, f"1_ALUMNO_{nombre}.jpg"), (foto_tutor, f"2_TUTOR_{nombre}.jpg"), (foto_persona_autorizada_, f"3_Persona_Autorizada_{nombre}.jpg"), (foto_qr, f"4_QR_{nombre}.jpg")]:
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

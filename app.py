import streamlit as st
import qrcode
from PIL import Image
import io

st.set_page_config(page_title="Credenciales Nueva Creación", page_icon="🎒")
st.title('🎒 Jardín "Nueva Creación" - Rellena tus datos')

# --- FORMULARIO ---
nombre = st.text_input("Nombre del estudiante", "ABDIEL JOSUE ROMERO ALMARAZ")
grado = st.text_input("Grado", "3°")
ciclo = st.text_input("Ciclo Escolar", "2025-2026")
curp = st.text_input("CURP", "ROAA210605HOCMLBA9")
maestro = st.text_input("Maestro", "Mtra. Elizabeth Velázquez Martínez")
sangre = st.text_input("Tipo de sangre", "O+")
alergias = st.text_input("Alergias", "Ninguna")
tutor = st.text_input("Nombre del tutor", "GABRIELA BEATRIZ ALMARAZ GARCIA")
telefono = st.text_input("WhatsApp (10 dígitos)", "9511991046")
direccion = st.text_input("Dirección", "Priv. de Puerto Escondido, Rivera de San Jeronimo Yahuiche")

foto_est = st.file_uploader("Foto estudiante", type=["jpg","png","jpeg"])
foto_tutor = st.file_uploader("Foto tutor", type=["jpg","png","jpeg"])

if st.button("✨ Generar Credencial con QR Real"):
    # QR REAL
    qr = qrcode.QRCode(box_size=10, border=1)
    qr.add_data(f"https://wa.me/52{telefono}")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").resize((300,300))

    st.success("✅ ¡Listo! Ahora descarga y mándasela a la maestra")
    st.image(qr_img, caption=f"QR de {tutor}")

    # Mostrar resumen
    st.subheader("FRENTE")
    st.write(f"**{nombre}** - Grado: {grado} - CURP: {curp}")
    if foto_est: st.image(foto_est, width=150)

    st.subheader("REVERSO")
    st.write(f"Tutor: {tutor} - Tel: {telefono}")
    if foto_tutor: st.image(foto_tutor, width=150)

    # Botón para descargar QR
    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    st.download_button("📥 Descargar Credencial / QR", buf.getvalue(), f"credencial_{nombre}.png", "image/png")
    st.info("👉 Descarga la imagen y mándala por WhatsApp al grupo de la escuela")
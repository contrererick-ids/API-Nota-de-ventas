from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

def generar_pdf(cliente, nota) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("NOTA DE VENTA", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Información del cliente
    elements.append(Paragraph("Información del Cliente", styles["Heading2"]))
    cliente_data = [
        ["Razón Social:", cliente.razon_social],
        ["Nombre Comercial:", cliente.nombre_comercial or "N/A"],
        ["RFC:", cliente.rfc],
        ["Correo:", cliente.correo],
        ["Teléfono:", cliente.telefono or "N/A"],
    ]
    tabla_cliente = Table(cliente_data, colWidths=[150, 350])
    tabla_cliente.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(tabla_cliente)
    elements.append(Spacer(1, 12))

    # Información de la nota
    elements.append(Paragraph("Información de la Nota", styles["Heading2"]))
    nota_data = [
        ["Folio:", nota.folio],
    ]
    tabla_nota = Table(nota_data, colWidths=[150, 350])
    tabla_nota.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(tabla_nota)
    elements.append(Spacer(1, 12))

    # Contenido de la nota
    elements.append(Paragraph("Contenido de la Nota", styles["Heading2"]))
    contenido_header = [["Cantidad", "Producto", "Precio Unitario", "Importe"]]
    contenido_data = [
        [
            str(item.cantidad),
            item.producto.nombre,
            f"${item.precio_unitario:.2f}",
            f"${item.importe:.2f}"
        ]
        for item in nota.contenido
    ]
    contenido_footer = [["", "TOTAL", "", f"${nota.total:.2f}"]]

    tabla_contenido = Table(
        contenido_header + contenido_data + contenido_footer,
        colWidths=[80, 250, 100, 100]
    )
    tabla_contenido.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.lightgrey]),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("LINEABOVE", (0, -1), (-1, -1), 1, colors.black),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(tabla_contenido)

    doc.build(elements)
    buffer.seek(0)
    return buffer.read()
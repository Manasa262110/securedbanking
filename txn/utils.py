from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import FileResponse

def generate_receipt_pdf(txn):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Transaction Receipt")

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 100, f"Transaction ID: {txn.id}")
    p.drawString(50, height - 120, f"From Account: {txn.from_account}")
    p.drawString(50, height - 140, f"To Account: {txn.to_account}")
    p.drawString(50, height - 160, f"Type: {txn.txntype}")
    p.drawString(50, height - 180, f"Amount: ₹{txn.amount}")
    p.drawString(50, height - 200, f"Timestamp: {txn.time.strftime('%Y-%m-%d %H:%M:%S')}")

    p.drawString(50, height - 250, "Thank you for using our service.")

    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f"txn_{txn.id}_receipt.pdf")

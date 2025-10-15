from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import pandas as pd, random, os
from faker import Faker

faker = Faker()
base = "data/sap_tables"
out_dir = "data/incoming_invoices/pdf"
os.makedirs(out_dir, exist_ok=True)

ekpo = pd.read_csv(f"{base}/EKPO.csv")
ekko = pd.read_csv(f"{base}/EKKO.csv")
lfa1 = pd.read_csv(f"{base}/LFA1.csv")

invoice_records = []
num_invoices = 100

print(f"Generating {num_invoices} realistic invoices with intentional mismatches...")

for i in range(num_invoices):
    po_header = ekko.sample(1).iloc[0]
    vendor = lfa1[lfa1["LIFNR"] == po_header["LIFNR"]].iloc[0]
    po_items = ekpo[ekpo["EBELN"] == po_header["EBELN"]]

    # mix single/multi-line
    if len(po_items) > 1 and random.random() > 0.4:
        selected_lines = po_items.sample(random.randint(2, min(4, len(po_items))))
    else:
        selected_lines = po_items.sample(1)

    invoice_no = f"INV_{faker.random_int(50000,99999)}"
    invoice_date = faker.date_between(start_date="-30d", end_date="today")
    currency = po_header["WAERS"]
    pdf_file = f"{out_dir}/{invoice_no}_{vendor['LIFNR']}.pdf"

    # --- mismatch flags ---
    mismatch_type = random.choices(
        ["full", "partial", "no_match"],
        weights=[0.6, 0.25, 0.15],
        k=1
    )[0]

    c = canvas.Canvas(pdf_file, pagesize=A4)
    width, height = A4
    y = height - inch
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y, f"INVOICE: {invoice_no}")
    y -= 0.3*inch
    c.setFont("Helvetica", 11)
    c.drawString(1*inch, y, f"Vendor: {vendor['NAME1']} ({vendor['LIFNR']})")
    y -= 0.2*inch
    c.drawString(1*inch, y, f"PO Number: {po_header['EBELN']}")
    y -= 0.2*inch
    c.drawString(1*inch, y, f"Invoice Date: {invoice_date}")
    y -= 0.3*inch

    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y, "Material")
    c.drawString(2.5*inch, y, "Qty")
    c.drawString(3.5*inch, y, "Unit Price")
    c.drawString(5*inch, y, "Line Total")
    y -= 0.2*inch
    c.line(1*inch, y, 6.5*inch, y)
    y -= 0.2*inch
    c.setFont("Helvetica", 10)

    total_amount = 0

    for _, line in selected_lines.iterrows():
        qty = line["MENGE"]
        price = line["NETPR"]
        matnr = line["MATNR"]

        if mismatch_type == "partial":
            # random tweak qty or price
            if random.random() > 0.5:
                qty = round(qty * random.uniform(0.7, 1.3), 2)
            else:
                price = round(price * random.uniform(0.8, 1.2), 2)
        elif mismatch_type == "no_match":
            # wrong PO/material combo
            matnr = f"X{faker.random_int(100,999)}"

        line_total = round(qty * price, 2)
        total_amount += line_total

        c.drawString(1*inch, y, str(matnr))
        c.drawString(2.5*inch, y, str(qty))
        c.drawString(3.5*inch, y, str(price))
        c.drawString(5*inch, y, str(line_total))
        y -= 0.25*inch

        invoice_records.append({
            "Invoice_No": invoice_no,
            "Vendor_ID": vendor["LIFNR"],
            "PO_Number": po_header["EBELN"],
            "Material": matnr,
            "Qty": qty,
            "Price": price,
            "Total": line_total,
            "Currency": currency,
            "Invoice_Date": invoice_date,
            "Mismatch_Type": mismatch_type
        })

        if y < 1*inch:
            c.showPage()
            y = height - inch
            c.setFont("Helvetica", 10)

    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y, f"TOTAL INVOICE AMOUNT: {round(total_amount,2)} {currency}")
    c.save()

csv_path = "data/incoming_invoices/invoice_reference_mismatched.csv"
pd.DataFrame(invoice_records).to_csv(csv_path, index=False)
print(f"✅ Created {num_invoices} invoices with realistic errors.")
print(f"📄 Reference CSV saved at {csv_path}")

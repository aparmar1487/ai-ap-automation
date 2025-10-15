from faker import Faker
import pandas as pd, random, os, datetime

faker = Faker()
base = "data/sap_tables"
os.makedirs(base, exist_ok=True)

# ---------- Vendor master ----------
vendors = [
    {"LIFNR": f"V{1000+i}", "NAME1": faker.company(), "LAND1": faker.country_code()}
    for i in range(10)
]
df_lfa1 = pd.DataFrame(vendors)
df_lfa1.to_csv(f"{base}/LFA1.csv", index=False)

# Company Code Data (LFB1)
lfb1 = [
    {"LIFNR": v["LIFNR"], "BUKRS": "1000", "ZUAWA": random.choice(["001", "002", "003"])}
    for v in vendors
]
pd.DataFrame(lfb1).to_csv(f"{base}/LFB1.csv", index=False)

# ---------- PO Header (EKKO) ----------
pos = [
    {
        "EBELN": f"45{1000+i}",
        "LIFNR": random.choice(vendors)["LIFNR"],
        "BEDAT": faker.date_between(start_date="-120d", end_date="today"),
    }
    for i in range(30)
]
df_ekko = pd.DataFrame(pos)
df_ekko.to_csv(f"{base}/EKKO.csv", index=False)

# ---------- PO Items (EKPO) ----------
materials = [f"M{faker.random_int(100,999)}" for _ in range(20)]
po_items = []
for po in pos:
    for _ in range(random.randint(1,3)):
        mat = random.choice(materials)
        qty = random.randint(1,10)
        price = round(random.uniform(50,500),2)
        po_items.append({
            "EBELN": po["EBELN"],
            "EBELP": faker.random_int(10,99),
            "MATNR": mat,
            "MENGE": qty,
            "NETPR": price,
            "PEINH": 1,
            "WERKS": "US01"
        })
df_ekpo = pd.DataFrame(po_items)
df_ekpo.to_csv(f"{base}/EKPO.csv", index=False)

# ---------- GR (MKPF / MSEG) ----------
gr_headers, gr_items = [], []
for i, po_item in enumerate(random.sample(po_items, 40)):
    mblnr = f"50{2000+i}"
    gr_date = faker.date_between(start_date="-90d", end_date="today")
    gr_headers.append({"MBLNR": mblnr, "BUDAT": gr_date})
    gr_items.append({
        "MBLNR": mblnr,
        "EBELN": po_item["EBELN"],
        "EBELP": po_item["EBELP"],
        "MATNR": po_item["MATNR"],
        "MENGE": po_item["MENGE"],
        "DMBTR": po_item["MENGE"] * po_item["NETPR"]
    })
pd.DataFrame(gr_headers).to_csv(f"{base}/MKPF.csv", index=False)
pd.DataFrame(gr_items).to_csv(f"{base}/MSEG.csv", index=False)

# ---------- PO History (EKBE) ----------
ekbe = []
for item in gr_items:
    ekbe.append({
        "EBELN": item["EBELN"],
        "EBELP": item["EBELP"],
        "VGABE": 1,  # GR
        "MATNR": item["MATNR"],
        "MENGE": item["MENGE"],
        "DMBTR": item["DMBTR"],
        "BUDAT": faker.date_between(start_date="-90d", end_date="today")
    })
for po_item in random.sample(po_items, 20):
    ekbe.append({
        "EBELN": po_item["EBELN"],
        "EBELP": po_item["EBELP"],
        "VGABE": 2,  # Invoice Receipt
        "MATNR": po_item["MATNR"],
        "MENGE": po_item["MENGE"],
        "DMBTR": po_item["MENGE"] * po_item["NETPR"],
        "BUDAT": faker.date_between(start_date="-60d", end_date="today")
    })
pd.DataFrame(ekbe).to_csv(f"{base}/EKBE.csv", index=False)

# ---------- Invoice Header / Items ----------
invoices, items = [], []
for i, po_item in enumerate(random.sample(po_items, 20)):
    inv_no = f"51{2000+i}"
    vendor = df_ekko[df_ekko["EBELN"] == po_item["EBELN"]]["LIFNR"].values[0]
    invoices.append({
        "BELNR": inv_no,
        "LIFNR": vendor,
        "BUDAT": faker.date_between(start_date="-60d", end_date="today")
    })
    items.append({
        "BELNR": inv_no,
        "EBELN": po_item["EBELN"],
        "EBELP": po_item["EBELP"],
        "MATNR": po_item["MATNR"],
        "MENGE": po_item["MENGE"],
        "WRBTR": round(po_item["MENGE"] * po_item["NETPR"],2)
    })
df_rbkp = pd.DataFrame(invoices)
df_rseg = pd.DataFrame(items)
df_rbkp.to_csv(f"{base}/RBKP.csv", index=False)
df_rseg.to_csv(f"{base}/RSEG.csv", index=False)

# ---------- Accounting (BKPF / BSEG) ----------
bkpf, bseg = [], []
for inv in invoices:
    bkpf.append({
        "BELNR": inv["BELNR"],
        "BUKRS": "1000",
        "LIFNR": inv["LIFNR"],
        "BLDAT": inv["BUDAT"]
    })
    bseg.append({
        "BELNR": inv["BELNR"],
        "BUZEI": 1,
        "WRBTR": round(random.uniform(1000,5000),2),
        "HKONT": random.choice(["200000", "210000", "220000"])
    })
pd.DataFrame(bkpf).to_csv(f"{base}/BKPF.csv", index=False)
pd.DataFrame(bseg).to_csv(f"{base}/BSEG.csv", index=False)

# ---------- Payments (REGUH / REGUP) ----------
reguh, regup = [], []
for inv in random.sample(invoices, 10):
    pay_id = f"P{random.randint(10000,99999)}"
    pay_date = faker.date_between(start_date="-30d", end_date="today")
    reguh.append({
        "ZBUKR": "1000",
        "LIFNR": inv["LIFNR"],
        "ZALDT": pay_date,
        "ZREGU": pay_id
    })
    regup.append({
        "BELNR": inv["BELNR"],
        "LIFNR": inv["LIFNR"],
        "ZREGU": pay_id,
        "ZBUKR": "1000",
        "ZALDT": pay_date
    })
pd.DataFrame(reguh).to_csv(f"{base}/REGUH.csv", index=False)
pd.DataFrame(regup).to_csv(f"{base}/REGUP.csv", index=False)

print("✅ Full SAP P2P dataset generated successfully in data/sap_tables/")

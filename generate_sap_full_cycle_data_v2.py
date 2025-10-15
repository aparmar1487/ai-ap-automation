from faker import Faker
import pandas as pd, random, os, datetime

faker = Faker()
base = "data/sap_tables"
os.makedirs(base, exist_ok=True)

# Helper: generate random currency and doc types
currencies = ["USD", "EUR", "GBP", "INR", "JPY"]
doc_types = ["RE", "KR", "PO", "SA"]
tax_codes = ["A0", "A1", "V0"]
company_codes = ["1000", "2000", "3000"]

# -------------------- Vendor Master --------------------
vendors = [
    {
        "LIFNR": f"V{1000+i}",
        "NAME1": faker.company(),
        "LAND1": faker.country_code(),
        "ORT01": faker.city(),
        "BUKRS": random.choice(company_codes),
        "WAERS": random.choice(currencies),
        "LOEVM": ""
    }
    for i in range(200)
]
df_lfa1 = pd.DataFrame(vendors)
df_lfa1.to_csv(f"{base}/LFA1.csv", index=False)

lfb1 = [
    {
        "LIFNR": v["LIFNR"],
        "BUKRS": v["BUKRS"],
        "ZUAWA": random.choice(["001", "002", "003"]),
        "AKONT": random.choice(["300000", "310000", "320000"]),
        "ZUAWA_TXT": faker.word()
    }
    for v in vendors
]
pd.DataFrame(lfb1).to_csv(f"{base}/LFB1.csv", index=False)

# -------------------- PO Header (EKKO) --------------------
num_pos = 1000
ekko = []
for i in range(num_pos):
    ekko.append({
        "EBELN": f"45{1000+i}",
        "LIFNR": random.choice(vendors)["LIFNR"],
        "BEDAT": faker.date_between(start_date="-180d", end_date="today"),
        "BUKRS": random.choice(company_codes),
        "EKORG": random.choice(["PUR1", "PUR2", "PUR3"]),
        "EKGRP": random.choice(["G01", "G02", "G03"]),
        "WAERS": random.choice(currencies),
        "BSART": random.choice(["NB", "FO"]),
        "AEDAT": faker.date_between(start_date="-180d", end_date="today")
    })
df_ekko = pd.DataFrame(ekko)
df_ekko.to_csv(f"{base}/EKKO.csv", index=False)

# -------------------- PO Items (EKPO) --------------------
materials = [f"M{faker.random_int(100,999)}" for _ in range(200)]
ekpo = []
for po in ekko:
    for _ in range(random.randint(1,4)):
        ekpo.append({
            "EBELN": po["EBELN"],
            "EBELP": faker.random_int(10,99),
            "MATNR": random.choice(materials),
            "WERKS": "US01",
            "LGORT": random.choice(["0001","0002"]),
            "MENGE": random.randint(1,20),
            "NETPR": round(random.uniform(50,1000),2),
            "PEINH": 1,
            "MWSKZ": random.choice(tax_codes),
            "EINDT": faker.date_between(start_date="-60d", end_date="+30d")
        })
df_ekpo = pd.DataFrame(ekpo)
df_ekpo.to_csv(f"{base}/EKPO.csv", index=False)

# -------------------- GR (MKPF / MSEG) --------------------
mkpf, mseg = [], []
for i in range(1000):
    mblnr = f"50{2000+i}"
    budat = faker.date_between(start_date="-120d", end_date="today")
    mkpf.append({
        "MBLNR": mblnr,
        "BUKRS": random.choice(company_codes),
        "BUDAT": budat,
        "BLDAT": budat,
        "USNAM": faker.first_name()
    })
    po_item = random.choice(ekpo)
    mseg.append({
        "MBLNR": mblnr,
        "EBELN": po_item["EBELN"],
        "EBELP": po_item["EBELP"],
        "MATNR": po_item["MATNR"],
        "MENGE": po_item["MENGE"],
        "DMBTR": round(po_item["MENGE"]*po_item["NETPR"],2),
        "SHKZG": random.choice(["S","H"])
    })
pd.DataFrame(mkpf).to_csv(f"{base}/MKPF.csv", index=False)
pd.DataFrame(mseg).to_csv(f"{base}/MSEG.csv", index=False)

# -------------------- PO History (EKBE) --------------------
ekbe = []
for item in mseg:
    ekbe.append({
        "EBELN": item["EBELN"],
        "EBELP": item["EBELP"],
        "VGABE": 1,
        "MATNR": item["MATNR"],
        "MENGE": item["MENGE"],
        "DMBTR": item["DMBTR"],
        "BUDAT": item["MBLNR"],
        "BEWTP": random.choice(["E","Q"])
    })
for i in range(500):
    po_item = random.choice(ekpo)
    ekbe.append({
        "EBELN": po_item["EBELN"],
        "EBELP": po_item["EBELP"],
        "VGABE": 2,
        "MATNR": po_item["MATNR"],
        "MENGE": po_item["MENGE"],
        "DMBTR": round(po_item["MENGE"]*po_item["NETPR"],2),
        "BUDAT": faker.date_between(start_date="-90d", end_date="today"),
        "BEWTP": "Q"
    })
pd.DataFrame(ekbe).to_csv(f"{base}/EKBE.csv", index=False)

# -------------------- Invoice (RBKP / RSEG) --------------------
rbkp, rseg = [], []
for i in range(1000):
    inv_no = f"51{2000+i}"
    lifnr = random.choice(vendors)["LIFNR"]
    rbkp.append({
        "BELNR": inv_no,
        "BUKRS": random.choice(company_codes),
        "LIFNR": lifnr,
        "BLART": random.choice(doc_types),
        "BUDAT": faker.date_between(start_date="-60d", end_date="today"),
        "WAERS": random.choice(currencies),
        "GJAHR": 2025
    })
    po_item = random.choice(ekpo)
    rseg.append({
        "BELNR": inv_no,
        "EBELN": po_item["EBELN"],
        "EBELP": po_item["EBELP"],
        "MATNR": po_item["MATNR"],
        "MENGE": po_item["MENGE"],
        "WRBTR": round(po_item["MENGE"]*po_item["NETPR"],2),
        "MWSKZ": random.choice(tax_codes)
    })
pd.DataFrame(rbkp).to_csv(f"{base}/RBKP.csv", index=False)
pd.DataFrame(rseg).to_csv(f"{base}/RSEG.csv", index=False)

# -------------------- Accounting (BKPF / BSEG) --------------------
bkpf, bseg = [], []
for inv in rbkp:
    bkpf.append({
        "BELNR": inv["BELNR"],
        "BUKRS": inv["BUKRS"],
        "BLART": inv["BLART"],
        "BLDAT": inv["BUDAT"],
        "BUDAT": inv["BUDAT"],
        "WAERS": inv["WAERS"],
        "USNAM": faker.first_name()
    })
    bseg.append({
        "BELNR": inv["BELNR"],
        "BUZEI": faker.random_int(1,99),
        "WRBTR": round(random.uniform(100,10000),2),
        "HKONT": random.choice(["200000","210000","220000"]),
        "SHKZG": random.choice(["S","H"]),
        "KOSTL": faker.random_int(1000,9999)
    })
pd.DataFrame(bkpf).to_csv(f"{base}/BKPF.csv", index=False)
pd.DataFrame(bseg).to_csv(f"{base}/BSEG.csv", index=False)

# -------------------- Payments (REGUH / REGUP) --------------------
reguh, regup = [], []
for i in range(1000):
    pay_id = f"P{random.randint(10000,99999)}"
    pay_date = faker.date_between(start_date="-45d", end_date="today")
    lifnr = random.choice(vendors)["LIFNR"]
    reguh.append({
        "ZBUKR": random.choice(company_codes),
        "LIFNR": lifnr,
        "ZALDT": pay_date,
        "HBKID": random.choice(["BANK1","BANK2"]),
        "RZAWE": random.choice(["T","C"]),
        "WAERS": random.choice(currencies),
        "ZREGU": pay_id
    })
    regup.append({
        "BELNR": random.choice(rbkp)["BELNR"],
        "LIFNR": lifnr,
        "ZREGU": pay_id,
        "ZBUKR": random.choice(company_codes),
        "ZALDT": pay_date
    })
pd.DataFrame(reguh).to_csv(f"{base}/REGUH.csv", index=False)
pd.DataFrame(regup).to_csv(f"{base}/REGUP.csv", index=False)

print("✅ Generated expanded SAP-like dataset (~1000 rows per table) in data/sap_tables/")

"""Generates every practice dataset used in the course.

All data is synthetic (made up). No real guests, clients, or employers.
Run it again any time to rebuild the files:  python data/generate_data.py
The random seed is fixed, so you always get the same files.
"""
import csv
import json
import random
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
random.seed(42)

FIRST = ["Ana", "Ben", "Carla", "Diego", "Elena", "Felix", "Grace", "Hiro", "Isla", "Jonas",
         "Kai", "Lena", "Marco", "Nina", "Oscar", "Paula", "Quinn", "Rafael", "Sofia", "Tomas",
         "Uma", "Victor", "Wren", "Ximena", "Yusuf", "Zara"]
LAST = ["Santos", "Reyes", "Cruz", "Tan", "Lim", "Garcia", "Muller", "Rossi", "Kim", "Sato",
        "Dubois", "Novak", "Silva", "Haddad", "Okafor", "Larsen", "Costa", "Mendoza"]
NATIONALITY = ["PH", "SG", "US", "GB", "DE", "JP", "AU", "FR", "IT", "KR"]
TIERS = ["Bronze", "Silver", "Gold", "Platinum"]

OUTLETS = {
    "Bar": (8, 60),
    "Restaurant": (25, 180),
    "Spa": (90, 420),
    "Boutique": (30, 900),
    "Excursions": (60, 350),
    "Cafe": (4, 25),
}
OUTLET_VARIANTS = {
    "Bar": ["Bar", "bar", " Bar", "BAR", "The Bar"],
    "Restaurant": ["Restaurant", "restaurant ", "Resto", "RESTAURANT"],
    "Spa": ["Spa", "spa", "Spa "],
    "Boutique": ["Boutique", "boutique"],
    "Excursions": ["Excursions", "excursions", "Shore Excursions"],
    "Cafe": ["Cafe", "cafe", "Café"],
}
VOYAGE_START = date(2026, 10, 1)
VOYAGE_DAYS = 14


def make_guests(n=60):
    guests = []
    for i in range(1, n + 1):
        first, last = random.choice(FIRST), random.choice(LAST)
        check_in = VOYAGE_START
        check_out = VOYAGE_START + timedelta(days=random.choice([7, 10, 14]))
        guests.append({
            "guest_id": f"G{i:03d}",
            "name": {"first": first, "last": last},
            "nationality": random.choice(NATIONALITY),
            "loyalty_tier": random.choice(TIERS),
            "stay": {"cabin": f"{random.choice('ABC')}{random.randint(101, 420)}",
                     "check_in": check_in.isoformat(), "check_out": check_out.isoformat()},
            "contact": {"email": f"{first.lower()}.{last.lower()}{i}@example.com",
                        "phone": f"+63917{random.randint(1000000, 9999999)}"},
        })
    return guests


def fmt_date_messy(d):
    style = random.random()
    if style < 0.70:
        return d.isoformat()                      # 2026-10-01
    if style < 0.88:
        return d.strftime("%d/%m/%Y")             # 01/10/2026 (day first, PH style)
    return d.strftime("%b %d %Y")                 # Oct 01 2026


def make_charges(guests):
    clean, messy = [], []
    charge_id = 1000
    for g in guests:
        stay_days = (date.fromisoformat(g["stay"]["check_out"]) - date.fromisoformat(g["stay"]["check_in"])).days
        for _ in range(random.randint(4, 14)):
            outlet = random.choice(list(OUTLETS))
            low, high = OUTLETS[outlet]
            d = VOYAGE_START + timedelta(days=random.randint(0, stay_days - 1))
            charge_id += 1
            row = {"charge_id": charge_id, "guest_id": g["guest_id"], "outlet": outlet,
                   "charge_date": d.isoformat(), "amount": round(random.uniform(low, high), 2),
                   "charge_type": "sale", "currency": "USD"}
            if random.random() < 0.05:
                row["amount"] = -round(random.uniform(low, high) / 2, 2)
                row["charge_type"] = "refund"
            clean.append(row)
    clean.sort(key=lambda r: (r["charge_date"], r["charge_id"]))

    for r in clean:
        m = dict(r)
        m["outlet"] = random.choice(OUTLET_VARIANTS[r["outlet"]])
        m["charge_date"] = fmt_date_messy(date.fromisoformat(r["charge_date"]))
        if random.random() < 0.03:
            m["amount"] = ""                       # missing amount
        messy.append(m)
    for r in random.sample(messy, 12):             # exact duplicates (double-posted)
        messy.append(dict(r))
    for k in range(4):                              # orphan charges, guest not in master list
        charge_id += 1
        messy.append({"charge_id": charge_id, "guest_id": "G999", "outlet": "Bar",
                      "charge_date": (VOYAGE_START + timedelta(days=k)).isoformat(),
                      "amount": 15.0, "charge_type": "sale", "currency": "USD"})
    random.shuffle(messy)
    return clean, messy


def write_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def make_logs(path, n=120):
    levels = ["INFO"] * 7 + ["WARNING"] * 2 + ["ERROR"]
    components = ["extract", "transform", "load", "scheduler"]
    messages = {
        "INFO": ["Batch {b} started", "Loaded {n} rows", "Batch {b} finished"],
        "WARNING": ["Row {r}: outlet name not recognised", "Slow query: {s}s"],
        "ERROR": ["Row {r}: missing amount", "Connection to database lost", "Row {r}: guest G999 not found"],
    }
    t = datetime(2026, 10, 1, 1, 0, 0)
    with open(path, "w", encoding="utf-8") as f:
        for i in range(n):
            t += timedelta(seconds=random.randint(5, 600))
            lvl = random.choice(levels)
            msg = random.choice(messages[lvl]).format(b=i // 10 + 1, n=random.randint(50, 900),
                                                       r=random.randint(2, 640), s=random.randint(3, 40))
            f.write(f"{t:%Y-%m-%d %H:%M:%S} {lvl} [{random.choice(components)}] {msg}\n")


def make_inventory_excel(path):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    schools = ["Paliparan ES", "Salitran NHS", "Burol IS"]
    items = [("Desktop Computer", "Acer"), ("Laptop", "Lenovo"), ("Projector", "Epson"),
             ("Router", "TP-Link"), ("Printer", "Brother"), ("Smart TV", "Samsung")]
    statuses = ["Working", "working", "Working ", "Defective", "defective", "For Repair", "for repair"]
    wb = Workbook()
    wb.remove(wb.active)
    for school in schools:
        ws = wb.create_sheet(school)
        ws["A1"] = f"Schools Division ICT Inventory - {school}"
        ws["A1"].font = Font(bold=True, size=13)
        ws["A2"] = "As of October 2026"
        ws.append([])
        ws.append(["Item", "Brand", "Qty", "Status", "Date Acquired"])
        for item, brand in random.sample(items, k=5):
            qty = random.randint(1, 40)
            qty_value = qty if random.random() < 0.7 else f"{qty} pcs"
            acquired = date(random.randint(2017, 2025), random.randint(1, 12), random.randint(1, 28))
            ws.append([item, brand, qty_value, random.choice(statuses), acquired.strftime("%m/%d/%Y")])
        ws.append([])
        ws.append(["Prepared by: ICT Coordinator"])
    wb.save(path)


INVOICE_ITEMS = [("Chicken Breast (kg)", 210.00), ("Pork Belly (kg)", 320.00), ("Ground Beef (kg)", 380.00),
                 ("Tilapia (kg)", 160.00), ("Cabbage (kg)", 55.00), ("Carrots (kg)", 70.00),
                 ("Eggplant (kg)", 80.00), ("Calamansi (kg)", 90.00), ("Rice 25kg Sack", 1350.00),
                 ("Eggs (tray of 30)", 245.00)]


def make_invoices(folder):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    folder.mkdir(exist_ok=True)
    meta = []
    for n in range(1, 6):
        inv_no = f"INV-{1000 + n}"
        inv_date = date(2026, 10, 2 + n * 2)
        lines = []
        for name, price in random.sample(INVOICE_ITEMS, k=random.randint(3, 6)):
            qty = random.randint(2, 30)
            lines.append((name, qty, price, round(qty * price, 2)))
        total = round(sum(l[3] for l in lines), 2)
        printed_total = total + 500.00 if n == 4 else total   # INV-1004 has a wrong total on purpose
        c = canvas.Canvas(str(folder / f"{inv_no}.pdf"), pagesize=A4)
        y = 800
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "BUKID FRESH TRADING")
        c.setFont("Helvetica", 11)
        for text in [f"Invoice No: {inv_no}", f"Date: {inv_date.isoformat()}",
                     "Bill To: Galley Stores Department", ""]:
            y -= 18
            c.drawString(50, y, text)
        y -= 18
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Item"); c.drawString(300, y, "Qty"); c.drawString(360, y, "Unit Price"); c.drawString(460, y, "Line Total")
        c.setFont("Helvetica", 11)
        for name, qty, price, lt in lines:
            y -= 18
            c.drawString(50, y, name); c.drawString(300, y, str(qty))
            c.drawString(360, y, f"{price:,.2f}"); c.drawString(460, y, f"{lt:,.2f}")
        y -= 28
        c.setFont("Helvetica-Bold", 12)
        c.drawString(360, y, "TOTAL"); c.drawString(460, y, f"{printed_total:,.2f}")
        c.save()
        meta.append({"invoice_no": inv_no, "lines": len(lines), "true_total": total, "printed_total": printed_total})
    with open(folder / "_answer_key.json", "w") as f:
        json.dump(meta, f, indent=2)


def make_api_pages(folder, guests):
    folder.mkdir(exist_ok=True)
    reviews = []
    for i, g in enumerate(random.sample(guests, 25), start=1):
        reviews.append({"review_id": i, "guest": {"id": g["guest_id"], "tier": g["loyalty_tier"]},
                        "outlet": random.choice(list(OUTLETS)), "rating": random.randint(1, 5),
                        "submitted_at": f"2026-10-{random.randint(2, 14):02d}T{random.randint(8, 22):02d}:00:00Z"})
    pages = [reviews[0:10], reviews[10:20], reviews[20:25]]
    for n, chunk in enumerate(pages, start=1):
        nxt = f"https://api.example.com/reviews?page={n + 1}" if n < len(pages) else None
        with open(folder / f"page_{n}.json", "w") as f:
            json.dump({"page": n, "results": chunk, "next": nxt}, f, indent=2)


def main():
    guests = make_guests()
    with open(HERE / "guests.json", "w", encoding="utf-8") as f:
        json.dump(guests, f, indent=2)
    flat = [{"guest_id": g["guest_id"], "first_name": g["name"]["first"], "last_name": g["name"]["last"],
             "nationality": g["nationality"], "loyalty_tier": g["loyalty_tier"], "cabin": g["stay"]["cabin"],
             "check_in": g["stay"]["check_in"], "check_out": g["stay"]["check_out"]} for g in guests]
    write_csv(HERE / "guests.csv", flat, list(flat[0]))

    clean, messy = make_charges(guests)
    fields = ["charge_id", "guest_id", "outlet", "charge_date", "amount", "charge_type", "currency"]
    write_csv(HERE / "charges_clean.csv", clean, fields)
    write_csv(HERE / "onboard_charges_raw.csv", messy, fields)

    write_csv(HERE / "outlets.csv", [
        {"outlet": "Bar", "category": "Beverage", "deck": 5}, {"outlet": "Restaurant", "category": "Food", "deck": 4},
        {"outlet": "Spa", "category": "Wellness", "deck": 6}, {"outlet": "Boutique", "category": "Retail", "deck": 3},
        {"outlet": "Excursions", "category": "Activities", "deck": 2}, {"outlet": "Cafe", "category": "Food", "deck": 5},
    ], ["outlet", "category", "deck"])

    make_logs(HERE / "pipeline.log")
    make_inventory_excel(HERE / "ict_inventory_messy.xlsx")
    make_invoices(HERE / "invoices")
    make_api_pages(HERE / "api_pages", guests)
    print("Datasets written to", HERE)
    print(f"  guests: {len(guests)} | clean charges: {len(clean)} | raw charges: {len(messy)}")


if __name__ == "__main__":
    main()

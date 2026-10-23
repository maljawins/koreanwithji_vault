import os, re, shutil, tempfile, zipfile
from xml.etree import ElementTree as ET

xlsx = r"C:\vault\koreanwithji_vault\02_product\02_course_creation\00_curriculum_and_index\01_Ji_Draft_review_report.xlsx"
NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
RNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
ET.register_namespace("x", NS)
ET.register_namespace("r", RNS)
ns = {"x": NS}

with zipfile.ZipFile(xlsx, "r") as zin:
    entries = {name: zin.read(name) for name in zin.namelist()}

sheet_name = None
for name, data in entries.items():
    if name.startswith("xl/worksheets/sheet") and name.endswith(".xml") and b"Ji_Draft Intro" in data:
        sheet_name = name
        break
if sheet_name is None:
    raise RuntimeError("intro sheet XML not found")

root = ET.fromstring(entries[sheet_name])
rels_name = sheet_name.replace("xl/worksheets/", "xl/worksheets/_rels/") + ".rels"
if rels_name in entries:
    rel_root = ET.fromstring(entries[rels_name])
else:
    rel_root = ET.Element("{http://schemas.openxmlformats.org/package/2006/relationships}Relationships")
rel_ns = {"pr": "http://schemas.openxmlformats.org/package/2006/relationships"}
ET.register_namespace("", "http://schemas.openxmlformats.org/package/2006/relationships")

existing_ids = {rel.attrib.get("Id") for rel in rel_root}
next_id = 1
def next_rel_id():
    global next_id
    while f"rId{next_id}" in existing_ids:
        next_id += 1
    rid = f"rId{next_id}"
    existing_ids.add(rid)
    next_id += 1
    return rid

hyperlinks = root.find("x:hyperlinks", ns)
if hyperlinks is None:
    sheet_data = root.find("x:sheetData", ns)
    hyperlinks = ET.Element(f"{{{NS}}}hyperlinks")
    insert_at = list(root).index(sheet_data) + 1
    root.insert(insert_at, hyperlinks)
else:
    for h in list(hyperlinks):
        hyperlinks.remove(h)

count = 0
for cell in root.findall(".//x:c", ns):
    ref = cell.attrib.get("r", "")
    if not ref.startswith("B"):
        continue
    formula = cell.find("x:f", ns)
    if formula is None or not formula.text or not formula.text.startswith("HYPERLINK("):
        continue
    m = re.match(r'HYPERLINK\("(.*?)","(.*?)"\)$', formula.text)
    if not m:
        continue
    target, title = m.group(1), m.group(2)
    # Convert the formula cell to a normal displayed string.
    for child in list(cell):
        cell.remove(child)
    cell.attrib["t"] = "str"
    v = ET.SubElement(cell, f"{{{NS}}}v")
    v.text = title
    rid = next_rel_id()
    link = ET.SubElement(hyperlinks, f"{{{NS}}}hyperlink")
    link.attrib["ref"] = ref
    link.attrib[f"{{{RNS}}}id"] = rid
    rel = ET.SubElement(rel_root, "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship")
    rel.attrib.update({"Id": rid, "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", "Target": target, "TargetMode": "External"})
    count += 1

if count == 0:
    raise RuntimeError("no HYPERLINK formulas found to patch")
entries[sheet_name] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
entries[rels_name] = ET.tostring(rel_root, encoding="utf-8", xml_declaration=True)

tmp = xlsx + ".tmp"
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for name, data in entries.items():
        zout.writestr(name, data)
os.replace(tmp, xlsx)
print(f"patched {count} native hyperlinks in {sheet_name}")

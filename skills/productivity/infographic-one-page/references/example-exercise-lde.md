# Worked example (sanitized) — one-page infographic prompt "Exercise หาย? จำ L · D · E"

Real prompt used for a TopSky ATC TMC training manual. Hostnames and paths are replaced with <placeholders> here; put the real ones in only when the user is taking the prompt to an external tool themselves. No passwords were ever included.

---เริ่ม---

Create a premium vertical (4:5) educational infographic in Thai for air traffic control system technicians.
Topic: "Exercise หาย? จำ L · D · E" (where TMC training exercises are stored, and why they disappear after a Distribute).

STYLE
- Modern sketchnote, white background (#FFFFFF) with a light gray dot grid (#F3F4F6)
- Fonts: Prompt / Kanit (Thai), bold black title, purple subtitle
- Palette: Purple #8B5CF6, Yellow #FACC15, Blue #60A5FA, Green #4ADE80, Pink #F9A8D4
- Hand-drawn arrows, sticky notes, checkmarks, small icons. Clean and printable. Not cartoon-heavy.
- Meaning of colors: red/pink = L (data lost) · yellow = D · green = E / restore · blue = normal path

STRICT TEXT RULES
- Render every Thai and English text EXACTLY as written below, character by character.
- Do NOT invent, translate, shorten or add any file path, command, or number.
- Keep text blocks short. Commands go in monospace boxes.
- No passwords anywhere.

LAYOUT: 8 sections stacked top to bottom

1) HOOK (largest, high contrast)
   Title: "Exercise หาย?"
   Purple subtitle: "จำ L · D · E"
   Tagline: "ก่อน Distribute: L → D"

2) BIG IDEA (one sticky note)
   "Exercise เก็บอยู่ 3 ที่ และ DPR Distribute เอา D ไปทับ L เสมอ"
   "ก่อน Distribute: copy L → D · หายแล้ว: กู้ E → L"

3) VISUAL FLOW (vertical arrow flow, 4 steps)
   "① สร้าง/แก้ใน EED → เขียนลง E และ L"
   "② copy L → D (ทำเอง)"
   "③ DPR Distribute → D ทับ L"
   "④ IHMI Leader อ่านจาก L → ATC เรียกใช้"
   Red note: "ข้าม ② = exercise ใหม่หาย"
   Green arrow: "กู้: E → L แล้ว stop node / start node cold ที่ tmc"

4) COMPONENT CARDS (4 cards, max 3 bullets each)
   Red card "L = LDR (ที่ ATC เห็น)": "IHMI Leader อ่านจากที่นี่" / "ถูกทับทุกครั้งที่ DPR Distribute" / "คำสั่งเข้า: ldr_db"
   Yellow card "D = Distribute source (ต้นทาง)": "DPR Distribute ใช้ส่งไปทับ L" / "ต้อง copy จาก L มาก่อนเสมอ" / "คำสั่งเข้า: offl"
   Green card "E = EED tmp (ที่กู้)": "EED เก็บสำเนาตอน Commit" / "หายแล้วกู้จากที่นี่" / "Commit ทุกครั้งที่แก้"
   Blue card "แยก 2 เครื่อง 2 dataset": "dso01 = ATC (SIM): Generate เท่านั้น" / "tmc01 = Pilot/Exercise (S01): Generate + Distribute + Link" / "อย่าสลับกัน"

5) ARCHITECTURE (two stacked boxes with arrows)
   Box 1: "<ATC-node> → ATC Dataset (SIM)" + "เกี่ยวกับ MAP" + "Generate เท่านั้น (ไม่ Distribute)"
   Box 2: "<TMC-node> → Pilot/Exercise Dataset (S01)" + "สร้าง exercise → E + L" + "L ⇢ D (copy เอง) → DPR Distribute → D ทับ L" + "EED: Link → Commit → EED Distribute" + "stop node / start node cold"

6) COMPARISON (table, 4 rows x 4 columns)
   Columns: สถานการณ์ | เริ่มจาก | copy ทิศไหน | จบด้วย
   A. Dataset ใหม่ | Generate → DPR Distribute | L → D ก่อน Distribute | Link → Commit → EED Distribute → node cold
   B. แก้ Exercise | EED Commit | L → D (เฉพาะ EXE ที่ต่าง) | DPR Distribute
   C. Exercise หาย | ดู L ไม่เจอ → ดู E | E → L (แล้ว L → D) | stop / start node cold
   D. อัปเกรด version | ใช้ path version ใหม่ | L (เก่า) → D (ใหม่) | เปลี่ยน version ใน EED → Distribute
   Small orange box "Generate ไม่ผ่าน": "ชื่อ dataset ไม่ตรง site → mv ชื่อผิดเป็นชื่อ site" / "FILE TYPE ไม่เหลือง → touch DATASET_CONFIGURATION" / "error ที่ SYSTEM_MAPS → เปลี่ยน svg_convertor_bin จาก release เก่า"

7) DECISION FRAMEWORK (two columns)
   Green column "แค่ copy L → D ถ้า…": "✅ exercise ยังอยู่ใน L ครบ" / "✅ ยังไม่ได้กด DPR Distribute" / "✅ เพิ่งแก้ใน EED และ Commit แล้ว"
   Red column "กู้ E → L ถ้า…": "✅ Distribute ไปแล้ว exercise หายจาก L" / "✅ ATC เรียกใน IHMI Leader ไม่เจอ" / "✅ เคย Commit ไว้ (ใน E ต้องมี EXE นั้น)"

8) SUMMARY (checklist + command strip)
   "✅ Exercise มี 3 ที่: L (ATC เห็น) · D (ต้นทาง) · E (ที่กู้)"
   "✅ ก่อน DPR Distribute: copy L → D ทุกครั้ง"
   "✅ หายแล้ว: กู้ E → L แล้ว stop / start node cold"
   "✅ Commit ใน EED ทุกครั้ง"
   "✅ ยืนยัน path ด้วย pwd ก่อนทำจริง"
   Monospace box "กฎเหล็กก่อน DPR Distribute" (render verbatim, 2 lines):
   cd <PATH-L: LDR exercise folder>
   cp -rp * <PATH-D: Distribute source folder>
   Footer disclaimer (small): "เอกสารภายในสำหรับช่าง ตรวจ path และคำสั่งกับเครื่องจริงก่อนใช้"

Audience: Thai ATC system technicians reading at the workstation. Short sentences and bullets only.

---จบ---

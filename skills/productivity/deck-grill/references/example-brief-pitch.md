# Deck Brief: Digital Tower Roadmap — แบ่งเฟสเพื่อวางแผนงบประมาณ
Version: v1 · Status: APPROVED (demo) · Format: sketch-deck HTML → SketchDeck editor

## 1. Brief summary
| Field | Answer |
|---|---|
| Objective (observable outcome) | ผู้บริหารรับทราบโครงสร้างเฟสใหม่ (หลัก A1–A8 + เสริม B0–B4) เพื่อใช้วางแผนงบ — ยังไม่ขออนุมัติงบ |
| Primary audience (persona) | ผู้บริหาร AEROTHAI ที่รู้จัก TOR เดิมดี ไม่ชอบรายละเอียดเทคนิค |
| What they care about most | งบประมาณ · ความเสี่ยงที่ตัดงบแล้วระบบใช้ไม่ได้ |
| Main objection to address | "เลือกเฟสแล้วจะได้ของครึ่งๆ กลางๆ หรือเปล่า" |
| Core message (one sentence) | แบ่งเป็นเฟสหลัก + เฟสเสริม ตัดงบจุดไหนก็ยังใช้งานได้จริง |
| Supporting points | ① TOR เดิมมี 2 เฟสก้อนเดียว ② เฟสหลักเรียงลำดับ ผ่านประตู CAAT ③ A6 Go-Live = จุดคุ้มทุนขั้นต่ำ ④ AI เสริมเลือกเพิ่มอิสระ |
| Call to action | รับทราบโครงสร้างเฟส (ยังไม่เลือกงบวันนี้) |
| Context | พูดสด · ประชุม ~10 นาที · ห้องประชุม |
| Language and tone | ไทย + ศัพท์อังกฤษ · เป็นกันเอง กระชับ |
| Must include / must avoid | ต้องมี: CAAT gate, A6 Go-Live, ภาพกล้อง SBA/DMA Best+Base · ห้าม: ตัวเลขราคา, ชื่อยี่ห้อ (AH-IPS) |
| Constraints | 7 สไลด์ · canvas 1600×900 · แก้ต่อใน editor |
| Style | **pitch-minimal** (badge + หัวข้อ + ป้ายสั้น ≤12 คำ/step · ไม่มีประโยคสรุปล่างสไลด์ · รายละเอียดใน notes) |
| Success looks like | ผู้บริหารพูดว่า "โอเค เดินตามโครงสร้างนี้" และไม่ถามว่า "ขอเงินเท่าไหร่วันนี้" |

## 2. Storyline
Pattern: **Before → After → Bridge** (โลกเดิม → โครงสร้างใหม่ → ทางที่ไป → ขอ "รับทราบ") เพราะเป้าคือให้ยอมรับกรอบใหม่ ไม่ใช่ตัดสินใจเงิน
1. Digital Tower Roadmap — แบ่งเฟสเพื่อวางแผนงบประมาณ *(title)*
2. TOR เดิมมีแค่ 2 เฟส
3. เฟสหลัก ก่อนถึง CAAT Approve
4. Go-Live ที่ A6 คือจุดคุ้มทุนขั้นต่ำ
5. เฟสเสริม AI ห้าโมดูล (Additional)
6. การวางกล้อง Best Case & Base Case
7. สิ่งที่ต้องการวันนี้

Time budget: 7 สไลด์ × ~1.3 นาที ≈ 9–10 นาที (slot: 10 นาที) ✔

## 2b. Format preview  ← **จุดที่คุณต้องอนุมัติ (หน้าตาสุดท้ายล็อกที่นี่)**
```
#  Title                              Pattern             Theme   Steps  Images
0  Digital Tower Roadmap              title               –       1      –
1  TOR เดิมมีแค่ 2 เฟส                old-vs-new          red     4      –
2  เฟสหลัก ก่อนถึง CAAT Approve       milestone timeline  blue    5      –
3  Go-Live ที่ A6 = จุดคุ้มทุน         milestone hub       green   4      –
4  เฟสเสริม AI ห้าโมดูล               hub-and-spoke       orange  3      –
5  การวางกล้อง Best & Base            image slot          teal    5      4 (1240×640)
6  สิ่งที่ต้องการวันนี้                two-box ask         green   3      –
```
กฎคงที่: canvas 1600×900 · ใช้เฉพาะรูปทรงที่ editor มี (text/box/srect/line/arrow/badge/check/stamp/image) · รูป = กรอบประเส้นประ 1240×640 ที่ยังว่าง · รายละเอียดทั้งหมดอยู่ใน notes · `board:false`

ภาพร่างต่อ pattern:
```
old-vs-new                         milestone timeline
┌─TOR เดิม──┐   ┌─แบบใหม่───┐        ─●A1────●A2────●A3────●A4(แดง)─
│ [Phase 1] │ → │ [เฟสหลัก]✓│         ชื่อ    ชื่อ    ชื่อ    ชื่อ
│ [Phase 2] │   │ [เฟสเสริม]✓│              (callout)          [CAAT GATE]
│ ไม่มีจุดตัดสินใจ │  ตัดงบก็ใช้ได้ │
└───────────┘   └───────────┘

milestone hub                      hub-and-spoke
 [A5] → [ A6 Go-Live ]{MVP} → [A7]   [ B0 Detection & Tracking ]
                            → [A8]     ↓     ↓     ↓     ↓
                                     [B1]  [B2]  [B3]  [B4]  (emoji cards)

image slot (ต่อ step 1 รูป)         two-box ask
 คำบรรยายภาพ (y=172)                 ┌เฟสหลัก────┐ ┌เฟสเสริม───┐
 ┌┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┐         │ ข้อความ    │ │ ข้อความ     │
 ┊   🖼 1240 × 640      ┊         └───────────┘ └───────────┘
 └┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┘
```

## 3. Slide-by-slide layout information

### Slide 0: Digital Tower Roadmap — แบ่งเฟสเพื่อวางแผนงบประมาณ
- **Role in story:** hook
- **Objective link:** ตั้งกรอบ "วางแผนงบ" ไม่ใช่ "ขอเงิน"
- **Takeaway:** วันนี้เรามาคุยเรื่องโครงสร้างเฟส
- **Visual concept:** title — ชื่อใหญ่ + เส้นใต้ + สนามบิน
- **Pattern / Theme:** title / blue
- **Layout:** `[กลาง]` ชื่อ 84px · รอง 54px (น้ำเงิน) · เส้นใต้ · `SBA · DMA` · `AEROTHAI`
- **Build steps:** 1. ทั้งหมดขึ้นพร้อมกัน — ทักทาย บอกวัตถุประสงค์ 1 ประโยค
- **Image slots:** none
- **On-slide text (exact):** Digital Tower Roadmap / แบ่งเฟสเพื่อวางแผนงบประมาณ / สุวรรณภูมิ (SBA) · ดอนเมือง (DMA) / AEROTHAI
- **Speaker notes:** ทักทาย + บอกวัตถุประสงค์ 1 ประโยค: วันนี้ขอให้รับทราบโครงสร้าง ยังไม่ขออนุมัติงบ
- **Evidence / source:** –
- **Audience lens:** ลดความกังวลเรื่องเงินตั้งแต่ต้น

### Slide 1: TOR เดิมมีแค่ 2 เฟส
- **Role in story:** problem
- **Objective link:** ①
- **Takeaway:** เดิมตัดสินใจได้ก้อนเดียว ไม่มีจุดถอย
- **Visual concept:** old vs new panels — ซ้ายเดิม (แดง) ขวาใหม่ (เขียว)
- **Pattern / Theme:** old-vs-new / red
- **Layout:** `[ซ้าย]` panel "TOR เดิม" 2 กล่อง · `[ขวา]` panel "แบบใหม่" กล่องน้ำเงิน+ส้ม · `[กลาง]` ลูกศร · ✓ ท้ายกล่องใหม่
- **Build steps:**
  1. panel เดิม: Phase 1 Validation, Phase 2 Main Ops+Contingency, "ไม่มีจุดตัดสินใจระหว่างทาง"
  2. panel ใหม่: เฟสหลัก A1–A8, เฟสเสริม B0–B4, "ตัดงบจุดไหนก็ยังใช้งานได้จริง"
  3. ลูกศรเดิม→ใหม่ + ✓ ✓
  4. (พัก — ให้ผู้ฟังถามได้)
- **Image slots:** none
- **On-slide text (exact):** TOR เดิม · Phase 1: Validation / Tuning · Phase 2: Main Ops + Contingency (รวมก้อนเดียว) · ไม่มีจุดตัดสินใจระหว่างทาง · แบบใหม่ · เฟสหลัก A1–A8 (8 ขั้น) · เฟสเสริม B0–B4 (AI เลือกได้) · ตัดงบจุดไหนก็ยังใช้งานได้จริง
- **Speaker notes:** เดิมตัดสินใจได้ก้อนเดียว ถ้างบไม่พอต้องรื้อทั้งแผน; แบบใหม่แตกเป็นขั้น เลือกงบได้
- **Evidence / source:** TOR V6.02 §8
- **Audience lens:** ตอบ "เลือกแล้วจะได้ของครึ่งๆ กลางๆ ไหม"

### Slide 2: เฟสหลัก ก่อนถึง CAAT Approve
- **Role in story:** how
- **Objective link:** ②
- **Takeaway:** เฟสหลักต้องเรียงลำดับ และ A4 คือประตูกำกับดูแลที่เราคุมเวลาเองไม่ได้
- **Visual concept:** milestone timeline — badge A1–A4 บนเส้น, A4 สีแดง, callout Video Wall, stamp CAAT GATE
- **Pattern / Theme:** milestone timeline / blue
- **Layout:** `[กลาง]` เส้น y=460 + 4 badge · ชื่อไทย/อังกฤษใต้ badge · callout เหนือ A2 · stamp เหนือ A4
- **Build steps:**
  1. A1 ติดตั้งกล้อง + เดินสาย (Camera & Network)
  2. A2 เชื่อม DT Lab + callout "จอเดียวเห็นได้แค่บางมุม ต้องมี Video Wall"
  3. A3 เก็บข้อมูล + HF (Data & HF Validation)
  4. A4 Safety Case + CAAT (Regulatory Approval) + stamp CAAT GATE
  5. (พัก)
- **Image slots:** none
- **On-slide text (exact):** A1 ติดตั้งกล้อง + เดินสาย · A2 เชื่อม DT Lab · A3 เก็บข้อมูล + HF · A4 Safety Case + CAAT · จอเดียวเห็นได้แค่บางมุม ต้องมี Video Wall · CAAT GATE
- **Speaker notes:** ต้องทำเรียงลำดับ; A4 คือประตูกำกับดูแล คุมไทม์ไลน์ เร่งเองไม่ได้
- **Evidence / source:** TOR V6.02 §8.x, CAAT requirements
- **Audience lens:** ทำไมไทม์ไลน์ยาว → เพราะประตู CAAT

### Slide 3: Go-Live ที่ A6 คือจุดคุ้มทุนขั้นต่ำ
- **Role in story:** solution
- **Objective link:** ③ + core message
- **Takeaway:** ถึง A6 แล้ว ATC ใช้งานจริงได้ — A7/A8 ต่อทีหลังไม่กระทบ
- **Visual concept:** milestone hub — A5 → กล่องเขียวใหญ่ A6 + stamp MVP → แตกไป A7, A8
- **Pattern / Theme:** milestone hub / green
- **Layout:** `[ซ้าย]` A5 · `[กลาง]` A6 กล่องใหญ่ + stamp · `[ขวา]` A7, A8 · ลูกศรแตก
- **Build steps:** 1. A5 CWP จริง · 2. A6 Go-Live + stamp MVP · 3. A7 Contingency Tower + A8 กล้อง Runway 3 · 4. (พัก)
- **Image slots:** none
- **On-slide text (exact):** A5 CWP จริง · A6 · Go-Live ใช้งานจริงกับ ATC บน Tower · MVP · A7 Contingency Tower · A8 กล้อง Runway 3
- **Speaker notes:** A6 คือจุดที่ ATC ใช้งานจริง; A7–A8 ต่อทีหลัง ไม่กระทบ Go-Live
- **Evidence / source:** TOR V6.02 §8 (ลำดับ A5–A8)
- **Audience lens:** ตอบ objection หลักตรงๆ

### Slide 4: เฟสเสริม AI ห้าโมดูล (Additional)
- **Role in story:** solution (optional)
- **Objective link:** ④
- **Takeaway:** B0 เป็นฐาน ที่เหลือเลือกเพิ่มอิสระตามงบ
- **Visual concept:** hub-and-spoke — กล่องส้ม B0 กลางบน → 4 การ์ดอีโมจิ B1–B4
- **Pattern / Theme:** hub-and-spoke / orange
- **Layout:** `[บน]` B0 · `[ล่าง]` 4 การ์ดเรียงแถว (🛡️ ⏱️ ✈️ ✨) · ลูกศรแตก 4 ทาง
- **Build steps:** 1. B0 Detection & Tracking · 2. ลูกศร + B1 Runway Incursion, B2 Runway Occupancy Time, B3 Approach Monitoring, B4 Automatic Sequencing · 3. (พัก)
- **Image slots:** none
- **On-slide text (exact):** B0 · Detection & Tracking · B1 Runway Incursion · B2 Runway Occupancy Time · B3 Approach Monitoring · B4 Automatic Sequencing
- **Speaker notes:** B0 เป็นฐาน; B1–B4 เลือกเพิ่มอิสระตามงบ
- **Evidence / source:** System Requirements DTS Rev3
- **Audience lens:** "ไม่ต้องซื้อ AI ทั้งชุด"

### Slide 5: การวางกล้อง Best Case & Base Case
- **Role in story:** proof
- **Objective link:** ยืนยันว่าแผนอิงการสำรวจจริง
- **Takeaway:** Best = แม่นกว่าแต่แพงกว่า · Base = ที่ติดตั้งได้จริงตอนนี้
- **Visual concept:** image slot ×4 — คำบรรยายสีต่างกัน 1 รูป/step
- **Pattern / Theme:** image slot / teal
- **Layout:** `[บน y=172]` คำบรรยาย · `[กลาง 180,205]` กรอบภาพ 1240×640
- **Build steps:** 1. (ว่าง) · 2. SBA Best · 3. SBA Base · 4. DMA Best · 5. DMA Base (แต่ละรูปโชว์ step ของตัวเอง)
- **Image slots:** step 2: SBA Best Case · step 3: SBA Base Case · step 4: DMA Best Case · step 5: DMA Base Case — ทุกช่อง 1240×640 · source: screenshot จาก `output/SBA_BestCase_Camera_Coverage.pptx` / `DMA_BestCase_…pptx` (+ Base จากผลสำรวจ 2026-09-12)
- **On-slide text (exact):** 1. สุวรรณภูมิ (SBA) — Best Case · 2. สุวรรณภูมิ (SBA) — Base Case · 3. ดอนเมือง (DMA) — Best Case · 4. ดอนเมือง (DMA) — Base Case
- **Speaker notes:** Best = 1 กล้อง/ทางออก แม่นกว่าแต่แพงกว่า; Base = ที่ติดตั้งจริงตอนนี้
- **Evidence / source:** site survey 2026-09-12 (Base Case ยืนยันแล้ว); Best Case รอข้อมูล
- **Audience lens:** "กล้องพอไหม/วางตรงไหน"

### Slide 6: สิ่งที่ต้องการวันนี้
- **Role in story:** ask
- **Objective link:** the objective itself
- **Takeaway:** ขอให้รับทราบโครงสร้าง — ยังไม่ขออนุมัติงบ
- **Visual concept:** two-box ask — กล่องมีหัว น้ำเงิน (หลัก) / ส้ม (เสริม)
- **Pattern / Theme:** two-box ask / green
- **Layout:** `[ซ้าย]` เฟสหลัก · `[ขวา]` เฟสเสริม
- **Build steps:** 1. เฟสหลัก: จำเป็นถึง A4 CAAT Approve (Lab Only) หรือ A6 Tower Installation · 2. เฟสเสริม: เลือกเพิ่มได้อิสระ Ex. AI Features ตาม Requirement · 3. (พัก / เปิดถามตอบ)
- **Image slots:** none
- **On-slide text (exact):** เฟสหลัก · จำเป็นถึง A4 CAAT Approve (Lab Only) หรือ A6 Tower Installation · เฟสเสริม · เลือกเพิ่มได้อิสระ Ex. AI Features ตาม Requirement
- **Speaker notes:** ขอให้รับทราบโครงสร้าง — ยังไม่ขออนุมัติงบ
- **Evidence / source:** –
- **Audience lens:** ปิดความกังวลเรื่อง "ขอเงิน"

## 4. Objective traceability
| Slide | Supports | If cut, what's lost? |
|---|---|---|
| 1 | ① เดิม vs ใหม่ | ไม่เห็นว่าทำไมต้องเปลี่ยน |
| 2 | ② ประตู CAAT | ตอบไม่ได้ว่าทำไมนาน |
| 3 | ③ / core message | **หาย core message** (ห้ามตัด) |
| 4 | ④ | ไม่รู้ว่า AI ซื้อแยกได้ |
| 5 | หลักฐานสำรวจ | ขาดความเชื่อถือ (ตัดได้ถ้าเวลาไม่พอ) |
| 6 | Objective | ไม่มี ask (ห้ามตัด) |

## 4b. Image list
| Slide/step | Shows | Size | Source / ChatGPT prompt | Status |
|---|---|---|---|---|
| 5 / step 2 | SBA Best Case coverage | 1240×640 | screenshot จาก SBA_BestCase_Camera_Coverage.pptx (หรือ ChatGPT: "top-down airport map, Suvarnabhumi, camera coverage cones green, clean flat style, 31:16") | TODO |
| 5 / step 3 | SBA Base Case | 1240×640 | ผลสำรวจ 2026-09-12 | TODO |
| 5 / step 4 | DMA Best Case | 1240×640 | DMA_BestCase_Camera_Coverage.pptx | TODO (รอ Best Case จากผู้ใช้) |
| 5 / step 5 | DMA Base Case | 1240×640 | ผลสำรวจ 2026-09-12 | TODO |

## 5. Open questions and risks
- BOQ ราคายังว่าง → ตั้งใจไม่ใส่ตัวเลขในสไลด์นี้ (ตรงกับ "must avoid")
- Best Case ของ DMA ยังไม่ได้รับ → รูป 4 อาจเป็นตัวแทนก่อน
- AH-IPS trademark ยังค้างใน TOR (ไม่เกี่ยวกับ deck นี้ แต่อย่าใส่ชื่อยี่ห้อบนสไลด์)

## 6. Change log
- v1: first draft → approved ที่ Format preview (demo)

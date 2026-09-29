# Prompt recipe — from idea to a final pitch deck (deck-grill → sketch-deck → editor)

Reverse-engineered from the AEROTHAI Digital Tower roadmap pitch (7 slides, executives, "acknowledge the framework").
What the final deck looked like: title slide + 6 content slides, each = round badge + short title + 3-5 build steps,
only short labels on slide, **no bottom takeaway**, one slide of 4 pictures (1240×640), a closing "ask" slide; all detail in notes.
Almost every hand edit afterwards was cosmetic (rotate stamp, add 2 arrows, move a label, fill images).

## Step 1 — /deck-grill (paste, fill the <…>)
```
/deck-grill  ทำ deck pitch <เรื่อง> ให้ <ผู้ฟัง เช่น ผู้บริหาร>
วัตถุประสงค์: <ให้เขา ตัดสินใจ/รับทราบ อะไร>
สไตล์: pitch-minimal (หัวข้อ + ป้ายสั้นๆ ไม่มีประโยคสรุปล่างสไลด์ รายละเอียดไว้ใน notes) ประมาณ <7> สไลด์
รูปภาพ: สไลด์ <..> ต้องการรูป <อะไร> <กี่รูป> (ผมหา/สร้างเอง)
แหล่งข้อมูล: <ไฟล์/โฟลเดอร์ที่ให้อ่านก่อน>
ขอ Format preview (ตาราง pattern/theme/steps/images) ก่อนลงรายละเอียด
```
Answer the grill fast: "recommended" is fine. Approve at **Format preview** — that is when the final look is fixed.

## Step 2 — /sketch-deck (after "approved")
```
/sketch-deck  ใช้ deck-brief.md สไตล์ pitch-minimal, เขียน slides.js จาก references/example-pitch-slides.js,
build แล้ว  sd from-slides → sd render ให้ดูทุกสไลด์  บอกช่องภาพ (sd slots) พร้อมขนาด
```

## Step 3 — pictures (only manual part)
`sd slots` lists each dashed slot (1240×640, aspect 31:16) and the exact command. Generate/pick images (ChatGPT prompt is in
the brief's Image list), then `sd fill-slot "<ref>" file.png` or drop them in the editor.

## Step 4 — touch-up
`sd build` → open `build/SketchDeck_Studio.html` → drag/rotate/edit → Save → `sd import <saved.html>`.
Small changes by message: quote the ref (`5/ภาพ 2 ขยับขึ้น 20`) — see the sketchdeck README "ภาษากลาง".

## Vocabulary to order layouts by name
old-vs-new · milestone timeline · milestone hub · hub-and-spoke · image slot · two-box ask
(themes: red=problem, green=solution/ask, blue=main flow, orange=optional, teal=evidence, purple/pink=extra).

## Worked examples
- `example-grill-QA.md` — the 10 questions + answers that fix the shape (Digital Tower roadmap pitch)
- `example-brief-pitch.md` — the resulting brief (Format preview, per-slide blocks, Image list)
- `../../sketch-deck/references/example-pitch-slides.js` — the slides.js built from that brief

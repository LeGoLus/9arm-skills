// Example: PITCH-MINIMAL style (executive pitch, ~7 slides). Reverse-engineered from a real final deck.
// Rules this file demonstrates:
//   - heading + a few short labels only (<= ~12 words per step); detail goes in `notes`
//   - NO bottom takeaway sentence (the action title IS the takeaway)
//   - 3-5 steps, one idea per step; every draw call uses only editor-native primitives
//     (txt, box, srect, sline, arrow, check, badge, stamp, imgslot) so `sd from-slides` converts 1:1
//   - image slides use imgslot() at the standard slot (180,205,1240,640) + a caption at y=172
const CONFIG = { stepLabel: 'step', boardLabel: 'board', revealedLabel: 'revealed', board: false };

const SLIDES = [
// 0 · title
{ steps:1, notes:'ทักทาย + บอกวัตถุประสงค์ 1 ประโยค', draw(E){
  E(0, txt(800, 380, 'Digital Tower Roadmap', {size:84, anchor:'middle', w:700}));
  E(0, txt(800, 470, 'แบ่งเฟสเพื่อวางแผนงบประมาณ', {size:54, anchor:'middle', w:700, color:C.blue.line}));
  E(0, sline(420, 520, 1180, 526, C.blue.line, 5));
  E(0, txt(800, 620, 'สุวรรณภูมิ (SBA) · ดอนเมือง (DMA)', {size:34, color:GRAY, anchor:'middle'}));
  E(0, txt(800, 680, 'AEROTHAI', {size:28, color:'#adb5bd', anchor:'middle', mono:true}));
}},

// 1 · old vs new panels  [pattern: old-vs-new]
{ n:1, t:'TOR เดิมมีแค่ 2 เฟส', c:C.red, steps:4, notes:'เดิมตัดสินใจได้ก้อนเดียว; แบบใหม่แตกเป็นขั้น เลือกงบได้', draw(E){
  E(0, srect(132, 227, 620, 500, '#fff'));
  E(0, txt(430, 282, 'TOR เดิม', {size:34, color:RED, anchor:'middle', base:'central', w:700}));
  E(0, box(160, 340, 540, 90, 'Phase 1: Validation / Tuning', '#f1f3f5', {fs:26, w:700}));
  E(0, box(160, 460, 540, 130, 'Phase 2: Main Ops +\nContingency (รวมก้อนเดียว)', '#f1f3f5', {fs:26, w:700}));
  E(0, txt(430, 660, 'ไม่มีจุดตัดสินใจระหว่างทาง', {size:28, color:RED, anchor:'middle'}));
  E(1, srect(860, 230, 620, 500, '#fff'));
  E(1, txt(1170, 282, 'แบบใหม่', {size:34, color:GREEN, anchor:'middle', base:'central', w:700}));
  E(1, box(900, 340, 540, 90, 'เฟสหลัก · A1–A8 (8 ขั้น)', C.blue.fill, {fs:26, w:700}));
  E(1, box(900, 460, 540, 90, 'เฟสเสริม · B0–B4 (AI เลือกได้)', C.orange.fill, {fs:26, w:700}));
  E(1, txt(1170, 610, 'ตัดงบจุดไหนก็ยังใช้งานได้จริง', {size:28, color:GREEN, anchor:'middle'}));
  E(2, arrow(750, 480, 850, 480, {color:GRAY}) + check(1450, 340, 34) + check(1450, 460, 34));
}},

// 2 · badge timeline + gate stamp + callout  [pattern: milestone timeline]
{ n:2, t:'เฟสหลัก ก่อนถึง CAAT Approve', c:C.blue, steps:5, notes:'ต้องทำเรียงลำดับ; A4 คือประตูกำกับดูแล คุมไทม์ไลน์ เร่งเองไม่ได้', draw(E){
  E(0, sline(200, 460, 1400, 460, GRAY, 4));
  const ph = [['A1','ติดตั้งกล้อง + เดินสาย','(Camera & Network)'], ['A2','เชื่อม DT Lab','(Lab Integration)'],
              ['A3','เก็บข้อมูล + HF','(Data & HF Validation)'], ['A4','Safety Case + CAAT','(Regulatory Approval)']];
  ph.forEach((p, i) => {
    const x = 260 + i * 360;
    E(i, badge(x, 460, p[0], i === 3 ? C.red.fill : C.blue.fill, 55));
    E(i, txt(x, 550, p[1], {size:23, anchor:'middle'}));
    E(i, txt(x, 578, p[2], {size:18, color:GRAY, anchor:'middle'}));
  });
  E(1, box(490, 230, 260, 130, 'จอเดียวเห็นได้แค่บางมุม\nต้องมี Video Wall', C.blue.fill, {fs:22}));
  E(1, arrow(600, 360, 615, 405, {color:GRAY}));
  E(3, stamp(1260, 310, 'CAAT GATE'));
}},

// 3 · hub → branches  [pattern: milestone hub]
{ n:3, t:'Go-Live ที่ A6 คือจุดคุ้มทุนขั้นต่ำ', c:C.green, steps:4, notes:'A6 คือจุดที่ ATC ใช้งานจริง; A7-A8 ต่อทีหลัง ไม่กระทบ Go-Live', draw(E){
  E(0, box(140, 385, 220, 90, 'A5\nCWP จริง', '#f1f3f5', {fs:24}));
  E(1, arrow(370, 430, 470, 415));
  E(1, box(480, 320, 440, 210, 'A6 · Go-Live\nใช้งานจริงกับ ATC บน Tower', C.green.fill, {fs:34}));
  E(1, stamp(770, 300, 'MVP'));
  E(2, box(1050, 260, 260, 90, 'A7\nContingency Tower', '#f1f3f5', {fs:22}));
  E(2, box(1050, 480, 260, 90, 'A8\nกล้อง Runway 3', '#f1f3f5', {fs:22}));
  E(2, arrow(932, 387, 1042, 310) + arrow(930, 413, 1043, 484));
}},

// 4 · hub-and-spoke with emoji cards  [pattern: hub-and-spoke]
{ n:4, t:'เฟสเสริม AI ห้าโมดูล (Additional)', c:C.orange, steps:3, notes:'B0 เป็นฐาน; B1-B4 เลือกเพิ่มอิสระตามงบ', draw(E){
  E(0, box(620, 220, 360, 100, 'B0 · Detection\n& Tracking', C.orange.fill, {fs:24}));
  const mods = [['🛡️ B1\nRunway\nIncursion', 140, 280], ['⏱️ B2\nRunway Occupancy\nTime', 460, 600],
                ['✈️ B3\nApproach\nMonitoring', 780, 920], ['✨ B4\nAutomatic\nSequencing', 1100, 1240]];
  mods.forEach(m => { E(1, arrow(800, 330, m[2], 420)); E(1, box(m[1], 430, 280, 170, m[0], '#fff', {fs:24})); });
}},

// 5 · image slides: one imgslot per step, caption above  [pattern: image slot]
{ n:5, t:'การวางกล้อง Best Case & Base Case', c:C.teal, steps:5, notes:'Best = 1 กล้อง/ทางออก แม่นกว่าแต่แพงกว่า; Base = ที่ติดตั้งจริงตอนนี้', draw(E){
  const cap = [['1. สุวรรณภูมิ (SBA) — Best Case', C.teal.line], ['2. สุวรรณภูมิ (SBA) — Base Case', C.blue.line],
               ['3. ดอนเมือง (DMA) — Best Case', C.orange.line], ['4. ดอนเมือง (DMA) — Base Case', C.purple.line]];
  cap.forEach((c, i) => {
    E(i + 1, txt(800, 172, c[0], {size:30, color:c[1], anchor:'middle', base:'central', w:700}), i + 2);
    E(i + 1, imgslot(180, 205, 1240, 640, 'ภาพ ' + (i + 1) + ' · ' + c[0].slice(3)), i + 2);
  });
}},

// 6 · the ask: two headed boxes  [pattern: two-box ask]
{ n:6, t:'สิ่งที่ต้องการวันนี้', c:C.green, steps:3, notes:'ขอให้รับทราบโครงสร้าง — ยังไม่ขออนุมัติงบ', draw(E){
  E(0, srect(220, 310, 560, 260, '#fff', 16));
  E(0, box(224, 314, 552, 60, 'เฟสหลัก', C.blue.fill, {fs:30, w:700}));
  E(0, txt(504, 450, 'จำเป็นถึง A4 CAAT Approve (Lab Only)\nหรือ A6 Tower Installation', {size:30, anchor:'middle', base:'central', w:700}));
  E(1, srect(820, 310, 560, 260, '#fff', 16));
  E(1, box(824, 314, 552, 60, 'เฟสเสริม', C.orange.fill, {fs:30, w:700}));
  E(1, txt(1100, 450, 'เลือกเพิ่มได้อิสระ\nEx. AI Features ตาม Requirement', {size:32, anchor:'middle', base:'central', w:700}));
}},
];

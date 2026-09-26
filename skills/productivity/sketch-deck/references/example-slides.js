// Example: 'What 1,000 hours of Claude Code taught me' (title + 15 tips).
// Copy patterns from here; coordinates are in the 1600x900 canvas.
const CONFIG = { stepLabel: 'tip', boardLabel: 'board' };

const SLIDES = [
{ steps:1, draw(E){
  E(0, txt(800, 390, 'What 1,000 hours of', {size:96, anchor:'middle', w:700}));
  E(0, txt(800, 510, 'Claude Code taught me', {size:96, anchor:'middle', w:700}));
  E(0, sline(440, 560, 1150, 566, C.orange.line, 5));
  E(0, sparkle(1235, 330, 30));
  E(0, txt(800, 690, '15 lessons, one at a time', {size:36, color:GRAY, anchor:'middle'}));
  E(0, txt(800, 760, "Adapted from Nick Saraev's Claude Code video", {size:26, color:'#adb5bd', anchor:'middle'}));
}},

{ n:1, t:"Don't trust the first output", c:C.orange, steps:5, draw(E){
  E(0, doc(150, 320, 200, 260, '#fff', {lines:6}) + txt(250, 368, 'Prompt', {size:30, anchor:'middle', w:700}));
  E(0, arrow(370, 450, 530, 450));
  E(0, doc(560, 390, 90, 120, '#fff', {lines:3}) + check(605, 345, 44));
  E(0, txt(560, 590, '🎲 worked once… lucky roll?', {size:32, color:RED}), 1);
  E(1, txt(980, 272, 'run it 3–10 times', {size:32, color:GRAY, anchor:'middle'}));
  const pass = [1,1,0,1,0,1];
  for (let i = 1; i < 6; i++){
    E(1, doc(560 + i * 150, 390, 90, 120, '#fff', {lines:3}));
    if (pass[i]) E(1, check(605 + i * 150, 345, 44));
    else { E(1, cross(605 + i * 150, 345, 38), 3); E(3, check(605 + i * 150, 345, 44)); }
  }
  E(1, txt(980, 580, '4 / 6 pass → not reliable yet', {size:34, color:RED, anchor:'middle'}), 3);
  E(2, arrow(900, 630, 262, 600, {bend:-110, color:GREEN}) + txt(580, 770, 'tighten it, test again', {size:34, color:GREEN, anchor:'middle'}));
  E(3, txt(980, 580, '6 / 6 pass → consistent', {size:34, color:GREEN, anchor:'middle'}));
  E(3, stamp(160, 290, 'SAVED'));
  E(4, txt(800, 855, 'Only save a prompt once it passes this test.', {size:38, anchor:'middle', w:700}));
}},

{ n:2, t:'Give it a way to check its own work', c:C.green, steps:5, draw(E){
  E(0, box(110, 420, 200, 90, 'Task', '#f1f3f5'));
  E(0, arrow(320, 465, 410, 465));
  E(0, box(420, 420, 230, 90, 'Attempt', C.blue.fill));
  E(0, txt(1440, 282, 'quality', {size:32, anchor:'middle'}));
  E(0, rect(1408, 560, 64, 162, C.green.fill, 6), 2);
  E(2, rect(1408, 312, 64, 410, C.green.fill, 6));
  E(0, srect(1400, 300, 80, 430, 'none', 12));
  E(0, sline(1380, 560, 1500, 560, RED, 3) + txt(1370, 518, 'build it,\nhope it works', {size:28, color:RED, anchor:'end'}));
  E(1, box(820, 230, 220, 90, 'Check', C.yellow.fill));
  E(1, box(840, 610, 190, 90, 'Fix', C.red.fill));
  E(1, arrow(560, 415, 812, 282, {bend:-60}));
  E(1, arrow(965, 328, 950, 602, {bend:-70}));
  E(1, arrow(832, 660, 560, 518, {bend:-60}));
  E(1, txt(1085, 460, 'check\nagain', {size:28, color:GRAY}));
  E(2, check(930, 190, 50) + arrow(1052, 275, 1180, 275, {color:GREEN}) + txt(1195, 286, 'ship it', {size:40, color:GREEN, base:'central'}));
  E(3, txt(305, 806, 'Ways to check:', {size:28, color:GRAY, anchor:'end', base:'central'}));
  E(3, chip(320, 770, 300, 70, '🧪 run the tests') + chip(645, 770, 300, 70, '📷 screenshot it') + chip(970, 770, 420, 70, '📄 compare to an example'));
  E(4, txt(800, 880, 'No way to check yet? Have Claude set one up first.', {size:34, anchor:'middle', w:700}));
}},

{ n:3, t:'Let the code be the context', c:C.teal, steps:4, draw(E){
  E(0, doc(120, 280, 260, 330, '#fff', {lines:7, lc:[INK, GREEN, C.purple.line, C.blue.line]}));
  E(0, txt(250, 660, 'code v4', {size:30, anchor:'middle', mono:true}));
  const ys = [285, 425, 565], names = ['NOTES.md', 'SPEC.md', 'LOG.md'];
  ys.forEach((y, i) => {
    E(0, dashed(390, 445, 512, y + 42) + txt(452, (445 + y + 42) / 2, '≠', {size:46, color:RED, anchor:'middle', base:'central'}));
    E(0, doc(520, y, 70, 85, C.yellow.fill, {lines:3}) + txt(610, y + 36, names[i], {size:26, mono:true}) + txt(610, y + 72, 'v1', {size:22, color:GRAY, mono:true}));
    E(1, zigzag(505, y + 6, 300, 72));
  });
  E(1, txt(140, 592, '// why: rate limit', {size:21, color:GREEN, mono:true}));
  E(0, txt(120, 745, 'two sources of truth drift apart', {size:38, color:RED}), 1);
  E(1, txt(120, 745, 'the code, plus a few inline comments', {size:38, color:GREEN}));
  E(2, win(900, 240, 420, 240, 'new session') + bubble(925, 305, 370, 115, 'Add a logout button\nto the navbar.', C.blue.fill, {fs:30}));
  E(2, arrow(1110, 490, 1110, 560) + robot(1110, 625) + arrow(1165, 625, 1262, 625) +
       doc(1275, 590, 55, 70, '#fff', {lines:3}) + doc(1345, 590, 55, 70, '#fff', {lines:3}) + doc(1415, 590, 55, 70, '#fff', {lines:3}) +
       magnifier(1462, 606) + txt(1110, 710, 'it reads the code it needs', {size:28, color:GRAY, anchor:'middle'}));
  E(3, srect(880, 745, 640, 135, C.yellow.fill, 12) + txt(905, 782, 'CLAUDE.md is the exception:', {size:30, w:700}) +
       check(925, 824, 28) + txt(955, 824, 'how to work (preferences, lessons)', {size:28, base:'central'}) +
       cross(925, 858, 22) + txt(955, 858, 'what the code does', {size:28, color:GRAY, base:'central'}));
}},

{ n:4, t:'Let Claude write your prompt', c:C.purple, steps:5, draw(E){
  E(0, bubble(90, 240, 450, 120, 'I want X for Y audience.\nHelp me write a prompt.', '#fff', {fs:30}));
  E(0, stick(150, 640));
  E(1, box(620, 250, 360, 72, "Who's it for?", C.purple.fill, {fs:30}) + box(620, 345, 360, 72, 'What does good look like?', C.purple.fill, {fs:30}) + box(620, 440, 360, 72, 'Any examples?', C.purple.fill, {fs:30}));
  E(1, sparkle(760, 600, 30) + txt(805, 602, 'Claude interviews you', {size:28, color:GRAY, base:'central'}));
  E(2, box(250, 410, 220, 60, 'founders', '#f1f3f5', {fs:26}) + box(250, 485, 220, 60, 'one page', '#f1f3f5', {fs:26}) + box(250, 560, 220, 60, 'like this one', '#f1f3f5', {fs:26}));
  E(2, arrow(610, 470, 482, 510, {dash:true, color:GRAY}));
  E(3, arrow(995, 380, 1110, 380) + doc(1120, 240, 210, 260, '#fff', {lines:6}) + txt(1225, 290, 'Prompt', {size:28, anchor:'middle', w:700}));
  E(3, arrow(1225, 510, 1225, 578) + win(1105, 590, 240, 165, 'fresh chat') + check(1225, 695, 58));
  E(4, check(300, 800, 30) + txt(332, 800, 'high-stakes or unfamiliar: worth it', {size:32, base:'central'}) +
       cross(300, 852, 24) + txt(332, 852, 'quick, simple asks: skip it', {size:32, color:GRAY, base:'central'}));
}},

{ n:5, t:'Watch your context window', c:C.yellow, steps:4, draw(E){
  E(0, txt(150, 268, 'context window', {size:30, color:GRAY}));
  const segs = [[0,110,'#dee2e6','system'],[110,440,C.purple.fill,'MCP tools\n(loaded even if unused)'],[440,540,C.yellow.fill,'CLAUDE.md'],[540,760,C.blue.fill,'files + chat']];
  segs.forEach(s => E(0, rect(150 + s[0], 290, s[1] - s[0], 90, s[2], 8) + txt(150 + (s[0] + s[1]) / 2, 425, s[3], {size:23, anchor:'middle', color:'#495057'})));
  E(1, rect(910, 290, 420, 90, '#74c0fc', 4) + txt(1120, 425, 'long session', {size:23, anchor:'middle', color:'#495057'}));
  E(0, srect(150, 290, 1300, 90, 'none', 10));
  E(1, txt(1450, 262, '⚠ quality drops as it fills', {size:30, color:RED, anchor:'end'}));
  const tips = [['/context', "see what's eating tokens"], ['prune tools', "disable MCPs you aren't using"], ['/compact', 'summarize, then keep going'], ['/clear', 'start a fresh session']];
  tips.forEach((t, i) => {
    const x = i % 2 ? 820 : 150, y = i < 2 ? 510 : 620;
    E(2, srect(x, y, 630, 88, '#fff', 12) + txt(x + 24, y + 46, t[0], {size:28, mono:true, w:700, base:'central'}) + txt(x + 250, y + 46, t[1], {size:28, color:'#495057', base:'central'}));
  });
  E(3, txt(800, 830, 'Treat context like RAM, not a junk drawer.', {size:40, anchor:'middle', w:700}));
}},

{ n:6, t:'Brief it like a contractor', c:C.red, steps:4, draw(E){
  E(0, srect(120, 230, 620, 500, '#fff', 14) + txt(430, 282, 'Micromanaging', {size:34, anchor:'middle', w:700, color:RED, base:'central'}));
  const steps = ['1. open src/auth.ts', '2. find login()', '3. add a try/catch', '4. log the error', '5. rename x → user', '6. run npm test', '7. …and 20 more'];
  steps.forEach((s, i) => E(0, txt(160, 350 + i * 50, s, {size:25, mono:true, color:'#495057'})));
  E(0, txt(430, 790, 'it follows steps and stops thinking', {size:30, color:RED, anchor:'middle'}));
  E(1, srect(860, 230, 620, 500, '#fff', 14) + txt(1170, 282, 'Contractor brief', {size:34, anchor:'middle', w:700, color:GREEN, base:'central'}));
  E(1, txt(890, 345, 'Goal: login never crashes on bad input', {size:26}));
  E(1, txt(890, 405, 'Definition of Done:', {size:28, w:700}));
  const dod = ['all auth tests pass', 'no unhandled errors in logs', 'matches existing code style', 'short summary of changes'];
  dod.forEach((d, i) => { const y = 450 + i * 55; E(1, srect(895, y - 14, 28, 28, '#fff', 5) + txt(940, y, d, {size:26, base:'central'})); E(2, check(911, y - 2, 30)); });
  E(1, txt(890, 700, 'Out of scope: /billing', {size:25, color:GRAY}));
  E(2, txt(1170, 790, 'it reasons its way to done', {size:30, color:GREEN, anchor:'middle'}));
  E(3, txt(800, 865, 'Define the finish line, not the route.', {size:40, anchor:'middle', w:700}));
}},

{ n:7, t:'Diagnose before you fix', c:C.blue, steps:3, draw(E){
  const top = [['bug', C.red.fill], ['edit', '#f1f3f5'], ['new bug', C.red.fill], ['edit', '#f1f3f5'], ['new bug', C.red.fill]];
  top.forEach((t, i) => { const x = 130 + i * 250; E(0, box(x, 250, 180, 70, t[0], t[1], {fs:28})); if (i) E(0, arrow(x - 64, 285, x - 8, 285)); });
  E(0, cross(1420, 285, 40) + txt(130, 370, 'fixing on sight = whack-a-mole', {size:30, color:RED}));
  E(1, box(130, 525, 170, 70, 'bug', C.red.fill, {fs:28}) + arrow(310, 560, 390, 560));
  E(1, srect(400, 440, 340, 240, '#fff', 12) + txt(425, 482, 'Issues found:', {size:26, w:700}) +
       ['1. null user on login', '2. token refresh race', '3. missing DB index', '4. stale cache'].map((s, i) => txt(425, 530 + i * 40, s, {size:21, mono:true, color:'#495057'})).join(''));
  E(1, arrow(750, 560, 820, 560) + box(830, 525, 210, 70, 'you review', C.yellow.fill, {fs:28}) + arrow(1050, 560, 1120, 560) + box(1130, 525, 190, 70, 'fix all', C.green.fill, {fs:28}) + check(1380, 560, 54));
  E(1, txt(130, 440, 'list → approve → edit', {size:30, color:GREEN}));
  E(2, srect(130, 740, 1340, 100, '#f8f9fa', 12) + txt(800, 792, '"Don\'t edit anything yet. List every issue you see, ranked by severity."', {size:25, mono:true, anchor:'middle', base:'central'}));
}},

{ n:8, t:'Prototype with MCPs, ship as Skills', c:C.pink, steps:4, draw(E){
  E(0, srect(130, 230, 440, 490, '#fff', 14) + rect(134, 234, 432, 62, C.pink.fill, 10) + txt(350, 268, 'MCP server', {size:32, anchor:'middle', w:700, base:'central'}));
  ['create_issue', 'list_repos', 'search_code', 'get_file', 'update_pr', 'list_users', 'post_comment', '+ 34 more…'].forEach((s, i) => E(0, txt(165, 345 + i * 45, s, {size:23, mono:true, color:i === 7 ? GRAY : '#495057'})));
  E(0, txt(350, 775, 'every tool loads, every session', {size:28, color:RED, anchor:'middle'}));
  E(1, arrow(600, 475, 960, 475) + txt(780, 440, 'workflow works? distill it', {size:28, color:GRAY, anchor:'middle'}));
  E(2, doc(990, 260, 300, 380, '#fff', {lines:6}) + txt(1140, 318, 'SKILL.md', {size:30, mono:true, w:700, anchor:'middle'}));
  E(2, doc(1320, 470, 130, 170, '#fff', {lines:4}) + txt(1385, 670, 'run.py', {size:24, mono:true, anchor:'middle'}));
  E(2, txt(1220, 740, 'loads only when it\'s needed', {size:30, color:GREEN, anchor:'middle'}));
  E(3, txt(800, 855, 'Explore with an MCP. Exploit with a Skill.', {size:40, anchor:'middle', w:700}));
}},

{ n:9, t:'Split work across parallel sub-agents', c:C.teal, steps:4, draw(E){
  E(0, box(620, 200, 360, 84, 'Refactor the app', '#f1f3f5'));
  const lanes = [['Agent A', '/api/**'], ['Agent B', '/ui/**'], ['Agent C', '/tests/**']];
  lanes.forEach((l, i) => {
    const x = 160 + i * 460;
    E(1, arrow(800, 292, x + 180, 400, {bend:i === 1 ? 0 : (i ? 30 : -30)}));
    E(1, srect(x, 410, 360, 150, '#fff', 14) + robot(x + 72, 492, .85) + txt(x + 140, 465, l[0], {size:30, w:700}) + txt(x + 140, 515, l[1], {size:24, mono:true, color:GRAY}));
    E(2, arrow(x + 180, 568, 800, 672, {bend:i === 1 ? 0 : (i ? -30 : 30)}));
  });
  E(1, txt(1000, 245, 'scoped: no two agents touch\nthe same files', {size:26, color:GREEN}));
  E(2, box(620, 680, 360, 84, 'merge + verify', C.green.fill));
  E(3, txt(800, 855, '3 agents × 10 min beats 1 agent × 30 min', {size:40, anchor:'middle', w:700}));
}},

{ n:10, t:'Write a handoff before you reset', c:C.green, steps:4, draw(E){
  E(0, win(110, 230, 420, 480, 'session 1'));
  [[140, 310, 240, '#f1f3f5'], [260, 365, 240, C.blue.fill], [140, 420, 280, '#f1f3f5'], [220, 475, 280, C.blue.fill], [140, 530, 220, '#f1f3f5']].forEach(b => E(0, rect(b[0], b[1], b[2], 38, b[3], 10)));
  E(0, meter(140, 650, 360, .86, C.red.fill, 'context 86% full'));
  E(1, arrow(545, 470, 625, 470));
  E(1, `<g transform="rotate(-1.5 830 470)">${srect(640, 230, 380, 480, C.yellow.fill, 6)}</g>`);
  const note = [['## HANDOFF', INK, 700], ['Done:', GREEN, 700], ['auth refactor + tests', '#495057', 400], ['Decisions:', C.blue.line, 700], ['keep JWT, drop sessions', '#495057', 400], ['Next:', C.orange.line, 700], ['wire the logout button', '#495057', 400], ['Open issues:', RED, 700], ['flaky e2e test on CI', '#495057', 400]];
  note.forEach((n, i) => E(1, txt(668, 285 + i * 47, n[0], {size:22, mono:true, color:n[1], w:n[2]})));
  E(2, arrow(1035, 470, 1100, 470) + win(1110, 230, 380, 480, 'session 2') + txt(1300, 420, 'picks up right\nwhere you left off', {size:30, color:'#495057', anchor:'middle', base:'central'}) + meter(1140, 650, 320, .06, C.green.fill, 'context 6%'));
  E(3, txt(800, 830, 'Ask for the handoff before you /clear.', {size:40, anchor:'middle', w:700}));
}},

{ n:11, t:'Ask side questions with /btw', c:C.purple, steps:4, draw(E){
  E(0, robot(190, 345) + txt(270, 292, 'main task: migrate 40 files', {size:30}));
  E(0, rect(274, 324, 420, 44, C.blue.fill, 8), 2);
  E(2, rect(274, 324, 900, 44, C.blue.fill, 8));
  E(0, srect(270, 320, 1150, 52, 'none', 10));
  E(1, stick(190, 610) + bubble(270, 480, 590, 84, '/btw what does --dry-run do?', C.purple.fill, {fs:26, mono:true}));
  E(1, srect(880, 600, 560, 84, '#f1f3f5', 22) + txt(1160, 644, 'It previews changes without writing.', {size:28, anchor:'middle', base:'central'}) + txt(880, 725, 'answered on the side', {size:26, color:GRAY}));
  E(2, check(290, 420, 34) + txt(320, 422, 'main task never stopped', {size:30, color:GREEN, base:'central'}));
  E(3, txt(800, 840, 'Side questions go beside the work, not in front of it.', {size:38, anchor:'middle', w:700}));
}},

{ n:12, t:'Fan out cheap, fan in smart', c:C.yellow, steps:4, draw(E){
  for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) E(0, doc(115 + c * 72, 255 + r * 100, 50, 66, '#fff', {lines:2}));
  E(0, txt(250, 690, 'huge search space', {size:28, color:GRAY, anchor:'middle'}));
  E(1, txt(610, 225, 'fan out: cheap & fast', {size:28, color:GRAY, anchor:'middle'}));
  for (let i = 0; i < 6; i++){ const y = 250 + i * 76; E(1, arrow(410, 300 + i * 60, 512, y + 28) + box(520, y, 180, 56, 'Haiku', C.yellow.fill, {fs:26})); E(2, arrow(708, y + 28, 852, 470, {color:'#adb5bd'})); }
  E(2, doc(860, 400, 120, 150, '#fff', {lines:4}) + txt(920, 585, 'findings', {size:26, color:GRAY, anchor:'middle'}));
  E(2, arrow(992, 475, 1090, 475) + txt(1220, 378, 'fan in: one smart pass', {size:28, color:GRAY, anchor:'middle'}) + box(1100, 410, 240, 130, 'Opus', C.purple.fill, {fs:40, w:700}));
  E(2, arrow(1350, 475, 1420, 475) + txt(1432, 478, 'answer', {size:30, base:'central'}) + check(1560, 470, 36));
  E(3, txt(345, 790, 'all frontier model:', {size:28, anchor:'end', base:'central'}) + rect(365, 772, 900, 38, C.red.fill, 8) + txt(380, 792, '$$$$$$$$', {size:26, color:RED, base:'central'}));
  E(3, txt(345, 848, 'fan-out / fan-in:', {size:28, anchor:'end', base:'central'}) + rect(365, 830, 250, 38, C.green.fill, 8) + txt(380, 850, '$$', {size:26, color:GREEN, base:'central'}));
}},

{ n:13, t:'Keep CLAUDE.md lean', c:C.blue, steps:4, draw(E){
  E(0, terminal(110, 240, 300, 80, '$ /init') + arrow(420, 280, 545, 280));
  E(0, doc(560, 220, 320, 560, '#fff'));
  const keep = [3, 7, 10, 13];
  for (let k = 0; k < 14; k++){
    const y = 300 + k * 33, w = 150 + rnd() * 90;
    E(0, sline(595, y, 595 + w, y, '#495057', 2.2));
    if (keep.includes(k)) E(1, check(900, y - 2, 26)); else E(1, sline(585, y + j(2), 850, y + j(2), RED, 3));
  }
  E(0, txt(720, 830, 'auto-generated: 400 lines', {size:28, color:RED, anchor:'middle'}), 1);
  E(1, txt(720, 830, 'cut "what the code does"', {size:28, color:RED, anchor:'middle'}));
  E(2, arrow(955, 480, 1045, 480) + srect(1060, 240, 440, 470, '#fff', 10));
  [['# CLAUDE.md', INK, 700], ['## How we work', C.blue.line, 700], ['- test: pnpm test', '#495057', 400], ['- small PRs, one concern', '#495057', 400], ['- ask before new deps', '#495057', 400], ['## Lessons', C.blue.line, 700], ['- mock time in tests', '#495057', 400], ['- never hand-edit migrations', '#495057', 400]]
    .forEach((l, i) => E(2, txt(1085, 295 + i * 50, l[0], {size:22, mono:true, color:l[1], w:l[2]})));
  E(2, txt(1280, 760, '~40 lines, always current', {size:28, color:GREEN, anchor:'middle'}));
  E(3, txt(800, 870, 'It loads every session, so every line has to earn its place.', {size:36, anchor:'middle', w:700}));
}},

{ n:14, t:'Keep a backup agent ready', c:C.green, steps:4, draw(E){
  E(0, doc(140, 260, 200, 250, '#fff', {lines:5}) + txt(240, 550, 'CLAUDE.md', {size:28, mono:true, anchor:'middle'}));
  E(0, doc(520, 260, 200, 250, '#fff', {lines:5}) + txt(620, 550, 'AGENTS.md', {size:28, mono:true, anchor:'middle'}));
  E(0, arrow(350, 385, 508, 385, {dash:true}) + txt(430, 362, 'symlink', {size:26, color:GRAY, anchor:'middle'}));
  E(0, terminal(140, 620, 580, 72, '$ ln -s CLAUDE.md AGENTS.md'));
  E(1, arrow(735, 330, 930, 295) + box(940, 240, 380, 110, 'Claude Code', C.orange.fill) + cross(1370, 295, 40) + txt(1130, 395, 'API outage / rate limit', {size:28, color:RED, anchor:'middle'}));
  E(2, arrow(735, 440, 930, 555) + box(940, 500, 380, 110, 'backup agent\n(Codex, Gemini CLI…)', C.green.fill, {fs:28}) + txt(1130, 660, 'same rules, keeps shipping', {size:28, color:GREEN, anchor:'middle'}));
  E(3, txt(800, 830, 'One instruction file that any agent can read.', {size:40, anchor:'middle', w:700}));
}},

{ n:15, t:'Make it teach itself', c:C.red, steps:5, draw(E){
  E(0, box(620, 210, 360, 84, 'finish a task', '#f1f3f5'));
  E(1, arrow(988, 252, 1200, 412, {bend:-50}) + box(1060, 420, 460, 116, 'ask: "How could you have done that\nfaster, with fewer tokens?"', C.yellow.fill, {fs:25}));
  E(2, arrow(1250, 545, 1008, 700, {bend:-50}) + box(600, 660, 400, 90, 'turn it into a positive rule', C.pink.fill, {fs:28}));
  E(2, txt(800, 420, '✗ "don\'t scan the whole repo"', {size:28, color:RED, anchor:'middle'}) + txt(800, 480, '✓ "start in /src/api, then grep"', {size:28, color:GREEN, anchor:'middle'}));
  E(3, arrow(592, 705, 300, 528, {bend:-50}) + box(100, 430, 380, 90, 'add it to CLAUDE.md', C.green.fill, {fs:30}));
  E(4, arrow(300, 422, 612, 252, {bend:-50}) + txt(800, 575, 'every loop, it gets sharper', {size:28, color:GRAY, anchor:'middle'}));
  E(4, txt(800, 855, 'Turn every "don\'t" into a "do", and keep it.', {size:40, anchor:'middle', w:700}));
}}
];

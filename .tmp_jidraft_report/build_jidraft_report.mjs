import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const vault = "C:/vault/koreanwithji_vault";
const sourceXlsx = path.join(vault, "02_product/02_course_creation/00_curriculum_and_index/01_Ji_Draft_index.xlsx");
const rawRoot = path.join(vault, "02_product/01_raw/01_by_level_lesson");
const outputXlsx = path.join(vault, "02_product/02_course_creation/00_curriculum_and_index/01_Ji_Draft_review_report.xlsx");
const previewDir = path.join(vault, ".tmp_jidraft_report", "previews");

function normalize(text) {
  return String(text ?? "")
    .normalize("NFKC")
    .toLocaleLowerCase()
    .replace(/[^\p{L}\p{N}_]+/gu, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function words(text) {
  const n = normalize(text);
  return n ? n.split(/\s+/) : [];
}

function contentWithoutFrontMatter(text) {
  return String(text).replace(/^---\s*[\s\S]*?\s*---\s*/u, "");
}

function paragraphs(text) {
  return contentWithoutFrontMatter(text)
    .split(/\n\s*\n/u)
    .map(normalize)
    .filter((x) => words(x).length > 5);
}

function levelName(levelDir) {
  if (levelDir.startsWith("00_")) return "VSL";
  if (levelDir.startsWith("01_")) return "Intro";
  if (levelDir.startsWith("02_")) return "Hangul";
  if (levelDir.startsWith("03_")) return "Numbers";
  return levelDir.startsWith("Level_") ? levelDir.slice(6) : levelDir;
}

function lessonInfo(filePath) {
  const draftDir = path.dirname(filePath);
  const lessonDir = path.dirname(draftDir);
  const levelDir = path.basename(path.dirname(lessonDir));
  const lessonFolder = path.basename(lessonDir);
  return {
    level: levelName(levelDir),
    lesson: Number(lessonFolder.split("_", 1)[0]),
    lessonFolder,
    levelDir,
  };
}

function key(level, lesson) {
  return `${String(level)}|${lesson === null || lesson === undefined || lesson === "" ? "" : Number(lesson)}`;
}

async function walk(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...await walk(full));
    else files.push(full);
  }
  return files;
}

function longestCommonBlock(a, b) {
  const dp = new Array(b.length + 1).fill(0);
  let best = 0;
  for (let i = 1; i <= a.length; i++) {
    const next = new Array(b.length + 1).fill(0);
    for (let j = 1; j <= b.length; j++) {
      if (a[i - 1] === b[j - 1]) {
        next[j] = dp[j - 1] + 1;
        if (next[j] > best) best = next[j];
      }
    }
    for (let j = 0; j <= b.length; j++) dp[j] = next[j];
  }
  return best;
}

function bestComparison(draftText, scripts) {
  const draftParas = paragraphs(draftText);
  const draftWords = words(draftParas.join(" "));
  let best = null;
  for (const script of scripts) {
    const scriptParas = paragraphs(script.text);
    const scriptText = scriptParas.join(" ");
    const scriptWords = words(scriptText);
    const coveredWords = draftParas
      .filter((paragraph) => scriptText.includes(paragraph))
      .reduce((sum, paragraph) => sum + words(paragraph).length, 0);
    const longest = longestCommonBlock(draftWords, scriptWords);
    const metrics = {
      coveredWords,
      draftWords: draftWords.length,
      coverage: draftWords.length ? coveredWords / draftWords.length : 0,
      longestWords: longest,
      longestCoverage: draftWords.length ? longest / draftWords.length : 0,
      scriptWords: scriptWords.length,
    };
    if (!best || metrics.coverage > best.metrics.coverage ||
      (metrics.coverage === best.metrics.coverage && metrics.longestCoverage > best.metrics.longestCoverage)) {
      best = { script, metrics };
    }
  }
  return best;
}

function rel(p) {
  return path.relative(vault, p).replaceAll("\\", "/");
}

function pct(value) {
  return `${(value * 100).toFixed(1)}%`;
}

function excelCol(n) {
  let s = "";
  let x = n;
  while (x > 0) {
    const r = (x - 1) % 26;
    s = String.fromCharCode(65 + r) + s;
    x = Math.floor((x - 1) / 26);
  }
  return s;
}

function styleSheet(sheet, usedRange, headerRange, widths = []) {
  sheet.showGridLines = false;
  usedRange.format = {
    font: { name: "Arial", size: 10, color: "#1F2937" },
    verticalAlignment: "center",
  };
  headerRange.format = {
    fill: "#1F4E78",
    font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" },
    horizontalAlignment: "center",
    verticalAlignment: "center",
    wrapText: true,
  };
  headerRange.format.rowHeight = 32;
  usedRange.format.borders = { preset: "inside", style: "thin", color: "#D9E2F3" };
  if (widths.length) {
    widths.forEach((width, i) => {
      sheet.getRange(`${excelCol(i + 1)}:${excelCol(i + 1)}`).format.columnWidth = width;
    });
  }
}

const source = await SpreadsheetFile.importXlsx(await FileBlob.load(sourceXlsx));
const currentRows = source.worksheets.getItem("Ji_Draft_index").getUsedRange().values;
const statusRows = source.worksheets.getItem("이전_매핑").getUsedRange().values;
const currentHeader = currentRows[0];
const statusHeader = statusRows[0];
const currentData = currentRows.slice(1);
const statusData = statusRows.slice(1).filter((row) => row[0] !== null);

const allFiles = (await walk(rawRoot)).filter((p) => p.toLowerCase().endsWith(".md") && p.split(path.sep).includes("01_Ji_draft"));
const actualByKey = new Map();
for (const file of allFiles) {
  const info = lessonInfo(file);
  const k = key(info.level, info.lesson);
  if (!actualByKey.has(k)) actualByKey.set(k, []);
  actualByKey.get(k).push(file);
}

const statusByKey = new Map(statusData.map((row) => [key(row[0], row[1]), row[5]]));
const titleByKey = new Map(statusData.map((row) => [key(row[0], row[1]), row[2]]));
const scriptsByKey = new Map();
for (const [k, files] of actualByKey) {
  const scripts = [];
  for (const draft of files) {
    const amiraDir = path.join(path.dirname(path.dirname(draft)), "03_Amira");
    let entries = [];
    try { entries = await fs.readdir(amiraDir, { withFileTypes: true }); } catch { entries = []; }
    for (const entry of entries) {
      if (entry.isFile() && entry.name.toLocaleLowerCase().includes("lesson script") && entry.name.toLocaleLowerCase().endsWith(".md")) {
        const full = path.join(amiraDir, entry.name);
        if (!scripts.some((x) => x.path === full)) scripts.push({ path: full, text: await fs.readFile(full, "utf8") });
      }
    }
  }
  scriptsByKey.set(k, scripts);
}

const comparisons = [];
const noScript = [];
for (const [k, files] of actualByKey) {
  const [level, lessonText] = k.split("|");
  const lesson = Number(lessonText);
  const scripts = scriptsByKey.get(k) ?? [];
  if (!scripts.length) {
    for (const file of files) noScript.push({ level, lesson, title: titleByKey.get(k) ?? "", draft: file });
    continue;
  }
  for (const draft of files) {
    const result = bestComparison(await fs.readFile(draft, "utf8"), scripts);
    const status = result.metrics.coverage >= 0.74 ? "복사·발췌" : result.metrics.coverage >= 0.4 ? "부분 복사 의심" : "독자 작성 비중 높음";
    if (status !== "독자 작성 비중 높음") comparisons.push({ level, lesson, title: titleByKey.get(k) ?? "", draft, script: result.script.path, status, metrics: result.metrics });
  }
}

const fileCheckRows = statusData.map((row) => {
  const k = key(row[0], row[1]);
  const files = actualByKey.get(k) ?? [];
  const scripts = scriptsByKey.get(k) ?? [];
  const indexCurrent = currentData.filter((x) => key(x[1], x[2]) === k);
  const pathExists = indexCurrent.length === 0 ? "목록 없음" : indexCurrent.every((x) => x[7] && fs.stat(path.join(rawRoot, x[7])).then(() => true).catch(() => false));
  return [
    row[0], row[1], row[2], row[4], row[5], files.length,
    files.map(rel).join("\n"), scripts.length,
    row[5] === "O" && files.length > 0 ? "일치" : row[5] === "X" && files.length > 0 ? "X인데 파일 있음" : row[5] === "O" && files.length === 0 ? "O인데 파일 없음" : "일치",
    files.length ? "" : "실제 01_Ji_draft 파일 없음",
  ];
});

const clearCount = comparisons.filter((x) => x.status === "복사·발췌").length;
const partialCount = comparisons.filter((x) => x.status === "부분 복사 의심").length;
const oRows = statusData.filter((r) => r[5] === "O");
const xRows = statusData.filter((r) => r[5] === "X");
const xWithFiles = xRows.filter((r) => (actualByKey.get(key(r[0], r[1])) ?? []).length > 0);
const oWithFiles = oRows.filter((r) => (actualByKey.get(key(r[0], r[1])) ?? []).length > 0);

const workbook = Workbook.create();
const summary = workbook.worksheets.add("요약");
const fileCheck = workbook.worksheets.add("파일 존재 대조");
const copyReview = workbook.worksheets.add("복사 판정");
const noScriptSheet = workbook.worksheets.add("비교 불가");

summary.getRange("A1:F1").merge();
summary.getRange("A1").values = [["Ji_Draft 검토 보고서"]];
summary.getRange("A3:B3").values = [["항목", "수치"]];
summary.getRange("A4:B13").values = [
  ["검토 기준일", "2026-10-21"],
  ["index O 표시 레슨", oRows.length],
  ["index X 표시 레슨", xRows.length],
  ["실제 Ji_draft 파일", allFiles.length],
  ["O 표시 중 실제 파일 있음", oWithFiles.length],
  ["X 표시 중 실제 파일 있음", xWithFiles.length],
  ["복사·발췌 판정", clearCount],
  ["부분 복사 의심", partialCount],
  ["Amira Script 없음", noScript.length],
  ["원본 보존 상태", "원본·index 읽기 전용"],
];
summary.getRange("D3:F3").values = [["판정 기준", "내용", "출처"]];
summary.getRange("D4:F8").values = [
  ["복사·발췌", "Draft 문단 단어의 74% 이상이 같은 Amira Lesson Script에 그대로 포함", "01_raw/01_by_level_lesson"],
  ["부분 복사 의심", "Draft 문단 단어의 40% 이상 74% 미만이 같은 Script에 포함", "01_raw/01_by_level_lesson"],
  ["파일 대조", "index의 O/X 표시와 실제 01_Ji_draft 파일 수 비교", "01_Ji_Draft_index.xlsx"],
  ["주의", "같은 Amira Script가 서로 다른 레슨 Draft에 반복 사용된 경우를 별도 확인", "03_Amira/Lesson Script.md"],
  ["원본", "이 보고서는 원본을 수정하지 않고 검토 결과만 복사해 기록", "01_raw/01_raw.md"],
];
summary.getRange("A1:F1").format = { font: { name: "Arial", size: 15, bold: true, color: "#1F2937" }, verticalAlignment: "center" };
summary.getRange("A1:F1").format.rowHeight = 28;
styleSheet(summary, summary.getRange("A3:F13"), summary.getRange("A3:B3"), [28, 20, 4, 22, 58, 34]);
summary.getRange("D3:F3").format = { fill: "#5B9BD5", font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" }, horizontalAlignment: "center", verticalAlignment: "center", wrapText: true };
summary.getRange("D4:F8").format.wrapText = true;
summary.freezePanes.freezeRows(3);

fileCheck.getRange("A1:J1").merge();
fileCheck.getRange("A1").values = [["Draft 보유여부와 실제 파일 대조"]];
const fileHeaders = ["Ji 레벨", "Ji 레슨", "Ji 레슨 Title", "Ref_No", "index 표시", "실제 파일 수", "실제 파일 경로", "Amira Script 수", "대조 결과", "비고"];
fileCheck.getRange("A3:J3").values = [fileHeaders];
fileCheck.getRange(`A4:J${3 + fileCheckRows.length}`).values = fileCheckRows;
styleSheet(fileCheck, fileCheck.getRange(`A3:J${3 + fileCheckRows.length}`), fileCheck.getRange("A3:J3"), [12, 10, 42, 18, 12, 12, 70, 15, 18, 30]);
fileCheck.getRange(`G4:G${3 + fileCheckRows.length}`).format.wrapText = true;
fileCheck.getRange(`I4:I${3 + fileCheckRows.length}`).format.wrapText = true;
fileCheck.getRange(`A3:J${3 + fileCheckRows.length}`).format.rowHeight = 22;
fileCheck.freezePanes.freezeRows(3);
fileCheck.tables.add(`A3:J${3 + fileCheckRows.length}`, true, "DraftFileCheckTable");

copyReview.getRange("A1:J1").merge();
copyReview.getRange("A1").values = [["Amira Lesson Script와의 복사·발췌 판정"]];
const copyHeaders = ["판정", "Ji 레벨", "Ji 레슨", "Ji 레슨 Title", "Ji Draft 파일", "비교한 Amira Script", "Draft 단어 수", "문단 단어 일치율", "최장 연속 일치율", "판정 근거"];
copyReview.getRange("A3:J3").values = [copyHeaders];
const copyRows = comparisons.map((x) => [x.status, x.level, x.lesson, x.title, rel(x.draft), rel(x.script), x.metrics.draftWords, pct(x.metrics.coverage), pct(x.metrics.longestCoverage), x.status === "복사·발췌" ? "Draft 문단 대부분이 Script에 그대로 존재" : "Script와 긴 문단 구간이 반복되지만 독자 작성 부분도 있음"]);
copyReview.getRange(`A4:J${3 + copyRows.length}`).values = copyRows;
styleSheet(copyReview, copyReview.getRange(`A3:J${3 + copyRows.length}`), copyReview.getRange("A3:J3"), [18, 12, 10, 42, 62, 54, 14, 18, 18, 48]);
copyReview.getRange(`E4:F${3 + copyRows.length}`).format.wrapText = true;
copyReview.getRange(`J4:J${3 + copyRows.length}`).format.wrapText = true;
copyReview.freezePanes.freezeRows(3);
copyReview.tables.add(`A3:J${3 + copyRows.length}`, true, "DraftCopyReviewTable");

noScriptSheet.getRange("A1:E1").merge();
noScriptSheet.getRange("A1").values = [["Amira Lesson Script가 없어 내용 비교가 불가능한 파일"]];
const noScriptHeaders = ["Ji 레벨", "Ji 레슨", "Ji 레슨 Title", "Ji Draft 파일", "상태"];
noScriptSheet.getRange("A3:E3").values = [noScriptHeaders];
const noScriptRows = noScript.map((x) => [x.level, x.lesson, x.title, rel(x.draft), "Amira Lesson Script 없음"]);
noScriptSheet.getRange(`A4:E${3 + noScriptRows.length}`).values = noScriptRows;
styleSheet(noScriptSheet, noScriptSheet.getRange(`A3:E${3 + noScriptRows.length}`), noScriptSheet.getRange("A3:E3"), [12, 10, 42, 75, 24]);
noScriptSheet.getRange(`D4:E${3 + noScriptRows.length}`).format.wrapText = true;
noScriptSheet.freezePanes.freezeRows(3);
noScriptSheet.tables.add(`A3:E${3 + noScriptRows.length}`, true, "DraftNoScriptTable");

for (const sheet of [summary, fileCheck, copyReview, noScriptSheet]) {
  sheet.getRange("A1").format.font = { name: "Arial", size: 15, bold: true, color: "#1F2937" };
}

workbook.recalculate();
await fs.mkdir(previewDir, { recursive: true });
for (const sheet of [summary, fileCheck, copyReview, noScriptSheet]) {
  const preview = await workbook.render({ sheetName: sheet.name, autoCrop: "all", scale: 1, format: "png" });
  await fs.writeFile(path.join(previewDir, `${sheet.name}.png`), new Uint8Array(await preview.arrayBuffer()));
}
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputXlsx);

console.log(JSON.stringify({ outputXlsx, allFiles: allFiles.length, oRows: oRows.length, xRows: xRows.length, xWithFiles: xWithFiles.length, clearCount, partialCount, noScript: noScript.length }, null, 2));

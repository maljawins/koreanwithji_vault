import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "file:///C:/Users/Jigyo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const root = "C:/vault/koreanwithji_vault/02_product/01_raw/01_by_level_lesson";
const workbookPath = "C:/vault/koreanwithji_vault/02_product/02_course_creation/00_curriculum_and_index/01_Ji_Draft_index.xlsx";

async function walk(dir) {
  const out = [];
  for (const ent of await fs.readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, ent.name);
    if (ent.isDirectory()) out.push(...await walk(full));
    else if (ent.isFile() && ent.name.toLowerCase().endsWith(".md") && full.split(path.sep).includes("01_Ji_draft")) out.push(full);
  }
  return out;
}

const actualRel = (await walk(root)).map(f => path.relative(root, f).replaceAll(path.sep, "/")).sort();
const actualSet = new Set(actualRel);
const input = await FileBlob.load(workbookPath);
const wb = await SpreadsheetFile.importXlsx(input);
const mainSheet = wb.worksheets.getItem("Ji_Draft_index");
const oldSheet = wb.worksheets.getItem("이전_매핑");
const mainValues = mainSheet.getRange("A1:J200").values;
const oldValues = oldSheet.getRange("A1:H200").values;

const currentLessonKeys = new Set();
const missingMainRows = [];
for (let i = 1; i < mainValues.length; i++) {
  const row = mainValues[i];
  const rel = row[7];
  if (!rel) continue;
  const relNorm = String(rel).replaceAll("\\", "/");
  const exists = actualSet.has(relNorm);
  const excelRow = i + 1;
  if (exists) {
    currentLessonKeys.add(`${row[1]}|${row[2]}`);
  } else {
    missingMainRows.push({ excelRow, level: row[1], lesson: row[2], rel: relNorm });
  }
}

// Make the current mapping sheet describe the actual raw folder.
for (const row of missingMainRows) {
  mainSheet.getRange(`I${row.excelRow}`).values = [["raw_deleted"]];
  mainSheet.getRange(`J${row.excelRow}`).values = [["현재 01_raw의 01_Ji_draft 파일이 없음. Ji가 직접 삭제한 상태로 확인됨."]];
}

// Recompute every Draft 보유여부 value from the current raw-backed lesson keys.
let oldChanged = 0;
for (let i = 1; i < oldValues.length; i++) {
  const row = oldValues[i];
  if (!row[0] || row[1] === null || row[5] === null || row[5] === "") continue;
  const key = `${row[0]}|${row[1]}`;
  const expected = currentLessonKeys.has(key) ? "O" : "X";
  if (String(row[5]) !== expected) {
    oldSheet.getRange(`F${i + 1}`).values = [[expected]];
    oldChanged++;
  }
}

wb.recalculate();
const mainCheck = await wb.inspect({ kind: "table", sheetId: "Ji_Draft_index", range: "A60:J74", include: "values,formulas", tableMaxRows: 20, tableMaxCols: 10, maxChars: 8000 });
const oldCheck = await wb.inspect({ kind: "table", sheetId: "이전_매핑", range: "A85:H112", include: "values,formulas", tableMaxRows: 35, tableMaxCols: 8, maxChars: 6000 });
console.log(mainCheck.ndjson);
console.log(oldCheck.ndjson);
console.log(JSON.stringify({actualJiDraftFiles: actualRel.length, missingMainRows, oldChanged}, null, 2));
const errors = await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 300 }, summary: "final formula error scan" });
console.log(errors.ndjson);

const outDir = "C:/vault/koreanwithji_vault/.codex_spreadsheet_work";
for (const name of ["Ji_Draft_index", "이전_매핑"]) {
  const img = await wb.render({ sheetName: name, autoCrop: "all", scale: 1, format: "png" });
  await fs.writeFile(`${outDir}/${name}_after.png`, new Uint8Array(await img.arrayBuffer()));
}
const output = await SpreadsheetFile.exportXlsx(wb);
await output.save(workbookPath);
console.log(`saved ${workbookPath}`);

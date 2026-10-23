import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "file:///C:/Users/Jigyo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const inputPath = "C:/vault/koreanwithji_vault/02_product/02_course_creation/00_curriculum_and_index/01_Ji_Draft_review_report.xlsx";
const vaultRoot = "C:/vault/koreanwithji_vault";
const input = await FileBlob.load(inputPath);
const wb = await SpreadsheetFile.importXlsx(input);
const copySheet = wb.worksheets.getItem("복사 판정");
const copyRows = copySheet.getRange("A4:J20").values;

const review = {
  "1-19": ["우선참고", "앞에서 배우지 않은 부분을 짚고, 이번 주제와 미학습 내용의 범위를 안내한다. 전체 Draft는 복사·발췌 판정이지만 Intro 구조는 참고 가치가 가장 높다."],
  "1-8": ["보조참고", "인사 뒤 학습자의 부담을 낮추고 한국어 irregular verbs의 규칙성을 기대하게 한다. 다만 명시적 Intro heading과 흐름 안내는 약하다."],
  "2-6": ["우선참고", "영어식 ‘to need’와 한국어 표현 차이에서 출발해 문제와 해결 구조로 연결한다. 부분 복사 의심이지만 도입부는 직접 작성 참고가 가능하다."],
  "2-9": ["보조참고", "이번 주제만 한 문장으로 안내하고 바로 첫 문법으로 들어간다. 최소한의 topic announcement 참고용이다."],
  "3-10": ["보조참고", "영어 예문을 잘못 옮기는 문제를 보여준 뒤 recipient particle의 필요성으로 연결한다. 문제 중심 도입의 보조 사례다."],
  "3-11": ["제외", "현재 Ji_draft 파일이 삭제 상태라 Intro 내용을 검토할 수 없다."],
  "3-12": ["제외", "현재 Ji_draft 파일이 삭제 상태라 Intro 내용을 검토할 수 없다."],
  "3-14": ["제외", "현재 Ji_draft 파일이 삭제 상태라 Intro 내용을 검토할 수 없다."],
  "4-2": ["우선참고", "표현의 목적, 핵심 형태, action verb 적용 범위를 순서대로 안내한다."],
  "4-8": ["우선참고", "대주제, 이번 레슨의 기본 범위, 뒤로 넘길 내용, 첫 형태까지 안내한다. roadmap형 Intro로 가장 유용하다."],
  "5-12": ["제외", "Intro 없이 바로 ‘or’ 관련 문법 설명으로 시작한다."],
  "6-12": ["제외", "Ji의 코스 Intro가 아니라 Amira 1:1 Session transcript가 포함된 자료다."],
  "6-1": ["보조참고", "modifier 개념을 예시로 바로 설명하지만 인사·범위·문제 상황 안내가 없다. 개념을 여는 보조 사례다."],
  "6-4": ["제외", "것 같다 개념을 바로 설명하는 소주제 도입이다. 레슨 전체 Intro 구조로는 약하다."],
  "7-2": ["우선참고", "영어 ‘but’의 표현 선택 문제와 기본 2개 범위를 안내한 뒤 첫 문법으로 들어간다."],
  "7-5": ["제외", "Intro 없이 바로 ‘~지만 VS ~데’ 비교로 시작한다."],
  "7-9": ["제외", "May/Must를 배우기 전 되다 선수 개념 설명으로 시작한다. 레슨 전체 Intro 참고로는 부적합하다."]
};

function pct(v) {
  if (typeof v === "number") return v;
  const n = Number(String(v ?? "").replace("%", "").trim());
  return Number.isFinite(n) ? n / 100 : null;
}
function escFormulaText(s) { return String(s).replaceAll('"', '""'); }
function toAbs(rel) { return path.join(vaultRoot, String(rel).replaceAll("/", path.sep)); }

let sheet;
try { sheet = wb.worksheets.getItem("intro"); }
catch { sheet = wb.worksheets.add("intro"); }

// Keep the new sheet deterministic if this builder is rerun.
const old = sheet.getUsedRange();
if (old) old.clear({ applyTo: "all" });

sheet.showGridLines = false;
sheet.getRange("A1").values = [["Ji_Draft Intro 참고 판정"]];
sheet.getRange("A2").values = [["복사 판정 대상의 첫 도입부를 `04_대사.md` 기준으로 검토. 삭제 상태 파일은 하이퍼링크를 만들지 않고 사유에 표시."]];
sheet.getRange("A3:F3").values = [["레벨-레슨", "레슨 타이틀", "인트로 참고", "사유", "문단 단어 일치율", "최장 연속 일치율"]];

const outputRows = [];
const linkRows = [];
for (let i = 0; i < copyRows.length; i++) {
  const row = copyRows[i];
  const level = String(row[1]);
  const lesson = String(row[2]);
  const title = String(row[3]);
  const key = `${level}-${lesson}`;
  const [grade, reason] = review[key] ?? ["제외", "Intro 검토 대상 분류 정보가 없어 제외 처리했다."];
  const relPath = String(row[8] ?? "");
  const absPath = toAbs(relPath);
  let exists = true;
  try { await fs.access(absPath); } catch { exists = false; }
  const finalReason = exists ? reason : `${reason} 현재 파일 경로: ${relPath}`;
  outputRows.push([`${level} | ${lesson}`, title, grade, finalReason, pct(row[5]), pct(row[6])]);
  if (exists) linkRows.push({ row: 4 + i, title, absPath });
}
sheet.getRange(`A4:F${3 + outputRows.length}`).values = outputRows;
for (const item of linkRows) {
  const address = item.absPath.replaceAll("\\", "/");
  sheet.getRange(`B${item.row}`).formulas = [[`=HYPERLINK("${escFormulaText(address)}","${escFormulaText(item.title)}")`]];
}

const table = sheet.tables.add(`A3:F${3 + outputRows.length}`, true, "IntroReviewTable");
table.style = "TableStyleMedium2";
table.showBandedRows = true;

sheet.getRange("A1:F20").format.font = { name: "Arial", size: 10, color: "#1F2937" };
sheet.getRange("A1").format.font = { name: "Arial", size: 14, bold: true, color: "#1F2937" };
sheet.getRange("A2").format.font = { name: "Arial", size: 9, italic: true, color: "#666666" };
sheet.getRange("A3:F3").format = {
  fill: "#1F4E78",
  font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" },
  horizontalAlignment: "center",
  verticalAlignment: "center",
};
sheet.getRange(`A4:F${3 + outputRows.length}`).format.verticalAlignment = "center";
sheet.getRange(`B4:B${3 + outputRows.length}`).format.wrapText = true;
sheet.getRange(`D4:D${3 + outputRows.length}`).format.wrapText = true;
sheet.getRange(`E4:F${3 + outputRows.length}`).format.numberFormat = "0.0%";
sheet.getRange(`A4:A${3 + outputRows.length}`).format.horizontalAlignment = "center";
sheet.getRange(`C4:C${3 + outputRows.length}`).format.horizontalAlignment = "center";
sheet.getRange(`E4:F${3 + outputRows.length}`).format.horizontalAlignment = "center";
sheet.getRange("A1:F1").format.rowHeight = 24;
sheet.getRange("A3:F3").format.rowHeight = 30;
sheet.getRange(`A4:F${3 + outputRows.length}`).format.rowHeight = 46;
sheet.getRange("A1:A20").format.columnWidth = 12;
sheet.getRange("B1:B20").format.columnWidth = 43;
sheet.getRange("C1:C20").format.columnWidth = 12;
sheet.getRange("D1:D20").format.columnWidth = 72;
sheet.getRange("E1:F20").format.columnWidth = 18;

for (let i = 0; i < outputRows.length; i++) {
  const cell = sheet.getRange(`C${4 + i}`);
  const grade = outputRows[i][2];
  if (grade === "우선참고") cell.format.fill = "#E2F0D9";
  else if (grade === "보조참고") cell.format.fill = "#FFF2CC";
  else cell.format.fill = "#E7E6E6";
}

sheet.freezePanes.freezeRows(3);
wb.recalculate();

const inspect = await wb.inspect({ kind: "table", sheetId: "intro", range: `A1:F${3 + outputRows.length}`, include: "values,formulas", tableMaxRows: 25, tableMaxCols: 6, maxChars: 12000 });
console.log(inspect.ndjson);
const errors = await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 300 }, summary: "final formula error scan" });
console.log(errors.ndjson);

const render = await wb.render({ sheetName: "intro", range: `A1:F${3 + outputRows.length}`, scale: 1, format: "png" });
await fs.writeFile("C:/vault/koreanwithji_vault/.codex_spreadsheet_work/intro.png", new Uint8Array(await render.arrayBuffer()));
const output = await SpreadsheetFile.exportXlsx(wb);
await output.save(inputPath);
console.log(`saved ${inputPath}`);

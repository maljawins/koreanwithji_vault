import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "file:///C:/Users/Jigyo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const inputPath = "C:/vault/koreanwithji_vault/02_product/02_course_creation/00_curriculum_and_index/Ji_draft_quality_check.xlsx";
const outputPath = "C:/vault/koreanwithji_vault/02_product/02_course_creation/00_curriculum_and_index/Ji_draft_quality_check_updated.xlsx";
const previewPath = "C:/vault/koreanwithji_vault/_tmp_update_draft_check.png";

const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(inputPath));
const sheet = workbook.worksheets.getItem("Sheet1");
const additions = [
  ["VSL", 1, "Video Sales Letter_The Korean Language Core", "01_Ji_draft", "Ji-VSL-1-2", "O"],
  ["Intro", 1, "How to use this course", "01_Ji_draft", "Ji-Intro-1-2", "O"],
  ["Intro", 2, "How to study vocabulary", "01_Ji_draft", "Ji-Intro-2-2", "O"],
  ["Intro", 2, "How to study vocabulary", "01_Ji_draft", "Ji-Intro-2-3", "O"],
];

sheet.getRange("A68:F71").copyFrom(sheet.getRange("A67:F67"), "all");
sheet.getRange("A68:F71").values = additions;
workbook.recalculate();

const check = await workbook.inspect({
  kind: "table",
  range: "A63:F71",
  include: "values,formulas",
  tableMaxRows: 12,
  tableMaxCols: 6,
});
console.log(check.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 100 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

const preview = await workbook.render({ sheetName: "Sheet1", range: "A1:F71", scale: 1, format: "png" });
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(`saved:${outputPath}`);

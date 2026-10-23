import { FileBlob, SpreadsheetFile } from "file:///C:/Users/Jigyo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";
const input = await FileBlob.load("C:/vault/koreanwithji_vault/02_product/02_course_creation/00_curriculum_and_index/01_Ji_Draft_review_report.xlsx");
const wb = await SpreadsheetFile.importXlsx(input);
const summary = await wb.inspect({kind:"workbook,sheet,table", maxChars:12000, tableMaxRows:8, tableMaxCols:12, tableMaxCellChars:120});
console.log(summary.ndjson);
for (const name of ["요약","파일 존재 대조","복사 판정","비교 불가"]){
  try { const sh=wb.worksheets.getItem(name); const used=sh.getUsedRange(); console.log("SHEET",name, used?.address); }
  catch(e){ console.log("NO",name,String(e)); }
}


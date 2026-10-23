import { FileBlob, SpreadsheetFile } from "file:///C:/Users/Jigyo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";
const p="C:/vault/koreanwithji_vault/02_product/02_course_creation/00_curriculum_and_index/01_Ji_Draft_index.xlsx"; const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(p));
console.log((await wb.inspect({kind:"workbook,sheet,table",maxChars:12000,tableMaxRows:10,tableMaxCols:12,tableMaxCellChars:140})).ndjson);

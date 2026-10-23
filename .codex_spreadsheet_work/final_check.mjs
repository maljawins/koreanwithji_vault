import { FileBlob, SpreadsheetFile } from "file:///C:/Users/Jigyo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";
const p="C:/vault/koreanwithji_vault/02_product/02_course_creation/00_curriculum_and_index/01_Ji_Draft_review_report.xlsx"; const input=await FileBlob.load(p); const wb=await SpreadsheetFile.importXlsx(input);
console.log((await wb.inspect({kind:"sheet",include:"id,name"})).ndjson);
console.log((await wb.inspect({kind:"table",sheetId:"intro",range:"A3:F20",include:"values,formulas",tableMaxRows:20,tableMaxCols:6,maxChars:5000})).ndjson);
console.log((await wb.inspect({kind:"match",searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",options:{useRegex:true,maxResults:300},summary:"final formula error scan"})).ndjson);

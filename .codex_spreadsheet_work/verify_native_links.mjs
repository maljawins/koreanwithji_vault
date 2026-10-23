import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "file:///C:/Users/Jigyo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";
const p="C:/vault/koreanwithji_vault/02_product/02_course_creation/00_curriculum_and_index/01_Ji_Draft_review_report.xlsx"; const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(p)); const sh=wb.worksheets.getItem("intro");
console.log((await wb.inspect({kind:"table",sheetId:"intro",range:"A3:F20",include:"values,formulas",tableMaxRows:20,tableMaxCols:6,maxChars:6000})).ndjson);
console.log((await wb.inspect({kind:"match",searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!|HYPERLINK is not implemented",options:{useRegex:true,maxResults:300},summary:"final formula error scan"})).ndjson);
const render=await wb.render({sheetName:"intro",range:"A1:F20",scale:1,format:"png"}); await fs.writeFile("C:/vault/koreanwithji_vault/.codex_spreadsheet_work/intro_final.png",new Uint8Array(await render.arrayBuffer()));

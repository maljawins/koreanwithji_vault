import { FileBlob, SpreadsheetFile } from "file:///C:/Users/Jigyo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";
const input=await FileBlob.load("C:/vault/koreanwithji_vault/02_product/02_course_creation/00_curriculum_and_index/01_Ji_Draft_review_report.xlsx"); const wb=await SpreadsheetFile.importXlsx(input);
for(const s of wb.worksheets.items){ console.log(s.name, s.tables.items.map(t=>({name:t.name,style:t.style,showHeaders:t.showHeaders,showBandedRows:t.showBandedRows}))); }

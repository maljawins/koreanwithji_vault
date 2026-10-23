import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "file:///C:/Users/Jigyo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";
const p="C:/vault/koreanwithji_vault/02_product/02_course_creation/00_curriculum_and_index/01_Ji_Draft_index.xlsx"; const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(p)); const out="C:/vault/koreanwithji_vault/.codex_spreadsheet_work";
for(const name of ["Ji_Draft_index","이전_매핑"]){const img=await wb.render({sheetName:name,autoCrop:"all",scale:1,format:"png"}); await fs.writeFile(`${out}/${name}_before.png`,new Uint8Array(await img.arrayBuffer()));}
console.log("rendered");

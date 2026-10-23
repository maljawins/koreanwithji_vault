import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "file:///C:/Users/Jigyo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";
const input = await FileBlob.load("C:/vault/koreanwithji_vault/02_product/02_course_creation/00_curriculum_and_index/01_Ji_Draft_review_report.xlsx");
const wb = await SpreadsheetFile.importXlsx(input);
const out="C:/vault/koreanwithji_vault/.codex_spreadsheet_work";
for (const name of ["요약","복사 판정"]){ const p=await wb.render({sheetName:name,autoCrop:"all",scale:1,format:"png"}); await fs.writeFile(`${out}/${name}.png`, new Uint8Array(await p.arrayBuffer())); }
console.log("rendered");

import fs from "node:fs/promises";
import { Workbook, SpreadsheetFile } from "file:///C:/Users/Jigyo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";
for (const [label,prop,val] of [["a","hyperlink",{address:"C:/vault/test.md",textToDisplay:"Title"}],["b","hyperlink",{address:"C:/vault/test.md"}],["c","link",{address:"C:/vault/test.md",text:"Title"}]]) {
 const wb=Workbook.create(); const sh=wb.worksheets.add("Test"); sh.getRange("A1").values=[["Title"]]; sh.getRange("A1")[prop]=val; const out=await SpreadsheetFile.exportXlsx(wb); await out.save(`C:/vault/koreanwithji_vault/.codex_spreadsheet_work/hyper_${label}.xlsx`);
}

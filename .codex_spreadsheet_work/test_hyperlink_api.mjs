import { Workbook, SpreadsheetFile } from "file:///C:/Users/Jigyo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";
const wb=Workbook.create(); const sh=wb.worksheets.add("Test"); sh.getRange("A1").values=[["Title"]];
const attempts=[];
for (const [name,val] of [["hyperlink",{address:"C:/vault/test.md",textToDisplay:"Title"}],["hyperlink2",{address:"C:/vault/test.md"}],["link",{address:"C:/vault/test.md",text:"Title"}]]) {
  try { sh.getRange("A1")[name==='hyperlink2'?'hyperlink':name]=val; attempts.push([name,"ok"]); } catch(e){ attempts.push([name,String(e)]); }
}
console.log(attempts);
console.log((await wb.inspect({kind:"table",sheetId:"Test",range:"A1:A1",include:"values,formulas",maxChars:2000})).ndjson);

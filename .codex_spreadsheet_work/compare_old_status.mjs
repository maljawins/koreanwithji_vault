import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "file:///C:/Users/Jigyo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";
const p="C:/vault/koreanwithji_vault/02_product/02_course_creation/00_curriculum_and_index/01_Ji_Draft_index.xlsx"; const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(p));
const main=wb.worksheets.getItem("Ji_Draft_index").getRange("A1:J74").values;
const old=wb.worksheets.getItem("이전_매핑").getRange("A1:H200").values;
const root="C:/vault/koreanwithji_vault/02_product/01_raw/01_by_level_lesson";
const actual={};
for(let i=1;i<main.length;i++){const row=main[i]; const key=`${row[1]}|${row[2]}`; const rel=row[7]; let exists=false; if(rel){try{await fs.access(path.join(root,String(rel).replaceAll("/",path.sep))); exists=true;}catch{}} if(!actual[key]) actual[key]={count:0,title:row[3]}; if(exists) actual[key].count++;}
const mism=[]; for(let i=1;i<old.length;i++){const row=old[i]; if(!row[0]||row[1]===null||row[5]===null||row[5]==='') continue; const key=`${row[0]}|${row[1]}`; const a=actual[key]?.count??0; const expected=a>0?'O':'X'; if(String(row[5])!==expected) mism.push({row:i+1,key,title:row[2],ref:row[4],old:row[5],expected,actualCount:a});}
console.log(JSON.stringify({actualKeys:Object.keys(actual).length,mismatches:mism},null,2));

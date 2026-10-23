import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "file:///C:/Users/Jigyo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";
const p="C:/vault/koreanwithji_vault/02_product/02_course_creation/00_curriculum_and_index/01_Ji_Draft_index.xlsx"; const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(p));
const main=wb.worksheets.getItem("Ji_Draft_index").getRange("A1:J74").values;
const old=wb.worksheets.getItem("이전_매핑").getRange("A1:H200").values;
const root="C:/vault/koreanwithji_vault/02_product/01_raw/01_by_level_lesson";
const missingMain=[]; for(let i=1;i<main.length;i++){const rel=main[i][7]; if(rel){try{await fs.access(path.join(root,String(rel).replaceAll("/",path.sep)))}catch{missingMain.push({row:i+1,ref:main[i][0],level:main[i][1],lesson:main[i][2],path:rel,status:main[i][8]})}}}
const counts={}; for(let i=1;i<old.length;i++){const v=String(old[i][5]??""); if(v) counts[v]=(counts[v]||0)+1;}
const oldMissing=[]; for(let i=1;i<old.length;i++){const rel=old[i][7]; if(String(old[i][5])==="O"&&rel){try{await fs.access(path.join(root,String(rel).replaceAll("/",path.sep)))}catch{oldMissing.push({row:i+1,level:old[i][0],lesson:old[i][1],title:old[i][2],ref:old[i][4],path:rel})}}}
console.log(JSON.stringify({mainRows:main.length-1,mainMissing:missingMain,oldCounts:counts,oldMissing},null,2));

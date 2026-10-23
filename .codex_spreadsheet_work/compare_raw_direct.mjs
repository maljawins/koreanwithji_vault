import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "file:///C:/Users/Jigyo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";
const root="C:/vault/koreanwithji_vault/02_product/01_raw/01_by_level_lesson";
const p="C:/vault/koreanwithji_vault/02_product/02_course_creation/00_curriculum_and_index/01_Ji_Draft_index.xlsx";
async function walk(dir){const out=[]; for(const e of await fs.readdir(dir,{withFileTypes:true})){const full=path.join(dir,e.name); if(e.isDirectory()) out.push(...await walk(full)); else if(e.isFile() && e.name.toLowerCase().endsWith('.md') && full.split(path.sep).includes('01_Ji_draft')) out.push(full);} return out;}
const actual=(await walk(root)).map(x=>path.relative(root,x).replaceAll(path.sep,'/')).sort();
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(p)); const main=wb.worksheets.getItem('Ji_Draft_index').getRange('A1:J200').values; const indexed=main.slice(1).filter(r=>r[7]).map(r=>String(r[7]).replaceAll('\\','/')).sort();
const actualSet=new Set(actual), indexedSet=new Set(indexed);
console.log(JSON.stringify({actualCount:actual.length,indexedCount:indexed.length,actualNotIndexed:actual.filter(x=>!indexedSet.has(x)),indexedNotActual:indexed.filter(x=>!actualSet.has(x))},null,2));

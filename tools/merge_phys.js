// 合併實體模式9人模擬並輸出各職業統計 JSON（供報告使用）
const fs=require('fs');
const files=process.argv.slice(2,-1), out=process.argv[process.argv.length-1];
const r=files.flatMap(f=>require(require('path').resolve(f)));
fs.writeFileSync(out,JSON.stringify(r));
console.log('merged games',r.length);

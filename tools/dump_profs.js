const {JSDOM,VirtualConsole}=require("jsdom");const fs=require("fs");
const dom=new JSDOM(fs.readFileSync("../index.html","utf8"),{runScripts:"dangerously",url:"http://localhost/",virtualConsole:new VirtualConsole()});
const w=dom.window;
console.log(w.eval("JSON.stringify(Object.keys(PROFESSIONS).filter(id=>!SANGUO_PROFS.has(id)).map(id=>({id,name:PROFESSIONS[id].name,icon:PROFESSIONS[id].icon,skills:PROFESSIONS[id].skills})))"));

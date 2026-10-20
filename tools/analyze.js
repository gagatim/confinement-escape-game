// 用法：node analyze.js <對局紀錄.json>  依存活輪數／z 值統計各職業
const recs=require(process.argv[2]||"./sim_700games.json");
const by={}; const allS=[];
recs.forEach(g=>g.players.forEach(p=>{
  const s=by[p.name]||(by[p.name]={n:p.name,g:0,sv:[],alive:0,hp:0,kills:0,dealt:0,taken:0,win:0,first:0});
  const sc=p.alive?7:(p.deathRound||1); s.sv.push(sc); allS.push(sc);
  s.g++; if(p.alive){s.alive++;s.hp+=p.hp;} s.kills+=p.kills; s.dealt+=p.dealt; s.taken+=p.taken; if(p.rank===1)s.win++;
}));
const mean=a=>a.reduce((x,y)=>x+y,0)/a.length;
const sd=a=>{const m=mean(a);return Math.sqrt(a.reduce((x,y)=>x+(y-m)**2,0)/(a.length-1));};
const gm=mean(allS), gsd=sd(allS);
const rows=Object.values(by).map(s=>{const m=mean(s.sv),se=gsd/Math.sqrt(s.g);return {...s,m,z:(m-gm)/se};}).sort((a,b)=>b.m-a.m);
const survRate=recs.reduce((x,g)=>x+g.players.filter(p=>p.alive).length,0)/(recs.length*8);
console.log(`局數 ${recs.length}｜全體平均存活輪數 ${gm.toFixed(2)}（標準差 ${gsd.toFixed(2)}）｜存活率 ${(survRate*100).toFixed(1)}%`);
console.log("職業|場|存活輪數|z|存活率|平均勝率(名次1)|場均擊殺|場均輸出|場均承傷");
rows.forEach(s=>console.log([s.n,s.g,s.m.toFixed(2),s.z.toFixed(1),(s.alive/s.g*100).toFixed(0)+"%",(s.win/s.g*100).toFixed(0)+"%",(s.kills/s.g).toFixed(2),(s.dealt/s.g).toFixed(1),(s.taken/s.g).toFixed(1)].join("|")));

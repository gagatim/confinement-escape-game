const fs=require("fs");
const load=fs.existsSync.bind(fs);
const files=process.argv.slice(2);
const games=files.flatMap(f=>JSON.parse(fs.readFileSync(f)));
const by={};
games.forEach(g=>g.players.forEach(p=>{const b=by[p.name]??={n:0,alive:0,rank:0,kills:0,dealt:0};b.n++;b.alive+=p.alive?1:0;b.rank+=p.rank;b.kills+=p.kills;b.dealt+=p.dealt}));
const tot=Object.values(by).reduce((a,b)=>a+b.n,0), avgRank=Object.values(by).reduce((a,b)=>a+b.rank,0)/tot, avgAlive=Object.values(by).reduce((a,b)=>a+b.alive,0)/tot;
console.log("games",games.length,"全體平均名次",avgRank.toFixed(2),"存活率",(avgAlive*100).toFixed(1)+"%");
Object.entries(by).sort((a,b)=>a[1].rank/a[1].n-b[1].rank/b[1].n).forEach(([k,b])=>console.log(k.padEnd(8),"n",String(b.n).padStart(3),"平均名次",(b.rank/b.n).toFixed(2),"存活",(b.alive/b.n*100).toFixed(0).padStart(2)+"%","殺",(b.kills/b.n).toFixed(2)));

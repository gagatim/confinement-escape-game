// 用法：node sim.js <局數> <輸出檔.json>   （需先 npm install jsdom）
// 注意：跑很多局時速度會越來越慢（記憶體累積），建議每次 150~250 局，分批跑再合併。
// 無畫面對戰模擬：用 jsdom 載入 index.html，把「你」也改成 AI，整局自動打完。
const {JSDOM,VirtualConsole}=require("jsdom");
const fs=require("fs");
const path=require("path");
const HTML=fs.readFileSync(path.resolve(__dirname,"../index.html"),"utf8");
const N=+process.argv[2]||20;
const OUT=process.argv[3]||"sim_result.json";
const MODE=process.argv[4]||"all"; // all = 一般+擴充職業

function runOne(seedNo){
  const errors=[];
  const vc=new VirtualConsole();
  vc.on("jsdomError",e=>errors.push(String(e.message||e).slice(0,200)));
  const dom=new JSDOM(HTML,{runScripts:"dangerously",url:"http://localhost/",pretendToBeVisual:true,virtualConsole:vc});
  const w=dom.window;
  try{
    const ev=s=>w.eval(s);
    const rnd=(a,b)=>a+Math.floor(Math.random()*(b-a+1));
    ev("expansionMode=true; physicalMode=true; syncPlayerRange();");
    const pool=JSON.parse(ev("JSON.stringify([...PHYSICAL_PROFS])"));
    const prof=process.env.FORCE_PROF||pool[rnd(0,pool.length-1)]; // FORCE_PROF=detective 可固定「你」的職業
    const pw=Math.min(rnd(2,6),(prof==='smuggler'||prof==='geneFreak')?5:99), sp=Math.min(rnd(1,4),10-pw-1), cr=10-pw-sp;
    ev(`selectedProf=${JSON.stringify(prof)};`);
    w.document.getElementById("playerCount").value=String(+process.env.PLAYERS||rnd(8,12));
    w.document.getElementById("allocPower").value=String(pw);
    w.document.getElementById("allocSpeed").value=String(sp);
    w.document.getElementById("allocCarry").value=String(cr);
    ev("startGame();");
    ev(`(function(){
      const me=STATE.players[0]; me.isAI=true;
      if(me.prof==="boss"){ applyBossHenchmen(me, shuffleArr(STATE.players.filter(x=>x.id!==me.id)).slice(0,3).map(x=>x.id)); }
      me.spawnRoom=chooseAISpawn(me);
      spawnSettlement();
      beginRound();   // 全員皆為 AI：beginRound -> advanceTurn -> settleRound 會自動往下
    })();`);
    // settleRound 結束後會停在回合摘要；手動往下一輪推進，直到遊戲結束
    for(let guard=0; guard<12 && !ev("STATE.gameOver"); guard++){
      ev("STATE.pendingEmbalmerChoice=null; advanceAfterRoundSummary();");
    }
    if(!ev("STATE.gameOver")) return {ok:false,error:"遊戲未結束",errors};
    const recs=JSON.parse(ev("JSON.stringify(loadGameRecords())"));
    return {ok:true,rec:recs[recs.length-1],errors};
  }catch(e){
    return {ok:false,error:String(e&&e.stack||e).split("\n").slice(0,4).join(" | "),errors};
  }finally{ w.close(); }
}

const results=[]; let fail=0; const t0=Date.now();
for(let i=0;i<N;i++){
  const tg=Date.now(); const r=runOne(i);
  if(i%10===0||Date.now()-tg>3000) console.log("game",i,"took",Date.now()-tg,"ms; total",((Date.now()-t0)/1000).toFixed(0),"s");
  if(r.ok) results.push(r.rec); else { fail++; console.log("FAIL",i,r.error); }
  if(i%25===24) fs.writeFileSync(OUT,JSON.stringify(results));
  if(r.errors.length) console.log("jsdomErrors",i,r.errors.slice(0,2));
}
fs.writeFileSync(OUT,JSON.stringify(results));
console.log(`done ${results.length}/${N} ok, ${fail} failed, ${((Date.now()-t0)/1000).toFixed(1)}s`);

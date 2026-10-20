# 禁閉逃殺

單檔網頁遊戲（`index.html`，約 9000 行／713KB）：桌遊改編，玩家 vs AI。介面與註解以繁體中文為主。
`index.html` 是唯一的遊戲檔，**必須保持單檔**（可離線 file:// 開啟；`tools/sim*.js` 用 jsdom 只讀這個檔）。

## 工作規則

- 官方職業（馴獸師等）不做平衡調整，只動自製職業。
- 不要跑大批模擬（使用者電腦會 LAG）；驗證用小測試，不要上百場。
- 沒有自動測試。改完至少做語法檢查（取出 `<script>` 內容丟給 `new Function`）。
- 不要整行讀取 `SFX_SAMPLES`（約第 1811 行，70KB base64 音效）；用 Grep 的 `-n` 搭配 `cut -c1-100`，或 Read 時避開那一行。
- 用 Grep 找函式，不要依賴行號（行號會隨編輯漂移）。下面以區段名稱為準。
- 技能說明文字（`desc`）、戰鬥紀錄文字、實作三處要一起改，三者不一致是常見 bug。

## index.html 結構

用 `/* ===== 名稱 ===== */` 分隔，可直接 Grep `^/\* =+` 列出區段：

| 區段 | 內容 |
|---|---|
| DATA: ITEMS / ROOMS | 道具表；房間、`ADJ` 相鄰表（靜態）、`bfsDist`（有快取）、`bfsPath`、暗影穿牆的 `GHOST_ADJ` |
| DATA: PROFESSIONS | `PROFESSIONS`：每個職業 `{name, skills:[{name, desc, passive}]}`；`fmtSkill` 負責顯示格式 |
| GAME STATE | `STATE` 全域狀態（`STATE.players[0]` 是玩家本人，`you()`） |
| SOUND EFFECTS / VOICE LINES | `SFX`（內嵌 base64 取樣＋合成備援）、技能台詞；`speakSkill`、`passiveFX` 在這附近 |
| GAME SETUP | `startGame`、職業分配、AI 出生點（`chooseAISpawn`） |
| ROUND FLOW | 每輪開始：`stepsLeft` 的各種加減（疾行、無聲離場、嗜殺等）、移動、`baseSpeed` |
| ROOM ACTIONS / ITEM USE / 神秘商店道具 | 玩家在房間內的動作、道具使用、地圖2商店 |
| PROFESSION SKILLS (human buttons) | 主動技能按鈕與實作 |
| VOTE / TRADE | 投票、交易 |
| AI | AI 決策（最大的一塊，約 700 行） |
| SETTLEMENT | `damagePlayer`、`killPlayer`、`settleRound`/`settleRoundCore`、`resolveCombat`、各職業結算被動 |
| RENDER | `renderAll` 與各面板重繪 |

## 關鍵慣例

- **傷害一律走 `damagePlayer(p, amount, cause, killerId)`**。只有戰鬥直擊（`resolveCombat` 的 1v1 命中）會帶 `killerId`；毒氣、火箭、飢餓等來源不帶，所以「造成傷害」類被動（屠夫、狂戰士嗜殺）只能由戰鬥觸發。
- 死亡走 `killPlayer`，擊殺類被動（刺客無聲離場、賞金獵人戰利品等）寫在它裡面。
- 「下回合生效」的效果：結算時設 `p.flags.xxxNext = true`，在 ROUND FLOW 分配 `stepsLeft` 時讀取並清除（例：刺客 `assassinSpeedNext`、狂戰士 `berserkSpeedNext`）。戰鬥發生在結算階段，移動已結束，所以步數類加成只能給下一輪。
- 職業有多個模式：一般／擴充／實體模式（`physicalToggle`）／三國模式（`sanguoToggle`、陣營戰）。改職業時確認是哪個模式的職業。
- 暗影（ghost）是死亡後的狀態，步數＝死前速度，可穿牆。

## tools/（模擬與報表，非遊戲本體）

- `sim.js`、`sim_physical.js`：jsdom 載入 `index.html`，全 AI 自動打完整局；`dump_profs.js` 匯出職業資料；`analyze*.js`、`build_*report.py` 產生分析報表。
- `generate_avatars.py`：從 `images/characters/` 等素材產生 `images/avatars/*.webp`（遊戲實際用的頭像）。
- `tools/node_modules`、`tools/sim_out` 是產物，不需讀取。

## 其他

- `images/avatars/` 是遊戲用到的圖。未使用的大圖已移到桌面 `禁閉逃殺_素材備份/`。
- `docs/規則與職業/`：職業與規則參考（`全部職業列表.txt`、`三國模式_技能總覽.txt`、`職業技能總覽.txt`、`地圖二功能.txt` 最新）；`docs/分析報告/`：平衡分析與設計文件（GDD）；`docs/舊版/`：舊版報告；`docs/素材/`：圖片與參考圖（含 `詳細地圖.jpg`）。
- `.gitignore` 已忽略 `node_modules`、`tools/sim_out/`、模擬 json 等產物。
- `lucky-wheel-app/`、`scavenger-skill-app/` 是無關的獨立小專案。

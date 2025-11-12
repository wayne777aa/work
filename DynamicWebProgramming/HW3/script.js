// ---- 遊戲狀態變數 ----
let deck = [];
let playerHand = [];
let dealerHand = [];
let playerPoints = 0;
let dealerPoints = 0;
let playerMoney = 1000;  // 初始金額
let bet = 0;
let isBetLocked = false;
let isCheated = false;

// ---- 初始化金額 ----
function loadMoneyFromLocalStorage() {
    const localData = JSON.parse(localStorage.getItem("blackjack_local") || '{"rounds":[]}');

    if (localData.rounds.length > 0) {
        // 取最後一局的 playerMoney
        const lastRound = localData.rounds[localData.rounds.length - 1];
        if (typeof lastRound.playerMoney === "number") {
            playerMoney = lastRound.playerMoney;
        }
    }

    updateMoneyDisplay();
}

// ---- 初始化撲克牌 ----
function createDeck() {
    const suits = ['♠', '♥', '♦', '♣'];
    const values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];
    deck = [];
    for (let s of suits) {
        for (let v of values) {
            deck.push({ value: v, suit: s });
        }
    }
}

// ---- 洗牌 ----
function shuffleDeck() {
    for (let i = deck.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [deck[i], deck[j]] = [deck[j], deck[i]];
    }
}

// ---- 抽牌 ----
function drawCard() {
    return deck.pop();
}

// ---- 下注 ----
function setBet() {
    if (isBetLocked) {
        showMessage("本局已下注，請先完成遊戲再下注。");
        return;
    }
    const betInput = document.getElementById("bet-input");
    const betValue = parseInt(betInput.value);

    if (isNaN(betValue) || betValue <= 0) {
        showMessage("請輸入正確的下注金額。");
        return;
    }

    if (betValue > playerMoney) {
        showMessage("金額不足。");
        return;
    }

    bet = betValue;
    playerMoney -= betValue;  // 扣除下注金額
    document.getElementById("bet-btn").disabled = true;
    document.getElementById("deal-btn").disabled = false;
    isBetLocked = true;
    updateMoneyDisplay();
    showMessage(`你下注了 ${bet}！按「發牌」開始。`);
}

function updateMoneyDisplay() {
    document.getElementById("money-display").innerText = `💰 餘額：${playerMoney}`;
}

// ---- 計算點數 ----
function calculatePoints(hand) {
    let total = 0;
    let aces = 0; // A 的數量
    for (let card of hand) {
        if (['J', 'Q', 'K'].includes(card.value)) 
            total += 10;
        else if (card.value === 'A') {
            total += 11;
            aces += 1;
        } else total += parseInt(card.value);
    }
    // 調整 A 的值（如果超過 21，就把 A 當 1）
    while (total > 21 && aces > 0) {
        total -= 10;
        aces--;
    }
    return total;
}

// ---- 遊戲開始 ----
function deal() {
    if (!isBetLocked) {
        showMessage("本局還未下注，請先下注再遊玩。");
        return;
    }
    document.getElementById("hit-btn").disabled = false;
    document.getElementById("stand-btn").disabled = false;
    document.getElementById("deal-btn").disabled = true;

    createDeck();
    shuffleDeck();

    if (isCheated) {
        cheatMoveAand10ToTop();
    }

    dealerHand = [drawCard(), drawCard()];
    playerHand = [drawCard(), drawCard()];

    updatePoints(false);
    renderHands(false); // false 表示莊家有一張是蓋住的
}

// ---- 要牌 ----
async function hit() {
    playerHand.push(drawCard());
    updatePoints(false);
    renderHands(false);
    // 延遲 0.5 秒，避免還沒更新就顯示訊息
    await new Promise(r => setTimeout(r, 300)); 

    if (playerPoints > 21) {
        renderHands(true);
        updatePoints(true);
        showMessage("你爆了！莊家勝利。");
        saveGameResult();
        isBetLocked = false;
        document.getElementById("bet-btn").disabled = false;
        document.getElementById("deal-btn").disabled = true;
        document.getElementById("hit-btn").disabled = true;
        document.getElementById("stand-btn").disabled = true;
    }
}

// ---- 停牌 ----
async function stand() {
    // 莊家補牌直到 >= 17
    renderHands(true);
    updatePoints(true);
    while (dealerPoints < 17) {
        dealerHand.push(drawCard());
        renderHands(true);
        updatePoints(true);
        await new Promise(r => setTimeout(r, 300)); // 延遲 0.5 秒
    }

    checkWinner();
}

function updatePoints(showDealerAll) {
    playerPoints = calculatePoints(playerHand);
    document.getElementById("player-points").innerText = "點數：" + playerPoints;

    if (showDealerAll) {
        // 翻牌後才算全部
        dealerPoints = calculatePoints(dealerHand);
    } else {
        // 只算第一張明牌
        dealerPoints = calculatePoints([dealerHand[0]]);
    }
    document.getElementById("dealer-points").innerText = "點數：" + dealerPoints;
}

function renderHands(showDealerAll) {
    const playerDiv = document.getElementById("player-cards");
    const dealerDiv = document.getElementById("dealer-cards");
    playerDiv.innerHTML = "";
    dealerDiv.innerHTML = "";

    // 顯示玩家手牌
    playerHand.forEach(card => {
        playerDiv.innerHTML += `<div class='card'>${card.value}${card.suit}</div>`;
    });

    // 顯示莊家手牌
    dealerHand.forEach((card, i) => {
        if (!showDealerAll && i === 1) {
            dealerDiv.innerHTML += `<div class='card hidden'>🂠</div>`;
        } else {
            dealerDiv.innerHTML += `<div class='card'>${card.value}${card.suit}</div>`;
        }
    });
}

function checkWinner() {
    let result = "";
    if (dealerPoints > 21) {
        result = '莊家爆了！你贏了！';
        playerMoney += bet * 2;
    }
    else if (playerPoints > 21) {
        result = '你爆了！莊家勝利。';
    }
    else if (playerPoints > dealerPoints) {
        result = '你贏了！';
        playerMoney += bet * 2;
    }
    else if (playerPoints < dealerPoints) {
        result = '莊家贏了！';
    }
    else {
        result = '平手。';
        playerMoney += bet; // 退錢
    }

    updateMoneyDisplay();
    showMessage(result);
    saveGameResult();

    isBetLocked = false;
    document.getElementById("bet-btn").disabled = false;
    document.getElementById("deal-btn").disabled = true;
    document.getElementById("hit-btn").disabled = true;
    document.getElementById("stand-btn").disabled = true;
}

function showMessage(text, callback = null) {
    const box = document.getElementById("message-box");
    const msg = document.getElementById("message-text");
    const btn = document.getElementById("message-ok");

    msg.textContent = text;
    box.classList.remove("hidden");

    // 點「確定」時隱藏訊息框
    btn.onclick = () => {
        box.classList.add("hidden");
        if (callback) callback();  // 若有 callback 就執行（可用來進入下一局）
    };
}

function saveGameResult() {
    const now = new Date();
    const timeStr = now.toLocaleString();

    // === LocalStorage ===
    const localData = JSON.parse(localStorage.getItem("blackjack_local") || '{"rounds":[]}'); // 用 || 避免沒資料
    const Round = localData.rounds.length + 1;

    localData.rounds.push({
        round: Round,
        playerPoints: playerPoints,
        dealerPoints: dealerPoints,
        playerMoney: playerMoney,  // 你可以自行定義初始值 1000 + 輸贏加減
        playTime: timeStr
    });

    localStorage.setItem("blackjack_local", JSON.stringify(localData));

    // === SessionStorage ===
    const sessionData = JSON.parse(sessionStorage.getItem("blackjack_session") || '{"rounds":[]}');
    sessionData.rounds.push({
        round: Round,
        playerCards: playerHand.map(c => `${c.value}${c.suit}`),
        dealerCards: dealerHand.map(c => `${c.value}${c.suit}`)
    });
    sessionStorage.setItem("blackjack_session", JSON.stringify(sessionData));
}

function showRecords() {
    const tableBody = document.querySelector("#record-table tbody");
    tableBody.innerHTML = ""; // 清空舊資料

    const localData = JSON.parse(localStorage.getItem("blackjack_local") || '{"rounds":[]}');

    const sessionData = JSON.parse(sessionStorage.getItem("blackjack_session") || '{"rounds":[]}');

    if (localData.rounds.length === 0 && sessionData.rounds.length === 0) {
        showMessage("目前沒有任何紀錄。");
        return;
    }

    localData.rounds.forEach(lr => {
        const sr = sessionData.rounds.find(s => s.round === lr.round);

        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${lr.round}</td>
            <td>${lr.playTime}</td>
            <td>${lr.playerPoints}</td>
            <td>${lr.dealerPoints}</td>
            <td>${lr.playerMoney ?? "-"}</td>
            <td>${sr ? sr.dealerCards.join(" ") : "-"}</td>
            <td>${sr ? sr.playerCards.join(" ") : "-"}</td>
        `;
        tableBody.appendChild(row);
    });

    showMessage("已載入紀錄！");
}

function cheatMoveAand10ToTop() {
    // 找出第一張 A 和第一張 10
    const aceIndex = deck.findIndex(c => c.value === 'A');
    const tenIndex = deck.findIndex(c => c.value === '10');

    if (aceIndex === -1 || tenIndex === -1) {
        showMessage("找不到 A 或 10，無法作弊。");
        return;
    }

    // 取出 A 和 10
    const aceCard = deck.splice(aceIndex, 1)[0];
    const tenCard = deck.splice(tenIndex > aceIndex ? tenIndex - 1 : tenIndex, 1)[0]; // 10 在 A 後面的話 index 會換

    // 把它們放到最上面（讓莊家拿到）
    if (Math.random() < 0.5) {
        // A 在前
        deck.push(aceCard);
        deck.push(tenCard);
    } else {
        // 10 在前
        deck.push(tenCard);
        deck.push(aceCard);
    }
}

function updateCheat(){
    const btn = document.getElementById("cheat-btn");
    if (isCheated) {
        isCheated = false;
        btn.classList.add("off");
        btn.classList.remove("on");
    } else {
        isCheated = true;
        btn.classList.add("on");
        btn.classList.remove("off");
    }
}

function resetGame() {
    localStorage.removeItem("blackjack_local");
    sessionStorage.removeItem("blackjack_session");
    playerHand = [];
    dealerHand = [];
    playerPoints = 0;
    dealerPoints = 0;
    playerMoney = 1000;
    isBetLocked = false;
    const btn = document.getElementById("cheat-btn");
    if(isCheated){
        isCheated = false;
        btn.classList.add("off");
        btn.classList.remove("on");
    }
    document.getElementById("player-cards").innerHTML = "";
    document.getElementById("dealer-cards").innerHTML = "";
    document.getElementById("player-points").innerText = "點數：0";
    document.getElementById("dealer-points").innerText = "點數：0";
    document.getElementById("money-display").innerText = `💰 餘額：${playerMoney}`;
    document.getElementById("bet-btn").disabled = false;
    document.getElementById("deal-btn").disabled = true;
    document.getElementById("hit-btn").disabled = true;
    document.getElementById("stand-btn").disabled = true;
    showMessage("已清除所有紀錄。");
    const tableBody = document.querySelector("#record-table tbody");
    tableBody.innerHTML = ""; // 清空舊資料
}

document.getElementById("deal-btn").addEventListener("click", deal);
document.getElementById("hit-btn").addEventListener("click", hit);
document.getElementById("stand-btn").addEventListener("click", stand);
document.getElementById("show-btn").addEventListener("click", showRecords);
document.getElementById("cheat-btn").addEventListener("click", updateCheat);
document.getElementById("reset-btn").addEventListener("click", resetGame);
document.getElementById("bet-btn").addEventListener("click", setBet);

window.addEventListener("DOMContentLoaded", () => {
    loadMoneyFromLocalStorage();
});
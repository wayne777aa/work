/* feature 1 */
// 點擊按鈕開啟 aboutme.html
window.addEventListener('DOMContentLoaded', () => {
    const toabout = document.getElementById('to_about');
    if (toabout) {
        toabout.addEventListener('click', () => {
            window.open('aboutme.html', '_blank');
        });
    }

    const togame = document.getElementById('to_game');
    if (togame) {
        togame.addEventListener('click', () => {
            window.open('game.html', '_blank');
        });
    }

    const toVTuber = document.getElementById('to_VTuber');
    if (toVTuber) {
        toVTuber.addEventListener('click', () => {
            window.open('vtuber.html', '_blank');
        });
    }
});

/* feature 2 */
// 頁面載入時自動彈出 autoPopup
window.addEventListener('load', () => {
    const autoPopup = document.getElementById('autoPopup');
    if (autoPopup) {
        autoPopup.classList.remove('hidden');
    }
});

// 手動點擊觸發 popup
const btn = document.getElementById('showPopupBtn');
if (btn) {
    btn.addEventListener('click', () => {
        const manualPopup = document.getElementById('manualPopup');
        if (manualPopup) {
            manualPopup.classList.remove('hidden');
        }
    });
}

// 關閉函式
function closePopup(id) {
    const popup = document.getElementById(id);
    if (popup) {
        popup.classList.add('hidden');
    }
}


/* feature 3 */
// 計時器功能
const timer = document.getElementById("timer");
const ad = document.getElementById("ad");
if (timer) {
    const startTime = performance.now();

    function formatTime(t) {
        let sec = t / 1000;
        let intPart = Math.floor(sec).toString().padStart(4, '0'); // 取整數部分，轉string，補零到4位
        let decimal = Math.floor((sec * 10) % 10);
        return `${intPart}.${decimal}s`;
    }

    setInterval(
        () => {
            let now = performance.now();
            timer.textContent = formatTime(now - startTime);
        }, 
        100
    ); // 每 0.1 秒更新

    setTimeout(
        () => {ad.classList.remove('hidden');}, 
        3000
    ); // 3 秒後出現廣告
}

/* feature 4 */
// 滾動偵測功能
function isInViewport(el) {
    const rect = el.getBoundingClientRect(); // 取得元素相對於視窗的位置
    return (
        window.innerHeight > rect.top && rect.bottom > 0 // 元素在視窗內
    );
}

function onScrollCheck() {
    document.querySelectorAll('.trigger_text').forEach(
        (el) => { // 選取所有目標元素，回傳陣列，逐一檢查
            if (isInViewport(el)) {
                el.classList.add('visible');
            } else {
                el.classList.remove('visible');
            }
        }
    );
}

// 初始與捲動時觸發檢查
window.addEventListener('scroll', onScrollCheck);
window.addEventListener('load', onScrollCheck);

/* feature 5 */
// 音樂播放控制
const ad_close = document.getElementById("ad_close");
if (ad_close) {
    ad_close.addEventListener("click", stopMusic);
    ad_close.addEventListener("click", () => closePopup('ad'));
}

function playMusic() {
    const audio = document.getElementById("hanafubuki");
    audio.volume = 0.1;
    audio.currentTime = 0;
    audio.play();
}

function stopMusic() {
    const audio = document.getElementById("hanafubuki");
    audio.pause();
}

function openYouTube() {
    window.open("https://youtu.be/aOcYn6YAO5E?si=l-E8rBJg7vWQT2fR", "_blank");
    closePopup('confirmpopup');
    document.body.classList.remove('noscroll');
}

const confirmbtn = document.getElementById('youtube_btn');
if (confirmbtn) {
    confirmbtn.addEventListener('click', () => {
        const confirmPopup = document.getElementById('confirmpopup');
        if (confirmPopup) {
            confirmPopup.classList.remove('hidden');
            document.body.classList.add('noscroll'); // 禁止背景滾動
        }
    });
}
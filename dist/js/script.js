// querySelector setting
function $$(element) {
  return document.querySelector(element);
}
function $$all(element) {
  return document.querySelectorAll(element);
}
// 移除第一次進入頁面的animated屬性
$$("#homePage").addEventListener("animationend", function () {
  $$("#homePage").classList.remove("animate__animated", "animate__fadeInDown");
});

// 顯示等待頁面
function showLoadingPage() {
  // homePage Out
  $$("#homePage").classList.add("d-none");
  // loadingPage In
  $$("#loadingPage").classList.remove("d-none");
  $$("#loadingPage").classList.add("animate__animated", "animate__zoomIn");
  $$("#loadingPage").addEventListener("animationend", function () {
    $$("#loadingPage").classList.remove(
      "animate__animated",
      "animate__zoomIn"
    );
  });
}
// 顯示結果頁面
function showResultPage() {
  // loadingPage Out
  $$("#loadingPage").classList.add("d-none");
  // resultPage In
  $$("#resultPage").classList.remove("d-none");
  $$("#resultPage").classList.add("animate__animated", "animate__zoomIn");
  $$("#resultPage").addEventListener("animationend", function () {
    $$("#resultPage").classList.remove("animate__animated", "animate__zoomIn");
  });
  loadRandomImage(); //顯示結果時立即刷新Loading頁面的gif
}
// 返回主畫面
function returnToHome() {
  $$("#resultPage").classList.add("d-none");
  $$("#homePage").classList.remove("d-none");
  $$("#homePage").classList.add("animate__animated", "animate__zoomIn");
  $$("#homePage").addEventListener("animationend", function () {
    $$("#homePage").classList.remove("animate__animated", "animate__zoomIn");
  });
}

// 切換Search模式
$$("#checkSearchByUser").onclick = function () {
  dataProcessor.statusSearchByUser = true;
  dataProcessor.statusSearchByGame = false;
};
$$("#checkSearchByGame").onclick = function () {
  dataProcessor.statusSearchByUser = false;
  dataProcessor.statusSearchByGame = true;
};

function shakeAlert(element) {
  element.classList.add("animate__animated", "animate__headShake");
  element.addEventListener("animationend", function () {
    element.classList.remove("animate__animated", "animate__headShake");
  });
}
// 開始分析前，較驗輸入資料
function checkSettingInput() {
  // 輸入為空則晃動提醒
  if ($$("#inputId").value === "") {
    shakeAlert($$("#inputIdGroup"));
    return false;
  }
  dataProcessor.inputId = parseInt($$("#inputId").value, 10);
  return true;
}

var imageLinks = [
  "https://cdn.discordapp.com/attachments/862518605433012268/1109140766024015934/Rick_Roll_Lossy.gif",
  // "https://cdn.discordapp.com/attachments/862518605433012268/1113317328193585182/4d10aff27de4f7a4260dd6528b556c8d.gif", //鳥鳥
];
// Loading畫面隨機選擇圖片撥放
function loadRandomImage() {
  var randomIndex = Math.floor(Math.random() * imageLinks.length);
  var randomImageLink = imageLinks[randomIndex];
  var imgElement = document.getElementById('loadingImage');
  var image = new Image();
  image.onload = function() {
    imgElement.src = randomImageLink;
  };
  image.src = randomImageLink;
}
window.onload = loadRandomImage;
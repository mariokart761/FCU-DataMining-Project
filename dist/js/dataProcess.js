class DataProcessor {
  constructor() {
    this._statusSearchByUser = true;
    this._statusSearchByGame = false;
    this._statusInputId = "";
  }

  get statusSearchByUser() {
    return this._statusSearchByUser;
  }
  set statusSearchByUser(newValue) {
    this._statusSearchByUser = newValue;
  }

  get statusSearchByGame() {
    return this._statusSearchByGame;
  }
  set statusSearchByGame(newValue) {
    this._statusSearchByGame = newValue;
  }

  get inputId() {
    return this._inputId;
  }
  set inputId(newValue) {
    this._inputId = newValue;
  }
}
const dataProcessor = new DataProcessor();

function build_carousel_data(
  gameHeaderImgUrl,
  recommendGameTitles,
  gameShopUrl
) {
  let carouselData = [];
  for (let i = 0; i < gameHeaderImgUrl.length; i++) {
    carouselData.push({
      imageUrl: gameHeaderImgUrl[i],
      title: recommendGameTitles[i],
      shopLink: gameShopUrl[i],
    });
  }

  // Get the carousel inner container
  const carouselInner = document.getElementById("carouselInner");

  // Generate carousel items using the data
  carouselData.forEach((item, index) => {
    const carouselItem = document.createElement("div");
    if (index === 0) {
      carouselItem.classList.add("carousel-item", "active");
    } else {
      carouselItem.classList.add("carousel-item");
    }

    const imgContainer = document.createElement("div");
    imgContainer.classList.add("result-img-container");
    imgContainer.innerHTML = `<img class="d-block w-100 result-img img-fluid" src="${item.imageUrl}" alt=""/>`;

    const textContainer = document.createElement("div");
    textContainer.classList.add("result-text-container");
    textContainer.innerHTML = `
      <div class="game-title-container">
        <h3 class="game-title">${item.title}</h3>
      </div>
      <div class="shop-link-container">
        <label class="shop-label">商店連結 :</label>
        <a href="${item.shopLink}" target="_blank" class="shop-link">${item.shopLink}</a>
      </div>
    `;

    carouselItem.appendChild(imgContainer);
    carouselItem.appendChild(textContainer);
    carouselInner.appendChild(carouselItem);
  });

  // Initialize the carousel after adding items
  const resultCarousel = new bootstrap.Carousel(document.getElementById("resultCarousel"), {
    interval: false, // Set to false to prevent auto sliding
  });
}

$(document).ready(function () {
  var originalContent = $("#resultCarousel").html(); // 儲存原始的(空的) Carousel 內容

  // 按下 returnButton 按鈕時恢復原狀
  $("#returnButton").click(function () {
    $("#resultCarousel").html(originalContent); // 還原 Carousel 內容
    $(".carousel-control-prev, .carousel-control-next").show(); // 顯示左右換頁按鈕
  });
});

document
  .getElementById("sendButton")
  .addEventListener("click", async function () {
    try {
      if (checkSettingInput() != true) return;

      // 顯示等待頁面
      showLoadingPage();

      if (dataProcessor.statusSearchByUser === true) {
        const formData = new FormData();
        formData.append("user_id", dataProcessor.inputId);
        const response = await axios.post("/api/sim_user_analyzer", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        var recommendGameIds = response.data.recommend_game_ids;
        var recommendGameTitles = response.data.recommend_game_names;
        let gameHeaderImgUrl = [];
        let gameShopUrl = [];
        for (let i = 0; i < recommendGameIds.length; i++) {
          gameHeaderImgUrl.push(
            `https://cdn.akamai.steamstatic.com/steam/apps/${recommendGameIds[i]}/header.jpg`
          );
          gameShopUrl.push(
            `https://store.steampowered.com/app/${recommendGameIds[i]}`
          );
        }
        build_carousel_data(gameHeaderImgUrl, recommendGameTitles, gameShopUrl);

        // 顯示結果頁面
        showResultPage();

      } else if (dataProcessor.statusSearchByGame === true) {
        const formData = new FormData();
        formData.append("game_id", dataProcessor.inputId);
        const response = await axios.post("/api/sim_game_analyzer", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });

        var recommendGameIds = response.data.sim_app_ids;
        var recommendGameTitles = response.data.sim_game_names;
        let gameHeaderImgUrl = [];
        let gameShopUrl = [];
        for (let i = 0; i < recommendGameIds.length; i++) {
          gameHeaderImgUrl.push(
            `https://cdn.akamai.steamstatic.com/steam/apps/${recommendGameIds[i]}/header.jpg`
          );
          gameShopUrl.push(
            `https://store.steampowered.com/app/${recommendGameIds[i]}`
          );
        }
        build_carousel_data(gameHeaderImgUrl, recommendGameTitles, gameShopUrl);

        // 顯示結果頁面
        showResultPage();
      }
    } catch (error) {
      console.error(error);
    }
  });

console.log("✅ app.js 読み込み開始");

let app = new PIXI.Application({
  width: 1200,
  height: 800,
  backgroundColor: 0x333333
});
document.body.appendChild(app.view);

let ws = new WebSocket("ws://localhost:8767");
ws.onopen = () => console.log("✅ WebSocket接続完了");
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  handleServerMessage(data);
};

// パーツ管理
let sprites = {
  body: null,
  swimsuit: null,
  clothes: null,
  rightArm: null,
  leftArm: null,
  edamame: null,
  mouth: null,
  eyeWhite: null,
  eyeBlack: null,
  eyebrow: null
};

let eyeTextures = {
  whiteOpen: null,
  blackOpen: null,
  closed: null
};

let mouthTextures = {
  closed: null,
  open1: null,
  open2: null
};

function handleServerMessage(data) {
  switch(data.action) {
    case "blink":
      console.log("👁️ まばたき実行");
      startBlinkAnimation();
      break;
    case "speak":
      console.log("💬 発話:", data.text);
      startMouthAnimation();
      break;
    case "monologue":
      console.log("💭 独り言:", data.text);
      startMouthAnimation();
      break;
  }
}

function startBlinkAnimation() {
  if (!sprites.eyeWhite || !sprites.eyeBlack || !eyeTextures.closed) return;
  
  // 目を閉じる
  sprites.eyeWhite.texture = eyeTextures.closed;
  sprites.eyeBlack.visible = false;
  
  setTimeout(() => {
    // 目を開く
    if (sprites.eyeWhite && eyeTextures.whiteOpen) {
      sprites.eyeWhite.texture = eyeTextures.whiteOpen;
    }
    if (sprites.eyeBlack) {
      sprites.eyeBlack.visible = true;
    }
  }, 150);
}

function startMouthAnimation() {
  if (!sprites.mouth || !mouthTextures.open1) return;
  
  // 口を開く
  sprites.mouth.texture = mouthTextures.open1;
  
  setTimeout(() => {
    if (sprites.mouth && mouthTextures.open2) {
      sprites.mouth.texture = mouthTextures.open2;
    }
  }, 100);
  
  setTimeout(() => {
    if (sprites.mouth && mouthTextures.closed) {
      sprites.mouth.texture = mouthTextures.closed;
    }
  }, 200);
}

// 全パーツ読み込み
app.loader
  .add("body", "/assets/zundamon_en/outfit2/body.png")
  .add("swimsuit", "/assets/zundamon_en/outfit2/swimsuit.png")
  .add("clothes", "/assets/zundamon_en/outfit1/usual_clothes.png")
  .add("rightArm", "/assets/zundamon_en/outfit1/right_arm/basic.png")
  .add("leftArm", "/assets/zundamon_en/outfit1/left_arm/basic.png")
  .add("edamame", "/assets/zundamon_en/edamame/edamame_normal.png")
  .add("mouthClosed", "/assets/zundamon_en/mouth/muhu.png")
  .add("mouthOpen1", "/assets/zundamon_en/mouth/hoa.png")
  .add("mouthOpen2", "/assets/zundamon_en/mouth/hoaー.png")
  .add("eyeWhiteOpen", "/assets/zundamon_en/eye/eye_set/normal_white_eye.png")
  .add("eyeBlackOpen", "/assets/zundamon_en/eye/eye_set/pupil/normal_eye.png")
  .add("eyeClosed", "/assets/zundamon_en/eye/sleepy_eye.png")
  .add("eyebrow", "/assets/zundamon_en/eyebrow/normal_eyebrow.png")
  .load((loader, resources) => {
    console.log("✅ 画像ロード完了");

    // テクスチャを保存
    eyeTextures.whiteOpen = resources.eyeWhiteOpen.texture;
    eyeTextures.blackOpen = resources.eyeBlackOpen.texture;
    eyeTextures.closed = resources.eyeClosed.texture;
    
    mouthTextures.closed = resources.mouthClosed.texture;
    mouthTextures.open1 = resources.mouthOpen1.texture;
    mouthTextures.open2 = resources.mouthOpen2.texture;

    // レイヤー順序で配置
    createSprite("body", resources.body);
    createSprite("swimsuit", resources.swimsuit);
    createSprite("clothes", resources.clothes);
    
    // 目は初期状態で開いた状態
    sprites.eyeWhite = new PIXI.Sprite(eyeTextures.whiteOpen);
    sprites.eyeWhite.x = 0;
    sprites.eyeWhite.y = 0;
    app.stage.addChild(sprites.eyeWhite);
    
    sprites.eyeBlack = new PIXI.Sprite(eyeTextures.blackOpen);
    sprites.eyeBlack.x = 0;
    sprites.eyeBlack.y = 0;
    app.stage.addChild(sprites.eyeBlack);
    
    createSprite("eyebrow", resources.eyebrow);
    
    // 口は初期状態で閉じた状態
    sprites.mouth = new PIXI.Sprite(mouthTextures.closed);
    sprites.mouth.x = 0;
    sprites.mouth.y = 0;
    app.stage.addChild(sprites.mouth);
    
    createSprite("rightArm", resources.rightArm);
    createSprite("leftArm", resources.leftArm);
    createSprite("edamame", resources.edamame);

    console.log("✅ ずんだもん完全表示（まばたき + 口パク対応）");
  });

function createSprite(name, resource) {
  if (resource && resource.texture) {
    sprites[name] = new PIXI.Sprite(resource.texture);
    sprites[name].x = 0;
    sprites[name].y = 0;
    app.stage.addChild(sprites[name]);
    console.log(`✅ ${name} パーツ追加完了`);
  } else {
    console.error(`❌ ${name} パーツの読み込み失敗`);
  }
}
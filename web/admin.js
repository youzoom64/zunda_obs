console.log("管理画面起動");

let app = new PIXI.Application({
  width: 600,
  height: 500,
  backgroundColor: 0x333333
});
document.getElementById('preview-container').appendChild(app.view);

let ws = new WebSocket("ws://localhost:8767");
ws.onopen = () => console.log("WebSocket接続完了");
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  handleServerMessage(data);
};

let presets = {};
let currentState = {
  expression: "normal",
  pose: "basic", 
  outfit: "usual"
};

let sprites = {};
let textures = {};

// プリセット読み込み
async function loadPresets() {
  try {
    const response = await fetch('/config/presets.json');
    presets = await response.json();
    setupUI();
    loadAssets();
  } catch (error) {
    console.error("プリセット読み込みエラー:", error);
  }
}

function setupUI() {
  // 表情ボタン
  const expressionContainer = document.getElementById('expression-buttons');
  Object.entries(presets.expressions).forEach(([key, preset]) => {
    const btn = document.createElement('button');
    btn.className = 'preset-btn';
    btn.textContent = preset.name;
    btn.onclick = () => changeExpression(key);
    if (key === currentState.expression) btn.classList.add('active');
    expressionContainer.appendChild(btn);
  });

  // ポーズボタン
  const poseContainer = document.getElementById('pose-buttons');
  Object.entries(presets.poses).forEach(([key, preset]) => {
    const btn = document.createElement('button');
    btn.className = 'preset-btn';
    btn.textContent = preset.name;
    btn.onclick = () => changePose(key);
    if (key === currentState.pose) btn.classList.add('active');
    poseContainer.appendChild(btn);
  });

  // 衣装ボタン
  const outfitContainer = document.getElementById('outfit-buttons');
  Object.entries(presets.outfits).forEach(([key, preset]) => {
    const btn = document.createElement('button');
    btn.className = 'preset-btn';
    btn.textContent = preset.name;
    btn.onclick = () => changeOutfit(key);
    if (key === currentState.outfit) btn.classList.add('active');
    outfitContainer.appendChild(btn);
  });

  // 音声ボタン
  document.getElementById('speak-btn').onclick = () => {
    const text = document.getElementById('speech-text').value.trim();
    if (text) {
      ws.send(JSON.stringify({action: "speak_text", text: text}));
    }
  };
}

function changeExpression(key) {
  currentState.expression = key;
  updateActiveButtons();
  updateCharacter();
  ws.send(JSON.stringify({action: "change_expression", preset: key}));
}

function changePose(key) {
  currentState.pose = key;
  updateActiveButtons();
  updateCharacter();
  ws.send(JSON.stringify({action: "change_pose", preset: key}));
}

function changeOutfit(key) {
  currentState.outfit = key;
  updateActiveButtons();
  updateCharacter();
  ws.send(JSON.stringify({action: "change_outfit", preset: key}));
}

function updateActiveButtons() {
  document.querySelectorAll('.preset-btn').forEach(btn => btn.classList.remove('active'));
  
  const containers = ['expression-buttons', 'pose-buttons', 'outfit-buttons'];
  const states = [currentState.expression, currentState.pose, currentState.outfit];
  
  containers.forEach((containerId, index) => {
    const container = document.getElementById(containerId);
    const buttons = container.querySelectorAll('.preset-btn');
    const presetKeys = Object.keys(presets[containerId.replace('-buttons', '').replace('expression', 'expressions')]);
    const activeIndex = presetKeys.indexOf(states[index]);
    if (activeIndex >= 0 && buttons[activeIndex]) {
      buttons[activeIndex].classList.add('active');
    }
  });
}

function loadAssets() {
  app.loader
    .add("body", "/assets/zundamon_en/outfit2/body.png")
    .add("swimsuit", "/assets/zundamon_en/outfit2/swimsuit.png")
    .add("usual_clothes", "/assets/zundamon_en/outfit1/usual_clothes.png")
    .add("uniform", "/assets/zundamon_en/outfit1/uniform.png")
    .add("basic_right", "/assets/zundamon_en/outfit1/right_arm/basic.png")
    .add("basic_left", "/assets/zundamon_en/outfit1/left_arm/basic.png")
    .add("point_right", "/assets/zundamon_en/outfit1/right_arm/point.png")
    .add("waist_left", "/assets/zundamon_en/outfit1/left_arm/waist.png")
    .add("raise_hand_right", "/assets/zundamon_en/outfit1/right_arm/raise_hand.png")
    .add("think_left", "/assets/zundamon_en/outfit1/left_arm/think.png")
    .add("mic_right", "/assets/zundamon_en/outfit1/right_arm/mic.png")
    .add("edamame", "/assets/zundamon_en/edamame/edamame_normal.png")
    .add("normal_white_eye", "/assets/zundamon_en/eye/eye_set/normal_white_eye.png")
    .add("sharp_white_eye", "/assets/zundamon_en/eye/eye_set/sharp_white_eye.png")
    .add("normal_eye", "/assets/zundamon_en/eye/eye_set/pupil/normal_eye.png")
    .add("smile_eye", "/assets/zundamon_en/eye/smile_eye.png")
    .add("sharp_eye", "/assets/zundamon_en/eye/sharp_eye.png")
    .add("sleepy_eye", "/assets/zundamon_en/eye/sleepy_eye.png")
    .add("normal_eyebrow", "/assets/zundamon_en/eyebrow/normal_eyebrow.png")
    .add("angry_eyebrow", "/assets/zundamon_en/eyebrow/angry_eyebrow.png")
    .add("troubled_eyebrow1", "/assets/zundamon_en/eyebrow/troubled_eyebrow1.png")
    .add("troubled_eyebrow2", "/assets/zundamon_en/eyebrow/troubled_eyebrow2.png")
    .add("muhu", "/assets/zundamon_en/mouth/muhu.png")
    .add("hoa", "/assets/zundamon_en/mouth/hoa.png")
    .add("triangle", "/assets/zundamon_en/mouth/triangle.png")
    .add("nn", "/assets/zundamon_en/mouth/nn.png")
    .add("nnaa", "/assets/zundamon_en/mouth/nnaa.png")
    .load((loader, resources) => {
      textures = resources;
      createCharacter();
    });
}

function createCharacter() {
  app.stage.removeChildren();
  sprites = {};

  // レイヤー順で配置
  createSprite("body", "body");
  createSprite("swimsuit", "swimsuit");
  createSprite("clothes", getCurrentClothes());
  createSprite("eyeWhite", getCurrentEyeWhite());
  createSprite("eyeBlack", getCurrentEyeBlack());
  createSprite("eyebrow", getCurrentEyebrow());
  createSprite("mouth", getCurrentMouth());
  createSprite("rightArm", getCurrentRightArm());
  createSprite("leftArm", getCurrentLeftArm());
  createSprite("edamame", "edamame");
}

function createSprite(name, textureKey) {
  if (textureKey && textures[textureKey]) {
    sprites[name] = new PIXI.Sprite(textures[textureKey].texture);
    sprites[name].x = 0;
    sprites[name].y = 0;
    app.stage.addChild(sprites[name]);
  }
}

function getCurrentEyeWhite() {
  return presets.expressions[currentState.expression].eyeWhite;
}

function getCurrentEyeBlack() {
  return presets.expressions[currentState.expression].eyeBlack;
}

function getCurrentEyebrow() {
  return presets.expressions[currentState.expression].eyebrow;
}

function getCurrentMouth() {
  return presets.expressions[currentState.expression].mouth;
}

function getCurrentRightArm() {
  return presets.poses[currentState.pose].rightArm + "_right";
}

function getCurrentLeftArm() {
  return presets.poses[currentState.pose].leftArm + "_left";
}

function getCurrentClothes() {
  const clothes = presets.outfits[currentState.outfit].clothes;
  return clothes;
}

function updateCharacter() {
  createCharacter();
}

function handleServerMessage(data) {
  // サーバーからのメッセージ処理
}

// 初期化
loadPresets();
console.log("✅ app.js 読み込み開始");

// Pixiアプリ初期化
let app = new PIXI.Application({
  width: 800,
  height: 600,
  backgroundColor: 0x333333
});
document.body.appendChild(app.view);
console.log("✅ Pixi初期化OK");

// 素体と口を読み込む
PIXI.Loader.shared
  .add("body", "/assets/zundamon/_服装2/_素体_pos_306_167_751_1579.png")
  .add("mouth", "/assets/zundamon/!口/_むー_pos_475_483_518_512.png")
  .load((loader, resources) => {
    console.log("✅ 画像ロード完了");

    // 素体
    let bodySprite = new PIXI.Sprite(resources.body.texture);
    bodySprite.x = 0;
    bodySprite.y = 0;
    app.stage.addChild(bodySprite);

    // 口
    let mouthSprite = new PIXI.Sprite(resources.mouth.texture);
    mouthSprite.x = 300;
    mouthSprite.y = 300;
    app.stage.addChild(mouthSprite);

    console.log("✅ 素体と口を追加");
  });

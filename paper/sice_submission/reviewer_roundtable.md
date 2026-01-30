---
marp: true
theme: default
size: 9:16
paginate: true
header: "SICE Reviewer Roundtable"
footer: "2026-01-18"
style: |
  section {
    font-family: "Hiragino Maru Gothic Pro", "Yu Gothic", sans-serif;
    padding: 40px;
    font-size: 24px;
    justify-content: flex-start;
  }
  h1 { font-size: 36px; color: #2d5f8b; }
  h2 { font-size: 28px; color: #d64045; border-bottom: none; }
  strong { color: #d64045; }
  .chat-bubble {
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 20px;
    position: relative;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  .reviewer-a { background: #e3f2fd; border-left: 5px solid #2196f3; }
  .reviewer-b { background: #f3e5f5; border-left: 5px solid #9c27b0; }
  .reviewer-c { background: #e8f5e9; border-left: 5px solid #4caf50; }
  .name { font-weight: bold; font-size: 18px; margin-bottom: 5px; display: block; }
---

# SICE論文 査読座談会
## 「頭が真っ白」を数理で防ぐ！？

**参加者:**
- 🔵 **Dr. 数理 (制御工学)**
- 🟣 **Prof. 心理 (認知科学)**
- 🟢 **Dr. 実装 (社会実装)**

---

<div class="chat-bubble reviewer-a">
<span class="name">🔵 Dr. 数理</span>
この論文、面白いね。「パニック」を<b>Double-Well Potential</b>の「雪崩現象」としてモデル化してる。
制御屋としては「スライディングモード制御(SMC)」をここに持ってくるか！という驚きがあるよ。
</div>

<div class="chat-bubble reviewer-b">
<span class="name">🟣 Prof. 心理</span>
ええ。心理学でも「うつ」を双安定系で捉える話はあるけど、それを<b>「リアルタイム制御」</b>しようという発想はなかったわ。
</div>

---

<div class="chat-bubble reviewer-a">
<span class="name">🔵 Dr. 数理</span>
ただ、普通のSMCだと<b>チャタリング</b>（ガタガタ振動）が起きるよね？心に対してそれはマズくない？
</div>

<div class="chat-bubble reviewer-b">
<span class="name">🟣 Prof. 心理</span>
そう！そこが重要。
著者は $\tanh$ 関数を使って<b>「滑らかに」</b>介入してる。
「心のエアバッグ」という比喩は言い得て妙ね。ガツンと止めるんじゃなくて、フワッと支える。
</div>

---

<div class="chat-bubble reviewer-c">
<span class="name">🟢 Dr. 実装</span>
社会実装の観点からも興味深いです。
パワハラ対策とか、企業のメンタルヘルス管理に使える。
「パニックになりそうな瞬間」だけ介入するから、普段は邪魔にならないのがいい。
</div>

<div class="chat-bubble reviewer-a">
<span class="name">🔵 Dr. 数理</span>
シミュレーション結果も、遵守率99.9%と優秀だね。
ただ、パラメータ $a, b$ の個人差はどうするつもりかな？
</div>

---

<div class="chat-bubble reviewer-c">
<span class="name">🟢 Dr. 実装</span>
そこは「今後の課題」で触れられていますね。
ウェアラブルセンサで個人の特性を学習する<b>「キャリブレーション期間」</b>が必要でしょう。
</div>

<div class="chat-bubble reviewer-b">
<span class="name">🟣 Prof. 心理</span>
倫理面も大事よ。「機械に心を操作される」という拒否感が出ないようなUI設計が鍵になりそう。
</div>

---

<div class="chat-bubble reviewer-a">
<span class="name">🔵 Dr. 数理</span>
総評としては？
</div>

<div class="chat-bubble reviewer-b">
<span class="name">🟣 Prof. 心理</span>
<b>「採録 (Accept)」</b>でいいと思うわ。
心理学と制御工学の新しい融合領域を開拓してる。
</div>

<div class="chat-bubble reviewer-c">
<span class="name">🟢 Dr. 実装</span>
同感です。この技術、僕もプレゼンの時に欲しいです(笑)
</div>

---

# 判定: 採録 (Accept)

**新規性:** ⭐️⭐️⭐️⭐️⭐️
**有効性:** ⭐️⭐️⭐️⭐️
**面白さ:** ⭐️⭐️⭐️⭐️⭐️

> 「心の安定」をエンジニアリングする、野心的な研究である。

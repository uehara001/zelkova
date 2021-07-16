<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="../css/stylesheet.css">
  <title>Zelkova-指数作成コンテンツ</title>
 
</head>
<body>
<!-- ヘッダー -->
  <header class="maincolor">
    <div class="wrapper" id="hc">
    <a href="../index.html"><img class="logo" src="../img/logo.png"></a>
    </div>
  </header>
  
<!-- メイン -->
  <main class="wrapper">
  <time id="raceday">2020年5月28日</time>
  <div id="raceinfo">
    <h1>川崎競馬1R</h1>
    <p class="distance">距離:</p>
    <p class="condition">馬場状態:</p>
  </div>
  <section id="tool">
    <!-- 指数表 -->
    <div class="content" id="indextable">
      <?php
      $index_file = "allIndex.csv";
      if (( $handle = fopen  ( $index_file, "r" )) !== FALSE) {
        echo "<table id='allIndex'>\n";
        while (($data = fgetcsv ($handle, 1000, ",", '"')) !== FALSE) {
        echo "\t<tr class='maincolor'>\n";
        for ($i = 0; $i < count($data); $i++) {
          echo "\t\t<td>{$data[$i]}</td>\n";
        }
        echo "\t</tr>\n";
        }
        echo "</table>\n";
        fclose ($handle);
      }
      ?>
    </div>
    <!-- ランキング -->
    <div class="content" id="ranking">
      <table>
        <thead >
          <tr>
            <th class="tablehead maincolor">指数</th>
            <th class="tablehead maincolor">競走馬</th>
          </tr>
        </thead>
        <tbody id="rankingtbody">
          <tr id="rankingdefo"><td colspan="2">ここに計算結果が出力されます。</td></tr>
        </tbody>
      </table>
      
    </div>
  </section>
    <!-- スライダー -->
    <section class="content" id="numselect">
      <form>
        <div id="slider">
          <div class="range">
            <p>馬番</p>
            <span class="ratio">5</span>
            <input name="r1" type="range" min="0" max="10" step="1" value="5" list="nummarks">
          </div>
          <div class="range">
            <p>種牡馬</p>
            <span class="ratio">5</span>
            <input name="r2" type="range" min="0" max="10" step="1" value="5" >
          </div>
          <div class="range">
            <p>騎手</p>
            <span class="ratio">5</span>
            <input name="r3" type="range" min="0" max="10" step="1" value="5" >
          </div>
          <div class="range">
            <p>調教師</p>
            <span class="ratio">5</span>
            <input name="r4" type="range" min="0" max="10" step="1" value="5" >
          </div>
          <div class="range">
            <p>スピード</p>
            <span class="ratio">5</span>
            <input name="r5" type="range" min="0" max="10" step="1" value="5" >
          </div>
          <div id="tool-button" class="range">
            <input id="reset" type="reset" value="リセット" onclick="resetFunction()">
            <input id="calc-button" type="button" onclick="calc(r1.value, r2.value, r3.value, r4.value, r5.value);" value="決　定">
          </div>
        </div>

      </form>
    </section>
    <!-- 出走表 -->
    <section id="cardtable">
      <?php
      $raceCard_file = "raceCard.csv";
      if (( $handle = fopen  ( $raceCard_file, "r" )) !== FALSE) {
        echo "<table>\n";
        while (($data = fgetcsv ($handle, 1000, ",", '"')) !== FALSE) {
          echo "\t<tr>\n";
          for ($i = 0; $i < count($data); $i++) {
            echo "\t\t<td>{$data[$i]}</td>\n";
          }
          echo "\t</tr>\n";
        }
        echo "</table>\n";
        fclose ($handle);
      }
      ?>
    </section>
  </main>
  
  <!-- フッター -->
  <footer>

  </footer>
  <script src="../js/main.js"></script>
</body>
</html>
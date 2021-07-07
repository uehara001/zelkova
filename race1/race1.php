<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="../css/stylesheet.css">
  <title>Keiba</title>
 
</head>
<body>
<!-- ヘッダー -->
  <header>
    <div class="wrapper" id="hc">
    <a href="../index.html"><img class="logo"></a>
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
    <!-- ランキング -->
    <div class="content tc" id="ranking">
      <table id="rankingTable"></table>
    </div>
    <!-- 指数表 -->
    <div class="content tc" id="indextable">
      <?php
      $index_file = "allIndex.csv";
      if (( $handle = fopen  ( $index_file, "r" )) !== FALSE) {
        echo "<table id='allIndex'>\n";
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
    </div>
  </section>
    <!-- スライダー -->
    <section class="content tc" id="numselect">
      <form action="index.php" method="post">
        <div class="range"><p>馬番</p>
        <input name="r1" type="range" min="0" max="10" step="0.1" value="5" >
        <span class="ratio">5</span>
        </div>
        <div class="range"><p>種牡馬</p>
          <input name="r2" type="range" min="0" max="10" step="0.1" value="5" >
          <span class="ratio">5</span>
        </div>
        <div class="range"><p>騎手</p>
          <input name="r3" type="range" min="0" max="10" step="0.1" value="5" >
          <span class="ratio">5</span>
        </div>
        <div class="range"><p>調教師</p>
          <input name="r4" type="range" min="0" max="10" step="0.1" value="5" >
          <span class="ratio">5</span>
        </div>
        <div class="range"><p>スピード</p>
          <input name="r5" type="range" min="0" max="10" step="0.1" value="5" >
          <span class="ratio">5</span>
        </div>

        <div id="tool_button">
          <input id="calc-button" type="button" onclick="calc(r1.value, r2.value, r3.value, r1.value, r5.value);" value="決定">
          <input id="reset" type="reset" value="リセット" onclick="resetFunction()">
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
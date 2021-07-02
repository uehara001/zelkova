<?php
$dsn = 'mysql:host=localhost;dbname=keiba;charaset=utf8';
$user = 'keiba_user';
$pass = 'sxug92s';
try {
  $dbh = new PDO($dsn,$user,$pass,[
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
  ]);
  // echo '接続成功';
  $sql = 'SELECT * FROM ooi062912';
  $stmt = $dbh->query($sql);
  $result = $stmt -> fetchall(PDO::FETCH_ASSOC);
  $dbh = null;
} catch(PDOException $e) {
  echo '接続失敗',  $e->getMessage();
  exit();
};
?>
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="css/stylesheet.css">
  <title>Keiba</title>
 
</head>
<body>
  <header>
    <div class="wrapper" id="hc">
    <img class="logo">
    </div>
  </header>
  <main class="wrapper">
  <time>2020年5月28日</time>
  <div id="raceinfo">
    <h1>川崎競馬1R</h1>
    <p class="distance">距離:</p>
    <p class="condition">馬場状態:</p>
  </div>
  <!-- メイン -->
  <section id="tool">
    <div class="content tc" id="ranking">
      <table id="rankingTable"></table>
    </div>
    
    <div class="content tc" id="indextable">
      <table id="allIndex">
      <tr>
        <td>  </td>
        <td>競走馬</td>
        <td>馬番</td>
        <td>種牡馬</td>
        <td>騎手</td>
        <td>調教師</td>
        <td>スピード</td>
      </tr>
        <?php
          foreach($result as $column){
          echo "\t<tr>\n";
          echo "\t\t<td>" ;
          echo $column['num'];
          echo "</td>\n";
          echo "\t\t<td>" ;
          echo $column['name'];
          echo "</td>\n";
          echo "\t\t<td>" ;
          echo $column['position'];
          echo "</td>\n";
          echo "\t\t<td>" ;
          echo $column['stallion'];
          echo "</td>\n";
          echo "\t\t<td>" ;
          echo $column['jockey'];
          echo "</td>\n";
          echo "\t\t<td>" ;
          echo $column['trainer'];
          echo "</td>\n";
          echo "\t\t<td>" ;
          echo $column['speed'];
          echo "</td>\n";
          echo "\t</tr>\n";
          echo "\n";
          }
        ?>
      </table>
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
    $file = "出走表.csv";
    if (( $handle = fopen  ( $file, "r" )) !== FALSE) {
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

  <footer>

  </footer>
  <script src="js/main.js"></script>
</body>
</html>
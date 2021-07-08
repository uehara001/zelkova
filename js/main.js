"use strict";
// スライダーについて-----------------
let elem = document.getElementsByClassName('range');
let rangeValue = function (elem, target) {
  return function (evt) {
    target.innerHTML = elem.value;
  };
};
for (let i = 0, max = elem.length; i < max; i++) {
  let bar = elem[i].getElementsByTagName('input')[0];
  let target = elem[i].getElementsByTagName('span')[0];
  bar.addEventListener('input', rangeValue(bar, target));
};

// リセットボタン
function resetFunction() {
  let ratioElements = document.getElementsByClassName('ratio');
  ratioElements = Array.from(ratioElements);
  ratioElements.forEach(element => {
    element.innerHTML = '5';
  });
}


// calc関数定義
let trElements = document.getElementById('allIndex').getElementsByTagName('tr');
let rankingTable = document.getElementById('rankingtbody');
function calc(r1, r2, r3, r4, r5) {
  let resultArray = [];
  const makeRunking = new Promise(function (resolve) {
    while (rankingTable.firstChild) {
      rankingTable.removeChild(rankingTable.firstChild);
    }
    for (let i = 1, max = trElements.length; i < max; i++) {
      let trElement = trElements[i];
      let tdElements = trElement.getElementsByTagName('td');

      let a = tdElements[2].textContent;
      let b = tdElements[3].textContent;
      let c = tdElements[4].textContent;
      let d = tdElements[5].textContent;
      let e = tdElements[6].textContent;
      let params = [a, b, c, d, e];
      let num = params.filter(function (value) {
        return value == 0;
      });
      let n = num.length;
      let x = Math.round((a * r1 + b * r2 + c * r3 + d * r4 + e * r5) / (5 - n)) / 10;
      let resultData = {};
      resultData.name = tdElements[1].textContent;
      resultData.index = x;
      resultArray.push(resultData);
    }
    resultArray.sort(function (s, t) {
      if (s.index < t.index) return 1;
      if (s.index > t.index) return -1;
      return 0;
    });
    resolve();
  });

  makeRunking.then(function () {
    for (let i = 0; i < resultArray.length; i++) {
      let resultCol = resultArray[i];
      document.getElementById('rankingtbody').innerHTML
        += '<tr><td>' + resultCol.index + '</td><td>' + resultCol.name + '</td></tr>';
    };
  });
}

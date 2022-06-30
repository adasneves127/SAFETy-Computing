let sclX, sclY, resX, resY;
let character = new characterData();

function setup() {

  resX = 4;
  resY = 8;
  sclX = 30;
  sclY = 30


  resX++;
  resY;

  createCanvas(resX * sclX, resY * sclY);
  character.init();

  let reset = createButton('reset');

  reset.mousePressed(function() {
    character.init();
  });

  let convert = createButton('convert');

  convert.mousePressed(convertChar);

}

function drawChar(charArr){
  for(let i = 0; i < charArr.length; i++){
    for(let j = 0; j < 8; j++){
      if(charArr[i] & (1 << j)){
      characterData.toggle(i, j)
      }
    }
  }
}

function convertChar(){
  
  for( let x = 0; x < resX; x++){
    let charData = "0b";
    for (let i = resY - 1; i >= 0 ; i--) {
      charData += character.data[x][i] ? "1" : "0";
    }
    print(charData);
  }



}

function draw() {
  background(220);
  //drawGrid();
  character.draw();

}


function drawGrid(){
  for (let i = 0; i < resX; i++) {
    for (let j = 0; j < resY; j++) {
      let x = i * scl;
      let y = j * scl;
      stroke(0);
      strokeWeight(1);
      line(x, 0, x, height);
      line(0, y, width, y);
    }
  }
}

function mouseClicked(){
  let x = floor(mouseX / sclX);
  let y = floor(mouseY / sclY);
  character.toggle(x, y);
}

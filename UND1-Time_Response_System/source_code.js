function cor(r_color, g_color, b_color){
	return [r_color, g_color, b_color]
}

var lista_letras = ["A", "S", "D", "F"]
var lista_cores = ["red", "green", "blue", "yellow"]
var keycode_letras = {"A" : 65, "S" : 83, "D" : 68, "F" : 70}
var cores_letras = {"A" : "red", "S" : "green", "D" : "blue", "F" : "yellow"}
var letras_cores = {"red" : "A","green" : "S", "blue" : "D","yellow" :  "F"}
var cores_rgb = {"red" : cor(255, 0, 0), "green" : cor(0, 255, 0), "blue" : cor(0, 0, 255), "yellow" : cor(255, 255, 0), "white" : 255}
var stage = 0
var acertos = 0
var cont_tentativa = 0
var tempo_por_tentativa = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

function setup() {
	createCanvas(1000, 1000)
	background(255, 255, 255)
}

function draw_blocks(){
	noStroke()
	fill(cores_rgb["yellow"])
	rect(750,750,250,250)
	fill(cores_rgb["blue"])
	rect(500,750,250,250)
	fill(cores_rgb["green"])
	rect(250,750,250,250)
	fill(cores_rgb["red"])
	rect(0,750,250,250)
	fill(0)
	textSize(100)
	text(lista_letras[0],100,900)
	text(lista_letras[1],350,900)
	text(lista_letras[2],600,900)
	text(lista_letras[3],850,900)
}

function shade_specific_block(block_letter){
	if (block_letter === "A"){
		fill(80, 0, 0)
		rect(0,750,250,250)
	}
	if (block_letter === "S"){
		fill(0, 80, 0)
		rect(250,750,250,250)
	}
	if (block_letter === "D"){
		fill(0, 0, 80)
		rect(500,750,250,250)
	}
	if (block_letter === "F"){
		fill(80, 80, 0)
		rect(750,750,250,250)
	}
	fill(0)
	textSize(100)
	text(lista_letras[0],100,900)
	text(lista_letras[1],350,900)
	text(lista_letras[2],600,900)
	text(lista_letras[3],850,900)
} 

function random_block(random_color){
	noStroke()
	fill(cores_rgb[random_color])
	rect(250,100,500,500)
}

function wait_time(ms){
   var start = new Date().getTime();
   var end = start;
   while(end < start + ms){
     end = new Date().getTime();
  }
}

function get_mean(tempo_por_tentativa, len = 10){
	var sum = 0
	for (var i = 0; i < len; i++){
		sum+= tempo_por_tentativa[i]
	}
	return sum / len
}

function calc_score(tempo_por_tentativa, acertos, len = 10){
	score = 0
	for (var i = 0; i < len; i++){
		score+= Math.exp(- 2 * (tempo_por_tentativa[i] / 1000))
	}
	return 100 * (acertos / len) * score
}

function draw (){

	if (stage === 0){ //Tela de inicio
		draw_blocks()
		textSize(50)
		text("PRESS ENTER \n   AND WAIT", 350, 350)
		if(keyIsDown(ENTER)){
			stage = 1
		}
	}
	
	if (stage === 1){ //Transicao de cor
		draw_blocks()
		random_time_wait = 1 + Math.random() * 4
		wait_time(random_time_wait * 1000) //Espera por um tempo aleatorio entre 1s e 5s
		random_color = lista_cores[Math.floor(Math.random() * 4)]
		random_block(random_color)
		stage = 2
		letra_correta = letras_cores[random_color]
		init_time = performance.now()
	}
	
	if (stage === 2){ //Interacao com o usuario. Tempo contando
		if(keyIsDown(keycode_letras["A"])){
			end_time = performance.now()
			shade_specific_block("A")
			if(letra_correta === "A"){
				acertos++
			}
			stage = 3
		}
		if(keyIsDown(keycode_letras["S"])){
			end_time = performance.now()
			shade_specific_block("S")
			if(letra_correta === "S"){
				acertos++
			}
			stage = 3
		}
		if(keyIsDown(keycode_letras["D"])){
			end_time = performance.now()
			shade_specific_block("D")
			if(letra_correta === "D"){
				acertos++
			}
			stage = 3
		}
		if(keyIsDown(keycode_letras["F"])){
			end_time = performance.now()
			shade_specific_block("F")
			if(letra_correta === "F"){
				acertos++
			}
			stage = 3
		}
	}
	
	if (stage === 3){ //Contabilizando pontos e verificando se ja encerrou ou nao
		tempo_por_tentativa[cont_tentativa] = end_time - init_time //Tempo de resposta em ms
		cont_tentativa++
		alert("Time: " + (end_time - init_time) + " ms")
		if (cont_tentativa == 10){
			stage = 4
		}
		else{
			stage = 1
		}
		random_block("white")
	}
	
	if (stage === 4){ //Estagio final. Aqui sera exibido um relatorio dos resultados para o usuario
		background(51);
		textSize(70)
		fill(255)
		text("🏁 Performance Report 🏁", 50, 200)
		textSize(50)
		tempo_por_tentativa.sort((a,b) => a-b) //Ordenando array
		text("🐇 Min Time:\t" + (tempo_por_tentativa[0] / 1000).toFixed(4) + "s", 80, 400)
		text("🐢 Max Time:\t" + (tempo_por_tentativa[9] / 1000).toFixed(4) + "s", 80, 500)
		text("📌 Mean Time:\t" + (get_mean(tempo_por_tentativa) / 1000).toFixed(4) + "s", 80, 600)
		text("🤺 Hit Rate:\t" + acertos  + "/10", 80, 700)
		text("🤖 Score:\t" + calc_score(tempo_por_tentativa, acertos).toFixed(4), 80, 800)
	}
}


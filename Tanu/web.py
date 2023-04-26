def web_page():
    webpage = """
<!DOCTYPE html>
<html>
<body>

    <!DOCTYPE html>
    <html>
    <head>
    <title>Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://kit.fontawesome.com/b6fe3b813e.js" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"></script>
    
    <style>
    h2 {
        font-size: 2.3rem;
        text-align: center;
    }
    h3 {
        font-size: 2.3rem;
        text-align: center;
    }
    p {
        font-size: 1.9rem;
        text-align: center;
    }
    
    /* Progress bar code */
    .progress {
      position: relative;
      width: 250px;
      height: 40px;
      background: #FFF47C;
      border-radius: 5px;
      overflow: hidden;
      margin: auto;
    }
    
    /* Progress bar code */
    .progress__fill {
      width: 0%;
      height: 100%;
      background: #FFD65C;
      transition: all 0.2s;
    }
    
    /* Progress bar code */
    .progress__text {
      position: absolute;
      top: 50%;
      right: 5px;
      transform: translateY(-50%);
      font: bold 16px "Quicksand", sans-serif;
      color: #000000;
    }
    
    /* Gauge and Slider for motor */
    
    .gauge {margin:auto; width: 100%; max-width: 250px; font-family: "Roboto", sans-serif; font-size: 32px; color: #003249;}
    .gauge__body {width: 100%; height: 0; padding-bottom: 50%; background: #003249; position: relative; border-top-left-radius: 100% 200%;
     border-top-right-radius: 100% 200%; overflow: hidden; }
    .gauge__fill { position: absolute; top: 100%; left: 0; width: inherit; height: 100%; background: #9fc5e8; transform-origin: center top;
     transform: rotate(0.25turn);
     transition: transform 0.2s ease-out;}
    .gauge__cover {width: 75%; height: 150%; background: #ffffff; border-radius: 50%; position: absolute; top: 25%; left: 50%; transform: translateX(-50%);
     display: flex; align-items: center; justify-content: center; padding-bottom: 25%; box-sizing: border-box; }
     .slider { -webkit-appearance: none; margin: 14px; width: 360px; height: 25px; background: #9fc5e8;
      outline: none; -webkit-transition: .2s; transition: opacity .2s;}
    .slider::-webkit-slider-thumb {-webkit-appearance: none; appearance: none; width: 35px; height: 35px; background: #003249; cursor: pointer;}
    .slider::-moz-range-thumb { width: 35px; height: 35px; background: #003249; cursor: pointer; }
    * {box-sizing: border-box}
    
    /* Set height of body and the document to 100% */
    
    body, html {
      height: 100%;
      margin: 0;
      font-family: Arial;
    }
    /* Style tab links */
    
    .tablink {
      background-color: #555;
      color: white;
      float: left;
      border: none;
      outline: none;
      cursor: pointer;
      padding: 14px 16px;
      font-size: 20px;
      width: 33.33%;
    }
    .tablink:hover {
      background-color: #777;
    }
    /* Style the tab content (and add height:100% for full page content) */
    
    .tabcontent {
      color: black;
      display: none;
      padding: 10px 20px;
    }
    
    
     .graph {
          padding-left: 0;
          padding-right: 0;
          margin-left: auto;
          margin-right: auto;
          display: block;
      }
      
    
    
    /* Button to add and delete valuues from the table */
    .button {
      border: none;
      color: white;
      padding: 10px 10px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      margin: 4px 2px;
      transition-duration: 0.4s;
      cursor: pointer;
      border-radius: 8px;
    }
    .button1 {
      font-size: 20px;
      background-color:green; 
      border: 5px solid grey;
      color: white; 
    }
    .button1:hover {
      border: 5px solid white;
      color: white;
    }
    
    .button2 {
      font-size: 20px;
      background-color: white; 
      color: black; 
      border: 8px solid #0F52BA;
    }
    .button2:hover {
      background-color: #0F52BA;
      color: white;
    }
    
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        text-align: left;
        padding: 8px;
    }
    tr:nth-child(even){background-color: #f2f2f2}
    th {
      background-color: #003249;
      color: white;
    }
    .center {
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    </head>
    <body>
    
    <button class="tablink" onclick="openPage('explore', this, 'purple')" id="defaultOpen">Explore <i class="fa-brands fa-wpexplorer"></i></button>
    <button class="tablink" onclick="openPage('train', this, '#0F52BA')" >Train <i class="fa-solid fa-code-branch"></i></button>
    <button class="tablink" onclick="openPage('play', this, 'green')">Play <i class="fa-solid fa-play"></i></button>
    
    <div id="explore" class="tabcontent">
        <h2> Explore Motor and Light sensor </h2>
    </div>
    
    <div id="train" class="tabcontent">
        <h2> Train Motor and Light sensor </h2>
    </div>
    
    <div id="play" class="tabcontent">
      <p> <button class="button button1" type="button" onclick="test()" id="toggle_play">Play!
 </button></p> 

    </div>
    
  
    
    <div id="motor" class="tabcontent">
        <div class="gauge">
          <div class="gauge__body">
            <div class="gauge__fill"></div>
            <div class="gauge__cover"></div>
          </div>
        </div>
    </div>
    
    <div id="slider_thing" class="tabcontent">
        <p><input type="range" onchange="updateSliderPWM(this)" id="pwmSlider" min="0" max="180" value="%SLIDERVALUE%" step="1" class="slider"></p>
    </div>
    
    <div id="light_sensor" class="tabcontent">
        <! –– Progress Bar code  ––>
        <div class="progress">
          <div class="progress__fill"></div>
          <span class="progress__text">0%</span>
        </div>
        
        <p>Light Sensor Reading <strong><span id="temp">--.-</span> </strong></p>
    </div>
    
    <div id="train_test_button" class="tabcontent">
        
        <p>
            <button class="button button2" type="button" onclick="addvalue()">Add Value</button>
            <button class="button button2" type="button" onclick="deletevalue()">Delete Value</button>
        </p>
    </div>
    <div id="my_graph" class="tabcontent">
                <canvas class="graph" id="myCanvas" width="330" height="280" style="border:1px solid #d3d3d3;">
Your browser does not support the HTML canvas tag.</canvas>
</div>
    
    
    <div id="tableeee" class="tabcontent">
    
        <h3>Training Values</h3>
        <table id="myTable" class="center">
        <thead>
             <th> Sensor Value </th>
             <th> Motor Value </th>
        </thead>
        <tbody id="tableBody">
             
        </tbody>
        </table>
    </div>
    
    <script>
            const sensor_array = [];
            const motor_array = [];
            var g;
            // Tabs 
            function openPage(pageName,elmnt,color) {
              var elem = document.getElementById("heading");
              var i, tabcontent, tablinks;
              tabcontent = document.getElementsByClassName("tabcontent");
              for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
              }
              tablinks = document.getElementsByClassName("tablink");
              for (i = 0; i < tablinks.length; i++) {
                tablinks[i].style.backgroundColor = "";
              }
              document.getElementById(pageName).style.display = "block";
              elmnt.style.backgroundColor = color;
              
              // displaying the motor and light sensor only when on exploration or training mode 
              if(pageName == "train" || pageName == "explore"){
                document.getElementById("motor").style.display = "block";
                document.getElementById("slider_thing").style.display = "block";
                document.getElementById("light_sensor").style.display = "block";
              }
              if(pageName == "explore")
              {
                  stop();
              }
              
              // displaying the buttons when on training mode 
              if(pageName == "train" ){
                stop();
                document.getElementById("train_test_button").style.display = "block";
                document.getElementById("tableeee").style.display = "block";
                document.getElementById("my_graph").style.display = "block";
              }
              
              if(pageName == "play"){
                //document.getElementById("motor").style.display = "block";
                document.getElementById("light_sensor").style.display = "block";
                document.getElementById("tableeee").style.display = "block";
                document.getElementById("my_graph").style.display = "block";
              
              }
              
              var c = document.getElementById("myCanvas");
        g = new Graph(c)
              
              
            }
            
            // Get the element with id="defaultOpen" and click on it
            document.getElementById("defaultOpen").click();
    
            // upDateProgressBar takes in progressBar container and updates the display of progress bar given a value 
            function updateProgressBar(progressBar, value) {
              progressBar.querySelector(".progress__fill").style.width = `${value}%`;
              progressBar.querySelector(".progress__text").textContent = `${value}%`;
            }
            const myProgressBar = document.querySelector(".progress");
            
            // set the value of the gauge 
            function setGaugeValue(gauge, value) {
                  if (value < 0 || value > 1) {
                    return;
                  }
                  gauge.querySelector(".gauge__fill").style.transform = `rotate(${
                    value / 2
                  }turn)`;
                  gauge.querySelector(".gauge__cover").textContent = `${Math.round(
                    value * 180
                  )} deg`;
            }
    
            // updates slidervalue 
            function updateSliderPWM(element) {
                  var sliderValue = document.getElementById("pwmSlider").value;
                  const gaugeElement = document.querySelector(".gauge");
                  setGaugeValue(gaugeElement, sliderValue/180);
                  console.log(sliderValue);
                  var xhr = new XMLHttpRequest();
                  xhr.open("GET", "/slider?value="+sliderValue, true);
                  xhr.send();
                  g.update_motor_val(Number(sliderValue))
                  g.redraw()
            }
            const gaugeElement = document.querySelector(".gauge");
            setGaugeValue(gaugeElement, 0.5);
            
            // update the light sensor reading 
            var ajaxRequest = new XMLHttpRequest();  
       
            function ajaxLoad(ajaxURL)  
            {  
                ajaxRequest.open('GET',ajaxURL,true);  
                ajaxRequest.onreadystatechange = function()  
                {  
                    if(ajaxRequest.readyState == 4 && ajaxRequest.status==200)  
                     {  
                        var ajaxResult = ajaxRequest.responseText;  
                        var tmpArray = ajaxResult.split("|");  
                        document.getElementById("temp").innerHTML = tmpArray[0];
                        if(tmpArray[1] != "-1")
                        {
                            g.update_motor_val(Number(tmpArray[1]))
                        }
                        updateProgressBar(myProgressBar, parseInt(ajaxResult));
                        g.update_sensor_val(Number(tmpArray[0]))
                        g.redraw()
                     }
                 
                }  
                ajaxRequest.send();  
            }  
             
            function updateDHT()   
            {   
                ajaxLoad('getDHT');   
            }
            // Controls how often the sensor is read 
            setInterval(updateDHT, 250);
            
            // add a row to the table
            function addvalue(){
                // get slider value reading
                var sliderValue = document.getElementById("pwmSlider").value;
                // get sensor reading
                var sensorValue = document.getElementById("temp").innerHTML;
                
                var xhttp = new XMLHttpRequest();
                xhttp.open("GET", "/?addvalue="+sliderValue+"="+sensorValue, true);
                xhttp.send();
                
                
                // Get the table body element in which you want to add row
                let table = document.getElementById("tableBody");
           
                // Create row element
                let row = document.createElement("tr")
          
                // Create cells
                let c1 = document.createElement("td")
                let c2 = document.createElement("td")
                
                sensor_array.push(Number(sensorValue));
                motor_array.push(Number(sliderValue));
                
                console.log("Sensor Array", sensor_array)
                console.log("Motor Array", motor_array)
              
                // Insert data to cells
                c1.innerText = sensorValue;
                c2.innerText = sliderValue;
          
                // Append cells to row
                row.appendChild(c1);
                row.appendChild(c2);
              
                // Append row to table body
                table.appendChild(row)
                
                // Add point to graph
                g.redraw();
            }
            
            function deletevalue() {
                var xhttp = new XMLHttpRequest();
                
                xhttp.open("GET", "/?deletevalue", true);
                xhttp.send();
                
                var table = document.getElementById('myTable');
                var rowCount = table.rows.length;
                if(rowCount > 1) {
                    table.deleteRow(rowCount -1);
                    sensor_array.pop();
                    motor_array.pop();
                    g.redraw();
                
                }
                
            }
            
            function test(){
                var button_text = document.getElementById('toggle_play').innerHTML;
                if(button_text == "Play!"){
                    document.getElementById('toggle_play').innerHTML = "Stop!";
                    document.getElementById('toggle_play').style.backgroundColor = 'red';
                    var xhttp = new XMLHttpRequest();
                    xhttp.open("GET", "/?test", true);
                    xhttp.send();
                      
                } else {
                    stop();
                }
            }
            
            function stop(){
                document.getElementById('toggle_play').innerHTML = "Play!";
                document.getElementById('toggle_play').style.backgroundColor = 'green';
                var xhttp = new XMLHttpRequest();
                xhttp.open("GET", "/?stop", true);
                xhttp.send();
            }
            
            class Graph{
            
            constructor(c) {  // Constructor
               this.canvas = c
               this.ctx = this.canvas.getContext("2d");
                // GRID width
                this.bw = this.canvas.width;
                // GRID height
                this.bh = this.canvas.height;
                // GRID PADDING
                this.start = 40;
                // GRID SPACING
                this.gap = 50;
                
                this.last_sensor_val = 50;
                this.last_motor_val = 90;
                
               this.redraw();
               
   
            }
            
           update_sensor_val(sval){
               this.last_sensor_val = sval;
           }
           
           update_motor_val(mval){
               this.last_motor_val = mval;
           }
            
           redraw(){
              console.log("Update graph");
              this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                this.draw_axes()
                this.draw_sensorline(this.last_sensor_val);
                this.draw_motorline(this.last_motor_val);
                for (var i = 0; i < sensor_array.length; i++) {
                    this.draw_point(sensor_array[i], motor_array[i]) 
                }
                
           }
           
           convert_x(x){
            // Assume the svals are 0-100 convert to a scale - start to bw-start
            var cx = ((this.bw-this.start*2) * (x/100)) + this.start;
            return cx;
           }
           
            convert_y(y){
            // Assume the svals are 0-100 convert to a scale - start to bh-start
            var cy = ((this.bh-this.start*2) * (180-y)/180) + this.start;
            return cy;
           }
           draw_sensorline(sval){
                this.ctx.beginPath();
                this.ctx.lineWidth = 4;
                this.ctx.strokeStyle = "#FFD65C";
                this.ctx.moveTo(this.convert_x(sval), this.convert_y(0));
                this.ctx.lineTo(this.convert_x(sval), this.convert_y(180));
                this.ctx.stroke();
           }
           draw_motorline(mval){
                this.ctx.beginPath();
                this.ctx.lineWidth = 4;
                this.ctx.strokeStyle = "#85B3DE";
                this.ctx.moveTo(this.convert_x(0), this.convert_y(mval));
                this.ctx.lineTo(this.convert_x(100), this.convert_y(mval));
                this.ctx.stroke();
           
           }
           
           draw_axes(){
                this.ctx.lineWidth = 1;
                this.ctx.beginPath();
                this.ctx.strokeStyle = "#e8e8e8";
                 for (var x = 0; x <= 100; x += 20) {
                //vert lines
                       this.ctx.moveTo(this.convert_x(x), this.convert_y(0));
                       this.ctx.lineTo(this.convert_x(x), this.convert_y(180));
                  }
                  for (var y = 0; y <= 180; y += 45) {
                 //horz lines
                      this.ctx.moveTo(this.convert_x(0), this.convert_y(y));
                      this.ctx.lineTo(this.convert_x(100), this.convert_y(y));
                  }
                  this.ctx.stroke();
                
                this.ctx.beginPath();
                this.ctx.strokeStyle = "#757575";
                this.ctx.rect(this.convert_x(0), this.convert_y(0), this.convert_x(100)-this.convert_x(0), this.convert_y(180)-this.convert_y(0));
                this.ctx.stroke();
                
                this.ctx.beginPath();
                this.ctx.font = "15px Arial";
                this.ctx.strokeText("Sensor Value",120,265);
                // horizontal axis
                this.ctx.strokeText("0",20,257);
                this.ctx.strokeText("100",276,257);
                // vertical axis
                this.ctx.strokeText("180",10,50);
                // save orientation again
                this.ctx.save();
                // hold top-right hand corner when rotating
                this.ctx.translate( 330 - 1, 0 );
                // rotate 270 degrees
                this.ctx.rotate( 3 * Math.PI / 2 );
                //this.ctx.font = "16px serif";
                //this.ctx.fillStyle = "#0000FF"; // blue
                this.ctx.textAlign = "right";
                // draw relative to translate point
                //this.ctx.fillText( "right-aligned 270 deg", -75, -300 );
                this.ctx.strokeText("Motor Value",-100,-300);
                this.ctx.restore();
           }
           
           
           draw_point(sval, mval) {
           
           //Assume the mvals are 0-180 convert to a scale - start+bh to star
              
              this.ctx.beginPath();
              this.ctx.fillStyle = "gray";
              this.ctx.arc(this.convert_x(sval),this.convert_y(mval),5,0,2*Math.PI);
        
        this.ctx.fill();
      }
            }
            
            
    </script>
       
    </body>
    </html> 
"""
    return webpage







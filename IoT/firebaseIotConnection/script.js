import {service} from "./js/datebaseConfig.js"

const endPoint = "/Amilton"

// Definindo estrutura do corpo do meu objeto do banco.
var body = {
    
}

// Carregando dados do meu banco
const loadData = () => {
    service.load(endPoint).then( data => {
        body = data;

        const room = ['LED1', 'LED2']

        room.forEach(room => {
            getLightsValues(room)
            setTempValues(room) 
            getTvValues(room)
        });
    })
}
// Definindo os dados no meu banco.
// service.set(endPoint, body)

// ==================  Colocando os dados no HTML   ==================
const getLightsValues = (idLocal) => {
    let lamp = document.getElementById('lightBulb' + idLocal)
    let lightOn = 0;
    let color = 0;

    switch (idLocal) {
        case 'LED1':
            lightOn = body.LED1.principalLight;
            color = body.LED1.color
            if(lightOn == 1){
                switch (color) {
                    case 1:
                        lamp.classList.add("light-red");
                        break;
        
                    case 2:
                        lamp.classList.add("light-blue");
                        break;
        
                    case 0:
                        lamp.classList.add("light-on");
                        break;
                
                    default:
                        break;
                }
            } else {
                lamp.classList.remove("light-on");
                lamp.classList.remove("light-red")
                lamp.classList.remove("light-blue")
            }
            break;
        
        case 'LED2':
            lightOn = body.LED2.principalLight;
            color = body.LED2.color
            if(lightOn == 1){
                switch (color) {
                    case 1:
                        lamp.classList.add("light-red");
                        break;
        
                    case 2:
                        lamp.classList.add("light-blue");
                        break;
        
                    case 0:
                        lamp.classList.add("light-on");
                        break;
                
                    default:
                        break;
                }
            } else {
                lamp.classList.remove("light-on");
                lamp.classList.remove("light-red")
                lamp.classList.remove("light-blue")
            }
            break;
    
        default:
            break;
    }

}

const getTvValues = (idLocal) => {
    let tv = document.getElementById(idLocal + "Tv")
    let tvOn = false;
    let tvValue = 0;

    switch (idLocal) {
        case 'LED1':
            tvValue = body.LED1.Tv;
            if (tvValue == 1){
                tvOn = !tvOn
            }
            break;

        case 'LED2':
            tvValue = body.LED2.Tv;
            if (tvValue == 1){
                tvOn = !tvOn
            }
            break;
    }

    if(tvOn){ 
        tv.innerHTML = 'On'
    } else {
        tv.innerHTML = 'OFF'
    }
}

const setTempValues = (idLocal) => {

    const TempElement = document.getElementById(idLocal + "Temp")
    const HumidElement = document.getElementById(idLocal + "Humidity")

    let Hvalue = 0;
    let Tvalue = 0;

    switch (idLocal) {
        case 'LED1':
            Hvalue = body.LED1.Umidade;
            Tvalue = body.LED1.Temperatura;
        
            TempElement.innerHTML = Tvalue + "°C"
            HumidElement.innerHTML = Hvalue + "%"
            break;

        case 'LED2':
                Hvalue = body.LED2.Umidade;
                Tvalue = body.LED2.Temperatura;
            
                TempElement.innerHTML = Tvalue + "°C"
                HumidElement.innerHTML = Hvalue + "%"
                break;
    
        default:
            break;
    }
}

// ================== Funções de Interação com HTML ==================

const toggleLamp = (idRoom) => {
    const element = document.getElementById("lightBulb" + idRoom);

    let lightOn = 0;
    let color = 0;

    switch (idRoom) {
        case 'LED1':
            lightOn = body.LED1.principalLight;
            color = body.LED1.color
            if(lightOn == 1){
                switch (color) {
                    case 1:
                        element.classList.add('light-red');
                        break;
        
                    case 2:
                        element.classList.add('light-blue');
                        break;
        
                    case 0:
                        element.classList.add('light-on');
                        break;
                
                    default:
                        break;
                }
            } else {
                element.classList.remove('light-red');
                element.classList.remove('light-blue');
                element.classList.remove('light-on');
            }
            break;

        case 'LED2':
            lightOn = body.LED2.principalLight;
            color = body.LED2.color
            if(lightOn == 1){
                switch (color) {
                    case 1:
                        element.classList.add('light-red');
                        break;
        
                    case 2:
                        element.classList.add('light-blue');
                        break;
        
                    case 0:
                        element.classList.add('light-on');
                        break;
                
                    default:
                        break;
                }
            } else {
                element.classList.remove('light-red');
                element.classList.remove('light-blue');
                element.classList.remove('light-on');
            }
            break;

        default:
            break;
    }

    service.set(endPoint, body);
}

const toggleLampClick = (idRoom) => {
    const element = document.getElementById("lightBulb" + idRoom);

    let lightOn = false;

    switch (idRoom) {
        case 'LED1':
            lightOn = !lightOn;
            if(lightOn){
                element.classList.add('light-on');
                body.principalLight = 1;
                body.color = 1;
                service.set(endPoint, body);
            } else {
                element.classList.remove('light-on');
                body.principalLight = 0;
                body.color = 0;
                service.set(endPoint, body);
            }

            break;

        case 'LED2':
            lightOn = !lightOn;
            if(lightOn){
                element.classList.add('light-on');
                body.principalLight = 1;
                body.color = 1;
                service.set(endPoint, body);
            } else {
                element.classList.remove('light-on');
                body.principalLight = 0;
                body.color = 0;
                service.set(endPoint, body);
            }
            break;

        default:
            break;
    }

}
const toggleTv = (idRoom) => {
    const element = document.getElementById(idRoom + "Tv")
    let isOn = false;

    switch (idRoom) {
        case "LED1":
            body.LED1.tv = !body.LED1.tv;
            isOn = body.LED1.tv;
            service.set(endPoint, body);
            break;
            
        case 'LED2' :
            body.LED2.tv = !body.LED2.tv;
            isOn = body.LED2.tv;
            service.set(endPoint, body);
            break;

        default:
            break;
    }
    if(isOn) {
        element.innerHTML = "ON"
    } else {
        element.innerHTML = "OFF"
    }
}


console.log('script loaded');

//! Adicionando as funções no HTML 

window.toggleLamp = toggleLamp
window.toggleTv = toggleTv
window.toggleLampClick = toggleLampClick

setInterval(() => {
    loadData();
}, 1000);
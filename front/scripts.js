var socket = io(apiDomain());


function dibujarPixels(){
    var matriz = document.getElementById('matriz')
    for(let i = 0; i < 24; i++){
        var fila = document.createElement('div')
        fila.className = 'fila'

        for(let j = 0; j < 24; j++){
            var p = document.createElement('div')
            p.className = 'caja'
            p.id = 'pixel_' + i + '_' + j

            p.style.backgroundColor = "#222222"

            p.addEventListener('click', pintarPixel)

            fila.appendChild(p)
        }
        matriz.appendChild(fila)
    }
}

function pintarPixel(event){
    var id = event.srcElement.id
    var color = document.getElementById('colorpicker').value
    document.getElementById(id).style.backgroundColor = color
    
    socket.emit('pixel', {data: [id, color]});
    //guardar()
}

function guardar(){
    var listaPixeles = []
    var matriz = document.getElementById('matriz');
    var rows = matriz.childNodes;
    rows.forEach(row => {
        var pixels = row.childNodes;
        pixels.forEach(p => {
            listaPixeles.push([p.id, p.style.backgroundColor])
        });
    });


    fetch(apiDomain() + '/guardar', {
        mode: 'cors', 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(listaPixeles)
    })
}

function cargar(){
    fetch(apiDomain() + '/cargar', {
        mode: 'cors', 
    }).then(response => response.json())
        .then(response => {
            response.forEach(p => {
                document.getElementById(p[0]).style.backgroundColor = p[1]
            })
        }).then(() => {
            setTimeout(cargar, 1000)
        })
}

socket.on('pixels', function(response) {
    console.log('pixels', response)
    Object.keys(response).forEach(id => {
        document.getElementById(id).style.backgroundColor = response[id]
    })
});


dibujarPixels()
//cargar()

$(document).ready(function() {
    lista = []
    objeto_consulta_info_p = {}
    console.log("Ready")
        url_get_consulta1 = "http://localhost:8080/info_preguntas"
        console.log("url_get_consulta1")
        $.ajax({
        type: "GET",
        url: url_get_consulta1
        }).then(function(data) {
            var data_json = JSON.parse(data)
            console.log("data: ")
            console.log(data_json)

            /*$.each(lista, function (i, item) {
            $('#selector_consulta_1').append($('<option>', { 
                value: item,
                text : item 
            }));
        });*/
    });
});
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
            $.each(data_json, function (i, item) {
                console.log(item)

                var e_list = "<ul>"
                $.each(item['entities'], function (j, jtem) {
                    var value = ""
                    if('geometry' in jtem){
                        value = jtem["id"] + " - lugar/organización"
                    }
                    else if(jtem["type"] == 1){
                        value = jtem["id"] + " - personaje"
                    }
                    else{
                        value = jtem["id"] + " - otro"
                    }
                    e_list = e_list+"<li>"+value+"</li>"
                });
                e_list = e_list + "</ul>"

                var tags_list = "<ul>"
                tag_1 = item['tag_1']
                tag_2 = item['tag_2']
                tag_3 = item['tag_3']
                
                if (tag_1 != null){
                    tags_list = tags_list+"<li>"+tag_1+"</li>"
                }
                if (tag_2 != null){
                    tags_list = tags_list+"<li>"+tag_2+"</li>"
                }
                if (tag_3 != null){
                    tags_list = tags_list+"<li>"+tag_3["id"]+"</li>"
                }
                tags_list = tags_list + "</ul>"

                $('#tabla_info_preguntas').append("<tr><td>"+item['question']+"</td><td>"+item['answer_1']+"</td><td>"+tags_list+"</td><td>"+e_list+"</td></tr>");
            });
            /*$.each(lista, function (i, item) {
            $('#selector_consulta_1').append($('<option>', { 
                value: item,
                text : item 
            }));
        });*/
    });
});
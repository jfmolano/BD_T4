$(document).ready(function() {

    console.log("Ready")

    url_get_consulta1 = "http://localhost:8080/info_preguntas"
    console.log("url_get_consulta1")
    $.ajax({
    type: "GET",
    url: url_get_consulta1
    }).then(function(data) {
        var data_json = JSON.parse(data)
        //console.log("data: ")
        //console.log(data_json)
        $.each(data_json, function (i, item) {
            //console.log(item)

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
    });

    url_get_consulta2 = "http://localhost:8080/info_georef"
    console.log("url_get_consulta2")
    $.ajax({
    type: "GET",
    url: url_get_consulta2
    }).then(function(data) {
        var data_json = JSON.parse(data)
        console.log("data: ")
        console.log(data_json)
        var map = L.map('mapid').setView([30, 0], 2);
              // load a tile layer
              L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                {
                  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                  subdomains: ['a','b','c']
                }).addTo(map);
        markers = [
           {
             "name": "test",
             "desc": "desc",
             "ans": "ans",
             "entities": ["e1","e2","e3"],
             "lat": -10,
             "lng": -10
           }
        ];

        for ( var i=0; i < data_json.length; ++i ){
            var entities_l = []
            var rest_entities_l = data_json[i].entities.enrichment
            for ( var j=0; j < rest_entities_l.length; ++j ){
                entities_l.push(data_json[i].entities.enrichment[j].id)
            }
           var obj = {
             "name": data_json[i].entities.id,
             "desc": data_json[i].question,
             "ans": data_json[i].answer_1,
             "entities": entities_l,
             "lat": data_json[i].entities.geometry.lat,
             "lng": data_json[i].entities.geometry.lon
           }
           console.log(obj)
           if(obj.lat!=0 && obj.lon!=0){
           markers.push(obj)
            }
        }

        for ( var i=0; i < markers.length; ++i ){
            entities_list = markers[i].entities
            var e_list = "<ul>"
            for ( var j=0; j < entities_list.length; ++j ){
                e_list = e_list+"<li>"+entities_list[j]+"</li>"
            }
            e_list = e_list + "</ul>"
           L.marker( [markers[i].lat+(Math.random()-0.5)*0.05, markers[i].lng+(Math.random()-0.5)*0.05] )
              .bindPopup( markers[i].name + "<br><br>" + markers[i].desc + "<br><br>" + markers[i].ans + "<br><br>" + e_list)
              .addTo( map );
        }
    });
});
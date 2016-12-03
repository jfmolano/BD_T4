$(document).ready(function() {

    ////console.log("Ready")
    objeto_bono = []
    url_get_consulta1 = "http://localhost:8080/info_preguntas"
    ////console.log("url_get_consulta1")
    $.ajax({
    type: "GET",
    url: url_get_consulta1
    }).then(function(data) {
        var data_json = JSON.parse(data)
        //////console.log("data: ")
        //////console.log(data_json)
        $.each(data_json, function (i, item) {
            //////console.log(item)

            var e_list = "<ul>"
            $.each(item['entities'], function (j, jtem) {
                var value = ""
                if('geometry' in jtem){
                    enriched = ""
                    if ("enrichment" in jtem){
                        if (jtem["enrichment"].length > 1){
                            enriched = jtem["enrichment"].reduce(function(a,b){return a.id+", "+b.id;});
                            enriched = "<br><i>Información de enriquecimiento:</i> " + enriched.replace("undefined,", "")
                        }
                    }
                    value = jtem["id"] + " - lugar/organización" + enriched
                }
                else if(jtem["type"] == 1){
                    enriched = ""
                    if ("enrichment" in jtem){
                        if (jtem["enrichment"].length > 1){
                            enriched = jtem["enrichment"].reduce(function(a,b){return a.id+", "+b.id;});
                            enriched = "<br><i>Información de enriquecimiento:</i> " + enriched.replace("undefined,", "")
                        }
                    }
                    value = jtem["id"] + " - personaje" + enriched
                }
                else{
                    value = jtem["id"] + " - otro"
                }
                e_list = e_list+"<li>"+value+"<br><br></li>"
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
    ////console.log("url_get_consulta2")
    $.ajax({
    type: "GET",
    url: url_get_consulta2
    }).then(function(data) {
        var data_json = JSON.parse(data)
        //////console.log("data: ")
        //////console.log(data_json)
        var map = L.map('mapid').setView([30, 0], 2);
              // load a tile layer
              L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                {
                  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                  subdomains: ['a','b','c']
                }).addTo(map);
        var markers = [
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
           //////console.log(obj)
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

    url_get_consulta3 = "http://localhost:8080/info_entidad"
    ////console.log("url_get_consulta3")
    $.ajax({
    type: "GET",
    url: url_get_consulta3
    }).then(function(data) {
        var data_json = JSON.parse(data)
        //////console.log("data: ")
        //////console.log(data_json)
        $.each(data_json, function (i, item) {
            //////console.log(item)
            categoria = ""
            if('geometry' in item.entities){
                    categoria = "Lugar/Organización"
                }
                else if(item.entities.type == 1){
                    categoria = "Personaje"
                }
                else{
                    categoria = "Otro"
                }
            var e_list = "<ul>"
            if("enrichment" in item.entities){
                $.each(item.entities.enrichment, function (j, jtem) {
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
                    e_list = e_list+"<li>"+value+"<br><br></li>"
                });       
            }
            e_list = e_list + "</ul>"
            $('#tabla_entidades').append("<tr><td>"+categoria+"</td><td>"+item.entities.id+"</td><td>"+e_list+"</td><td>"+item.question+"</td></tr>");
        });
    });

    url_get_consulta4 = "http://localhost:8080/info_geo_people"
    ////console.log("url_get_consulta4")
    $.ajax({
    type: "GET",
    url: url_get_consulta4
    }).then(function(data) {
        var data_json = JSON.parse(data)
        //////console.log("data: ")
        ////console.log(data_json)
        var map = L.map('mapid_people').setView([30, 0], 2);
              // load a tile layer
              L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                {
                  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                  subdomains: ['a','b','c']
                }).addTo(map);
        var markers = [
           {
             "name": "test",
             "plac": "place",
             "ques": "question",
             "entities": ["e1","e2","e3"],
             "lat": -10,
             "lng": -10
           }
        ];

        for ( var i=0; i < data_json.length; ++i ){
            item = data_json[i]
            var is_geo = false
            var lat = 0
            var lon = 0
            var is_geo_loc = false
            var place_name = ""
            if("enrichment" in item.entities){
                var entities_l = []
                $.each(item.entities.enrichment, function (j, jtem) {
                    var value = ""
                    if('geometry' in jtem){
                        value = jtem["id"] + " - lugar/organización"
                        if(!is_geo_loc && jtem.lat != 0 && jtem.lon != 0){
                            is_geo_loc = true
                            lat = jtem.geometry.lat
                            lon = jtem.geometry.lon
                            place_name = value
                            //console.log(jtem)
                        }
                    }
                    else if(jtem["type"] == 1){
                        value = jtem["id"] + " - personaje"
                    }
                    else{
                        value = jtem["id"] + " - otro"
                    }
                    entities_l.push(value)
                });       
            }
            var obj = {
             "name": data_json[i].entities.id,
             "ques": data_json[i].question,
             "plac": place_name,
             "entities": entities_l,
             "lat": lat,
             "lng": lon
           }
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
            //console.log("markers[i]")
            //console.log(markers[i])
            var redIcon = new L.Icon({
              iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
              shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
              iconSize: [25, 41],
              iconAnchor: [12, 41],
              popupAnchor: [1, -34],
              shadowSize: [41, 41]
            });
           L.marker( [markers[i].lat+(Math.random()-0.5)*0.05, markers[i].lng+(Math.random()-0.5)*0.05], {icon: redIcon} )
              .bindPopup( markers[i].name + "<br><br>Lugar: " + markers[i].plac + "<br><br>Pregunta: " + markers[i].ques + "<br><br>" + e_list)
              .addTo( map );
        }
    });

    url_get_consulta5 = "http://localhost:8080/info_tw_people"
    ////console.log("url_get_consulta3")
    $.ajax({
    type: "GET",
    url: url_get_consulta5
    }).then(function(data) {
        var data_json = JSON.parse(data)
        //////console.log("data: ")
        //////console.log(data_json)
        $.each(data_json, function (i, item) {
            var e_list = "<ul>"
            $.each(item.tweets, function (j, jtem) {
                e_list = e_list+"<li>Username: "+jtem.user+"</li>"
                e_list = e_list+"<li>Fecha: "+jtem.date+"</li>"
                e_list = e_list+"<li>Tweet: "+jtem.text+"<br><br></li>"
            });   
            e_list = e_list + "</ul>"
            $('#tabla_tw').append("<tr><td style=\"width=20%\">"+item.entities.id+"</td><td style=\"width=20%\">"+item.question+"</td><td style=\"width=20%\">"+item.answer_1+"</td><td style=\"width=30%\">"+e_list+"</td><td style=\"width=10%\">"+"11/11/2016"+"</td></tr>");
        });
    });

    url_get_consulta7 = "http://localhost:8080/tag_cloud"
    ////console.log("url_get_consulta3")
    $.ajax({
    type: "GET",
    url: url_get_consulta7
    }).then(function(data) {
        var data_json = JSON.parse(data)
        objeto_bono = data_json
        //////console.log("data: ")
        //////console.log(data_json)
        $.each(data_json, function (i, item) {
            $('#tg_container').append('<div style="font-size: 500%;word-break: keep-all;width:50%">');
            //console.log(item)
            $('#tg_container').append('<div style="color:green;">'+item.movie+"</div>");
            $.each(item.word_list, function (j, jtem) {
                var tam = 180/14*jtem.count
                if (tam>220){tam = 220}
                if (tam<40){tam = 40}
                $('#tg_container').append("<span style=\"font-size:"+tam+"%;\">"+jtem.word+" </span>");
            });
            $('#tg_container').append("</div><br><br>");
        });
    });

    url_get_consulta6 = "http://localhost:8080/questions_words"
    ////console.log("url_get_consulta3")
    $.ajax({
    type: "GET",
    url: url_get_consulta6
    }).then(function(data) {
        var data_json = JSON.parse(data)
        //////console.log("data: ")
        //////console.log(data_json)
        $.each(data_json, function (i, item) {
            $('#tabla_words_common').append("<tr><td>"+item.word+"</td></tr>");
            $('#tabla_words_common').append("<tr><td>"+item.questions+"</td></tr>");
        });
    });

    $("#Consultar").click(function(){
        var fini = $('#txt_FechaIni').val();
        var ffin = $('#txt_FechaFin').val();
        url_post = "http://localhost:8080/info_tw_people_post"
        var jsonData = "{\"fini\":\""+fini+"\",\"ffin\":\""+ffin+"\"}";
        //console.log(url_post)
        //console.log("JSON: "+jsonData)
        $.ajax({
            type: "POST",
            data: jsonData,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url: url_post
        }).then(function(data) {
            //console.log(data)
            //var data_json = JSON.parse(data)
            $('#tabla_tw tr').not(':first').remove();
            $.each(data, function (i, item) {
                var e_list = "<ul>"
                $.each(item.tweets, function (j, jtem) {
                    e_list = e_list+"<li>Username: "+jtem.user+"</li>"
                    e_list = e_list+"<li>Fecha: "+jtem.date+"</li>"
                    e_list = e_list+"<li>Tweet: "+jtem.text+"<br><br></li>"
                });   
                e_list = e_list + "</ul>"
                var bd = item.db
                if(bd == null){
                    bd = " - "
                }
                //console.log(bd)
                $('#tabla_tw').append("<tr><td style=\"width=20%\">"+item.entities.id+"</td><td style=\"width=20%\">"+item.question+"</td><td style=\"width=20%\">"+item.answer_1+"</td><td style=\"width=30%\">"+e_list+"</td><td style=\"width=10%\">"+bd+"</td></tr>");
            });
        });
    });
    hide = true
    $("#Ver").click(function(){
        if(hide){
            $("#movie_trivia").css("background-color", "white");
            hide = false
        }
        else{
            $("#movie_trivia").css("background-color", "black");
            hide = true
        }
    });
    $("#Siguiente").click(function(){
        var rand_movie = objeto_bono[Math.floor(Math.random() * objeto_bono.length)];
        $( "#movie_trivia" ).text(rand_movie.movie);
        var hint = ""
        for (var i=0;i<rand_movie.word_list.length;i++){
            console.log(rand_movie.word_list[i].word)
            hint = hint + ", " + rand_movie.word_list[i].word
        }
        $( "#hint_trivia" ).text(hint);
        console.log(rand_movie.word_list)
    });
});
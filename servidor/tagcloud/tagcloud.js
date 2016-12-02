//Tomado de http://geekthis.net/blog/101/javascript-tag-cloud
    function tagcloud(dom,tag) {
       var highVal = 0;
       var lowVal = Number.MAX_VALUE;
       var elements = dom.getElementsByTagName(tag);
       var minFont = parseInt(dom.getAttribute('data-minfont'),10);
       var maxFont = parseInt(dom.getAttribute('data-maxfont'),10);
       var fontDif = 0;
       var sizeDif = 0;
       var size = 0;
       var i = 0;
       var data = 0;
     
       for(i = 0; i < elements.length; ++i) {
          data = parseInt(elements[i].getAttribute('data-count'),10);
          if(data > highVal) {
             highVal = data;
          }
          if(data < lowVal) {
             lowVal = data;
          }
       }
     
       fontDif = maxFont - minFont;
       sizeDif = highVal - lowVal;
     
       for(i = 0; i < elements.length; ++i) {
          data = parseInt(elements[i].getAttribute('data-count'),10);
          size = (fontDif * (data - lowVal) / sizeDif) + minFont;
          size = Math.round(size);
          elements[i].style.fontSize = size + "px";
       }
    }

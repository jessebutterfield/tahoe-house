window.mapsConfig={1:{defaultLat:37.762496,defaultLng:-122.466341,southWest:[36.54,-120.3],northEast:[38.51,-123.23]},9:{defaultLat:45.523187,defaultLng:-122.681424,southWest:[46.346,-124.272],northEast:[44,-121]}},function(){var a=$("#map.viewposting");if(a.length){var b=a.data("latitude"),c=a.data("longitude"),d=a.data("accuracy")+0;if(b&&c){L.Icon.Default.imagePath="//www.craigslist.org/images/map";var e=new L.LatLng(b,c),f='&copy; craigslist - Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',g=new L.TileLayer(CL.maps.clMapsUrl,{subdomains:"0123456789",setView:!0,enableHighAccuracy:!0,prefix:"",attribution:f}),h=new L.Map("map",{center:e,zoom:14,zoomControl:!1,maxZoom:17,minZoom:1,maxBounds:[[-90,-180],[90,180]],layers:[g]});if(h.attributionControl.setPrefix(""),d>19?L.circle(e,500,{color:"#770091",weight:1,fillOpacity:.1}).addTo(h):L.marker(e,{draggable:!1}).addTo(h),CL.page.isMobile&&$("body.post").length)h.dragging.disable(),h.touchZoom.disable(),h.doubleClickZoom.disable(),h.scrollWheelZoom.disable(),h.boxZoom.disable(),h.keyboard.disable(),a.prepend('<div class="mapglass"></div>').find(".mapglass").on("touchstart touchmove",function(a){a.stopImmediatePropagation()});else{var i=L.Control.ZoomFS||L.Control.Zoom;h.addControl(new i),$(".leaflet-bar a").text("")}}}}(),function(){if(0!==$("body.posting, body.post, body.best").length){CL.when.localStorageAvailable.done(function(a){var b=a.getItem("srch"),c=a.getItem("searches"),d=!1;if(c)try{c=JSON.parse(c);var e=c[b];if(e){var f=e.header_list;if(f.length>1){var g=e.id2headeridx,h=Number(g[window.pID]),i=e.pag_table,j=100+Number(e.s);if(100===Number(i[e.s])&&!i[""+j]){var k="http://"+b.replace(/([&?]s=)0/,"$1"+j).replace(/index.html/,"index"+j+".html");$("body").append('<iframe id="refrload" style="display:none"></iframe>'),f[h+1]||$("#refrload").load(function(){var c=a.getItem("searches");if(c){c=JSON.parse(c);var e=c[b];if(e){var f=e.header_list;f[h+1]&&($(".next").attr("href",f[h+1][1]).removeAttr("disabled"),d=!0)}}}).attr("src",k)}if(g&&f&&f.length>0){for(var l="",m=1;h-m>=0;){if(f[h-m]){$(".prev").attr("href",f[h-m][1]).removeAttr("disabled"),d=!0;break}m++}for(m=1;h+m<f.length;){if(f[h+m]){$(".next").attr("href",f[h+m][1]).removeAttr("disabled"),d=!0;break}m++}$("#has_been_removed").length&&(f[h]="",a.setItem("searches",JSON.stringify(c)));var n=100*Math.floor(h/100)||"",o="http://"+b;o=o.replace(/index.html/,"index"+n+".html").replace(/index.html/,"").replace(/([&?]s=)0/,"$1"+n),$(".backup").attr("href",o).removeAttr("disabled"),l+="</div>",$(".next").click(function(){a.setItem("srch",b),a.setItem("dir","fwd")}),$(".prev").click(function(){a.setItem("srch",b),a.setItem("dir","bak")})}}}}catch(p){}d&&$(".prevnext a").show()});var a,b=$(".returnemail"),c=$(".reply_button"),d=$(".reply_options"),e=$(".flaglink"),f=$(".bestoflink");CL.page.isMobile&&$(".mapbox").insertAfter("#postingbody"),window.pID&&(e.on("click",function(a){a.preventDefault(),$(".flag").addClass("active"),$.get("/flag/?async=async&flagCode="+$(this).data("flag")+"&postingID="+window.pID).done(function(a){$(".flags").addClass("done"),e.find(".flagtext").text(a),e.contents().unwrap()})}),f.on("click",function(a){a.preventDefault(),$(".bestof").addClass("done"),$.get("/flag/?async=async&flagCode="+$(this).data("flag")+"&postingID="+window.pID).done(function(){f.contents().unwrap()})}));var g=$("section.body").innerWidth();$(window).on("resize",function(){window.innerWidth<g&&window.innerWidth>0&&($("#postingbody").css("width",window.innerWidth-16),$("aside.tsb").css("width",window.innerWidth-32))}).trigger("resize");var h=$("time");h.timeago().on("click",function(){h.each(function(){var a=$(this),b=a.text();a.text(a.attr("title")).attr("title",b).toggleClass("abs")})}),!window.bestOf&&c.length&&(b.show(),c.on("click",function(){b.load($("#replylink").attr("href"),"",function(e,f,g){404===g.status?CL.util.reload():d.length?(b.toggle(),a.trigger("select")):(d=$(".reply_options"),d.find("a").add("html").on("click",function(){b.hide()}),d.add(c).on("click",function(a){a.stopPropagation()}),d.add(b).show(),a=$(".anonemail"),a.on("mouseup",function(a){a.preventDefault()}),a.trigger("select"))})})),$(".showcontact").on("click",function(a){a.preventDefault(),$("#postingbody").load($(this).attr("href"),function(a,b,c){404===c.status&&CL.util.reload()})}),function(){var a=new Date,b=new Date(a.getFullYear(),a.getMonth(),a.getDate()),c=b.getMonth()+1;c=10>c?"0"+c:c;var d=b.getDate();d=10>d?"0"+d:d,$(".property_date").each(function(){var a=$(this);a.attr("date")<=b.getFullYear()+"-"+c+"-"+d&&a.addClass("attr_is_today").text(a.attr("today_msg"))})}();var i=$(".carousel"),j=i.find(".tray"),k=j.find(".slide"),l=function(a){var b=$("<img>");return b.attr({title:window.imageText+" "+a,alt:window.imageText+" "+a})};if(CL.page.isMobile){var m=$(".iw"),n=m.find(".slidernav");window.imgList&&Object.keys(window.imgList).length>1&&(n.show(),i.removeClass("carousel").addClass("swipe"),j.removeClass("tray").addClass("swipe-wrap"),k.each(function(a,b){if($(b).on("click",function(a){a.preventDefault(),window.open($(this).find("img").attr("src"),"clImageWindow")}),0!==a){var c=$(b);c.append(l(a+1).attr({src:window.imgList[c.data("imgid")]}))}}),CL.swipe.makeGallery(m))}else{var o=$("#thumbs"),p="",q=function(a){var b=$(a.target).parent("a"),c=b.data("imgid");if(c!==p){p=c;var d=$("#image_"+c);d.data("isLoaded")||(d.data("isLoaded",!0),$("<img>").attr({src:window.imgList[p]}).hide().on("load",function(){$(this).scaleToFit(i).show()}).appendTo(d)),$("#thumbs img").removeClass("selected"),b.find("img").addClass("selected"),j.css({top:-d.position().top})}};k.show().each(function(a,b){var c,d=$(b);c=0===a?d.find("img"):l(a+1),c.one("load",function(){c.scaleToFit(i)})});var r=$(".tray .slide.first");r.data("isLoaded",!0);var s=r.find("img");s.length>0&&s[0].complete&&s.trigger("load"),o.on("mouseover","img",q).on("click","a",function(a){a.preventDefault()})}}}();
/* {"sources":{"postings-concat.js":"c15afd40dc6dcc33e18ec46799d45990"}} */
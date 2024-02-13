$(function(){
  var c = $('#coordinates'), aa = c.find('a'), url
  for( var i = 0; i < aa.length; i++ ){
    url = aa[i].href
    if( !/geohack/.test(url)  || /_globe:/.test(url) ) continue
    c.append('<br>').append(
      $('<a href="#">Показать географическую карту</a>')
       .attr( 'params', mw.util.getParamValue('params', url) )
       .click(openStreetMapToggle)
    )
    break
  }
})


function openStreetMapToggle() {
 var osm = $('#openstreetmap')
 if( osm.length > 0 )
   osm.toggle()
 else
   $('#contentSub').append(
     '<iframe id="openstreetmap" style="width:100%; height:350px; clear:both"'
     + 'src="http://toolserver.org/~kolossos/openlayers/kml-on-ol.php?lang=ru&uselang=ru'
     + '&params=' + $(this).attr('params')
     + '&title=' + mw.util.wikiUrlencode( mw.config.get('wgTitle') )
     + '" />'
   )
 return false
}
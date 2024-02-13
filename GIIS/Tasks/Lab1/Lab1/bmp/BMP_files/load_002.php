importMW=function(name){importScript('MediaWiki:'+name+'.js')}
importScript_=importScript
importScript=function(page,proj){if(!proj)importScript_(page)
else{if(proj.indexOf('.')==-1)proj+='.wikipedia.org'
importScriptURI('//'+proj+'/w/index.php?action=raw&ctype=text/javascript&title='+mw.util.wikiUrlencode(page))}}
mw.config.set('tableSorterCollation',{'ё':'е'})
var listFA={fa:'Эта статья является избранной',fl:'Этот список или портал является избранным',ga:'Эта статья является хорошей'}
var textFA=' в другом языковом разделе'
var zeroSectionTip='Править введение'
var NavigationBarHide='[скрыть]'
var NavigationBarShow='[показать]'
var NavigationBarShowDefault=2
if(/^en$/.test(wgUserLanguage))importMW('Common-'+wgUserLanguage)
function LinkFA(){var ll,s
$('#p-lang li').each(function(i,iw){ll=iw.className.split(' ')[0]+'-'
for(var s in listFA)if(document.getElementById(ll+s))$(iw).addClass(s.toUpperCase()).attr('title',listFA[s]+textFA)})}function editZeroSection(){if(!wgArticleId)return
mw.util.$content.find('h2').children('span.editsection').first().clone().prependTo(mw.util.$content).css('float','right').find('a').attr('title',zeroSectionTip).attr('href',wgScript+'?title='+mw.util.wikiUrlencode(wgPageName)+'&action=edit&section=0')}var hasClass=(function(){var reCache={}
return function(element,className){return(reCache[className]?reCache[className]:(reCache[className]=new RegExp("(?:\\s|^)"+className+"(?:\\s|$)"))).test(element.className)}})()
function collapsibleTables(){var Table,HRow,HCell,btn,a,tblIdx=0,colTables=[]
var allTables=document.getElementsByTagName('table')
for(var i=0;Table=allTables[i];i++){if(!hasClass(Table,'collapsible'))continue
if(!(HRow=Table.rows[0]))continue
if(!(HCell=HRow.getElementsByTagName('th')[0]))continue
Table.id='collapsibleTable'+tblIdx
btn=document.createElement('span')
btn.style.cssText='float:right; font-weight:normal; font-size:smaller'
a=document.createElement('a')
a.id='collapseButton'+tblIdx
a.href='javascript:collapseTable('+tblIdx+');'
a.style.color=HCell.style.color
a.appendChild(document.createTextNode(NavigationBarHide))
btn.appendChild(a)
HCell.insertBefore(btn,HCell.childNodes[0])
colTables[tblIdx++]=Table}for(var i=0;i<tblIdx;i++)if((tblIdx>NavigationBarShowDefault&&hasClass(colTables[i],'autocollapse'))||hasClass(colTables[i],'collapsed'))collapseTable(i)}function collapseTable(idx){var Table=document.getElementById('collapsibleTable'+idx)
var btn=document.getElementById('collapseButton'+idx)
if(!Table||!btn)return false
var Rows=Table.rows
var isShown=(btn.firstChild.data==NavigationBarHide)
btn.firstChild.data=isShown?NavigationBarShow:NavigationBarHide
var disp=isShown?'none':Rows[0].style.display
for(var i=1;i<Rows.length;i++)Rows[i].style.display=disp}function collapsibleDivs(){var navIdx=0,colNavs=[],i,NavFrame
var divs=document.getElementById('content').getElementsByTagName('div')
for(i=0;NavFrame=divs[i];i++){if(!hasClass(NavFrame,'NavFrame'))continue
NavFrame.id='NavFrame'+navIdx
var a=document.createElement('a')
a.className='NavToggle'
a.id='NavToggle'+navIdx
a.href='javascript:collapseDiv('+navIdx+');'
a.appendChild(document.createTextNode(NavigationBarHide))
for(var j=0;j<NavFrame.childNodes.length;j++)if(hasClass(NavFrame.childNodes[j],'NavHead'))NavFrame.childNodes[j].appendChild(a)
colNavs[navIdx++]=NavFrame}for(i=0;i<navIdx;i++)if((navIdx>NavigationBarShowDefault&&!hasClass(colNavs[i],'expanded'))||hasClass(colNavs[i],'collapsed'))collapseDiv(i)}function collapseDiv(idx){var div=document.getElementById('NavFrame'+idx)
var btn=document.getElementById('NavToggle'+idx)
if(!div||!btn)return false
var isShown=(btn.firstChild.data==NavigationBarHide)
btn.firstChild.data=isShown?NavigationBarShow:NavigationBarHide
var disp=isShown?'none':'block'
for(var child=div.firstChild;child!=null;child=child.nextSibling)if(hasClass(child,'NavPic')||hasClass(child,'NavContent'))child.style.display=disp}mw.loader.using('mediawiki.util',function(){if(wgCanonicalNamespace=='Special'){if(/^(Uplo|Sear|Stat|Spec|Abus|Prefe|Move|Watch|Newp|Log)/i.test(wgCanonicalSpecialPageName))importMW(wgCanonicalSpecialPageName)}else switch(wgAction){case'history':importMW('History');break
case'delete':importMW('Deletepage');break
case'edit':case'submit':importMW('Editpage')
default:$(editZeroSection)
addOnloadHook(collapsibleDivs)
addOnloadHook(collapsibleTables)
mw.loader.load('//meta.wikimedia.org/w/index.php?title=MediaWiki:Wikiminiatlas.js&action=raw&ctype=text/javascript&smaxage=21600&maxage=86400')
if(document.location&&document.location.protocol=='https:')importMW('Secure')
if(navigator.platform.indexOf('Win')!=-1)mw.util.addCSS('.IPA, .Unicode { font-family: "Arial Unicode MS", "Lucida Sans Unicode"; }')
switch(wgNamespaceNumber){case 0:case 100:$(LinkFA)
importMW('Osm')
if(wgArticleId==4401)importMW('Mainpage')
break
case 6:importMW('Filepage')
break}}if(!wgUserName)mw.util.addCSS('#mw-fr-revisiontag {display:none}')
if($.client.profile().name=='msie'){if($.client.profile().versionBase=='8'){$('.hlist').find('dd:last-child, dt:last-child, li:last-child').addClass('hlist-last-child');}if($.client.profile().versionBase<'8'){$('.hlist').find('dt + dd, dt + dt').prev().append('<b>:</b> ');$('.hlist').find('dd + dd, dd + dt, li + li').prev().append('<b>•</b> ');$('.hlist').find('dl dl, ol ol, ul ul').prepend('( ').append(') ');}}if(wgArticleId!=639373&&wgArticleId!=932117&&wgArticleId!=1297302&&wgArticleId!=25133866)importMW('Wikibugs')
if(!wgUserName||(wgUserName&&(((typeof wgLangPrefs=='undefined')?false:true)||((typeof wgAddLangHints=='undefined')?false:wgAddLangHints)||((typeof wgUseUserLanguage=='undefined')?false:wgUseUserLanguage))))importMW('Interwiki-links');})
var withJS=document.URL.match(/[&?]withjs=((mediawiki:)?([^&#]+))/i)
if(withJS)importScript_('MediaWiki:'+withJS[3])
var execJS=document.getElementById('executeJS')
if(execJS)$.each(execJS.className.split(' '),function(i,sc){sc=$.trim(sc.replace(/[^\w ]/g,''))
if(sc)importMW('Script/'+sc)})
$('#searchform').bind('keyup keydown mousedown',function(e){$(this).attr('target',e.shiftKey?'_blank':'')})
if(wgNamespaceNumber&&wgAction=='view')$('#ca-addsection a').clone().css({'float':'right','font-size':'0.8em',padding:'4px',background:'#f2f7fb',border:'1px outset #1ED8FC','border-top-style':'none'}).insertAfter('#content');mw.loader.state({"site":"ready"});

/* cache key: ruwiki:resourceloader:filter:minify-js:7:b65515beda06f402567ec4484ed2bf52 */

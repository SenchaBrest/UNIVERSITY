/*
; Источник: http://pl.wikipedia.org/wiki/MediaWiki:Wikibugs.js
; Адаптация под русский: [[User:Александр Сигачёв]], [[User:Putnik]], [[User:LEMeZza]]
;
; Идея, текст на польском: [[:pl:User:Dodek]], [[:pl:User:Adziura]]
; Реализация: [[:pl:User:Nux]], [[:pl:User:Saper]], [[:pl:User:Beau]], [[User:Putnik]]
*/

var wb$description = "Пожалуйста, опишите ошибку как можно точнее. По возможности, укажите ваш источник информации."
var wb$badPages = new Array(
  "Википедия:Сообщения об ошибках",
  "Заглавная страница"
)
 
addOnloadHook(function()
{
  var el = document.getElementById('n-bug_in_article')
 
  if (el)
    el.getElementsByTagName('a')[0].onclick= wb$popWikibug
})
 
function wb$popWikibug()
{
  var link_wiki = window.wgArticlePath.replace(/\$1/, 'вики')
  var link_tocreate = window.wgArticlePath.replace(/\$1/, 'Википедия:К_созданию')
  var link_bebold = window.wgArticlePath.replace(/\$1/, 'Википедия:Правьте_смело')
  var link_buglist = window.wgArticlePath.replace(/\$1/, 'Википедия:Сообщения_об_ошибках')
 
  wb$popBugBoth("Википедия:Сообщения об ошибках", '\
    <div style="float:right;width:200px;padding:4px 10px;margin:2px 0px 0px 10px;font-size:90%;border:2px solid #900"><p><strong>Не\u00A0сообщайте</strong> об\u00A0ошибках на\u00A0других сайтах (например, <strong>«В\u00A0Контакте»</strong> или <strong>«Одноклассники»</strong>), они будут проигнорированы.</p>\
    <p>Отсутствие статьи в\u00A0Википедии\u00A0— не\u00A0ошибка, вы можете оставить <a href="' + link_tocreate + '">запрос на её создание</a>.</p></div>\
    <p style="margin-top:0px">Если вы заметили ошибку в\u00A0Википедии, пожалуйста, исправьте её самостоятельно, используемая на\u00A0этом сайте технология <a href="' + link_wiki + '">вики</a> позволяет это сделать. Не\u00A0смущайтесь, одно из\u00A0правил Википедии гласит: «<a href="' + link_bebold + '">Правьте смело</a>»! Если вы не\u00A0можете исправить ошибку самостоятельно, сообщите о\u00A0ней с\u00A0помощью данной формы.</p><p><strong>Если ошибка уже исправлена\u00A0— не\u00A0сообщайте о\u00A0ней.</strong></p><p>Не\u00A0оставляйте свой телефон и/или электронный адрес, ответ на\u00A0сообщение будет дан только на\u00A0странице с\u00A0сообщениями и нигде больше.</p>\
    <ul><li><a href="' + link_buglist + '">Текущий список сообщений об ошибках.</a></li></ul>\
    ')
  return false
}
 
function wb$getEditToken(page)
{
  var objhttp = (window.XMLHttpRequest) ? new XMLHttpRequest(): new ActiveXObject('Microsoft.XMLHTTP')
  if (!objhttp)
    return
  objhttp.onreadystatechange=function() {
    if (objhttp.readyState == 4) {
      if (objhttp.status == 200) {
        var r_sti = /value="(\d+)" name=["']wpStarttime["']/
        var r_eti = /value="(\d+)" name=["']wpEdittime["']/
        var r_etk = /value="(.*?)" name=["']wpEditToken["']/
        var r_asm = /name="wpAutoSummary" type="hidden" value="(.*?)"/
        sti = r_sti.exec(objhttp.responseText)
        eri = r_eti.exec(objhttp.responseText)
        etk = r_etk.exec(objhttp.responseText)
        asm = r_asm.exec(objhttp.responseText)
        document.getElementById('Starttime').value=sti[1]
        document.getElementById('Edittime').value=eri[1]
        document.getElementById('EditToken').value=etk[1]
        document.getElementById('AutoSummary').value=asm[1]
      }
      else
        alert(objhttp.status)
    }
  }
  objhttp.open("GET", wgServer+wgScript+"?title="+encodeURIComponent(page)+"&action=edit")
  objhttp.send("")
}
 
function wb$isValidPageName(name)
{
  if (name == "")
    return false
  if (name.substr(0, 10) == "Служебная:")
    return false
  name = name.replace(/_/g, " ")
  for (var i = 0; i < wb$badPages.length; i++)
    if (name == wb$badPages[i])
      return false
 
  return true
}
 
function wb$checkForm(form)
{
  var page = form.wpSummary.value
  var content = form.wpTextbox1.value

  if (content=="" || content==wb$description || content.length<20 || !content.match(' ')) {
    alert("Описание ошибки слишком коротко. Пожалуйста, расширьте его.")
    form.wpTextbox1.focus()
    return false
  }
 
  page = page.replace(/^https?:\/\/ru\.wikipedia\.org\/wiki\/(.+)$/, "$1")
  page = page.replace(/_/g, " ")
  page = decodeURIComponent(page)
 
  if (page == wgPageName.replace(/_/g, " ") && wb$isValidPageName(wgPageName)) {
    if (wgNamespaceNumber == 6) {
      page = "[[:Файл:"+wgTitle+"|"+wgTitle+"]]"
      content = "[[Файл:"+wgTitle+"|thumb|left|100px]]\n* "+content+"\r\n{{clear}}"
    }
    else {
      page = page.replace(/^(Категория:|Файл:|\/)/, ":$1")
      page = "[["+page+"]]"
    }
  }
  else {
    page = page.replace(/\[\[([^\[\]\|]+)\|[^\[\]\|]+\]\]/g, "$1")
    page = page.replace(/[\[\]\|]/g, "")
    page = page.replace(/^\s+/g, "")
    page = page.replace(/\s+$/g, "")
 
    if (! wb$isValidPageName(page) ) {
      alert("Введите имя страницы.")
      if ( wb$isValidPageName(wgPageName) )
        form.wpSummary.value = wgPageName
      else {
        form.wpSummary.value = ""
        form.wpSummary.focus()
      }
      return false
    }
    if (page.indexOf(':') > 0)
      page = '[[:'+page+']]'
    else
      page = '[['+page+']]'
  }
 
  form.submit.disabled = 'disabled'
 
  if (wgUserName != null) 
    content += '\r\n\r\nАвтор сообщения: ~~'+'~~'
  else
    content += '\r\n\r\nАвтор сообщения: '+form.author.value+' ~~'+'~~'
 
  form.wpTextbox1.value = content
  form.wpSummary.value = page
 
  return true
}
 
function wb$goToEditPage()
{
  var edit_el = document.getElementById('ca-edit')
  var edit_href = window.wgArticlePath.replace(/\$1/, 'Википедия:Сообщения_об_ошибках')
  if (edit_el)
    edit_href = edit_el.getElementsByTagName('a')[0].href
  window.location.assign(edit_href)
}
 
function wb$popBugBoth(action_page, infoHTML)
{
  var glob = document.body
 
  // затемнение
  var nel = document.createElement('div')
  nel.id='specpop-globhidden'
  nel.style.cssText = 'background:white;filter:alpha(opacity=75);opacity:0.75;position:absolute;left:0px;top:0px;z-index:2000'
  nel.style.width = document.documentElement.scrollWidth+'px'
  nel.style.height= document.documentElement.scrollHeight+'px'
  glob.appendChild(nel)
 
  // перемещение окна
  window.scroll(0, 150)
 
  // информация
  var edit_el = document.getElementById('ca-edit')
  if (edit_el)
    var can_edit = true
  else
    var can_edit = false
 
  nel = document.createElement('div')
  nel.id='specpop-info'
  nel.style.cssText = 'font-size:13px;background:white;padding:21px 30px;border:1px solid black;position:absolute;width:500px;min-height:300px;top:200px;z-index:2002'
  if (nel.style.maxHeight==undefined)
    nel.style.height='300px' // IE blah
  var tmp = Math.floor(glob.clientWidth/2)-300
  if (tmp<5)
    tmp = 5
  nel.style.left = tmp+'px'
 
  nel.innerHTML	= infoHTML
  if (window.wgUserName == null)
    nel.innerHTML = nel.innerHTML + '<p><strong>Внимание.</strong> Ваш IP-адрес будет записан в журнал изменений страницы.</p>'
  nel.innerHTML	= nel.innerHTML + '<p style="text-align:center;margin-top:15px">\
    '+(can_edit ? '<input type="button" value="Исправить самостоятельно" onclick="wb$goToEditPage()" />' : '')+ '\
    <input type="button" value="Сообщить об ошибке" onclick="wb$elementsRemove(\'specpop-info\')" />&nbsp;&nbsp;&nbsp;\
    <input type="button" value="Отмена" onclick="wb$elementsRemove(\'specpop-info\',\'specpop-form\',\'specpop-globhidden\',\'specpop-pos\')" />\
    </p>'
  glob.appendChild(nel)
 
  var action_url = window.wgServer + window.wgScript + "?title=" +encodeURIComponent(action_page)  + "&action=submit"
 
  // форма
  nel = document.createElement('div')
  nel.id = 'specpop-form'
  nel.style.cssText = 'background:white;padding:5px 10px;border:1px solid black;position:absolute;width:330px;min-height:300px;top:200px;z-index:2001'
  if (nel.style.maxHeight==undefined)
    nel.style.height='300px' // IE blah
  nel.style.left = (Math.floor(glob.clientWidth/2)-165)+'px'
  //nel.style.top = (this.offsetTop-100)+'px'
  nel.innerHTML	= '<form id="fm1" action="'+action_url+'" method="post" enctype="multipart/form-data" onsubmit="return wb$checkForm(this)">\
    Название страницы:<br /><input type="text" name="wpSummary" id="wpSummary" style="width:320px" /><br />\
    <input type="hidden" name="wpSection" value="new" />\
    <input type="hidden" name="wpSave" value="Записать" />\
    <input type="hidden" id="Starttime" name="wpStarttime" value="" />\
    <input type="hidden" id="Edittime" name="wpEdittime" value="" />\
    <input type="hidden" id="EditToken" name="wpEditToken" value="" />\
    <input type="hidden" id="AutoSummary" name="wpAutoSummary" value="" />\
    <input type="hidden" name="wpScrolltop" value="0" />\
    Текст сообщения:<br /><textarea id="TextBox" name="wpTextbox1" style="width:320px;height:200px" onfocus="if (this.value == wb$description) {this.value = \'\'}">' + wb$description + '</textarea><br />\
    Подпись:<input type="text" name="author" id="wikibug-input-author" /><br />\
    <input type="submit" id="submit" value="Отправить" /> &nbsp; \
    <input type="button" value="Отмена" onclick="wb$elementsRemove(\'specpop-form\',\'specpop-globhidden\',\'specpop-pos\')" />\
    </form>'
  glob.appendChild(nel)
  if (wb$isValidPageName(wgPageName))
    document.getElementById('wpSummary').value = wgPageName.replace(/_/g, " ")
 
  if (wgUserName != null) {
    var author = document.getElementById("wikibug-input-author")
    author.value = '~~'+'~~'
    author.disabled = 'disabled'
  }
  wb$getEditToken(action_page)
}
 
function wb$elementsRemove()
{
  var el
  for (var i=arguments.length-1; i>=0; i--) {
    el = document.getElementById(arguments[i])
    if (el)
      el.parentNode.removeChild(el)
  }
}
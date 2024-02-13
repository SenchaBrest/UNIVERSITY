/** Sort iw-links according to a preference table ****************************************************** 
 *
 *  First revision was imported from http://no.wikipedia.org/wiki/MediaWiki:Interwiki-links.js
 *  Original description [[:no:Wikipedia:Sortering av interwiki-lenker]]
 *
 */

appendCSS('.iw-focus {font-weight: bold} .iw-babel {font-style: italic}')

var wgDebugIWlang;
var wgUseUserlanguage;
var wgAddLangHints;
var wgInterwikiDone = false;
var wgDefaultLangPrefs = [];
 
// make sure we in fact has a array
var wgLangPrefs;
if (typeof wgLangPrefs == 'undefined') wgLangPrefs = Array();
wgLangPrefs.push(wgUserLanguage);
 
// choose and adjust lists for prefered languages
if (wgUserName) {
    wgLangPrefs = wgLangPrefs;
}
else {
    wgLangPrefs = wgDefaultLangPrefs;
}
var wgLangIWlinks = Object();
for (i=0;i<wgLangPrefs.length;i++) {
    wgLangPrefs[wgLangPrefs[i]] = 1;
    wgLangIWlinks["interwiki-" + wgLangPrefs[i]] = 1;
}
 
// get data structures for nameing and sorting of languages
// this will block any languages that isn't defined
var wgLanguages = { 'nn' : true, 'no' : true, 'ru' : true };
if ( wgUserName == null ? wgUserLanguage != wgContentLanguage : true ) {
    if ( wgLanguages[ wgUserLanguage ] )
        importScript('MediaWiki:User-lang-' + wgUserLanguage + '.js');
}
var wgLangNames;
if ( typeof wgLangNames != 'object' ) wgLangNames = Object();
 
 
function sortIWlinks(a,b)
{
   try {
      return wgLangNames[ wgUserLanguage ][ a.className.split(' ')[0] ][ 1 ] - wgLangNames[ wgUserLanguage ][ b.className.split(' ')[0] ][ 1 ];
    }
    catch (e) {
        /* just skip this if its happens to fail, but then the link might be placed a bit random */
    }

}
 
addOnloadHook( function () {

    if (wgInterwikiDone) return;
    wgInterwikiDone = true;
    if ( typeof wgDebugIWlang != 'undefined' && wgDebugIWlang ) return; // bail out for debugging
 
    // reorganize wgLangNames so we can use it for sorting
    var j = 0;
    var ta = Array();
    for (x in wgLangNames[ wgUserLanguage ]) {
        ta.push(x);
    }
    for (i=0;i<ta.length;i++) {
        wgLangNames[ wgUserLanguage ][ 'interwiki-' + ta[i] ] = [ wgLangNames[ wgUserLanguage ][ ta[i] ], j ];
        wgLangNames[ wgUserLanguage ][ ta[i] ] = [ wgLangNames[ wgUserLanguage ][ ta[i] ], j ];
        j++
    }
 
    // if we don't have anything from wgLangNames we give up
    if (!j) return;
 
    // locate iw-links, and the container
    var container = document.getElementById("p-lang");
    if (!container) return;
    var ul = container.getElementsByTagName("ul");
    if (!ul) return;
    if (ul.length != 1) return;
    ul = ul[0];
    var c = container.getElementsByTagName("li");
    if (!c) return;
 
    // loop over the iw-links, translate names and
    // separate those we know how to sort from the rest
    // and add babel links
    var childs = Array();
    var keeps = Array();
    var adds = Array();
    for (i=0;i<c.length;i++) {
        if (wgLangNames) {
            var s = c[ i ].className.split(' ')[0];
            if (0>s.indexOf('interwiki-')) continue;
            s = s.replace(/^.*?interwiki-/, '');
            s = s.replace(/\s.*$/, '');
            var a = c[ i ].getElementsByTagName("a");

            // localize language names
            try {
                if ( typeof wgUseUserLanguage != 'undefined' && wgUseUserLanguage
                     && typeof wgLangNames[ wgUserLanguage ] != 'undefined' ) {
                    if ( typeof wgLangNames[ wgUserLanguage ][ s ] != 'undefined'
                         && typeof wgLangNames[ wgUserLanguage ][ s ][ 0 ] == 'string' ) {
                        if (a.length){
                            a[0].innerHTML = wgLangNames[ wgUserLanguage ][ s ][ 0 ];
                            a[0].lang = 'ru';
                        }  
                    }
                }
            }
            catch (e) { /* just skip this */ }
            
            // add hints for language names
            try {
                if ( typeof wgAddLangHints != 'undefined' && wgAddLangHints
                     && typeof wgLangNames[ wgUserLanguage ] != 'undefined' ) {
                    if ( typeof wgLangNames[ wgUserLanguage ][ s ] != 'undefined'
                         && typeof wgLangNames[ wgUserLanguage ][ s ][ 0 ] == 'string' ) {
                        //c[ i ].setAttribute( 'title', wgLangNames[ wgUserLanguage ][ s ][ 0 ] );
                        a[0].setAttribute( 'title', wgLangNames[ wgUserLanguage ][ s ][ 0 ] + ' — ' + decodeURIComponent(a[0].getAttribute('href').replace(/^.*?\/wiki\/(.*)$/, '$1')).replace(/_/g, ' '));
                    }
                }
            }            
            catch (e) { /* just skip this */ }
            
            
            // check if we have any odd link}
            try {
                if ( typeof wgUseUserLanguage != 'undefined' && wgUseUserLanguage
                     && typeof wgLangNames[ wgUserLanguage ][ s ] != 'undefined'
                     && typeof wgLangNames[ wgUserLanguage ][ s ][ 1 ] == 'number' ) {
                    childs.push(c[ i ]);
                    //wgLangNames[ c[ i ].className ] = wgLangNames[ wgUserLanguage ][ s ];
                }
                else {
	              adds.push(c[ i ]);
                }
            }
            catch (e) { /* just skip this */ }
        }
        else {
	      childs.push(c[ i ]);
        }
    }
 
    // sort the childs according to definitions used by sortIWlinks
    if ( typeof wgUseUserLanguage != 'undefined' && wgUseUserLanguage
         && typeof wgLangNames[ wgUserLanguage ] != 'undefined' ) {
        childs = childs.sort(sortIWlinks);
    }
 
    // reinsert those we didn't know how to sort into the list of children
    for (i=0;i<adds.length;i++) {
	      childs.push(adds[ i ]);
    }
 
    // move one block to the top
    try {
        // separate out those that shall be moved to the top
        for (i=0;i<childs.length;i++) {
            // the following test fails if there are several classes for the actual child
            if ( typeof wgLangIWlinks[ childs[i].className.split(' ')[0] ] != 'undefined' && wgLangIWlinks[ childs[i].className.split(' ')[0] ]) {
                keeps.push(childs[i]);
            }
        }
 
        // reorganize the list of children
        var n = childs.length;
        for (i=childs.length-1;i>=0;i--) {
            if ( typeof wgLangIWlinks[ childs[i].className.split(' ')[0] ] != 'undefined' && wgLangIWlinks[ childs[i].className.split(' ')[0] ] ) {
                childs[i].className += ' iw-focus';
            }
            else {
                keeps[--n] = childs[i];
            }
        }
    }
    catch (e) { /* just skip this */ }
 
    // remove all existing children and reinsert from our own list
    if (keeps.length) {
        var child;
        while (child = ul.firstChild) {
            ul.removeChild(child);
        }
        for (i=0;i<keeps.length;i++) {
            ul.appendChild(keeps[i]);
        }
    }
    // }
    // catch (e) { /* just skip this */ }
});
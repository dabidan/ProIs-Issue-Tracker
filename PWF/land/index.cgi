<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
                      "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
  <head>
    <title>Bugzilla Main Page</title>

      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">


<link rel="Top" href="http://localhost:5080/">

  


  


  
    <link rel="Saved&nbsp;Searches" title="My Bugs"
          href="buglist.cgi?resolution=---&amp;emailassigned_to1=1&amp;emailreporter1=1&amp;emailtype1=exact&amp;email1=dabi%40blazemail.com">


   <link rel="Administration" title="Parameters"    
                  href="editparams.cgi"><link rel="Administration" title="Users"    
                  href="editusers.cgi"><link rel="Administration" title="Products" href="editproducts.cgi"><link rel="Administration" title="Flag Types"   
                  href="editflagtypes.cgi"><link rel="Administration" title="Groups"        
                  href="editgroups.cgi"><link rel="Administration" title="Keywords"      
                  href="editkeywords.cgi"><link rel="Administration" title="Whining"       
                  href="editwhines.cgi"><link rel="Administration" title="Sanity Check"  
                  href="sanitycheck.cgi">



    
    
    <link href="skins/standard/global.css?1328889968"
          rel="alternate stylesheet" 
          title="Classic"><link href="skins/standard/global.css?1328889968" rel="stylesheet"
        type="text/css" ><link href="skins/standard/index.css?1328889968" rel="stylesheet"
        type="text/css" ><!--[if lte IE 7]>
      



  <link href="skins/standard/IE-fixes.css?1328889968" rel="stylesheet"
        type="text/css" >
<![endif]-->

    <link href="skins/contrib/Dusk/global.css?1328889968" rel="stylesheet"
        type="text/css" title="Dusk"><link href="skins/contrib/Dusk/index.css?1328889968" rel="stylesheet"
        type="text/css" title="Dusk">


    

    

    
<script type="text/javascript" src="js/yui/yahoo-dom-event/yahoo-dom-event.js?1328889968"></script><script type="text/javascript" src="js/yui/cookie/cookie-min.js?1328889968"></script><script type="text/javascript" src="js/global.js?1328889968"></script>

    <script type="text/javascript">
    <!--
        YAHOO.namespace('bugzilla');
        YAHOO.util.Event.addListener = function (el, sType, fn, obj, overrideContext) {
               if ( ("onpagehide" in window || YAHOO.env.ua.gecko) && sType === "unload") { sType = "pagehide"; };
               var capture = ((sType == "focusin" || sType == "focusout") && !YAHOO.env.ua.ie) ? true : false;
               return this._addListener(el, this._getType(sType), fn, obj, overrideContext, capture);
         };
        if ( "onpagehide" in window || YAHOO.env.ua.gecko) {
            YAHOO.util.Event._simpleRemove(window, "unload", 
                                           YAHOO.util.Event._unload);
        }
        
        function unhide_language_selector() { 
            YAHOO.util.Dom.removeClass(
                'lang_links_container', 'bz_default_hidden'
            ); 
        } 
        YAHOO.util.Event.onDOMReady(unhide_language_selector);

        
        var BUGZILLA = {
            param: {
                cookiepath: '\/4AG7aCX8My\/',
                maxusermatches: 1000
            },
            constant: {
                COMMENT_COLS: 80
            },
            string: {
                

                attach_desc_required:
                    'You must enter a Description for this attachment.',
                component_required:
                    'You must select a Component for this bug.',
                description_required:
                    'You must enter a Description for this bug.',
                short_desc_required:
                    'You must enter a Summary for this bug.',
                version_required:
                    'You must select a Version for this bug.'
            }
        };

    // -->
    </script>


    

    
    <link rel="search" type="application/opensearchdescription+xml"
                       title="Bugzilla" href="./search_plugin.cgi">
    <link rel="shortcut icon" href="images/favicon.ico" >
  </head>



  <body onload=""
        class="landfill-bugzilla-org-4AG7aCX8My yui-skin-sam">



<div id="header">
<div id="banner">
  </div>

<table border="0" cellspacing="0" cellpadding="0" id="titles">
<tr>
    <td id="title">
      <p>Bugzilla &ndash; Main Page</p>
    </td>


    <td id="information">
      <p class="header_addl_info">version 4.2rc2+</p>
    </td>
</tr>
</table>

<table id="lang_links_container" cellpadding="0" cellspacing="0"
       class="bz_default_hidden"><tr><td>
</td></tr></table>
<ul class="links">
  <li><a href="./">Home</a></li>
  <li><span class="separator">| </span><a href="enter_bug.cgi">New</a></li>
  <li><span class="separator">| </span><a href="describecomponents.cgi">Browse</a></li>
  <li><span class="separator">| </span><a href="query.cgi">Search</a></li>

  <li class="form">
    <span class="separator">| </span>
    <form action="buglist.cgi" method="get"
        onsubmit="if (this.quicksearch.value == '')
                  { alert('Please enter one or more search terms first.');
                    return false; } return true;">
    <input class="txt" type="text" id="quicksearch_top" name="quicksearch" 
           title="Quick Search" value="">
    <input class="btn" type="submit" value="Search" 
           id="find_top"></form>
  <a href="page.cgi?id=quicksearch.html" title="Quicksearch Help">[?]</a></li>

  <li><span class="separator">| </span><a href="report.cgi">Reports</a></li>

  <li>
      <span class="separator">| </span>
        <a href="request.cgi?requester=dabi%40blazemail.com&amp;requestee=dabi%40blazemail.com&amp;do_union=1&amp;group=type&amp;action=queue">My Requests</a></li>

    <li><span class="separator">| </span><a href="userprefs.cgi">Preferences</a></li>
      <li><span class="separator">| </span><a href="admin.cgi">Administration</a></li>


    <li>
      <span class="separator">| </span>
        <a href="index.cgi?logout=1">Log&nbsp;out</a>
        dabi&#64;blazemail.com</li>
</ul>
</div> 

<div id="bugzilla-body">


<script type="text/javascript">
<!--
function onLoadActions() {
  quicksearchHelpText('quicksearch_main', 'show');
  if( window.external.AddSearchProvider ){
    YAHOO.util.Dom.removeClass('quicksearch_plugin', 'bz_default_hidden');
  }
  document.getElementById('quicksearch_top').focus();
}
var quicksearch_message = "Enter a bug # or some search terms";

function checkQuicksearch( form ) {
  if (form.quicksearch.value == '' || form.quicksearch.value == quicksearch_message ) { 
    alert('Please enter one or more search terms first.');
    return false; 
  }
  return true;         
}

function quicksearchHelpText(el_id, action){
  var el = document.getElementById(el_id);
  if ( action == "show") {
    if( el.value == "" ) {
      el.value = quicksearch_message
      YAHOO.util.Dom.addClass(el, "quicksearch_help_text");
    }
  } else {
    if( el.value == quicksearch_message ) {
      el.value = "";
      YAHOO.util.Dom.removeClass(el, "quicksearch_help_text");
    }
  }
}
YAHOO.util.Event.onDOMReady(onLoadActions);
//-->
</script>


<div id="page-index">
  <table>
    <tr>
      <td>
        <h1 id="welcome"> Welcome to Bugzilla</h1>
        <div class="intro"></div>

        <div class="bz_common_actions">
          <ul>
            <li>
              <a id="enter_bug" href="enter_bug.cgi"><span>File a Bug</span></a>
            </li>
            <li>
              <a id="query" href="query.cgi"><span>Search</span></a>
            </li>
            <li>
              <a id="account"
                   href="userprefs.cgi"><span>User Preferences</span></a>
            </li>
          </ul>
        </div>

        <form id="quicksearchForm" name="quicksearchForm" action="buglist.cgi"
              onsubmit="return checkQuicksearch(this);">
          <div>
            <input id="quicksearch_main" type="text" name="quicksearch"
              title="Quick Search" 
              onfocus="quicksearchHelpText(this.id, 'hide');"
              onblur="quicksearchHelpText(this.id, 'show');"
            >
            <input id="find" type="submit" value="Quick Search">
            <ul class="additional_links" id="quicksearch_links">
              <li>
                <a href="page.cgi?id=quicksearch.html">Quick Search help</a>
              </li>
              <li class="bz_default_hidden" id="quicksearch_plugin">
                |
                <a href="javascript:window.external.AddSearchProvider('http://localhost:5080/search_plugin.cgi')">
                 Install the Quick Search plugin
                </a>
              </li>
            </ul>
            <ul class="additional_links">
              <li>
                <a href="docs/en/html/using.html">Bugzilla User's Guide</a>
              </li>
              <li>
                |
                <a href="page.cgi?id=release-notes.html">Release Notes</a>
              </li>
            </ul>
          </div>
        </form>
        <div class="outro"></div>
      </td>
    </tr>
  </table>
</div>
</div>



<div id="footer">
  <div class="intro"></div>




<ul id="useful-links">
  <li id="links-actions"><ul class="links">
  <li><a href="./">Home</a></li>
  <li><span class="separator">| </span><a href="enter_bug.cgi">New</a></li>
  <li><span class="separator">| </span><a href="describecomponents.cgi">Browse</a></li>
  <li><span class="separator">| </span><a href="query.cgi">Search</a></li>

  <li class="form">
    <span class="separator">| </span>
    <form action="buglist.cgi" method="get"
        onsubmit="if (this.quicksearch.value == '')
                  { alert('Please enter one or more search terms first.');
                    return false; } return true;">
    <input class="txt" type="text" id="quicksearch_bottom" name="quicksearch" 
           title="Quick Search" value="">
    <input class="btn" type="submit" value="Search" 
           id="find_bottom"></form>
  <a href="page.cgi?id=quicksearch.html" title="Quicksearch Help">[?]</a></li>

  <li><span class="separator">| </span><a href="report.cgi">Reports</a></li>

  <li>
      <span class="separator">| </span>
        <a href="request.cgi?requester=dabi%40blazemail.com&amp;requestee=dabi%40blazemail.com&amp;do_union=1&amp;group=type&amp;action=queue">My Requests</a></li>

    <li><span class="separator">| </span><a href="userprefs.cgi">Preferences</a></li>
      <li><span class="separator">| </span><a href="admin.cgi">Administration</a></li>


    <li>
      <span class="separator">| </span>
        <a href="index.cgi?logout=1">Log&nbsp;out</a>
        dabi&#64;blazemail.com</li>
</ul>
  </li>

  
    
    <li id="links-saved">
      <ul class="links">
          <li><a href="buglist.cgi?resolution=---&amp;emailassigned_to1=1&amp;emailreporter1=1&amp;emailtype1=exact&amp;email1=dabi%40blazemail.com">My Bugs</a></li>

      </ul>
    </li>

  
<li id="links-special">
    <script type="text/javascript">
      <!--
      function update_text() {
        // 'lob' means list_of_bugs.
        var lob_action = document.getElementById('lob_action');
        var action = lob_action.options[lob_action.selectedIndex].value;
        var text = document.getElementById('lob_direction');
        var new_query_text = document.getElementById('lob_new_query_text');

        if (action == "add") {
          text.innerHTML = "to";
          new_query_text.style.display = 'inline';
        }
        else {
          text.innerHTML = "from";
          new_query_text.style.display = 'none';
        }
      }

      function manage_old_lists() {
        var old_lists = document.getElementById('lob_oldqueryname');
        // If there is no saved searches available, returns.
        if (!old_lists) return;

        var new_query = document.getElementById('lob_newqueryname').value;

        if (new_query != "") {
          old_lists.disabled = true;
        }
        else {
          old_lists.disabled = false;
        }
      }
      //-->
    </script>

    <div class="label"></div>
    <ul class="links"><li class="form">
      <form id="list_of_bugs" action="buglist.cgi" method="get">
        <input type="hidden" name="cmdtype" value="doit">
        <input type="hidden" name="remtype" value="asnamed">
        <input type="hidden" name="list_of_bugs" value="1">
        <input type="hidden" name="token" value="1328891125-a7a295ea54a8117119521296902e9dec">
        <select id="lob_action" name="action" onchange="update_text();">
          <option value="add">Add</option>
        </select>

          <a href="docs/en/html/query.html#individual-buglists">the named tag</a>

        <span id="lob_new_query_text">
          <input class="txt" type="text" id="lob_newqueryname"
                 size="20" maxlength="64" name="newqueryname"
                 onkeyup="manage_old_lists();">
        </span>
        <span id="lob_direction">to</span>
        bugs
        <input type="text" name="bug_ids" size="12" maxlength="80">
        <input type="submit" value="Commit" id="commit_list_of_bugs">
      </form>
    </li></ul>
  </li>

  
</ul>

  <div class="outro"></div>
</div>


</body>
</html>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
                      "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
  <head>
    <title>Bugzilla Main Page</title>

      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">


<link rel="Top" href="https://landfill.bugzilla.org/4AG7aCX8My/">



    
    
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
        <a href="request.cgi">Requests</a></li>

  
    
      <li id="new_account_container_top">
        <span class="separator">| </span>
        <a href="createaccount.cgi">New&nbsp;Account</a>
      </li>

    <li id="mini_login_container_top">
  <span class="separator">| </span>
  <a id="login_link_top" href="https://landfill.bugzilla.org/4AG7aCX8My/index.cgi?GoAheadAndLogIn=1"
     onclick="return show_mini_login_form('_top')">Log In</a>
  <form action="https://landfill.bugzilla.org/4AG7aCX8My/index.cgi" method="POST" 
        class="mini_login bz_default_hidden"
        id="mini_login_top"
        onsubmit="return check_mini_login_fields( '_top' );"
  >
    <input id="Bugzilla_login_top" 
           class="bz_login"
           name="Bugzilla_login"
           title="Login"
           onfocus="mini_login_on_focus('_top')"
    >
    <input class="bz_password" 
           id="Bugzilla_password_top" 
           name="Bugzilla_password"
           type="password"
           title="Password"
    >
    <input class="bz_password bz_default_hidden bz_mini_login_help" type="text" 
           id="Bugzilla_password_dummy_top" value="password"
           title="Password"
           onfocus="mini_login_on_focus('_top')"
    >
    <input type="submit" name="GoAheadAndLogIn" value="Log in" 
            id="log_in_top">
    <script type="text/javascript">
      mini_login_constants = {
          "login" : "login",
          "warning" : "You must set the login and password before logging in."
      };
      
      if (YAHOO.env.ua.gecko || YAHOO.env.ua.ie || YAHOO.env.ua.opera) {
          YAHOO.util.Event.onDOMReady(function() {
              init_mini_login_form('_top');
          });
      }
      else {
          YAHOO.util.Event.on(window, 'load', function () {
              window.setTimeout(function() {
                  init_mini_login_form('_top');
              }, 200);
          });
    }
    </script>
    <a href="#" onclick="return hide_mini_login_form('_top')">[x]</a>
  </form>
</li>
<li id="forgot_container_top">
  <span class="separator">| </span>
  <a id="forgot_link_top" href="https://landfill.bugzilla.org/4AG7aCX8My/index.cgi?GoAheadAndLogIn=1#forgot"
     onclick="return show_forgot_form('_top')">Forgot Password</a>
  <form action="token.cgi" method="post" id="forgot_form_top"
        class="mini_forgot bz_default_hidden">
    <label for="login_top">Login:</label>
    <input type="text" name="loginname" size="20" id="login_top">
    <input id="forgot_button_top" value="Reset Password" 
           type="submit">
    <input type="hidden" name="a" value="reqpw">
    <a href="#" onclick="return hide_forgot_form('_top')">[x]</a>
  </form>
</li>
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
                   href="createaccount.cgi"><span>Open a New Account</span></a>
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
                <a href="javascript:window.external.AddSearchProvider('https://landfill.bugzilla.org/4AG7aCX8My/search_plugin.cgi')">
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
        <a href="request.cgi">Requests</a></li>

  
    
      <li id="new_account_container_bottom">
        <span class="separator">| </span>
        <a href="createaccount.cgi">New&nbsp;Account</a>
      </li>

    <li id="mini_login_container_bottom">
  <span class="separator">| </span>
  <a id="login_link_bottom" href="https://landfill.bugzilla.org/4AG7aCX8My/index.cgi?GoAheadAndLogIn=1"
     onclick="return show_mini_login_form('_bottom')">Log In</a>
  <form action="https://landfill.bugzilla.org/4AG7aCX8My/index.cgi" method="POST" 
        class="mini_login bz_default_hidden"
        id="mini_login_bottom"
        onsubmit="return check_mini_login_fields( '_bottom' );"
  >
    <input id="Bugzilla_login_bottom" 
           class="bz_login"
           name="Bugzilla_login"
           title="Login"
           onfocus="mini_login_on_focus('_bottom')"
    >
    <input class="bz_password" 
           id="Bugzilla_password_bottom" 
           name="Bugzilla_password"
           type="password"
           title="Password"
    >
    <input class="bz_password bz_default_hidden bz_mini_login_help" type="text" 
           id="Bugzilla_password_dummy_bottom" value="password"
           title="Password"
           onfocus="mini_login_on_focus('_bottom')"
    >
    <input type="submit" name="GoAheadAndLogIn" value="Log in" 
            id="log_in_bottom">
    <script type="text/javascript">
      mini_login_constants = {
          "login" : "login",
          "warning" : "You must set the login and password before logging in."
      };
      
      if (YAHOO.env.ua.gecko || YAHOO.env.ua.ie || YAHOO.env.ua.opera) {
          YAHOO.util.Event.onDOMReady(function() {
              init_mini_login_form('_bottom');
          });
      }
      else {
          YAHOO.util.Event.on(window, 'load', function () {
              window.setTimeout(function() {
                  init_mini_login_form('_bottom');
              }, 200);
          });
    }
    </script>
    <a href="#" onclick="return hide_mini_login_form('_bottom')">[x]</a>
  </form>
</li>
<li id="forgot_container_bottom">
  <span class="separator">| </span>
  <a id="forgot_link_bottom" href="https://landfill.bugzilla.org/4AG7aCX8My/index.cgi?GoAheadAndLogIn=1#forgot"
     onclick="return show_forgot_form('_bottom')">Forgot Password</a>
  <form action="token.cgi" method="post" id="forgot_form_bottom"
        class="mini_forgot bz_default_hidden">
    <label for="login_bottom">Login:</label>
    <input type="text" name="loginname" size="20" id="login_bottom">
    <input id="forgot_button_bottom" value="Reset Password" 
           type="submit">
    <input type="hidden" name="a" value="reqpw">
    <a href="#" onclick="return hide_forgot_form('_bottom')">[x]</a>
  </form>
</li>
</ul>
  </li>

  
    

  


  
</ul>

  <div class="outro"></div>
</div>


</body>
</html>
CTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
                      "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
  <head>
    <title>Invalid Username Or Password</title>

      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">


<link rel="Top" href="https://landfill.bugzilla.org/bugzilla-tip-sqlite/">



    
    
    <link href="skins/standard/global.css?1326323524"
          rel="alternate stylesheet" 
          title="Classic"><link href="skins/standard/global.css?1326323524" rel="stylesheet"
        type="text/css" ><!--[if lte IE 7]>
      



  <link href="skins/standard/IE-fixes.css?1326323524" rel="stylesheet"
        type="text/css" >
<![endif]-->

    <link href="skins/contrib/Dusk/global.css?1326323524" rel="stylesheet"
        type="text/css" title="Dusk">


    

    

    
<script type="text/javascript" src="js/yui/yahoo-dom-event/yahoo-dom-event.js?1303744147"></script><script type="text/javascript" src="js/yui/cookie/cookie-min.js?1303744147"></script><script type="text/javascript" src="js/global.js?1326323524"></script>

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
                cookiepath: '\/bugzilla-tip-sqlite\/',
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
        class="landfill-bugzilla-org-bugzilla-tip-sqlite yui-skin-sam">



<div id="header">
<div id="banner">
  </div>

<table border="0" cellspacing="0" cellpadding="0" id="titles">
<tr>
    <td id="title">
      <p>Bugzilla &ndash; Invalid Username Or Password</p>
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

    
</ul>
</div> 

<div id="bugzilla-body">


<table cellpadding="20">
  <tr>
    <td id="error_msg" class="throw_error">
    The username or password you entered is not valid.
    

    </td>

  </tr>
</table>

<p>
  Please press <b>Back</b> and try again.
</p>


            
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

    
</ul>
  </li>

  
    

  


  
</ul>

  <div class="outro"></div>
</div>


</body>
</html>


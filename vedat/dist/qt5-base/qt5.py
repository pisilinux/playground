




<!DOCTYPE html>
<html class="   ">
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object: http://ogp.me/ns/object# article: http://ogp.me/ns/article# profile: http://ogp.me/ns/profile#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    
    
    <title>playground/obsoleteman/qt5/qt5.py at c571fdf0f13b3c858fd2f140abfd9295b8a3c23f · pisilinux/playground</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub" />
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub" />
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-144.png" />
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png" />
    <meta property="fb:app_id" content="1401488693436528"/>

      <meta content="@github" name="twitter:site" /><meta content="summary" name="twitter:card" /><meta content="pisilinux/playground" name="twitter:title" /><meta content="playground - Playgrounds for PiSi Linux developers" name="twitter:description" /><meta content="https://avatars0.githubusercontent.com/u/3696896?s=400" name="twitter:image:src" />
<meta content="GitHub" property="og:site_name" /><meta content="object" property="og:type" /><meta content="https://avatars0.githubusercontent.com/u/3696896?s=400" property="og:image" /><meta content="pisilinux/playground" property="og:title" /><meta content="https://github.com/pisilinux/playground" property="og:url" /><meta content="playground - Playgrounds for PiSi Linux developers" property="og:description" />

    <link rel="assets" href="https://assets-cdn.github.com/">
    <link rel="conduit-xhr" href="https://ghconduit.com:25035/">
    <link rel="xhr-socket" href="/_sockets" />

    <meta name="msapplication-TileImage" content="/windows-tile.png" />
    <meta name="msapplication-TileColor" content="#ffffff" />
    <meta name="selected-link" value="repo_source" data-pjax-transient />
      <meta name="google-analytics" content="UA-3769691-2">

    <meta content="collector.githubapp.com" name="octolytics-host" /><meta content="collector-cdn.github.com" name="octolytics-script-host" /><meta content="github" name="octolytics-app-id" /><meta content="58F24557:7CF4:D2F51C1:538CEA03" name="octolytics-dimension-request_id" /><meta content="7329803" name="octolytics-actor-id" /><meta content="vdemir" name="octolytics-actor-login" /><meta content="8613b4c6903010cd8b84c4f6c5c32fe2be2a71d424684dd429eaeebd47218d72" name="octolytics-actor-hash" />
    

    
    
    <link rel="icon" type="image/x-icon" href="https://assets-cdn.github.com/favicon.ico" />


    <meta content="authenticity_token" name="csrf-param" />
<meta content="F/NEyKxFLWiqlqN26jHa/z49bi0KJv+hJSciyXLU9JmpBoNQuyvAdONhLDy2z+niJxmJGxGN+F3C8V5qxMur3Q==" name="csrf-token" />

    <link href="https://assets-cdn.github.com/assets/github-382e2d2394fe36287509f9d88e1aae81a78b71b2.css" media="all" rel="stylesheet" type="text/css" />
    <link href="https://assets-cdn.github.com/assets/github2-e54beab53eeb6d90e5f0ec66633ed0d01247abd9.css" media="all" rel="stylesheet" type="text/css" />
    


    <meta http-equiv="x-pjax-version" content="11ce9eeae337a80af63fa36c715d84f5">

      
  <meta name="description" content="playground - Playgrounds for PiSi Linux developers" />

  <meta content="3696896" name="octolytics-dimension-user_id" /><meta content="pisilinux" name="octolytics-dimension-user_login" /><meta content="8429459" name="octolytics-dimension-repository_id" /><meta content="pisilinux/playground" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="false" name="octolytics-dimension-repository_is_fork" /><meta content="8429459" name="octolytics-dimension-repository_network_root_id" /><meta content="pisilinux/playground" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/pisilinux/playground/commits/c571fdf0f13b3c858fd2f140abfd9295b8a3c23f.atom" rel="alternate" title="Recent Commits to playground:c571fdf0f13b3c858fd2f140abfd9295b8a3c23f" type="application/atom+xml" />

  </head>


  <body class="logged_in  env-production linux vis-public page-blob">
    <a href="#start-of-content" tabindex="1" class="accessibility-aid js-skip-to-content">Skip to content</a>
    <div class="wrapper">
      
      
      
      


      <div class="header header-logged-in true">
  <div class="container clearfix">

    <a class="header-logo-invertocat" href="https://github.com/">
  <span class="mega-octicon octicon-mark-github"></span>
</a>

    
    <a href="/pisilinux/playground/notifications" aria-label="You have unread notifications in this repository" class="notification-indicator tooltipped tooltipped-s contextually-unread" data-hotkey="g n">
        <span class="mail-status unread"></span>
</a>

      <div class="command-bar js-command-bar  in-repository">
          <form accept-charset="UTF-8" action="/search" class="command-bar-form" id="top_search_form" method="get">

<div class="commandbar">
  <span class="message"></span>
  <input type="text" data-hotkey="s, /" name="q" id="js-command-bar-field" placeholder="Search or type a command" tabindex="1" autocapitalize="off"
    
    data-username="vdemir"
      data-repo="pisilinux/playground"
      data-branch="c571fdf0f13b3c858fd2f140abfd9295b8a3c23f"
      data-sha="7eaf0aa9ff712f3358ceab793e66d24a5b6f61f2"
  >
  <div class="display hidden"></div>
</div>

    <input type="hidden" name="nwo" value="pisilinux/playground" />

    <div class="select-menu js-menu-container js-select-menu search-context-select-menu">
      <span class="minibutton select-menu-button js-menu-target" role="button" aria-haspopup="true">
        <span class="js-select-button">This repository</span>
      </span>

      <div class="select-menu-modal-holder js-menu-content js-navigation-container" aria-hidden="true">
        <div class="select-menu-modal">

          <div class="select-menu-item js-navigation-item js-this-repository-navigation-item selected">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" class="js-search-this-repository" name="search_target" value="repository" checked="checked" />
            <div class="select-menu-item-text js-select-button-text">This repository</div>
          </div> <!-- /.select-menu-item -->

          <div class="select-menu-item js-navigation-item js-all-repositories-navigation-item">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" name="search_target" value="global" />
            <div class="select-menu-item-text js-select-button-text">All repositories</div>
          </div> <!-- /.select-menu-item -->

        </div>
      </div>
    </div>

  <span class="help tooltipped tooltipped-s" aria-label="Show command bar help">
    <span class="octicon octicon-question"></span>
  </span>


  <input type="hidden" name="ref" value="cmdform">

</form>
        <ul class="top-nav">
          <li class="explore"><a href="/explore">Explore</a></li>
            <li><a href="https://gist.github.com">Gist</a></li>
            <li><a href="/blog">Blog</a></li>
          <li><a href="https://help.github.com">Help</a></li>
        </ul>
      </div>

    


  <ul id="user-links">
    <li>
      <a href="/vdemir" class="name">
        <img alt="vdemir" class=" js-avatar" data-user="7329803" height="20" src="https://avatars0.githubusercontent.com/u/7329803?s=140" width="20" /> vdemir
      </a>
    </li>

    <li class="new-menu dropdown-toggle js-menu-container">
      <a href="#" class="js-menu-target tooltipped tooltipped-s" aria-label="Create new...">
        <span class="octicon octicon-plus"></span>
        <span class="dropdown-arrow"></span>
      </a>

      <div class="new-menu-content js-menu-content">
      </div>
    </li>

    <li>
      <a href="/settings/profile" id="account_settings"
        class="tooltipped tooltipped-s"
        aria-label="Account settings ">
        <span class="octicon octicon-tools"></span>
      </a>
    </li>
    <li>
      <form class="logout-form" action="/logout" method="post">
        <button class="sign-out-button tooltipped tooltipped-s" aria-label="Sign out">
          <span class="octicon octicon-sign-out"></span>
        </button>
      </form>
    </li>

  </ul>

<div class="js-new-dropdown-contents hidden">
  

<ul class="dropdown-menu">
  <li>
    <a href="/new"><span class="octicon octicon-repo"></span> New repository</a>
  </li>
  <li>
    <a href="/organizations/new"><span class="octicon octicon-organization"></span> New organization</a>
  </li>


    <li class="section-title">
      <span title="pisilinux/playground">This repository</span>
    </li>
      <li>
        <a href="/pisilinux/playground/issues/new"><span class="octicon octicon-issue-opened"></span> New issue</a>
      </li>
</ul>

</div>


    
  </div>
</div>

      

        



      <div id="start-of-content" class="accessibility-aid"></div>
          <div class="site" itemscope itemtype="http://schema.org/WebPage">
    <div id="js-flash-container">
      
    </div>
    <div class="pagehead repohead instapaper_ignore readability-menu">
      <div class="container">
        

<ul class="pagehead-actions">

    <li class="subscription">
      <form accept-charset="UTF-8" action="/notifications/subscribe" class="js-social-container" data-autosubmit="true" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="authenticity_token" type="hidden" value="ftjuWv3MlZ3JCsfnbhoBvclTbsoXVNVzMHSMgNJInj2nZRWcp0VLE8lvCoSECJcpbdFot95fqhcPZPesw0uuSQ==" /></div>  <input id="repository_id" name="repository_id" type="hidden" value="8429459" />

    <div class="select-menu js-menu-container js-select-menu">
      <a class="social-count js-social-count" href="/pisilinux/playground/watchers">
        42
      </a>
      <span class="minibutton select-menu-button with-count js-menu-target" role="button" tabindex="0" aria-haspopup="true">
        <span class="js-select-button">
          <span class="octicon octicon-eye"></span>
          Unwatch
        </span>
      </span>

      <div class="select-menu-modal-holder">
        <div class="select-menu-modal subscription-menu-modal js-menu-content" aria-hidden="true">
          <div class="select-menu-header">
            <span class="select-menu-title">Notification status</span>
            <span class="octicon octicon-x js-menu-close"></span>
          </div> <!-- /.select-menu-header -->

          <div class="select-menu-list js-navigation-container" role="menu">

            <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <div class="select-menu-item-text">
                <input id="do_included" name="do" type="radio" value="included" />
                <h4>Not watching</h4>
                <span class="description">You only receive notifications for conversations in which you participate or are @mentioned.</span>
                <span class="js-select-button-text hidden-select-button-text">
                  <span class="octicon octicon-eye"></span>
                  Watch
                </span>
              </div>
            </div> <!-- /.select-menu-item -->

            <div class="select-menu-item js-navigation-item selected" role="menuitem" tabindex="0">
              <span class="select-menu-item-icon octicon octicon octicon-check"></span>
              <div class="select-menu-item-text">
                <input checked="checked" id="do_subscribed" name="do" type="radio" value="subscribed" />
                <h4>Watching</h4>
                <span class="description">You receive notifications for all conversations in this repository.</span>
                <span class="js-select-button-text hidden-select-button-text">
                  <span class="octicon octicon-eye"></span>
                  Unwatch
                </span>
              </div>
            </div> <!-- /.select-menu-item -->

            <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <div class="select-menu-item-text">
                <input id="do_ignore" name="do" type="radio" value="ignore" />
                <h4>Ignoring</h4>
                <span class="description">You do not receive any notifications for conversations in this repository.</span>
                <span class="js-select-button-text hidden-select-button-text">
                  <span class="octicon octicon-mute"></span>
                  Stop ignoring
                </span>
              </div>
            </div> <!-- /.select-menu-item -->

          </div> <!-- /.select-menu-list -->

        </div> <!-- /.select-menu-modal -->
      </div> <!-- /.select-menu-modal-holder -->
    </div> <!-- /.select-menu -->

</form>
    </li>

  <li>
  

  <div class="js-toggler-container js-social-container starring-container ">

    <form accept-charset="UTF-8" action="/pisilinux/playground/unstar" class="js-toggler-form starred" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="authenticity_token" type="hidden" value="3rAnmgVzpdphEwPLAxRiTmhx45VjK1gLWQHNe+UUs/c8EihR3E33pZYCSSTQbnBP8lcC62vG4pVHM6HTgS8DoA==" /></div>
      <button
        class="minibutton with-count js-toggler-target star-button"
        aria-label="Unstar this repository" title="Unstar pisilinux/playground">
        <span class="octicon octicon-star"></span><span class="text">Unstar</span>
      </button>
        <a class="social-count js-social-count" href="/pisilinux/playground/stargazers">
          3
        </a>
</form>
    <form accept-charset="UTF-8" action="/pisilinux/playground/star" class="js-toggler-form unstarred" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="authenticity_token" type="hidden" value="Tu8hoIn0mJGwVxzucCawpr2NG/3wxWsVWlNoeR+W3LXnpFKfiPBqhJlSf/f2933sg0W2GDlrrJERz/Y8GX/pMA==" /></div>
      <button
        class="minibutton with-count js-toggler-target star-button"
        aria-label="Star this repository" title="Star pisilinux/playground">
        <span class="octicon octicon-star"></span><span class="text">Star</span>
      </button>
        <a class="social-count js-social-count" href="/pisilinux/playground/stargazers">
          3
        </a>
</form>  </div>

  </li>


        <li>
          <a href="/pisilinux/playground/fork" class="minibutton with-count js-toggler-target fork-button lighter tooltipped-n" title="Fork your own copy of pisilinux/playground to your account" aria-label="Fork your own copy of pisilinux/playground to your account" rel="facebox nofollow">
            <span class="octicon octicon-repo-forked"></span><span class="text">Fork</span>
          </a>
          <a href="/pisilinux/playground/network" class="social-count">10</a>
        </li>


</ul>

        <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public">
          <span class="repo-label"><span>public</span></span>
          <span class="mega-octicon octicon-repo"></span>
          <span class="author"><a href="/pisilinux" class="url fn" itemprop="url" rel="author"><span itemprop="title">pisilinux</span></a></span><!--
       --><span class="path-divider">/</span><!--
       --><strong><a href="/pisilinux/playground" class="js-current-repository js-repo-home-link">playground</a></strong>

          <span class="page-context-loader">
            <img alt="" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
          </span>

        </h1>
      </div><!-- /.container -->
    </div><!-- /.repohead -->

    <div class="container">
      <div class="repository-with-sidebar repo-container new-discussion-timeline js-new-discussion-timeline  ">
        <div class="repository-sidebar clearfix">
            

<div class="sunken-menu vertical-right repo-nav js-repo-nav js-repository-container-pjax js-octicon-loaders">
  <div class="sunken-menu-contents">
    <ul class="sunken-menu-group">
      <li class="tooltipped tooltipped-w" aria-label="Code">
        <a href="/pisilinux/playground" aria-label="Code" class="selected js-selected-navigation-item sunken-menu-item" data-hotkey="g c" data-pjax="true" data-selected-links="repo_source repo_downloads repo_commits repo_releases repo_tags repo_branches /pisilinux/playground">
          <span class="octicon octicon-code"></span> <span class="full-word">Code</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

        <li class="tooltipped tooltipped-w" aria-label="Issues">
          <a href="/pisilinux/playground/issues" aria-label="Issues" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-hotkey="g i" data-selected-links="repo_issues /pisilinux/playground/issues">
            <span class="octicon octicon-issue-opened"></span> <span class="full-word">Issues</span>
            <span class='counter'>3</span>
            <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>        </li>

      <li class="tooltipped tooltipped-w" aria-label="Pull Requests">
        <a href="/pisilinux/playground/pulls" aria-label="Pull Requests" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-hotkey="g p" data-selected-links="repo_pulls /pisilinux/playground/pulls">
            <span class="octicon octicon-git-pull-request"></span> <span class="full-word">Pull Requests</span>
            <span class='counter'>1</span>
            <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>


        <li class="tooltipped tooltipped-w" aria-label="Wiki">
          <a href="/pisilinux/playground/wiki" aria-label="Wiki" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-hotkey="g w" data-selected-links="repo_wiki /pisilinux/playground/wiki">
            <span class="octicon octicon-book"></span> <span class="full-word">Wiki</span>
            <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>        </li>
    </ul>
    <div class="sunken-menu-separator"></div>
    <ul class="sunken-menu-group">

      <li class="tooltipped tooltipped-w" aria-label="Pulse">
        <a href="/pisilinux/playground/pulse" aria-label="Pulse" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="pulse /pisilinux/playground/pulse">
          <span class="octicon octicon-pulse"></span> <span class="full-word">Pulse</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped tooltipped-w" aria-label="Graphs">
        <a href="/pisilinux/playground/graphs" aria-label="Graphs" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="repo_graphs repo_contributors /pisilinux/playground/graphs">
          <span class="octicon octicon-graph"></span> <span class="full-word">Graphs</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped tooltipped-w" aria-label="Network">
        <a href="/pisilinux/playground/network" aria-label="Network" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-selected-links="repo_network /pisilinux/playground/network">
          <span class="octicon octicon-repo-forked"></span> <span class="full-word">Network</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>
    </ul>


  </div>
</div>

              <div class="only-with-full-nav">
                

  

<div class="clone-url open"
  data-protocol-type="http"
  data-url="/users/set_protocol?protocol_selector=http&amp;protocol_type=push">
  <h3><strong>HTTPS</strong> clone URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="https://github.com/pisilinux/playground.git" readonly="readonly">
    <span class="url-box-clippy">
    <button aria-label="copy to clipboard" class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="https://github.com/pisilinux/playground.git" data-copied-hint="copied!" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>

  

<div class="clone-url "
  data-protocol-type="ssh"
  data-url="/users/set_protocol?protocol_selector=ssh&amp;protocol_type=push">
  <h3><strong>SSH</strong> clone URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="git@github.com:pisilinux/playground.git" readonly="readonly">
    <span class="url-box-clippy">
    <button aria-label="copy to clipboard" class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="git@github.com:pisilinux/playground.git" data-copied-hint="copied!" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>

  

<div class="clone-url "
  data-protocol-type="subversion"
  data-url="/users/set_protocol?protocol_selector=subversion&amp;protocol_type=push">
  <h3><strong>Subversion</strong> checkout URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="https://github.com/pisilinux/playground" readonly="readonly">
    <span class="url-box-clippy">
    <button aria-label="copy to clipboard" class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="https://github.com/pisilinux/playground" data-copied-hint="copied!" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>


<p class="clone-options">You can clone with
      <a href="#" class="js-clone-selector" data-protocol="http">HTTPS</a>,
      <a href="#" class="js-clone-selector" data-protocol="ssh">SSH</a>,
      or <a href="#" class="js-clone-selector" data-protocol="subversion">Subversion</a>.
  <span class="help tooltipped tooltipped-n" aria-label="Get help on which URL is right for you.">
    <a href="https://help.github.com/articles/which-remote-url-should-i-use">
    <span class="octicon octicon-question"></span>
    </a>
  </span>
</p>



                <a href="/pisilinux/playground/archive/c571fdf0f13b3c858fd2f140abfd9295b8a3c23f.zip"
                   class="minibutton sidebar-button"
                   aria-label="Download pisilinux/playground as a zip file"
                   title="Download pisilinux/playground as a zip file"
                   rel="nofollow">
                  <span class="octicon octicon-cloud-download"></span>
                  Download ZIP
                </a>
              </div>
        </div><!-- /.repository-sidebar -->

        <div id="js-repo-pjax-container" class="repository-content context-loader-container" data-pjax-container>
          


<a href="/pisilinux/playground/blob/c571fdf0f13b3c858fd2f140abfd9295b8a3c23f/obsoleteman/qt5/qt5.py" class="hidden js-permalink-shortcut" data-hotkey="y">Permalink</a>

<!-- blob contrib key: blob_contributors:v21:d7aa4caae7a719960983492559cb57dd -->

<p title="This is a placeholder element" class="js-history-link-replace hidden"></p>

<a href="/pisilinux/playground/find/c571fdf0f13b3c858fd2f140abfd9295b8a3c23f" data-pjax data-hotkey="t" class="js-show-file-finder" style="display:none">Show File Finder</a>

<div class="file-navigation">
  

<div class="select-menu js-menu-container js-select-menu" >
  <span class="minibutton select-menu-button js-menu-target" data-hotkey="w"
    data-master-branch="master"
    data-ref=""
    role="button" aria-label="Switch branches or tags" tabindex="0" aria-haspopup="true">
    <span class="octicon octicon-git-branch"></span>
    <i>tree:</i>
    <span class="js-select-button">c571fdf0f1</span>
  </span>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax aria-hidden="true">

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <span class="select-menu-title">Switch branches/tags</span>
        <span class="octicon octicon-x js-menu-close"></span>
      </div> <!-- /.select-menu-header -->

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Find or create a branch…" id="context-commitish-filter-field" class="js-filterable-field js-navigation-enable" placeholder="Find or create a branch…">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" class="js-select-menu-tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" class="js-select-menu-tab">Tags</a>
            </li>
          </ul>
        </div><!-- /.select-menu-tabs -->
      </div><!-- /.select-menu-filters -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/pisilinux/playground/blob/master/obsoleteman/qt5/qt5.py"
                 data-name="master"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="master">master</a>
            </div> <!-- /.select-menu-item -->
        </div>

          <form accept-charset="UTF-8" action="/pisilinux/playground/branches" class="js-create-branch select-menu-item select-menu-new-item-form js-navigation-item js-new-item-form" method="post"><div style="margin:0;padding:0;display:inline"><input name="authenticity_token" type="hidden" value="9saxrlZYRmR6BS+hdBfu9N9TzmejZFt85KMJsEaM+FimaOOA4TZXOPq92UNWCZhn0ud13yS1gLrIrajFuKRZxA==" /></div>
            <span class="octicon octicon-git-branch select-menu-item-icon"></span>
            <div class="select-menu-item-text">
              <h4>Create branch: <span class="js-new-item-name"></span></h4>
              <span class="description">from ‘c571fdf’</span>
            </div>
            <input type="hidden" name="name" id="name" class="js-new-item-value">
            <input type="hidden" name="branch" id="branch" value="c571fdf0f13b3c858fd2f140abfd9295b8a3c23f" />
            <input type="hidden" name="path" id="path" value="obsoleteman/qt5/qt5.py" />
          </form> <!-- /.select-menu-item -->

      </div> <!-- /.select-menu-list -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

    </div> <!-- /.select-menu-modal -->
  </div> <!-- /.select-menu-modal-holder -->
</div> <!-- /.select-menu -->

  <div class="breadcrumb">
    <span class='repo-root js-repo-root'><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/pisilinux/playground/tree/c571fdf0f13b3c858fd2f140abfd9295b8a3c23f" data-branch="c571fdf0f13b3c858fd2f140abfd9295b8a3c23f" data-direction="back" data-pjax="true" itemscope="url" rel="nofollow"><span itemprop="title">playground</span></a></span></span><span class="separator"> / </span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/pisilinux/playground/tree/c571fdf0f13b3c858fd2f140abfd9295b8a3c23f/obsoleteman" data-branch="c571fdf0f13b3c858fd2f140abfd9295b8a3c23f" data-direction="back" data-pjax="true" itemscope="url" rel="nofollow"><span itemprop="title">obsoleteman</span></a></span><span class="separator"> / </span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/pisilinux/playground/tree/c571fdf0f13b3c858fd2f140abfd9295b8a3c23f/obsoleteman/qt5" data-branch="c571fdf0f13b3c858fd2f140abfd9295b8a3c23f" data-direction="back" data-pjax="true" itemscope="url" rel="nofollow"><span itemprop="title">qt5</span></a></span><span class="separator"> / </span><strong class="final-path">qt5.py</strong> <button aria-label="copy to clipboard" class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="obsoleteman/qt5/qt5.py" data-copied-hint="copied!" type="button"><span class="octicon octicon-clippy"></span></button>
  </div>
</div>


  <div class="commit file-history-tease">
      <img alt="Serdar Soytetir" class="main-avatar js-avatar" data-user="2321128" height="24" src="https://avatars3.githubusercontent.com/u/2321128?s=140" width="24" />
      <span class="author"><a href="/obsoleteman" rel="contributor">obsoleteman</a></span>
      <time datetime="2014-05-23T07:02:53+03:00" is="relative-time">May 23, 2014</time>
      <div class="commit-title">
          <a href="/pisilinux/playground/commit/214bafa4cacfb213de19c8ac31cf9b572819915e" class="message" data-pjax="true" title="try qt5 with emul32">try qt5 with emul32</a>
      </div>

    <div class="participation">
      <p class="quickstat"><a href="#blob_contributors_box" rel="facebox"><strong>1</strong>  contributor</a></p>
      
    </div>
    <div id="blob_contributors_box" style="display:none">
      <h2 class="facebox-header">Users who have contributed to this file</h2>
      <ul class="facebox-user-list">
          <li class="facebox-user-list-item">
            <img alt="Serdar Soytetir" class=" js-avatar" data-user="2321128" height="24" src="https://avatars3.githubusercontent.com/u/2321128?s=140" width="24" />
            <a href="/obsoleteman">obsoleteman</a>
          </li>
      </ul>
    </div>
  </div>

<div class="file-box">
  <div class="file">
    <div class="meta clearfix">
      <div class="info file-name">
        <span class="icon"><b class="octicon octicon-file-text"></b></span>
        <span class="mode" title="File Mode">file</span>
        <span class="meta-divider"></span>
          <span>72 lines (55 sloc)</span>
          <span class="meta-divider"></span>
        <span>2.321 kb</span>
      </div>
      <div class="actions">
        <div class="button-group">
              <a class="minibutton disabled tooltipped tooltipped-w" href="#"
                 aria-label="You must be on a branch to make or propose changes to this file">Edit</a>
          <a href="/pisilinux/playground/raw/c571fdf0f13b3c858fd2f140abfd9295b8a3c23f/obsoleteman/qt5/qt5.py" class="button minibutton " id="raw-url">Raw</a>
            <a href="/pisilinux/playground/blame/c571fdf0f13b3c858fd2f140abfd9295b8a3c23f/obsoleteman/qt5/qt5.py" class="button minibutton js-update-url-with-hash">Blame</a>
          <a href="/pisilinux/playground/commits/c571fdf0f13b3c858fd2f140abfd9295b8a3c23f/obsoleteman/qt5/qt5.py" class="button minibutton " rel="nofollow">History</a>
        </div><!-- /.button-group -->
          <a class="minibutton danger disabled empty-icon tooltipped tooltipped-w" href="#"
             aria-label="You must be on a branch to make or propose changes to this file">
          Delete
        </a>
      </div><!-- /.actions -->
    </div>
      
  <div class="blob-wrapper data type-python js-blob-data">
       <table class="file-code file-diff tab-size-8">
         <tr class="file-code-line">
           <td class="blob-line-nums">
             <span id="L1" rel="#L1">1</span>
<span id="L2" rel="#L2">2</span>
<span id="L3" rel="#L3">3</span>
<span id="L4" rel="#L4">4</span>
<span id="L5" rel="#L5">5</span>
<span id="L6" rel="#L6">6</span>
<span id="L7" rel="#L7">7</span>
<span id="L8" rel="#L8">8</span>
<span id="L9" rel="#L9">9</span>
<span id="L10" rel="#L10">10</span>
<span id="L11" rel="#L11">11</span>
<span id="L12" rel="#L12">12</span>
<span id="L13" rel="#L13">13</span>
<span id="L14" rel="#L14">14</span>
<span id="L15" rel="#L15">15</span>
<span id="L16" rel="#L16">16</span>
<span id="L17" rel="#L17">17</span>
<span id="L18" rel="#L18">18</span>
<span id="L19" rel="#L19">19</span>
<span id="L20" rel="#L20">20</span>
<span id="L21" rel="#L21">21</span>
<span id="L22" rel="#L22">22</span>
<span id="L23" rel="#L23">23</span>
<span id="L24" rel="#L24">24</span>
<span id="L25" rel="#L25">25</span>
<span id="L26" rel="#L26">26</span>
<span id="L27" rel="#L27">27</span>
<span id="L28" rel="#L28">28</span>
<span id="L29" rel="#L29">29</span>
<span id="L30" rel="#L30">30</span>
<span id="L31" rel="#L31">31</span>
<span id="L32" rel="#L32">32</span>
<span id="L33" rel="#L33">33</span>
<span id="L34" rel="#L34">34</span>
<span id="L35" rel="#L35">35</span>
<span id="L36" rel="#L36">36</span>
<span id="L37" rel="#L37">37</span>
<span id="L38" rel="#L38">38</span>
<span id="L39" rel="#L39">39</span>
<span id="L40" rel="#L40">40</span>
<span id="L41" rel="#L41">41</span>
<span id="L42" rel="#L42">42</span>
<span id="L43" rel="#L43">43</span>
<span id="L44" rel="#L44">44</span>
<span id="L45" rel="#L45">45</span>
<span id="L46" rel="#L46">46</span>
<span id="L47" rel="#L47">47</span>
<span id="L48" rel="#L48">48</span>
<span id="L49" rel="#L49">49</span>
<span id="L50" rel="#L50">50</span>
<span id="L51" rel="#L51">51</span>
<span id="L52" rel="#L52">52</span>
<span id="L53" rel="#L53">53</span>
<span id="L54" rel="#L54">54</span>
<span id="L55" rel="#L55">55</span>
<span id="L56" rel="#L56">56</span>
<span id="L57" rel="#L57">57</span>
<span id="L58" rel="#L58">58</span>
<span id="L59" rel="#L59">59</span>
<span id="L60" rel="#L60">60</span>
<span id="L61" rel="#L61">61</span>
<span id="L62" rel="#L62">62</span>
<span id="L63" rel="#L63">63</span>
<span id="L64" rel="#L64">64</span>
<span id="L65" rel="#L65">65</span>
<span id="L66" rel="#L66">66</span>
<span id="L67" rel="#L67">67</span>
<span id="L68" rel="#L68">68</span>
<span id="L69" rel="#L69">69</span>
<span id="L70" rel="#L70">70</span>
<span id="L71" rel="#L71">71</span>

           </td>
           <td class="blob-line-code"><div class="code-body highlight"><pre><div class='line' id='LC1'><span class="c"># -*- coding: utf-8 -*-</span></div><div class='line' id='LC2'><span class="c">#</span></div><div class='line' id='LC3'><span class="c"># Copyright (C) 2010 TUBITAK/UEKAE</span></div><div class='line' id='LC4'><span class="c">#</span></div><div class='line' id='LC5'><span class="c"># This program is free software; you can redistribute it and/or modify it under</span></div><div class='line' id='LC6'><span class="c"># the terms of the GNU General Public License as published by the Free</span></div><div class='line' id='LC7'><span class="c"># Software Foundation; either version 2 of the License, or (at your option)</span></div><div class='line' id='LC8'><span class="c"># any later version.</span></div><div class='line' id='LC9'><span class="c">#</span></div><div class='line' id='LC10'><span class="c"># Please read the COPYING file.</span></div><div class='line' id='LC11'><br/></div><div class='line' id='LC12'><span class="kn">import</span> <span class="nn">glob</span></div><div class='line' id='LC13'><span class="kn">import</span> <span class="nn">gettext</span></div><div class='line' id='LC14'><span class="n">__trans</span> <span class="o">=</span> <span class="n">gettext</span><span class="o">.</span><span class="n">translation</span><span class="p">(</span><span class="s">&#39;pisi&#39;</span><span class="p">,</span> <span class="n">fallback</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span></div><div class='line' id='LC15'><span class="n">_</span> <span class="o">=</span> <span class="n">__trans</span><span class="o">.</span><span class="n">ugettext</span></div><div class='line' id='LC16'><br/></div><div class='line' id='LC17'><span class="c"># Pisi Modules</span></div><div class='line' id='LC18'><span class="kn">import</span> <span class="nn">pisi.context</span> <span class="kn">as</span> <span class="nn">ctx</span></div><div class='line' id='LC19'><br/></div><div class='line' id='LC20'><span class="c"># ActionsAPI Modules</span></div><div class='line' id='LC21'><span class="kn">import</span> <span class="nn">pisi.actionsapi</span></div><div class='line' id='LC22'><br/></div><div class='line' id='LC23'><span class="c"># ActionsAPI Modules</span></div><div class='line' id='LC24'><span class="kn">from</span> <span class="nn">pisi.actionsapi</span> <span class="kn">import</span> <span class="n">get</span></div><div class='line' id='LC25'><span class="kn">from</span> <span class="nn">pisi.actionsapi</span> <span class="kn">import</span> <span class="n">cmaketools</span></div><div class='line' id='LC26'><span class="kn">from</span> <span class="nn">pisi.actionsapi</span> <span class="kn">import</span> <span class="n">shelltools</span></div><div class='line' id='LC27'><br/></div><div class='line' id='LC28'><span class="n">basename</span> <span class="o">=</span> <span class="s">&quot;qt5&quot;</span></div><div class='line' id='LC29'><br/></div><div class='line' id='LC30'><span class="n">prefix</span> <span class="o">=</span> <span class="s">&quot;/</span><span class="si">%s</span><span class="s">&quot;</span> <span class="o">%</span> <span class="n">get</span><span class="o">.</span><span class="n">defaultprefixDIR</span><span class="p">()</span></div><div class='line' id='LC31'><span class="n">libdir</span> <span class="o">=</span> <span class="s">&quot;</span><span class="si">%s</span><span class="s">/lib&quot;</span> <span class="o">%</span> <span class="n">prefix</span></div><div class='line' id='LC32'><span class="n">libexecdir</span> <span class="o">=</span> <span class="s">&quot;</span><span class="si">%s</span><span class="s">/libexec&quot;</span> <span class="o">%</span> <span class="n">prefix</span></div><div class='line' id='LC33'><span class="n">sysconfdir</span><span class="o">=</span> <span class="s">&quot;/etc&quot;</span></div><div class='line' id='LC34'><span class="n">bindir</span> <span class="o">=</span> <span class="s">&quot;</span><span class="si">%s</span><span class="s">/bin&quot;</span> <span class="o">%</span> <span class="n">prefix</span></div><div class='line' id='LC35'><span class="n">includedir</span> <span class="o">=</span> <span class="s">&quot;</span><span class="si">%s</span><span class="s">/include&quot;</span> <span class="o">%</span> <span class="n">prefix</span></div><div class='line' id='LC36'><br/></div><div class='line' id='LC37'><span class="c"># qt5 spesific variables</span></div><div class='line' id='LC38'><br/></div><div class='line' id='LC39'><span class="n">headerdir</span> <span class="o">=</span> <span class="s">&quot;</span><span class="si">%s</span><span class="s">/include/</span><span class="si">%s</span><span class="s">&quot;</span> <span class="o">%</span> <span class="p">(</span><span class="n">prefix</span><span class="p">,</span> <span class="n">basename</span><span class="p">)</span></div><div class='line' id='LC40'><span class="n">datadir</span> <span class="o">=</span> <span class="s">&quot;</span><span class="si">%s</span><span class="s">/share/</span><span class="si">%s</span><span class="s">&quot;</span> <span class="o">%</span> <span class="p">(</span><span class="n">prefix</span><span class="p">,</span> <span class="n">basename</span><span class="p">)</span></div><div class='line' id='LC41'><span class="n">docdir</span> <span class="o">=</span> <span class="s">&quot;/</span><span class="si">%s</span><span class="s">/</span><span class="si">%s</span><span class="s">&quot;</span> <span class="o">%</span> <span class="p">(</span><span class="n">get</span><span class="o">.</span><span class="n">docDIR</span><span class="p">(),</span> <span class="n">basename</span><span class="p">)</span></div><div class='line' id='LC42'><span class="n">archdatadir</span> <span class="o">=</span> <span class="s">&quot;</span><span class="si">%s</span><span class="s">/</span><span class="si">%s</span><span class="s">&quot;</span> <span class="o">%</span> <span class="p">(</span><span class="n">libdir</span><span class="p">,</span> <span class="n">basename</span><span class="p">)</span></div><div class='line' id='LC43'><span class="n">examplesdir</span> <span class="o">=</span> <span class="s">&quot;</span><span class="si">%s</span><span class="s">/</span><span class="si">%s</span><span class="s">/examples&quot;</span> <span class="o">%</span> <span class="p">(</span><span class="n">libdir</span><span class="p">,</span> <span class="n">basename</span><span class="p">)</span></div><div class='line' id='LC44'><span class="n">importdir</span> <span class="o">=</span> <span class="s">&quot;</span><span class="si">%s</span><span class="s">/</span><span class="si">%s</span><span class="s">/imports&quot;</span> <span class="o">%</span> <span class="p">(</span><span class="n">libdir</span><span class="p">,</span> <span class="n">basename</span><span class="p">)</span></div><div class='line' id='LC45'><span class="n">plugindir</span> <span class="o">=</span> <span class="s">&quot;</span><span class="si">%s</span><span class="s">/</span><span class="si">%s</span><span class="s">/plugins&quot;</span> <span class="o">%</span> <span class="p">(</span><span class="n">libdir</span><span class="p">,</span> <span class="n">basename</span><span class="p">)</span></div><div class='line' id='LC46'><span class="n">translationdir</span> <span class="o">=</span> <span class="s">&quot;</span><span class="si">%s</span><span class="s">/translations&quot;</span> <span class="o">%</span> <span class="n">datadir</span></div><div class='line' id='LC47'><br/></div><div class='line' id='LC48'><span class="n">qmake</span> <span class="o">=</span> <span class="s">&quot;</span><span class="si">%s</span><span class="s">/qmake-qt5&quot;</span> <span class="o">%</span> <span class="n">bindir</span></div><div class='line' id='LC49'><br/></div><div class='line' id='LC50'><span class="k">class</span> <span class="nc">ConfigureError</span><span class="p">(</span><span class="n">pisi</span><span class="o">.</span><span class="n">actionsapi</span><span class="o">.</span><span class="n">Error</span><span class="p">):</span></div><div class='line' id='LC51'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">value</span><span class="o">=</span><span class="s">&#39;&#39;</span><span class="p">):</span></div><div class='line' id='LC52'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">pisi</span><span class="o">.</span><span class="n">actionsapi</span><span class="o">.</span><span class="n">Error</span><span class="o">.</span><span class="n">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">value</span><span class="p">)</span></div><div class='line' id='LC53'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="bp">self</span><span class="o">.</span><span class="n">value</span> <span class="o">=</span> <span class="n">value</span></div><div class='line' id='LC54'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">ctx</span><span class="o">.</span><span class="n">ui</span><span class="o">.</span><span class="n">error</span><span class="p">(</span><span class="n">value</span><span class="p">)</span></div><div class='line' id='LC55'><br/></div><div class='line' id='LC56'><span class="k">def</span> <span class="nf">configure</span><span class="p">(</span><span class="n">projectfile</span><span class="o">=</span><span class="s">&#39;&#39;</span><span class="p">,</span> <span class="n">parameters</span><span class="o">=</span><span class="s">&#39;&#39;</span><span class="p">,</span> <span class="n">installPrefix</span><span class="o">=</span><span class="n">prefix</span><span class="p">):</span></div><div class='line' id='LC57'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="n">projectfile</span> <span class="o">!=</span> <span class="s">&#39;&#39;</span> <span class="ow">and</span> <span class="ow">not</span> <span class="n">shelltools</span><span class="o">.</span><span class="n">can_access_file</span><span class="p">(</span><span class="n">projectfile</span><span class="p">):</span></div><div class='line' id='LC58'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">raise</span> <span class="n">ConfigureError</span><span class="p">(</span><span class="n">_</span><span class="p">(</span><span class="s">&quot;Project file &#39;</span><span class="si">%s</span><span class="s">&#39; not found.&quot;</span><span class="p">)</span> <span class="o">%</span> <span class="n">projectfile</span><span class="p">)</span></div><div class='line' id='LC59'><br/></div><div class='line' id='LC60'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">profiles</span> <span class="o">=</span> <span class="n">glob</span><span class="o">.</span><span class="n">glob</span><span class="p">(</span><span class="s">&quot;*.pro&quot;</span><span class="p">)</span></div><div class='line' id='LC61'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">profiles</span><span class="p">)</span> <span class="o">&gt;</span> <span class="mi">1</span> <span class="ow">and</span> <span class="n">projectfile</span> <span class="o">==</span> <span class="s">&#39;&#39;</span><span class="p">:</span></div><div class='line' id='LC62'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">raise</span> <span class="n">ConfigureError</span><span class="p">(</span><span class="n">_</span><span class="p">(</span><span class="s">&quot;It seems there are more than one .pro file, you must specify one. (Possible .pro files: </span><span class="si">%s</span><span class="s">)&quot;</span><span class="p">)</span> <span class="o">%</span> <span class="s">&quot;, &quot;</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">profiles</span><span class="p">))</span></div><div class='line' id='LC63'><br/></div><div class='line' id='LC64'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">shelltools</span><span class="o">.</span><span class="n">system</span><span class="p">(</span><span class="s">&quot;</span><span class="si">%s</span><span class="s"> -makefile </span><span class="si">%s</span><span class="s"> PREFIX=&#39;</span><span class="si">%s</span><span class="s">&#39; QMAKE_CFLAGS+=&#39;</span><span class="si">%s</span><span class="s">&#39; QMAKE_CXXFLAGS+=&#39;</span><span class="si">%s</span><span class="s">&#39; </span><span class="si">%s</span><span class="s">&quot;</span> <span class="o">%</span> <span class="p">(</span><span class="n">qmake</span><span class="p">,</span> <span class="n">projectfile</span><span class="p">,</span> <span class="n">installPrefix</span><span class="p">,</span> <span class="n">get</span><span class="o">.</span><span class="n">CFLAGS</span><span class="p">(),</span> <span class="n">get</span><span class="o">.</span><span class="n">CXXFLAGS</span><span class="p">(),</span> <span class="n">parameters</span><span class="p">))</span></div><div class='line' id='LC65'><br/></div><div class='line' id='LC66'><span class="k">def</span> <span class="nf">make</span><span class="p">(</span><span class="n">parameters</span><span class="o">=</span><span class="s">&#39;&#39;</span><span class="p">):</span></div><div class='line' id='LC67'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">cmaketools</span><span class="o">.</span><span class="n">make</span><span class="p">(</span><span class="n">parameters</span><span class="p">)</span></div><div class='line' id='LC68'><br/></div><div class='line' id='LC69'><span class="k">def</span> <span class="nf">install</span><span class="p">(</span><span class="n">parameters</span><span class="o">=</span><span class="s">&#39;&#39;</span><span class="p">,</span> <span class="n">argument</span><span class="o">=</span><span class="s">&#39;install&#39;</span><span class="p">):</span></div><div class='line' id='LC70'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">cmaketools</span><span class="o">.</span><span class="n">install</span><span class="p">(</span><span class="s">&#39;INSTALL_ROOT=&quot;</span><span class="si">%s</span><span class="s">&quot; </span><span class="si">%s</span><span class="s">&#39;</span> <span class="o">%</span> <span class="p">(</span><span class="n">get</span><span class="o">.</span><span class="n">installDIR</span><span class="p">(),</span> <span class="n">parameters</span><span class="p">),</span> <span class="n">argument</span><span class="p">)</span></div><div class='line' id='LC71'><br/></div></pre></div></td>
         </tr>
       </table>
  </div>

  </div>
</div>

<a href="#jump-to-line" rel="facebox[.linejump]" data-hotkey="l" class="js-jump-to-line" style="display:none">Jump to Line</a>
<div id="jump-to-line" style="display:none">
  <form accept-charset="UTF-8" class="js-jump-to-line-form">
    <input class="linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" autofocus>
    <button type="submit" class="button">Go</button>
  </form>
</div>

        </div>

      </div><!-- /.repo-container -->
      <div class="modal-backdrop"></div>
    </div><!-- /.container -->
  </div><!-- /.site -->


    </div><!-- /.wrapper -->

      <div class="container">
  <div class="site-footer">
    <ul class="site-footer-links right">
      <li><a href="https://status.github.com/">Status</a></li>
      <li><a href="http://developer.github.com">API</a></li>
      <li><a href="http://training.github.com">Training</a></li>
      <li><a href="http://shop.github.com">Shop</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/about">About</a></li>

    </ul>

    <a href="/">
      <span class="mega-octicon octicon-mark-github" title="GitHub"></span>
    </a>

    <ul class="site-footer-links">
      <li>&copy; 2014 <span title="0.08138s from github-fe140-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="/site/terms">Terms</a></li>
        <li><a href="/site/privacy">Privacy</a></li>
        <li><a href="/security">Security</a></li>
        <li><a href="/contact">Contact</a></li>
    </ul>
  </div><!-- /.site-footer -->
</div><!-- /.container -->


    <div class="fullscreen-overlay js-fullscreen-overlay" id="fullscreen_overlay">
  <div class="fullscreen-container js-fullscreen-container">
    <div class="textarea-wrap">
      <textarea name="fullscreen-contents" id="fullscreen-contents" class="fullscreen-contents js-fullscreen-contents" placeholder="" data-suggester="fullscreen_suggester"></textarea>
    </div>
  </div>
  <div class="fullscreen-sidebar">
    <a href="#" class="exit-fullscreen js-exit-fullscreen tooltipped tooltipped-w" aria-label="Exit Zen Mode">
      <span class="mega-octicon octicon-screen-normal"></span>
    </a>
    <a href="#" class="theme-switcher js-theme-switcher tooltipped tooltipped-w"
      aria-label="Switch themes">
      <span class="octicon octicon-color-mode"></span>
    </a>
  </div>
</div>



    <div id="ajax-error-message" class="flash flash-error">
      <span class="octicon octicon-alert"></span>
      <a href="#" class="octicon octicon-x close js-ajax-error-dismiss"></a>
      Something went wrong with that request. Please try again.
    </div>


      <script crossorigin="anonymous" src="https://assets-cdn.github.com/assets/frameworks-31cf39cf6a61d4c498cba6c0e9c100fb2b06b2f8.js" type="text/javascript"></script>
      <script async="async" crossorigin="anonymous" src="https://assets-cdn.github.com/assets/github-f46fb267b17abef29428ce8d483896a272c7a5a3.js" type="text/javascript"></script>
      
      
        <script async src="https://www.google-analytics.com/analytics.js"></script>
  </body>
</html>


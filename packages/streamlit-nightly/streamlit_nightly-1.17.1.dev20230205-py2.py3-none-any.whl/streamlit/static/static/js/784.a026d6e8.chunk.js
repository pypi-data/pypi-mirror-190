"use strict";(self.webpackChunkstreamlit_browser=self.webpackChunkstreamlit_browser||[]).push([[784],{37800:function(e,t,r){r.r(t),r.d(t,{default:function(){return o}});var n=r(47313),a=r(49950),i=r(7976),s=r(93986),u=r(46417);function o(e){var t=e.element,r=e.width,o=(0,n.useRef)(null),c=(0,n.useContext)(a.Z).getBaseUriParts,l=t.type,d=t.url;(0,n.useEffect)((function(){var e=o.current,r=function(){e&&(e.currentTime=t.startTime)};return e&&e.addEventListener("loadedmetadata",r),function(){e&&e.removeEventListener("loadedmetadata",r)}}),[t]);if(l===i.nk.Type.YOUTUBE_IFRAME){var f=0!==r?.75*r:528;return(0,u.jsx)("iframe",{title:d,src:function(e){var r=t.startTime;return r?"".concat(e,"?start=").concat(r):e}(d),width:r,height:f,frameBorder:"0",allow:"autoplay; encrypted-media",allowFullScreen:!0})}return(0,u.jsx)("video",{ref:o,controls:!0,src:(0,s.Bz)(d,c()),className:"stVideo",style:{width:r,height:0===r?528:void 0}})}}}]);
"use strict";(self.webpackChunkstreamlit_browser=self.webpackChunkstreamlit_browser||[]).push([[628],{75006:function(e,t,n){n.d(t,{Z:function(){return f}});n(47313);var r,o=n(64243),i=n(65167),a=n(1413),u=n(30168),l=n(47167),c=(0,n(30686).F4)(r||(r=(0,u.Z)(["\n  50% {\n    color: rgba(0, 0, 0, 0);\n  }\n"]))),s=(0,l.Z)("span",{target:"e1m4n6jn0"})((function(e){var t=e.includeDot,n=e.shouldBlink,r=e.theme;return(0,a.Z)((0,a.Z)({},t?{"&::before":{opacity:1,content:'"\u2022"',animation:"none",color:r.colors.gray,margin:"0 5px"}}:{}),n?{color:r.colors.red,animationName:"".concat(c),animationDuration:"0.5s",animationIterationCount:5}:{})}),""),p=n(46417),f=function(e){var t=e.dirty,n=e.value,r=e.maxLength,a=e.className,u=e.type,l=[],c=function(e){var t=arguments.length>1&&void 0!==arguments[1]&&arguments[1];l.push((0,p.jsx)(s,{includeDot:l.length>0,shouldBlink:t,children:e},l.length))};return t&&("multiline"===(void 0===u?"single":u)?(0,o.Ge)()?c("Press \u2318+Enter to apply"):c("Press Ctrl+Enter to apply"):c("Press Enter to apply")),r&&c("".concat(n.length,"/").concat(r),t&&n.length>=r),(0,p.jsx)(i.X7,{className:a,children:l})}},14628:function(e,t,n){n.r(t),n.d(t,{default:function(){return g}});var r=n(15671),o=n(43144),i=n(60136),a=n(29388),u=n(47313),l=n(3208),c=n(7976),s=n(46332),p=n(75006),f=n(65167),d=n(73290),y=n(80213),h=n(64243),m=(0,n(47167).Z)("div",{target:"edfmue0"})((function(e){e.theme;return{position:"relative",width:e.width}}),""),b=n(46417),v=function(e){(0,i.Z)(n,e);var t=(0,a.Z)(n);function n(){var e;(0,r.Z)(this,n);for(var o=arguments.length,i=new Array(o),a=0;a<o;a++)i[a]=arguments[a];return(e=t.call.apply(t,[this].concat(i))).formClearHelper=new s.Kz,e.state={dirty:!1,value:e.initialValue},e.commitWidgetValue=function(t){e.props.widgetMgr.setStringValue(e.props.element,e.state.value,t),e.setState({dirty:!1})},e.onFormCleared=function(){e.setState((function(e,t){return{value:t.element.default}}),(function(){return e.commitWidgetValue({fromUi:!0})}))},e.onBlur=function(){e.state.dirty&&e.commitWidgetValue({fromUi:!0})},e.onChange=function(t){var n=t.target.value,r=e.props.element.maxChars;0!==r&&n.length>r||((0,h.$b)(e.props.element)?e.setState({dirty:!1,value:n},(function(){return e.commitWidgetValue({fromUi:!0})})):e.setState({dirty:!0,value:n}))},e.onKeyPress=function(t){"Enter"===t.key&&e.state.dirty&&e.commitWidgetValue({fromUi:!0})},e}return(0,o.Z)(n,[{key:"initialValue",get:function(){var e=this.props.widgetMgr.getStringValue(this.props.element);return void 0!==e?e:this.props.element.default}},{key:"componentDidMount",value:function(){this.props.element.setValue?this.updateFromProtobuf():this.commitWidgetValue({fromUi:!1})}},{key:"componentDidUpdate",value:function(){this.maybeUpdateFromProtobuf()}},{key:"componentWillUnmount",value:function(){this.formClearHelper.disconnect()}},{key:"maybeUpdateFromProtobuf",value:function(){this.props.element.setValue&&this.updateFromProtobuf()}},{key:"updateFromProtobuf",value:function(){var e=this,t=this.props.element.value;this.props.element.setValue=!1,this.setState({value:t},(function(){e.commitWidgetValue({fromUi:!1})}))}},{key:"getTypeString",value:function(){return this.props.element.type===c.oi.Type.PASSWORD?"password":"text"}},{key:"render",value:function(){var e,t=this.state,n=t.dirty,r=t.value,o=this.props,i=o.element,a=o.width,u=o.disabled,c=o.widgetMgr,s=i.placeholder;return this.formClearHelper.manageFormClearListener(c,i.formId,this.onFormCleared),(0,b.jsxs)(m,{className:"row-widget stTextInput",width:a,children:[(0,b.jsx)(f.ON,{label:i.label,disabled:u,labelVisibility:(0,h.iF)(null===(e=i.labelVisibility)||void 0===e?void 0:e.value),children:i.help&&(0,b.jsx)(f.dT,{children:(0,b.jsx)(d.Z,{content:i.help,placement:y.ug.TOP_RIGHT})})}),(0,b.jsx)(l.Z,{value:r,placeholder:s,onBlur:this.onBlur,onChange:this.onChange,onKeyPress:this.onKeyPress,"aria-label":i.label,disabled:u,type:this.getTypeString(),autoComplete:i.autocomplete,overrides:{Input:{style:{minWidth:0,"::placeholder":{opacity:"0.7"},lineHeight:"1.4",paddingRight:".5rem",paddingLeft:".5rem",paddingBottom:".5rem",paddingTop:".5rem"}},Root:{style:{borderLeftWidth:"1px",borderRightWidth:"1px",borderTopWidth:"1px",borderBottomWidth:"1px"}}}}),(0,b.jsx)(p.Z,{dirty:n,value:r,maxLength:i.maxChars})]})}}]),n}(u.PureComponent),g=v},3208:function(e,t,n){var r=n(47313),o=n(74969),i=n(84886),a=n(53998),u=n(12903),l=n(37613);function c(e){return c="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},c(e)}var s=["Root","StartEnhancer","EndEnhancer"],p=["startEnhancer","endEnhancer","overrides"];function f(){return f=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},f.apply(this,arguments)}function d(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!==typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==n)return;var r,o,i=[],a=!0,u=!1;try{for(n=n.call(e);!(a=(r=n.next()).done)&&(i.push(r.value),!t||i.length!==t);a=!0);}catch(l){u=!0,o=l}finally{try{a||null==n.return||n.return()}finally{if(u)throw o}}return i}(e,t)||function(e,t){if(!e)return;if("string"===typeof e)return y(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);"Object"===n&&e.constructor&&(n=e.constructor.name);if("Map"===n||"Set"===n)return Array.from(e);if("Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return y(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function y(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function h(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}function m(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function b(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function v(e,t){return v=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(e,t){return e.__proto__=t,e},v(e,t)}function g(e){var t=function(){if("undefined"===typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"===typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=O(e);if(t){var o=O(this).constructor;n=Reflect.construct(r,arguments,o)}else n=r.apply(this,arguments);return w(this,n)}}function w(e,t){if(t&&("object"===c(t)||"function"===typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return j(e)}function j(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function O(e){return O=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},O(e)}function P(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var S=function(e){!function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),Object.defineProperty(e,"prototype",{writable:!1}),t&&v(e,t)}(w,e);var t,n,c,y=g(w);function w(){var e;m(this,w);for(var t=arguments.length,n=new Array(t),r=0;r<t;r++)n[r]=arguments[r];return P(j(e=y.call.apply(y,[this].concat(n))),"state",{isFocused:e.props.autoFocus||!1}),P(j(e),"onFocus",(function(t){e.setState({isFocused:!0}),e.props.onFocus(t)})),P(j(e),"onBlur",(function(t){e.setState({isFocused:!1}),e.props.onBlur(t)})),e}return t=w,(n=[{key:"render",value:function(){var e=this.props,t=e.startEnhancer,n=e.endEnhancer,c=e.overrides,y=c.Root,m=c.StartEnhancer,b=c.EndEnhancer,v=h(c,s),g=h(e,p),w=d((0,o.jb)(y,u.fC),2),j=w[0],O=w[1],P=d((0,o.jb)(m,u.Fp),2),S=P[0],C=P[1],F=d((0,o.jb)(b,u.Fp),2),k=F[0],V=F[1],B=(0,i.t)(this.props,this.state);return r.createElement(j,f({"data-baseweb":"input"},B,O,{$adjoined:E(t,n),$hasIconTrailing:this.props.clearable||"password"==this.props.type}),x(t)&&r.createElement(S,f({},B,C,{$position:l.Xf.start}),"function"===typeof t?t(B):t),r.createElement(a.Z,f({},g,{overrides:v,adjoined:E(t,n),onFocus:this.onFocus,onBlur:this.onBlur})),x(n)&&r.createElement(k,f({},B,V,{$position:l.Xf.end}),"function"===typeof n?n(B):n))}}])&&b(t.prototype,n),c&&b(t,c),Object.defineProperty(t,"prototype",{writable:!1}),w}(r.Component);function E(e,t){return x(e)&&x(t)?l.y4.both:x(e)?l.y4.left:x(t)?l.y4.right:l.y4.none}function x(e){return Boolean(e||0===e)}P(S,"defaultProps",{autoComplete:"on",autoFocus:!1,disabled:!1,name:"",onBlur:function(){},onFocus:function(){},overrides:{},required:!1,size:l.NO.default,startEnhancer:null,endEnhancer:null,clearable:!1,type:"text",readOnly:!1}),t.Z=S}}]);
(self.webpackChunktest_blog=self.webpackChunktest_blog||[]).push([[7],{4070:function(e){"use strict";function t(e){if("string"!=typeof e)throw new TypeError("Path must be a string. Received "+JSON.stringify(e))}function r(e,t){for(var r,n="",a=0,o=-1,i=0,s=0;s<=e.length;++s){if(s<e.length)r=e.charCodeAt(s);else{if(47===r)break;r=47}if(47===r){if(o===s-1||1===i);else if(o!==s-1&&2===i){if(n.length<2||2!==a||46!==n.charCodeAt(n.length-1)||46!==n.charCodeAt(n.length-2))if(n.length>2){var l=n.lastIndexOf("/");if(l!==n.length-1){-1===l?(n="",a=0):a=(n=n.slice(0,l)).length-1-n.lastIndexOf("/"),o=s,i=0;continue}}else if(2===n.length||1===n.length){n="",a=0,o=s,i=0;continue}t&&(n.length>0?n+="/..":n="..",a=2)}else n.length>0?n+="/"+e.slice(o+1,s):n=e.slice(o+1,s),a=s-o-1;o=s,i=0}else 46===r&&-1!==i?++i:i=-1}return n}var n={resolve:function(){for(var e,n="",a=!1,o=arguments.length-1;o>=-1&&!a;o--){var i;o>=0?i=arguments[o]:(void 0===e&&(e=process.cwd()),i=e),t(i),0!==i.length&&(n=i+"/"+n,a=47===i.charCodeAt(0))}return n=r(n,!a),a?n.length>0?"/"+n:"/":n.length>0?n:"."},normalize:function(e){if(t(e),0===e.length)return".";var n=47===e.charCodeAt(0),a=47===e.charCodeAt(e.length-1);return 0!==(e=r(e,!n)).length||n||(e="."),e.length>0&&a&&(e+="/"),n?"/"+e:e},isAbsolute:function(e){return t(e),e.length>0&&47===e.charCodeAt(0)},join:function(){if(0===arguments.length)return".";for(var e,r=0;r<arguments.length;++r){var a=arguments[r];t(a),a.length>0&&(void 0===e?e=a:e+="/"+a)}return void 0===e?".":n.normalize(e)},relative:function(e,r){if(t(e),t(r),e===r)return"";if((e=n.resolve(e))===(r=n.resolve(r)))return"";for(var a=1;a<e.length&&47===e.charCodeAt(a);++a);for(var o=e.length,i=o-a,s=1;s<r.length&&47===r.charCodeAt(s);++s);for(var l=r.length-s,g=i<l?i:l,c=-1,h=0;h<=g;++h){if(h===g){if(l>g){if(47===r.charCodeAt(s+h))return r.slice(s+h+1);if(0===h)return r.slice(s+h)}else i>g&&(47===e.charCodeAt(a+h)?c=h:0===h&&(c=0));break}var f=e.charCodeAt(a+h);if(f!==r.charCodeAt(s+h))break;47===f&&(c=h)}var u="";for(h=a+c+1;h<=o;++h)h!==o&&47!==e.charCodeAt(h)||(0===u.length?u+="..":u+="/..");return u.length>0?u+r.slice(s+c):(s+=c,47===r.charCodeAt(s)&&++s,r.slice(s))},_makeLong:function(e){return e},dirname:function(e){if(t(e),0===e.length)return".";for(var r=e.charCodeAt(0),n=47===r,a=-1,o=!0,i=e.length-1;i>=1;--i)if(47===(r=e.charCodeAt(i))){if(!o){a=i;break}}else o=!1;return-1===a?n?"/":".":n&&1===a?"//":e.slice(0,a)},basename:function(e,r){if(void 0!==r&&"string"!=typeof r)throw new TypeError('"ext" argument must be a string');t(e);var n,a=0,o=-1,i=!0;if(void 0!==r&&r.length>0&&r.length<=e.length){if(r.length===e.length&&r===e)return"";var s=r.length-1,l=-1;for(n=e.length-1;n>=0;--n){var g=e.charCodeAt(n);if(47===g){if(!i){a=n+1;break}}else-1===l&&(i=!1,l=n+1),s>=0&&(g===r.charCodeAt(s)?-1==--s&&(o=n):(s=-1,o=l))}return a===o?o=l:-1===o&&(o=e.length),e.slice(a,o)}for(n=e.length-1;n>=0;--n)if(47===e.charCodeAt(n)){if(!i){a=n+1;break}}else-1===o&&(i=!1,o=n+1);return-1===o?"":e.slice(a,o)},extname:function(e){t(e);for(var r=-1,n=0,a=-1,o=!0,i=0,s=e.length-1;s>=0;--s){var l=e.charCodeAt(s);if(47!==l)-1===a&&(o=!1,a=s+1),46===l?-1===r?r=s:1!==i&&(i=1):-1!==r&&(i=-1);else if(!o){n=s+1;break}}return-1===r||-1===a||0===i||1===i&&r===a-1&&r===n+1?"":e.slice(r,a)},format:function(e){if(null===e||"object"!=typeof e)throw new TypeError('The "pathObject" argument must be of type Object. Received type '+typeof e);return function(e,t){var r=t.dir||t.root,n=t.base||(t.name||"")+(t.ext||"");return r?r===t.root?r+n:r+e+n:n}("/",e)},parse:function(e){t(e);var r={root:"",dir:"",base:"",ext:"",name:""};if(0===e.length)return r;var n,a=e.charCodeAt(0),o=47===a;o?(r.root="/",n=1):n=0;for(var i=-1,s=0,l=-1,g=!0,c=e.length-1,h=0;c>=n;--c)if(47!==(a=e.charCodeAt(c)))-1===l&&(g=!1,l=c+1),46===a?-1===i?i=c:1!==h&&(h=1):-1!==i&&(h=-1);else if(!g){s=c+1;break}return-1===i||-1===l||0===h||1===h&&i===l-1&&i===s+1?-1!==l&&(r.base=r.name=0===s&&o?e.slice(1,l):e.slice(s,l)):(0===s&&o?(r.name=e.slice(1,i),r.base=e.slice(1,l)):(r.name=e.slice(s,i),r.base=e.slice(s,l)),r.ext=e.slice(i,l)),s>0?r.dir=e.slice(0,s-1):o&&(r.dir="/"),r},sep:"/",delimiter:":",win32:null,posix:null};n.posix=n,e.exports=n},8072:function(e,t,r){var n=r(4070);e.exports={siteMetadata:{title:"Notion2Gatsby",description:"Transform any Notion pages to Gatsby static sites",author:"Indosaram",siteUrl:"https://Indosaram.github.io"},pathPrefix:"notion2gatsby",plugins:[{resolve:"gatsby-plugin-google-analytics",options:{trackingId:"UA-178749604-1"}},{resolve:"gatsby-plugin-google-adsense",options:{publisherId:"ca-pub-xxxxxxxxxx"}},"gatsby-plugin-dark-mode","gatsby-plugin-emotion",{resolve:"gatsby-source-filesystem",options:{name:"blog-posts",path:n.join("/","content","blog")}},{resolve:"gatsby-source-filesystem",options:{name:"pages",path:n.join("/","src","pages")}},{resolve:"gatsby-source-filesystem",options:{name:"images",path:n.join("/","src","images")}},"gatsby-plugin-sharp","gatsby-transformer-sharp",{resolve:"gatsby-transformer-remark",options:{plugins:["gatsby-remark-embed-video","gatsby-remark-responsive-iframe",{resolve:"gatsby-remark-images",options:{maxWidth:680}},{resolve:"gatsby-remark-table-of-contents",options:{tight:!1,ordered:!1,fromHeading:2,toHeading:4}},"gatsby-remark-autolink-headers","gatsby-remark-prismjs"]}},{resolve:"gatsby-plugin-typography",options:{pathToConfigModule:"src/utils/typography"}},"gatsby-plugin-catch-links","gatsby-plugin-react-helmet"]}},223:function(e,t,r){"use strict";r.r(t),r.d(t,{default:function(){return c}});r(7294);var n=r(5004),a=r(3964),o=r(5713),i=r(5444),s=r(9843),l=r(8072);var g={name:"u5gtp",styles:"text-decoration:none;color:inherit;&:hover{text-decoration-color:var(--textTitle);}"};function c(e){var t=e.data,r=e.location;return(0,a.tZ)(n.Z,null,(0,a.tZ)(s.Z,{title:l.siteMetadata.title,description:l.siteMetadata.description,pathname:r.pathname}),(0,a.tZ)("main",null,t.allMarkdownRemark.edges.map((function(e){var t=e.node;return(0,a.tZ)("article",{key:t.fields.slug,css:(0,a.iv)("margin-bottom:",(0,o.q)(2),";")},(0,a.tZ)("header",null,(0,a.tZ)(i.Link,{to:"/blog"+t.fields.slug,css:g},(0,a.tZ)("h3",{css:(0,a.iv)("margin-bottom:",(0,o.q)(1/4),";")},t.frontmatter.title," ")),(0,a.tZ)("small",null,t.frontmatter.date)),(0,a.tZ)("p",null,t.frontmatter.description))}))))}}}]);
//# sourceMappingURL=component---src-pages-blog-js-09639d0f0edd821ba8bb.js.map
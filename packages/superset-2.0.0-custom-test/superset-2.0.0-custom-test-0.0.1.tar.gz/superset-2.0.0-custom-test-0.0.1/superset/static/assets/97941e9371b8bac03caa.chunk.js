"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[3126],{96989:(t,e,n)=>{n.r(e),n.d(e,{default:()=>Q});var r=n(5872),i=n.n(r),o=n(67294);function l(t,e){let n;if(void 0===e)for(const e of t)null!=e&&(n<e||void 0===n&&e>=e)&&(n=e);else{let r=-1;for(let i of t)null!=(i=e(i,++r,t))&&(n<i||void 0===n&&i>=i)&&(n=i)}return n}var a=n(4459),s=n(63326),c=n(6609),u=n(88889),d=n(61988),g=n(51115),h=n(5364),p=n(55786),m=n(51995),f=n(79521),v=n(90233),y=n(26635);n(35666);var b=n(11965);function w({count:t,value:e,onChange:n}){return(0,b.tZ)("span",{className:"dt-global-filter"},"Search"," ",(0,b.tZ)("input",{className:"form-control input-sm",placeholder:`${t} records...`,value:e,onChange:n}))}const k=o.memo((function({preGlobalFilteredRows:t,filterValue:e="",searchInput:n,setGlobalFilter:r}){const i=t.length,[l,a]=function(t,e,n=200){const[r,i]=(0,o.useState)(t),l=(0,o.useRef)(t),a=(0,f.useAsyncDebounce)(e,n);return l.current!==t&&(l.current=t,r!==t&&i(t)),[r,t=>{i(t),a(t)}]}(e,(t=>{r(t||void 0)}),200),s=n||w;return(0,b.tZ)(s,{count:i,value:l,onChange:t=>{const e=t.target;t.preventDefault(),a(e.value)}})}));var S=n(6126);function C({current:t,options:e,onChange:n}){return(0,b.tZ)("span",{className:"dt-select-page-size form-inline"},(0,d.t)("Show")," ",(0,b.tZ)("select",{className:"form-control input-sm",value:t,onBlur:()=>{},onChange:t=>{n(Number(t.target.value))}},e.map((t=>{const[e,n]=Array.isArray(t)?t:[t,t];return(0,b.tZ)("option",{key:e,value:e},n)})))," ",(0,d.t)("entries"))}function Z(t){return Array.isArray(t)?t[0]:t}const N=o.memo((function({total:t,options:e,current:n,selectRenderer:r,onChange:i}){const o=e.map(Z);let l=[...e];void 0===n||n===t&&o.includes(0)||o.includes(n)||(l=[...e],l.splice(o.findIndex((t=>t>n)),0,(0,S.m)([n])[0]));const a=void 0===n?o[0]:n,s=r||C;return(0,b.tZ)(s,{current:a,options:l,onChange:i})})),P=o.memo((0,o.forwardRef)((function({style:t,pageCount:e,currentPage:n=0,maxPageItemCount:r=9,onPageChange:i},o){const l=function(t,e,n){if(n<7)throw new Error("Must allow at least 7 page items");if(n%2==0)throw new Error("Must allow odd number of page items");if(t<n)return[...new Array(t).keys()];const r=Math.max(0,Math.min(t-n,e-Math.floor(n/2))),i=new Array(n);for(let t=0;t<n;t+=1)i[t]=t+r;return i[0]>0&&(i[0]=0,i[1]="prev-more"),i[i.length-1]<t-1&&(i[i.length-1]=t-1,i[i.length-2]="next-more"),i}(e,n,r);return(0,b.tZ)("div",{ref:o,className:"dt-pagination",style:t},(0,b.tZ)("ul",{className:"pagination pagination-sm"},l.map((t=>"number"==typeof t?(0,b.tZ)("li",{key:t,className:n===t?"active":void 0},(0,b.tZ)("a",{href:`#page-${t}`,role:"button",onClick:e=>{e.preventDefault(),i(t)}},t+1)):(0,b.tZ)("li",{key:t,className:"dt-pagination-ellipsis"},(0,b.tZ)("span",null,"…"))))))})));let R;const x=t=>t.join("\n");function M(t=!1){if("undefined"==typeof document)return 0;if(void 0===R||t){const t=document.createElement("div"),e=document.createElement("div");t.style.cssText=x`
      width: auto;
      height: 100%;
      overflow: scroll;
    `,e.style.cssText=x`
      position: absolute;
      visibility: hidden;
      overflow: hidden;
      width: 100px;
      height: 50px;
    `,e.append(t),document.body.append(e),R=e.clientWidth-t.clientWidth,e.remove()}return R}var T;!function(t){t.init="init",t.setStickyState="setStickyState"}(T||(T={}));const z=(t,e)=>t+e,$=(t,e)=>({style:{...t.props.style,...e}}),D={tableLayout:"fixed"};function A({sticky:t={},width:e,height:n,children:r,setStickyState:i}){if(!r||"table"!==r.type)throw new Error("<StickyWrap> must have only one <table> element as child");let l,a,s;if(o.Children.forEach(r.props.children,(t=>{t&&("thead"===t.type?l=t:"tbody"===t.type?a=t:"tfoot"===t.type&&(s=t))})),!l||!a)throw new Error("<table> in <StickyWrap> must contain both thead and tbody.");const c=(0,o.useMemo)((()=>{var t;return o.Children.toArray(null==(t=l)?void 0:t.props.children).pop().props.children.length}),[l]),u=(0,o.useRef)(null),d=(0,o.useRef)(null),g=(0,o.useRef)(null),h=(0,o.useRef)(null),p=(0,o.useRef)(null),m=M(),{bodyHeight:f,columnWidths:v}=t,y=!v||t.width!==e||t.height!==n||t.setStickyState!==i;let w,k,S,C;if((0,o.useLayoutEffect)((()=>{if(!u.current)return;const t=u.current,r=t.clientHeight,o=d.current?d.current.clientHeight:0;if(!r)return;const l=t.parentNode.clientHeight,a=t.childNodes[0].childNodes,s=Array.from(a).map((t=>{var e;return(null==(e=t.getBoundingClientRect())?void 0:e.width)||t.clientWidth})),[c,g]=function({width:t,height:e,innerHeight:n,innerWidth:r,scrollBarSize:i}){const o=n>e;return[o,r>t-(o?i:0)]}({width:e,height:n-r-o,innerHeight:l,innerWidth:s.reduce(z),scrollBarSize:m}),h=Math.min(n,g?l+m:l);i({hasVerticalScroll:c,hasHorizontalScroll:g,setStickyState:i,width:e,height:n,realHeight:h,tableHeight:l,bodyHeight:h-r-o,columnWidths:s})}),[e,n,i,m]),y){const t=o.cloneElement(l,{ref:u}),e=s&&o.cloneElement(s,{ref:d});w=(0,b.tZ)("div",{key:"sizer",style:{height:n,overflow:"auto",visibility:"hidden"}},o.cloneElement(r,{},t,a,e))}const Z=null==v?void 0:v.slice(0,c);if(Z&&f){const e=(0,b.tZ)("colgroup",null,Z.map(((t,e)=>(0,b.tZ)("col",{key:e,width:t})))),n=t.hasVerticalScroll&&m?(0,b.tZ)("colgroup",null,Z.map(((t,e)=>(0,b.tZ)("col",{key:e,width:t+(e===Z.length-1?m:0)})))):e;k=(0,b.tZ)("div",{key:"header",ref:g,style:{overflow:"hidden"}},o.cloneElement(r,$(r,D),n,l),k),S=s&&(0,b.tZ)("div",{key:"footer",ref:h,style:{overflow:"hidden"}},o.cloneElement(r,$(r,D),n,s),S);const i=t=>{g.current&&(g.current.scrollLeft=t.currentTarget.scrollLeft),h.current&&(h.current.scrollLeft=t.currentTarget.scrollLeft)};C=(0,b.tZ)("div",{key:"body",ref:p,style:{height:f,overflow:"auto"},onScroll:t.hasHorizontalScroll?i:void 0},o.cloneElement(r,$(r,D),e,a))}return(0,b.tZ)("div",{style:{width:e,height:t.realHeight||n,overflow:"hidden"}},k,C,S,w)}function E(t){const{dispatch:e,state:{sticky:n},data:r,page:i,rows:l,allColumns:a,getTableSize:s=(()=>{})}=t,c=(0,o.useCallback)((t=>{e({type:T.setStickyState,size:t})}),[e,s,i,l]);Object.assign(t,{setStickyState:c,wrapStickyTable:t=>{const{width:e,height:u}=function(t,e){const n=(0,o.useRef)();return(0,o.useLayoutEffect)((()=>{n.current=t})),(0,o.useMemo)((()=>{if(n.current)return t()}),[n.current,n.current===t,...e||[]])}(s,[s])||n,d=(0,o.useMemo)(t,[i,l,a]);return(0,o.useLayoutEffect)((()=>{e&&u||c()}),[e,u]),e&&u?0===r.length?d:(0,b.tZ)(A,{width:e,height:u,sticky:n,setStickyState:c},d):null}})}function F(t){t.useInstance.push(E),t.stateReducers.push(((t,e,n)=>{const r=e;if(r.type===T.init)return{...t,sticky:{...null==n?void 0:n.sticky}};if(r.type===T.setStickyState){const{size:e}=r;return e?{...t,sticky:{...null==n?void 0:n.sticky,...null==t?void 0:t.sticky,...r.size}}:{...t}}return t}))}F.pluginName="useSticky";var H=n(2608);const I={alphanumeric:(t,e,n)=>{const r=t.values[n],i=e.values[n];return r&&"string"==typeof r?i&&"string"==typeof i?r.localeCompare(i):1:-1}},L=(0,y.l)((function({tableClassName:t,columns:e,data:n,serverPaginationData:r,width:l="100%",height:a=300,pageSize:s=0,initialState:c={},pageSizeOptions:u=H.T,maxPageItemCount:d=9,sticky:g,searchInput:h=!0,onServerPaginationChange:p,rowCount:m,selectPageSize:y,noResults:w="No data found",hooks:S,serverPagination:C,wrapperRef:Z,onColumnOrderChange:R,...x}){const M=[f.useGlobalFilter,f.useSortBy,f.usePagination,f.useColumnOrder,g?F:[],S||[]].flat(),T=C?m:n.length,z=(0,o.useRef)([]),$=(0,o.useRef)([s,T]),D=s>0&&T>0,A=D||!!h,E={...c,sortBy:z.current,pageSize:s>0?s:T||10},L=(0,o.useRef)(null),W=(0,o.useRef)(null),O=(0,o.useRef)(null),B=Z||L,G=JSON.stringify(r),j=(0,o.useCallback)((()=>{var t,e;if(B.current)return{width:Number(l)||B.current.clientWidth,height:(Number(a)||B.current.clientHeight)-((null==(t=W.current)?void 0:t.clientHeight)||0)-((null==(e=O.current)?void 0:e.clientHeight)||0)}}),[a,l,B,D,A,O,T,G]),V=(0,o.useCallback)(((t,e,n)=>(0,v.Lu)(t,n,{keys:[...e,t=>e.map((e=>t.values[e])).join(" ")],threshold:v.tL.ACRONYM})),[]),{getTableProps:_,getTableBodyProps:U,prepareRow:J,headerGroups:K,footerGroups:X,page:Y,pageCount:q,gotoPage:Q,preGlobalFilteredRows:tt,setGlobalFilter:et,setPageSize:nt,wrapStickyTable:rt,setColumnOrder:it,allColumns:ot,state:{pageIndex:lt,pageSize:at,globalFilter:st,sticky:ct={}}}=(0,f.useTable)({columns:e,data:n,initialState:E,getTableSize:j,globalFilter:V,sortTypes:I,...x},...M),ut=t=>{C&&p(0,t),(t||0!==T)&&nt(0===t?T:t)},dt="function"==typeof w?w(st):w,gt=()=>(0,b.tZ)("div",{className:"dt-no-results"},dt);if(!e||0===e.length)return rt?rt(gt):gt();const ht=e.some((t=>!!t.Footer));let pt=-1;const mt=t=>{const e=t.target;pt=ot.findIndex((t=>t.id===e.dataset.columnName)),t.dataTransfer.setData("text/plain",`${pt}`)},ft=t=>{const e=t.target,n=ot.findIndex((t=>t.id===e.dataset.columnName));if(-1!==n){const t=ot.map((t=>t.id)),e=t.splice(pt,1);t.splice(n,0,e[0]),it(t),R()}t.preventDefault()},vt=()=>(0,b.tZ)("table",_({className:t}),(0,b.tZ)("thead",null,K.map((t=>{const{key:e,...n}=t.getHeaderGroupProps();return(0,b.tZ)("tr",i()({key:e||t.id},n),t.headers.map((t=>t.render("Header",{key:t.id,...t.getSortByToggleProps(),onDragStart:mt,onDrop:ft}))))}))),(0,b.tZ)("tbody",U(),Y&&Y.length>0?Y.map((t=>{J(t);const{key:e,...n}=t.getRowProps();return(0,b.tZ)("tr",i()({key:e||t.id},n),t.cells.map((t=>t.render("Cell",{key:t.column.id}))))})):(0,b.tZ)("tr",null,(0,b.tZ)("td",{className:"dt-no-results",colSpan:e.length},dt))),ht&&(0,b.tZ)("tfoot",null,X.map((t=>{const{key:e,...n}=t.getHeaderGroupProps();return(0,b.tZ)("tr",i()({key:e||t.id},n),t.headers.map((t=>t.render("Footer",{key:t.id}))))}))));($.current[0]!==s||0===s&&$.current[1]!==T)&&($.current=[s,T],ut(s));const yt=ct.height?{}:{visibility:"hidden"};let bt=q,wt=at,kt=lt,St=Q;if(C){var Ct,Zt;const t=null!=(Ct=null==r?void 0:r.pageSize)?Ct:s;bt=Math.ceil(m/t),Number.isFinite(bt)||(bt=0),wt=t,-1===u.findIndex((([t])=>t>=wt))&&(wt=0),kt=null!=(Zt=null==r?void 0:r.currentPage)?Zt:0,St=e=>p(e,t)}return(0,b.tZ)("div",{ref:B,style:{width:l,height:a}},A?(0,b.tZ)("div",{ref:W,className:"form-inline dt-controls"},(0,b.tZ)("div",{className:"row"},(0,b.tZ)("div",{className:"col-sm-6"},D?(0,b.tZ)(N,{total:T,current:wt,options:u,selectRenderer:"boolean"==typeof y?void 0:y,onChange:ut}):null),h?(0,b.tZ)("div",{className:"col-sm-6"},(0,b.tZ)(k,{searchInput:"boolean"==typeof h?void 0:h,preGlobalFilteredRows:tt,setGlobalFilter:et,filterValue:st})):null)):null,rt?rt(vt):vt(),D&&bt>1?(0,b.tZ)(P,{ref:O,style:yt,maxPageItemCount:d,pageCount:bt,currentPage:kt,onPageChange:St}):null)})),W=m.iK.div`
  ${({theme:t})=>b.iv`
    table {
      width: 100%;
      min-width: auto;
      max-width: none;
      margin: 0;
    }

    th,
    td {
      min-width: 4.3em;
    }

    thead > tr > th {
      padding-right: 0;
      position: relative;
      background: ${t.colors.grayscale.light5};
      text-align: left;
    }
    th svg {
      color: ${t.colors.grayscale.light2};
      margin: ${t.gridUnit/2}px;
    }
    th.is-sorted svg {
      color: ${t.colors.grayscale.base};
    }
    .table > tbody > tr:first-of-type > td,
    .table > tbody > tr:first-of-type > th {
      border-top: 0;
    }

    .table > tbody tr td {
      font-feature-settings: 'tnum' 1;
    }

    .dt-controls {
      padding-bottom: 0.65em;
    }
    .dt-metric {
      text-align: right;
    }
    .dt-totals {
      font-weight: ${t.typography.weights.bold};
    }
    .dt-is-null {
      color: ${t.colors.grayscale.light1};
    }
    td.dt-is-filter {
      cursor: pointer;
    }
    td.dt-is-filter:hover {
      background-color: ${t.colors.secondary.light4};
    }
    td.dt-is-active-filter,
    td.dt-is-active-filter:hover {
      background-color: ${t.colors.secondary.light3};
    }

    .dt-global-filter {
      float: right;
    }

    .dt-pagination {
      text-align: right;
      /* use padding instead of margin so clientHeight can capture it */
      padding-top: 0.5em;
    }
    .dt-pagination .pagination {
      margin: 0;
    }

    .pagination > li > span.dt-pagination-ellipsis:focus,
    .pagination > li > span.dt-pagination-ellipsis:hover {
      background: ${t.colors.grayscale.light5};
    }

    .dt-no-results {
      text-align: center;
      padding: 1em 0.6em;
    }
  `}
`;var O=n(68924),B=n(67190),G=n(57790);const j=new O.FilterXSS({whiteList:{...(0,O.getDefaultWhiteList)(),span:["style","class","title"],div:["style","class"],a:["style","class","href","title","target"],img:["style","class","src","alt","title","width","height"],video:["autoplay","controls","loop","preload","src","height","width","muted"]},stripIgnoreTag:!0,css:!1});function V(t,e){const{dataType:n,formatter:r,config:i={}}=t,o=n===u.Z.NUMERIC,l=void 0===i.d3SmallNumberFormat?r:(0,B.JB)(i.d3SmallNumberFormat);return function(t,e){return void 0===e?[!1,""]:null===e||e instanceof G.Z&&null===e.input?[!1,"N/A"]:t?[!1,t(e)]:"string"==typeof e?/<[^>]+>/.test(e)?[!0,j.process(e)]:[!1,e]:[!1,e.toString()]}(o&&"number"==typeof e&&Math.abs(e)<1?l:r,e)}var _=n(12456);function U(t){return t===u.Z.TEMPORAL?"datetime":t===u.Z.STRING?"alphanumeric":"basic"}function J({column:t}){const{isSorted:e,isSortedDesc:n}=t;let r=(0,b.tZ)(a.r,null);return e&&(r=n?(0,b.tZ)(s.s,null):(0,b.tZ)(c.h,null)),r}function K({count:t,value:e,onChange:n}){return(0,b.tZ)("span",{className:"dt-global-filter"},(0,d.t)("Search")," ",(0,b.tZ)("input",{className:"form-control input-sm",placeholder:(0,d.t)("search.num_records",t),value:e,onChange:n}))}function X({options:t,current:e,onChange:n}){return(0,b.tZ)("span",{className:"dt-select-page-size form-inline"},(0,d.t)("page_size.show")," ",(0,b.tZ)("select",{className:"form-control input-sm",value:e,onBlur:()=>{},onChange:t=>{n(Number(t.target.value))}},t.map((t=>{const[e,n]=Array.isArray(t)?t:[t,t];return(0,b.tZ)("option",{key:e,value:e},n)})))," ",(0,d.t)("page_size.entries"))}const Y=t=>t?(0,d.t)("No matching records found"):(0,d.t)("No records found");var q={name:"tvoj80",styles:"display:inline-flex;align-items:flex-end"};function Q(t){const{timeGrain:e,height:n,width:r,data:a,totals:s,isRawRecords:c,rowCount:u=0,columns:f,alignPositiveNegative:v=!1,colorPositiveNegative:y=!1,includeSearch:w=!1,pageSize:k=0,serverPagination:S=!1,serverPaginationData:C,setDataMask:Z,showCellBars:N=!0,emitFilter:P=!1,sortDesc:R=!1,filters:x,sticky:T=!0,columnColorFormatters:z,allowRearrangeColumns:$=!1}=t,D=(0,o.useCallback)((t=>(0,g.uh)(e)(t)),[e]),[A,E]=(0,o.useState)({width:0,height:0}),[F,I]=(0,o.useState)(!1),O=(0,o.useCallback)((t=>{if(!P)return;const n=Object.keys(t),r=Object.values(t),i=[];n.forEach((e=>{const n=e===h.W3,r=(0,p.Z)(null==t?void 0:t[e]);if(r.length){const t=r.map((t=>n?D(t):t));i.push(`${t.join(", ")}`)}})),Z({extraFormData:{filters:0===n.length?[]:n.map((n=>{const r=(0,p.Z)(null==t?void 0:t[n]);return r.length?{col:n,op:"IN",val:r.map((t=>t instanceof Date?t.getTime():t)),grain:n===h.W3?e:void 0}:{col:n,op:"IS NULL"}}))},filterState:{label:i.join(", "),value:r.length?r:null,filters:t&&Object.keys(t).length?t:null}})}),[P,Z]),B=(0,o.useMemo)((()=>H.T.filter((([t])=>S?(t=>t<=u)(t):t<=2*a.length))),[a.length,u,S]),G=(0,o.useCallback)((function(t,e){var n;if("number"==typeof(null==a||null==(n=a[0])?void 0:n[t])){const n=a.map((e=>e[t]));return e?[0,l(n.map(Math.abs))]:function(t,e){let n,r;for(const e of t)null!=e&&(void 0===n?e>=e&&(n=r=e):(n>e&&(n=e),r<e&&(r=e)));return[n,r]}(n)}return null}),[a]),j=(0,o.useCallback)((function(t,e){var n;return!!x&&(null==(n=x[t])?void 0:n.includes(e))}),[x]),Q=(0,o.useCallback)((function(t,e){let n={...x||{}};const r=function(t){var e;const n=null==f?void 0:f.find((e=>e.key===t));return(null==n||null==(e=n.config)?void 0:e.emitTarget)||t}(t);n=x&&j(r,e)?{}:{[r]:[e]},Array.isArray(n[r])&&0===n[r].length&&delete n[r],O(n)}),[x,O,j]),tt=(0,o.useCallback)(((t,e)=>{const{key:n,label:r,isNumeric:o,dataType:l,isMetric:a,config:u={}}=t,g=Number.isNaN(Number(u.columnWidth))?u.columnWidth:Number(u.columnWidth),h=(t=>{const{isNumeric:e,config:n={}}=t;return{textAlign:n.horizontalAlign?n.horizontalAlign:e?"right":"left"}})(t),p=void 0===u.alignPositiveNegative?v:u.alignPositiveNegative,f=void 0===u.colorPositiveNegative?y:u.colorPositiveNegative,w=o&&Array.isArray(z)&&z.length>0,k=!w&&(void 0===u.showCellBars?N:u.showCellBars)&&(a||c)&&G(n,p);let S="";return P&&(S+=" dt-is-filter"),{id:String(e),accessor:t=>t[n],Cell:({value:e})=>{const[r,o]=V(t,e),l=r?{__html:o}:void 0;let a;w&&z.filter((e=>e.column===t.key)).forEach((t=>{const n=t.getColorFromValue(e);n&&(a=n)}));const s=m.iK.td`
            text-align: ${h.textAlign};
            background: ${a||(k?function({value:t,valueRange:e,colorPositiveNegative:n=!1,alignPositiveNegative:r}){const[i,o]=e,l=n&&t<0?150:0;if(r){const e=Math.abs(Math.round(t/o*100));return`linear-gradient(to right, rgba(${l},0,0,0.2), rgba(${l},0,0,0.2) ${e}%, rgba(0,0,0,0.01) ${e}%, rgba(0,0,0,0.001) 100%)`}const a=Math.abs(Math.max(o,0)),s=Math.abs(Math.min(i,0)),c=a+s,u=Math.round(Math.min(s+t,s)/c*100),d=Math.round(Math.abs(t)/c*100);return`linear-gradient(to right, rgba(0,0,0,0.01), rgba(0,0,0,0.001) ${u}%, rgba(${l},0,0,0.2) ${u}%, rgba(${l},0,0,0.2) ${u+d}%, rgba(0,0,0,0.01) ${u+d}%, rgba(0,0,0,0.001) 100%)`}({value:e,valueRange:k,alignPositiveNegative:p,colorPositiveNegative:f}):void 0)};
            white-space: ${e instanceof Date?"nowrap":void 0};
          `,c={title:"number"==typeof e?String(e):void 0,onClick:P&&!k?()=>Q(n,e):void 0,className:[S,null==e?"dt-is-null":"",j(n,e)?" dt-is-active-filter":""].join(" ")};return l?(0,b.tZ)(s,i()({},c,{dangerouslySetInnerHTML:l})):(0,b.tZ)(s,c,o)},Header:({column:t,onClick:e,style:n,onDragStart:o,onDrop:l})=>(0,b.tZ)("th",i()({title:(0,d.t)("Shift + Click to sort by multiple columns"),className:[S,t.isSorted?"is-sorted":""].join(" "),style:{...h,...n},onClick:e,"data-column-name":t.id},$&&{draggable:"true",onDragStart:o,onDragOver:t=>t.preventDefault(),onDragEnter:t=>t.preventDefault(),onDrop:l}),u.columnWidth?(0,b.tZ)("div",{style:{width:g,height:.01}}):null,(0,b.tZ)("div",{"data-column-name":t.id,css:q},(0,b.tZ)("span",{"data-column-name":t.id},r),(0,b.tZ)(J,{column:t}))),Footer:s?0===e?(0,b.tZ)("th",null,(0,d.t)("Totals")):(0,b.tZ)("td",{style:h},(0,b.tZ)("strong",null,V(t,s[n])[1])):void 0,sortDescFirst:R,sortType:U(l)}}),[v,y,P,G,j,c,N,R,Q,s,z,F]),et=(0,o.useMemo)((()=>f.map(tt)),[f,tt]),nt=(0,o.useCallback)(((t,e)=>{(0,_.X)(Z,t,e)}),[Z]),rt=(0,o.useCallback)((({width:t,height:e})=>{E({width:t,height:e})}),[]);(0,o.useLayoutEffect)((()=>{const t=M(),{width:e,height:i}=A;r-e>t||n-i>t?rt({width:r-t,height:n-t}):(e-r>t||i-n>t)&&rt({width:r,height:n})}),[r,n,rt,A]);const{width:it,height:ot}=A;return(0,b.tZ)(W,null,(0,b.tZ)(L,{columns:et,data:a,rowCount:u,tableClassName:"table table-striped table-condensed",pageSize:k,serverPaginationData:C,pageSizeOptions:B,width:it,height:ot,serverPagination:S,onServerPaginationChange:nt,onColumnOrderChange:()=>I(!F),maxPageItemCount:r>340?9:7,noResults:Y,searchInput:w&&K,selectPageSize:null!==k&&X,sticky:T}))}}}]);
//# sourceMappingURL=97941e9371b8bac03caa.chunk.js.map
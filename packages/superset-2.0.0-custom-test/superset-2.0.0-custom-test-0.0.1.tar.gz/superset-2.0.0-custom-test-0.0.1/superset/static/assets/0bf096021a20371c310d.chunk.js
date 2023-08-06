(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[665],{45578:(e,t,a)=>{var r=a(67206),l=a(45652);e.exports=function(e,t){return e&&e.length?l(e,r(t,2)):[]}},26996:(e,t,a)=>{"use strict";a.d(t,{Z:()=>y});var r=a(67294),l=a(51995),i=a(61988),o=a(35932),n=a(74069),s=a(4715),d=a(34858),c=a(29487),u=a(11965);const p=(0,d.z)(),m=p?p.support:"https://superset.apache.org/docs/databases/installing-database-drivers",h=({errorMessage:e,showDbInstallInstructions:t})=>(0,u.tZ)(c.Z,{closable:!1,css:e=>(e=>u.iv`
  border: 1px solid ${e.colors.warning.light1};
  padding: ${4*e.gridUnit}px;
  margin: ${4*e.gridUnit}px 0;
  color: ${e.colors.warning.dark2};

  .ant-alert-message {
    margin: 0;
  }

  .ant-alert-description {
    font-size: ${e.typography.sizes.s+1}px;
    line-height: ${4*e.gridUnit}px;

    .ant-alert-icon {
      margin-right: ${2.5*e.gridUnit}px;
      font-size: ${e.typography.sizes.l+1}px;
      position: relative;
      top: ${e.gridUnit/4}px;
    }
  }
`)(e),type:"error",showIcon:!0,message:e,description:t?(0,u.tZ)(r.Fragment,null,(0,u.tZ)("br",null),(0,i.t)("Database driver for importing maybe not installed. Visit the Superset documentation page for installation instructions:"),(0,u.tZ)("a",{href:m,target:"_blank",rel:"noopener noreferrer",className:"additional-fields-alert-description"},(0,i.t)("here")),"."):""}),g=l.iK.div`
  display: block;
  color: ${({theme:e})=>e.colors.grayscale.base};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
`,b=l.iK.div`
  padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
  padding-top: ${({theme:e})=>2*e.gridUnit}px;

  & > div {
    margin: ${({theme:e})=>e.gridUnit}px 0;
  }

  &.extra-container {
    padding-top: 8px;
  }

  .confirm-overwrite {
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  .input-container {
    display: flex;
    align-items: center;

    label {
      display: flex;
      margin-right: ${({theme:e})=>2*e.gridUnit}px;
    }

    i {
      margin: 0 ${({theme:e})=>e.gridUnit}px;
    }
  }

  input,
  textarea {
    flex: 1 1 auto;
  }

  textarea {
    height: 160px;
    resize: none;
  }

  input::placeholder,
  textarea::placeholder {
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }

  textarea,
  input[type='text'],
  input[type='number'] {
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    border-style: none;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;

    &[name='name'] {
      flex: 0 1 auto;
      width: 40%;
    }

    &[name='sqlalchemy_uri'] {
      margin-right: ${({theme:e})=>3*e.gridUnit}px;
    }
  }
`,y=({resourceName:e,resourceLabel:t,passwordsNeededMessage:a,confirmOverwriteMessage:l,onModelImport:c,show:p,onHide:m,passwordFields:y=[],setPasswordFields:f=(()=>{})})=>{const[Z,v]=(0,r.useState)(!0),[w,_]=(0,r.useState)({}),[x,S]=(0,r.useState)(!1),[C,$]=(0,r.useState)(!1),[k,E]=(0,r.useState)([]),[T,I]=(0,r.useState)(!1),[z,N]=(0,r.useState)(),H=()=>{E([]),f([]),_({}),S(!1),$(!1),I(!1),N("")},{state:{alreadyExists:D,passwordsNeeded:F},importResource:M}=(0,d.PW)(e,t,(e=>{N(e)}));(0,r.useEffect)((()=>{f(F),F.length>0&&I(!1)}),[F,f]),(0,r.useEffect)((()=>{S(D.length>0),D.length>0&&I(!1)}),[D,S]);return Z&&p&&v(!1),(0,u.tZ)(n.Z,{name:"model",className:"import-model-modal",disablePrimaryButton:0===k.length||x&&!C||T,onHandledPrimaryAction:()=>{var e;(null==(e=k[0])?void 0:e.originFileObj)instanceof File&&(I(!0),M(k[0].originFileObj,w,C).then((e=>{e&&(H(),c())})))},onHide:()=>{v(!0),m(),H()},primaryButtonName:x?(0,i.t)("Overwrite"):(0,i.t)("Import"),primaryButtonType:x?"danger":"primary",width:"750px",show:p,title:(0,u.tZ)("h4",null,(0,i.t)("Import %s",t))},(0,u.tZ)(b,null,(0,u.tZ)(s.gq,{name:"modelFile",id:"modelFile",accept:".yaml,.json,.yml,.zip",fileList:k,onChange:e=>{E([{...e.file,status:"done"}])},onRemove:e=>(E(k.filter((t=>t.uid!==e.uid))),!1),customRequest:()=>{},disabled:T},(0,u.tZ)(o.Z,{loading:T},(0,i.t)("Select file")))),z&&(0,u.tZ)(h,{errorMessage:z,showDbInstallInstructions:y.length>0}),0===y.length?null:(0,u.tZ)(r.Fragment,null,(0,u.tZ)("h5",null,(0,i.t)("Database passwords")),(0,u.tZ)(g,null,a),y.map((e=>(0,u.tZ)(b,{key:`password-for-${e}`},(0,u.tZ)("div",{className:"control-label"},e,(0,u.tZ)("span",{className:"required"},"*")),(0,u.tZ)("input",{name:`password-${e}`,autoComplete:`password-${e}`,type:"password",value:w[e],onChange:t=>_({...w,[e]:t.target.value})}))))),x?(0,u.tZ)(r.Fragment,null,(0,u.tZ)(b,null,(0,u.tZ)("div",{className:"confirm-overwrite"},l),(0,u.tZ)("div",{className:"control-label"},(0,i.t)('Type "%s" to confirm',(0,i.t)("OVERWRITE"))),(0,u.tZ)("input",{id:"overwrite",type:"text",onChange:e=>{var t,a;const r=null!=(t=null==(a=e.currentTarget)?void 0:a.value)?t:"";$(r.toUpperCase()===(0,i.t)("OVERWRITE"))}}))):null)}},13434:(e,t,a)=>{"use strict";a.r(t),a.d(t,{default:()=>O});var r=a(45578),l=a.n(r),i=a(51995),o=a(61988),n=a(11064),s=a(31069),d=a(67294),c=a(15926),u=a.n(c),p=a(91877),m=a(93185),h=a(40768),g=a(34858),b=a(32228),y=a(19259),f=a(20755),Z=a(36674),v=a(18782),w=a(38703),_=a(61337),x=a(14114),S=a(83673),C=a(26996),$=a(58593),k=a(70163),E=a(1510),T=a(34993),I=a(8272),z=a(79789),N=a(34024),H=a(11965);const D=i.iK.div`
  align-items: center;
  display: flex;

  a {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    line-height: 1.2;
  }

  svg {
    margin-right: ${({theme:e})=>e.gridUnit}px;
  }
`,F=(0,o.t)('The passwords for the databases below are needed in order to import them together with the charts. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in export files, and should be added manually after the import if they are needed.'),M=(0,o.t)("You are importing one or more charts that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?");(0,T.Z)();const A=(0,n.Z)(),U=async(e="",t,a)=>{var r;const i=e?{filters:[{col:"table_name",opr:"sw",value:e}]}:{},o=u().encode({columns:["datasource_name","datasource_id"],keys:["none"],order_column:"table_name",order_direction:"asc",page:t,page_size:a,...i}),{json:n={}}=await s.Z.get({endpoint:`/api/v1/dataset/?q=${o}`}),d=null==n||null==(r=n.result)?void 0:r.map((({table_name:e,id:t})=>({label:e,value:t})));return{data:l()(d,"value"),totalCount:null==n?void 0:n.count}},B=i.iK.div`
  color: ${({theme:e})=>e.colors.grayscale.base};
`,O=(0,x.ZP)((function(e){const{addDangerToast:t,addSuccessToast:a,user:{userId:r}}=e,{state:{loading:l,resourceCount:i,resourceCollection:n,bulkSelectEnabled:c},setResourceCollection:x,hasPerm:T,fetchData:O,toggleBulkSelect:L,refreshData:R}=(0,g.Yi)("chart",(0,o.t)("chart"),t),P=(0,d.useMemo)((()=>n.map((e=>e.id))),[n]),[V,q]=(0,g.NE)("chart",P,t),{sliceCurrentlyEditing:j,handleChartUpdated:W,openChartEditModal:K,closeChartEditModal:Y}=(0,g.fF)(x,n),[X,G]=(0,d.useState)(!1),[J,Q]=(0,d.useState)([]),[ee,te]=(0,d.useState)(!1),ae=(0,_.OH)(null==r?void 0:r.toString(),null),re=T("can_write"),le=T("can_write"),ie=T("can_write"),oe=T("can_export")&&(0,p.cr)(m.T.VERSIONED_EXPORT),ne=[{id:"changed_on_delta_humanized",desc:!0}],se=e=>{const t=e.map((({id:e})=>e));(0,b.Z)("chart",t,(()=>{te(!1)})),te(!0)},de=(0,d.useMemo)((()=>[{Cell:({row:{original:{id:e}}})=>r&&(0,H.tZ)(Z.Z,{itemId:e,saveFaveStar:V,isStarred:q[e]}),Header:"",id:"id",disableSortBy:!0,size:"xs",hidden:!r},{Cell:({row:{original:{url:e,slice_name:t,certified_by:a,certification_details:r,description:l}}})=>(0,H.tZ)(D,null,(0,H.tZ)("a",{href:e},a&&(0,H.tZ)(d.Fragment,null,(0,H.tZ)(z.Z,{certifiedBy:a,details:r})," "),(0,H.tZ)($.u,{title:t,id:`chart-name-tooltip-${t}`},t)),l&&(0,H.tZ)(I.Z,{tooltip:l,viewBox:"0 -1 24 24"})),Header:(0,o.t)("Chart"),accessor:"slice_name"},{Cell:({row:{original:{viz_type:e}}})=>{var t;return(null==(t=A.get(e))?void 0:t.name)||e},Header:(0,o.t)("Visualization type"),accessor:"viz_type",size:"xxl"},{Cell:({row:{original:{datasource_name_text:e,datasource_url:t}}})=>(0,H.tZ)("a",{href:t},e),Header:(0,o.t)("Dataset"),accessor:"datasource_id",disableSortBy:!0,size:"xl"},{Cell:({row:{original:{perm:e}}})=>e?e.split(".")[0].replace("[","").replace("]",""):"-",Header:(0,o.t)("Database"),accessor:"perm",disableSortBy:!0,size:"xl"},{Cell:({row:{original:{last_saved_by:e,changed_by_url:t}}})=>(0,H.tZ)("a",{href:t},null!=e&&e.first_name?`${null==e?void 0:e.first_name} ${null==e?void 0:e.last_name}`:null),Header:(0,o.t)("Modified by"),accessor:"last_saved_by.first_name",size:"xl"},{Cell:({row:{original:{changed_on_delta_humanized:e}}})=>(0,H.tZ)("span",{className:"no-wrap"},e),Header:(0,o.t)("Last modified"),accessor:"changed_on_delta_humanized",size:"xl"},{accessor:"owners",hidden:!0,disableSortBy:!0},{Cell:({row:{original:{created_by:e}}})=>e?`${e.first_name} ${e.last_name}`:"",Header:(0,o.t)("Created by"),accessor:"created_by",disableSortBy:!0,size:"xl"},{Cell:({row:{original:e}})=>le||ie||oe?(0,H.tZ)(B,{className:"actions"},ie&&(0,H.tZ)(y.Z,{title:(0,o.t)("Please confirm"),description:(0,H.tZ)(d.Fragment,null,(0,o.t)("Are you sure you want to delete")," ",(0,H.tZ)("b",null,e.slice_name),"?"),onConfirm:()=>(0,h.Gm)(e,a,t,R)},(e=>(0,H.tZ)($.u,{id:"delete-action-tooltip",title:(0,o.t)("Delete"),placement:"bottom"},(0,H.tZ)("span",{role:"button",tabIndex:0,className:"action-button",onClick:e},(0,H.tZ)(k.Z.Trash,null))))),oe&&(0,H.tZ)($.u,{id:"export-action-tooltip",title:(0,o.t)("Export"),placement:"bottom"},(0,H.tZ)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>se([e])},(0,H.tZ)(k.Z.Share,null))),le&&(0,H.tZ)($.u,{id:"edit-action-tooltip",title:(0,o.t)("Edit"),placement:"bottom"},(0,H.tZ)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>K(e)},(0,H.tZ)(k.Z.EditAlt,null)))):null,Header:(0,o.t)("Actions"),id:"actions",disableSortBy:!0,hidden:!le&&!ie}]),[r,le,ie,oe,V,q,R,a,t]),ce=(0,d.useMemo)((()=>({Header:(0,o.t)("Favorite"),id:"id",urlDisplay:"favorite",input:"select",operator:v.p.chartIsFav,unfilteredLabel:(0,o.t)("Any"),selects:[{label:(0,o.t)("Yes"),value:!0},{label:(0,o.t)("No"),value:!1}]})),[]),ue=(0,d.useMemo)((()=>[{Header:(0,o.t)("Owner"),id:"owners",input:"select",operator:v.p.relationManyMany,unfilteredLabel:(0,o.t)("All"),fetchSelects:(0,h.tm)("chart","owners",(0,h.v$)((e=>t((0,o.t)("An error occurred while fetching chart owners values: %s",e)))),e.user),paginate:!0},{Header:(0,o.t)("Created by"),id:"created_by",input:"select",operator:v.p.relationOneMany,unfilteredLabel:(0,o.t)("All"),fetchSelects:(0,h.tm)("chart","created_by",(0,h.v$)((e=>t((0,o.t)("An error occurred while fetching chart created by values: %s",e)))),e.user),paginate:!0},{Header:(0,o.t)("Chart type"),id:"viz_type",input:"select",operator:v.p.equals,unfilteredLabel:(0,o.t)("All"),selects:A.keys().filter((e=>{var t;return(0,E.X3)((null==(t=A.get(e))?void 0:t.behaviors)||[])})).map((e=>{var t;return{label:(null==(t=A.get(e))?void 0:t.name)||e,value:e}})).sort(((e,t)=>e.label&&t.label?e.label>t.label?1:e.label<t.label?-1:0:0))},{Header:(0,o.t)("Dataset"),id:"datasource_id",input:"select",operator:v.p.equals,unfilteredLabel:(0,o.t)("All"),fetchSelects:U,paginate:!0},...r?[ce]:[],{Header:(0,o.t)("Certified"),id:"id",urlDisplay:"certified",input:"select",operator:v.p.chartIsCertified,unfilteredLabel:(0,o.t)("Any"),selects:[{label:(0,o.t)("Yes"),value:!0},{label:(0,o.t)("No"),value:!1}]},{Header:(0,o.t)("Search"),id:"slice_name",input:"search",operator:v.p.chartAllText}]),[t,ce,e.user]),pe=[{desc:!1,id:"slice_name",label:(0,o.t)("Alphabetical"),value:"alphabetical"},{desc:!0,id:"changed_on_delta_humanized",label:(0,o.t)("Recently modified"),value:"recently_modified"},{desc:!1,id:"changed_on_delta_humanized",label:(0,o.t)("Least recently modified"),value:"least_recently_modified"}],me=(0,d.useCallback)((e=>(0,H.tZ)(N.Z,{chart:e,showThumbnails:ae?ae.thumbnails:(0,p.cr)(m.T.THUMBNAILS),hasPerm:T,openChartEditModal:K,bulkSelectEnabled:c,addDangerToast:t,addSuccessToast:a,refreshData:R,userId:r,loading:l,favoriteStatus:q[e.id],saveFavoriteStatus:V,handleBulkChartExport:se})),[t,a,c,q,T,l]),he=[];return(ie||oe)&&he.push({name:(0,o.t)("Bulk select"),buttonStyle:"secondary","data-test":"bulk-select",onClick:L}),re&&(he.push({name:(0,H.tZ)(d.Fragment,null,(0,H.tZ)("i",{className:"fa fa-plus"})," ",(0,o.t)("Chart")),buttonStyle:"primary",onClick:()=>{window.location.assign("/chart/add")}}),(0,p.cr)(m.T.VERSIONED_EXPORT)&&he.push({name:(0,H.tZ)($.u,{id:"import-tooltip",title:(0,o.t)("Import charts"),placement:"bottomRight"},(0,H.tZ)(k.Z.Import,null)),buttonStyle:"link",onClick:()=>{G(!0)}})),(0,H.tZ)(d.Fragment,null,(0,H.tZ)(f.Z,{name:(0,o.t)("Charts"),buttons:he}),j&&(0,H.tZ)(S.Z,{onHide:Y,onSave:W,show:!0,slice:j}),(0,H.tZ)(y.Z,{title:(0,o.t)("Please confirm"),description:(0,o.t)("Are you sure you want to delete the selected charts?"),onConfirm:function(e){s.Z.delete({endpoint:`/api/v1/chart/?q=${u().encode(e.map((({id:e})=>e)))}`}).then((({json:e={}})=>{R(),a(e.message)}),(0,h.v$)((e=>t((0,o.t)("There was an issue deleting the selected charts: %s",e)))))}},(e=>{const t=[];return ie&&t.push({key:"delete",name:(0,o.t)("Delete"),type:"danger",onSelect:e}),oe&&t.push({key:"export",name:(0,o.t)("Export"),type:"primary",onSelect:se}),(0,H.tZ)(v.Z,{bulkActions:t,bulkSelectEnabled:c,cardSortSelectOptions:pe,className:"chart-list-view",columns:de,count:i,data:n,disableBulkSelect:L,fetchData:O,filters:ue,initialSort:ne,loading:l,pageSize:25,renderCard:me,showThumbnails:ae?ae.thumbnails:(0,p.cr)(m.T.THUMBNAILS),defaultViewMode:(0,p.cr)(m.T.LISTVIEWS_DEFAULT_CARD_VIEW)?"card":"table"})})),(0,H.tZ)(C.Z,{resourceName:"chart",resourceLabel:(0,o.t)("chart"),passwordsNeededMessage:F,confirmOverwriteMessage:M,addDangerToast:t,addSuccessToast:a,onModelImport:()=>{G(!1),R(),a((0,o.t)("Chart imported"))},show:X,onHide:()=>{G(!1)},passwordFields:J,setPasswordFields:Q}),ee&&(0,H.tZ)(w.Z,null))}))}}]);
//# sourceMappingURL=0bf096021a20371c310d.chunk.js.map
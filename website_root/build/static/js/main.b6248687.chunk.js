(this.webpackJsonpwebsite=this.webpackJsonpwebsite||[]).push([[0],{119:function(e,t,n){e.exports=n(235)},133:function(e,t){},138:function(e,t){},140:function(e,t){},152:function(e,t){},154:function(e,t){},179:function(e,t){},181:function(e,t){},182:function(e,t){},187:function(e,t){},189:function(e,t){},195:function(e,t){},197:function(e,t){},216:function(e,t){},228:function(e,t){},231:function(e,t){},235:function(e,t,n){"use strict";n.r(t);var a=n(1),l=n.n(a),r=n(117),c=n.n(r),o=n(241),i=n(238),u=n(239),d=n(118),s=n(242),m=n(240),f=n(243);var E=()=>{const[e,t]=Object(a.useState)(null),[n,r]=Object(a.useState)(null),[c,E]=Object(a.useState)("");return l.a.createElement(i.a,null,l.a.createElement(u.a,{className:"mt-5 mb-3"},l.a.createElement(d.a,{xs:6},l.a.createElement(s.a.Group,null,l.a.createElement(s.a.Label,null,"Photo 1"),l.a.createElement(s.a.Control,{id:"file1",type:"file",onChange:e=>{E(""),t(e.target.files[0]),null==e.target.files[0]?document.getElementById("delButton1").hidden=!0:document.getElementById("delButton1").hidden=!1}})),e&&l.a.createElement(m.a,{className:"mt-2",src:URL.createObjectURL(e),alt:"File 1 Preview",fluid:!0,style:{border:"2px solid #ddd",borderRadius:"8px",maxHeight:"150px",minHeight:"150px"}})),l.a.createElement(d.a,{xs:6,className:"justify-content-center"},l.a.createElement(s.a.Group,null,l.a.createElement(s.a.Label,null,"Photo 2"),l.a.createElement(s.a.Control,{type:"file",id:"file1",onChange:e=>{E(""),r(e.target.files[0]),null==e.target.files[0]?document.getElementById("delButton2").hidden=!0:document.getElementById("delButton2").hidden=!1}})),n&&l.a.createElement(m.a,{className:"mt-2 ",src:URL.createObjectURL(n),alt:"File 2 Preview",fluid:!0,style:{border:"2px solid #ddd",borderRadius:"8px",maxHeight:"150px",minHeight:"150px"}}))),l.a.createElement(u.a,{className:"mt-2 mb-2"},l.a.createElement(d.a,{xs:6},l.a.createElement(f.a,{variant:"danger",hidden:"true",id:"delButton1",onClick:e=>{E(""),t(null),document.getElementById("file1").value=null,document.getElementById("delButton1").hidden=!0}},"X")),l.a.createElement(d.a,{xs:6},l.a.createElement(f.a,{variant:"danger",hidden:"true",id:"delButton2",onClick:e=>{E(""),r(null),document.getElementById("file2").value=null,document.getElementById("delButton2").hidden=!0}},"X"))),l.a.createElement(u.a,{className:"justify-content-center"},l.a.createElement(f.a,{variant:"primary",onClick:()=>{if(!e||!n)return void E("Please select files for both inputs");const t=e=>new Promise((t,n)=>{const a=new FileReader;a.onloadend=()=>t(a.result.split(",")[1]),a.onerror=n,a.readAsDataURL(e)});(async()=>{try{const a=await t(e),l={modelId:"sift",image1:a,image2:await t(n)},r=await o.a.post("https://lubomyr-ai-api-b1f15885f038.herokuapp.com/ai/predict",l);E(r.request.responseText)}catch(a){E("An error has occured!"),console.error("Error uploading files:",a)}})()}},"Upload")),l.a.createElement(u.a,{className:"mt-3 justify-content-center"},l.a.createElement("p",null,"Result: ",c)))};var p=function(){return l.a.createElement("div",null,l.a.createElement(E,null))};n(132).config();c.a.createRoot(document.getElementById("root")).render(l.a.createElement(p,null))}},[[119,1,2]]]);
//# sourceMappingURL=main.b6248687.chunk.js.map
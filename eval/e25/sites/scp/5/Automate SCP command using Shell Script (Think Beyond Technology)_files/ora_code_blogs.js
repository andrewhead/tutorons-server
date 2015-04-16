function s_setAccount(){var sa=["oracledevall","ocom","en-us"];if(location.href.indexOf("-stage")!=-1||location.href.indexOf("-dev")!=-1||location.href.indexOf("localhost")!=-1){sa[0]="oracledevblogs1,oracledevall";
sa[1]="blogs";sa[2]="en-us";}else{sa[0]="oracleblogs,oracleglobal";sa[1]="blogs";
sa[2]="en-us";}return sa;}function s_prePlugins(s){s.prop10="Not Set";findStart='">';
findEnd="</a>";if(location.href=="http://blogs.oracle.com/"){s.prop10="Blogs Home Page";
}if(document.getElementById("jumbotron").getElementsByTagName("h5")[0]!=null){var startTitle=document.getElementById("jumbotron").getElementsByTagName("h5")[0].innerHTML.toLowerCase().indexOf(findStart)+findStart.length;
var endTitle=document.getElementById("jumbotron").getElementsByTagName("h5")[0].innerHTML.toLowerCase().indexOf(findEnd)-startTitle;
if(startTitle>0&&endTitle>0){s.prop10=document.getElementById("jumbotron").getElementsByTagName("h5")[0].innerHTML.substr(startTitle,endTitle);
}}}
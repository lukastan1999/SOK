

var lastSelectedVertex = '';

function selectVertex(vertex){

    deSelectOnComplexView(lastSelectedVertex)
    deSelectOnSimpleView(lastSelectedVertex);
    deSelectOnTreeView(lastSelectedVertex);

    selectOnTreeView(vertex);
    selectOnSimpleView(vertex);
    selectOnComplexView(vertex);

    lastSelectedVertex = vertex;
}
function deSelectVertex(vertex){

    deSelectOnComplexView(lastSelectedVertex)
    deSelectOnSimpleView(lastSelectedVertex);
    deSelectOnTreeView(lastSelectedVertex);

}

function selectOnSimpleView(vertex){
    try{
    document.getElementById('cvor_'+vertex).getElementsByTagName('circle')[0].style.fill = 'red';
    }catch(error){
        console.log('nespela selekcija na simple view');
    }
}


function deSelectOnSimpleView(vertex){

    try{
    document.getElementById('cvor_'+vertex).getElementsByTagName('circle')[0].style.fill = 'url(#gradientVertex)';
    }
    catch(error){
        console.log('nespela deselekcija na simple view');
    }
}

function selectOnTreeView(vertex){
    try{
    document.getElementById(vertex).style.color = 'red';
    document.getElementById(vertex).getElementsByTagName('ul')[0].style.color = 'black';
    }
    catch(error){
        console.log('nespela selekcija na tree view');
    }
}


function deSelectOnTreeView(vertex){

    try{
        document.getElementById(vertex).style.color = 'black';
        document.getElementById(vertex).getElementsByTagName('ul')[0].style.color = 'black';
    }
    catch(error){
        console.log('neuspela deselekcija na tree view');
    }
}

function selectOnComplexView(vertex){

    try{
        document.getElementById('cvor'+vertex).getElementsByTagName('rect')[0].style.fill = 'red';
    }
    catch(error){
        console.log('neuspela selekcija na complex view');
    }


}
function deSelectOnComplexView(vertex){

    try{
        document.getElementById('cvor'+vertex).getElementsByTagName('rect')[0].style.fill = 'white';
    }
    catch(error){
        console.log('nuespela deselekcija na complex view');
    }


}
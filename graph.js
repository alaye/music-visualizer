// Artist graph class
function ArtistNode(name, edges) {
    this.name = name
    this.edges = edges
    this.circle = null
    this.x = null
    this.y = null
    // this.html = d3.
}

// function ArtistGraph(artists) {
//     this.nodes = [];
//     function node(name, edges) {
// 	this.name = name;
// 	this.edges = edges;
// 	// this.html = d3.
//     }
//     artists.foreach(function(a) {
// 	// TEMP do properly when server is updated
// 	nodes.push(a);
//     })
// }

// Declerations and onload
var graph
var circles
window.onload = function() {
    var ArtistList = [];
    ArtistList['Kanye'] = new ArtistNode('Kanye', ['Kendrick'])
    ArtistList['Kendrick'] = new ArtistNode('Kendrick', ['Kanye'])
    ArtistList['DJ Khaled'] = new ArtistNode('DJ Khaled', ['Kanye'])
    var svg = d3.select('svg')
    for(var name in ArtistList) {
	ArtistList[name].x = Math.random()*400
	ArtistList[name].y = Math.random()*400
    }
    // Draw the lines
    var lineFunc = d3.line()
    var lines = []
    for(var name in ArtistList) {
	var firstArtist = ArtistList[name]
	if(!lines[name])
	    lines[name] = []
	for(var edge in firstArtist.edges) {
	    var other = firstArtist.edges[edge]
	    if(lines[other] && lines[other][name])
		continue;
	    lines[name][other] = true
	    var otherArtist = ArtistList[other]
	    var points = [[otherArtist.x,otherArtist.y],
			  [firstArtist.x,firstArtist.y]]
	    svg.append('path')
		.attr('d', lineFunc(points))
		.attr('stroke', 'black')
		.attr('stroke-width', 2)
		.attr('fill', 'none')
	}
    }

    // Draw circles
    for(var name in ArtistList) {
	var ele = ArtistList[name]
	var dx = ArtistList[name].x,dy = ArtistList[name].y
	var group = svg.append('g').attr('id',ele.name);
	var text = group.append('text')
	    .attr('dy', dy)
	    .attr('dx', dx)
	    .html(ele.name)
	ele.circle = group.append('circle')
	    .attr('r',text.node().getBBox().width/2)
	    .style('fill', 'steelblue')
	    .attr('cy', dy)
	    .attr('cx', dx)
	group.append('text')
	    .attr('dy', dy)
	    .attr('dx', dx-text.node().getBBox().width/2)
	    .html(ele.name)
	text.remove()
    }
    circle = d3.selectAll('circle')
}

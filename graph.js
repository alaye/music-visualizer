// Artist graph class
function ArtistNode(name, edges) {
    this.name = name;
    this.edges = edges;
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
    var ArtistList = [new ArtistNode('Kayne', [1,2,3]), new ArtistNode('Kendrick', [1,2,3])]
    var svg = d3.select('svg')
    ArtistList.forEach(function(ele, n) {
	var group = svg.append('g');
	var text = group.append('text')
	    .attr('dy', 60)
	    .attr('dx', 55*n)
	    .html(ele.name);
	group.append('circle')
	    .attr('r',text.node().getBBox().width/2)
	    .style('fill', 'steelblue')
	    .attr('cy', 60)
	    .attr('cx', 55*n+text.node().getBBox().width/2)
	group.append('text')
	    .attr('dy', 60)
	    .attr('dx', 55*n)
	    .html(ele.name);
	text.remove();
    })
    circle = d3.selectAll('circle');
}

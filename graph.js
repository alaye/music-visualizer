// Artist graph class
function ArtistNode(name, edges) {
    this.name = name
    this.edges = edges
    this.circle = null
    this.x = null
    this.y = null
    this.lines = []
    this.text = null
    this.update = function(x,y) {
	this.x = x
	this.y = y
	this.lines.forEach(function(line) {
	    var other = ArtistList[line.other]
	    line.points = [[x,y],
			   [other.x, other.y]]
	    var lineFunc = d3.line()
	    line.path.attr('d', lineFunc(line.points))
	})
	this.text.attr('dx', x-this.radius+10)
	    .attr('dy', y)
	this.circle.attr('cx',x)
	    .attr('cy', y)
    }
}

// Declerations and onload
var graph
var circles
var ArtistList = []
window.onload = function() {
    artist = sessionStorage.getItem('artist')
    if(!artist)
	window.location = 'https://alaye.github.io/music-visualizer/'
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
	if(this.readyState == 4 && this.status == 200) {
	    console.log(this.responseText)
	    var list = JSON.parse(this.responseText)
	    for(var name in list) {
		ArtistList[name] = new ArtistNode(name, list[name])
	    }
	    setup()
	} else if(this.readyState == 4 && this.status != 200) {
	    alert("There was an error. status: " +this.status +" state: " + this.readyState)
	    alert(this.responseText)
	    window.location = 'https://alaye.github.io/music-visualizer/'
	}
    }
    httpRequest.open('GET', 'http://10.104.246.185:5000/relations/'+artist, true)
    // httpRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    //httpRequest.setRequestHeader("Access-Control-Allow-Origin", "null");
    // httpRequest.withCredentials = false;
    httpRequest.send()
}

function setup() {
    // ArtistList['Kanye West'] = new ArtistNode('Kanye West', ['Kendrick Lamar'])
    // ArtistList['Kendrick Lamar'] = new ArtistNode('Kendrick Lamar', ['Kanye West', 'DJ Khaled'])
    // ArtistList['DJ Khaled'] = new ArtistNode('DJ Khaled', ['Kanye West'])
    // ArtistList['The Beatles'] = new ArtistNode('The Beatles', ['Kanye West'])
    var svg = d3.select('svg')
    svg.append('circle')
    for(var name in ArtistList) {
	var dis = 20, range = 800
	ArtistList[name].x = Math.random()*1000
	ArtistList[name].y = Math.random()*range
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
	    var otherArtist = ArtistList[other]
	    var points = [[otherArtist.x,otherArtist.y],
			  [firstArtist.x,firstArtist.y]]
	    lines[name][other] = {points: points}
	    lines[name][other].path = svg.append('path')
	    lines[name][other].path.attr('d', lineFunc(points))
		.attr('stroke', 'black')
		.attr('stroke-width', 2)
		.attr('fill', 'none')
	    firstArtist.lines.push(lines[name][other])
	    firstArtist.lines[firstArtist.lines.length-1].other = other
	    // otherArtist.lines.push(lines[name][other])
	    // otherArtist.lines[otherArtist.lines.length-1].other = name
	}
    }

    // Draw circles and set up collison nodes
    var color = ['red', 'steelblue', 'orange'],
	i = 0 //Math.floor(Math.random*20)
    for(var name in ArtistList) {
	var ele = ArtistList[name]
	var dx = ArtistList[name].x,dy = ArtistList[name].y
	var group = svg.append('g').attr('id',ele.name);
	var text = group.append('text')
	    .attr('dy', dy)
	    .attr('dx', dx)
	    .html(ele.name)
	ele.circle = group.append('circle')
	    .attr('r',text.node().getBBox().width/2 + 5)
	    .style('fill', color[i++ % 3])
	    .attr('cy', dy)
	    .attr('cx', dx)
	ele.radius = text.node().getBBox().width/2 + 10
	ele.text = group.append('text')
	    .attr('dy', dy)
	    .attr('dx', dx-text.node().getBBox().width/2)
	    .html(ele.name)
	text.remove()
    }
    circles = d3.selectAll('circle')
    var radData = [{radius: 10, fixed: true}]
    for(name in ArtistList) {
	radData.push({radius: ArtistList[name].radius, x: ArtistList[name].x, y: ArtistList[name].y, ref: ArtistList[name]})
    }
    circles.data(radData)
    var nodes = circles.data()
    var root = nodes[0]
    // circles.data(radData.splice(1)		)
    // make sure the circles don't collide
    var force = d3.forceSimulation(nodes)
	.force('collision', d3.forceCollide().radius(function(node,index){return node.radius}))
	.force('charge', d3.forceManyBody().strength(function(n,i){return i==0? 10: 0}))
    force.on("tick", function(e) {
        var //q = d3.quadtree(nodes),
    	i = 0,
    	n = nodes.length;

        //while (++i < n) q.visit(collide(nodes[i]));

        circles.attr("cy", function(d) {
	    // sneaky use this to update the lines and text
	    // if(!d.fixed)
	    if(i++!=0)
		d.ref.update(d.x,d.y)
	    return d.y; });
    })

    d3.select('svg').on("mousemove", function() {
        var p1 = d3.mouse(this);
        root.x = p1[0];
        root.y = p1[1];
	force.alpha(1).restart()
    });

    // circles.on('mousedown', function() {
    // 	circles.on('mousemove',function(){
    // 	    var pointer = d3.mouse(this)
    // 	    var data = d3.select(this).data()[0]
    // 	    data.ref.update(pointer[0],pointer[1])
    // 	    for(name in data.ref.edges) {
    // 		var other = ArtistList[name]
    // 		other.update(other.x,other.y)
    // 	    }
    // 	})
    // 	circles.on('mouseup', function() {
    // 	    circles('mousemove',null)
    // 	    circles('mouseup',null)
    // 	})
    // })
}

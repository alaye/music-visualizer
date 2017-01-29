window.onload = function() {
    var width = 960,
	height = 500;

    var nodes = d3.range(20).map(function() { return {radius: Math.random() * 24 + 10}}),
	root = nodes[0],
	color = ['red', 'steelblue', 'orange'];
    
    root.radius = 0;
    root.fixed = true;

    var force = d3.forceSimulation(nodes)
	.force('collision', d3.forceCollide().radius(function(node,index){return node.radius}))
	.force('charge', d3.forceManyBody().strength(function(n,i){return i==0? 20: 10}))

    var svg = d3.select("svg")
	.attr("width", width)
	.attr("height", height);

    svg.selectAll("circle")
	.data(nodes.slice(1))
	.enter().append("circle")
	.attr("r", function(d) { return d.radius; })
	.style("fill", function(d, i) { return color[i % 3]; });
    
    d3.selectAll('circle').data().forEach(function(ele,n){
	ele.x = width/2 -100+Math.random()*200
	ele.y = height/2 - 100+Math.random()*200
    })

    force.on("tick", function(e) {
        var //q = d3.quadtree(nodes),
    	i = 0,
    	n = nodes.length;

        //while (++i < n) q.visit(collide(nodes[i]));

        svg.selectAll("circle")
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });

    });

    svg.on("mousemove", function() {
        var p1 = d3.mouse(this);
        root.x = p1[0];
        root.y = p1[1];
	force.alpha(1).restart()
    });
}

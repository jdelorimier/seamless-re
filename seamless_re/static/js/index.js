(async() => {
    let response = await fetch(`${window.origin}/get-graph`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify("Get data"),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    });

    var svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height");

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.id; }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    let responseString = await response.json();
    let responseJSON = JSON.parse(responseString);

    var g = svg.append("g")
        .attr("class", "everything");

    var link = g.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(responseJSON.links)
        .enter().append("line");

    var node = g.append("g")
        .attr("id", "circleCustomTooltip") // added
        .attr("class", "nodes")
        .selectAll("circle")
        .data(responseJSON.nodes)
        .enter().append("circle")
        .attr("r", 5.0)
        .attr("fill", "darkgray")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));
    
    var tooltip = d3.select("body")
       .append("div")
       .attr('class','tooltipdiv')
       .style("position", "absolute")
       .style("z-index", "10")
       .style("visibility", "hidden")
        // added from https://www.d3-graph-gallery.com/graph/interactivity_tooltip.html
       .style("background-color", "white")
       .style("border", "solid")
       .style("border-width", "1px")
       .style("border-radius", "5px")
       .style("padding", "10px")
       .html("<p>I'm a tooltip written in HTML</p><img src='https://github.com/holtzy/D3-graph-gallery/blob/master/img/section/ArcSmal.png?raw=true'></img><br>Fancy<br><span style='font-size: 40px;'>Isn't it?</span>");
        // end
    //    .text("node tooltip");

    // kinda works
    // node.on("click", function(d){
    //     d3.select(this).classed('hovernode', true)
    //     return tooltip.style("visibility", "visible").html();})
    //     .on("mousemove", function(){return tooltip.style("top",
    //         (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");})
    //     .on("mouseout", function(){
    //     d3.select(this).classed('hovernode', false)
    //     return tooltip.style("visibility", "hidden");});

    // http://jsfiddle.net/cyril123/9u9a30y4/9/
    node.on("mouseover", function(d) {
        console.log('mouseover: ' + d3.select(this));
        // var xPosition = parseFloat(d3.select(this).attr("cx")) + scatter_radius;
        // var yPosition = parseFloat(d3.select(this).attr("cy"));
        //console.log(xPosition + ',' + yPosition);
        console.log('1. ' + d3.select(this));
        //Update the tooltip position and value

        d3.select("#tooltip_svg_01")
            .style("left", (d3.event.pageX+10)+"px")
            .style("top", (d3.event.pageY-10)+"px");
        d3.select("#tooltip_header")
            .text(d['name']);
        d3.select("#value_tt_01")
            .text("Type: " + d['type']);
        d3.select('#link_tt_01')
            .attr("href", d['path'])
            .text("Link to filing")
            // .text(d['id'] + ',' + d['id']);
   
        //Show the tooltip
        d3.select("#tooltip_svg_01").style('opacity', 1);
   })    

    node.append("title")
        .text(function(d) { return d.name; });
    
    node.append("p")
        .text(function(d) { return d.id; })
    
    node.append("p")
        .text(function(d) { return d.path; })
    
    // https://stackoverflow.com/questions/49357718/both-single-and-double-click-on-a-node-in-d3-force-directed-graph
    // node.on("click",function(d){ return tooltip.style("visibility", "visible").text(d.name); })

    simulation
        .nodes(responseJSON.nodes)
        .on("tick", ticked);

    simulation
        .force("link")
        .links(responseJSON.links);
    var zoom_handler = d3.zoom()
        .on("zoom", zoom_actions);

    zoom_handler(svg);

    function zoom_actions() {
        g.attr("transform", d3.event.transform)
    }

    function ticked() {
        link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
    }

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

})();